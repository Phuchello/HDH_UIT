/**
 * HDH_UIT V2 — Deterministic Local-First Learning Runtime
 * Learning Architecture V1.2 Implementation
 *
 * Features implemented:
 *  - SM-2 Project Heuristic scheduler (HARD != AGAIN invariant)
 *  - M0-M3 mastery state machine (M3 only from TransferProblem evidence)
 *  - Learn / Review / Reference mode switch (persisted)
 *  - Legacy localStorage migration (hdh_card_<id> -> new schema)
 *  - Exception-safe localStorage (quota, JSON, unavailable)
 *  - Progressive disclosure: hint / keypoints / answer reveal buttons
 *  - AGAIN / HARD / GOOD / EASY rating buttons
 *  - Review mode: only due/weak cards visible
 *  - Backup / Restore (export/import versioned JSON)
 *  - ARIA + keyboard navigation
 */

(function () {
  'use strict';

  // ============================================================
  // CONSTANTS
  // ============================================================
  var SCHEMA_VERSION = 1;
  var STORAGE_KEYS = {
    mastery:   'hdh_mastery_v1',
    scheduler: 'hdh_spaced_scheduler_v1',
    drafts:    'hdh_practice_drafts_v1',
    mistakes:  'hdh_mistakes_log_v1',
    uiMode:    'hdh_ui_mode',
    theme:     'hdh_theme',
  };

  // ============================================================
  // SAFE localStorage WRAPPER
  // All reads/writes are wrapped to never throw.
  // ============================================================
  var Store = {
    _available: null,

    available: function () {
      if (this._available !== null) return this._available;
      try {
        var t = '__hdh_test__';
        localStorage.setItem(t, '1');
        localStorage.removeItem(t);
        this._available = true;
      } catch (_) {
        this._available = false;
      }
      return this._available;
    },

    get: function (key, fallback) {
      if (fallback === undefined) fallback = null;
      if (!this.available()) return fallback;
      try {
        var raw = localStorage.getItem(key);
        if (raw === null) return fallback;
        return JSON.parse(raw);
      } catch (_) {
        return fallback;
      }
    },

    set: function (key, value) {
      if (!this.available()) return false;
      try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
      } catch (_) {
        // Quota exceeded or SecurityError: ignore, content still works.
        return false;
      }
    },

    remove: function (key) {
      if (!this.available()) return;
      try { localStorage.removeItem(key); } catch (_) {}
    },

    keys: function () {
      if (!this.available()) return [];
      try {
        return Object.keys(localStorage);
      } catch (_) {
        return [];
      }
    },
  };

  // ============================================================
  // SM-2 PROJECT HEURISTIC SCHEDULER
  // Pure function -- inject `today` (YYYY-MM-DD) for testability.
  // Invariant: HARD is a SUCCESSFUL recall (reps++, interval grows).
  //            AGAIN is FAILURE (reps=0, interval=1, lapses++).
  // ============================================================
  var Scheduler = {
    /**
     * @param {object} prev   { reps, ef, interval_days, due_timestamp, lapses }
     * @param {string} rating 'AGAIN' | 'HARD' | 'GOOD' | 'EASY'
     * @param {string} today  YYYY-MM-DD
     * @returns {object} new state (same shape)
     */
    schedule: function (prev, rating, today) {
      var ef       = Math.min(2.8, Math.max(1.3, prev.ef !== undefined ? prev.ef : 2.5));
      var reps     = prev.reps !== undefined ? prev.reps : 0;
      var interval = prev.interval_days !== undefined ? prev.interval_days : 0;
      var lapses   = prev.lapses !== undefined ? prev.lapses : 0;

      var newReps, newEf, newInterval, newLapses;

      if (rating === 'AGAIN') {
        // Recall failure: reset reps, shrink EF, increment lapses
        newReps     = 0;
        newInterval = 1;
        newEf       = Math.max(1.3, ef - 0.20);
        newLapses   = lapses + 1;
      } else if (rating === 'HARD') {
        // Successful but hard: DO NOT reset reps (HARD != AGAIN invariant)
        newReps   = reps + 1;
        newLapses = lapses;
        newEf     = Math.max(1.3, ef - 0.15);
        if (newReps <= 1) {
          newInterval = 1;
        } else {
          newInterval = Math.max(interval + 1, Math.round(interval * 1.2));
        }
      } else if (rating === 'GOOD') {
        newReps   = reps + 1;
        newLapses = lapses;
        newEf     = ef; // unchanged
        if (newReps === 1)      newInterval = 1;
        else if (newReps === 2) newInterval = 3;
        else                    newInterval = Math.round(interval * ef);
      } else if (rating === 'EASY') {
        newReps   = reps + 1;
        newLapses = lapses;
        newEf     = Math.min(2.8, ef + 0.15);
        if (newReps === 1)      newInterval = 2;
        else if (newReps === 2) newInterval = 4;
        else                    newInterval = Math.round(interval * ef * 1.3);
      } else {
        // Unknown rating: no-op
        return Object.assign({}, prev);
      }

      // Avoid DST-sensitive drift: compute due date via whole calendar days
      var newDue = this._addDays(today, newInterval);

      return {
        reps:          newReps,
        ef:            Math.round(newEf * 1000) / 1000,
        interval_days: newInterval,
        due_timestamp: newDue,
        lapses:        newLapses,
      };
    },

    /** YYYY-MM-DD -> UTC midnight ms (avoids local-timezone DST drift) */
    _dateToMs: function (s) {
      var parts = s.split('-');
      return Date.UTC(+parts[0], +parts[1] - 1, +parts[2]);
    },

    /** Returns UTC midnight ms for (today + days) -- no DST drift */
    _addDays: function (today, days) {
      return this._dateToMs(today) + days * 86400000;
    },

    today: function () {
      var now = new Date();
      var y = now.getFullYear();
      var m = String(now.getMonth() + 1).padStart('0', 2);
      var d = String(now.getDate()).padStart('0', 2);
      // Use standard padStart signature
      m = (now.getMonth() + 1 < 10 ? '0' : '') + (now.getMonth() + 1);
      d = (now.getDate() < 10 ? '0' : '') + now.getDate();
      return y + '-' + m + '-' + d;
    },

    isDue: function (dueTimestamp) {
      if (!dueTimestamp) return true; // never reviewed = always due
      return dueTimestamp <= this._dateToMs(this.today());
    },
  };

  // ============================================================
  // MASTERY STATE STORE
  // M0 -> M1 via first non-AGAIN rating
  // M1 -> M2 via RecallCheckpoint rubric >=80% (SELF_ASSESSED)
  // M2 -> M3 via TransferProblem only (NOT by rating)
  // ============================================================
  var MasteryStore = {
    _cache: null,

    _load: function () {
      if (this._cache) return this._cache;
      this._cache = Store.get(STORAGE_KEYS.mastery, {});
      return this._cache;
    },

    _save: function () {
      Store.set(STORAGE_KEYS.mastery, this._cache);
    },

    _defaultRecord: function (conceptId) {
      return {
        schema_version: SCHEMA_VERSION,
        concept_id: conceptId,
        mastery_state: 'M0',
        mastery_evidence: {
          recall_passed: false,
          transfer_passed: false,
          verification_mode: 'SELF_ASSESSED',
        },
        review_schedule: {
          reps: 0,
          ef: 2.5,
          interval_days: 0,
          due_timestamp: null,
          lapses: 0,
        },
        review_rating_history: [],
        mistake_history: [],
      };
    },

    get: function (conceptId) {
      var data = this._load();
      return data[conceptId] || this._defaultRecord(conceptId);
    },

    /** Record a rating and advance the scheduler.
     *  Rating CAN: M0->M1 (first non-AGAIN), demote M0/M1 on AGAIN.
     *  Rating CANNOT: grant M2 or M3.
     */
    recordRating: function (conceptId, rating) {
      var data = this._load();
      if (!data[conceptId]) data[conceptId] = this._defaultRecord(conceptId);
      var rec = data[conceptId];
      rec.review_schedule = Scheduler.schedule(rec.review_schedule, rating, Scheduler.today());

      rec.review_rating_history.push({ timestamp: Date.now(), rating: rating });
      if (rec.review_rating_history.length > 50) {
        rec.review_rating_history = rec.review_rating_history.slice(-50);
      }

      if (rating === 'AGAIN') {
        if (rec.mastery_state === 'M0' || rec.mastery_state === 'M1') {
          rec.mastery_state = 'M0';
        }
      } else {
        if (rec.mastery_state === 'M0') rec.mastery_state = 'M1';
      }

      this._save();
      return rec;
    },

    /** RecallCheckpoint self-assessed evidence: M0/M1 -> M2 if passed+rubric>=80 */
    recordRecallEvidence: function (conceptId, passed, rubricPct) {
      var data = this._load();
      if (!data[conceptId]) data[conceptId] = this._defaultRecord(conceptId);
      var rec = data[conceptId];
      rec.mastery_evidence.recall_passed = passed;
      rec.mastery_evidence.verification_mode = 'SELF_ASSESSED';
      if (passed && rubricPct >= 80 && rec.mastery_state !== 'M3') {
        rec.mastery_state = 'M2';
        rec.mastery_evidence.recall_timestamp = Date.now();
      } else if (!passed && rec.mastery_state === 'M1') {
        rec.mastery_state = 'M0';
      }
      this._save();
      return rec;
    },

    /** TransferProblem evidence: M2 -> M3 ONLY path */
    recordTransferEvidence: function (conceptId, passed) {
      var data = this._load();
      if (!data[conceptId]) data[conceptId] = this._defaultRecord(conceptId);
      var rec = data[conceptId];
      rec.mastery_evidence.transfer_passed = passed;
      if (passed && rec.mastery_state === 'M2') rec.mastery_state = 'M3';
      this._save();
      return rec;
    },

    isDue: function (conceptId) {
      return Scheduler.isDue(this.get(conceptId).review_schedule.due_timestamp);
    },

    isWeak: function (conceptId) {
      var s = this.get(conceptId).mastery_state;
      return s === 'M0' || s === 'M1';
    },
  };

  // ============================================================
  // LEGACY MIGRATION
  // hdh_card_<id> { remembered: bool } -> new mastery schema
  // One-time, idempotent, exception-safe.
  // ============================================================
  var LegacyMigration = {
    FLAG: 'hdh_migration_v1_done',

    run: function () {
      if (Store.get(this.FLAG, false)) return;
      var keys = Store.keys();
      for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if (key.indexOf('hdh_card_') !== 0) continue;
        try {
          var old = Store.get(key, null);
          if (!old || typeof old.remembered !== 'boolean') continue;
          var cid = key.replace('hdh_card_', '');
          var data = Store.get(STORAGE_KEYS.mastery, {});
          if (!data[cid]) {
            var rec = MasteryStore._defaultRecord(cid);
            if (old.remembered) {
              rec.mastery_state = 'M1';
              rec.mastery_evidence.verification_mode = 'LEGACY_SELF_REPORT';
            }
            data[cid] = rec;
            Store.set(STORAGE_KEYS.mastery, data);
            MasteryStore._cache = null;
          }
        } catch (_) {}
      }
      Store.set(this.FLAG, true);
    },
  };

  // ============================================================
  // BACKUP / RESTORE
  // ============================================================
  var BackupRestore = {
    exportData: function () {
      var payload = {
        backup_version: SCHEMA_VERSION,
        exported_at: new Date().toISOString(),
        mastery:   Store.get(STORAGE_KEYS.mastery, {}),
        scheduler: Store.get(STORAGE_KEYS.scheduler, {}),
        drafts:    Store.get(STORAGE_KEYS.drafts, {}),
        mistakes:  Store.get(STORAGE_KEYS.mistakes, {}),
      };
      var blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'hdh_learning_backup_' + Scheduler.today() + '.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    },

    importData: function (jsonText) {
      try {
        var payload = JSON.parse(jsonText);
        if (!payload.backup_version) throw new Error('Invalid backup format');
        if (payload.mastery)   Store.set(STORAGE_KEYS.mastery, payload.mastery);
        if (payload.scheduler) Store.set(STORAGE_KEYS.scheduler, payload.scheduler);
        if (payload.drafts)    Store.set(STORAGE_KEYS.drafts, payload.drafts);
        if (payload.mistakes)  Store.set(STORAGE_KEYS.mistakes, payload.mistakes);
        MasteryStore._cache = null;
        return { ok: true };
      } catch (e) {
        return { ok: false, error: String(e) };
      }
    },
  };

  // ============================================================
  // REVIEW QUEUE (Deterministic Priority Queue)
  // Priority ordering:
  //   1. Overdue AGAIN / M0 items (score 10)
  //   2. Overdue HARD / M1 items (score 20)
  //   3. Due today M2 items (score 30)
  //   4. Mistake-linked items (score 40)
  //   5. Pending TransferProblem checks (score 50)
  //   6. All other items (score 100)
  // ============================================================
  var ReviewQueue = {
    sortItems: function (items) {
      var self = this;
      return items.slice().sort(function (a, b) {
        var idA = a.concept_id || a.id || '';
        var idB = b.concept_id || b.id || '';
        var scoreA = self.getPriorityScore(idA);
        var scoreB = self.getPriorityScore(idB);
        if (scoreA !== scoreB) return scoreA - scoreB;
        return idA.localeCompare(idB);
      });
    },

    getPriorityScore: function (conceptId) {
      if (!conceptId) return 100;
      var rec = MasteryStore.get(conceptId);
      var due = Scheduler.isDue(rec.review_schedule.due_timestamp);
      var state = rec.mastery_state;
      var mistakes = rec.mistake_history ? rec.mistake_history.length : 0;

      if (due && state === 'M0') return 10;
      if (due && state === 'M1') return 20;
      if (due && state === 'M2') return 30;
      if (mistakes > 0) return 40;
      if (state === 'M2' && !rec.mastery_evidence.transfer_passed) return 50;
      return 100;
    },
  };

  // ============================================================
  // UI MODE MANAGER
  // ============================================================
  var UIModeManager = {
    MODES: ['learn', 'review', 'reference'],

    init: function () {
      var saved = Store.get(STORAGE_KEYS.uiMode, 'learn');
      var mode = this.MODES.indexOf(saved) >= 0 ? saved : 'learn';
      this.applyMode(mode);

      var self = this;
      document.querySelectorAll('.mode-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          self.applyMode(btn.getAttribute('data-mode'));
        });
      });
    },

    applyMode: function (mode) {
      if (this.MODES.indexOf(mode) < 0) mode = 'learn';
      Store.set(STORAGE_KEYS.uiMode, mode);
      document.documentElement.setAttribute('data-ui-mode', mode);

      document.querySelectorAll('.mode-btn').forEach(function (btn) {
        var active = btn.getAttribute('data-mode') === mode;
        btn.setAttribute('aria-pressed', String(active));
        if (active) btn.classList.add('mode-btn-active');
        else        btn.classList.remove('mode-btn-active');
      });

      // Reference mode: reveal all hidden sections
      if (mode === 'reference') {
        document.querySelectorAll('.card-section').forEach(function (sec) {
          sec.classList.add('visible');
          sec.setAttribute('aria-hidden', 'false');
        });
        document.querySelectorAll('.btn-hint, .btn-keypoints, .btn-answer').forEach(function (btn) {
          btn.setAttribute('aria-expanded', 'true');
        });
      } else {
        // Re-hide sections unless user explicitly opened them
        document.querySelectorAll('.card-section').forEach(function (sec) {
          if (!sec.dataset.userOpened) {
            sec.classList.remove('visible');
            sec.setAttribute('aria-hidden', 'true');
          }
        });
        document.querySelectorAll('.btn-hint, .btn-keypoints, .btn-answer').forEach(function (btn) {
          if (!btn.dataset.userExpanded) btn.setAttribute('aria-expanded', 'false');
        });
      }

      // Review mode: hide non-due/non-weak cards and reorder by priority
      if (mode === 'review') {
        var cards = Array.from(document.querySelectorAll('.study-card'));
        cards.forEach(function (card) {
          var cid = card.getAttribute('data-card-id');
          var show = MasteryStore.isDue(cid) || MasteryStore.isWeak(cid);
          if (show) card.classList.remove('review-hidden');
          else      card.classList.add('review-hidden');
        });
        if (cards.length > 1 && cards[0].parentNode) {
          var parent = cards[0].parentNode;
          var items = cards.map(function (c) {
            return { el: c, id: c.getAttribute('data-card-id') };
          });
          var sorted = ReviewQueue.sortItems(items);
          sorted.forEach(function (item) {
            parent.appendChild(item.el);
          });
        }
      } else {
        document.querySelectorAll('.study-card').forEach(function (card) {
          card.classList.remove('review-hidden');
        });
      }
    },
  };


  // ============================================================
  // STUDY CARD ENGINE V2
  // ============================================================
  var StudyCardEngine = {
    init: function () {
      var self = this;
      document.querySelectorAll('.study-card').forEach(function (card) {
        var cardId = card.getAttribute('data-card-id');
        self._restoreState(card, cardId);
        self._bindRevealButtons(card);
        self._bindRatingButtons(card, cardId);
        self._bindKeyboard(card);
      });
    },

    _restoreState: function (card, cardId) {
      if (!cardId) return;
      var rec = MasteryStore.get(cardId);
      this._applyMasteryUI(card, rec.mastery_state);
    },

    _applyMasteryUI: function (card, state) {
      card.setAttribute('data-mastery', state);
      var badge = card.querySelector('.card-mastery-badge');
      if (badge) badge.textContent = state;
    },

    _bindRevealButtons: function (card) {
      var pairs = [
        { btnSel: '.btn-hint',      secSel: '.card-hint' },
        { btnSel: '.btn-keypoints', secSel: '.card-keypoints' },
        { btnSel: '.btn-answer',    secSel: '.card-answer' },
      ];
      pairs.forEach(function (pair) {
        var btn = card.querySelector(pair.btnSel);
        var sec = card.querySelector(pair.secSel);
        if (!btn || !sec) return;
        btn.addEventListener('click', function () {
          var nowVisible = sec.classList.toggle('visible');
          sec.setAttribute('aria-hidden', String(!nowVisible));
          btn.setAttribute('aria-expanded', String(nowVisible));
          btn.dataset.userExpanded = nowVisible ? '1' : '';
          sec.dataset.userOpened  = nowVisible ? '1' : '';
        });
      });
    },

    _bindRatingButtons: function (card, cardId) {
      var self = this;
      card.querySelectorAll('.btn-rating').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (!cardId) return;
          var rating = btn.getAttribute('data-rating');
          var rec = MasteryStore.recordRating(cardId, rating);
          self._applyMasteryUI(card, rec.mastery_state);
          self._showRatingFeedback(card, rating, rec);
        });
      });
    },

    _showRatingFeedback: function (card, rating, rec) {
      var colors = { AGAIN: '#cf222e', HARD: '#e36209', GOOD: '#1a7f37', EASY: '#0969da' };
      var color = colors[rating] || '#0969da';
      card.style.transition = 'border-color 0.15s ease';
      card.style.borderLeftColor = color;
      var scratchpad = card.querySelector('.card-scratchpad');
      if (scratchpad) {
        scratchpad.placeholder = 'Ôn lại sau ' + rec.review_schedule.interval_days + ' ngày';
      }
      setTimeout(function () { card.style.borderLeftColor = ''; }, 800);
    },

    _bindKeyboard: function (card) {
      var ratingBtns = Array.from(card.querySelectorAll('.btn-rating'));
      ratingBtns.forEach(function (btn, i) {
        btn.addEventListener('keydown', function (e) {
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            ratingBtns[(i + 1) % ratingBtns.length].focus();
          } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            ratingBtns[(i - 1 + ratingBtns.length) % ratingBtns.length].focus();
          }
        });
      });
    },
  };

  // ============================================================
  // SUBJECTIVE PRACTICE ENGINE (enhanced, preserved)
  // ============================================================
  var SubjectivePracticeEngine = {
    init: function () {
      document.querySelectorAll('.subjective-practice').forEach(function (container) {
        var practiceId      = container.getAttribute('data-practice-id');
        var textarea        = container.querySelector('.practice-textarea');
        var compareBtn      = container.querySelector('.btn-compare');
        var rubricContainer = container.querySelector('.rubric-container');
        var checkboxes      = container.querySelectorAll('.rubric-check');
        var scoreDisplay    = container.querySelector('.current-score');
        var maxScore        = parseFloat(container.getAttribute('data-max-score') || '1.0');
        var stateKey        = 'hdh_practice_' + practiceId;

        var saveState = function () {
          if (!practiceId) return;
          Store.set(stateKey, {
            draft: textarea ? textarea.value : '',
            checked: Array.from(checkboxes).map(function (cb) { return cb.checked; }),
            rubricVisible: rubricContainer ? rubricContainer.classList.contains('visible') : false,
            score: scoreDisplay ? scoreDisplay.textContent : '0.00',
          });
        };

        if (practiceId && textarea) {
          var saved = Store.get(stateKey, null);
          var savedDraft = saved ? saved.draft : Store.get('hdh_draft_' + practiceId, null);
          if (savedDraft) textarea.value = savedDraft;
          if (saved) {
            checkboxes.forEach(function (cb, i) {
              cb.checked = !!(saved.checked && saved.checked[i]);
            });
            if (saved.rubricVisible && rubricContainer) rubricContainer.classList.add('visible');
          }
          textarea.addEventListener('input', saveState);
        }

        if (compareBtn && rubricContainer) {
          compareBtn.addEventListener('click', function () {
            rubricContainer.classList.toggle('visible');
            compareBtn.textContent = rubricContainer.classList.contains('visible')
              ? 'Ẩn Rubric tự kiểm tra'
              : 'So sánh với Rubric tự kiểm tra';
            saveState();
          });
        }

        var updateScore = function () {
          var score = 0;
          checkboxes.forEach(function (cb) {
            if (cb.checked) score += parseFloat(cb.getAttribute('data-weight') || '0');
          });
          score = Math.min(score, maxScore);
          if (scoreDisplay) scoreDisplay.textContent = score.toFixed(2);
          saveState();
        };
        updateScore();
        checkboxes.forEach(function (cb) { cb.addEventListener('change', updateScore); });
      });
    },
  };

  // ============================================================
  // KNOWLEDGE GRAPH (preserved)
  // ============================================================
  var KnowledgeGraph = {
    canvas: null, ctx: null, nodes: [], edges: [],

    init: function () {
      this.canvas = document.getElementById('knowledge-graph-canvas');
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      var depth = window.location.pathname.split('/').filter(Boolean).length
        - (window.location.pathname.endsWith('/') ? 0 : 1);
      var prefix = Array(Math.max(0, depth) + 1).join('../');
      var self = this;
      fetch(prefix + 'graph_data.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          self.nodes = data.nodes || [];
          self.edges = data.edges || [];
          self.nodes.forEach(function (n) { n.link = prefix + n.link; });
          self.draw();
        })
        .catch(function () { self.draw(); });
      this.resize();
      this.draw();
      this.canvas.addEventListener('click', function (e) {
        var rect = self.canvas.getBoundingClientRect();
        var mx = e.clientX - rect.left, my = e.clientY - rect.top;
        self.nodes.forEach(function (n) {
          var dx = n.x - mx, dy = n.y - my;
          if (Math.sqrt(dx * dx + dy * dy) <= n.r + 4 && n.link) {
            window.location.href = n.link;
          }
        });
      });
      window.addEventListener('resize', function () { self.resize(); self.draw(); });
    },

    resize: function () {
      if (!this.canvas) return;
      this.canvas.width = this.canvas.parentElement.clientWidth;
      this.canvas.height = 180;
    },

    draw: function () {
      if (!this.ctx || !this.canvas) return;
      var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.strokeStyle = isDark ? '#30363d' : '#e2e2da';
      this.ctx.lineWidth = 1.5;
      var self = this;
      this.edges.forEach(function (edge) {
        var n1 = self.nodes.find(function (n) { return n.id === edge.from; });
        var n2 = self.nodes.find(function (n) { return n.id === edge.to; });
        if (n1 && n2) {
          self.ctx.beginPath();
          self.ctx.moveTo(n1.x, n1.y);
          self.ctx.lineTo(n2.x, n2.y);
          self.ctx.stroke();
        }
      });
      this.nodes.forEach(function (node) {
        self.ctx.beginPath();
        self.ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
        self.ctx.fillStyle = node.color;
        self.ctx.fill();
        self.ctx.fillStyle = isDark ? '#e6edf3' : '#1f2328';
        self.ctx.font = '10px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
        self.ctx.textAlign = 'center';
        self.ctx.fillText(node.label, node.x, node.y + node.r + 12);
      });
    },
  };
  window.KnowledgeGraph = KnowledgeGraph;

  // ============================================================
  // THEME MANAGER
  // ============================================================
  var ThemeManager = {
    init: function () {
      var saved = Store.get(STORAGE_KEYS.theme, null)
        || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      this.setTheme(saved);
      var self = this;
      var btn = document.getElementById('theme-toggle-btn');
      if (btn) {
        btn.addEventListener('click', function () {
          var current = document.documentElement.getAttribute('data-theme') || 'light';
          self.setTheme(current === 'dark' ? 'light' : 'dark');
        });
      }
    },

    setTheme: function (theme) {
      document.documentElement.setAttribute('data-theme', theme);
      Store.set(STORAGE_KEYS.theme, theme);
      var icon = document.getElementById('theme-icon');
      if (icon) icon.textContent = theme === 'dark' ? '\u2600\uFE0F' : '\uD83C\uDF19';
      if (window.KnowledgeGraph) window.KnowledgeGraph.draw();
    },
  };

  // ============================================================
  // SEARCH ENGINE (preserved)
  // ============================================================
  var SearchEngine = {
    searchIndex: [],

    init: function () {
      var self = this;
      var modalOverlay = document.getElementById('search-modal-overlay');
      var triggerBtn   = document.getElementById('search-trigger-btn');
      var searchInput  = document.getElementById('search-input');
      var resultsList  = document.getElementById('search-results-list');

      var depth = window.location.pathname.split('/').filter(Boolean).length
        - (window.location.pathname.endsWith('/') ? 0 : 1);
      var prefix = Array(Math.max(0, depth) + 1).join('../');

      fetch(prefix + 'search_index.json')
        .then(function (r) { return r.json(); })
        .then(function (items) {
          self.searchIndex = items.map(function (item) {
            return Object.assign({}, item, { url: prefix + item.url });
          });
        })
        .catch(function () { self.searchIndex = []; });

      var open = function () {
        if (modalOverlay) {
          modalOverlay.classList.add('active');
          if (searchInput) {
            searchInput.focus();
            searchInput.value = '';
            self.renderResults(self.searchIndex, resultsList);
          }
        }
      };
      var close = function () { if (modalOverlay) modalOverlay.classList.remove('active'); };

      if (triggerBtn) triggerBtn.addEventListener('click', open);
      window.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); open(); }
        if (e.key === 'Escape') close();
      });
      if (modalOverlay) modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) close();
      });
      if (searchInput && resultsList) {
        searchInput.addEventListener('input', function (e) {
          var q = e.target.value.toLowerCase().trim();
          if (!q) { self.renderResults(self.searchIndex, resultsList); return; }
          var filtered = self.searchIndex.filter(function (item) {
            var texts = [item.title, item.summary, item.snippet]
              .concat(item.headings || [])
              .concat([item.searchable_text]);
            return texts.filter(Boolean).some(function (v) {
              return String(v).toLowerCase().indexOf(q) >= 0;
            });
          });
          self.renderResults(filtered, resultsList);
        });
      }
    },

    renderResults: function (items, container) {
      if (!container) return;
      container.innerHTML = '';
      if (!items.length) {
        container.innerHTML = '<li style="padding:1rem;text-align:center;color:var(--text-muted)">Kh\u00f4ng t\u00ecm th\u1ea5y k\u1ebft qu\u1ea3 ph\u00f9 h\u1ee3p.</li>';
        return;
      }
      items.forEach(function (item) {
        var li = document.createElement('li');
        li.innerHTML = '<a class="search-result-item" href="' + item.url + '">'
          + '<span class="search-result-title">' + item.title + '</span>'
          + '<span class="search-result-snippet">' + item.snippet + '</span>'
          + '</a>';
        container.appendChild(li);
      });
    },
  };

  // ============================================================
  // TOC SCROLL SPY (preserved)
  // ============================================================
  var TOCScrollSpy = {
    init: function () {
      var headings = document.querySelectorAll('.article-body h2, .article-body h3');
      var tocLinks  = document.querySelectorAll('.toc-link');
      if (!headings.length || !tocLinks.length) return;
      window.addEventListener('scroll', function () {
        var currentId = '';
        var scrollY = window.pageYOffset;
        headings.forEach(function (h) { if (scrollY >= h.offsetTop - 100) currentId = h.id; });
        tocLinks.forEach(function (link) {
          var active = link.getAttribute('href') === '#' + currentId;
          if (active) link.classList.add('active');
          else        link.classList.remove('active');
        });
      });
    },
  };

  // ============================================================
  // INIT
  // ============================================================
  document.addEventListener('DOMContentLoaded', function () {
    LegacyMigration.run();
    ThemeManager.init();
    UIModeManager.init();
    StudyCardEngine.init();
    SubjectivePracticeEngine.init();
    KnowledgeGraph.init();
    SearchEngine.init();
    TOCScrollSpy.init();
  });

  // Expose for testing, backup-restore UI, and pedagogical primitives
  window.HDH = {
    Scheduler:       Scheduler,
    MasteryStore:    MasteryStore,
    ReviewQueue:     ReviewQueue,
    BackupRestore:   BackupRestore,
    UIModeManager:   UIModeManager,
    Store:           Store,
    LegacyMigration: LegacyMigration,
  };

})();

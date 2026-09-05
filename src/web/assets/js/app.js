/**
 * HDH_UIT V2 — Deterministic Local-First Learning Runtime
 * Learning Architecture V1.2 Implementation
 * Independent QA Hardened Runtime
 *
 * Features implemented:
 *  - SM-2 Project Heuristic scheduler (HARD != AGAIN invariant)
 *  - M0-M3 mastery state machine (M3 only from TransferProblem evidence)
 *  - End-to-end evidence primitives: RecallCheckpoint (M2) & TransferProblem (M3)
 *  - Rating controls revealed only after feedback (PED-LEARN-004)
 *  - Scratchpad persistence in STORAGE_KEYS.drafts (STATE-LEARN-001)
 *  - Learn / Review / Reference mode switch (persisted)
 *  - Global Review Hub and live queue updates (REVIEW-LEARN-001, REVIEW-LEARN-002)
 *  - Deterministic DOM IDs for aria-controls (A11Y-LEARN-001)
 *  - Legacy localStorage migration (hdh_card_<id> -> new schema)
 *  - Exception-safe localStorage (quota, JSON, unavailable)
 *  - Hardened Backup / Restore schema validation
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
        return Object.assign({}, prev);
      }

      // Avoid DST-sensitive drift: compute due date via UTC calendar days
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
      var m = (now.getMonth() + 1 < 10 ? '0' : '') + (now.getMonth() + 1);
      var d = (now.getDate() < 10 ? '0' : '') + now.getDate();
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
  // Invariant: Review Rating alone CANNOT produce M2 or M3.
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
      if (passed && rec.mastery_state === 'M2') {
        rec.mastery_state = 'M3';
        rec.mastery_evidence.transfer_timestamp = Date.now();
      }
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

    isEligibleForReview: function (conceptId) {
      if (!conceptId) return false;
      var rec = this.get(conceptId);
      var isDue = Scheduler.isDue(rec.review_schedule.due_timestamp);
      var isWeak = rec.mastery_state === 'M0' || rec.mastery_state === 'M1';
      var hasMistakes = !!(rec.mistake_history && rec.mistake_history.length > 0);
      var isPendingTransfer = rec.mastery_state === 'M2' && !rec.mastery_evidence.transfer_passed;
      return isDue || isWeak || hasMistakes || isPendingTransfer;
    },

    getRecord: function (conceptId) {
      return this.get(conceptId);
    },

    getAllRecords: function () {
      return this._load();
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
      var keys = Store.keys();
      var allSucceeded = true;
      for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if (key.indexOf('hdh_card_') !== 0) continue;
        try {
          var old = Store.get(key, null);
          if (!old) continue;
          var isRemembered = (typeof old.remembered === 'boolean' && old.remembered) ||
                             (old.rating === 'GOOD' || old.rating === 'EASY');
          var cid = key.replace('hdh_card_', '');
          var data = Store.get(STORAGE_KEYS.mastery, {}) || {};
          if (!data[cid]) {
            var rec = MasteryStore._defaultRecord(cid);
            if (isRemembered) {
              rec.mastery_state = 'M1';
              rec.mastery_evidence.verification_mode = 'LEGACY_SELF_REPORT';
            }
            data[cid] = rec;
            var writeOk = Store.set(STORAGE_KEYS.mastery, data);
            if (writeOk) {
              var verified = Store.get(STORAGE_KEYS.mastery, null);
              if (verified && verified[cid] && verified[cid].mastery_state === rec.mastery_state) {
                MasteryStore._cache = null;
                Store.remove(key);
              } else {
                allSucceeded = false;
              }
            } else {
              allSucceeded = false;
            }
          } else {
            // Already safely in mastery store
            Store.remove(key);
          }
        } catch (_) {
          allSucceeded = false;
        }
      }
      if (allSucceeded) {
        Store.set(this.FLAG, true);
      }
    },

    migrateLegacyCards: function () {
      this.run();
    },
  };

  // ============================================================
  // BACKUP / RESTORE (HARDENED SCHEMA VALIDATION)
  // API-only / Deferred UI. Performs all validations before write.
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
        if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
          return { ok: false, error: 'Dữ liệu sao lưu không đúng định dạng đối tượng' };
        }
        if (payload.backup_version !== SCHEMA_VERSION) {
          return { ok: false, error: 'Phiên bản sao lưu không được hỗ trợ (yêu cầu phiên bản ' + SCHEMA_VERSION + ')' };
        }
        var stores = ['mastery', 'scheduler', 'drafts', 'mistakes'];
        for (var i = 0; i < stores.length; i++) {
          var key = stores[i];
          if (payload[key] !== undefined) {
            if (typeof payload[key] !== 'object' || payload[key] === null || Array.isArray(payload[key])) {
              return { ok: false, error: 'Trường ' + key + ' phải là một đối tượng từ điển hợp lệ' };
            }
          }
        }
        // All validations passed before writing to storage
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

      // Reference mode: reveal all hidden sections, hide ratings
      if (mode === 'reference') {
        document.querySelectorAll('.card-section').forEach(function (sec) {
          sec.classList.add('visible');
          sec.setAttribute('aria-hidden', 'false');
          sec.style.display = '';
        });
        document.querySelectorAll('.btn-hint, .btn-keypoints, .btn-answer, .btn-reveal-rubric, .btn-reveal-transfer-solution').forEach(function (btn) {
          btn.setAttribute('aria-expanded', 'true');
        });
        document.querySelectorAll('.card-rating-actions').forEach(function (actions) {
          actions.style.display = 'none';
          actions.setAttribute('aria-hidden', 'true');
        });
      } else {
        // Re-hide sections unless user explicitly opened them
        document.querySelectorAll('.card-section').forEach(function (sec) {
          if (!sec.dataset.userOpened) {
            sec.classList.remove('visible');
            sec.setAttribute('aria-hidden', 'true');
            if (sec.classList.contains('rubric-container') || sec.classList.contains('transfer-solution-container')) {
              sec.style.display = 'none';
            }
          }
        });
        document.querySelectorAll('.btn-hint, .btn-keypoints, .btn-answer, .btn-reveal-rubric, .btn-reveal-transfer-solution').forEach(function (btn) {
          if (!btn.dataset.userExpanded) btn.setAttribute('aria-expanded', 'false');
        });
      }

      // Review mode: filter cards in place without DOM reordering
      var shortcut = document.getElementById('review-hub-shortcut');
      if (mode === 'review') {
        if (shortcut) shortcut.style.display = 'inline-flex';
        this.updateReviewVisibility();
      } else {
        if (shortcut) shortcut.style.display = 'none';
        document.querySelectorAll('.study-card, .recall-checkpoint, .transfer-problem').forEach(function (card) {
          card.classList.remove('review-hidden');
        });
      }
    },

    updateReviewVisibility: function () {
      var count = 0;
      document.querySelectorAll('.study-card, .recall-checkpoint, .transfer-problem').forEach(function (card) {
        var cid = card.getAttribute('data-concept-id') || card.getAttribute('data-card-id') || card.getAttribute('data-item-id');
        var show = MasteryStore.isEligibleForReview(cid);
        if (show) {
          card.classList.remove('review-hidden');
          count++;
        } else {
          card.classList.add('review-hidden');
        }
      });
      return count;
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
        var conceptId = card.getAttribute('data-concept-id') || cardId;
        self._restoreState(card, cardId, conceptId);
        self._bindRevealButtons(card);
        self._bindRatingButtons(card, conceptId);
        self._bindKeyboard(card);
      });
    },

    _restoreState: function (card, cardId, conceptId) {
      if (!conceptId) return;
      var rec = MasteryStore.get(conceptId);
      this._applyMasteryUI(card, rec.mastery_state);

      // STATE-LEARN-001: Restore scratchpad text from STORAGE_KEYS.drafts
      var scratchpad = card.querySelector('.card-scratchpad');
      if (scratchpad && cardId) {
        var drafts = Store.get(STORAGE_KEYS.drafts, {});
        if (drafts && drafts[cardId] && typeof drafts[cardId].text === 'string') {
          scratchpad.value = drafts[cardId].text;
        }
        scratchpad.addEventListener('input', function () {
          var curDrafts = Store.get(STORAGE_KEYS.drafts, {}) || {};
          curDrafts[cardId] = {
            text: scratchpad.value,
            updated_at: Date.now(),
          };
          Store.set(STORAGE_KEYS.drafts, curDrafts);
        });
      }
    },

    _applyMasteryUI: function (card, state) {
      card.setAttribute('data-mastery', state);
      var badge = card.querySelector('.card-mastery-badge');
      if (badge) badge.textContent = state;
    },

    _bindRevealButtons: function (card) {
      var self = this;
      var buttons = card.querySelectorAll('.btn-hint, .btn-keypoints, .btn-answer');
      buttons.forEach(function (btn) {
        var targetId = btn.getAttribute('aria-controls');
        if (!targetId) return;
        var sec = document.getElementById(targetId);
        if (!sec) return;

        btn.addEventListener('click', function () {
          var nowVisible = sec.classList.toggle('visible');
          sec.setAttribute('aria-hidden', String(!nowVisible));
          btn.setAttribute('aria-expanded', String(nowVisible));
          btn.dataset.userExpanded = nowVisible ? '1' : '';
          sec.dataset.userOpened  = nowVisible ? '1' : '';

          var isHint = btn.classList.contains('btn-hint');
          var isKeypoints = btn.classList.contains('btn-keypoints');
          var isAnswer = btn.classList.contains('btn-answer');
          var feedbackStatus = card.querySelector('.card-feedback-status');

          // PED-LEARN-005: Hint must not unlock review ratings.
          // Only keypoints (reveal + unlock) and answer (reveal + unlock) unlock rating controls.
          if (nowVisible) {
            if (isHint) {
              if (feedbackStatus) feedbackStatus.textContent = 'Đã mở gợi ý. Hãy tiếp tục tự trả lời trước khi đối chiếu.';
            } else if (isKeypoints) {
              if (feedbackStatus) feedbackStatus.textContent = 'Đã mở các ý đối soát. Bạn có thể đánh giá lượt ôn.';
              self._unlockRatings(card);
            } else if (isAnswer) {
              if (feedbackStatus) feedbackStatus.textContent = 'Đã mở lời giải. Bạn có thể đánh giá lượt ôn.';
              self._unlockRatings(card);
            }
          }
        });
      });
    },

    _unlockRatings: function (card) {
      var mode = document.documentElement.getAttribute('data-ui-mode') || 'learn';
      if (mode === 'reference') return;
      var ratingActions = card.querySelector('.card-rating-actions');
      if (ratingActions) {
        ratingActions.style.display = '';
        ratingActions.setAttribute('aria-hidden', 'false');
      }
    },

    _bindRatingButtons: function (card, conceptId) {
      var self = this;
      card.querySelectorAll('.btn-rating').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (!conceptId) return;
          var rating = btn.getAttribute('data-rating');
          var rec = MasteryStore.recordRating(conceptId, rating);
          self._applyMasteryUI(card, rec.mastery_state);
          self._showRatingFeedback(card, rating, rec);

          // REVIEW-LEARN-002: Live queue update in review mode
          if (document.documentElement.getAttribute('data-ui-mode') === 'review') {
            UIModeManager.updateReviewVisibility();
          }
          if (window.ReviewHubEngine) {
            window.ReviewHubEngine.renderQueue();
          }
        });
      });
    },

    _showRatingFeedback: function (card, rating, rec) {
      var colors = { AGAIN: '#cf222e', HARD: '#e36209', GOOD: '#1a7f37', EASY: '#0969da' };
      var color = colors[rating] || '#0969da';
      card.style.transition = 'border-color 0.15s ease';
      card.style.borderLeftColor = color;
      var feedbackStatus = card.querySelector('.card-feedback-status');
      if (feedbackStatus) {
        feedbackStatus.textContent = 'Đã ghi nhận (' + rating + '). Ôn lại sau ' + rec.review_schedule.interval_days + ' ngày.';
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
  // RECALL CHECKPOINT ENGINE (MASTERY-LEARN-001)
  // ============================================================
  var RecallCheckpointEngine = {
    init: function () {
      var self = this;
      document.querySelectorAll('.recall-checkpoint').forEach(function (cp) {
        var itemId = cp.getAttribute('data-item-id');
        var conceptId = cp.getAttribute('data-concept-id') || itemId;
        self._restoreState(cp, itemId, conceptId);
        self._bindRubric(cp, itemId, conceptId);
      });
    },

    _restoreState: function (cp, itemId, conceptId) {
      var rec = MasteryStore.get(conceptId);
      var badge = cp.querySelector('.card-mastery-badge');
      if (badge) badge.textContent = rec.mastery_state;
      cp.setAttribute('data-mastery', rec.mastery_state);

      var status = cp.querySelector('.checkpoint-status');
      if (status) {
        if (rec.mastery_state === 'M2' || rec.mastery_state === 'M3') {
          status.textContent = 'Đã đạt M2 (Tự giải thích bản chất)';
        } else {
          status.textContent = 'Chưa tự kiểm tra';
        }
      }

      var scratchpad = cp.querySelector('.checkpoint-scratchpad');
      if (scratchpad && itemId) {
        var drafts = Store.get(STORAGE_KEYS.drafts, {});
        if (drafts && drafts[itemId] && typeof drafts[itemId].text === 'string') {
          scratchpad.value = drafts[itemId].text;
        }
        scratchpad.addEventListener('input', function () {
          var curDrafts = Store.get(STORAGE_KEYS.drafts, {}) || {};
          curDrafts[itemId] = { text: scratchpad.value, updated_at: Date.now() };
          Store.set(STORAGE_KEYS.drafts, curDrafts);
        });
      }
    },

    _bindRubric: function (cp, itemId, conceptId) {
      var revealBtn = cp.querySelector('.btn-reveal-rubric');
      var rubricContainer = cp.querySelector('.rubric-container');
      var submitBtn = cp.querySelector('.btn-submit-recall');
      var feedback = cp.querySelector('.recall-feedback');
      var badge = cp.querySelector('.card-mastery-badge');
      var status = cp.querySelector('.checkpoint-status');

      if (revealBtn && rubricContainer) {
        revealBtn.addEventListener('click', function () {
          var isVis = rubricContainer.style.display !== 'none';
          rubricContainer.style.display = isVis ? 'none' : 'block';
          rubricContainer.setAttribute('aria-hidden', String(isVis));
          revealBtn.setAttribute('aria-expanded', String(!isVis));
        });
      }

      if (submitBtn && rubricContainer) {
        submitBtn.addEventListener('click', function () {
          var checkboxes = rubricContainer.querySelectorAll('.rubric-check');
          var totalWeight = 0;
          var earnedWeight = 0;
          checkboxes.forEach(function (cb) {
            var w = parseFloat(cb.getAttribute('data-weight') || '1.0');
            totalWeight += w;
            if (cb.checked) earnedWeight += w;
          });
          var rubricPct = totalWeight > 0 ? (earnedWeight / totalWeight) * 100 : 100;
          var passed = rubricPct >= 80;

          var rec = MasteryStore.recordRecallEvidence(conceptId, passed, rubricPct);
          if (badge) badge.textContent = rec.mastery_state;
          cp.setAttribute('data-mastery', rec.mastery_state);

          if (passed) {
            if (feedback) feedback.textContent = 'Đạt M2 thành công! (Điểm rubric: ' + Math.round(rubricPct) + '% >= 80%).';
            if (status) status.textContent = 'Đã đạt M2 (Tự giải thích bản chất)';
          } else {
            if (feedback) feedback.textContent = 'Chưa đạt M2 (Điểm rubric: ' + Math.round(rubricPct) + '% < 80%). Cần nắm chắc từ khóa cốt lõi.';
            if (status) status.textContent = 'Chưa đạt M2';
          }

          if (document.documentElement.getAttribute('data-ui-mode') === 'review') {
            UIModeManager.updateReviewVisibility();
          }
          if (window.ReviewHubEngine) {
            window.ReviewHubEngine.renderQueue();
          }
        });
      }
    },
  };

  // ============================================================
  // TRANSFER PROBLEM ENGINE (MASTERY-LEARN-001)
  // ============================================================
  var TransferProblemEngine = {
    init: function () {
      var self = this;
      document.querySelectorAll('.transfer-problem').forEach(function (tp) {
        var itemId = tp.getAttribute('data-item-id');
        var conceptId = tp.getAttribute('data-concept-id') || itemId;
        self._restoreState(tp, itemId, conceptId);
        self._bindActions(tp, itemId, conceptId);
      });
    },

    _restoreState: function (tp, itemId, conceptId) {
      var rec = MasteryStore.get(conceptId);
      var badge = tp.querySelector('.card-mastery-badge');
      if (badge) badge.textContent = rec.mastery_state;
      tp.setAttribute('data-mastery', rec.mastery_state);

      var gateStatus = tp.querySelector('.transfer-gate-status');
      if (gateStatus) {
        if (rec.mastery_state === 'M3') {
          gateStatus.textContent = 'Đã xác lập M3 (Chuyển giao độc lập)';
        } else if (rec.mastery_state === 'M2') {
          gateStatus.textContent = 'Sẵn sàng kiểm tra M3 (Đã đạt M2)';
        } else {
          gateStatus.textContent = 'Cần đạt cấp độ M2 trước khi kiểm tra M3';
        }
      }

      var scratchpad = tp.querySelector('.transfer-scratchpad');
      if (scratchpad && itemId) {
        var drafts = Store.get(STORAGE_KEYS.drafts, {});
        if (drafts && drafts[itemId] && typeof drafts[itemId].text === 'string') {
          scratchpad.value = drafts[itemId].text;
        }
        scratchpad.addEventListener('input', function () {
          var curDrafts = Store.get(STORAGE_KEYS.drafts, {}) || {};
          curDrafts[itemId] = { text: scratchpad.value, updated_at: Date.now() };
          Store.set(STORAGE_KEYS.drafts, curDrafts);
        });
      }
    },

    _bindActions: function (tp, itemId, conceptId) {
      var revealBtn = tp.querySelector('.btn-reveal-transfer-solution');
      var solContainer = tp.querySelector('.transfer-solution-container');
      var passBtn = tp.querySelector('.btn-transfer-pass');
      var failBtn = tp.querySelector('.btn-transfer-fail');
      var feedback = tp.querySelector('.transfer-feedback');
      var badge = tp.querySelector('.card-mastery-badge');
      var gateStatus = tp.querySelector('.transfer-gate-status');

      if (revealBtn && solContainer) {
        revealBtn.addEventListener('click', function () {
          var isVis = solContainer.style.display !== 'none';
          solContainer.style.display = isVis ? 'none' : 'block';
          solContainer.setAttribute('aria-hidden', String(isVis));
          revealBtn.setAttribute('aria-expanded', String(!isVis));
        });
      }

      if (passBtn) {
        passBtn.addEventListener('click', function () {
          var curRec = MasteryStore.get(conceptId);
          if (curRec.mastery_state !== 'M2' && curRec.mastery_state !== 'M3') {
            if (feedback) feedback.textContent = 'Không thể cấp M3: Bạn phải hoàn thành M2 trước khi tự đánh giá M3.';
            return;
          }
          var rec = MasteryStore.recordTransferEvidence(conceptId, true);
          if (badge) badge.textContent = rec.mastery_state;
          tp.setAttribute('data-mastery', rec.mastery_state);
          if (feedback) feedback.textContent = 'Đạt chuẩn M3: Năng lực chuyển giao độc lập đã được xác lập!';
          if (gateStatus) gateStatus.textContent = 'Đã xác lập M3 (Chuyển giao độc lập)';
          if (document.documentElement.getAttribute('data-ui-mode') === 'review') {
            UIModeManager.updateReviewVisibility();
          }
          if (window.ReviewHubEngine) {
            window.ReviewHubEngine.renderQueue();
          }
        });
      }

      if (failBtn) {
        failBtn.addEventListener('click', function () {
          MasteryStore.recordTransferEvidence(conceptId, false);
          if (feedback) feedback.textContent = 'Chưa đạt chuyển giao. Hãy rà soát lại phương pháp giải.';
          if (document.documentElement.getAttribute('data-ui-mode') === 'review') {
            UIModeManager.updateReviewVisibility();
          }
          if (window.ReviewHubEngine) {
            window.ReviewHubEngine.renderQueue();
          }
        });
      }
    },
  };

  // ============================================================
  // REVIEW HUB ENGINE (REVIEW-LEARN-001)
  // ============================================================
  var ReviewHubEngine = {
    init: function () {
      var queueContainer = document.getElementById('review-hub-queue');
      if (!queueContainer) return;
      this.renderQueue();

      var refreshBtn = document.getElementById('btn-refresh-hub');
      var self = this;
      if (refreshBtn) {
        refreshBtn.addEventListener('click', function () {
          self.renderQueue();
        });
      }
    },

    renderQueue: function () {
      var queueContainer = document.getElementById('review-hub-queue');
      if (!queueContainer) return;

      var dueCountEl = document.getElementById('hub-due-count');
      var weakCountEl = document.getElementById('hub-weak-count');
      var totalCountEl = document.getElementById('hub-total-count');
      var pendingCountEl = document.getElementById('hub-pending-count');
      var mistakeCountEl = document.getElementById('hub-mistake-count');

      var depth = window.location.pathname.split('/').filter(Boolean).length
        - (window.location.pathname.endsWith('/') ? 0 : 1);
      var prefix = Array(Math.max(0, depth) + 1).join('../');

      fetch(prefix + 'study_index.json')
        .then(function (r) { return r.json(); })
        .then(function (items) {
          var total = items.length;
          var dueCount = 0;
          var weakCount = 0;
          var pendingTransferCount = 0;
          var mistakeCount = 0;

          var eligibleItems = items.filter(function (item) {
            var cid = item.concept_id || item.id;
            var rec = MasteryStore.get(cid);
            var isDue = Scheduler.isDue(rec.review_schedule.due_timestamp);
            var isWeak = rec.mastery_state === 'M0' || rec.mastery_state === 'M1';
            var hasMistakes = !!(rec.mistake_history && rec.mistake_history.length > 0);
            var isPendingTransfer = rec.mastery_state === 'M2' && !rec.mastery_evidence.transfer_passed;

            if (isDue) dueCount++;
            if (isWeak && !isDue) weakCount++;
            if (isPendingTransfer) pendingTransferCount++;
            if (hasMistakes) mistakeCount++;

            return MasteryStore.isEligibleForReview(cid);
          });

          if (totalCountEl) totalCountEl.textContent = total;
          if (weakCountEl) weakCountEl.textContent = weakCount;
          if (dueCountEl) dueCountEl.textContent = dueCount;
          if (pendingCountEl) pendingCountEl.textContent = pendingTransferCount;
          if (mistakeCountEl) mistakeCountEl.textContent = mistakeCount;

          if (eligibleItems.length === 0) {
            queueContainer.innerHTML = '<div class="hub-empty-message">🎉 Xuất sắc! Tất cả các mục ôn tập đã được hoàn thành.</div>';
            return;
          }

          var sorted = ReviewQueue.sortItems(eligibleItems);
          var html = '<ul class="review-hub-list">';
          sorted.forEach(function (item) {
            var cid = item.concept_id || item.id;
            var rec = MasteryStore.get(cid);
            var score = ReviewQueue.getPriorityScore(cid);
            var isDue = Scheduler.isDue(rec.review_schedule.due_timestamp);
            var hasMistakes = !!(rec.mistake_history && rec.mistake_history.length > 0);
            var isPendingTransfer = rec.mastery_state === 'M2' && !rec.mastery_evidence.transfer_passed;
            var isWeak = rec.mastery_state === 'M0' || rec.mastery_state === 'M1';

            var statusLabel = 'Đang ôn';
            var statusClass = 'badge-review';

            if (isDue) {
              statusLabel = 'Đến hạn';
              statusClass = 'badge-due';
            } else if (hasMistakes) {
              statusLabel = 'Có lỗi sai';
              statusClass = 'badge-mistake';
            } else if (isPendingTransfer) {
              statusLabel = 'Chờ chuyển giao';
              statusClass = 'badge-pending-transfer';
            } else if (isWeak) {
              statusLabel = 'Cần củng cố';
              statusClass = 'badge-weak';
            }

            var targetUrl = prefix + item.url + '#' + item.anchor;

            html += '<li class="review-queue-card" data-hub-card-id="' + cid + '" data-priority="' + score + '">'
              + '<div class="queue-card-meta">'
              + '<span class="queue-card-doc">' + (item.doc_title || 'Tài liệu') + '</span>'
              + '<span class="card-mastery-badge">' + rec.mastery_state + '</span>'
              + '<span class="queue-status-badge ' + statusClass + '">' + statusLabel + '</span>'
              + '</div>'
              + '<div class="queue-card-question">' + (item.question || item.id) + '</div>'
              + '<div class="queue-card-action">'
              + '<a class="btn-card primary" href="' + targetUrl + '">Ôn tập ngay ↗</a>'
              + '</div>'
              + '</li>';
          });
          html += '</ul>';
          queueContainer.innerHTML = html;
        })
        .catch(function () {
          queueContainer.innerHTML = '<div class="queue-error">Không thể tải dữ liệu chỉ mục học tập.</div>';
        });
    },
  };

  // ============================================================
  // SUBJECTIVE PRACTICE ENGINE
  // ============================================================
  var SubjectivePracticeEngine = {
    init: function () {
      document.querySelectorAll('.subjective-practice').forEach(function (container) {
        var practiceId      = container.getAttribute('data-practice-id');
        var conceptId       = container.getAttribute('data-concept-id') || practiceId;
        var textarea        = container.querySelector('.practice-textarea');
        var compareBtn      = container.querySelector('.btn-compare');
        var rubricContainer = container.querySelector('.rubric-container');
        var checkboxes      = container.querySelectorAll('.rubric-check');
        var scoreDisplay    = container.querySelector('.current-score');
        var maxScore        = parseFloat(container.getAttribute('data-max-score') || '1.0');
        var claimM2Btn      = container.querySelector('.btn-practice-claim-m2');
        var feedback        = container.querySelector('.practice-feedback');
        var badge           = container.querySelector('.card-mastery-badge');
        var stateKey        = 'hdh_practice_' + practiceId;

        // Restore mastery badge
        if (conceptId && badge) {
          badge.textContent = MasteryStore.get(conceptId).mastery_state;
        }

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
            if (saved.rubricVisible && rubricContainer) {
              rubricContainer.classList.add('visible');
              rubricContainer.setAttribute('aria-hidden', 'false');
            }
          }
          textarea.addEventListener('input', saveState);
        }

        if (compareBtn && rubricContainer) {
          compareBtn.addEventListener('click', function () {
            var nowVisible = rubricContainer.classList.toggle('visible');
            rubricContainer.setAttribute('aria-hidden', String(!nowVisible));
            compareBtn.setAttribute('aria-expanded', String(nowVisible));
            compareBtn.textContent = nowVisible
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

          // Allow claiming M2 if >= 80% rubric score
          if (claimM2Btn) {
            if (score >= 0.8 * maxScore) {
              claimM2Btn.style.display = '';
            } else {
              claimM2Btn.style.display = 'none';
            }
          }
          saveState();
        };

        if (claimM2Btn) {
          claimM2Btn.addEventListener('click', function () {
            var pct = maxScore > 0 ? (parseFloat(scoreDisplay.textContent) / maxScore) * 100 : 100;
            var rec = MasteryStore.recordRecallEvidence(conceptId, true, pct);
            if (badge) badge.textContent = rec.mastery_state;
            if (feedback) feedback.textContent = 'Đã ghi nhận cấp độ M2 qua bài tự luận (Rubric: ' + Math.round(pct) + '% >= 80%).';
          });
        }

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
    RecallCheckpointEngine.init();
    TransferProblemEngine.init();
    ReviewHubEngine.init();
    SubjectivePracticeEngine.init();
    KnowledgeGraph.init();
    SearchEngine.init();
    TOCScrollSpy.init();
  });

  // Expose for testing, backup-restore UI, and pedagogical primitives
  window.HDH = {
    Scheduler:                Scheduler,
    MasteryStore:             MasteryStore,
    ReviewQueue:              ReviewQueue,
    BackupRestore:            BackupRestore,
    UIModeManager:            UIModeManager,
    Store:                    Store,
    LegacyMigration:          LegacyMigration,
    Migration:                LegacyMigration,
    StudyCardEngine:          StudyCardEngine,
    RecallCheckpointEngine:   RecallCheckpointEngine,
    TransferProblemEngine:    TransferProblemEngine,
    ReviewHubEngine:          ReviewHubEngine,
  };

})();

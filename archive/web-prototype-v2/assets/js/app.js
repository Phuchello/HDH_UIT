/**
 * HDH_UIT V2 — Interactive Web Companion Runtime
 * Quartz-inspired Digital Garden Client Scripts
 */

(function () {
  'use strict';

  // ==========================================
  // 1. THEME MANAGER (DARK / LIGHT MODE)
  // ==========================================
  const ThemeManager = {
    init() {
      const savedTheme = localStorage.getItem('hdh_theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      this.setTheme(savedTheme);

      const toggleBtn = document.getElementById('theme-toggle-btn');
      if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
          const current = document.documentElement.getAttribute('data-theme') || 'light';
          const next = current === 'dark' ? 'light' : 'dark';
          this.setTheme(next);
        });
      }
    },

    setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('hdh_theme', theme);
      const icon = document.getElementById('theme-icon');
      if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
      }
      // Notify Graph to redraw with theme-appropriate colors
      if (window.KnowledgeGraph) {
        window.KnowledgeGraph.draw();
      }
    }
  };

  // ==========================================
  // 2. STUDY CARD ACTIVE RECALL COMPONENT
  // ==========================================
  const StudyCardEngine = {
    init() {
      document.querySelectorAll('.study-card').forEach(card => {
        const cardId = card.getAttribute('data-card-id');
        const hintBtn = card.querySelector('.btn-hint');
        const keypointsBtn = card.querySelector('.btn-keypoints');
        const answerBtn = card.querySelector('.btn-answer');
        const rememberBtn = card.querySelector('.btn-remember');
        const forgotBtn = card.querySelector('.btn-forgot');

        const hintSec = card.querySelector('.card-hint');
        const keypointsSec = card.querySelector('.card-keypoints');
        const answerSec = card.querySelector('.card-answer');

        if (hintBtn && hintSec) {
          hintBtn.addEventListener('click', () => {
            hintSec.classList.toggle('visible');
          });
        }

        if (keypointsBtn && keypointsSec) {
          keypointsBtn.addEventListener('click', () => {
            keypointsSec.classList.toggle('visible');
          });
        }

        if (answerBtn && answerSec) {
          answerBtn.addEventListener('click', () => {
            answerSec.classList.toggle('visible');
          });
        }

        if (rememberBtn) {
          rememberBtn.addEventListener('click', () => {
            this.recordProgress(cardId, true);
            rememberBtn.style.opacity = '0.5';
            if (forgotBtn) forgotBtn.style.opacity = '1';
          });
        }

        if (forgotBtn) {
          forgotBtn.addEventListener('click', () => {
            this.recordProgress(cardId, false);
            forgotBtn.style.opacity = '0.5';
            if (rememberBtn) rememberBtn.style.opacity = '1';
          });
        }
      });
    },

    recordProgress(cardId, remembered) {
      if (!cardId) return;
      const key = `hdh_card_${cardId}`;
      const state = { remembered, timestamp: Date.now() };
      localStorage.setItem(key, JSON.stringify(state));
    }
  };

  // ==========================================
  // 3. SUBJECTIVE PRACTICE SELF-SCORING
  // ==========================================
  const SubjectivePracticeEngine = {
    init() {
      document.querySelectorAll('.subjective-practice').forEach(container => {
        const practiceId = container.getAttribute('data-practice-id');
        const textarea = container.querySelector('.practice-textarea');
        const compareBtn = container.querySelector('.btn-compare');
        const rubricContainer = container.querySelector('.rubric-container');
        const checkboxes = container.querySelectorAll('.rubric-check');
        const scoreDisplay = container.querySelector('.current-score');
        const maxScore = parseFloat(container.getAttribute('data-max-score') || '1.0');

        // Restore draft from localStorage
        if (practiceId && textarea) {
          const savedDraft = localStorage.getItem(`hdh_draft_${practiceId}`);
          if (savedDraft) {
            textarea.value = savedDraft;
          }
          textarea.addEventListener('input', () => {
            localStorage.setItem(`hdh_draft_${practiceId}`, textarea.value);
          });
        }

        if (compareBtn && rubricContainer) {
          compareBtn.addEventListener('click', () => {
            rubricContainer.classList.toggle('visible');
            if (rubricContainer.classList.contains('visible')) {
              compareBtn.textContent = 'Ẩn Barem Chấm';
            } else {
              compareBtn.textContent = 'So Sánh Với Barem Điểm';
            }
          });
        }

        // Calculate score on checkbox change
        const updateScore = () => {
          let score = 0;
          checkboxes.forEach(cb => {
            if (cb.checked) {
              score += parseFloat(cb.getAttribute('data-weight') || '0');
            }
          });
          score = Math.min(score, maxScore);
          if (scoreDisplay) {
            scoreDisplay.textContent = score.toFixed(2);
          }
          if (practiceId) {
            localStorage.setItem(`hdh_score_${practiceId}`, score);
          }
        };

        checkboxes.forEach(cb => {
          cb.addEventListener('change', updateScore);
        });
      });
    }
  };

  // ==========================================
  // 4. KNOWLEDGE GRAPH VIEW (CANVAS ENGINE)
  // ==========================================
  const KnowledgeGraph = {
    canvas: null,
    ctx: null,
    nodes: [],
    edges: [],

    init() {
      this.canvas = document.getElementById('knowledge-graph-canvas');
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      const depth = window.location.pathname.split('/').filter(Boolean).length - (window.location.pathname.endsWith('/') ? 0 : 1);
      const prefix = '../'.repeat(Math.max(0, depth));
      fetch(`${prefix}graph_data.json`).then(response => response.json()).then(data => {
        this.nodes = data.nodes || [];
        this.edges = data.edges || [];
        this.nodes.forEach(node => { node.link = `${prefix}${node.link}`; });
        this.draw();
      }).catch(() => this.draw());
      this.resize();
      this.draw();

      this.canvas.addEventListener('click', (e) => {
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        this.nodes.forEach(node => {
          const dx = node.x - mouseX;
          const dy = node.y - mouseY;
          if (Math.sqrt(dx * dx + dy * dy) <= node.r + 4) {
            if (node.link) {
              window.location.href = node.link;
            }
          }
        });
      });

      window.addEventListener('resize', () => {
        this.resize();
        this.draw();
      });
    },

    resize() {
      if (!this.canvas) return;
      this.canvas.width = this.canvas.parentElement.clientWidth;
      this.canvas.height = 180;
    },

    draw() {
      if (!this.ctx || !this.canvas) return;
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      // Draw edges
      this.ctx.strokeStyle = isDark ? '#30363d' : '#e2e2da';
      this.ctx.lineWidth = 1.5;
      this.edges.forEach(edge => {
        const n1 = this.nodes.find(n => n.id === edge.from);
        const n2 = this.nodes.find(n => n.id === edge.to);
        if (n1 && n2) {
          this.ctx.beginPath();
          this.ctx.moveTo(n1.x, n1.y);
          this.ctx.lineTo(n2.x, n2.y);
          this.ctx.stroke();
        }
      });

      // Draw nodes
      this.nodes.forEach(node => {
        this.ctx.beginPath();
        this.ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
        this.ctx.fillStyle = node.color;
        this.ctx.fill();

        // Label
        this.ctx.fillStyle = isDark ? '#e6edf3' : '#1f2328';
        this.ctx.font = '10px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(node.label, node.x, node.y + node.r + 12);
      });
    }
  };
  window.KnowledgeGraph = KnowledgeGraph;

  // ==========================================
  // 5. SEARCH MODAL ENGINE
  // ==========================================
  const SearchEngine = {
    searchIndex: [],

    init() {
      const modalOverlay = document.getElementById('search-modal-overlay');
      const triggerBtn = document.getElementById('search-trigger-btn');
      const searchInput = document.getElementById('search-input');
      const resultsList = document.getElementById('search-results-list');

      const depth = window.location.pathname.split('/').filter(Boolean).length - (window.location.pathname.endsWith('/') ? 0 : 1);
      const prefix = '../'.repeat(Math.max(0, depth));
      fetch(`${prefix}search_index.json`).then(response => response.json()).then(items => {
        this.searchIndex = items.map(item => ({ ...item, url: `${prefix}${item.url}` }));
      }).catch(() => { this.searchIndex = []; });

      const openSearch = () => {
        if (modalOverlay) {
          modalOverlay.classList.add('active');
          if (searchInput) {
            searchInput.focus();
            searchInput.value = '';
            this.renderResults(this.searchIndex, resultsList);
          }
        }
      };

      const closeSearch = () => {
        if (modalOverlay) modalOverlay.classList.remove('active');
      };

      if (triggerBtn) {
        triggerBtn.addEventListener('click', openSearch);
      }

      // Keyboard Shortcut (Ctrl+K or Cmd+K)
      window.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
          e.preventDefault();
          openSearch();
        }
        if (e.key === 'Escape') {
          closeSearch();
        }
      });

      if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
          if (e.target === modalOverlay) closeSearch();
        });
      }

      if (searchInput && resultsList) {
        searchInput.addEventListener('input', (e) => {
          const query = e.target.value.toLowerCase().trim();
          if (!query) {
            this.renderResults(this.searchIndex, resultsList);
            return;
          }
          const filtered = this.searchIndex.filter(item => 
            item.title.toLowerCase().includes(query) || item.snippet.toLowerCase().includes(query)
          );
          this.renderResults(filtered, resultsList);
        });
      }
    },

    renderResults(items, container) {
      if (!container) return;
      container.innerHTML = '';
      if (items.length === 0) {
        container.innerHTML = '<li style="padding: 1rem; text-align: center; color: var(--text-muted);">Không tìm thấy kết quả phù hợp.</li>';
        return;
      }
      items.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
          <a class="search-result-item" href="${item.url}">
            <span class="search-result-title">${item.title}</span>
            <span class="search-result-snippet">${item.snippet}</span>
          </a>
        `;
        container.appendChild(li);
      });
    }
  };

  // ==========================================
  // 6. TABLE OF CONTENTS SCROLLSPY
  // ==========================================
  const TOCScrollSpy = {
    init() {
      const headings = document.querySelectorAll('.article-body h2, .article-body h3');
      const tocLinks = document.querySelectorAll('.toc-link');
      if (headings.length === 0 || tocLinks.length === 0) return;

      window.addEventListener('scroll', () => {
        let currentId = '';
        const scrollY = window.pageYOffset;

        headings.forEach(heading => {
          const top = heading.offsetTop - 100;
          if (scrollY >= top) {
            currentId = heading.id;
          }
        });

        tocLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${currentId}`) {
            link.classList.add('active');
          }
        });
      });
    }
  };

  // Initialize all components on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    StudyCardEngine.init();
    SubjectivePracticeEngine.init();
    KnowledgeGraph.init();
    SearchEngine.init();
    TOCScrollSpy.init();
  });

})();

// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('HDH_UIT V2 Deterministic Learning System Browser Suite', () => {

  test.beforeEach(async ({ page }) => {
    // Clear localStorage before each test
    await page.goto('/index.html');
    await page.evaluate(() => localStorage.clear());
  });

  // -------------------------------------------------------------------------
  // Scenario 1: Learn Mode - Progressive Disclosure & Rating Unlock (PED-LEARN-004, PED-LEARN-005)
  // -------------------------------------------------------------------------
  test('1. Learn Mode enforces progressive disclosure: hint leaves rating hidden; answer unlocks rating', async ({ page }) => {
    await page.goto('/flashcards/ch01-cards.html');

    const card = page.locator('#fc-01-mode-bit');
    await expect(card).toBeVisible();

    const hint = card.locator('#fc-01-mode-bit__hint');
    const answer = card.locator('#fc-01-mode-bit__answer');
    const ratingActions = card.locator('#fc-01-mode-bit__rating_actions');
    const feedbackStatus = card.locator('#fc-01-mode-bit__feedback');

    // Initially hidden
    await expect(hint).toBeHidden();
    await expect(answer).toBeHidden();
    await expect(ratingActions).toBeHidden();

    // PED-LEARN-005: Click reveal hint -> hint visible, rating controls STILL HIDDEN
    const btnHint = card.locator('.btn-hint');
    if (await btnHint.count() > 0) {
      await btnHint.click();
      await expect(hint).toBeVisible();
      expect(await btnHint.getAttribute('aria-expanded')).toBe('true');
      await expect(ratingActions).toBeHidden();
      await expect(feedbackStatus).toContainText('Đã mở gợi ý');
    }

    // Click reveal answer -> answer revealed AND rating controls unlocked
    const btnAnswer = card.locator('.btn-answer');
    await btnAnswer.click();

    // Answer revealed
    await expect(answer).toBeVisible();
    expect(await btnAnswer.getAttribute('aria-expanded')).toBe('true');

    // Rating controls unlocked and visible
    await expect(ratingActions).toBeVisible();
    await expect(feedbackStatus).toContainText('Đã mở lời giải');
  });

  // -------------------------------------------------------------------------
  // Scenario 2: Reference Mode - All Sections Visible & Ratings Hidden
  // -------------------------------------------------------------------------
  test('2. Reference Mode reveals all sections and hides rating actions', async ({ page }) => {
    await page.goto('/flashcards/ch01-cards.html');

    // Switch to reference mode
    const refBtn = page.locator('button[data-mode="reference"]');
    await refBtn.click();

    const mode = await page.evaluate(() => document.documentElement.getAttribute('data-ui-mode'));
    expect(mode).toBe('reference');

    const card = page.locator('#fc-01-mode-bit');
    const hint = card.locator('#fc-01-mode-bit__hint');
    const answer = card.locator('#fc-01-mode-bit__answer');
    const ratingActions = card.locator('#fc-01-mode-bit__rating_actions');

    // In reference mode, all content sections are visible
    await expect(hint).toBeVisible();
    await expect(answer).toBeVisible();

    // Rating controls must remain hidden in reference mode
    await expect(ratingActions).toBeHidden();
  });

  // -------------------------------------------------------------------------
  // Scenario 3: Scratchpad Persistence across Reloads (STATE-LEARN-001)
  // -------------------------------------------------------------------------
  test('3. StudyCard scratchpad persists draft across page reloads', async ({ page }) => {
    await page.goto('/flashcards/ch01-cards.html');

    const scratchpad = page.locator('#fc-01-mode-bit__scratchpad');
    const testDraft = 'Kernel mode bit = 0; User mode bit = 1.';

    await scratchpad.fill(testDraft);
    await page.waitForTimeout(200); // allow input event to persist

    // Reload page
    await page.reload();

    const restoredPad = page.locator('#fc-01-mode-bit__scratchpad');
    await expect(restoredPad).toHaveValue(testDraft);
  });

  // -------------------------------------------------------------------------
  // Scenario 4: Rating Persistence across Reloads
  // -------------------------------------------------------------------------
  test('4. Rating a card persists mastery and schedule across reloads', async ({ page }) => {
    await page.goto('/flashcards/ch01-cards.html');

    const card = page.locator('#fc-01-mode-bit');
    await card.locator('.btn-answer').click();

    const btnGood = card.locator('.btn-good');
    await expect(btnGood).toBeVisible();
    await btnGood.click();

    // Status updated
    const badge = card.locator('.card-mastery-badge');
    await expect(badge).toHaveText('M1');

    // Reload
    await page.reload();

    const cardAfter = page.locator('#fc-01-mode-bit');
    const badgeAfter = cardAfter.locator('.card-mastery-badge');
    await expect(badgeAfter).toHaveText('M1');

    // Verify localStorage has persisted record
    const record = await page.evaluate(() => window.HDH.MasteryStore.getRecord('fc-01-mode-bit'));
    expect(record.mastery_state).toBe('M1');
    expect(record.review_schedule.reps).toBe(1);
    expect(record.review_schedule.interval_days).toBe(1);
  });

  // -------------------------------------------------------------------------
  // Scenario 5: HARD != AGAIN Invariant
  // -------------------------------------------------------------------------
  test('5. HARD != AGAIN scheduler invariant: HARD increments reps, AGAIN resets to 0', async ({ page }) => {
    await page.goto('/index.html');

    const result = await page.evaluate(() => {
      const prev = { reps: 4, ef: 2.5, interval_days: 10, lapses: 1 };
      const hardRes = window.HDH.Scheduler.schedule(prev, 'HARD', '2026-09-05');
      const againRes = window.HDH.Scheduler.schedule(prev, 'AGAIN', '2026-09-05');
      return { hardRes, againRes };
    });

    // HARD: reps must NOT be reset to 0; must increment
    expect(result.hardRes.reps).toBe(5);
    expect(result.hardRes.interval_days).toBeGreaterThanOrEqual(10);
    expect(result.hardRes.lapses).toBe(1);

    // AGAIN: reps reset to 0, interval = 1, lapses incremented
    expect(result.againRes.reps).toBe(0);
    expect(result.againRes.interval_days).toBe(1);
    expect(result.againRes.lapses).toBe(2);
  });

  // -------------------------------------------------------------------------
  // Scenario 6: Legacy Card Migration & Transactional Safety (STATE-LEARN-002)
  // -------------------------------------------------------------------------
  test('6. Legacy flashcard ratings migrate cleanly, and write failure preserves legacy key (STATE-LEARN-002)', async ({ page }) => {
    await page.goto('/index.html');

    const result = await page.evaluate(() => {
      // 1. Normal migration success
      localStorage.setItem('hdh_card_legacy_ch01_test', JSON.stringify({
        remembered: true,
        timestamp: Date.now() - 500000
      }));
      window.HDH.Migration.migrateLegacyCards();
      const rec = window.HDH.MasteryStore.getRecord('legacy_ch01_test');
      const oldKeyStillExists = localStorage.getItem('hdh_card_legacy_ch01_test') !== null;

      // 2. Transactional failure simulation: Store.set fails / returns false
      localStorage.setItem('hdh_card_legacy_fail_test', JSON.stringify({
        remembered: true,
        timestamp: Date.now() - 500000
      }));
      const origSet = window.HDH.Store.set;
      window.HDH.Store.set = function (k, v) {
        if (k === 'hdh_mastery_v1') return false; // simulate write failure / quota error
        return origSet.call(window.HDH.Store, k, v);
      };
      window.HDH.Migration.migrateLegacyCards();
      const failKeyPreserved = localStorage.getItem('hdh_card_legacy_fail_test') !== null;
      window.HDH.Store.set = origSet; // restore

      return { rec, oldKeyStillExists, failKeyPreserved };
    });

    expect(result.rec.mastery_state).toBe('M1');
    expect(result.rec.mastery_evidence.verification_mode).toBe('LEGACY_SELF_REPORT');
    expect(result.oldKeyStillExists).toBe(false);
    expect(result.failKeyPreserved).toBe(true);
  });

  // -------------------------------------------------------------------------
  // Scenario 7: Corrupt localStorage Resilience (QA-LEARN-002 A)
  // -------------------------------------------------------------------------
  test('7. Corrupt localStorage does not crash runtime and falls back gracefully (QA-LEARN-002 A)', async ({ page }) => {
    await page.goto('/index.html');

    // Inject corrupt JSON into actual runtime storage keys
    await page.evaluate(() => {
      localStorage.setItem('hdh_mastery_v1', '{corrupt json!!!');
      localStorage.setItem('hdh_spaced_scheduler_v1', 'null');
      localStorage.setItem('hdh_practice_drafts_v1', '[invalid]');
      localStorage.setItem('hdh_mistakes_log_v1', '<<<not json>>>');
    });

    // Navigate to cards page - should not throw
    await page.goto('/flashcards/ch01-cards.html');

    const card = page.locator('#fc-01-mode-bit');
    await expect(card).toBeVisible();

    // Verify user can still interact and rate
    await card.locator('.btn-answer').click();
    const btnGood = card.locator('.btn-good');
    await expect(btnGood).toBeVisible();
    await btnGood.click();

    const badge = card.locator('.card-mastery-badge');
    await expect(badge).toHaveText('M1');
  });

  // -------------------------------------------------------------------------
  // Scenario 8: Mastery Separation, Evidence Invariant & DOM Interaction (MASTERY-LEARN-001, QA-LEARN-002 C)
  // -------------------------------------------------------------------------
  test('8. Mastery invariants and real M2/M3 DOM interaction test (QA-LEARN-002 C)', async ({ page }) => {
    await page.goto('/index.html');

    // Part A: Logical Invariants
    const evidenceTest = await page.evaluate(() => {
      const store = window.HDH.MasteryStore;

      // 1. Repeated review ratings on M1 card: NEVER grants M2
      for (let i = 0; i < 15; i++) {
        store.recordRating('mastery_test_card', 'EASY', Date.now());
      }
      const ratingOnlyState = store.getRecord('mastery_test_card').mastery_state;

      // 2. RecallCheckpoint rubric < 80%: does NOT grant M2
      store.recordRecallEvidence('mastery_test_card', true, 75);
      const sub80State = store.getRecord('mastery_test_card').mastery_state;

      // 3. RecallCheckpoint rubric >= 80%: GRANTS M2
      store.recordRecallEvidence('mastery_test_card', true, 80);
      const m2State = store.getRecord('mastery_test_card').mastery_state;

      // 4. TransferProblem from M1: does NOT grant M3 directly
      store.recordRating('transfer_card', 'GOOD', Date.now());
      store.recordTransferEvidence('transfer_card', true);
      const m1TransferState = store.getRecord('transfer_card').mastery_state;

      // 5. TransferProblem from M2: GRANTS M3
      store.recordRecallEvidence('transfer_card', true, 100); // promote to M2
      store.recordTransferEvidence('transfer_card', true);     // transfer passed
      const m3State = store.getRecord('transfer_card').mastery_state;

      return { ratingOnlyState, sub80State, m2State, m1TransferState, m3State };
    });

    expect(evidenceTest.ratingOnlyState).toBe('M1');
    expect(evidenceTest.sub80State).toBe('M1');
    expect(evidenceTest.m2State).toBe('M2');
    expect(evidenceTest.m1TransferState).toBe('M1');
    expect(evidenceTest.m3State).toBe('M3');

    // Part B: Real DOM interactive M2/M3 UI Click Handlers (QA-LEARN-002 C)
    await page.evaluate(() => {
      const container = document.createElement('div');
      container.id = 'dom-fixture-container';
      container.innerHTML = `
        <div class="recall-checkpoint" id="rc-fixture" data-item-id="rc-fixture" data-concept-id="fixture-concept" data-mastery="M0">
          <div class="checkpoint-header">
            <span class="card-tag">Recall Checkpoint</span>
            <span class="card-mastery-badge">M0</span>
            <span class="checkpoint-status">Chưa tự kiểm tra</span>
          </div>
          <div class="checkpoint-prompt">Nêu định nghĩa và điều kiện bế tắc.</div>
          <textarea class="checkpoint-scratchpad"></textarea>
          <div class="checkpoint-actions">
            <button type="button" class="btn-card btn-reveal-rubric" aria-expanded="false">📝 Mở Rubric</button>
          </div>
          <div class="rubric-container" style="display: none;" aria-hidden="true">
            <div class="rubric-items">
              <div class="rubric-item"><label><input type="checkbox" class="rubric-check" data-weight="1.0"> Điều kiện 1</label></div>
            </div>
            <div class="rubric-evaluation">
              <button type="button" class="btn-card primary btn-submit-recall">Tự đánh giá</button>
              <div class="recall-feedback"></div>
            </div>
          </div>
        </div>

        <div class="transfer-problem" id="tp-fixture" data-item-id="tp-fixture" data-concept-id="fixture-concept" data-mastery="M0">
          <div class="problem-header">
            <span class="card-tag">Transfer Problem</span>
            <span class="card-mastery-badge">M0</span>
            <span class="transfer-gate-status">Cần đạt cấp độ M2 trước khi kiểm tra M3</span>
          </div>
          <div class="problem-prompt">Bài toán chuyển giao tình huống thực tế.</div>
          <textarea class="transfer-scratchpad"></textarea>
          <div class="problem-actions">
            <button type="button" class="btn-card btn-reveal-transfer-solution" aria-expanded="false">🚀 Mở Lời giải</button>
          </div>
          <div class="transfer-solution-container" style="display: none;" aria-hidden="true">
            <div class="transfer-evaluation">
              <button type="button" class="btn-card success btn-transfer-pass">Đạt M3</button>
              <button type="button" class="btn-card danger btn-transfer-fail">Chưa đạt</button>
              <div class="transfer-feedback"></div>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(container);
      window.HDH.RecallCheckpointEngine.init();
      window.HDH.TransferProblemEngine.init();
    });

    const rc = page.locator('#rc-fixture');
    const tp = page.locator('#tp-fixture');

    // Verify initial M0 badges
    await expect(rc.locator('.card-mastery-badge')).toHaveText('M0');
    await expect(tp.locator('.card-mastery-badge')).toHaveText('M0');

    // Reveal transfer solution
    await tp.locator('.btn-reveal-transfer-solution').click();
    await expect(tp.locator('.transfer-solution-container')).toBeVisible();

    // Click transfer pass while at M0 -> blocked by gate!
    await tp.locator('.btn-transfer-pass').click();
    await expect(tp.locator('.transfer-feedback')).toContainText('Bạn phải hoàn thành M2');
    await expect(tp.locator('.card-mastery-badge')).toHaveText('M0');

    // Reveal RecallCheckpoint rubric
    await rc.locator('.btn-reveal-rubric').click();
    await expect(rc.locator('.rubric-container')).toBeVisible();

    // Check rubric item and submit recall
    await rc.locator('.rubric-check').check();
    await rc.locator('.btn-submit-recall').click();

    // Verified: promoted to M2
    await expect(rc.locator('.card-mastery-badge')).toHaveText('M2');
    await expect(rc.locator('.recall-feedback')).toContainText('Đạt M2 thành công');

    // Now click transfer pass -> promoted to M3!
    await tp.locator('.btn-transfer-pass').click();
    await expect(tp.locator('.card-mastery-badge')).toHaveText('M3');
    await expect(tp.locator('.transfer-feedback')).toContainText('Đạt chuẩn M3');
  });

  // -------------------------------------------------------------------------
  // Scenario 9: Review Hub Queue Rendering, Unified Eligibility & Badging (REVIEW-LEARN-003)
  // -------------------------------------------------------------------------
  test('9. Review Hub renders queue with unified eligibility, distinct badges, and deterministic tie ordering (REVIEW-LEARN-003)', async ({ page }) => {
    await page.goto('/index.html');

    // Seed test cases A-E:
    // A: fc-01-mode-bit: M1 weak, future due date -> eligible, badge-weak ("Cần củng cố"), score 100
    // B: fc-02-storage-criteria: M2 pending transfer, future due date -> eligible, badge-pending-transfer ("Chờ chuyển giao"), score 50
    // C: fc-03-multiprogramming-goal: mistake-linked, future due date -> eligible, badge-mistake ("Có lỗi sai"), score 40
    // D: fc-04-trap-definition: M3 future, 0 mistakes -> NOT eligible, excluded!
    // E: viva-lab01-hardlink-symlink: due M2, transfer passed -> eligible, badge-due ("Đến hạn"), score 30
    await page.evaluate(() => {
      const now = Date.now();
      const sched = {
        'fc-01-mode-bit': {
          reps: 1, ef: 2.5, interval_days: 10, due_timestamp: now + (10 * 86400000), lapses: 0
        },
        'fc-02-storage-criteria': {
          reps: 3, ef: 2.5, interval_days: 20, due_timestamp: now + (20 * 86400000), lapses: 0
        },
        'fc-03-multiprogramming-goal': {
          reps: 5, ef: 2.5, interval_days: 30, due_timestamp: now + (30 * 86400000), lapses: 0
        },
        'fc-04-trap-definition': {
          reps: 5, ef: 2.5, interval_days: 30, due_timestamp: now + (30 * 86400000), lapses: 0
        },
        'viva-lab01-hardlink-symlink': {
          reps: 2, ef: 2.5, interval_days: 1, due_timestamp: now - 86400000, lapses: 0 // OVERDUE
        }
      };
      const mastery = {
        // Case A: M1 weak
        'fc-01-mode-bit': {
          concept_id: 'fc-01-mode-bit',
          mastery_state: 'M1',
          mastery_evidence: { recall_passed: false, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-01-mode-bit'],
          review_rating_history: [],
          mistake_history: []
        },
        // Case B: M2 pending transfer
        'fc-02-storage-criteria': {
          concept_id: 'fc-02-storage-criteria',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-02-storage-criteria'],
          review_rating_history: [],
          mistake_history: []
        },
        // Case C: Mistake-linked M2
        'fc-03-multiprogramming-goal': {
          concept_id: 'fc-03-multiprogramming-goal',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: true, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-03-multiprogramming-goal'],
          review_rating_history: [],
          mistake_history: [{ timestamp: now - 100000, note: 'Error in scheduling concept' }]
        },
        // Case D: M3 future, transfer passed, no mistakes -> EXCLUDED!
        'fc-04-trap-definition': {
          concept_id: 'fc-04-trap-definition',
          mastery_state: 'M3',
          mastery_evidence: { recall_passed: true, transfer_passed: true, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-04-trap-definition'],
          review_rating_history: [],
          mistake_history: []
        },
        // Case E: Due M2
        'viva-lab01-hardlink-symlink': {
          concept_id: 'viva-lab01-hardlink-symlink',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: true, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['viva-lab01-hardlink-symlink'],
          review_rating_history: [],
          mistake_history: []
        }
      };
      localStorage.setItem('hdh_spaced_scheduler_v1', JSON.stringify(sched));
      localStorage.setItem('hdh_mastery_v1', JSON.stringify(mastery));
    });

    await page.goto('/review/index.html');

    const queue = page.locator('#review-hub-queue');
    await expect(queue).toBeVisible();

    // Check stats counters
    await expect(page.locator('#hub-due-count')).toHaveText('1');
    await expect(page.locator('#hub-weak-count')).toHaveText('1');
    await expect(page.locator('#hub-pending-count')).toHaveText('1');
    await expect(page.locator('#hub-mistake-count')).toHaveText('1');
    await expect(page.locator('#hub-total-count')).toHaveText('5');

    // Case D: Future M3 must NOT appear in queue
    await expect(queue.locator('[data-hub-card-id="fc-04-trap-definition"]')).toHaveCount(0);

    // Case F: Deterministic priority order check:
    // 1st: viva-lab01-hardlink-symlink (score 30, badge-due)
    // 2nd: fc-03-multiprogramming-goal (score 40, badge-mistake)
    // 3rd: fc-02-storage-criteria (score 50, badge-pending-transfer)
    // 4th: fc-01-mode-bit (score 100, badge-weak)
    const cards = queue.locator('.review-queue-card');
    await expect(cards).toHaveCount(4);

    // Card 1
    const card1 = cards.nth(0);
    expect(await card1.getAttribute('data-hub-card-id')).toBe('viva-lab01-hardlink-symlink');
    await expect(card1.locator('.queue-status-badge')).toHaveClass(/badge-due/);
    await expect(card1.locator('.queue-status-badge')).toHaveText('Đến hạn');

    // Card 2
    const card2 = cards.nth(1);
    expect(await card2.getAttribute('data-hub-card-id')).toBe('fc-03-multiprogramming-goal');
    await expect(card2.locator('.queue-status-badge')).toHaveClass(/badge-mistake/);
    await expect(card2.locator('.queue-status-badge')).toHaveText('Có lỗi sai');

    // Card 3
    const card3 = cards.nth(2);
    expect(await card3.getAttribute('data-hub-card-id')).toBe('fc-02-storage-criteria');
    await expect(card3.locator('.queue-status-badge')).toHaveClass(/badge-pending-transfer/);
    await expect(card3.locator('.queue-status-badge')).toHaveText('Chờ chuyển giao');

    // Card 4
    const card4 = cards.nth(3);
    expect(await card4.getAttribute('data-hub-card-id')).toBe('fc-01-mode-bit');
    await expect(card4.locator('.queue-status-badge')).toHaveClass(/badge-weak/);
    await expect(card4.locator('.queue-status-badge')).toHaveText('Cần củng cố');
  });

  // -------------------------------------------------------------------------
  // Scenario 10: Accessibility - ARIA Controls & Keyboard Operability (A11Y-LEARN-001)
  // -------------------------------------------------------------------------
  test('10. Accessibility: All aria-controls resolve to valid elements and are keyboard operable', async ({ page }) => {
    await page.goto('/flashcards/ch01-cards.html');

    // Check all aria-controls on the page resolve
    const unresolved = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('[aria-controls]'));
      const missing = [];
      buttons.forEach(btn => {
        const targetId = btn.getAttribute('aria-controls');
        if (targetId && !document.getElementById(targetId)) {
          missing.push(targetId);
        }
      });
      return missing;
    });
    expect(unresolved).toEqual([]);

    // Test keyboard activation of reveal button
    const card = page.locator('#fc-01-mode-bit');
    const btnHint = card.locator('.btn-hint');
    await btnHint.focus();
    await page.keyboard.press('Enter');

    const hint = card.locator('#fc-01-mode-bit__hint');
    await expect(hint).toBeVisible();
    expect(await btnHint.getAttribute('aria-expanded')).toBe('true');
  });

  // -------------------------------------------------------------------------
  // -------------------------------------------------------------------------
  // Scenario 11: Mobile Viewport Usability & Review Hub Shortcut at 390px (QA-LEARN-002 D, UX-LEARN-001)
  // -------------------------------------------------------------------------
  test('11. Mobile usability at 390px: no scroll overflow, review shortcut visible/clickable, and controls operable', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });

    const pagesToCheck = [
      '/index.html',
      '/flashcards/ch01-cards.html',
      '/review/index.html'
    ];

    for (const p of pagesToCheck) {
      await page.goto(p);
      const isOverflowing = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });
      expect(isOverflowing, `Page ${p} has horizontal scroll overflow on 390px viewport`).toBe(false);
    }

    // UX-LEARN-001: Test review shortcut on mobile
    await page.goto('/flashcards/ch01-cards.html');
    const reviewModeBtn = page.locator('button[data-mode="review"]');
    await expect(reviewModeBtn).toBeVisible();
    await reviewModeBtn.click();

    const shortcut = page.locator('#review-hub-shortcut');
    await expect(shortcut).toBeVisible();
    await shortcut.click();

    // Must navigate to /review/index.html
    await page.waitForURL('**/review/index.html');
    expect(page.url()).toContain('review/index.html');

    // Test mobile interaction on card: mode button, answer reveal, rating clickability
    await page.goto('/flashcards/ch01-cards.html');
    const card = page.locator('#fc-01-mode-bit');
    const btnAnswer = card.locator('.btn-answer');
    await expect(btnAnswer).toBeVisible();
    await btnAnswer.click();

    const btnGood = card.locator('.btn-good');
    await expect(btnGood).toBeVisible();
    await btnGood.click();

    const badge = card.locator('.card-mastery-badge');
    await expect(badge).toHaveText('M1');
  });

  // -------------------------------------------------------------------------
  // Scenario 12: Zero Console / Page Errors (QA-LEARN-002 B)
  // -------------------------------------------------------------------------
  test('12. Console cleanliness: No uncaught page errors or console.errors across core pages', async ({ page }) => {
    const pageErrors = [];
    const consoleErrors = [];
    page.on('pageerror', (err) => pageErrors.push(err.message));
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    const pagesToVisit = [
      '/index.html',
      '/theory/ch01-overview.html',
      '/flashcards/ch01-cards.html',
      '/review/index.html'
    ];

    for (const p of pagesToVisit) {
      await page.goto(p);
      await page.waitForLoadState('domcontentloaded');
    }

    expect(pageErrors).toEqual([]);
    expect(consoleErrors).toEqual([]);
  });

});

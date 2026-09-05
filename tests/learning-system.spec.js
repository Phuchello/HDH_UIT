// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('HDH_UIT V2 Deterministic Learning System Browser Suite', () => {

  test.beforeEach(async ({ page }) => {
    // Clear localStorage before each test
    await page.goto('/index.html');
    await page.evaluate(() => localStorage.clear());
  });

  // -------------------------------------------------------------------------
  // Scenario 1: Learn Mode - Progressive Disclosure & Rating Unlock (PED-LEARN-004)
  // -------------------------------------------------------------------------
  test('1. Learn Mode enforces progressive disclosure and hides ratings until reveal', async ({ page }) => {
    await page.goto('/flashcards/ch01-cards.html');

    const card = page.locator('#fc-01-mode-bit');
    await expect(card).toBeVisible();

    const hint = card.locator('#fc-01-mode-bit__hint');
    const answer = card.locator('#fc-01-mode-bit__answer');
    const ratingActions = card.locator('#fc-01-mode-bit__rating_actions');

    // Initially hidden
    await expect(hint).toBeHidden();
    await expect(answer).toBeHidden();
    await expect(ratingActions).toBeHidden();

    // Click reveal answer
    const btnAnswer = card.locator('.btn-answer');
    await btnAnswer.click();

    // Answer revealed
    await expect(answer).toBeVisible();
    expect(await btnAnswer.getAttribute('aria-expanded')).toBe('true');

    // Rating controls unlocked and visible
    await expect(ratingActions).toBeVisible();
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
  // Scenario 6: Legacy Card Migration
  // -------------------------------------------------------------------------
  test('6. Legacy flashcard ratings migrate cleanly to M1 with LEGACY_SELF_REPORT', async ({ page }) => {
    await page.goto('/index.html');

    const migrated = await page.evaluate(() => {
      localStorage.setItem('hdh_card_legacy_ch01_test', JSON.stringify({
        remembered: true,
        timestamp: Date.now() - 500000
      }));
      window.HDH.Migration.migrateLegacyCards();
      const rec = window.HDH.MasteryStore.getRecord('legacy_ch01_test');
      const oldKeyStillExists = localStorage.getItem('hdh_card_legacy_ch01_test') !== null;
      return { rec, oldKeyStillExists };
    });

    expect(migrated.rec.mastery_state).toBe('M1');
    expect(migrated.rec.mastery_evidence.verification_mode).toBe('LEGACY_SELF_REPORT');
    expect(migrated.oldKeyStillExists).toBe(false);
  });

  // -------------------------------------------------------------------------
  // Scenario 7: Corrupt localStorage Resilience
  // -------------------------------------------------------------------------
  test('7. Corrupt localStorage does not crash runtime and falls back gracefully', async ({ page }) => {
    await page.goto('/index.html');

    // Inject corrupt JSON into storage
    await page.evaluate(() => {
      localStorage.setItem('hdh_learning_mastery_v1', '{corrupt json!!!');
      localStorage.setItem('hdh_learning_schedule_v1', 'null');
      localStorage.setItem('hdh_practice_drafts_v1', '[invalid]');
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
  // Scenario 8: Mastery Separation & Evidence Invariant (MASTERY-LEARN-001)
  // -------------------------------------------------------------------------
  test('8. Mastery invariants: review ratings cannot grant M2/M3; rubric >= 80% required for M2; transfer required for M3', async ({ page }) => {
    await page.goto('/index.html');

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
  });

  // -------------------------------------------------------------------------
  // Scenario 9: Review Hub Queue Rendering & Filtering (REVIEW-LEARN-001)
  // -------------------------------------------------------------------------
  test('9. Review Hub displays due/overdue cards, excludes future cards, and links to target anchor', async ({ page }) => {
    await page.goto('/index.html');

    // Seed one card overdue and mark one card as mastered M2 due in 30 days
    await page.evaluate(() => {
      const now = Date.now();
      const sched = {
        'fc-01-mode-bit': {
          reps: 1, ef: 2.5, interval_days: 1, due_timestamp: now - 86400000, lapses: 0 // DUE
        },
        'fc-02-storage-criteria': {
          reps: 5, ef: 2.5, interval_days: 30, due_timestamp: now + (30 * 86400000), lapses: 0 // FUTURE
        },
        'fc-03-multiprogramming-goal': {
          reps: 5, ef: 2.5, interval_days: 30, due_timestamp: now + (30 * 86400000), lapses: 0
        },
        'fc-04-trap-definition': {
          reps: 5, ef: 2.5, interval_days: 30, due_timestamp: now + (30 * 86400000), lapses: 0
        },
        'viva-lab01-hardlink-symlink': {
          reps: 5, ef: 2.5, interval_days: 30, due_timestamp: now + (30 * 86400000), lapses: 0
        }
      };
      const mastery = {
        'fc-01-mode-bit': {
          concept_id: 'fc-01-mode-bit',
          mastery_state: 'M1',
          mastery_evidence: { recall_passed: false, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-01-mode-bit'],
          review_rating_history: [],
          mistake_history: []
        },
        'fc-02-storage-criteria': {
          concept_id: 'fc-02-storage-criteria',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-02-storage-criteria'],
          review_rating_history: [],
          mistake_history: []
        },
        'fc-03-multiprogramming-goal': {
          concept_id: 'fc-03-multiprogramming-goal',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-03-multiprogramming-goal'],
          review_rating_history: [],
          mistake_history: []
        },
        'fc-04-trap-definition': {
          concept_id: 'fc-04-trap-definition',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['fc-04-trap-definition'],
          review_rating_history: [],
          mistake_history: []
        },
        'viva-lab01-hardlink-symlink': {
          concept_id: 'viva-lab01-hardlink-symlink',
          mastery_state: 'M2',
          mastery_evidence: { recall_passed: true, transfer_passed: false, verification_mode: 'SELF_ASSESSED' },
          review_schedule: sched['viva-lab01-hardlink-symlink'],
          review_rating_history: [],
          mistake_history: []
        }
      };
      localStorage.setItem('hdh_spaced_scheduler_v1', JSON.stringify(sched));
      localStorage.setItem('hdh_mastery_v1', JSON.stringify(mastery));
    });

    await page.goto('/review/index.html');

    // Wait for queue container
    const queue = page.locator('#review-hub-queue');
    await expect(queue).toBeVisible();

    // Due card must appear in queue
    const dueCard = queue.locator('[data-hub-card-id="fc-01-mode-bit"]');
    await expect(dueCard).toBeVisible();

    // Future card must NOT appear in queue
    const futureCard = queue.locator('[data-hub-card-id="fc-02-storage-criteria"]');
    await expect(futureCard).toHaveCount(0);

    // Verify study link points to card anchor
    const studyLink = dueCard.locator('a.btn-card');
    const href = await studyLink.getAttribute('href');
    expect(href).toContain('flashcards/ch01-cards.html#fc-01-mode-bit');
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
  // Scenario 11: Mobile Viewport Responsiveness (390px)
  // -------------------------------------------------------------------------
  test('11. Mobile responsiveness: 390px viewport does not cause horizontal scroll overflow', async ({ page }) => {
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
  });

  // -------------------------------------------------------------------------
  // Scenario 12: Zero Console / Page Errors
  // -------------------------------------------------------------------------
  test('12. Console cleanliness: No uncaught page errors across core pages', async ({ page }) => {
    const pageErrors = [];
    page.on('pageerror', (err) => pageErrors.push(err.message));

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
  });

});

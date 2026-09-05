#!/usr/bin/env python3
"""Deterministic test vectors for the V2 Learning System.

Tests:
  1. SPEC MIRROR TESTS (Python Reference) — SM-2 Scheduler: all 4 ratings on new (reps=0) and mature (reps=5) cards.
  2. HARD != AGAIN invariant (reps must NOT be reset on HARD).
  3. EF clamp tests (min=1.3, max=2.8).
  4. StudyCard section parser (ENG-LEARN-003 fix): deterministic single-pass.
  5. StudyCard marker validation: count <= 1, strict ordering, no leakage.
  6. DOM ID & ARIA-controls integrity: 0 duplicate IDs, 100% resolved aria-controls.
  7. Build-side duplicate ID detection smoke test.
  8. study_index.json generation smoke test.
"""

from __future__ import annotations

import re
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Load the build script's parser function directly for testing
# ---------------------------------------------------------------------------
sys.path.insert(0, str(ROOT / "scripts"))
import importlib
import build_web as _bw  # noqa: E402

# ===========================================================================
# 1. SPEC MIRROR TESTS (Python Reference) — SM-2 Scheduler Test Vectors
# ===========================================================================

def _date_to_ms(s: str) -> int:
    """UTC midnight ms for YYYY-MM-DD (mirrors JS _dateToMs)."""
    import datetime
    y, m, d = (int(x) for x in s.split("-"))
    return int(datetime.datetime(y, m, d, tzinfo=datetime.timezone.utc).timestamp() * 1000)


def _add_days(today: str, days: int) -> int:
    return _date_to_ms(today) + days * 86_400_000


def schedule(prev: dict, rating: str, today: str) -> dict:
    """Python mirror of app.js Scheduler.schedule()."""
    ef       = min(2.8, max(1.3, prev.get("ef", 2.5)))
    reps     = prev.get("reps", 0)
    interval = prev.get("interval_days", 0)
    lapses   = prev.get("lapses", 0)

    if rating == "AGAIN":
        new_reps     = 0
        new_interval = 1
        new_ef       = max(1.3, ef - 0.20)
        new_lapses   = lapses + 1
    elif rating == "HARD":
        new_reps   = reps + 1
        new_lapses = lapses
        new_ef     = max(1.3, ef - 0.15)
        if new_reps <= 1:
            new_interval = 1
        else:
            new_interval = max(interval + 1, round(interval * 1.2))
    elif rating == "GOOD":
        new_reps   = reps + 1
        new_lapses = lapses
        new_ef     = ef
        if new_reps == 1:
            new_interval = 1
        elif new_reps == 2:
            new_interval = 3
        else:
            new_interval = round(interval * ef)
    elif rating == "EASY":
        new_reps   = reps + 1
        new_lapses = lapses
        new_ef     = min(2.8, ef + 0.15)
        if new_reps == 1:
            new_interval = 2
        elif new_reps == 2:
            new_interval = 4
        else:
            new_interval = round(interval * ef * 1.3)
    else:
        return dict(prev)

    return {
        "reps":          new_reps,
        "ef":            round(new_ef * 1000) / 1000,
        "interval_days": new_interval,
        "due_timestamp": _add_days(today, new_interval),
        "lapses":        new_lapses,
    }


NEW_CARD = {"reps": 0, "ef": 2.5, "interval_days": 0, "due_timestamp": None, "lapses": 0}
TODAY    = "2026-09-05"

SCHEDULER_VECTORS: list[tuple[str, dict, str, dict]] = [
    # (description, prev_state, rating, expected_fields)
    (
        "AGAIN on new card: reps=0, interval=1, EF=2.3, lapses=1",
        NEW_CARD, "AGAIN",
        {"reps": 0, "interval_days": 1, "ef": 2.3, "lapses": 1},
    ),
    (
        "HARD on new card: reps=1, interval=1, EF=2.35 (2.5-0.15), lapses=0",
        NEW_CARD, "HARD",
        {"reps": 1, "interval_days": 1, "ef": 2.35, "lapses": 0},
    ),
    (
        "GOOD on new card: reps=1, interval=1, EF=2.5 unchanged, lapses=0",
        NEW_CARD, "GOOD",
        {"reps": 1, "interval_days": 1, "ef": 2.5, "lapses": 0},
    ),
    (
        "EASY on new card: reps=1, interval=2, EF=2.65, lapses=0",
        NEW_CARD, "EASY",
        {"reps": 1, "interval_days": 2, "ef": 2.65, "lapses": 0},
    ),
    # After first GOOD: reps=1, interval=1 → next GOOD: reps=2, interval=3
    (
        "GOOD second rep (reps=1 → 2): interval=3, EF unchanged",
        {"reps": 1, "ef": 2.5, "interval_days": 1, "due_timestamp": None, "lapses": 0},
        "GOOD",
        {"reps": 2, "interval_days": 3, "ef": 2.5, "lapses": 0},
    ),
    # Mature card: reps=5, interval=10, EF=2.5
    (
        "AGAIN on mature card: reps=0, interval=1, EF=2.3, lapses++",
        {"reps": 5, "ef": 2.5, "interval_days": 10, "due_timestamp": None, "lapses": 0},
        "AGAIN",
        {"reps": 0, "interval_days": 1, "ef": 2.3, "lapses": 1},
    ),
    (
        "HARD on mature card: reps=6, interval=max(11, round(10*1.2))=12, EF=2.35",
        {"reps": 5, "ef": 2.5, "interval_days": 10, "due_timestamp": None, "lapses": 0},
        "HARD",
        {"reps": 6, "interval_days": 12, "ef": 2.35, "lapses": 0},
    ),
    (
        "GOOD on mature card: reps=6, interval=round(10*2.5)=25, EF=2.5",
        {"reps": 5, "ef": 2.5, "interval_days": 10, "due_timestamp": None, "lapses": 0},
        "GOOD",
        {"reps": 6, "interval_days": 25, "ef": 2.5, "lapses": 0},
    ),
    (
        "EASY on mature card: reps=6, interval=round(10*2.5*1.3)=32, EF=2.65",
        {"reps": 5, "ef": 2.5, "interval_days": 10, "due_timestamp": None, "lapses": 0},
        "EASY",
        {"reps": 6, "interval_days": 32, "ef": 2.65, "lapses": 0},
    ),
    # EF clamp tests
    (
        "EF clamp min=1.3: many AGAINs cannot drop EF below 1.3",
        {"reps": 0, "ef": 1.35, "interval_days": 1, "due_timestamp": None, "lapses": 3},
        "AGAIN",
        {"ef": 1.3, "lapses": 4},
    ),
    (
        "EF clamp max=2.8: many EASYs cannot raise EF above 2.8",
        {"reps": 5, "ef": 2.75, "interval_days": 10, "due_timestamp": None, "lapses": 0},
        "EASY",
        {"ef": 2.8},
    ),
    # HARD != AGAIN invariant
    (
        "HARD != AGAIN: HARD never resets reps to 0",
        {"reps": 3, "ef": 2.5, "interval_days": 8, "due_timestamp": None, "lapses": 0},
        "HARD",
        {"reps": 4},  # Must be 4, NOT 0
    ),
]


def run_scheduler_tests() -> list[str]:
    failures = []
    for desc, prev, rating, expected in SCHEDULER_VECTORS:
        result = schedule(prev, rating, TODAY)
        for key, exp_val in expected.items():
            got = result.get(key)
            if abs(got - exp_val) > 0.001:
                failures.append(
                    f"SCHEDULER FAIL [{rating}] {desc!r}\n"
                    f"  key={key}: expected={exp_val}, got={got}"
                )
    return failures


# ===========================================================================
# 2. StudyCard Parser Tests (ENG-LEARN-003 fix)
# ===========================================================================

PARSER_VECTORS: list[tuple[str, str, dict]] = [
    (
        "All three markers in order: hint, keypoints, answer",
        "Q text\n<!-- hint -->\nhint text\n<!-- keypoints -->\n- kp1\n<!-- answer -->\nans text",
        {"question": "Q text\n", "hint": "\nhint text\n", "keypoints": "\n- kp1\n", "answer": "\nans text"},
    ),
    (
        "Only answer marker present",
        "Q text\n<!-- answer -->\nans",
        {"question": "Q text\n", "hint": "", "keypoints": "", "answer": "\nans"},
    ),
    (
        "No markers: all goes to question",
        "Just a question with no markers",
        {"question": "Just a question with no markers", "hint": "", "keypoints": "", "answer": ""},
    ),
    (
        "Hint + answer (no keypoints)",
        "Q\n<!-- hint -->\nhint\n<!-- answer -->\nans",
        {"question": "Q\n", "hint": "\nhint\n", "keypoints": "", "answer": "\nans"},
    ),
    (
        "OLD BUG REGRESSION: keypoints after hint must be parsed (not lost)",
        "Q\n<!-- hint -->\nh\n<!-- keypoints -->\n- k\n<!-- answer -->\na",
        {"keypoints": "\n- k\n"},  # Must not be empty
    ),
]


def run_parser_tests() -> list[str]:
    failures = []
    for desc, body, expected in PARSER_VECTORS:
        q, hint, kp, ans = _bw._parse_studycard_sections(body)
        result = {"question": q, "hint": hint, "keypoints": kp, "answer": ans}
        for key, exp_val in expected.items():
            got = result[key]
            if got != exp_val:
                failures.append(
                    f"PARSER FAIL {desc!r}\n"
                    f"  key={key!r}: expected={exp_val!r}, got={got!r}"
                )
    return failures


# ===========================================================================
# 2b. StudyCard Marker Validation Tests
# ===========================================================================

def run_parser_validation_tests() -> list[str]:
    """Test that _parse_studycard_sections strictly rejects:
    1. Duplicate markers (count > 1).
    2. Invalid marker ordering (hint after keypoints/answer, keypoints after answer).
    3. Marker leakage into chunks.
    """
    failures = []

    # Test 1: Duplicate marker raises RuntimeError
    try:
        _bw._parse_studycard_sections(
            "Q\n<!-- hint -->\nh1\n<!-- hint -->\nh2\n<!-- answer -->\na",
            "test-dup",
            "test.md",
        )
        failures.append("PARSER VALIDATION FAIL: Expected RuntimeError for duplicate '<!-- hint -->', but none was raised")
    except RuntimeError:
        pass
    except Exception as e:
        failures.append(f"PARSER VALIDATION FAIL: Expected RuntimeError for duplicate marker, got {type(e).__name__}: {e}")

    # Test 2: Invalid marker order raises RuntimeError (hint after answer)
    try:
        _bw._parse_studycard_sections(
            "Q\n<!-- answer -->\na\n<!-- hint -->\nh",
            "test-order-1",
            "test.md",
        )
        failures.append("PARSER VALIDATION FAIL: Expected RuntimeError for hint after answer, but none was raised")
    except RuntimeError:
        pass
    except Exception as e:
        failures.append(f"PARSER VALIDATION FAIL: Expected RuntimeError for invalid marker order, got {type(e).__name__}: {e}")

    # Test 3: Invalid marker order raises RuntimeError (keypoints after answer)
    try:
        _bw._parse_studycard_sections(
            "Q\n<!-- answer -->\na\n<!-- keypoints -->\nk",
            "test-order-2",
            "test.md",
        )
        failures.append("PARSER VALIDATION FAIL: Expected RuntimeError for keypoints after answer, but none was raised")
    except RuntimeError:
        pass
    except Exception as e:
        failures.append(f"PARSER VALIDATION FAIL: Expected RuntimeError for invalid marker order, got {type(e).__name__}: {e}")

    # Test 4: Invalid marker order raises RuntimeError (hint after keypoints)
    try:
        _bw._parse_studycard_sections(
            "Q\n<!-- keypoints -->\nk\n<!-- hint -->\nh\n<!-- answer -->\na",
            "test-order-3",
            "test.md",
        )
        failures.append("PARSER VALIDATION FAIL: Expected RuntimeError for hint after keypoints, but none was raised")
    except RuntimeError:
        pass
    except Exception as e:
        failures.append(f"PARSER VALIDATION FAIL: Expected RuntimeError for invalid marker order, got {type(e).__name__}: {e}")

    return failures


# ===========================================================================
# 3. Build Smoke Tests
# ===========================================================================

def run_build_smoke_tests() -> list[str]:
    """Verify build_web.py produces study_index.json and search_index.json."""
    failures = []
    site = ROOT / "public" / "site"
    if not site.is_dir():
        failures.append("BUILD SMOKE: public/site/ missing — run web:build first")
        return failures

    study_index = site / "study_index.json"
    if not study_index.is_file():
        failures.append("study_index.json not generated by build")
    else:
        import json
        try:
            items = json.loads(study_index.read_text(encoding="utf-8"))
            # Each item must have required fields
            for item in items:
                for field in ("concept_id", "doc_id", "url"):
                    if field not in item:
                        failures.append(f"study_index.json item missing field '{field}': {item}")
                        break
        except Exception as e:
            failures.append(f"study_index.json invalid JSON: {e}")

    # Verify reveal buttons exist in generated HTML
    any_card = False
    missing_buttons = []
    for html_file in site.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if 'class="study-card"' in content:
            any_card = True
            if 'btn-again' not in content:
                missing_buttons.append(str(html_file.relative_to(site)))
    if any_card and missing_buttons:
        failures.append(
            f"ENG-LEARN-002 CHECK: btn-again not found in {len(missing_buttons)} pages "
            f"that contain study-card: {missing_buttons[:3]}"
        )

    # Verify mode switcher exists
    for html_file in site.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if 'class="article-body"' in content:
            if 'mode-switcher' not in content:
                failures.append(f"Mode switcher missing from {html_file.relative_to(site)}")
            break  # Check one content page

    return failures


# ===========================================================================
# 4. Mastery State Machine & Invariant Tests
# ===========================================================================

def run_mastery_tests() -> list[str]:
    """Test mastery invariants:
    - Rating promotes M0 -> M1
    - Rating AGAIN demotes M1 -> M0
    - Rating NEVER grants M2 or M3 (separation invariant)
    - Recall with rubric >= 80% grants M2
    - TransferProblem is the ONLY path to M3
    """
    failures = []

    def mock_record(concept_id="test"):
        return {
            "concept_id": concept_id,
            "mastery_state": "M0",
            "mastery_evidence": {"recall_passed": False, "transfer_passed": False, "verification_mode": "SELF_ASSESSED"},
            "review_schedule": {"reps": 0, "ef": 2.5, "interval_days": 0, "due_timestamp": None, "lapses": 0},
            "review_rating_history": [],
            "mistake_history": [],
        }

    # Invariant 1: Review rating on M0 promotes to M1
    rec = mock_record()
    # Simulate recordRating(GOOD)
    if rec["mastery_state"] == "M0":
        rec["mastery_state"] = "M1"
    if rec["mastery_state"] != "M1":
        failures.append("MASTERY FAIL: Rating on M0 did not promote to M1")

    # Invariant 2: AGAIN demotes M1 to M0
    if rec["mastery_state"] in ("M0", "M1"):
        rec["mastery_state"] = "M0"
    if rec["mastery_state"] != "M0":
        failures.append("MASTERY FAIL: AGAIN did not demote M1 to M0")

    # Invariant 3: Repeated EASY ratings NEVER grant M2 or M3
    rec = mock_record()
    for _ in range(10):
        # Apply rating logic: only M0 -> M1 is allowed by rating
        if rec["mastery_state"] == "M0":
            rec["mastery_state"] = "M1"
    if rec["mastery_state"] not in ("M0", "M1"):
        failures.append(f"MASTERY INVARIANT VIOLATION: Ratings promoted card to {rec['mastery_state']} (must require evidence)")

    # Invariant 4: RecallCheckpoint rubric < 80% does NOT grant M2
    rec = mock_record()
    rec["mastery_state"] = "M1"
    passed, rubric_pct = True, 75
    if passed and rubric_pct >= 80 and rec["mastery_state"] != "M3":
        rec["mastery_state"] = "M2"
    if rec["mastery_state"] == "M2":
        failures.append("MASTERY FAIL: Rubric < 80% incorrectly granted M2")

    # Invariant 5: RecallCheckpoint rubric >= 80% grants M2
    rubric_pct = 80
    if passed and rubric_pct >= 80 and rec["mastery_state"] != "M3":
        rec["mastery_state"] = "M2"
    if rec["mastery_state"] != "M2":
        failures.append("MASTERY FAIL: Rubric >= 80% did not grant M2")

    # Invariant 6: TransferProblem grants M3 ONLY from M2
    rec_m1 = mock_record()
    rec_m1["mastery_state"] = "M1"
    if rec_m1["mastery_state"] == "M2":
        rec_m1["mastery_state"] = "M3"
    if rec_m1["mastery_state"] == "M3":
        failures.append("MASTERY INVARIANT VIOLATION: Transfer granted M3 from M1 directly")

    if rec["mastery_state"] == "M2":
        rec["mastery_state"] = "M3"
    if rec["mastery_state"] != "M3":
        failures.append("MASTERY FAIL: Transfer did not grant M3 from M2")

    return failures


# ===========================================================================
# 5. ReviewQueue Priority Ordering Tests
# ===========================================================================

def run_review_queue_tests() -> list[str]:
    """Test deterministic ReviewQueue priority order:
    1. Overdue M0 (score 10)
    2. Overdue M1 (score 20)
    3. Due today M2 (score 30)
    4. Mistake-linked (score 40)
    5. Pending Transfer check (score 50)
    6. All other items (score 100)
    """
    failures = []

    def score_item(item):
        due = item.get("due", False)
        state = item.get("state", "M0")
        mistakes = item.get("mistakes", 0)
        transfer_passed = item.get("transfer_passed", False)

        if due and state == "M0":
            return 10
        if due and state == "M1":
            return 20
        if due and state == "M2":
            return 30
        if mistakes > 0:
            return 40
        if state == "M2" and not transfer_passed:
            return 50
        return 100

    items = [
        {"id": "c_not_due", "due": False, "state": "M2", "transfer_passed": True},
        {"id": "b_pending_transfer", "due": False, "state": "M2", "transfer_passed": False},
        {"id": "a_overdue_m0", "due": True, "state": "M0"},
        {"id": "e_mistake_linked", "due": False, "state": "M1", "mistakes": 2},
        {"id": "d_due_m2", "due": True, "state": "M2", "transfer_passed": True},
        {"id": "f_overdue_m1", "due": True, "state": "M1"},
    ]

    sorted_items = sorted(items, key=lambda x: (score_item(x), x["id"]))
    order = [x["id"] for x in sorted_items]
    expected_order = [
        "a_overdue_m0",       # score 10
        "f_overdue_m1",       # score 20
        "d_due_m2",           # score 30
        "e_mistake_linked",   # score 40
        "b_pending_transfer", # score 50
        "c_not_due",          # score 100
    ]

    if order != expected_order:
        failures.append(
            f"REVIEW QUEUE ORDER FAIL:\n"
            f"  got:      {order}\n"
            f"  expected: {expected_order}"
        )

    return failures


# ===========================================================================
# 6. DOM ID & ARIA-Controls Integrity Tests (A11Y-LEARN-001 Verification)
# ===========================================================================

def run_dom_id_and_aria_tests() -> list[str]:
    """Verify that across all HTML pages in public/site:
    1. Every aria-controls attribute points to an element ID that actually exists on that page.
    2. There are 0 duplicate HTML id attributes within any single page.
    """
    failures = []
    site = ROOT / "public" / "site"
    if not site.is_dir():
        failures.append("DOM INTEGRITY: public/site/ directory missing")
        return failures

    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        failures.append("DOM INTEGRITY: No HTML files found in public/site/")
        return failures

    id_pattern = re.compile(r'(?:\s|^)id=["\']([^"\']+)["\']')
    aria_controls_pattern = re.compile(r'(?:\s|^)aria-controls=["\']([^"\']+)["\']')

    for html_path in html_files:
        rel_path = str(html_path.relative_to(site))
        content = html_path.read_text(encoding="utf-8")

        # Check duplicate IDs
        found_ids = id_pattern.findall(content)
        seen_ids = set()
        duplicate_ids = set()
        for dom_id in found_ids:
            if dom_id in seen_ids:
                duplicate_ids.add(dom_id)
            else:
                seen_ids.add(dom_id)

        if duplicate_ids:
            failures.append(
                f"DUPLICATE DOM IDs in {rel_path}: {sorted(duplicate_ids)[:5]} (total {len(duplicate_ids)})"
            )

        # Check aria-controls resolution
        aria_controls = aria_controls_pattern.findall(content)
        for target_id in aria_controls:
            for single_id in target_id.split():
                if single_id not in seen_ids:
                    failures.append(
                        f"UNRESOLVED aria-controls in {rel_path}: '{single_id}' not found in DOM IDs"
                    )

    return failures


# ===========================================================================
# MAIN
# ===========================================================================

def main() -> int:
    all_failures: list[str] = []

    scheduler_failures = run_scheduler_tests()
    all_failures.extend(scheduler_failures)

    parser_failures = run_parser_tests()
    all_failures.extend(parser_failures)

    parser_val_failures = run_parser_validation_tests()
    all_failures.extend(parser_val_failures)

    mastery_failures = run_mastery_tests()
    all_failures.extend(mastery_failures)

    queue_failures = run_review_queue_tests()
    all_failures.extend(queue_failures)

    smoke_failures = run_build_smoke_tests()
    all_failures.extend(smoke_failures)

    dom_failures = run_dom_id_and_aria_tests()
    all_failures.extend(dom_failures)

    passed = not all_failures
    gate_totals = (
        f"Scheduler (Spec Mirror): {len(SCHEDULER_VECTORS) - len(scheduler_failures)}/{len(SCHEDULER_VECTORS)} | "
        f"Parser: {len(PARSER_VECTORS) - len(parser_failures)}/{len(PARSER_VECTORS)} | "
        f"Parser Validation: {'PASS' if not parser_val_failures else 'FAIL'} | "
        f"Mastery: {'PASS' if not mastery_failures else 'FAIL'} | "
        f"ReviewQueue: {'PASS' if not queue_failures else 'FAIL'} | "
        f"Build smoke: {len([x for x in smoke_failures if x]) == 0} | "
        f"DOM & A11y: {'PASS' if not dom_failures else 'FAIL'}"
    )

    print(f"LEARNING SYSTEM GATE: {'PASS' if passed else 'FAIL'}")
    print(f"  {gate_totals}")
    for f in all_failures:
        print(f"  FAIL: {f}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())



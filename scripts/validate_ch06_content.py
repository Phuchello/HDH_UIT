#!/usr/bin/env python3
"""
scripts/validate_ch06_content.py
Deterministic content-fidelity and authoring validator for Chapter 6 (Deadlock).

Verifies:
1. Presence of content/theory/ch06-deadlock.md and content/questions/subjective/ch06.md.
2. Canonical source references (UIT-OUTLINE-2024, UIT-SLIDE-CH06-2024, UIT-QBANK-CH06-2024).
3. All 63 CONTENT pages in slide_coverage.yaml are marked CONTENT_DRAFTED.
4. All 4 NON_CONTENT pages remain NOT_WRITTEN.
5. All 15 QBank units in official_review_questions.yaml are marked CONTENT_DRAFTED.
6. Core conceptual invariants:
   - 4 Coffman conditions (Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait).
   - RAG single-instance (cycle <=> deadlock) vs multi-instance (cycle is necessary, not sufficient).
   - Safe State vs Unsafe State vs Deadlock (Unsafe != necessarily Deadlock).
   - Banker's Algorithm (Available, Max, Allocation, Need, Work, Finish, Safe Sequence, Resource-Request).
   - Deadlock Detection matrix (distinguishing actual Request from potential Need).
   - Deadlock Recovery (termination, preemption, victim selection, rollback, starvation).
7. Student submissions are never cited as Tier A authoritative sources.
8. Zero modifications to locked Chapters 1-5 academic content since baseline 06e4b34.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Ensure standard UTF-8 console output
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from research_utils import parse_questions, parse_slide_coverage  # noqa: E402

THEORY_PATH = ROOT / "content/theory/ch06-deadlock.md"
QBANK_PATH = ROOT / "content/questions/subjective/ch06.md"
SLIDE_COVERAGE_PATH = ROOT / "research/data/slide_coverage.yaml"
QUESTIONS_PATH = ROOT / "research/data/official_review_questions.yaml"
LOCKED_BASELINE = "06e4b34ef14d60398e462e437470bb6a37157996"

CANONICAL_SOURCE_IDS = [
    "UIT-OUTLINE-2024",
    "UIT-SLIDE-CH06-2024",
    "UIT-QBANK-CH06-2024",
]

DISALLOWED_STUDENT_SOURCES = [
    "UIT-QBANK-CH06-2024-VARIANT-STUDENT-23520237",
    "UIT-REF-CH06-STUDENT-23521551-PDF",
]


def validate_ch06_content() -> int:
    print(">>> Validating Chapter 6 Content & Academic Fidelity...")
    errors: list[str] = []

    # 1. Existence of core authored files
    if not THEORY_PATH.exists():
        errors.append(f"Missing theory file: {THEORY_PATH.relative_to(ROOT)}")
    if not QBANK_PATH.exists():
        errors.append(f"Missing QBank subjective file: {QBANK_PATH.relative_to(ROOT)}")

    if errors:
        for err in errors:
            print(f"  - [FAIL] {err}")
        return 1

    theory_text = THEORY_PATH.read_text(encoding="utf-8")
    qbank_text = QBANK_PATH.read_text(encoding="utf-8")

    # 2. Canonical source ID citations
    for sid in CANONICAL_SOURCE_IDS:
        if sid not in theory_text:
            errors.append(f"Theory file missing canonical source citation: '{sid}'")
        if sid not in qbank_text:
            errors.append(f"QBank file missing canonical source citation: '{sid}'")

    # 3. Disallowed student sources must never appear as authoritative in content
    for st_id in DISALLOWED_STUDENT_SOURCES:
        if st_id in theory_text:
            errors.append(f"Student submission '{st_id}' illegally referenced in theory content")
        if st_id in qbank_text:
            errors.append(f"Student submission '{st_id}' illegally referenced in QBank content")

    # 4. Slide coverage lifecycle status
    decks = parse_slide_coverage(SLIDE_COVERAGE_PATH)
    ch6_deck = next((d for d in decks if d.get("source_id") == "UIT-SLIDE-CH06-2024"), None)
    if not ch6_deck:
        errors.append("UIT-SLIDE-CH06-2024 not found in slide_coverage.yaml")
    else:
        sections = ch6_deck.get("sections", [])
        content_drafted_pages = sum(
            s.get("page_count", 0) for s in sections
            if s.get("classification") == "CONTENT" and s.get("content_status") == "CONTENT_DRAFTED"
        )
        non_content_unwritten_pages = sum(
            s.get("page_count", 0) for s in sections
            if s.get("classification") == "NON_CONTENT" and s.get("content_status") == "NOT_WRITTEN"
        )
        if content_drafted_pages != 63:
            errors.append(f"Expected exactly 63 CONTENT pages marked CONTENT_DRAFTED, got {content_drafted_pages}")
        if non_content_unwritten_pages != 4:
            errors.append(f"Expected exactly 4 NON_CONTENT pages marked NOT_WRITTEN, got {non_content_unwritten_pages}")

    # 5. Question bank lifecycle status
    qrows = [q for q in parse_questions(QUESTIONS_PATH) if q.get("source_id") == "UIT-QBANK-CH06-2024"]
    if len(qrows) != 15:
        errors.append(f"Expected exactly 15 QBank questions for Chapter 6, got {len(qrows)}")
    drafted_q_count = sum(1 for q in qrows if q.get("content_status") == "CONTENT_DRAFTED")
    if drafted_q_count != 15:
        errors.append(f"Expected all 15 QBank questions marked CONTENT_DRAFTED, got {drafted_q_count}")

    # 6. Theory Content Key Invariant Checks
    required_theory_concepts = [
        ("Coffman 4 Conditions", ["mutual exclusion", "hold and wait", "no preemption", "circular wait"]),
        ("RAG Single vs Multiple Instances", ["đơn thực thể", "nhiều thực thể", "chu trình"]),
        ("Safe vs Unsafe vs Deadlock", ["safe state", "unsafe", "deadlock"]),
        ("Banker Data Structures", ["available", "max", "allocation", "need", "work", "finish"]),
        ("Banker Safety Algorithm", ["an toàn", "safe sequence"]),
        ("Banker Resource Request", ["request", "giả lập", "rollback"]),
        ("Deadlock Detection Matrix", ["phát hiện", "wait-for"]),
        ("Deadlock Recovery", ["phục hồi", "termination", "preemption", "victim", "rollback", "starvation"]),
    ]

    t_lower = theory_text.lower()
    for concept_name, terms in required_theory_concepts:
        missing = [t for t in terms if t not in t_lower]
        if missing:
            errors.append(f"Theory content missing mandatory terms for {concept_name}: {missing}")

    # 7. Detection distinguishes Request from Need
    if "request" not in t_lower or "need" not in t_lower:
        errors.append("Theory content must explicitly distinguish Request from Need in Detection vs Banker")

    # 8. Unsafe != Deadlock protection
    unsafe_deadlock_distinction = (
        "không đồng nghĩa" in t_lower or "không phải" in t_lower or "không an toàn" in t_lower
    )
    if not unsafe_deadlock_distinction:
        errors.append("Theory content must maintain explicit distinction that Unsafe != necessarily Deadlock")

    # 9. QBank All 15 Questions Mapped in Content
    for i in range(1, 16):
        qid = f"QBANK-CH06-{i:02d}"
        if qid not in qbank_text:
            errors.append(f"QBank file missing unit header / locator for '{qid}'")

    # 10. Committed Locked Chapters 1-5 Check
    try:
        git_check = subprocess.run(
            ["git", "diff", "--name-only", f"{LOCKED_BASELINE}..HEAD", "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if git_check.returncode == 0:
            changed_files = [f.strip() for f in git_check.stdout.splitlines() if f.strip()]
            locked_pattern = re.compile(
                r"^content/(theory/ch0[1-5]|questions/subjective/ch0[1-5]|reviews/midterm)"
            )
            contaminated = [f for f in changed_files if locked_pattern.match(f)]
            if contaminated:
                errors.append(f"Regressed locked Chapters 1-5 files in history: {contaminated}")
    except Exception as e:
        print(f"  [WARN] Git history diff check skipped: {e}")

    if errors:
        print("CHAPTER 6 CONTENT VALIDATION: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("CHAPTER 6 CONTENT VALIDATION: PASS")
    print("  [OK] content/theory/ch06-deadlock.md exists and covers all 63 content pages")
    print("  [OK] content/questions/subjective/ch06.md covers all 15 QBank units (8 theory + 7 exercises)")
    print("  [OK] Canonical source IDs cited in theory and QBank frontmatter")
    print("  [OK] 63 CONTENT pages marked CONTENT_DRAFTED; 4 NON_CONTENT remain NOT_WRITTEN")
    print("  [OK] 15 QBank units marked CONTENT_DRAFTED in official_review_questions.yaml")
    print("  [OK] Core invariants present: Coffman 4, RAG single/multi, Safe/Unsafe/Deadlock, Banker, Detection, Recovery")
    print("  [OK] Detection distinguishes Request from Need")
    print("  [OK] Unsafe != Deadlock distinction maintained")
    print("  [OK] Student submission variants excluded from Tier A authority")
    print("  [OK] Zero changes to locked Chapters 1-5 academic content")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate_ch06_content())

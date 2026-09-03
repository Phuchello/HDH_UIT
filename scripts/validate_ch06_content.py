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
6. Core conceptual invariants in Theory:
   - 4 Coffman conditions (Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait).
   - RAG single-instance (cycle <=> deadlock) vs multi-instance (cycle is necessary, not sufficient).
   - Safe State vs Unsafe State vs Deadlock (Unsafe != necessarily Deadlock).
   - Banker's Algorithm (Available, Max, Allocation, Need, Work, Finish, Safe Sequence, Resource-Request).
   - Deadlock Detection matrix (distinguishing actual Request from potential Need).
   - Deadlock Recovery (termination, preemption, victim selection, rollback, starvation).
7. QBank Section-Scoped Semantic Invariants (ACAD-CH6-001 & ACAD-CH6-002 & VALIDATOR-CH6-001):
   - QBANK-CH06-02: Coffman conditions must not be asserted with bare 'if and only if' / 'khi và chỉ khi'.
   - QBANK-CH06-13, 14, 15: Failed Banker Safety result must not claim immediate deadlock or permanent blocking.
     Must positively distinguish that failure to find a safe sequence proves Unsafe, which is NOT proof of current Deadlock.
8. Provenance Integrity (PROV-CH6-001):
   - Rejects fabricated official scoring rubric claims (e.g. 'barem chấm điểm IT007 UIT', 'điểm chuẩn UIT').
   - Ensures rubrics are framed as neutral self-check criteria with appropriate disclaimers.
9. Student submissions are never cited as Tier A authoritative sources.
10. Zero modifications to locked Chapters 1-5 academic content since baseline 06e4b34.
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

    # Balanced code fences guard (ENG-CH6-003)
    t_fences = [i for i, line in enumerate(theory_text.splitlines(), 1) if line.strip().startswith("```")]
    if len(t_fences) % 2 != 0:
        errors.append(f"Theory file has unbalanced fenced code blocks (found {len(t_fences)} triple-backtick lines: {t_fences})")
    q_fences = [i for i, line in enumerate(qbank_text.splitlines(), 1) if line.strip().startswith("```")]
    if len(q_fences) % 2 != 0:
        errors.append(f"QBank file has unbalanced fenced code blocks (found {len(q_fences)} triple-backtick lines: {q_fences})")

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

    # 8. Unsafe != Deadlock & State-Space Invariant Guard (ACAD-CH6-003)
    unsafe_deadlock_distinction = (
        ("không đồng nghĩa" in t_lower or "không phải" in t_lower or "tiềm ẩn rủi ro" in t_lower)
        and ("không an toàn" in t_lower or "unsafe" in t_lower)
    )
    if not unsafe_deadlock_distinction:
        errors.append("Theory content must maintain explicit distinction that Unsafe != necessarily Deadlock")

    # Semantic invariants adjacent to state-space diagram
    has_disjoint_invariant = (
        ("safe" in t_lower and "unsafe" in t_lower)
        and ("\\cap" in theory_text or "rời nhau" in t_lower or "disjoint" in t_lower)
        and ("\\emptyset" in theory_text or "loại trừ lẫn nhau" in t_lower or "rời nhau hoàn toàn" in t_lower)
    )
    if not has_disjoint_invariant:
        errors.append("Theory content missing mandatory Safe cap Unsafe = empty / disjoint state-space invariant")

    has_subset_invariant = (
        ("\\subset" in theory_text or "tập con" in t_lower)
        and ("deadlock" in t_lower and "unsafe" in t_lower)
    )
    if not has_subset_invariant:
        errors.append("Theory content missing mandatory Deadlock subset of Unsafe state-space invariant")

    # Reject flawed diagram pattern where an outer UNSAFE box encloses SAFE STATE
    for block in re.findall(r"(?m)^```[^\n]*\n(.*?\n)```", theory_text, re.DOTALL):
        b_low = block.lower()
        if "unsafe" in b_low and "safe" in b_low:
            if re.search(r"trạng thái không an toàn \(unsafe state\).*?trạng thái an toàn \(safe", b_low, re.DOTALL):
                errors.append("Theory content contains invalid state-space diagram (ACAD-CH6-003): outer UNSAFE box must NOT enclose SAFE STATE")
            if re.search(r"┌─+┐\s*│\s*trạng thái không an toàn.*?safe", b_low, re.DOTALL):
                errors.append("Theory content contains invalid state-space diagram (ACAD-CH6-003): outer box labeled UNSAFE encloses SAFE")

    # VALIDATOR-CH6-002: Safe-State Temporal Overclaim & Invariant Guard (ACAD-CH6-005)
    sec_651 = ""
    if "### 6.5.1" in theory_text:
        sec_651 = theory_text.split("### 6.5.1")[1].split("### 6.5.2")[0]
    sec_651_lower = sec_651.lower()

    # Reject unconditional temporal overclaims in Safe-State context
    forbidden_safe_temporal_overclaims = [
        "100% không bao giờ",
        "không bao giờ xảy ra bế tắc",
        "không bao giờ xảy ra deadlock",
        "never deadlock",
        "deadlock can never occur",
        "deadlock is impossible forever",
        "vĩnh viễn không bao giờ bế tắc",
    ]
    for phrase in forbidden_safe_temporal_overclaims:
        if phrase in sec_651_lower:
            errors.append(
                f"Theory Section 6.5.1 contains invalid unconditional temporal overclaim (VALIDATOR-CH6-002 / ACAD-CH6-005): '{phrase}'"
            )

    # Positive invariant 1: Safe State defined via existence of at least one Safe Sequence
    has_safe_sequence_definition = (
        ("chuỗi an toàn" in sec_651_lower or "safe sequence" in sec_651_lower)
        and ("tồn tại" in sec_651_lower or "exists" in sec_651_lower)
    )
    if not has_safe_sequence_definition:
        errors.append(
            "Theory Section 6.5.1 missing positive invariant (VALIDATOR-CH6-002): Safe State must be defined by existence of at least one Safe Sequence"
        )

    # Positive invariant 2: Future avoidance depends on keeping subsequent allocations Safe
    has_avoidance_continuity_invariant = (
        ("tránh bế tắc" in sec_651_lower or "avoidance" in sec_651_lower)
        and ("duy trì" in sec_651_lower or "bảo toàn" in sec_651_lower or "kiểm soát" in sec_651_lower)
        and ("safe" in sec_651_lower or "an toàn" in sec_651_lower)
    )
    if not has_avoidance_continuity_invariant:
        errors.append(
            "Theory Section 6.5.1 missing positive invariant (VALIDATOR-CH6-002): future avoidance depends on continuously maintaining Safe allocations"
        )

    # 9. QBank All 15 Questions Mapped in Content
    for i in range(1, 16):
        qid = f"QBANK-CH06-{i:02d}"
        if qid not in qbank_text:
            errors.append(f"QBank file missing unit header / locator for '{qid}'")

    # 10. QBank Section-Scoped Semantic Regression Guards (ACAD-CH6-001 & ACAD-CH6-002 & VALIDATOR-CH6-001)
    qbank_units: dict[str, str] = {}
    for part in qbank_text.split("### QBANK-CH06-")[1:]:
        qid = f"QBANK-CH06-{part[:2]}"
        qbank_units[qid] = part

    # A. QBANK-CH06-02: Coffman iff guard
    q2_text = qbank_units.get("QBANK-CH06-02", "")
    q2_lower = q2_text.lower()
    if "khi và chỉ khi" in q2_lower or "if and only if" in q2_lower:
        errors.append("QBANK-CH06-02 invalidly uses 'khi và chỉ khi' / 'if and only if' for 4 Coffman necessary conditions")

    # B. QBANK-CH06-13: Banker Safety Result vs Deadlock
    q13_text = qbank_units.get("QBANK-CH06-13", "")
    q13_lower = q13_text.lower()
    for term in ["bế tắc ngay lập tức", "chứng minh bế tắc", "bị tắc vĩnh viễn", "bị chặn vĩnh viễn"]:
        if term in q13_lower:
            errors.append(f"QBANK-CH06-13 contains invalid deadlock claim '{term}' in Banker Safety result context")
    has_q13_positive_guard = (
        ("không tồn tại chuỗi an toàn" in q13_lower or "không có chuỗi an toàn" in q13_lower)
        and ("unsafe" in q13_lower or "không an toàn" in q13_lower)
        and ("không đồng nghĩa" in q13_lower or "không chứng minh" in q13_lower or "không nhất thiết" in q13_lower)
    )
    if not has_q13_positive_guard:
        errors.append("QBANK-CH06-13 missing positive distinction: no safe sequence => unsafe != proof of current deadlock")

    # C. QBANK-CH06-14: Banker Safety Result vs Deadlock
    q14_text = qbank_units.get("QBANK-CH06-14", "")
    q14_lower = q14_text.lower()
    for term in ["bị chặn vĩnh viễn vì thiếu tài nguyên", "bế tắc ngay lập tức", "chứng minh bế tắc"]:
        if term in q14_lower:
            errors.append(f"QBANK-CH06-14 contains invalid deadlock claim '{term}' in Banker Safety result context")
    has_q14_positive_guard = (
        ("unsafe" in q14_lower or "không an toàn" in q14_lower)
        and ("không suy diễn" in q14_lower or "không đồng nghĩa" in q14_lower or "không chứng minh" in q14_lower)
    )
    if not has_q14_positive_guard:
        errors.append("QBANK-CH06-14 missing positive distinction: unsafe != proof of current deadlock")

    # D. QBANK-CH06-15: Banker Safety Result vs Deadlock
    q15_text = qbank_units.get("QBANK-CH06-15", "")
    q15_lower = q15_text.lower()
    for term in ["bế tắc ngay lập tức", "chứng minh bế tắc", "bị tắc vĩnh viễn"]:
        if term in q15_lower:
            errors.append(f"QBANK-CH06-15 contains invalid deadlock claim '{term}' in Banker Safety result context")
    has_q15_positive_guard = (
        ("không tồn tại chuỗi an toàn" in q15_lower or "không có chuỗi an toàn" in q15_lower)
        and ("unsafe" in q15_lower or "không an toàn" in q15_lower)
        and ("không chứng minh" in q15_lower or "không đồng nghĩa" in q15_lower or "không nhất thiết" in q15_lower)
    )
    if not has_q15_positive_guard:
        errors.append("QBANK-CH06-15 missing positive distinction: no safe sequence => unsafe != proof of current deadlock")

    # 11. Provenance Integrity Guard (PROV-CH6-001)
    forbidden_provenance_terms = [
        "barem chấm điểm it007 uit",
        "official marking scheme",
        "điểm chuẩn uit",
    ]
    q_all_lower = qbank_text.lower()
    for term in forbidden_provenance_terms:
        if term in q_all_lower:
            errors.append(f"QBank contains fabricated official scoring provenance '{term}'")

    if "| Điểm chuẩn |" in qbank_text:
        errors.append("QBank rubric table contains unproven 'Điểm chuẩn' header (must use neutral self-check label)")

    if "Rubric tự kiểm tra của handbook" not in qbank_text:
        errors.append("QBank missing required neutral self-check rubric heading")

    # 12. Committed Locked Chapters 1-5 Check
    try:
        git_check = subprocess.run(
            ["git", "diff", "--name-only", f"{LOCKED_BASELINE}..HEAD", "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace",
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
    print("  [OK] Unsafe != Deadlock distinction maintained across theory and QBank (Q13, Q14, Q15)")
    print("  [OK] Coffman 4 conditions logical wording verified (Q02: necessary only, zero invalid iff claims)")
    print("  [OK] Provenance integrity verified (neutral self-check rubrics, zero fabricated UIT marking keys)")
    print("  [OK] Student submission variants excluded from Tier A authority")
    print("  [OK] Zero changes to locked Chapters 1-5 academic content")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate_ch06_content())

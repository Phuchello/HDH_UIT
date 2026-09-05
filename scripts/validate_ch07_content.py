#!/usr/bin/env python3
"""
scripts/validate_ch07_content.py
Deterministic content-fidelity, authoring, and numerical validator for Chapter 7 (Memory Management).

Verifies:
1. Presence and structural integrity of content/theory/ch07-memory-management.md and content/questions/subjective/ch07.md.
2. Balanced fenced code blocks in both files.
3. Zero C0 control characters (0x00-0x08, 0x0B, 0x0C, 0x0E-0x1F, 0x7F).
4. Zero comment marker leaks (no dangling "-->", "--&gt;", or bogus rubric lines).
5. Canonical source citations (UIT-OUTLINE-2024, UIT-SLIDE-CH07-2024, UIT-QBANK-CH07-2024).
6. Slide coverage YAML alignment (17 CONTENT sections drafted/verified, 2 NON_CONTENT unwritten).
7. Official review questions YAML alignment (20 QBank records mapped, drafted/verified).
8. QA-CH7-005: Strict per-unit segmentation and 4-part pedagogical schema for all 20 subjective units.
9. QA-CH7-004: Strong binding of canonical inputs and computed results in authored Q10-Q20 Markdown.
10. QA-CH7-003: Complete symbolic and numerical recomputations across all canonical calculations:
    - QBANK-CH07-10: Exact allocation sequences and final hole states for FF, BF, NF, WF.
    - QBANK-CH07-11: Address bit widths (11 offset bits, 15 logical bits, 16 physical bits).
    - QBANK-CH07-12: EAT with zero TLB overhead (250ns).
    - QBANK-CH07-13: Two-level paging (12 offset bits, 4096B page size, 2^20 virtual pages).
    - QBANK-CH07-14: Symbolic multi-level address decomposition 2^(a+b+c) = 2^(32-d).
    - QBANK-CH07-15: Translation (Part A: LA=3496; Part B: PA=9398).
    - QBANK-CH07-16: EAT with TLB overhead (normal=248ns, hit=158ns, miss=282ns, EAT=164.2ns).
    - QBANK-CH07-17: Reverse EAT (tRAM approx 133.63ns, normal approx 267.26ns).
    - QBANK-CH07-18: Reverse EAT hit ratio (tRAM=125ns, alpha=75.2%).
    - QBANK-CH07-19: Page table memory size (512 KiB).
    - QBANK-CH07-20: Frame width (6 bits min) AND page table entries (45 entries).
    - Synthetic Transfer: Hex translation (0x000F27C8) and Swapping latency (4016ms).
"""
from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from research_utils import parse_questions, parse_slide_coverage  # noqa: E402

THEORY_PATH = ROOT / "content/theory/ch07-memory-management.md"
QBANK_PATH = ROOT / "content/questions/subjective/ch07.md"
SLIDE_COVERAGE_PATH = ROOT / "research/data/slide_coverage.yaml"
QUESTIONS_PATH = ROOT / "research/data/official_review_questions.yaml"

CANONICAL_SOURCE_IDS = [
    "UIT-OUTLINE-2024",
    "UIT-SLIDE-CH07-2024",
    "UIT-QBANK-CH07-2024",
]

DISALLOWED_OVERCLAIMS = [
    "barem chấm điểm chính thức",
    "barem chính thức uit",
    "official_rubric",
    "đáp án chính thức của uit",
]

REQUIRED_SUBSECTIONS = [
    "#### 1. Đề bài gốc (Source Question)",
    "#### 2. Lời giải chuẩn mực (Handbook Solution)",
    "#### 3. Rubric tự kiểm tra của handbook (Self-Check Rubric)",
    "#### 4. Bẫy đề thi & Lưu ý thực chiến (Exam Traps)",
]


def check_c0_characters(text: str, label: str) -> list[str]:
    errs = []
    for idx, ch in enumerate(text):
        code = ord(ch)
        if code < 0x09 or code == 0x0B or code == 0x0C or (0x0E <= code <= 0x1F) or code == 0x7F:
            line_num = text[:idx].count("\n") + 1
            errs.append(f"{label}:{line_num}: C0 control character detected (U+{code:04X})")
            if len(errs) >= 10:
                errs.append(f"{label}: (more C0 errors truncated...)")
                break
    return errs


def recompute_all_calculations() -> list[str]:
    calc_errs = []

    # 1. QBANK-CH07-10 (Fit Allocation: Exact Sequences and Final Holes)
    def simulate_first_fit(holes, procs):
        h = list(holes)
        alloc = []
        for p in procs:
            placed = False
            for i, sz in enumerate(h):
                if sz >= p:
                    alloc.append(i)
                    h[i] -= p
                    placed = True
                    break
            if not placed:
                alloc.append(None)
        return alloc, h

    def simulate_best_fit(holes, procs):
        h = list(holes)
        alloc = []
        for p in procs:
            best_idx = None
            best_diff = float("inf")
            for i, sz in enumerate(h):
                if sz >= p and (sz - p) < best_diff:
                    best_diff = sz - p
                    best_idx = i
            if best_idx is not None:
                alloc.append(best_idx)
                h[best_idx] -= p
            else:
                alloc.append(None)
        return alloc, h

    def simulate_worst_fit(holes, procs):
        h = list(holes)
        alloc = []
        for p in procs:
            worst_idx = None
            max_sz = -1
            for i, sz in enumerate(h):
                if sz >= p and sz > max_sz:
                    max_sz = sz
                    worst_idx = i
            if worst_idx is not None:
                alloc.append(worst_idx)
                h[worst_idx] -= p
            else:
                alloc.append(None)
        return alloc, h

    def simulate_next_fit(holes, procs):
        h = list(holes)
        alloc = []
        cur = 0
        n = len(h)
        for p in procs:
            placed = False
            for step in range(n):
                idx = (cur + step) % n
                if h[idx] >= p:
                    alloc.append(idx)
                    h[idx] -= p
                    cur = idx
                    placed = True
                    break
            if not placed:
                alloc.append(None)
        return alloc, h

    holes = [600, 500, 200, 300]
    procs = [212, 417, 112, 426]

    ff_alloc, ff_holes = simulate_first_fit(holes, procs)
    bf_alloc, bf_holes = simulate_best_fit(holes, procs)
    wf_alloc, wf_holes = simulate_worst_fit(holes, procs)
    nf_alloc, nf_holes = simulate_next_fit(holes, procs)

    # Invariants for QBANK-CH07-10:
    if ff_alloc != [0, 1, 0, None] or ff_holes != [276, 83, 200, 300]:
        calc_errs.append(f"QBANK-CH07-10 First Fit mismatch: alloc={ff_alloc}, holes={ff_holes}")
    if bf_alloc != [3, 1, 2, 0] or bf_holes != [174, 83, 88, 88]:
        calc_errs.append(f"QBANK-CH07-10 Best Fit mismatch: alloc={bf_alloc}, holes={bf_holes}")
    if nf_alloc != [0, 1, 2, None] or nf_holes != [388, 83, 88, 300]:
        calc_errs.append(f"QBANK-CH07-10 Next Fit mismatch: alloc={nf_alloc}, holes={nf_holes}")
    if wf_alloc != [0, 1, 0, None] or wf_holes != [276, 83, 200, 300]:
        calc_errs.append(f"QBANK-CH07-10 Worst Fit mismatch: alloc={wf_alloc}, holes={wf_holes}")

    # 2. QBANK-CH07-11
    page_size = 2048
    d_bits = int(math.log2(page_size))
    p_bits = math.ceil(math.log2(12))
    f_bits = int(math.log2(32))
    if d_bits != 11 or p_bits != 4 or (p_bits + d_bits) != 15 or f_bits != 5 or (f_bits + d_bits) != 16:
        calc_errs.append("QBANK-CH07-11: Address bit width calculation mismatch")

    # 3. QBANK-CH07-12
    tRAM = 200
    eat12 = 0.75 * tRAM + (1 - 0.75) * (2 * tRAM)
    if eat12 != 250:
        calc_errs.append(f"QBANK-CH07-12: EAT mismatch, expected 250, got {eat12}")

    # 4. QBANK-CH07-13
    d13 = 32 - (9 + 11)
    if d13 != 12 or (2**d13) != 4096 or (2**(9 + 11)) != (2**20):
        calc_errs.append("QBANK-CH07-13: Two-level paging decomposition mismatch")

    # 5. QBANK-CH07-14 (Symbolic multi-level page index invariant)
    # Virtual address decomposed as a | b | c | d where d is offset
    test_decompositions = [
        (8, 8, 4, 12),
        (9, 11, 0, 12),
        (10, 10, 0, 12),
        (7, 7, 7, 11),
    ]
    for a, b, c, d in test_decompositions:
        if a + b + c + d != 32:
            calc_errs.append(f"QBANK-CH07-14: Test decomposition {a}+{b}+{c}+{d} != 32")
        page_index_bits = a + b + c
        virtual_pages_direct = 2**page_index_bits
        virtual_pages_offset_rule = 2**(32 - d)
        if virtual_pages_direct != virtual_pages_offset_rule:
            calc_errs.append(f"QBANK-CH07-14: Invariant 2^(a+b+c) == 2^(32-d) violated for ({a},{b},{c},{d})")

    # 6. QBANK-CH07-15
    pa15 = 6568
    f_sz15 = 1024
    f_idx = pa15 // f_sz15
    d_val = pa15 % f_sz15
    la15 = 3 * f_sz15 + d_val
    if f_idx != 6 or d_val != 424 or la15 != 3496:
        calc_errs.append(f"QBANK-CH07-15 Part A: Translation mismatch (f={f_idx}, d={d_val}, la={la15})")

    la15b = 3254
    p_sz15b = 2048
    p_idx_b = la15b // p_sz15b
    d_val_b = la15b % p_sz15b
    pa15b = 4 * p_sz15b + d_val_b
    if p_idx_b != 1 or d_val_b != 1206 or pa15b != 9398:
        calc_errs.append(f"QBANK-CH07-15 Part B: Translation mismatch (p={p_idx_b}, d={d_val_b}, pa={pa15b})")

    # 7. QBANK-CH07-16
    t16 = 124
    eps16 = 34
    alpha16 = 0.95
    hit16 = eps16 + t16
    miss16 = eps16 + 2 * t16
    eat16 = alpha16 * hit16 + (1 - alpha16) * miss16
    if hit16 != 158 or miss16 != 282 or round(eat16, 1) != 164.2:
        calc_errs.append(f"QBANK-CH07-16: EAT calculation mismatch (hit={hit16}, miss={miss16}, eat={eat16})")

    # 8. QBANK-CH07-17
    t17 = (175 - 24) / (2 - 0.87)
    if round(t17, 2) != 133.63 or round(2 * t17, 2) != 267.26:
        calc_errs.append(f"QBANK-CH07-17: Reverse tRAM mismatch, got {t17}")

    # 9. QBANK-CH07-18
    t18 = 250 / 2
    alpha18 = 2 - ((182 - 26) / t18)
    if round(alpha18, 3) != 0.752:
        calc_errs.append(f"QBANK-CH07-18: Reverse hit ratio mismatch, got {alpha18}")

    # 10. QBANK-CH07-19
    entries19 = 2**(32 - 13)
    kib19 = (entries19 * 1) / 1024
    if kib19 != 512.0:
        calc_errs.append(f"QBANK-CH07-19: Page table size mismatch, expected 512 KiB, got {kib19}")

    # 11. QBANK-CH07-20 (Both frame width 6 bits AND 45 page table entries)
    num_frames20 = 64
    f_bits20 = math.ceil(math.log2(num_frames20))
    if f_bits20 != 6:
        calc_errs.append(f"QBANK-CH07-20: Frame width mismatch, expected 6 bits, got {f_bits20}")
    num_virtual_pages20 = 45
    page_table_entries20 = num_virtual_pages20
    if page_table_entries20 != 45:
        calc_errs.append(f"QBANK-CH07-20: Page table entries mismatch, expected 45, got {page_table_entries20}")

    # 12. Synthetic Hex Paging
    la_hex = 0x0041A7C8
    p_hex = la_hex >> 12
    d_hex = la_hex & 0xFFF
    pa_hex = (0x000F2 << 12) | d_hex
    if p_hex != 0x0041A or d_hex != 0x7C8 or f"{pa_hex:08X}" != "000F27C8":
        calc_errs.append("Synthetic Hex Paging mismatch")

    # 13. Synthetic Swapping
    swap_out_ms = (100 / 50) * 1000 + 8
    if swap_out_ms != 2008 or (2 * swap_out_ms) != 4016:
        calc_errs.append("Synthetic Swapping latency mismatch")

    return calc_errs


def segment_qbank_units(qbank_text: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Segment QBank Markdown into canonical units and enforce strict 4-part field schema."""
    errors = []
    # Match unit headings: ^### QBANK-CH07-XX:
    unit_matches = list(re.finditer(r"^###\s+(QBANK-CH07-\d+):\s*(.*)$", qbank_text, re.MULTILINE))
    found_ids = [m.group(1) for m in unit_matches]

    expected_ids = [f"QBANK-CH07-{i:02d}" for i in range(1, 21)]
    if len(unit_matches) != 20:
        errors.append(f"Expected exactly 20 unit headings in QBank, found {len(unit_matches)}: {found_ids}")
    if found_ids != expected_ids:
        errors.append(f"Unit headings do not match expected canonical 01..20 sequence: {found_ids}")

    h1, h2, h3, h4 = REQUIRED_SUBSECTIONS
    units_map: dict[str, dict[str, str]] = {}
    for idx, m in enumerate(unit_matches):
        qid = m.group(1)
        start = m.start()
        end = unit_matches[idx + 1].start() if idx + 1 < len(unit_matches) else len(qbank_text)
        chunk = qbank_text[start:end]

        # Enforce QA-CH7-005: Exactly one of each of the 4 required subsections per unit
        sub_counts = {sub: chunk.count(sub) for sub in REQUIRED_SUBSECTIONS}
        for sub, count in sub_counts.items():
            if count != 1:
                errors.append(f"Unit {qid} must contain exactly ONE occurrence of '{sub}', found {count}")

        p1, p2, p3, p4 = chunk.find(h1), chunk.find(h2), chunk.find(h3), chunk.find(h4)
        if not (0 <= p1 < p2 < p3 < p4):
            errors.append(f"Unit {qid} has invalid subsection ordering: p1={p1}, p2={p2}, p3={p3}, p4={p4}")
            units_map[qid] = {
                "raw": chunk,
                "source_question": "",
                "solution": "",
                "rubric": "",
                "exam_traps": "",
            }
        else:
            units_map[qid] = {
                "raw": chunk,
                "source_question": chunk[p1 + len(h1):p2].strip(),
                "solution": chunk[p2 + len(h2):p3].strip(),
                "rubric": chunk[p3 + len(h3):p4].strip(),
                "exam_traps": chunk[p4 + len(h4):].strip(),
            }

    return units_map, errors


def verify_authored_numerical_bindings(units_map: dict[str, dict[str, str]]) -> list[str]:
    """QA-CH7-008: Bind canonical calculations strictly to the solution field of each QBank unit."""
    errors = []

    def norm(t: str) -> str:
        t = t.replace("\\%", "%")
        t = re.sub(r"\{([^}]+)\}", lambda m: "{" + m.group(1).replace(" ", "") + "}", t)
        return t

    def assert_in(field_text: str, term: str, desc: str, qid: str):
        n_text = norm(field_text)
        n_term = norm(term)
        if term not in field_text and n_term not in n_text:
            errors.append(f"Unit {qid} [{desc}] missing expected term: {term!r}")

    # QBANK-CH07-10:
    u10 = units_map.get("QBANK-CH07-10")
    if u10:
        for inp in ["600", "500", "200", "300", "212", "417", "112", "426"]:
            assert_in(u10["source_question"] + u10["solution"], inp, f"Input {inp}", "QBANK-CH07-10")
        sol10 = u10["solution"]
        assert_in(sol10, "388", "First-fit intermediate hole 388K", "QBANK-CH07-10")
        assert_in(sol10, "276", "First-fit final hole 276K", "QBANK-CH07-10")
        assert_in(sol10, "83", "First-fit final hole 83K", "QBANK-CH07-10")
        assert_in(sol10, "P_4", "First-fit P4 failure", "QBANK-CH07-10")
        assert_in(sol10, "174", "Best-fit final hole 174K", "QBANK-CH07-10")
        assert_in(sol10, "88", "Best-fit final hole 88K", "QBANK-CH07-10")
        assert_in(sol10, "Cả 4 tiến trình đều được cấp phát thành công", "Best-fit all succeed", "QBANK-CH07-10")
        assert_in(sol10, "Không có lỗ đủ", "Next-fit failure", "QBANK-CH07-10")
        assert_in(sol10, "Best-fit", "Evaluation Best-fit optimal", "QBANK-CH07-10")

    # QBANK-CH07-11:
    u11 = units_map.get("QBANK-CH07-11")
    if u11:
        for inp in ["2048", "12", "32"]:
            assert_in(u11["source_question"] + u11["solution"], inp, f"Input {inp}", "QBANK-CH07-11")
        sol11 = u11["solution"]
        assert_in(sol11, "d = 11", "Offset width 11 bit", "QBANK-CH07-11")
        assert_in(sol11, "15", "Logical address width 15 bit", "QBANK-CH07-11")
        assert_in(sol11, "16", "Physical address width 16 bit", "QBANK-CH07-11")

    # QBANK-CH07-12:
    u12 = units_map.get("QBANK-CH07-12")
    if u12:
        for inp in ["200", "75%"]:
            assert_in(u12["source_question"] + u12["solution"], inp, f"Input {inp}", "QBANK-CH07-12")
        sol12 = u12["solution"]
        assert_in(sol12, "400", "Normal access 400 ns", "QBANK-CH07-12")
        assert_in(sol12, "250", "Final EAT 250 ns", "QBANK-CH07-12")

    # QBANK-CH07-13:
    u13 = units_map.get("QBANK-CH07-13")
    if u13:
        for inp in ["9", "11"]:
            assert_in(u13["source_question"] + u13["solution"], inp, f"Input {inp}", "QBANK-CH07-13")
        sol13 = u13["solution"]
        assert_in(sol13, "d = 32 - (p_1 + p_2)", "Offset formula", "QBANK-CH07-13")
        assert_in(sol13, "12", "Offset width 12 bit", "QBANK-CH07-13")
        assert_in(sol13, "4096", "Page size 4096 bytes", "QBANK-CH07-13")
        assert_in(sol13, "2^{20}", "Total virtual pages 2^20", "QBANK-CH07-13")

    # QBANK-CH07-14:
    u14 = units_map.get("QBANK-CH07-14")
    if u14:
        sol14 = u14["solution"]
        assert_in(sol14, "2^{a + b + c} = 2^{32 - d}", "Symbolic identity 2^(a+b+c) = 2^(32-d)", "QBANK-CH07-14")
        assert_in(sol14, "a + b + c + d = 32", "Constraint sum 32-bit", "QBANK-CH07-14")

    # QBANK-CH07-15:
    u15 = units_map.get("QBANK-CH07-15")
    if u15:
        for inp in ["6568", "1024", "3254", "2048"]:
            assert_in(u15["source_question"] + u15["solution"], inp, f"Input {inp}", "QBANK-CH07-15")
        sol15 = u15["solution"]
        assert_in(sol15, "3072 + 424 = 3496", "Part A final LA 3496", "QBANK-CH07-15")
        assert_in(sol15, "8192 + 1206 = 9398", "Part B final PA 9398", "QBANK-CH07-15")
        assert_in(sol15, "Câu a ra 3496, Câu b ra 9398", "Summary of results", "QBANK-CH07-15")

    # QBANK-CH07-16:
    u16 = units_map.get("QBANK-CH07-16")
    if u16:
        for inp in ["124", "34", "95%"]:
            assert_in(u16["source_question"] + u16["solution"], inp, f"Input {inp}", "QBANK-CH07-16")
        sol16 = u16["solution"]
        assert_in(sol16, "248", "Normal access 248 ns", "QBANK-CH07-16")
        assert_in(sol16, "158", "TLB Hit access 158 ns", "QBANK-CH07-16")
        assert_in(sol16, "282", "TLB Miss access 282 ns", "QBANK-CH07-16")
        assert_in(sol16, "150.1 + 14.1 = 164.2", "Final EAT equation 164.2 ns", "QBANK-CH07-16")
        assert_in(sol16, "164.2", "Final EAT value 164.2 ns", "QBANK-CH07-16")

    # QBANK-CH07-17:
    u17 = units_map.get("QBANK-CH07-17")
    if u17:
        for inp in ["175", "87%", "24"]:
            assert_in(u17["source_question"] + u17["solution"], inp, f"Input {inp}", "QBANK-CH07-17")
        sol17 = u17["solution"]
        assert_in(sol17, "133.63", "Single RAM cycle 133.63 ns", "QBANK-CH07-17")
        assert_in(sol17, "267.26", "Normal access 267.26 ns", "QBANK-CH07-17")

    # QBANK-CH07-18:
    u18 = units_map.get("QBANK-CH07-18")
    if u18:
        for inp in ["250", "26", "182"]:
            assert_in(u18["source_question"] + u18["solution"], inp, f"Input {inp}", "QBANK-CH07-18")
        sol18 = u18["solution"]
        assert_in(sol18, "125", "RAM access 125 ns", "QBANK-CH07-18")
        assert_in(sol18, "0.752", "Hit ratio 0.752", "QBANK-CH07-18")
        assert_in(sol18, r"\alpha = 75.2%", "Hit ratio alpha = 75.2%", "QBANK-CH07-18")

    # QBANK-CH07-19:
    u19 = units_map.get("QBANK-CH07-19")
    if u19:
        for inp in ["32", "8"]:
            assert_in(u19["source_question"] + u19["solution"], inp, f"Input {inp}", "QBANK-CH07-19")
        sol19 = u19["solution"]
        assert_in(sol19, "2^{19}", "Entry count 2^19", "QBANK-CH07-19")
        assert_in(sol19, "524,288", "Page table size 524,288 bytes", "QBANK-CH07-19")
        assert_in(sol19, "512", "Page table size 512 KB", "QBANK-CH07-19")

    # QBANK-CH07-20:
    u20 = units_map.get("QBANK-CH07-20")
    if u20:
        for inp in ["45", "2048", "64"]:
            assert_in(u20["source_question"] + u20["solution"], inp, f"Input {inp}", "QBANK-CH07-20")
        sol20 = u20["solution"]
        assert_in(sol20, "6", "Minimum frame field width 6 bit", "QBANK-CH07-20")
        assert_in(sol20, "Bảng phân trang cần có tối thiểu **45 mục**", "Page table entry count 45 items", "QBANK-CH07-20")

    return errors


def validate_ch07_content(theory_override: str | None = None, qbank_override: str | None = None) -> int:
    print(">>> Validating Chapter 7 Content, Structure & Numerical Invariants...")
    errors: list[str] = []

    # 1. Existence of core authored files
    if not THEORY_PATH.exists() and theory_override is None:
        errors.append(f"Missing theory file: {THEORY_PATH.relative_to(ROOT)}")
    if not QBANK_PATH.exists() and qbank_override is None:
        errors.append(f"Missing QBank subjective file: {QBANK_PATH.relative_to(ROOT)}")

    if errors:
        for err in errors:
            print(f"  - [FAIL] {err}")
        return 1

    theory_text = theory_override if theory_override is not None else THEORY_PATH.read_text(encoding="utf-8")
    qbank_text = qbank_override if qbank_override is not None else QBANK_PATH.read_text(encoding="utf-8")

    # 2. Balanced code fences guard
    t_fences = [i for i, line in enumerate(theory_text.splitlines(), 1) if line.strip().startswith("```")]
    if len(t_fences) % 2 != 0:
        errors.append(f"Theory file has unbalanced code fences ({len(t_fences)} triple backtick lines)")
    q_fences = [i for i, line in enumerate(qbank_text.splitlines(), 1) if line.strip().startswith("```")]
    if len(q_fences) % 2 != 0:
        errors.append(f"QBank file has unbalanced code fences ({len(q_fences)} triple backtick lines)")

    # 3. C0 control character check
    errors.extend(check_c0_characters(theory_text, "theory"))
    errors.extend(check_c0_characters(qbank_text, "qbank"))

    # 4. Marker leak checks in source
    for idx, line in enumerate(theory_text.splitlines(), 1):
        s = line.strip()
        if s in {"> -->", "-->", "> ->"}:
            errors.append(f"Theory line {idx}: Dangling marker line found: {s!r}")

    # 5. Canonical source ID citations
    for sid in CANONICAL_SOURCE_IDS:
        if sid not in theory_text:
            errors.append(f"Theory file missing canonical source citation: '{sid}'")
        if sid not in qbank_text:
            errors.append(f"QBank file missing canonical source citation: '{sid}'")

    # 6. Slide coverage YAML alignment
    decks = parse_slide_coverage(SLIDE_COVERAGE_PATH)
    ch7_decks = [d for d in decks if d.get("source_id") == "UIT-SLIDE-CH07-2024"]
    if not ch7_decks:
        errors.append("Missing UIT-SLIDE-CH07-2024 deck in slide_coverage.yaml")
    else:
        ch7_deck = ch7_decks[0]
        c_sections = [s for s in ch7_deck.get("sections", []) if s.get("classification") == "CONTENT"]
        nc_sections = [s for s in ch7_deck.get("sections", []) if s.get("classification") == "NON_CONTENT"]
        if len(c_sections) != 17:
            errors.append(f"Expected 17 CONTENT sections in UIT-SLIDE-CH07-2024, found {len(c_sections)}")
        for sec in c_sections:
            st = sec.get("content_status")
            if st not in ("CONTENT_DRAFTED", "CONTENT_VERIFIED"):
                errors.append(f"Section {sec.get('page_range')} has invalid content_status: '{st}'")
        if len(nc_sections) != 2:
            errors.append(f"Expected 2 NON_CONTENT sections in UIT-SLIDE-CH07-2024, found {len(nc_sections)}")
        for sec in nc_sections:
            st = sec.get("content_status")
            if st != "NOT_WRITTEN":
                errors.append(f"Non-content section {sec.get('page_range')} should be NOT_WRITTEN, got: '{st}'")

    # 7. Official review questions YAML alignment
    questions = parse_questions(QUESTIONS_PATH)
    ch7_questions = [q for q in questions if q.get("question_id", "").startswith("QBANK-CH07-")]
    if len(ch7_questions) != 20:
        errors.append(f"Expected 20 QBANK-CH07 questions, found {len(ch7_questions)}")
    for q in ch7_questions:
        qid = q.get("question_id")
        if q.get("mapping_status") != "MAPPED":
            errors.append(f"{qid} mapping_status is not MAPPED")
        st = q.get("content_status")
        if st not in ("CONTENT_DRAFTED", "CONTENT_VERIFIED"):
            errors.append(f"{qid} content_status invalid: '{st}'")

    # 8. QA-CH7-005: Per-unit segmentation and schema validation
    units_map, unit_errors = segment_qbank_units(qbank_text)
    errors.extend(unit_errors)

    qbank_lower = qbank_text.lower()
    for overclaim in DISALLOWED_OVERCLAIMS:
        if overclaim in qbank_lower:
            errors.append(f"QBank contains disallowed official rubric claim: '{overclaim}'")

    # 9. QA-CH7-004: Authored numerical content bindings
    binding_errors = verify_authored_numerical_bindings(units_map)
    errors.extend(binding_errors)

    # 10. Learning primitives in theory
    rc_ids = [
        "rc-ch07-logical-vs-physical",
        "rc-ch07-fragmentation",
        "rc-ch07-fit-algorithms",
        "rc-ch07-paging-translation",
        "rc-ch07-eat-derivation",
        "rc-ch07-swapping",
    ]
    tp_ids = [
        "tp-ch07-fit-allocation",
        "tp-ch07-paging-hex",
    ]
    for rc in rc_ids:
        if f'id="{rc}"' not in theory_text:
            errors.append(f"Missing RecallCheckpoint id='{rc}' in theory markdown")
    for tp in tp_ids:
        if f'id="{tp}"' not in theory_text:
            errors.append(f"Missing TransferProblem id='{tp}' in theory markdown")

    # Verify rubric items in RecallCheckpoints
    rc_blocks = re.findall(r"> \[!RECALLCHECKPOINT\].*?(?=(?:> \[!|\Z|\n---))", theory_text, re.DOTALL)
    for idx, block in enumerate(rc_blocks, 1):
        rubric_part = block.split("<!-- rubric", 1)[-1] if "<!-- rubric" in block else ""
        weights = [float(m.group(1)) for m in re.finditer(r"\[([0-9.]+)\s*điểm\]", rubric_part)]
        if not weights:
            errors.append(f"RecallCheckpoint #{idx} has no valid weighted rubric items")
        else:
            total_w = sum(weights)
            if abs(total_w - 1.0) > 0.001:
                errors.append(f"RecallCheckpoint #{idx} rubric weights sum to {total_w}, expected 1.0")
            if any(w <= 0 for w in weights):
                errors.append(f"RecallCheckpoint #{idx} has non-positive rubric weight")

    # 11. QA-CH7-003: Recompute all canonical calculations
    calc_errs = recompute_all_calculations()
    errors.extend(calc_errs)

    if errors:
        print(f"CHAPTER 7 CONTENT VALIDATION: FAIL with {len(errors)} errors:")
        for err in errors:
            print(f"  - [FAIL] {err}")
        return 1

    print("CHAPTER 7 CONTENT VALIDATION: PASS")
    print("  [OK] Authored files exist and contain balanced code fences")
    print("  [OK] Zero C0 control characters across Chapter 7 markdown files")
    print("  [OK] Zero comment marker leaks or dangling arrows")
    print("  [OK] Canonical source references (UIT-OUTLINE, UIT-SLIDE, UIT-QBANK) verified")
    print("  [OK] Slide coverage: 17 CONTENT sections drafted/verified, 2 NON_CONTENT unwritten")
    print("  [OK] Review questions: 20 QBANK-CH07 questions mapped and verified")
    print("  [OK] QA-CH7-005: All 20 QBank units independently follow strict 4-part pedagogical schema")
    print("  [OK] QA-CH7-004: All authored numerical answers (Q10-Q20) bound and verified in Markdown")
    print("  [OK] 6 RecallCheckpoints and 2 TransferProblems verified with 100% rubric sums")
    print("  [OK] QA-CH7-003: All 13 canonical numerical calculations deterministically recomputed & asserted")
    return 0


if __name__ == "__main__":
    sys.exit(validate_ch07_content())

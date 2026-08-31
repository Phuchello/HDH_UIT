#!/usr/bin/env python3
"""Deterministic source-fidelity gates for the Batch 1 canonical map."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from research_utils import parse_questions, parse_registry, parse_slide_coverage


REGISTRY = ROOT / "content/sources/registry.yaml"
COVERAGE = ROOT / "research/data/slide_coverage.yaml"
QUESTIONS = ROOT / "research/data/official_review_questions.yaml"
CH4 = ROOT / "content/theory/ch04-scheduling.md"
CH2_BANK = ROOT / "content/questions/subjective/ch02.md"
CH4_BANK = ROOT / "content/questions/subjective/ch04.md"
MIDTERM = ROOT / "content/reviews/midterm.md"
MIDTERM_MAPPING = ROOT / "research/data/midterm_answer_mapping.yaml"

# Regression fixture copied from the canonical PPTX wording and checked against
# the machine-readable source_question fields in official_review_questions.yaml.
EXPECTED_MIDTERM_SOURCE_QUESTIONS = {
    **{
        f"MIDTERM-REVIEW-{index:02d}": question
        for index, question in enumerate([
            "Định nghĩa hệ điều hành?",
            "Cấu trúc hệ thống máy tính gồm những phần nào?",
            "Chương trình hệ thống và chương trình ứng dụng khác nhau như thế nào?",
            "Những đặc điểm cơ bản của ngắt?",
            "Hệ thống lưu trữ được phân cấp dựa trên những yếu tố nào?",
            "Phân biệt các khái niệm cơ bản về bộ xử lý?",
            "Đặc điểm của hệ thống đơn bộ xử lý, hệ thống đa bộ xử lý, hệ thống gom cụm?",
            "Có những chế độ hoạt động nào bên trong hệ điều hành?",
            "Đặc điểm của hệ thống đơn chương, đa chương và đa nhiệm?",
            "Hệ điều hành bao gồm những thành phần nào? Cụ thể từng thành phần?",
            "Cấu trúc hệ thống gồm những loại nào? Cho ví dụ từng loại (theo sách tham khảo)",
            "Chương trình hệ thống gồm những chương trình nào?",
            "Lời gọi hệ thống là gì và dùng để làm gì?",
            "Hệ điều hành cung cấp những dịch vụ nào?",
            "Một tiến trình chứa những thành phần gì?",
            "Tiến trình có những trạng thái nào? Cách tiến trình chuyển trạng thái?",
            "Tại sao phải cộng tác giữa các tiến trình?",
            "PCB là gì? Dùng để làm gì?",
            "Tiểu trình là gì?",
            "Trình tự thực thi của tiến trình cha và tiến trình con?",
            "Cho đoạn chương trình sau: Hỏi trong quá trình thực thi thì tiến trình khi chạy từ chương trình trên đã trải qua những trạng thái nào? Vẽ sơ đồ chuyển trạng thái trong quá trình thực thi?",
            "Cho đoạn chương trình sau: Hỏi khi chạy thì tiến trình được tạo ra từ chương trình trên sẽ in ra màn hình những gì? Vẽ cây tiến trình và những từ được in ra khi thực thi đoạn chương trình trên?",
            "Tại sao phải định thời? Có những loại bộ định thời nào?",
            "Định thời CPU là gì? Bộ định thời nào chịu trách nhiệm thực hiện việc này?",
            "Phí tổn gây ra khi định thời là gì?",
            "Trình bày các tiêu chuẩn định thời CPU?",
            "Kể tên các giải thuật định thời CPU?",
            "Mô tả và nêu ưu điểm, nhược điểm của từng giải thuật định thời sau: FCFS, SJF, SRTF, RR, Priority Scheduling, HRRN, MQ, MFQ.",
            "Đặc điểm của định thời trên hệ thống có nhiều bộ xử lý? Khi nào cần phải thực hiện cân bằng tải?",
            "Đặc điểm định thời theo thời gian thực?",
            "Mô tả các đặc điểm cơ bản của bộ định thời CFS trên Linux?",
            "Mô tả các đặc điểm cơ bản của định thời trên Windows?",
            "Cho 5 tiến trình với thời gian vào hàng đợi ready và thời gian cần CPU tương ứng như bảng sau: Vẽ giản đồ Gantt và tính thời gian đợi trung bình, thời gian đáp ứng trung bình và thời gian lưu lại trong hệ thống (turnaround time) trung bình cho các giải thuật sau:\nFCFS\nSJF preemptive\nRR với quantum time = 10",
        ], start=1)
    },
    "MIDTERM-REVIEW-REF-12": "REFERENCE_TO_EXTERNAL_EXERCISE_SET",
    "MIDTERM-REVIEW-REF-16": "REFERENCE_TO_EXTERNAL_EXERCISE_SET",
}


def normalize_source_question(value: object) -> str:
    """Normalize transport whitespace only; never invent punctuation."""
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.strip().split("\n")]
    normalized = "\n".join(lines)
    return re.sub(r"\n[ \t]*\n+", "\n", normalized)


def parse_answer_mapping(path: Path) -> list[dict[str, str]]:
    """Parse the deliberately flat one-line mapping records without PyYAML."""
    records = []
    pattern = re.compile(
        r'question_id:\s*"([^"]+)".*?source_locator:\s*"([^"]+)".*?'
        r'canonical_answer_destination:\s*"([^"]+)".*?answer_status:\s*"([^"]+)"'
    )
    for line in path.read_text(encoding="utf-8").splitlines() if path.exists() else []:
        match = pattern.search(line)
        if match:
            records.append({
                "question_id": match.group(1),
                "source_locator": match.group(2),
                "canonical_answer_destination": match.group(3),
                "answer_status": match.group(4),
            })
    return records


def main() -> int:
    failures: list[str] = []

    def expect(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    registry = {row.get("id"): row for row in parse_registry(REGISTRY)}
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("exact_filename") == "#Week04-Chapter4-1 2024.pdf", "canonical Ch4 Part 1 filename mismatch")
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("sha256") == "f2323c438f260d0b5c37322e78eb0eee7af3e036bec109d68de9db31c4714dae", "canonical Ch4 Part 1 SHA mismatch")
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("page_count") == 74, "canonical Ch4 Part 1 must be 74 pages")
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("status") == "USER_ATTACHMENT_VERIFIED", "canonical Ch4 Part 1 verification status mismatch")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("sha256") == "9221a7e4a42ff88a98ee8f2980d879860ded2abd5e6de04ca35d7f768aee2040", "canonical Ch4 Part 2 SHA mismatch")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("exact_filename") == "#Week05-Chapter4-2 2024.pdf", "canonical Ch4 Part 2 filename mismatch")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("page_count") == 59, "canonical Ch4 Part 2 must be 59 pages")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("status") == "USER_ATTACHMENT_VERIFIED", "canonical Ch4 Part 2 verification status mismatch")
    expect("UIT-SLIDE-CH04-3-2024" not in registry, "unsupported official Ch4 Part 3 identity remains")
    expect(registry.get("UIT-SLIDE-CH04-3-2024-VARIANT-LOCAL-46", {}).get("type") == "source_variant", "local Ch4 Part 3 is not explicitly separated")

    midterm_source = registry.get("UIT-SLIDE-MIDTERM-REVIEW-2024", {})
    expect(midterm_source.get("exact_filename") == "#Week08-Midterm Review.pptx", "canonical Midterm filename mismatch")
    expect(midterm_source.get("sha256") == "cd3da900b5f8c0d4481afae68d4e4e33c6348867118d8f35966eac6203572326", "canonical Midterm SHA mismatch")
    # Canonical Batch 2 source records verified in registry.
    ch5_p1 = registry.get("UIT-SLIDE-CH05-1-2024") or registry.get("UIT-SLIDE-CH05-1-2024-CANONICAL-USER", {})
    ch5_p2 = registry.get("UIT-SLIDE-CH05-2-2024") or registry.get("UIT-SLIDE-CH05-2-2024-CANONICAL-USER", {})
    expect(ch5_p1.get("page_count") == 67, "canonical Ch5 Part 1 evidence missing")
    expect(ch5_p2.get("page_count") == 72, "canonical Ch5 Part 2 evidence missing")

    decks = {row.get("source_id"): row for row in parse_slide_coverage(COVERAGE)}
    p1 = decks.get("UIT-SLIDE-CH04-1-2024", {})
    p2 = decks.get("UIT-SLIDE-CH04-2-2024", {})

    def map_signature(deck: dict) -> list[tuple[str, str]]:
        return [(str(section.get("page_range")), str(section.get("classification"))) for section in deck.get("sections", [])]

    expect(p1.get("physical_pages") == 74, "Ch4 Part 1 coverage physical count mismatch")
    expect(map_signature(p1) == [
        ("1-3", "NON_CONTENT"), ("4-8", "CONTENT"), ("9-18", "CONTENT"),
        ("19-22", "CONTENT"), ("23-27", "CONTENT"), ("28-33", "CONTENT"),
        ("34-47", "CONTENT"), ("48-52", "CONTENT"), ("53-63", "CONTENT"),
        ("64", "CONTENT"), ("65", "CONTENT"), ("66-73", "CONTENT"),
        ("74", "NON_CONTENT")], "Ch4 Part 1 page map is not the verified 74-page map")
    expect(sum(int(section.get("page_count") or 0) for section in p1.get("sections", []) if section.get("classification") == "CONTENT") == 70, "Ch4 Part 1 content count must be 70")
    expect(p2.get("physical_pages") == 59, "Ch4 Part 2 coverage physical count mismatch")
    expect(map_signature(p2) == [
        ("1-2", "NON_CONTENT"), ("3-4", "CONTENT"), ("5-9", "CONTENT"),
        ("10-13", "CONTENT"), ("14-15", "CONTENT"), ("16-17", "CONTENT"),
        ("18-28", "CONTENT"), ("29-37", "CONTENT"), ("38-44", "CONTENT"),
        ("45-51", "CONTENT"), ("52-56", "CONTENT"), ("57", "CONTENT"),
        ("58", "CONTENT"), ("59", "NON_CONTENT")], "Ch4 Part 2 page map is not the verified 59-page map")
    expect(sum(int(section.get("page_count") or 0) for section in p2.get("sections", []) if section.get("classification") == "CONTENT") == 56, "Ch4 Part 2 content count must be 56")
    expect("UIT-SLIDE-CH04-3-2024" not in decks, "Ch4 Part 3 must not be mapped as an official deck")

    midterm_deck = decks.get("UIT-SLIDE-MIDTERM-REVIEW-2024", {})
    expect(midterm_deck.get("physical_pages") == 17, "Midterm coverage must be 17 slides")
    expect(sum(int(section.get("page_count") or 0) for section in midterm_deck.get("sections", [])) == 17, "Midterm coverage has a slide gap/overlap")
    expect(sum(int(section.get("page_count") or 0) for section in midterm_deck.get("sections", []) if section.get("classification") == "CONTENT") == 15, "Midterm content count must be 15 slides")
    expect(not any(sid in decks for sid in ("UIT-SLIDE-CH05-1-2024-CANONICAL-USER", "UIT-SLIDE-CH05-2-2024-CANONICAL-USER")), "future canonical Ch5 attachments must remain unmapped")

    ch4_text = CH4.read_text(encoding="utf-8")
    for term in ("CPU burst", "I/O burst", "CPU-bound", "I/O-bound", "long-term", "medium-term", "short-term", "dispatcher", "dispatch latency", "Selection function", "decision mode", "preemptive", "non-preemptive", "Fairness", "exponential averaging", "(n−1)q", "HRRN", "thread", "AMP", "SMP", "load balancing", "affinity", "periodic", "aperiodic", "sporadic", "RMS", "EDF", "TBS", "Linux CFS", "Windows", "Solaris"):
        expect(term.lower() in ch4_text.lower(), f"Ch4 theory missing required source term: {term}")
    expect("WTavg = 3.00" in ch4_text and "3.25" not in ch4_text, "SRTF arithmetic regression remains")

    ch2_text = CH2_BANK.read_text(encoding="utf-8")
    expect("QUESTION (giữ nguyên wording qbank)" in ch2_text and "Nêu 8 thành phần" in ch2_text, "Ch2 qbank wording was silently rewritten")
    expect("SOURCE CONFLICT" in ch2_text and "bảy" in ch2_text.lower(), "Ch2 source conflict is not preserved")
    ch4_bank_text = CH4_BANK.read_text(encoding="utf-8")
    expect("SOURCE CONFLICT NOTE" in ch4_bank_text and "sáu" in ch4_bank_text.lower(), "Ch4 five-vs-six criteria conflict is not preserved")

    midterm_text = MIDTERM.read_text(encoding="utf-8")
    for heading in ("Chương 1 — Source prompts", "Chương 2 — Source prompts", "Chương 3 — Source prompts", "Chương 4 — Source prompts", "Reference to external exercise set"):
        expect(heading in midterm_text, f"Midterm review missing section: {heading}")
    expect("Solaris không phải prompt" in midterm_text, "Midterm Solaris exclusion is not explicit")

    # Source-question fields must preserve the canonical Midterm wording; normalized
    # topics remain separate metadata and cannot substitute for the slide questions.
    questions = parse_questions(QUESTIONS)
    midterm_questions = [q for q in questions if q.get("source_id") == "UIT-SLIDE-MIDTERM-REVIEW-2024"]
    for question in midterm_questions:
        expected = EXPECTED_MIDTERM_SOURCE_QUESTIONS.get(str(question.get("question_id")))
        expect(expected is not None, f"unexpected Midterm question id: {question.get('question_id')}")
        if expected is not None:
            expect(normalize_source_question(question.get("source_question")) == normalize_source_question(expected), f"source_question mismatch for {question.get('question_id')}")
    for question in midterm_questions:
        if str(question.get("source_locator", "")).startswith("Slide 5"):
            expect(not any(term in str(question.get("source_question")) for term in ("User view", "Hard real-time", "Timer", "protection")), "Slide 5 source question contains normalized-only framing")
        if str(question.get("source_locator", "")).startswith("Slide 7"):
            expect("protection/security" not in str(question.get("source_question")), "Slide 7 protection boundary was promoted to a source question")
    slide15_manifest = next((q for q in midterm_questions if q.get("question_id") == "MIDTERM-REVIEW-33"), {})
    expect(slide15_manifest.get("source_data") == "P1 0 10; P2 2 29; P3 4 3; P4 5 7; P5 7 12", "Slide 15 source_data table is missing or incorrect")
    slide15_question = normalize_source_question(slide15_manifest.get("source_question"))
    expect(slide15_question.endswith("FCFS\nSJF preemptive\nRR với quantum time = 10"), "Slide 15 source_question must preserve canonical algorithm line breaks")
    expect("FCFS;" not in slide15_question and "SJF preemptive;" not in slide15_question, "Slide 15 source_question contains invented semicolon punctuation")
    expect("int main(int argc, char** argv)" in midterm_text and "for (int i = 1; i < 5; i++)" in midterm_text and 'printf("Hello world\\n");' in midterm_text, "Slide 10 source code identity missing")
    expect("New → Ready → Running → Terminated" in midterm_text and "không thể khẳng định" in midterm_text and "Waiting/Blocked" in midterm_text, "Slide 10 lifecycle answer or caveat missing")
    expect("for (i = 0; i < 4; i++)" in midterm_text and 'printf("hello\\n");' in midterm_text and "FINAL_PROCESS_COUNT = 16" in midterm_text and "NEW_CHILDREN_CREATED = 15" in midterm_text and "TOTAL_PRINTF_EXECUTIONS = 2 + 4 + 8 + 16 = 30" in midterm_text, "Slide 11 source/answer facts missing")
    expect("full buffering" in midterm_text and ("thứ tự tương đối không xác định" in midterm_text or "thứ tự lập lịch/output là không xác định" in midterm_text), "Slide 11 buffering/order caveat missing")
    tree_markers = ("P0", "├── P1", "│   ├── P3", "│   │   ├── P7", "│   │   │   └── P15", "│   │   └── P11", "├── P2", "│   ├── P6", "│   │   └── P14", "│   └── P10", "├── P4", "│   └── P12", "└── P8")
    expect(all(marker in midterm_text for marker in tree_markers), "Slide 11 literal parent-child process tree representation missing")
    expect("mọi process đi tới vòng đó đều gọi `fork()` đúng một lần" in midterm_text and "cây process literal" in midterm_text, "Slide 11 tree/doubling distinction missing")
    slide15_start = midterm_text.find("### Slide 15 — Source-faithful solution (canonical dataset)")
    slide15_end = midterm_text.find("### E1.", slide15_start)
    slide15_text = midterm_text[slide15_start:slide15_end if slide15_end != -1 else None]
    for marker in ("P1(AT=0, BT=10)", "P2(AT=2, BT=29)", "P3(AT=4, BT=3)", "P4(AT=5, BT=7)", "P5(AT=7, BT=12)", "FCFS", "SRTF", "q=10", "WTavg = 24.4", "WTavg = 10.8", "WTavg = 19.4", "RTavg = 24.4", "RTavg = 10.2", "RTavg = 13.0", "TATavg = 36.6", "TATavg = 23.0", "TATavg = 31.6"):
        expect(marker in slide15_text, f"Slide 15 canonical answer missing: {marker}")
    expect("additional practice fixture" in midterm_text, "old scheduling fixture is not labelled as additional practice")

    # Reuse the parsed Midterm records for occurrence and accounting checks.
    concrete = [q for q in midterm_questions if q.get("counting_class") == "CONCRETE_OCCURRENCE"]
    references = [q for q in midterm_questions if q.get("counting_class") == "REFERENCE_TO_EXTERNAL_EXERCISE_SET"]
    expect(len(concrete) == 33, f"Midterm concrete occurrence count is {len(concrete)}, expected 33")
    expect(len(references) == 2, f"Midterm external-reference count is {len(references)}, expected 2")
    expect(not any("Solaris" in str(q.get("topic")) or "Solaris" in str(q.get("source_locator")) for q in midterm_questions), "Solaris remains a fake Midterm question")
    expected_bullets = {5: 9, 7: 5, 9: 6, 14: 10}
    for slide, count in expected_bullets.items():
        actual = sum(1 for q in concrete if f"Slide {slide} / bullet" in str(q.get("source_locator")))
        expect(actual == count, f"Midterm slide {slide} has {actual} bullet occurrences, expected {count}")
    expect(sum(1 for q in concrete if q.get("source_locator") == "Slide 10 / compound exercise") == 1, "Midterm slide 10 compound occurrence missing")
    expect(sum(1 for q in concrete if q.get("source_locator") == "Slide 11 / compound exercise") == 1, "Midterm slide 11 compound occurrence missing")
    expect(sum(1 for q in concrete if q.get("source_locator") == "Slide 15 / compound scheduling exercise") == 1, "Midterm slide 15 compound occurrence missing")
    qbank = [q for q in questions if str(q.get("source_id", "")).startswith("UIT-QBANK-")]
    expect(len(qbank) == 60, f"dedicated qbank record count is {len(qbank)}, expected 60")
    expect(len([q for q in qbank if q.get("source_id") in {"UIT-QBANK-CH01-2024", "UIT-QBANK-CH02-2024", "UIT-QBANK-CH03-2024", "UIT-QBANK-CH04-2024"}]) == 31, "Batch 1 qbank count is not 31")

    # Every Midterm occurrence has an explicit, auditable answer destination.
    answer_mapping = parse_answer_mapping(MIDTERM_MAPPING)
    expect(len(answer_mapping) == 35, f"Midterm answer mapping has {len(answer_mapping)} records, expected 35")
    expect(sum(1 for row in answer_mapping if row["question_id"].startswith("MIDTERM-REVIEW-REF-")) == 2, "Midterm answer mapping must preserve exactly two external references")
    expect(sum(1 for row in answer_mapping if not row["question_id"].startswith("MIDTERM-REVIEW-REF-")) == 33, "Midterm answer mapping must contain exactly 33 concrete occurrences")
    expected_statuses = {"ANSWER_VERIFIED", "PARTIAL", "MISSING"}
    manifest_by_id = {str(q.get("question_id")): q for q in midterm_questions}
    for row in answer_mapping:
        expect(row["answer_status"] in expected_statuses, f"invalid answer status for {row['question_id']}")
        manifest = manifest_by_id.get(row["question_id"])
        expect(manifest is not None, f"answer mapping question is not in manifest: {row['question_id']}")
        if manifest is not None:
            expect(row["source_locator"] == manifest.get("source_locator"), f"source locator mismatch for {row['question_id']}")
        destination = row["canonical_answer_destination"]
        if destination == "REFERENCE_TO_EXTERNAL_EXERCISE_SET":
            expect(row["question_id"].startswith("MIDTERM-REVIEW-REF-"), f"non-reference mapped to external set: {row['question_id']}")
            continue
        file_part, _, anchor = destination.partition("#")
        target = ROOT / file_part
        expect(target.exists(), f"answer destination file missing for {row['question_id']}: {file_part}")
        if target.exists() and anchor:
            target_text = target.read_text(encoding="utf-8")
            heading_slugs = {
                re.sub(r"[^a-zA-Z0-9_-]+", "-", unicodedata.normalize("NFKD", heading).encode("ascii", "ignore").decode("ascii").lower()).strip("-")
                for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*$", target_text, flags=re.MULTILINE)
            }
            expect(anchor in heading_slugs, f"answer destination anchor missing for {row['question_id']}: {destination}")
    concrete_mapping = [row for row in answer_mapping if not row["question_id"].startswith("MIDTERM-REVIEW-REF-")]
    expect(not any(row["answer_status"] != "ANSWER_VERIFIED" for row in concrete_mapping), "Midterm concrete answer coverage contains PARTIAL or MISSING records")
    mapping_by_id = {row["question_id"]: row for row in answer_mapping}
    expect(mapping_by_id.get("MIDTERM-REVIEW-21", {}).get("canonical_answer_destination") == "content/reviews/midterm.md#slide-10-source-faithful-state-transition-answer", "Slide 10 answer is not mapped to its dedicated source-faithful section")
    expect(mapping_by_id.get("MIDTERM-REVIEW-22", {}).get("canonical_answer_destination") == "content/reviews/midterm.md#slide-11-source-faithful-fork-output-answer", "Slide 11 answer is not mapped to its dedicated source-faithful section")
    expect(mapping_by_id.get("MIDTERM-REVIEW-33", {}).get("canonical_answer_destination") == "content/reviews/midterm.md#slide-15-source-faithful-solution-canonical-dataset", "Slide 15 answer is not mapped to its dedicated source-faithful section")

    if failures:
        print("BATCH 1 CANONICAL SOURCE VALIDATION: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("BATCH 1 CANONICAL SOURCE VALIDATION: PASS (Ch4 74/70 + 59/56; Midterm 17 slides, 33 occurrences)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

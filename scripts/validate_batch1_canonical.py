#!/usr/bin/env python3
"""Deterministic source-fidelity gates for the Batch 1 canonical map."""

from __future__ import annotations

import re
import sys
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


def main() -> int:
    failures: list[str] = []

    def expect(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    registry = {row.get("id"): row for row in parse_registry(REGISTRY)}
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("exact_filename") == "#Week04-Chapter4-1 2024.pdf", "canonical Ch4 Part 1 filename mismatch")
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("sha256") == "f2323c438f260d0b5c37322e78eb0eee7af3e036bec109d68de9db31c4714dae", "canonical Ch4 Part 1 SHA mismatch")
    expect(registry.get("UIT-SLIDE-CH04-1-2024", {}).get("page_count") == 74, "canonical Ch4 Part 1 must be 74 pages")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("sha256") == "9221a7e4a42ff88a98ee8f2980d879860ded2abd5e6de04ca35d7f768aee2040", "canonical Ch4 Part 2 SHA mismatch")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("exact_filename") == "#Week05-Chapter4-2 2024.pdf", "canonical Ch4 Part 2 filename mismatch")
    expect(registry.get("UIT-SLIDE-CH04-2-2024", {}).get("page_count") == 59, "canonical Ch4 Part 2 must be 59 pages")
    expect("UIT-SLIDE-CH04-3-2024" not in registry, "unsupported official Ch4 Part 3 identity remains")
    expect(registry.get("UIT-SLIDE-CH04-3-2024-VARIANT-LOCAL-46", {}).get("type") == "source_variant", "local Ch4 Part 3 is not explicitly separated")

    midterm_source = registry.get("UIT-SLIDE-MIDTERM-REVIEW-2024", {})
    expect(midterm_source.get("exact_filename") == "#Week08-Midterm Review.pptx", "canonical Midterm filename mismatch")
    expect(midterm_source.get("sha256") == "cd3da900b5f8c0d4481afae68d4e4e33c6348867118d8f35966eac6203572326", "canonical Midterm SHA mismatch")
    expect(midterm_source.get("slide_count") == 17, "canonical Midterm must be 17 slides")
    expect(registry.get("UIT-SLIDE-MIDTERM-REVIEW-2024-VARIANT-LOCAL-16PDF", {}).get("type") == "source_variant", "16-page Midterm PDF is not separated")

    # The future Batch 2 attachments are recorded without being mapped into Ch5 coverage.
    expect(registry.get("UIT-SLIDE-CH05-1-2024-CANONICAL-USER", {}).get("page_count") == 67, "future canonical Ch5 Part 1 evidence missing")
    expect(registry.get("UIT-SLIDE-CH05-2-2024-CANONICAL-USER", {}).get("page_count") == 72, "future canonical Ch5 Part 2 evidence missing")

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

    questions = parse_questions(QUESTIONS)
    midterm_questions = [q for q in questions if q.get("source_id") == "UIT-SLIDE-MIDTERM-REVIEW-2024"]
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

    if failures:
        print("BATCH 1 CANONICAL SOURCE VALIDATION: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("BATCH 1 CANONICAL SOURCE VALIDATION: PASS (Ch4 74/70 + 59/56; Midterm 17 slides, 33 occurrences)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

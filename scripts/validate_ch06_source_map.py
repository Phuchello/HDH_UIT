#!/usr/bin/env python3
"""Deterministic Chapter 6 canonical source-map validator.

This validator checks only source-map evidence and lifecycle invariants.  It
never asserts textbook facts that are not represented by the inspected source
map.  Pass a --source-root containing the exact local source corpus to repeat
binary hash/page/XML verification; without it, the validator fails closed.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "content/sources/registry.yaml"
COVERAGE = ROOT / "research/data/slide_coverage.yaml"
QUESTIONS = ROOT / "research/data/official_review_questions.yaml"
REPORT = ROOT / "research/LUNA_CH6_SOURCE_MAP_REPORT.md"
SLIDE_ID = "UIT-SLIDE-CH06-2024"
QBANK_ID = "UIT-QBANK-CH06-2024"
SLIDE_SHA = "e55bf22554028859fc30747a39e72d97ca6e1e3c37e5a1bdcdc5ab94a7c3b56e"
QBANK_SHA = "f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803"
SLIDE_BYTES = 5816540
QBANK_BYTES = 101550
SLIDE_PAGES = 67
EXPECTED_RANGES = [
    ("1-3", "NON_CONTENT"), ("4-7", "CONTENT"), ("8-9", "CONTENT"),
    ("10-12", "CONTENT"), ("13-14", "CONTENT"), ("15-17", "CONTENT"),
    ("18-21", "CONTENT"), ("22-24", "CONTENT"), ("25-26", "CONTENT"),
    ("27-31", "CONTENT"), ("32-33", "CONTENT"), ("34-37", "CONTENT"),
    ("38-40", "CONTENT"), ("41-44", "CONTENT"), ("45-49", "CONTENT"),
    ("50-54", "CONTENT"), ("55-58", "CONTENT"), ("59-62", "CONTENT"),
    ("63", "CONTENT"), ("64-66", "CONTENT"), ("67", "NON_CONTENT"),
]
REQUIRED_TOPICS = ("deadlock", "resource", "coffman", "rag", "ngăn", "tránh", "safe", "banker", "request", "detection", "wait-for", "recovery")

sys.path.insert(0, str(ROOT / "scripts"))
from research_utils import parse_page_range, parse_registry, parse_questions, parse_slide_coverage  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def qbank_counts(path: Path) -> tuple[int, int]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = ET.fromstring(ZipFile(path).read("word/document.xml"))
    paragraphs = root.findall(".//w:p", ns)
    nonempty = sum(bool("".join(p.itertext()).strip()) for p in paragraphs)
    return len(paragraphs), nonempty


def find_one(source_root: Path, filename: str) -> Path | None:
    matches = sorted(source_root.rglob(filename))
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", help="Directory containing the exact canonical binaries")
    args = parser.parse_args()
    failures: list[str] = []
    registry = {row.get("id"): row for row in parse_registry(REGISTRY)}
    slide = registry.get(SLIDE_ID)
    qbank = registry.get(QBANK_ID)
    if not slide or slide.get("sha256") != SLIDE_SHA or slide.get("page_count") != SLIDE_PAGES or slide.get("byte_size") != SLIDE_BYTES or slide.get("status") != "VERIFIED_LOCAL":
        failures.append("canonical slide registry identity/size/page-count mismatch")
    if not qbank or qbank.get("sha256") != QBANK_SHA or qbank.get("byte_size") != QBANK_BYTES or qbank.get("status") != "VERIFIED_LOCAL":
        failures.append("canonical QBank registry identity/size mismatch")
    source_root = Path(args.source_root).resolve() if args.source_root else None
    if source_root is None:
        failures.append("binary evidence requires --source-root (fail-closed)")
    elif not source_root.is_dir():
        failures.append(f"source root is not a directory: {source_root}")
    else:
        slide_path = find_one(source_root, "Week11-Chapter6 2024.pdf")
        qbank_path = find_one(source_root, "Bai tap chuong 6 HDH.docx")
        if slide_path is None:
            failures.append("canonical slide binary not found or ambiguous")
        else:
            if sha256(slide_path) != SLIDE_SHA or slide_path.stat().st_size != SLIDE_BYTES:
                failures.append("canonical slide hash/byte-size mismatch")
            try:
                from pypdf import PdfReader
                if len(PdfReader(str(slide_path)).pages) != SLIDE_PAGES:
                    failures.append("canonical slide physical page count mismatch")
                if any(not (p.extract_text() or "").strip() for p in PdfReader(str(slide_path)).pages):
                    failures.append("canonical slide contains an uninspectable/empty physical page")
            except Exception as exc:
                failures.append(f"canonical slide inspection failed: {exc}")
        if qbank_path is None:
            failures.append("canonical QBank binary not found or ambiguous")
        else:
            if sha256(qbank_path) != QBANK_SHA or qbank_path.stat().st_size != QBANK_BYTES:
                failures.append("canonical QBank hash/byte-size mismatch")
            try:
                total, nonempty = qbank_counts(qbank_path)
                if (total, nonempty) != (582, 560):
                    failures.append(f"canonical QBank XML counts mismatch: {total}/{nonempty}")
            except Exception as exc:
                failures.append(f"canonical QBank XML inspection failed: {exc}")
    decks = {row.get("source_id"): row for row in parse_slide_coverage(COVERAGE)}
    deck = decks.get(SLIDE_ID)
    if not deck or deck.get("physical_pages") != SLIDE_PAGES:
        failures.append("Chapter 6 coverage deck missing or page count is not 67")
    else:
        sections = deck.get("sections", [])
        signature = [(str(s.get("page_range")), s.get("classification")) for s in sections]
        if signature != EXPECTED_RANGES:
            failures.append("Chapter 6 coverage does not match the inspected semantic range signature")
        pages = [p for s in sections for p in parse_page_range(s.get("page_range"))]
        if sorted(pages) != list(range(1, SLIDE_PAGES + 1)) or len(set(pages)) != SLIDE_PAGES:
            failures.append("Chapter 6 coverage has page gaps, overlaps, or out-of-range pages")
        if sum(s.get("classification") == "CONTENT" for s in sections for _ in parse_page_range(s.get("page_range"))) != 63:
            failures.append("Chapter 6 CONTENT page count is not 63")
        if sum(s.get("classification") == "NON_CONTENT" for s in sections for _ in parse_page_range(s.get("page_range"))) != 4:
            failures.append("Chapter 6 NON_CONTENT page count is not 4")
        for section in sections:
            if section.get("mapping_status") != "MAPPED" or section.get("content_status") != "NOT_WRITTEN":
                failures.append(f"Chapter 6 lifecycle status invalid at {section.get('page_range')}")
        topics = " ".join(str(s.get("topic", "")).lower() for s in sections)
        missing_topics = [term for term in REQUIRED_TOPICS if term not in topics]
        if missing_topics:
            failures.append("required source locators absent from coverage topics: " + ", ".join(missing_topics))
    qrows = [q for q in parse_questions(QUESTIONS) if q.get("source_id") == QBANK_ID]
    if [q.get("question_id") for q in qrows] != [f"QBANK-CH06-0{i}" for i in range(1, 7)]:
        failures.append("Chapter 6 structured question IDs are not the established six-record map")
    if any(q.get("mapping_status") != "MAPPED" or q.get("content_status") != "NOT_WRITTEN" for q in qrows):
        failures.append("Chapter 6 question records are not mapped/not-written")
    if (ROOT / "content/theory/ch06-deadlock.md").exists() or (ROOT / "content/questions/subjective/ch06.md").exists():
        failures.append("Chapter 6 authoring file exists before source-map closeout")
    try:
        changed = subprocess.run(["git", "diff", "--name-only"], cwd=ROOT, capture_output=True, text=True, check=False).stdout.splitlines()
        locked = [p for p in changed if re.match(r"(?:content/theory/ch0[1-5]|content/questions/subjective/ch0[1-5]|content/reviews/midterm)", p.replace("\\", "/"))]
        if locked:
            failures.append("locked Chapters 1-5 changed: " + ", ".join(locked))
    except Exception as exc:
        failures.append(f"could not inspect locked-file diff: {exc}")
    required_report_headings = ["REVIEWED HEAD", "SOURCE BINARIES DISCOVERED", "CANONICAL SOURCE IDENTITY", "EXCLUDED VARIANTS", "COURSE OUTLINE ALIGNMENT", "PAGE-BY-PAGE / RANGE MAP", "SOURCE-STRUCTURE CONFLICTS", "CH5/CH6 BOUNDARY", "ALGORITHM / NUMERICAL LOCATORS", "QBANK IDENTITY AND INVENTORY", "EVIDENCE LIMITATIONS", "FINDINGS", "FINAL DECISION"]
    report_text = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    failures.extend(f"source-map report missing section: {heading}" for heading in required_report_headings if heading not in report_text)
    if failures:
        print("CHAPTER 6 SOURCE MAP: FAIL")
        for failure in failures:
            print(" - " + failure)
        return 1
    print("CHAPTER 6 SOURCE MAP: PASS")
    print("  canonical slide: 67 pages / 5,816,540 bytes / SHA verified")
    print("  canonical QBank: 582 XML paragraphs / 560 non-empty / SHA verified")
    print("  coverage: 63 CONTENT + 4 NON_CONTENT, no gaps or overlaps")
    print("  Chapter 6 authoring: NOT_STARTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
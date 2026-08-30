#!/usr/bin/env python3
"""Verify V2 research evidence without hidden workstation paths or magic totals."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "research" / "data"
REGISTRY_PATH = ROOT / "content" / "sources" / "registry.yaml"
OUTPUT_MD = ROOT / "research" / "RESEARCH_GATE_QA.md"
VERIFICATION_JSON = DATA_DIR / "source_verification.json"
EXPANDED_COVERAGE_JSON = DATA_DIR / "slide_coverage_expanded.json"

sys.stdout.reconfigure(encoding="utf-8")

from research_utils import expand_coverage, parse_exams, parse_page_range, parse_questions, parse_registry, parse_slide_coverage


def _page_count(path: Path):
    if path.suffix.lower() != ".pdf":
        return None
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except Exception:
        return None


def _local_source_verification(registry, source_root: Path | None):
    local_mode = source_root is not None
    if local_mode and not source_root.is_dir():
        raise ValueError(f"--source-root is not a directory: {source_root}")
    rows = []
    for source in registry:
        if source.get("tier") != "A":
            continue
        filename = source.get("exact_filename")
        found = list(source_root.rglob(str(filename))) if local_mode and filename else []
        path = found[0] if found else None
        actual_sha = hashlib.sha256(path.read_bytes()).hexdigest() if path else None
        actual_pages = _page_count(path) if path else None
        expected_sha = source.get("sha256")
        expected_pages = source.get("page_count")
        rows.append({
            "source_id": source.get("id"),
            "file_present": bool(path),
            "actual_sha256": actual_sha,
            "hash_match": (actual_sha == expected_sha) if path and expected_sha else None,
            "actual_page_count": actual_pages,
            "page_count_match": (actual_pages == expected_pages) if actual_pages is not None and expected_pages is not None else None,
            "verification_timestamp": datetime.now(timezone.utc).isoformat(),
        })
    VERIFICATION_JSON.write_text(json.dumps({
        "mode": "LOCAL_SOURCE_VERIFICATION" if local_mode else "REPO_ONLY",
        "sources": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not local_mode:
        return rows, True
    return rows, all(r["file_present"] and r["hash_match"] is True and (r["page_count_match"] in (True, None)) for r in rows)


def _coverage_metrics(decks, registry):
    slide_sources = {s.get("id"): s for s in registry if s.get("type") == "official_slide"}
    physical_from_registry = sum(int(s.get("page_count") or 0) for s in slide_sources.values())
    expanded = expand_coverage(decks)
    duplicate_pages = []
    gaps = []
    schema_errors = []
    deck_results = []
    for deck in decks:
        sid = deck.get("source_id")
        expected = int(deck.get("physical_pages") or 0)
        pages = []
        malformed = []
        for section in deck.get("sections", []):
            section_pages = parse_page_range(section.get("page_range"))
            if section.get("page_count") != len(section_pages):
                malformed.append(section.get("page_range"))
            for field in ("topic", "classification", "mapping_status", "v2_destination", "content_status"):
                if section.get(field) in (None, ""):
                    schema_errors.append(f"{sid}:{section.get('page_range')}:{field}")
            pages.extend(section_pages)
        seen = set()
        for page in pages:
            if page in seen:
                duplicate_pages.append(f"{sid}:{page}")
            seen.add(page)
        expected_set = set(range(1, expected + 1))
        gaps.extend(f"{sid}:{p}" for p in sorted(expected_set - seen))
        gaps.extend(f"{sid}:{p}(out-of-range)" for p in sorted(seen - expected_set))
        deck_results.append({
            "source_id": sid,
            "physical_pages": expected,
            "covered_pages": len(pages),
            "coverage_complete": seen == expected_set and not malformed,
            "malformed_ranges": malformed,
        })
        if sid in slide_sources and int(slide_sources[sid].get("page_count") or 0) != expected:
            gaps.append(f"{sid}:registry_page_count_mismatch")
    content = sum(1 for p in expanded if p.get("classification") == "CONTENT")
    non_content = sum(1 for p in expanded if p.get("classification") == "NON_CONTENT")
    mapped = sum(1 for p in expanded if p.get("classification") == "CONTENT" and p.get("mapping_status") == "MAPPED")
    unmapped = sum(1 for p in expanded if p.get("classification") == "CONTENT" and p.get("mapping_status") != "MAPPED")
    drafted = sum(1 for p in expanded if p.get("classification") == "CONTENT" and p.get("content_status") == "DRAFTED")
    EXPANDED_COVERAGE_JSON.write_text(json.dumps({
        "schema": "one-record-per-physical-page",
        "records": expanded,
        "coverage_gaps": gaps,
        "duplicate_pages": duplicate_pages,
        "schema_errors": schema_errors,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "physical_pages_total": physical_from_registry,
        "coverage_pages_total": len(expanded),
        "content_pages_total": content,
        "non_content_pages_total": non_content,
        "mapped_content_pages": mapped,
        "unmapped_content_pages": unmapped,
        "drafted_content_pages": drafted,
        "coverage_gaps": gaps,
        "duplicate_pages": duplicate_pages,
        "schema_errors": schema_errors,
        "deck_results": deck_results,
    }


def _run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return result.returncode == 0, (result.stdout + "\n" + result.stderr).strip()


def verify_gates(source_root=None):
    print(">>> Executing Evidence-Driven Research Gate Verification...")
    registry = parse_registry(REGISTRY_PATH)
    registry_ids = [s.get("id") for s in registry if s.get("id")]
    duplicate_ids = len(registry_ids) - len(set(registry_ids))
    registry_schema_ok = bool(registry) and duplicate_ids == 0 and all(s.get("id") and s.get("title") and s.get("type") for s in registry)

    verification_rows, source_verification_ok = _local_source_verification(registry, Path(source_root).resolve() if source_root else None)
    decks = parse_slide_coverage(DATA_DIR / "slide_coverage.yaml")
    slides = _coverage_metrics(decks, registry)
    questions = parse_questions(DATA_DIR / "official_review_questions.yaml")
    required_question_fields = ("source_id", "question_id", "source_locator", "topic", "mapping_status", "v2_destination", "content_status")
    question_schema_ok = bool(questions) and all(all(q.get(k) not in (None, "") for k in required_question_fields) for q in questions)
    question_ids = [q.get("question_id") for q in questions]
    question_id_ok = len(question_ids) == len(set(question_ids))
    mapped_questions = sum(q.get("mapping_status") == "MAPPED" for q in questions)
    unmapped_questions = len(questions) - mapped_questions
    drafted_questions = sum(q.get("content_status") == "DRAFTED" for q in questions)

    exams = parse_exams(DATA_DIR / "exam_evidence.yaml")
    exam_schema_ok = bool(exams) and all(e.get("exam_id") and e.get("source_id") and e.get("classification") for e in exams)
    hygiene_ok, _ = _run([sys.executable, "scripts/check_public_hygiene.py"])
    content_ok, _ = _run([sys.executable, "scripts/validate_v2_content.py"])

    slide_invariants_ok = (
        bool(decks)
        and not slides["coverage_gaps"]
        and not slides["duplicate_pages"]
        and not slides["schema_errors"]
        and slides["physical_pages_total"] == slides["coverage_pages_total"]
        and slides["content_pages_total"] + slides["non_content_pages_total"] == slides["physical_pages_total"]
        and slides["unmapped_content_pages"] == 0
    )
    questions_ok = question_schema_ok and question_id_ok and unmapped_questions == 0
    overall = all((registry_schema_ok, source_verification_ok, slide_invariants_ok, questions_ok, exam_schema_ok, hygiene_ok, content_ok))
    status = lambda ok: "PASS" if ok else "FAIL"
    mode = "LOCAL_SOURCE_VERIFICATION" if source_root else "REPO_ONLY"
    report = f"""# RESEARCH GATE QUALITY ASSURANCE REPORT (HDH_UIT V2)

**Thời gian thẩm định:** {datetime.now(timezone.utc).date().isoformat()}
**Chế độ:** `{mode}`
**GATE STATUS:** **{"PASS" if overall else "FAIL"}**

All totals below are computed from registry records, expanded slide-page records, and question records. The former summary targets are informational only and are never used as gate inputs.

| Metric | Actual | Requirement | Result |
|---|---:|---|:---:|
| Registered sources | {len(registry)} | unique IDs and required schema | **{status(registry_schema_ok)}** |
| Tier-A local files / hash checks | {sum(r['file_present'] for r in verification_rows)} / {sum(r['hash_match'] is True for r in verification_rows)} | REPO_ONLY is informational; LOCAL requires all hashes | **{status(source_verification_ok)}** |
| Physical slide pages | {slides['physical_pages_total']} | sum of official-slide registry page counts | **PASS** |
| Expanded coverage records | {slides['coverage_pages_total']} | exactly physical-page total | **{status(slides['coverage_pages_total'] == slides['physical_pages_total'])}** |
| Content / non-content pages | {slides['content_pages_total']} / {slides['non_content_pages_total']} | sum equals physical total | **{status(slides['content_pages_total'] + slides['non_content_pages_total'] == slides['physical_pages_total'])}** |
| Coverage gaps / duplicates / schema errors | {len(slides['coverage_gaps'])} / {len(slides['duplicate_pages'])} / {len(slides['schema_errors'])} | zero | **{status(not slides['coverage_gaps'] and not slides['duplicate_pages'] and not slides['schema_errors'])}** |
| Unmapped content pages | {slides['unmapped_content_pages']} | zero | **{status(slides['unmapped_content_pages'] == 0)}** |
| Drafted content pages | {slides['drafted_content_pages']} | informational current authored set | **INFO** |
| Official question records | {len(questions)} | count of structured records | **{status(questions_ok)}** |
| Mapped / unmapped questions | {mapped_questions} / {unmapped_questions} | zero unmapped; required fields | **{status(questions_ok)}** |
| Drafted questions | {drafted_questions} | informational current authored set | **INFO** |
| Exam evidence records | {len(exams)} | valid record schema | **{status(exam_schema_ok)}** |
| Public hygiene | — | no forbidden paths | **{status(hygiene_ok)}** |
| Canonical content validation | — | schema/rubric/wikilink checks | **{status(content_ok)}** |

## Coverage integrity

Every declared slide range is expanded into `research/data/slide_coverage_expanded.json`. Each deck is checked for malformed ranges, overlaps, gaps, and registry page-count mismatches.
Coverage gaps: `{len(slides['coverage_gaps'])}`; duplicate physical pages: `{len(slides['duplicate_pages'])}`.

## Source verification semantics

`REPO_ONLY` validates registry/schema references and deliberately does not claim workstation files are present. `LOCAL_SOURCE_VERIFICATION` requires `--source-root`, locates exact filenames below that root, computes hashes, and records only portable IDs/results (never absolute paths) in `research/data/source_verification.json`.
"""
    OUTPUT_MD.write_text(report, encoding="utf-8")
    print(f"Generated {OUTPUT_MD} with status: {'PASS' if overall else 'FAIL'}")
    return overall


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", help="Explicit local source directory for LOCAL_SOURCE_VERIFICATION")
    args = parser.parse_args()
    sys.exit(0 if verify_gates(args.source_root) else 1)

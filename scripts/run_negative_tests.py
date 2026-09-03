#!/usr/bin/env python3
"""Inject one defect at a time and prove each foundation gate fails."""

from __future__ import annotations

import subprocess
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "research" / "GATE_NEGATIVE_TESTS.md"


def safe_evidence(output: str) -> str:
    """Keep failure evidence useful without publishing workstation paths."""
    compact = output.replace(str(ROOT), "<REPO_ROOT>")
    compact = re.sub(r"[A-Za-z]:\\Users\\[^\\\s]+(?:\\[^\s]*)?", "<LOCAL_PATH>", compact)
    return compact[:240].replace("\n", " ")


def run_case(name, mutate, command, expected):
    changed = []
    try:
        changed = mutate()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        output = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
        passed = result.returncode != 0 and expected.lower() in output.lower()
        return {"name": name, "passed": passed, "exit_code": result.returncode, "evidence": safe_evidence(output)}
    finally:
        for path, original in reversed(changed):
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(original, encoding="utf-8")


def replace(path, old, new):
    original = path.read_text(encoding="utf-8")
    if old not in original:
        raise RuntimeError(f"mutation anchor not found: {path}")
    path.write_text(original.replace(old, new, 1), encoding="utf-8")
    return [(path, original)]


def append_text(path, text):
    original = path.read_text(encoding="utf-8")
    path.write_text(original + text, encoding="utf-8")
    return [(path, original)]


def main():
    py = sys.executable
    registry = ROOT / "content/sources/registry.yaml"
    ch01 = ROOT / "content/theory/ch01-overview.md"
    slides = ROOT / "research/data/slide_coverage.yaml"
    exam = ROOT / "content/exams/midterm/2023-2024-hk1.md"
    cases = []
    cases.append(run_case("NEG-01 duplicate source ID", lambda: replace(registry, "\n  - id: \"UIT-SLIDE-CH01-2024\"", "\n  - id: \"UIT-SLIDE-CH01-2024\"\n  - id: \"UIT-SLIDE-CH01-2024\""), [py, "scripts/validate_sources.py"], "Duplicate source ID"))
    cases.append(run_case("NEG-02 unknown source reference", lambda: replace(ch01, '  - "UIT-SLIDE-CH01-2024"', '  - "NO-SUCH-SOURCE"'), [py, "scripts/validate_sources.py"], "Unknown source ID"))
    cases.append(run_case("NEG-03 malformed source hash", lambda: replace(registry, 'sha256: "4fc70c3a35d9632d678be2dbc5df1082388064a782b20a6bb7795c9a5d5adc62"', 'sha256: "not-a-sha256"'), [py, "scripts/validate_sources.py"], "invalid sha256"))
    cases.append(run_case("NEG-04 unmapped slide page", lambda: replace(slides, 'topic: "Định nghĩa & Vai trò HDH (User view vs System view)"\n        mapping_status: "MAPPED"', 'topic: "Định nghĩa & Vai trò HDH (User view vs System view)"\n        mapping_status: "UNMAPPED"'), [py, "scripts/verify_research_gates.py"], "status: FAIL"))
    cases.append(run_case("NEG-05 forbidden workstation path", lambda: append_text(ch01, "\n<!-- C:\\Users\\injected -->\n"), [py, "scripts/check_public_hygiene.py"], "PUBLIC HYGIENE AUDIT FAILED"))
    cases.append(run_case("NEG-06 broken wikilink", lambda: append_text(ch01, "\n[[missing-document]]\n"), [py, "scripts/validate_v2_content.py"], "Broken wikilink"))

    rubric_path = ROOT / "content/questions/subjective/ch01.md"
    cases.append(run_case("NEG-07 unsupported OFFICIAL_RUBRIC", lambda: append_text(rubric_path, "\nBarem Chấm Điểm Chính Thức\n"), [py, "scripts/validate_v2_content.py"], "SELF_CHECK_RUBRIC"))

    duplicate = ROOT / "content/fixtures/duplicate-id.md"
    def add_duplicate():
        duplicate.parent.mkdir(parents=True, exist_ok=True)
        duplicate.write_text('---\nid: "theory-ch01-overview"\ntitle: "duplicate"\n---\n', encoding="utf-8")
        return [(duplicate, None)]
    cases.append(run_case("NEG-08 duplicate document ID", add_duplicate, [py, "scripts/validate_v2_content.py"], "Duplicate document ID"))
    cases.append(run_case("NEG-09 malformed exam classification", lambda: replace(exam, 'classification: "RECONSTRUCTED_PRACTICE"', 'classification: "INVENTED_EXAM"'), [py, "scripts/validate_v2_content.py"], "invalid classification"))
    cases.append(run_case("NEG-10 duplicate slide page", lambda: replace(slides, 'page_range: "4-8"\n        page_count: 5', 'page_range: "1-8"\n        page_count: 8'), [py, "scripts/verify_research_gates.py"], "status: FAIL"))
    cases.append(run_case("NEG-11 missing slide page", lambda: replace(slides, 'page_range: "56-57"\n        page_count: 2', 'page_range: "57"\n        page_count: 1'), [py, "scripts/verify_research_gates.py"], "status: FAIL"))

    passed = all(case["passed"] for case in cases)
    rows = "\n".join(f"| {case['name']} | exit {case['exit_code']} | {'PASS' if case['passed'] else 'FAIL'} | {case['evidence']} |" for case in cases)
    REPORT.write_text(f"# Gate Negative Tests\n\n**Result:** **{'PASS' if passed else 'FAIL'}** ({sum(c['passed'] for c in cases)}/{len(cases)} defects rejected)\n\n| Injected defect | Exit | Result | Evidence |\n|---|---:|:---:|---|\n{rows}\n\nEach mutation is restored in a `finally` block before the next case.\n", encoding="utf-8")
    print(f"NEGATIVE TESTS: {'PASS' if passed else 'FAIL'} ({sum(c['passed'] for c in cases)}/{len(cases)})")
    return passed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

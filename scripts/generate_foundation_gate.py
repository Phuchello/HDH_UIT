#!/usr/bin/env python3
"""Run the foundation gates and generate a truthful machine-readable report."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "research/V2_FOUNDATION_GATE.md"


def run(name, command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {"name": name, "ok": result.returncode == 0, "output": (result.stdout + "\n" + result.stderr).strip()}


def main():
    py = sys.executable
    steps = [
        run("validate_sources", [py, "scripts/validate_sources.py"]),
        run("check_public_hygiene", [py, "scripts/check_public_hygiene.py"]),
        run("validate_v2_content", [py, "scripts/validate_v2_content.py"]),
        run("build_web", [py, "scripts/build_web.py"]),
        run("validate_site_routes", [py, "scripts/validate_site_routes.py"]),
        run("renderer_stress_test", [py, "scripts/stress_test_web_renderer.py"]),
        run("negative_tests", [py, "scripts/run_negative_tests.py"]),
        run("verify_research_gates", [py, "scripts/verify_research_gates.py"]),
    ]
    passed = all(step["ok"] for step in steps)
    generator = "CUSTOM_STATIC_GENERATOR"
    quartz = "IMPLEMENTED" if (ROOT / "node_modules/@jackyzha0/quartz").exists() else "NOT_IMPLEMENTED / INFO"
    rows = []
    for step in steps:
        rows.append(f"| `{step['name']}` | {'PASS' if step['ok'] else 'FAIL'} |")
    rows.append(f"| `REAL_QUARTZ_CLI` | INFO — {quartz} (does not gate readiness) |")
    report = f"""# V2 FOUNDATION GATE REPORT — HDH_UIT

**Generated:** {datetime.now(timezone.utc).isoformat()}
**Site generator:** `{generator}`
**Foundation Gate:** **{'PASS' if passed else 'FAIL'}**
**Ready to scale content:** **{'YES' if passed else 'NO'}**

The custom generator is the declared architecture. Quartz CLI is informational only. Gate decisions below are based on executed validators and their exit codes; no fixed page/question totals are embedded in this report.

| Check | Result |
|---|:---:|
{chr(10).join(rows)}

## Evidence outputs

- `research/RESEARCH_GATE_QA.md` — computed registry, source-mode, slide-page, and question metrics.
- `research/data/source_verification.json` — portable `REPO_ONLY` or explicit `LOCAL_SOURCE_VERIFICATION` results.
- `research/data/slide_coverage_expanded.json` — one record for every expanded physical slide page, with gap/duplicate checks.
- `research/data/route_validation.json` — generated-site internal `href`/`src` crawl.
- `research/WEB_RENDERER_STRESS_TEST.md` — temporary realistic-fixture build and HTML structure test.
- `research/GATE_NEGATIVE_TESTS.md` — injected defects that must produce non-zero validator exits.

## Milestone

Current implementation is ready for Chapters 2–9 and Labs 2–6 only when this report is **PASS** and the report’s open-blocker/open-major count is zero. This gate does not author those materials.
"""
    REPORT.write_text(report, encoding="utf-8")
    print(f"FOUNDATION GATE: {'PASS' if passed else 'FAIL'}")
    return passed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

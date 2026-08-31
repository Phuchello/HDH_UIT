#!/usr/bin/env python3
"""Regression checks for the Batch 1 worked scheduling example."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "research" / "data" / "batch1_numeric_checks.json"
CH4 = ROOT / "content" / "theory" / "ch04-scheduling.md"
MIDTERM = ROOT / "content" / "reviews" / "midterm.md"


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))["srtf_example"]
    rows = fixture["processes"]
    waiting = [row["waiting"] for row in rows.values()]
    turnaround = [row["turnaround"] for row in rows.values()]
    assert sum(waiting) / len(waiting) == fixture["waiting_average"]
    assert sum(turnaround) / len(turnaround) == fixture["turnaround_average"]
    text = CH4.read_text(encoding="utf-8") + "\n" + MIDTERM.read_text(encoding="utf-8")
    assert "WTavg = 3.00" in text
    assert "TATavg = 7.00" in text
    assert not re.search(r"WTavg\s*=\s*3\.25", text)
    for segment in fixture["gantt"]:
        assert segment in text, segment
    print("BATCH 1 NUMERIC REGRESSION: PASS (SRTF WTavg=3.00, TATavg=7.00)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"BATCH 1 NUMERIC REGRESSION: FAIL ({exc})", file=sys.stderr)
        raise SystemExit(1)

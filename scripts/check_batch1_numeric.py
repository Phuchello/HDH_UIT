#!/usr/bin/env python3
"""Regression checks for every explicit Batch 1 scheduling example."""

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
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def check_process_fixture(name: str) -> None:
        fixture = data[name]
        rows = fixture["processes"]
        for process, row in rows.items():
            assert row["turnaround"] == row["completion"] - row["arrival"], (name, process, "TAT")
            assert row["waiting"] == row["turnaround"] - row["burst"], (name, process, "WT")
            if "response" in row:
                assert 0 <= row["response"] <= row["waiting"], (name, process, "RT")
        for segment in fixture["gantt"]:
            assert segment in text, (name, segment)

    text = CH4.read_text(encoding="utf-8") + "\n" + MIDTERM.read_text(encoding="utf-8")
    check_process_fixture("srtf_example")
    srtf = data["srtf_example"]
    rows = srtf["processes"]
    waiting = [row["waiting"] for row in rows.values()]
    turnaround = [row["turnaround"] for row in rows.values()]
    assert sum(waiting) / len(waiting) == srtf["waiting_average"]
    assert sum(turnaround) / len(turnaround) == srtf["turnaround_average"]
    check_process_fixture("fcfs_example")
    check_process_fixture("sjf_example")
    rr = data["rr_example"]
    assert rr["quantum"] == 2
    check_process_fixture("rr_example")
    hrrn = data["hrrn_example"]
    assert hrrn["ratios"]["A"] == (4 + 4) / 4
    assert hrrn["ratios"]["B"] == (1 + 2) / 2
    assert hrrn["selected"] == "A"
    assert "WTavg = 3.00" in text
    assert "TATavg = 7.00" in text
    assert not re.search(r"WTavg\s*=\s*3\.25", text)
    assert "RR = (WT + BT) / BT = 1 + WT/BT" in text
    print("BATCH 1 NUMERIC REGRESSION: PASS (FCFS/SJF/SRTF/RR/HRRN)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"BATCH 1 NUMERIC REGRESSION: FAIL ({exc})", file=sys.stderr)
        raise SystemExit(1)

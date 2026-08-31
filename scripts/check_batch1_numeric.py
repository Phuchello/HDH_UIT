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

    def metrics(base: dict, completion: dict, first_start: dict) -> dict:
        result = {}
        for name, row in base.items():
            tat = completion[name] - row["arrival"]
            result[name] = {
                "completion": completion[name],
                "turnaround": tat,
                "waiting": tat - row["burst"],
                "response": first_start[name] - row["arrival"],
            }
        return result

    def simulate_fcfs(base: dict) -> tuple[list[str], dict]:
        time = 0
        completion, first = {}, {}
        gantt = []
        for name, row in sorted(base.items(), key=lambda item: (item[1]["arrival"], item[0])):
            time = max(time, row["arrival"])
            start = time
            first[name] = start
            time += row["burst"]
            completion[name] = time
            gantt.append(f"{name} {start}–{time}")
        return gantt, metrics(base, completion, first)

    def simulate_srtf(base: dict) -> tuple[list[str], dict]:
        remaining = {name: row["burst"] for name, row in base.items()}
        completion, first = {}, {}
        time = min(row["arrival"] for row in base.values())
        gantt = []
        while len(completion) < len(base):
            available = [name for name, row in base.items() if row["arrival"] <= time and remaining[name] > 0]
            if not available:
                time = min(row["arrival"] for name, row in base.items() if remaining[name] > 0 and row["arrival"] > time)
                continue
            name = min(available, key=lambda item: (remaining[item], base[item]["arrival"], item))
            start = time
            first.setdefault(name, start)
            next_arrivals = [row["arrival"] for row in base.values() if row["arrival"] > time and row["arrival"] < time + remaining[name]]
            end = min([time + remaining[name], *next_arrivals])
            remaining[name] -= end - time
            time = end
            if remaining[name] == 0:
                completion[name] = time
            segment = f"{name} {start}–{time}"
            if gantt and gantt[-1].split()[0] == name and gantt[-1].split("–")[-1] == str(start):
                gantt[-1] = f"{name} {gantt[-1].split()[1].split('–')[0]}–{time}"
            else:
                gantt.append(segment)
        return gantt, metrics(base, completion, first)

    def simulate_rr(base: dict, quantum: int) -> tuple[list[str], dict]:
        from collections import deque

        remaining = {name: row["burst"] for name, row in base.items()}
        completion, first = {}, {}
        arrivals = sorted(base, key=lambda name: (base[name]["arrival"], name))
        queue = deque()
        time = 0
        next_index = 0
        gantt = []

        def enqueue_arrivals() -> None:
            nonlocal next_index
            while next_index < len(arrivals) and base[arrivals[next_index]]["arrival"] <= time:
                queue.append(arrivals[next_index])
                next_index += 1

        while len(completion) < len(base):
            enqueue_arrivals()
            if not queue:
                time = base[arrivals[next_index]]["arrival"]
                enqueue_arrivals()
            name = queue.popleft()
            first.setdefault(name, time)
            start = time
            run = min(quantum, remaining[name])
            time += run
            remaining[name] -= run
            gantt.append(f"{name} {start}–{time}")
            enqueue_arrivals()
            if remaining[name] > 0:
                queue.append(name)
            else:
                completion[name] = time
        return gantt, metrics(base, completion, first)

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

    slide15 = data["midterm_slide15"]
    base = {
        name: {"arrival": row["arrival"], "burst": row["burst"]}
        for name, row in slide15["processes"].items()
    }
    expected_algorithms = {
        "fcfs": simulate_fcfs(base),
        "srtf": simulate_srtf(base),
        "rr": simulate_rr(base, slide15["rr"]["quantum"]),
    }
    for algorithm, (gantt, rows) in expected_algorithms.items():
        expected = slide15[algorithm]
        assert gantt == expected["gantt"], ("midterm_slide15", algorithm, "Gantt", gantt, expected["gantt"])
        for name, row in rows.items():
            assert row["completion"] == expected["completion"][name], ("midterm_slide15", algorithm, name, "CT")
            assert row["turnaround"] == expected["turnaround"][name], ("midterm_slide15", algorithm, name, "TAT")
            assert row["waiting"] == expected["waiting"][name], ("midterm_slide15", algorithm, name, "WT")
            assert row["response"] == expected["response"][name], ("midterm_slide15", algorithm, name, "RT")
        assert sum(row["waiting"] for row in rows.values()) / len(rows) == expected["waiting_average"]
        assert sum(row["response"] for row in rows.values()) / len(rows) == expected["response_average"]
        assert sum(row["turnaround"] for row in rows.values()) / len(rows) == expected["turnaround_average"]
        for segment in gantt:
            assert segment in text, ("midterm_slide15", algorithm, segment)

    counts = data["slide11_process_counts"]
    assert counts == {"forks": 4, "final_processes": 16, "new_children": 15, "printf_executions": 30, "per_iteration": [2, 4, 8, 16]}
    assert "for (i = 0; i < 4; i++)" in text and 'printf("hello\\n");' in text
    assert "FINAL_PROCESS_COUNT = 16" in text and "NEW_CHILDREN_CREATED = 15" in text and "TOTAL_PRINTF_EXECUTIONS = 2 + 4 + 8 + 16 = 30" in text
    assert "int main(int argc, char** argv)" in text and "for (int i = 1; i < 5; i++)" in text
    print("BATCH 1 NUMERIC REGRESSION: PASS (FCFS/SJF/SRTF/RR/HRRN)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"BATCH 1 NUMERIC REGRESSION: FAIL ({exc})", file=sys.stderr)
        raise SystemExit(1)

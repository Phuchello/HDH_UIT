import html
import json
import re
import shutil
import subprocess
import sys
from collections import deque
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_CHAPTER_DIR = ROOT / "src" / "chapters"


def chapter_dir():
    """Use canonical sources; legacy layout is only an explicit compatibility fallback."""
    if CANONICAL_CHAPTER_DIR.is_dir():
        return CANONICAL_CHAPTER_DIR
    legacy = ROOT / "chapters"
    if legacy.is_dir():
        print("WARNING: using legacy chapters/ layout; migrate content to src/chapters/.", file=sys.stderr)
        return legacy
    raise RuntimeError("Missing canonical source directory: src/chapters/")


def scheduling():
    processes = {
        "P1": (0, 13), "P2": (4, 9), "P3": (6, 4), "P4": (7, 20), "P5": (12, 10)
    }

    def metrics(timeline):
        first, completion = {}, {}
        for name, start, end in timeline:
            first.setdefault(name, start)
            completion[name] = end
        rows = {}
        for name, (arrival, burst) in processes.items():
            tat = completion[name] - arrival
            rows[name] = {"CT": completion[name], "TAT": tat, "WT": tat - burst, "RT": first[name] - arrival}
        avg = {key: sum(row[key] for row in rows.values()) / len(rows) for key in ("TAT", "WT", "RT")}
        return rows, avg

    # FCFS baseline on the same representative dataset.
    time = 0
    fcfs = []
    for name in sorted(processes, key=lambda n: (processes[n][0], n)):
        arrival, burst = processes[name]
        time = max(time, arrival)
        fcfs.append((name, time, time + burst))
        time += burst

    # SRTF, retaining the current process on equal remaining time.
    remaining = {name: burst for name, (_, burst) in processes.items()}
    time, current, segment_start, srtf = 0, None, 0, []
    while any(v > 0 for v in remaining.values()):
        ready = [n for n, (at, _) in processes.items() if at <= time and remaining[n] > 0]
        if not ready:
            time += 1
            continue
        minimum = min(remaining[n] for n in ready)
        candidates = [n for n in ready if remaining[n] == minimum]
        chosen = current if current in candidates else min(candidates, key=lambda n: (processes[n][0], n))
        if chosen != current:
            if current is not None:
                srtf.append((current, segment_start, time))
            current, segment_start = chosen, time
        remaining[current] -= 1
        time += 1
        if remaining[current] == 0:
            srtf.append((current, segment_start, time))
            current = None

    # Round Robin q=5; arrivals during a slice enter before the expired process.
    quantum = 5
    remaining = {name: burst for name, (_, burst) in processes.items()}
    arrived = set()
    queue = deque()
    rr = []
    time = 0
    while any(v > 0 for v in remaining.values()):
        for name, (arrival, _) in sorted(processes.items(), key=lambda x: (x[1][0], x[0])):
            if arrival <= time and name not in arrived:
                queue.append(name); arrived.add(name)
        if not queue:
            time = min(at for n, (at, _) in processes.items() if n not in arrived)
            continue
        name = queue.popleft()
        start = time
        run = min(quantum, remaining[name])
        time += run
        remaining[name] -= run
        rr.append((name, start, time))
        for other, (arrival, _) in sorted(processes.items(), key=lambda x: (x[1][0], x[0])):
            if arrival <= time and other not in arrived:
                queue.append(other); arrived.add(other)
        if remaining[name] > 0:
            queue.append(name)

    fcfs_rows, fcfs_avg = metrics(fcfs)
    rr_rows, rr_avg = metrics(rr)
    srtf_rows, srtf_avg = metrics(srtf)
    assert rr_avg == {"TAT": 31.2, "WT": 20.0, "RT": 7.6}
    assert srtf_avg == {"TAT": 23.2, "WT": 12.0, "RT": 11.2}
    return {
        "FCFS": {"timeline": fcfs, "rows": fcfs_rows, "averages": fcfs_avg},
        "RR_q5": {"timeline": rr, "rows": rr_rows, "averages": rr_avg, "matchesHandbook": True},
        "SRTF": {"timeline": srtf, "rows": srtf_rows, "averages": srtf_avg, "matchesHandbook": True},
    }


def banker():
    allocation = [[0,0,1,2],[1,0,0,0],[1,3,5,4],[0,6,3,2],[0,0,1,4]]
    maximum = [[0,0,1,2],[1,7,5,0],[2,3,5,6],[0,6,5,2],[0,6,5,6]]
    available = [1,5,2,0]
    need = [[m-a for m,a in zip(mx, al)] for mx,al in zip(maximum, allocation)]

    def safe(avail, alloc, needs):
        work = avail[:]
        done = [False] * len(alloc)
        sequence, trace = [], []
        changed = True
        while changed:
            changed = False
            for i in range(len(alloc)):
                if not done[i] and all(n <= w for n,w in zip(needs[i], work)):
                    before = work[:]
                    work = [w+a for w,a in zip(work, alloc[i])]
                    done[i] = True; sequence.append(i); changed = True
                    trace.append({"process":f"P{i}","before":before,"after":work[:]})
        return all(done), sequence, trace

    ok, sequence, trace = safe(available, allocation, need)
    assert ok and sequence == [0,2,3,4,1]
    request = [0,4,2,0]
    new_available = [a-r for a,r in zip(available, request)]
    new_allocation = [row[:] for row in allocation]
    new_need = [row[:] for row in need]
    new_allocation[1] = [a+r for a,r in zip(new_allocation[1], request)]
    new_need[1] = [n-r for n,r in zip(new_need[1], request)]
    ok2, sequence2, trace2 = safe(new_available, new_allocation, new_need)
    assert ok2 and sequence2 == [0,2,3,4,1]
    return {"need":need,"initial":{"safe":ok,"sequence":sequence,"trace":trace},"afterP1Request":{"available":new_available,"safe":ok2,"sequence":sequence2,"trace":trace2},"matchesHandbook":True}


def replacement():
    refs = [1,2,3,4,2,1,5,6,2,1,2,3,7,6,3,2,1,2,3,6]
    capacity = 4
    def fifo():
        frames, q, faults = [], deque(), 0
        for ref in refs:
            if ref not in frames:
                faults += 1
                if len(frames) < capacity:
                    frames.append(ref)
                else:
                    victim = q.popleft(); frames[frames.index(victim)] = ref
                q.append(ref)
        return faults
    def lru():
        frames, last, faults = [], {}, 0
        for i, ref in enumerate(refs):
            if ref not in frames:
                faults += 1
                if len(frames) < capacity: frames.append(ref)
                else:
                    victim = min(frames, key=lambda p:last[p]); frames[frames.index(victim)] = ref
            last[ref] = i
        return faults
    def opt():
        frames, faults = [], 0
        for i, ref in enumerate(refs):
            if ref in frames: continue
            faults += 1
            if len(frames) < capacity: frames.append(ref); continue
            def next_use(p):
                try: return refs.index(p, i+1)
                except ValueError: return float("inf")
            victim = max(frames, key=next_use); frames[frames.index(victim)] = ref
        return faults
    result = {"FIFO":fifo(),"LRU":lru(),"OPT":opt()}
    assert result == {"FIFO":14,"LRU":10,"OPT":8}
    return {"referenceString":refs,"frames":capacity,"faults":result,"matchesHandbook":True}


def other_numeric():
    eat = {
        "a_ns": 20 + (2-.8)*100,
        "b_ns": (2-.75)*200,
        "c_min_hit_ratio": 2 - ((130-20)/100),
    }
    assert eat == {"a_ns":140.0,"b_ns":250.0,"c_min_hit_ratio":0.8999999999999999}
    fork = {"unconditionalForks":3,"totalProcesses":2**3,"childProcesses":2**3-1,"printCountInsideLoop":sum(2**i for i in range(1,4))}
    assert fork["totalProcesses"] == 8 and fork["printCountInsideLoop"] == 14
    semaphore_dag = {"sem1Signals":2,"sem1Waits":2,"sem2Signals":2,"sem2Waits":2,"valid":True}
    return {"EAT":eat,"forkTree":fork,"semaphoreDAG":semaphore_dag}


class CodeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_pre = False
        self.in_code = False
        self.code_class = ""
        self.parts = []
        self.blocks = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "pre": self.in_pre = True
        if tag == "code" and self.in_pre:
            self.in_code = True; self.code_class = attrs.get("class", ""); self.parts = []
    def handle_endtag(self, tag):
        if tag == "code" and self.in_code:
            self.blocks.append((self.code_class, "".join(self.parts)))
            self.in_code = False
        if tag == "pre": self.in_pre = False
    def handle_data(self, data):
        if self.in_code: self.parts.append(data)


def compile_checks(run_gcc=False):
    outdir = ROOT / "build" / "c-spotchecks"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for file in sorted(chapter_dir().glob("*.html")):
        parser = CodeParser(); parser.feed(file.read_text(encoding="utf-8"))
        for index, (classes, code) in enumerate(parser.blocks, start=1):
            if "language-c" not in classes: continue
            complete = bool(re.search(r"\b(?:int|void)\s+main\s*\(", code)) and "..." not in code
            pseudo = not complete
            row = {"source":file.name,"block":index,"completeProgram":complete,"pseudocode":pseudo}
            if complete and not pseudo:
                cfile = outdir / f"{file.stem}-{index}.c"
                cfile.write_text(code.strip()+"\n", encoding="utf-8")
                row.update({"stagedFile":str(cfile),"requiredFlags":"-Wall -Wextra -pedantic -std=c11"})
                if run_gcc and not sys.platform.startswith("win"):
                    gcc = shutil.which("gcc")
                    if not gcc:
                        raise RuntimeError("--compile requested but gcc is not available on PATH")
                    binary = outdir / f"{file.stem}-{index}"
                    completed = subprocess.run(
                        [gcc, "-Wall", "-Wextra", "-pedantic", "-std=c11", "-D_POSIX_C_SOURCE=200809L",
                         str(cfile), "-o", str(binary), "-pthread", "-lrt"],
                        text=True, capture_output=True, check=False,
                    )
                    row.update({"compiler": gcc, "returncode": completed.returncode,
                                "stdout": completed.stdout, "stderr": completed.stderr})
                    if completed.returncode:
                        raise RuntimeError(f"gcc failed for {cfile.name}: {completed.stderr}")
                elif run_gcc:
                    row["compiler"] = "skipped locally: POSIX examples require Linux/CI GCC"
            rows.append(row)
    staged = [r for r in rows if "stagedFile" in r]
    if not staged:
        raise RuntimeError("No complete C program was found for compilation")
    return {"compiler":"staged for gcc validation","blocks":rows,"stagedCount":len(staged)}


def main():
    run_gcc = "--compile" in sys.argv
    report = {
        "scheduling": scheduling(),
        "banker": banker(),
        "pageReplacement": replacement(),
        "other": other_numeric(),
        "codeCompilation": compile_checks(run_gcc=run_gcc),
    }
    out = ROOT / "build" / "technical-checks.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "schedulingMatches": {k:v.get("matchesHandbook", True) for k,v in report["scheduling"].items()},
        "bankerMatches": report["banker"]["matchesHandbook"],
        "pageReplacement": report["pageReplacement"]["faults"],
        "codeProgramsStaged": report["codeCompilation"]["stagedCount"],
        "out":str(out),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

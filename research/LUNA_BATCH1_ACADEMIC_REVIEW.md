# Luna Ultra — Batch 1 Independent Academic and Source Review

**Review date:** 2026-08-31
**Scope:** Chương 1–4, Midterm Review, dedicated subjective banks, official-question accounting, canonical source maps, and Batch 1 numerical examples only.
**Out of scope:** Chương 5, web/renderer redesign, engineering architecture, and merge to `main`.

## Review result

**PASS — Batch 1 academic/source fidelity verified.**

| Severity | Open | Resolved in this pass |
|---|---:|---:|
| BLOCKER | 0 | 0 |
| MAJOR | 0 | 2 |
| MINOR | 0 | 4 |

The review used the repository’s immutable source registry and previously recorded Tier-A attachment hashes/page maps.  The canonical source binaries were not mounted for a second binary read in this turn; this report therefore does not make a new binary-verification claim.  Existing `USER_ATTACHMENT_VERIFIED` statuses are preserved.

## Findings and disposition

| ID | Severity | File / source | Claim or issue | Evidence and correction | Final status |
|---|---|---|---|---|---|
| ACAD-001 | MINOR | `content/questions/subjective/ch04.md`; `UIT-SLIDE-CH04-1/2-2024` | Several Ch4 subjective locators used stale page ranges. | Replaced with criteria 19–22, SJF/SRTF 34–47, Priority 48–52, RR 53–63, and MLFQ 10–13. | RESOLVED |
| ACAD-002 | MINOR | `research/data/slide_coverage.yaml`, answer map | Some destinations used transliterations different from the renderer’s deterministic Unicode slugification. | Updated destinations and regenerated `slide_coverage_expanded.json`; all reviewed anchors now exist in rendered Markdown routes. | RESOLVED |
| ACAD-003 | MINOR | `content/theory/ch03-process.md`; `POSIX-EXEC` | `exec*()` wording was qualified as “usually” retaining PID. | Tightened to: successful `exec*()` replaces the image in the same process, creates no PID, and keeps that process’s PID. | RESOLVED |
| ACAD-004 | MINOR | `research/data/batch1_numeric_checks.json`, `scripts/check_batch1_numeric.py` | Regression coverage did not machine-check every explicit Ch4 worked example. | Added independently recomputed FCFS, SJF, SRTF, RR and HRRN fixtures, including CT/TAT/WT/RT identities and Gantt fragments. | RESOLVED |

## Canonical source and framing checks

- Chương 4 Part 1 is `UIT-SLIDE-CH04-1-2024`, `#Week04-Chapter4-1 2024.pdf`, 74 pages, with the recorded SHA-256 and `USER_ATTACHMENT_VERIFIED` status.
- Chương 4 Part 2 is `UIT-SLIDE-CH04-2-2024`, `#Week05-Chapter4-2 2024.pdf`, 59 pages, with the recorded SHA-256 and `USER_ATTACHMENT_VERIFIED` status.
- No unsupported official `UIT-SLIDE-CH04-3-2024` record or coverage mapping remains.  The local 46-page variant has its own `source_variant` identity.
- Chương 2 preserves the official slide’s seven core components.  The qbank wording “8 thành phần” remains verbatim and is explicitly labelled `SOURCE CONFLICT`; networking/distributed and security enrichment is labelled Tier B rather than presented as an official eight/nine-item slide list.
- Midterm Review format and wording are explicitly scoped to the canonical 2024 review slides.  No all-semesters claim is made; Solaris is explicitly excluded as a Midterm prompt.
- `research/data/official_review_questions.yaml` distinguishes 60 dedicated qbank records, 33 concrete Midterm occurrences, 2 external exercise-set references, and 64 canonical deduplicated questions.
- `research/data/midterm_answer_mapping.yaml` contains one auditable mapping for each of the 33 concrete occurrences and both external references.  Every record has `question_id`, exact `source_locator`, `canonical_answer_destination`, and an allowed `answer_status`; all concrete records are `ANSWER_VERIFIED`.  The Slide 15 q=10 occurrence maps to the dedicated canonical P1–P5 source dataset and its checked FCFS/SRTF/RR solutions.

## Chapter coverage audit

| Source | Physical pages/slides | Content pages/slides | Reviewed status |
|---|---:|---:|---|
| `UIT-SLIDE-CH01-2024` | 57 | 53 | CONTENT_VERIFIED |
| `UIT-SLIDE-CH02-2024` | 57 | 53 | CONTENT_VERIFIED |
| `UIT-SLIDE-CH03-2024` | 64 | 60 | CONTENT_VERIFIED |
| `UIT-SLIDE-CH04-1-2024` | 74 | 70 | CONTENT_VERIFIED |
| `UIT-SLIDE-CH04-2-2024` | 59 | 56 | CONTENT_VERIFIED |
| `UIT-SLIDE-MIDTERM-REVIEW-2024` | 17 | 15 | CONTENT_VERIFIED |

All declared physical ranges remain gap-free and non-overlapping.  Future Ch5 attachments remain registered but unmapped.

## Academic spot checks

- **Ch1:** OS user/system views, bootstrap, interrupt versus trap/exception, IVT/ISR, storage/caching/locality, processor/core/SMP/AMP/cluster, dual mode and timer, and real-time environment distinctions are scoped and source-qualified.
- **Ch2:** component/service/system-program boundaries, API versus system call, parameter-passing mechanisms, and architecture trade-offs are distinguished; Tier-B enrichment is labelled.
- **Ch3:** process/program and memory layout, five-state lifecycle, PCB, scheduler/context switch, `fork`/`exec`/`wait`/`exit`, zombie/orphan scope, IPC, and POSIX thread mappings are technically consistent.
- **Ch4:** CPU/I/O bursts, scheduler layers, dispatch latency, six slide metrics versus five-item qbank wording, all named algorithms, MLQ/MLFQ, multiprocessor policies, real-time terminology, and implementation caveats are source-scoped.
- **Rubrics:** every subjective rubric is labelled `SELF_CHECK_RUBRIC` and explicitly disclaims official grading authority.
- **Exam claims:** no unsupported “always asked”, guaranteed, official barem, or all-semester claim remains in the reviewed Batch 1 material.

## Numerical verification

`python scripts/check_batch1_numeric.py` independently recomputes every explicit Ch4 fixture:

- FCFS: `P1 0–5 | P2 5–7 | P3 7–8`, WT `0,4,5`.
- SJF: `P1 0–7 | P3 7–8 | P2 8–12`, with CT/TAT/WT identities checked.
- SRTF: `P1 0–2 | P2 2–4 | P3 4–5 | P2 5–7 | P4 7–11 | P1 11–16`, WT `9,1,0,2`, `WTavg = 3.00`, `TATavg = 7.00`.
- RR: `P1 0–2 | P2 2–4 | P3 4–5 | P1 5–7 | P2 7–8 | P1 8–9`, `q=2`.
- HRRN: `A=2.0`, `B=1.5`, so A is selected under the stated rule.

No contradictory Batch 1 numerical value was found after these checks.

## Validation record

- `npm test`: PASS (`FOUNDATION GATE: PASS`)
- `python scripts/validate_batch1_canonical.py`: PASS
- `python scripts/check_batch1_numeric.py`: PASS
- `python scripts/validate.py`: PASS (6/6; 57/57 searchable A4 PDF pages)
- `python scripts/validate_final.py`: PASS (0 iframes, 0 remote dependencies, 0 missing assets, 0 broken anchors, 0 placeholder matches, 57 A4 pages)
- `python scripts/technical_checks.py --compile`: PASS locally (7 complete C programs staged; Windows skips POSIX GCC execution, while CI performs the GCC compile step).

## Closeout decision

**OPEN ACADEMIC BLOCKERS: 0**
**OPEN MAJORS: 0**
**OPEN MINORS: 0**
**Batch 1 status:** `CONTENT_VERIFIED`
**Next permitted action:** Terra Medium performs Batch 1 engineering closeout.

## POST-REVIEW SOURCE CORRECTION

The first review above accepted normalized Midterm topics without reopening the canonical binary. A subsequent direct inspection of `#Week08-Midterm Review.pptx` found semantic drift in the Slide 5/7/9 wording and in the Slide 10, 11, and 15 compound exercises. That prior academic PASS was therefore reopened for a source-fidelity repair; no history was erased.

The correction preserves the 33 concrete occurrence count and adds exact `source_question` fields for all 33 occurrences plus the two external references. Slide 10 now reproduces `test.c` and limits the lifecycle conclusion to `New → Ready → Running → Terminated`, with preemption/I/O caveats. Slide 11 now reproduces the four-fork program and verifies 16 final processes, 15 new children, and 30 `printf` executions with the stdout-buffering caveat. Slide 15 now records the canonical P1–P5 dataset and independently checked FCFS, SRTF, and RR (`q=10`) CT/TAT/WT/RT tables and averages; the older WTavg 3.00 fixture is explicitly additional practice.

| ID | Severity | Finding | Resolution | Final status |
|---|---|---|---|---|
| ACAD-005 | MAJOR | Midterm normalized topics and compound answers had drifted from the canonical Slide 5/7/9/10/11/15 source semantics. | Restored source-faithful wording, source identity, dedicated answers, exact answer destinations, and regression gates in `validate_batch1_canonical.py` and `check_batch1_numeric.py`. | RESOLVED |
| ACAD-006 | MAJOR | `source_question` remained normalized for Slides 10/11/14/15, and Slide 11 lacked the requested literal parent–child tree. | Restored verbatim canonical prompts, separated Slide 15 `source_data`, added the explicit P0–P15 logical tree, and added validator gates for verbatim provenance and tree topology. | RESOLVED |

After this correction, Midterm content status is restored to `CONTENT_VERIFIED`; the academic verification remains **PASS — BATCH 1 ONLY** pending engineering closeout. Chapter 5 remains out of scope.

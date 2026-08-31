# LUNA THEORY BATCH 1 CONTENT REPORT — CANONICAL SOURCE MAP FINAL REPAIR

**Scope:** Chapters 1–4, Midterm Review, subjective banks, and source/numerical regression  
**Status:** `CONTENT_VERIFIED — ACADEMIC REVIEW PASS (BATCH 1 ONLY)`
**Date:** 2026-08-31

## Canonical source evidence

Canonical attachment fingerprints are recorded in `content/sources/registry.yaml` with status `USER_ATTACHMENT_VERIFIED`. A workspace-local file is never silently substituted for a canonical identity; every distinct binary has its own immutable source ID.

| Source | Canonical evidence |
|---|---|
| Ch4 Part 1 | `#Week04-Chapter4-1 2024.pdf`; SHA256 `f2323c438f260d0b5c37322e78eb0eee7af3e036bec109d68de9db31c4714dae`; **74 physical / 70 content / 4 non-content** |
| Ch4 Part 2 | `#Week05-Chapter4-2 2024.pdf`; SHA256 `9221a7e4a42ff88a98ee8f2980d879860ded2abd5e6de04ca35d7f768aee2040`; **59 physical / 56 content / 3 non-content** |
| Midterm Review | `#Week08-Midterm Review.pptx`; SHA256 `cd3da900b5f8c0d4481afae68d4e4e33c6348867118d8f35966eac6203572326`; **17 slides** |

The former 56/34/46-page Chapter 4 files and 16-page Midterm PDF remain explicit local variants. The former Week06 Chapter 4 Part 3 identity is not an official source identity and is excluded from coverage.

## Verified page maps

`research/data/slide_coverage.yaml` records the authoritative ranges without gaps or overlaps. Ch4 Part 1 maps pages 4–63 to teaching sections, 64 summary, 65 review questions, 66–73 exercises, and page 74 as non-content. Ch4 Part 2 maps HRRN (3–4), MLQ (5–9), MLFQ (10–13), comparison (14–15), threads (16–17), multiprocessor (18–28), real-time (29–37), Linux (38–44), Windows (45–51), Solaris read-more (52–56), summary/review (57–58), and page 59 as non-content.

## Official question accounting

- Dedicated official qbank records: **60 total**; Batch 1 Chapters 1–4: **31** (`QBANK_OFFICIAL`).
- Canonical Midterm Review: **33 concrete source-question occurrences** (`MIDTERM_REVIEW_OFFICIAL`) under the documented bullet/compound counting convention: slide 5 = 9, slide 7 = 5, slide 9 = 6, slide 10 = 1 compound, slide 11 = 1 compound, slide 14 = 10, slide 15 = 1 compound.
- Slides 12 and 16 contribute **2 `REFERENCE_TO_EXTERNAL_EXERCISE_SET`** records and no invented questions.
- Canonical deduplicated answer slots: **64**, with source locators retained for every occurrence.
- Fake Solaris Midterm prompts: **0**. Solaris remains only as Chapter 4 Part 2 read-more content.

## Source conflicts and theory fidelity

- Chapter 2 qbank wording “8 thành phần” is preserved verbatim; the canonical slide’s seven core components are taught as the answer, with Tier-B extensions clearly separated.
- Chapter 4 qbank wording “5 tiêu chuẩn” is preserved; canonical theory covers all six slide criteria, including fairness, and marks the conflict explicitly. Fairness is qualitative in calculation exercises.
- Ch4 theory includes burst/service time, CPU-bound/I/O-bound behavior, all scheduler levels and invocation events, dispatcher/dispatch latency, selection function/decision mode, burst prediction/exponential averaging, RR `(n−1)q` bound under stated assumptions, HRRN, comparison, thread/AMP/SMP/affinity/load balancing, periodic/aperiodic/sporadic real-time tasks, RMS/EDF/TBS, Linux CFS, Windows, and Solaris at source READ_MORE depth.

## Numerical regression

`scripts/check_batch1_numeric.py` passes the SRTF fixture: WT = 9,1,0,2 ⇒ **WTavg = 3.00**; TAT = 16,5,1,6 ⇒ **TATavg = 7.00**. No stale `3.25` remains in active Batch 1 theory/review content.

## Future Batch 2 source blocker

Canonical Ch5 attachments are recorded as separate, unmapped evidence IDs: `#Week06-Chapter5-1 2024.pdf` (67 pages, SHA256 `2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416`) and `#Week07-Chapter5-2 2024.pdf` (72 pages, SHA256 `f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2`). Do not author Chapter 5 or mix these with local variants until the same source-fidelity split/map is performed.

## Acceptance

- `scripts/validate_batch1_canonical.py`: PASS
- `scripts/verify_research_gates.py`: PASS
- `scripts/check_batch1_numeric.py`: PASS
- `npm test`: PASS
- **Current Phase:** `V2_THEORY_BATCH1_ACADEMIC_REVIEW_PASS_PENDING_CLOSEOUT`
- **Academic Verification:** `PASS — BATCH 1 ONLY`
- **Exact Next Action:** Terra Medium performs Batch 1 closeout: clean-build stale-output guard, true nested-list renderer semantics, then canonical Chapter 5 source-map preparation.

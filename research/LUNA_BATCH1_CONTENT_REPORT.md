# LUNA THEORY BATCH 1 CONTENT REPORT — SOURCE-FIDELITY HOTFIX

**Scope:** Chapters 1–4, Midterm Review, subjective banks, and source/number regression
**Status:** `CONTENT_DRAFTED` but **not ready for engineering QA** until the canonical 74/59 PDFs are available locally
**Date:** 2026-08-31

## Canonical source binaries and variants

The hotfix brief identifies the canonical user-provided binaries below. They are not present in this workspace, so their hashes/page counts are recorded as declarations, not local verification. The Downloads corpus contains a different, hash-verified variant; it is explicitly separated in `content/sources/registry.yaml`.

| Source | Canonical user-provided evidence | Local status |
|---|---|---|
| Week04-Chapter4-1 2024.pdf | 74 pages; `f2323c438f260d0b5c37322e78eb0eee7af3e036bec109d68de9db31c4714dae` | **NOT PRESENT**; local variant is 56 pages, ID `UIT-SLIDE-CH04-1-2024-VARIANT-LOCAL-56` |
| Week05-Chapter4-2 2024.pdf | 59 pages; `9221a7e4a42ff88a98ee8f2980d879860ded2abd5e6de04ca35d7f768aee2040` | **NOT PRESENT**; local variant is 34 pages, ID `UIT-SLIDE-CH04-2-2024-VARIANT-LOCAL-34` |
| Week06-Chapter4-3 2024.pdf | No canonical counterpart identified | Local 46-page file is `UIT-SLIDE-CH04-3-2024-VARIANT-LOCAL-46`, excluded from official coverage |

The user-provided Week06-Chapter5-1 (67 pages) and Week07-Chapter5-2 (72 pages) were also not found locally; Chapters 5+ remain out of scope and are not silently substituted.

## Page-level coverage (canonical declared ranges)

| Deck | Physical | Non-content | Content mapped | Destination |
|---|---:|---:|---:|---|
| Ch1 | 57 | 4 | 53 | `content/theory/ch01-overview.md` + `ch01` bank |
| Ch2 | 57 | 4 | 53 | `content/theory/ch02-structure.md` + `ch02` bank |
| Ch3 | 64 | 4 | 60 | `content/theory/ch03-process.md` + `ch03` bank |
| Ch4 Part 1 (canonical declared) | 74 | 3 | 71 | `content/theory/ch04-scheduling.md` |
| Ch4 Part 2 (canonical declared) | 59 | 2 | 57 | `content/theory/ch04-scheduling.md` |
| Midterm Review | 16 | 2 | 14 | `content/reviews/midterm.md` |

All physical pages in the manifest are classified `CONTENT` or `NON_CONTENT`; no separate Ch4 Part 3 is counted.

## Official question coverage

- Dedicated qbank records covered: **31/31** for Chapters 1–4 (`QBANK_OFFICIAL`).
- Midterm Review prompts recorded: **16/16** (`MIDTERM_REVIEW_OFFICIAL`), including scheduler purpose/types, overhead, criteria, algorithm characteristics/trade-offs, multiprocessor/load balancing, real-time, Linux CFS, Windows and Solaris.
- Source-question occurrences: **47** (31 qbank + 16 Midterm Review records).
- Unique canonical answer slots after explicit equivalence review: **41**; equivalent prompts retain separate source locators.
- Unsupported official rubric claims: **0**.
- Unsupported exam universals: **0**; the 2024 format is labelled source-specific historical information.

### Chapter 2 source-count conflict

The UIT Chapter 2 slide is represented as **seven core components**: process, main memory, files, I/O, secondary storage, protection, and command interpreter. The official qbank title says “8 thành phần”; that source conflict is preserved in the manifest and subjective bank. Networking/distributed and a separate security distinction are labelled Tier-B textbook extensions, not attributed to the UIT slide.

## Midterm format evidence

`content/reviews/midterm.md` now records slide 2’s source-specific format: subjective 4 points (1.5 short answer/process creation across 3 questions; 2.5 CPU scheduling across 2 questions) and MCQ 6 points (12 × 0.5). It is explicitly not a guarantee for every semester.

## Worked-example arithmetic

`research/data/batch1_numeric_checks.json` and `scripts/check_batch1_numeric.py` assert the SRTF example independently: WT values 9, 1, 0, 2 ⇒ `WTavg = 3.00`; TAT values 16, 5, 1, 6 ⇒ `TATavg = 7.00`; the previously reported incorrect average literal is rejected. The check is wired into `.github/workflows/validate.yml`.

## Open findings and status

- **OPEN_CONTENT_BLOCKERS:** 1 — canonical user-provided Chapter 4 Part 1/2 binaries are unavailable locally for hash/page verification and exact slide-level topic inspection.
- **OPEN_CONTENT_MAJORS:** 1 — Chapter 4 coverage is declared against the supplied canonical page counts but cannot yet be independently content-checked against those binaries.
- **Ready for engineering QA:** `NO`.
- **Next action:** obtain/mount the canonical source corpus, verify hashes/pages, then rerun the source-fidelity and coverage checks. Do not start Chapter 5.

# TERRA BATCH 1 ENGINEERING QA — HDH_UIT V2

**Scope:** Engineering/build/web/CI regression only for Chapters 1–4, Midterm Review, and subjective banks.
**Baseline remote commit tested:** `7205b0fad59238f3e859f74fd2b4417a7a184eaa`
**Date:** 2026-08-31
**Academic verification:** `NOT_YET_PERFORMED`

## Outcome

**ENGINEERING QA: PASS.** No Batch 1 academic prose was rewritten, no Chapter 5 work was started, and no main-branch merge was performed.

## Clean build and determinism

- Clean dependency install: `npm ci` completed with **0 vulnerabilities**.
- Generated companion build: `npm run web:build` completed successfully.
- Two consecutive builds produced identical SHA-256 manifests for **124** files: `TREE_MATCH=YES`.
- The generated companion has **14** HTML pages.

## Validation and CI parity

- `npm test`: **PASS** — sources, public hygiene, V2 content, build, routes, renderer stress, negative tests, Batch 1 canonical source gate, and research gates.
- CI-equivalent sequence: **PASS** — foundation gate, canonical source validation, Batch 1 numeric regression, publication validation, final publication validation, and `technical_checks.py --compile`.
- Technical spot checks: FCFS/RR/SRTF, Banker, FIFO/LRU/OPT, and **7** staged C programs all passed.
- Negative tests: **PASS (11/11)**. Failure evidence is now sanitized to portable `<REPO_ROOT>`/`<LOCAL_PATH>` tokens.

## Generated-site regression checks

`research/data/route_validation.json` records:

| Check | Result |
|---|:---:|
| Broken routes | 0 |
| Broken anchors | 0 |
| Broken assets | 0 |
| Invalid empty `href="#"` | 0 |
| Remote runtime dependencies | 0 |
| Internal references crawled | 382 |

The search index and local knowledge graph are generated from the same document manifest. Browser exercise confirmed a query for `SRTF` returns the Chapter 4 target. Local graph and backlinks remain generated from canonical `related` metadata.

## Browser and renderer checks

- Desktop Chapter 4 renderer: loading succeeds with no console errors; SRTF, `WTavg = 3.00`, tables, and code blocks are present.
- Interaction checks: navigation, search modal/results, and light/dark theme toggle work without console errors.
- Responsive checks at 390px: Ch1–Ch4, Midterm Review, and subjective Ch1–Ch4 all have **zero root horizontal overflow**.
- Tablet check at 768px: Chapter 4 has zero root overflow and its table remains within the reading canvas.
- Root cause repaired: shared CSS now constrains source tables and code blocks to scroll inside the reading canvas instead of widening the mobile viewport.
- Offline core rendering: all generated runtime CSS, JavaScript, MathJax, routes, and assets resolve locally; publication validation also reports 0 remote dependencies, 0 MathJax errors, and 0 unresolved visible math delimiters.

## Source metadata consistency

The unambiguous Ch4 metadata mismatch was normalized: both 74-page Part 1 and 59-page Part 2 canonical records now use `USER_ATTACHMENT_VERIFIED`, matching their immutable supplied-attachment fingerprints and the Batch 1 content report. The canonical validator now prevents this status regression. Local 56/34/46-page variants remain separate source identities.

## Public hygiene

- Public hygiene: **PASS**.
- No credentials or private workstation paths detected in reader-facing outputs.
- Validator safety scan now excludes only transient runtime directories (`node_modules`, `__pycache__`, `.pytest_cache`, build output) and continues scanning source and generated reader-facing materials.

## Engineering blockers / majors / minors

- **Blockers:** 0
- **Majors:** 0
- **Minors:** 1 — final publication diagnostics retain five non-failing nested list/solution-step width warnings. `validate_final.py` remains PASS; this is a separate print-layout follow-up, not a Batch 1 web companion regression.

## Academic follow-ups (not performed here)

- Luna Ultra must independently review source fidelity and academic correctness for all Batch 1 prose; this engineering pass makes no academic-verification claim.
- In particular, confirm whether any Chapter 4 subjective-question slide locators/ranges still reflect pre-canonical source mapping, and correct only after source review.

## Next phase

`V2_THEORY_BATCH1_ENGINEERING_QA_PASS_READY_FOR_ACADEMIC_REVIEW`

Exact next action: **Luna Ultra performs independent academic/source review of Batch 1.**

## ENGINEERING HOTFIX / INDEPENDENT REVIEW REMEDIATION

| Area | Result |
|---|:---:|
| PRODUCTION_ASSET_SOURCE | PASS — `src/web/assets/` is the sole active CSS/JS source; build rejects archive references. |
| FULL_TEXT_SEARCH | PASS — canonical Markdown supplies title, summary, headings, and body-derived `searchable_text`; convoy effect, exponential averaging, dispatch latency, zombie, and processor affinity regressions resolve. |
| MIDTERM_NAVIGATION | PASS — visible `ÔN TẬP` sidebar group reaches `reviews/midterm.html` from the homepage. |
| BACKLINKS | IMPLEMENTED — reverse `related`/wikilink references are generated as `LIÊN KẾT TỪ CÁC TRANG KHÁC`. |
| STUDYCARD_PERSISTENCE | PASS — browser mark/reload checks retained remembered and forgotten `data-state` values. |
| SUBJECTIVE_PRACTICE_PERSISTENCE | IMPLEMENTED, NOT INSTANTIATED — draft, checkbox selection, rubric visibility, and self-check score restore code is present, but current Batch 1 content renders zero SubjectivePractice instances; no untested browser-PASS claim is made. |
| READER_UI_HYGIENE | PASS — no reader-facing `CUSTOM_STATIC_GENERATOR`, `Barem Chấm`, or `Barem Điểm`. |
| READER_PAGE_REACHABILITY | PASS — `UNREACHABLE_READER_PAGES=0` for all required reader documents. |

Interactive browser checks also confirmed deep-content search, theme persistence, Midterm navigation, graph canvas presence, backlinks, and mobile rendering without root overflow for Chapters 1–4 and Midterm.

### Hotfix disposition

- **ENGINEERING_BLOCKERS:** 0
- **ENGINEERING_MAJORS:** 0
- **ENGINEERING_MINORS:** 1 — SubjectivePractice is not currently instantiated in Batch 1 content, so its persistence cannot be exercised against a reader page without adding new learning UI/content. The component persistence path is implemented and its status is recorded truthfully above.

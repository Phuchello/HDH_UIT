# Terra Batch 1 Engineering Closeout

**Scope:** Batch 1 build, renderer, generated-site, provenance serialization, and regression engineering only.
**REMOTE HEAD TESTED:** `2516b732c9747b9de2ec053fdb16da4f20343cce`
**Academic verification:** `PASS — BATCH 1 ONLY`
**Engineering verification:** `PASS — BATCH 1 CLOSED`
**Chapter 5:** not authored; `main` not merged.

## Required closeout fields

| Field | Result |
|---|---|
| STALE_OUTPUT_GUARD | PASS — cleanup rejects repository root, protected source directories, symlink output directories, and unsafe parents. |
| SAFE_OUTPUT_CLEANUP | PASS — generated output is cleaned and recreated from canonical content, production assets, and local vendor assets. |
| STALE_ROUTE_REMOVAL | PASS — delete/rebuild fixture removes the deleted HTML route. |
| SEARCH_GHOST_REMOVAL | PASS — deleted document ID is absent from `search_index.json`. |
| GRAPH_GHOST_REMOVAL | PASS — deleted document ID is absent from `graph_data.json`. |
| NESTED_UNORDERED_LIST | PASS — structural tree assertion. |
| NESTED_ORDERED_LIST | PASS — structural tree assertion. |
| MIXED_NESTED_LIST | PASS — structural tree assertion. |
| DEPTH_3_LIST | PASS — three list levels verified. |
| TABLE_REGRESSION | PASS — pipe-containing table fixture survives. |
| CODE_REGRESSION | PASS — fenced C code and 7 complete C programs staged. |
| MATH_REGRESSION | PASS — LaTeX fixture and offline publication math checks pass. |
| UNICODE_REGRESSION | PASS — Vietnamese Unicode fixture and publication checks pass. |
| CALLOUT_REGRESSION | PASS — note callout and StudyCard fixtures survive. |
| MIDTERM_SLIDE15_VERBATIM_SERIALIZATION | PASS — `source_question` uses a YAML literal block scalar with canonical algorithm lines; `source_data` remains separate. Validator normalization is whitespace-only (CRLF, trailing spaces, repeated blank lines); it does not invent punctuation. |
| ROUTES | PASS — 14 generated pages; 0 broken routes. |
| ANCHORS | PASS — 0 broken anchors. |
| ASSETS | PASS — 0 broken assets; local production/vendor assets rebuilt. |
| REACHABILITY | PASS — 0 unreachable required reader pages. |
| OFFLINE | PASS — local runtime assets and MathJax; 0 remote runtime dependencies. |
| PUBLIC_HYGIENE | PASS — repository hygiene gate passes. |
| NPM_TEST | PASS — foundation gate and all Batch 1 gates pass. |
| CI | PASS — GitHub Actions run [33376970284](https://github.com/Phuchello/HDH_UIT/actions/runs/33376970284) passed for closeout commit `ecad5806e1c4f964ac9a1743d96e8bc4b49fba94`. |

## Determinism

Two clean builds from the same canonical input produced identical SHA-256
manifests for all generated files in the temporary fixture (`124` files in the
production build and matching fixture trees). Unexplained differences: `0`.

## Engineering disposition

- **ENGINEERING_BLOCKERS:** 0
- **ENGINEERING_MAJORS:** 0
- **ENGINEERING_MINORS:** 1 — pre-existing non-gating publication diagnostic width warnings and an uninstantiated Batch 1 SubjectivePractice fixture remain documented in the prior engineering QA; no new Batch 1 blocker or major was introduced.

The temporary fixture is deleted after each stress-test run. No source content
was rewritten beyond the mechanical Slide 15 serialization required for
verbatim line preservation.

## Final state

`V2_THEORY_BATCH1_LOCKED_READY_FOR_BATCH2_SOURCE_MAPPING`

Exact next action: **Luna Ultra performs canonical Chapter 5 source-map audit and prepares Theory Batch 2 evidence before any Chapter 5 authoring.**

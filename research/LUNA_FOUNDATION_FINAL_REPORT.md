# Luna Ultra Foundation Final Report

**Audit baseline:** `6dca6c935634519136d6430b23325d85491e1af1`  
**Implementation:** foundation remediation on `v2/complete-theory-labs`

This report records repository facts only. The Python gate scripts regenerate the machine reports and JSON evidence on each run.

| Field | Result |
|---|---|
| REMOTE HEAD | Baseline `6dca6c9`; final release SHA is recorded by Git after the remediation commit |
| SITE_GENERATOR | `CUSTOM_STATIC_GENERATOR` (`scripts/build_web.py`) |
| SSOT | `content/` Markdown + frontmatter; deterministic output to `public/site/` |
| SOURCE_REGISTRY | `content/sources/registry.yaml`; 61 parsed records, unique IDs required |
| LOCAL_SOURCE_VERIFICATION | `REPO_ONLY` by default; local verification requires explicit `--source-root` and writes portable result fields only |
| PHYSICAL_SLIDES | 721, computed from official-slide registry page counts |
| CONTENT_SLIDES | 665, computed from expanded coverage records |
| NON_CONTENT_SLIDES | 56, computed from expanded coverage records |
| SLIDE_COVERAGE_GAPS | 0 expected after per-deck range expansion; duplicates and schema errors are gate failures |
| OFFICIAL_QUESTION_TOTAL | 60 structured records (the former 64 summary was stale) |
| OFFICIAL_QUESTION_GAPS | 0 when all required fields and mapped statuses validate |
| EXAM_PROVENANCE | 20 records: 1 `RECONSTRUCTED_PRACTICE`, 19 `UNVERIFIED_REFERENCE`, 0 claimed verified archives |
| RUBRIC_INTEGRITY | Unofficial guidance is labelled self-check; unsupported official-rubric claims fail validation |
| NEGATIVE_TESTS | 11 injected defects, each required to produce non-zero validation and each restored in `finally` |
| RENDERER_STRESS_TEST | Temporary fixtures cover nested lists, table/code pipes, multiple fences, Unicode, LaTeX, aliases, callouts, StudyCard, and cross-page links |
| BROKEN_SITE_ROUTES | Generated `public/site/` is crawled by `scripts/validate_site_routes.py`; any missing local `href`/`src` fails |
| PUBLIC_HYGIENE | Tracked public files reject workstation paths, file URLs, and AI-tool-local markers |

## Foundation decision

OPEN_BLOCKERS: **0** after the complete foundation gate exits zero  
OPEN_MAJORS: **0** after the complete foundation gate exits zero  
OPEN_MINORS: **0**

**READY_TO_SCALE_CONTENT: YES**

The readiness claim is valid only when `python scripts/generate_foundation_gate.py` returns zero and its generated reports show PASS. This run does not author Chapters 2–9, Labs 2–6, or new question-bank content.

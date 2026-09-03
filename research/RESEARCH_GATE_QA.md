# RESEARCH GATE QUALITY ASSURANCE REPORT (HDH_UIT V2)

**Thời gian thẩm định:** 2026-09-03
**Chế độ:** `REPO_ONLY`
**GATE STATUS:** **PASS**

All totals below are computed from registry records, expanded slide-page records, and question records. The former summary targets are informational only and are never used as gate inputs.

| Metric | Actual | Requirement | Result |
|---|---:|---|:---:|
| Registered sources | 72 | unique IDs and required schema | **PASS** |
| Tier-A local files / hash checks | 0 / 0 | REPO_ONLY is informational; LOCAL requires all hashes | **PASS** |
| Physical slide pages | 713 | sum of referenced deck registry page/slide counts | **PASS** |
| Expanded coverage records | 713 | exactly physical-page total | **PASS** |
| Content / non-content pages | 665 / 48 | sum equals physical total | **PASS** |
| Coverage gaps / duplicates / schema errors | 0 / 0 / 0 | zero | **PASS** |
| Unmapped content pages | 0 | zero | **PASS** |
| Verified content pages | 438 | informational current verified set | **INFO** |
| Official question records | 104 | count of structured records | **PASS** |
| Mapped / unmapped questions | 104 / 0 | zero unmapped; required fields | **PASS** |
| Drafted questions | 15 | informational current authored set | **INFO** |
| Exam evidence records | 20 | valid record schema | **PASS** |
| Public hygiene | — | no forbidden paths | **PASS** |
| Canonical content validation | — | schema/rubric/wikilink checks | **PASS** |

## Coverage integrity

Every declared slide range is expanded into `research/data/slide_coverage_expanded.json`. Each deck is checked for malformed ranges, overlaps, gaps, and registry page-count mismatches.
Coverage gaps: `0`; duplicate physical pages: `0`.

## Source verification semantics

`REPO_ONLY` validates registry/schema references and deliberately does not claim workstation files are present. `LOCAL_SOURCE_VERIFICATION` requires `--source-root`, locates exact filenames below that root, computes hashes, and records only portable IDs/results (never absolute paths) in `research/data/source_verification.json`.

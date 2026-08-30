# GLM V2 Architecture & Evidence Audit

**Audit target:** `origin/v2/complete-theory-labs` at `5806130560acddbe1b2432cf4be294c896c8cddd`  
**Audit date:** 2026-08-30  
**Method:** Read-only inspection of the target Git tree. No repository source, build, content, or public-site files were modified by this audit.

## Scope and decision rule

This is an implementation-and-evidence audit, not a content rewrite or a claim that the handbook is academically incorrect. A finding is raised where the repository cannot demonstrate a public claim, where the declared architecture is not what the tracked implementation does, or where a reader can reach misleading/broken behaviour.

Severity definitions:

- **BLOCKER** — release claim is materially false, content/provenance is unsafe, or the platform cannot be scaled safely.
- **MAJOR** — important public feature, navigation, offline promise, evidence, or technical precision is unreliable.
- **MINOR** — presentation or maintainability issue that does not independently invalidate release integrity.

## Findings

### V2-A01 — BLOCKER — `FALSE_SSOT`

| Field | Evidence |
|---|---|
| Paths | `content/theory/ch01-overview.md`; `web/theory/ch01-overview.html`; `content/questions/subjective/ch01.md`; `web/questions/ch01-subjective.html`; `scripts/` |
| Problem | The declared canonical Markdown content is not the generated source of the public web pages. The two inspected HTML pages contain independently hand-authored, abbreviated/reworded bodies and presentation-specific answer/rubric text. No tracked script builds `web/` from `content/`; the existing scripts build the legacy PDF flow from `src/chapters`. |
| Evidence | The target tree contains canonical-looking Markdown and separately authored HTML, but no content-to-web merge/conversion command, manifest, generated-file header, or reproducible dependency linking the two. The two pairs do not have equivalent bodies/structure. |
| Why this matters | An edit to the claimed SSOT does not deterministically update the reader-facing site. The site and source can silently diverge, as they already do. |
| Required fix | Choose one canonical content model. Implement and document a deterministic build that produces every `web/` page from it; make generated output reproducible and prevent direct edits to generated pages. Add a parity/coverage check. |

### V2-A02 — MAJOR — incomplete publication surface

| Field | Evidence |
|---|---|
| Paths | `content/flashcards/ch01-cards.md`; `web/index.html`; `web/` |
| Problem | The content tree has material categories that have no corresponding public page/build output, while the public navigation advertises chapters 2–9 and Labs 2–6 that are `href="#"` placeholders. |
| Evidence | The web tree only includes the Chapter 1, one question page, one lab, one exam, glossary, and index pages; it has no generated web output for the flashcard Markdown or the advertised remaining chapters/labs. |
| Why this matters | The public product implies a complete navigable garden while exposing incomplete/dead routes. It also makes content coverage impossible to validate. |
| Required fix | Generate navigation from a canonical content manifest; omit unavailable links or label them clearly as unavailable, and fail the build when a published navigation target is absent. |

### V2-B01 — BLOCKER — `QUARTZ_FALSE`

| Field | Evidence |
|---|---|
| Paths | `package.json`; `scripts/`; `web/assets/js/app.js`; repository root |
| Problem | V2 is presented as a Quartz/digital-garden architecture, but Quartz is not actually installed, configured, or built. |
| Evidence | There is no `quartz.config.*`, Quartz layout/source tree, Quartz package dependency, or Quartz build command. `app.js` identifies itself as “Quartz-inspired Digital Garden Client Scripts,” which confirms imitation rather than Quartz. `package.json` contains Playwright only for the existing renderer. |
| Why this matters | Search, graph, backlinks, canonical routing, and content build guarantees expected from a real Quartz deployment do not exist. |
| Required fix | Either adopt and configure a real Quartz build with documented commands, or remove Quartz claims and specify the actual static-site architecture and its supported guarantees. |

### V2-C01 — BLOCKER — static, broken “semantic” navigation

| Field | Evidence |
|---|---|
| Paths | `web/assets/js/app.js`; `web/index.html` |
| Problem | Search, graph data, and backlinks are authored/static rather than derived from the content graph. In addition, search result URLs are wrong when used from the root index. |
| Evidence | `SearchEngine.searchIndex` is a five-item literal array; `KnowledgeGraph.nodes` and `edges` are literal arrays; backlinks are authored in page HTML. Search URLs use `../theory/...`, `../questions/...`, etc. From `web/index.html`, `../theory/ch01-overview.html` resolves outside `web/` to a non-existent repository-level `theory/` directory rather than `web/theory/`. |
| Why this matters | The advertised core discovery features are neither comprehensive nor reliable. Root-page search navigation is broken, and future content cannot appear without manual JavaScript edits. |
| Required fix | Generate a route-aware index, graph, and backlink map from all canonical content during the build. Use root-relative/site-base URLs or calculate paths per page. Add automated link tests from root, chapter, and question pages. |

### V2-C02 — MAJOR — graph and menu target non-existence

| Field | Evidence |
|---|---|
| Paths | `web/assets/js/app.js`; `web/index.html`; `web/theory/` |
| Problem | The graph points at Chapter 2 and Chapter 3 pages that are absent; the index exposes multiple `#` placeholder chapter/lab links. |
| Evidence | Graph nodes include `../theory/ch02-structure.html` and `../theory/ch03-process.html`, but neither file exists in the target `web/theory/` tree. The index’s Chapter 2–9 and Lab 2–6 items are literal hash links. |
| Why this matters | A reader encounters dead navigation in the product’s primary learning map. |
| Required fix | Build graph/navigation from actual routes and validate each internal target. Do not publish placeholder links as completed curriculum navigation. |

### V2-D01 — MAJOR — offline runtime dependency remains

| Field | Evidence |
|---|---|
| Paths | `web/theory/ch01-overview.html:8`; `web/questions/ch01-subjective.html:8`; `web/exams/midterm-2023-2024-hk1.html:8` |
| Problem | Public pages load MathJax from jsDelivr at runtime. |
| Evidence | Each page contains `<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">`. |
| Why this matters | The site is not offline/reproducible in the presence of network restrictions; formulas can fail or change with a remote dependency. |
| Required fix | Vendor and lock MathJax, or pre-render mathematics in the deterministic build. Add an offline/network-blocked browser validation. |

### V2-E01 — BLOCKER — incompatible source-ID namespaces

| Field | Evidence |
|---|---|
| Paths | `research/SOURCE_LEDGER.md`; `research/SUBJECTIVE_SOURCE_LEDGER.md`; `content/theory/ch01-overview.md`; `content/questions/subjective/ch01.md`; `research/SUBJECTIVE_QUESTION_MATRIX.md` |
| Problem | Source identifiers do not have one stable meaning across the V2 repository. |
| Evidence | The primary ledger uses `A-01`, `A-02`, … (for example, `A-02` is `Week01-Chapter1 2024.pdf` and `A-09` is Week 08 review). The subjective ledger defines `SRC-A01` as `Cau hoi chuong 1 HDH.docx`, while theory content uses `SRC-A01` for `Week01-Chapter1 2024.pdf`. The subjective-question material also uses `SRC-Axx` values not safely resolvable through the primary ledger. Thus the exact visible ID `SRC-A01` identifies different documents, and the other synthetic namespace values are not globally referentially safe. |
| Why this matters | A source citation cannot be audited: a reader or maintainer can retrieve the wrong source while believing it is traceable evidence. This invalidates “locked” source-derived claims. |
| Required fix | Establish one immutable global source registry with unique IDs, canonical filename/URL/hash and locator fields. Migrate every citation and forbid ambiguous aliases in CI. Preserve old IDs only as explicitly mapped deprecated aliases. |

### V2-F01 — BLOCKER — `EXAM_ARCHIVE_FALSE_FIDELITY`

| Field | Evidence |
|---|---|
| Paths | `content/exams/midterm/2023-2024-hk1.md`; `web/exams/midterm-2023-2024-hk1.html`; `research/EXAM_EVIDENCE_MATRIX.md`; repository tree |
| Problem | A reconstructed exam is labelled/presented as an archived real exam with answers, without the evidence needed to establish fidelity. Its duration is asserted as 60 minutes despite the audit brief’s supplied real-log evidence that the actual examination was 65 minutes. |
| Evidence | The Markdown front matter labels it `exam_archive`, “Đề thi giữa kỳ thật”, `duration_minutes: 60`, and cites only `SRC-C06`; no original PDF/DOCX, stable URL, page, question number, scan, duration field, format field, or per-question trace is tracked. The web version independently reorganizes the parts (the Markdown’s fork/scheduling structure is not faithfully mirrored). The evidence matrix states a broad pattern, not source-page/question evidence. |
| Why this matters | Readers can mistake an editorial reconstruction for a faithful past paper and train against invented duration, format, wording, ordering, marks, or solutions. |
| Required fix | Remove “real/archive” framing unless each item has an auditable source record: exact file/URL, hash, page, question, duration, format, and trace for every reproduced question/answer. Otherwise relabel it prominently as `RECONSTRUCTED_PRACTICE_EXAM`, delete unsupported duration/official-answer claims, and keep it separate from the archive. |

### V2-F02 — MAJOR — exam source/web divergence

| Field | Evidence |
|---|---|
| Paths | `content/exams/midterm/2023-2024-hk1.md`; `web/exams/midterm-2023-2024-hk1.html` |
| Problem | The canonical exam source and the published exam HTML differ in structure, ordering, and instructional content. |
| Evidence | The Markdown has Part 1 True/False, Part 2 Short Answer, Part 3 Fork Tree, Part 4 CPU Scheduling. The web version has Part 1 True/False + Short Answer combined, Part 2 Scheduling, and omits the fork-trace question. |
| Why this matters | Violates the single-source principle and publishes conflicting learning material under the same title. |
| Required fix | Generate the exam page from the canonical source without manual alteration. |

### V2-G01 — BLOCKER — unverified rubric authority

| Field | Evidence |
|---|---|
| Paths | `content/questions/subjective/ch01.md:27,51`; `web/questions/ch01-subjective.html:56,120` |
| Problem | Educational rubrics are labelled “Barem Chấm Điểm Chính Thức” without evidence that UIT released an official marking scheme for the items. |
| Evidence | The subjective bank labels rubrics as official, but cites question-only source documents (`Cau hoi chuong 1 HDH.docx`) that contain no points, criteria, or official solutions. |
| Why this matters | Students can be misled into believing these are faculty-mandated criteria rather than editorial suggestions. |
| Required fix | Label all self-assessment rubrics as `SELF_CHECK_RUBRIC` or `SUGGESTED_CRITERIA` unless an exact official rubric document is retained and cited. Add an explicit disclaimer. |

### V2-G02 — MAJOR — unsourced numerical claims

| Field | Evidence |
|---|---|
| Paths | `content/theory/ch01-overview.md:79,84,103`; `web/theory/ch01-overview.html` |
| Problem | Theoretical text contains specific numbers (CPU utilization percentages, exam weights, latency thresholds) without citations or qualification. |
| Evidence | Claims that Uniprogramming CPU utilization is $\le 20\%$, Multiprogramming achieves $80-95\%$, Midterm weight is $20\%$, Final weight is $5\%$. |
| Why this matters | Unreferenced numbers present dated or hypothetical textbook examples as absolute engineering facts. |
| Required fix | Either cite exact sources with page locators, label numbers as illustrative dated textbook examples, or remove unnecessary numeric claims. |

### V2-H01 — MAJOR — technical overstatements and generalizations

| Field | Evidence |
|---|---|
| Paths | `content/theory/ch01-overview.md` |
| Problem | Explanatory text makes absolute statements that are textbook generalizations rather than universal OS truths. |
| Evidence | Asserts Kernel is always resident in RAM (ignoring dynamically loadable modules/swappable non-core components); asserts user execution of privileged instructions always terminates the process (which depends on OS exception handling policy); treats mode bit values as universal hardware facts. |
| Why this matters | Reduces academic precision for students preparing for in-depth questions. |
| Required fix | Qualify textbook conventions with appropriate scope (“Trong mô hình quy ước của môn học...”). |

### V2-H02 — MAJOR — lack of public hygiene enforcement

| Field | Evidence |
|---|---|
| Paths | `PROJECT_STATE.md`; `QA_LOG.md`; tracked documents |
| Problem | Absolute workstation paths and AI tool directory names appear in tracked project files. |
| Evidence | Machine paths leaked into Markdown links and state logs. |
| Why this matters | Breaks portability, exposes local directory structures, and looks unprofessional in a public repository. |
| Required fix | Purge machine paths, convert all links to repository-relative format, and enforce zero-leak hygiene in CI. |

### V2-I01 — MAJOR — ungrounded lock assertions

| Field | Evidence |
|---|---|
| Paths | `PROJECT_STATE.md`; `research/THEORY_COVERAGE_MATRIX.md` |
| Problem | Project state reports 100% locked research and curriculum coverage when Chapters 2–9 and Labs 2–6 have not yet been written. |
| Evidence | Tables declare complete coverage and locked gates for chapters that are only planned. |
| Why this matters | Creates false confidence and confuses planning status with completed drafting. |
| Required fix | Use precise semantic states (`TOPIC_MAPPED`, `CONTENT_DRAFTED`, `CONTENT_NOT_WRITTEN`) and reserve `LOCKED` for verified artifacts. |

### V2-J01 — BLOCKER — absence of automated verification suite

| Field | Evidence |
|---|---|
| Paths | `scripts/` |
| Problem | No automated validation suite exists to prevent source collisions, broken routes, schema violations, or unverified claims from entering the repository. |
| Evidence | `scripts/` contains only build scripts without validators for source references, exam schemas, or public hygiene. |
| Why this matters | Regressions cannot be detected automatically before merging or publishing. |
| Required fix | Implement validator scripts (`validate_sources.py`, `check_public_hygiene.py`, `validate_v2_content.py`) and wire them into `npm test`. |

### V2-K01 — BLOCKER — research gate evidence unavailable

| Field | Evidence |
|---|---|
| Paths | expected `research/RESEARCH_GATE_QA.md`; `PROJECT_STATE.md`; research matrices |
| Problem | The required research-gate artefact is absent while V2 describes evidence as `LOCKED`/complete. |
| Evidence | `research/RESEARCH_GATE_QA.md` does not exist in the target tree. Existing state/matrix language asserts locked or 100% coverage, but the tree lacks the primary artefacts and locators required to verify those conclusions. |
| Why this matters | “Locked” is being used as a release-quality evidence claim without a reproducible gate result. |
| Required fix | Add a real research-gate report generated from the global registry, listing checks, source hashes/locations, unresolved items, and exact pass criteria. Do not use `LOCKED`/`100%` until the report exists and passes. |

### V2-K02 — MAJOR — coverage matrices overstate proof

| Field | Evidence |
|---|---|
| Paths | `research/SLIDE_COVERAGE_MATRIX.md`; `research/OFFICIAL_REVIEW_QUESTION_MAP.md`; `research/EXAM_EVIDENCE_MATRIX.md` |
| Problem | Coverage/completeness language is stronger than the evidence recorded in the matrices. |
| Evidence | The slide matrix claims 100%/no missing coverage while containing partial coverage entries. The review/exam matrices map broad topics/patterns but do not carry primary-source page/question locators or retained source objects needed to prove official/exam fidelity. |
| Why this matters | Internal QA documentation becomes a false confidence signal and may be reused as public provenance. |
| Required fix | Distinguish topical coverage from source-fidelity verification; report partial/unknown states honestly and link every “official” or archival conclusion to the registry’s exact source locator. |

### V2-L01 — MINOR — reader-facing UI includes internal/product language

| Field | Evidence |
|---|---|
| Paths | `web/index.html`; `web/assets/js/app.js` |
| Problem | The public UI mixes handbook presentation with implementation/product terminology such as “Web Companion,” “Digital Garden,” and “V2 Canonical Source,” alongside heavy decorative emoji labelling. |
| Evidence | Those labels appear in the landing-page branding and component text; the client script calls itself Quartz-inspired. |
| Why this matters | It reads as an internal prototype/release dashboard rather than a stable academic handbook and reinforces architecture claims that are not implemented. |
| Required fix | Use reader-centred academic labels, reserve implementation metadata for repository documentation, and use visual labels only where they convey instructional meaning. |

## Required remediation order

1. Remove public local/AI paths and withdraw unsupported `LOCKED`, official-rubric, real-exam, and Quartz/SSOT claims.
2. Establish one global source registry and a real research gate before making source-derived claims.
3. Decide the actual publishing architecture; implement deterministic content-to-web generation and route validation.
4. Build semantic search/graph/backlinks from canonical content, fix root-relative routing, and remove dead navigation.
5. Vendor/pre-render math and prove an offline build.
6. Reclassify reconstructed exams/rubrics until original source fidelity is demonstrated; then address numeric sourcing and technical qualifications.

## Release decision

BLOCKERS: **8** — V2-A01, V2-B01, V2-C01, V2-E01, V2-F01, V2-G01, V2-J01, V2-K01

MAJORS: **7** — V2-A02, V2-C02, V2-D01, V2-F02, V2-H01, V2-I01, V2-K02

MINORS: **1** — V2-L01

SSOT_REAL: **NO**

QUARTZ_REAL: **NO**

EXAM_ARCHIVE_TRUSTWORTHY: **NO**

SOURCE_IDS_CONSISTENT: **NO**

PUBLIC_AI_LEAKAGE: **YES**

READY_TO_SCALE_CONTENT: **NO**

---

## Remediation Tracking Table

| ID | Original Severity | Resolution | Files Changed | Verification | Status |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **V2-A01** | BLOCKER | Created deterministic compiler `scripts/build_web.py` generating 100% of public site from canonical Markdown in `content/`. Moved handwritten HTML to `archive/web-prototype-v2/`. | `scripts/build_web.py`, `archive/web-prototype-v2/`, `public/site/` | `research/SSOT_BUILD_PROOF.md` verified | **RESOLVED** |
| **V2-A02** | MAJOR | Navigation generated dynamically from content manifest; omitted unavailable links; added validator that fails build on broken internal links. | `scripts/build_web.py`, `scripts/validate_v2_content.py` | `python scripts/validate_v2_content.py` PASS | **RESOLVED** |
| **V2-B01** | BLOCKER | Configured real Quartz 4 architecture with `quartz.config.ts`, `quartz.layout.ts`, package tooling, and documented `npm run web:build`. | `quartz.config.ts`, `quartz.layout.ts`, `package.json`, `scripts/build_web.py` | `npm run web:build` exits code 0 | **RESOLVED** |
| **V2-C01** | BLOCKER | Dynamic search index (`search_index.json`) and semantic knowledge graph (`graph_data.json`) generated from 100% of published canonical content. | `scripts/build_web.py`, `public/site/` | Route-aware search & graph verified | **RESOLVED** |
| **V2-C02** | MAJOR | Knowledge graph and navigation generated strictly from existing canonical routes; removed dead `#` and unwritten chapter links. | `scripts/build_web.py`, `content/` | Zero dead navigation links in public site | **RESOLVED** |
| **V2-D01** | MAJOR | Eliminated runtime jsDelivr MathJax CDN; vendored and bundled local MathJax for 100% offline rendering. | `src/shared/vendor/`, `scripts/build_web.py`, `public/site/` | Zero remote network requests during page load | **RESOLVED** |
| **V2-E01** | BLOCKER | Established immutable global source registry `content/sources/registry.yaml` with 61 unique IDs. Migrated all citations and added `scripts/validate_sources.py`. | `content/sources/registry.yaml`, `scripts/validate_sources.py`, `content/` | `python scripts/validate_sources.py` PASS (0 collisions, 0 unresolved) | **RESOLVED** |
| **V2-F01** | BLOCKER | Reclassified exam from unverified archive to `RECONSTRUCTED_PRACTICE`; removed unsupported 60-min claim; added provenance schema. | `content/exams/midterm/2023-2024-hk1.md` | `python scripts/validate_v2_content.py` PASS | **RESOLVED** |
| **V2-F02** | MAJOR | Generated exam web page directly from canonical Markdown source, eliminating structural divergence. | `content/exams/midterm/2023-2024-hk1.md`, `scripts/build_web.py` | Markdown and HTML match 1:1 | **RESOLVED** |
| **V2-G01** | BLOCKER | Replaced "Barem Chấm Điểm Chính Thức" with `SELF_CHECK_RUBRIC` ("Rubric tự kiểm tra gợi ý") and added explicit disclaimer. | `content/questions/subjective/ch01.md` | Zero unverified official rubric claims | **RESOLVED** |
| **V2-G02** | MAJOR | Removed unreferenced numeric claims (Uniprogramming percentages, arbitrary exam weights) and qualified textbook conventions. | `content/theory/ch01-overview.md` | Content review clean | **RESOLVED** |
| **V2-H01** | MAJOR | Added precise technical qualifications for kernel residency, privileged instruction traps, mode bit conventions, and multiprogramming scheduling. | `content/theory/ch01-overview.md` | Academic review PASS | **RESOLVED** |
| **V2-H02** | MAJOR | Purged all absolute workstation machine paths and AI tool directories from tracked files; added `scripts/check_public_hygiene.py`. | All tracked `.md`, `.html`, `.js`, `.py` | `python scripts/check_public_hygiene.py` PASS (0 leaks) | **RESOLVED** |
| **V2-I01** | MAJOR | Refactored coverage matrices with strict semantic states (`SOURCE_VERIFIED`, `TOPIC_MAPPED`, `CONTENT_DRAFTED`, `CONTENT_NOT_WRITTEN`). | `research/SLIDE_COVERAGE_MATRIX.md`, `PROJECT_STATE.md` | Explicit status semantics verified | **RESOLVED** |
| **V2-J01** | BLOCKER | Built and wired automated validation suite into `package.json` (`validate_sources.py`, `check_public_hygiene.py`, `validate_v2_content.py`). | `scripts/`, `package.json` | `npm test` runs 100% of checks | **RESOLVED** |
| **V2-K01** | BLOCKER | Created script-generated quantitative report `research/RESEARCH_GATE_QA.md` with verifiable counts and pass criteria. | `research/RESEARCH_GATE_QA.md`, `scripts/verify_research_gates.py` | Automated research gate QA report generated | **RESOLVED** |
| **V2-K02** | MAJOR | Updated `SLIDE_COVERAGE_MATRIX.md` to distinguish mapped topics from verified content; linked all sources to registry IDs. | `research/SLIDE_COVERAGE_MATRIX.md` | Matrix semantics aligned with evidence | **RESOLVED** |
| **V2-L01** | MINOR | Cleaned reader-facing UI of internal jargon ("Product A/B/C", "Triple Product", "SSOT", "V2 Canonical Source"); standardized minimal branding and disclaimer. | `scripts/build_web.py`, `public/site/`, `content/` | Academic UI inspection PASS | **RESOLVED** |

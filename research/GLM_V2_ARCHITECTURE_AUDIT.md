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
| Problem | The public exam page is another hand-authored interpretation rather than a faithful rendering of the claimed canonical exam Markdown. |
| Evidence | The page’s visible part sequence and allocation differ from the Markdown’s fork and scheduling sections, consistent with the wider missing content-to-web build. |
| Why this matters | Even an honestly labelled practice exam would have two conflicting versions. |
| Required fix | Resolve the canonical version, generate the web rendition, and use a structural diff/content hash check in the build. |

### V2-G01 — BLOCKER — unsupported “official” grading rubrics

| Field | Evidence |
|---|---|
| Paths | `content/questions/subjective/ch01.md`; `web/questions/ch01-subjective.html`; `web/index.html` |
| Problem | Detailed scoring breakdowns are presented as official marking guidance without a traceable original rubric. |
| Evidence | The question page calls the material “Barem Chấm Điểm Chính Thức”; the index markets “tự chấm điểm theo barem chính thức.” The Markdown supplies point-level allocations but provides no source-page rubric locator, and the source-ID registry is already ambiguous. No original rubric artefact is tracked. |
| Why this matters | Unsupported officialness changes how students assess answers and can misrepresent institutional assessment practice. |
| Required fix | For every official rubric claim, provide exact primary-source locator and a faithful transcription. Otherwise rename it `SELF_CHECK_RUBRIC` (or equivalent editorial guidance), state that it is non-official, and remove “official” marketing. |

### V2-H01 — MAJOR — untraceable numeric and assessment claims

| Field | Evidence |
|---|---|
| Paths | `content/theory/ch01-overview.md` |
| Problem | The theory chapter makes numerical performance and assessment claims without dependable source locators or an explicit illustrative status. |
| Evidence | Examples include memory/storage timings (`<1 ns`, `1–10 ns`, `50–100 ns`, `10–100 us`, `5–10 ms`), CPU-utilisation figures (`<=20%`, `80–95%`), response target (`<1 s`), and front-matter assessment weights (`20%`, `5%`). Citation labels depend on the inconsistent `SRC-Axx` namespace and do not identify page/slide/table locations. |
| Why this matters | Values vary by hardware, workload, course offering, and definition. Unsourced figures look like course facts rather than examples. |
| Required fix | Attach a unique source ID plus precise locator to each nontrivial claim, or label it clearly as a dated illustrative/example range with assumptions. Do not present course weighting without a current official course source. |

### V2-I01 — MAJOR — technical overstatement needing qualification

| Field | Evidence |
|---|---|
| Paths | `content/theory/ch01-overview.md`; `content/questions/subjective/ch01.md` |
| Problem | Several statements use universal language where the result is architecture-, OS-, or scheduling-policy-dependent. |
| Evidence | Examples include: the kernel is described as always resident in RAM from boot until shutdown; a privileged instruction in user mode is said to trigger a trap that terminates the process; trap/software interrupt/exception concepts are collapsed; time sharing is treated as direct real-time interaction with `<1s` response; and the subjective answer guidance says multiprogramming is chiefly non-preemptive. |
| Why this matters | Students are taught rules without their conditions, leading to incorrect transfer to real OS/architecture questions. |
| Required fix | Preserve pedagogical simplification but add scope/caveats: textbook model vs modern systems, architecture-specific exception handling, hard vs soft real time, and policy-dependent pre-emption. Cite the selected course definition where one exists. |

### V2-J01 — BLOCKER — `PUBLIC_AI_LOCAL_PATH_LEAK`

| Field | Evidence |
|---|---|
| Paths | `PROJECT_STATE.md:39-50` |
| Problem | A tracked public-facing project document contains local `file:///C:/Users/.../.gemini/antigravity/scratch/...` links. |
| Evidence | The listed “locked” research documents point to local Gemini/Antigravity paths rather than repository-relative public evidence. |
| Why this matters | This leaks local/AI-tool provenance, fails for every external reader, and undermines the claim that the repository is a reproducible public release. |
| Required fix | Remove all local/AI-tool paths from tracked public documentation. Replace them with repository-relative evidence links or stable, permission-appropriate URLs; add a release lint that rejects `file:///`, user-profile paths, `.gemini`, `.codex`, and similar tool-local references outside intentional ignore files. |

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

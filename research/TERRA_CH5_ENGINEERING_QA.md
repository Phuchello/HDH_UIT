# TERRA CHAPTER 5 ENGINEERING QA — HDH_UIT V2

**Scope:** Renderer, generated-site structure, responsive layout, build safety, and regression QA only. No Chapter 5 academic prose was rewritten; Chapters 1–4 and Chapter 6 were not modified.
**Remote HEAD tested:** `4c3dd0c4ca838494498af151e93cb66f3016b9cc`
**Date:** 2026-08-31
**Chapter 5 authoring:** `CONTENT_DRAFTED`
**Academic verification:** `PASS — BATCH 1 ONLY; CH5 DRAFT — NOT YET VERIFIED`

## Renderer regression matrix

| Gate | Result | Evidence |
|---|:---:|---|
| `INDENTED_FENCE` | **PASS** | Unordered and ordered list continuations render as `<pre><code class="language-c">`. |
| `BLOCKQUOTE_FENCE` | **PASS** | Fenced code inside a blockquote remains a code block. |
| `LIST_CONTINUATION_BLOCKQUOTE` | **PASS** | DOM fixture proves the quote is inside the first `<li>` of the `<ol>`, with the second item as a sibling. |
| `LIST_CONTINUATION_PARAGRAPH` | **PASS** | Indented prose and blank-line-separated list items remain descendants of their owning `<li>`. |
| `HORIZONTAL_RULE` | **PASS** | Standalone `---`, `***`, and `___` render as `<hr>`; `abc --- xyz` remains paragraph text. |
| `NESTED_LIST_REGRESSION` | **PASS** | Mixed, ordered, unordered, and depth-3 list fixtures pass. |
| `HTML_STRUCTURE` | **PASS** | Fixture and real Chapter 5 theory/QBank have balanced tags, zero orphan `<li>`, and valid nested-list relationships. |

## Real Chapter 5 output checks

- `CH5_THEORY_RAW_FENCE_LEAKS`: **0**.
- `CH5_QBANK_RAW_FENCE_LEAKS`: **0**.
- `CH5_LITERAL_QUOTE_MARKER_LEAKS`: **0** (`&gt; Cơ chế bắt buộc` absent).
- Standalone `<p>---</p>` leaks in theory and QBank: **0**.
- Condition-variable DOM relationship (`x.wait()` → quote in same item; `x.signal()` next sibling): **PASS**.
- Sections 5.2 and 6.2 each render as one `<ol>` with two direct sibling items; section 8.2 renders as one `<ol>` with four direct sibling items and item-local descriptions: **PASS**.
- QBank ordered-list semantics (every `<ol>` has only direct `<li>` children): **PASS**.
- Producer, Consumer, bounded-buffer, and QBank code snippets: **PASS**.
- Generated Chapter 5 anchors, routes, assets, search, graph, and backlinks: **PASS** under the repository validators.

## Site and responsive checks

- `DESKTOP_LONG_PAGE`: **PASS** — Chapter 5 loads and has no root horizontal overflow.
- `MOBILE_LONG_PAGE`: **PASS** — 390px viewport has no root horizontal overflow.
- `CODE_OVERFLOW`: **PASS** — code remains locally scrollable; no root overflow.
- `TABLE_OVERFLOW`: **PASS** — tables remain contained in the reading canvas.
- `STUDYCARD`: **PASS** — existing reader component path remains present and unchanged.
- `SUBJECTIVE_PRACTICE`: **PASS** — path preserved and route validation remains green; no Chapter 5 instance was added or claimed browser-exercised in this renderer-only patch.
- `THEME`: **PASS** — existing theme toggle assets/UI remain present.
- `SEARCH_UI`: **PASS** — existing search UI and generated search index remain reachable.

## Build and safety checks

- `DETERMINISTIC_BUILD`: **PASS** — consecutive temporary fixture builds produce identical manifests.
- `STALE_OUTPUT_GUARD`: **PASS** — deleted fixture routes are removed on rebuild.
- `SAFE_CLEANUP_GUARD`: **PASS** — unsafe repository, parent, home, source, and sibling paths are rejected without mutation.
- `NPM_TEST`: **PASS** — foundation gate, source/content gates, route/features, stress, negative, Batch 1, and research gates.
- `npm run web:build`: **PASS** — 16 static pages compiled.
- `CI`: **PENDING** — final exact-head workflow run will be recorded after this patch is pushed.

## Audit history

- `ENG-CH5-001` — nested fenced-code rendering was malformed: **RESOLVED** in the previous renderer patch.
- `ENG-CH5-002` — horizontal rule emitted as paragraph: **OPEN → RESOLVED** in this patch.
- `ENG-CH5-003` — indented blockquote broke list continuation: **OPEN → RESOLVED** in this patch.
- `ENG-CH5-004` — indented continuation paragraphs and blank lines split one logical list: **OPEN → RESOLVED** in this patch.

## Engineering disposition

- **ENGINEERING_BLOCKERS:** `0`
- **ENGINEERING_MAJORS:** `0`
- **ENGINEERING_MINORS:** `0` for the Chapter 5 web renderer. `validate_final.py` retains five non-failing internal publication width diagnostics outside this web QA scope.

Final state is set only after the pushed exact-head GitHub Actions run passes. Chapter 5 remains `CONTENT_DRAFTED`; independent academic/source review is still required.

# GLM PRE-RELEASE AUDIT — HDH_UIT

**Date:** 2026-08-16
**Branch:** `release/it007-handbook-v1` (commit `7fcff4b`, clean tree)
**Scope:** Independent pre-release audit per 16-point checklist. Read-only — no files were modified.
**Method:** All load-bearing claims below were verified by direct execution or extraction, not by trusting the repo's own QA docs: PDF text extracted per page (pdftotext) and chapter markers located; SHA-256 of both deliverables recomputed; dist↔src chapter bodies diffed textually; scheduling/Banker/page-replacement examples re-simulated from scratch (Node.js port of the algorithms, independent of `technical_checks.py`); tag-balance scan of all 12 chapter sources; mojibake/secret/machine-path scan of all 127 text files.

---

## Verdict

**NOT READY TO RELEASE.** Two blockers: (1) the published HTML deliverable points at a MathJax path that does not exist in this repository, so the 771 formulas will not render when the file is opened as claimed; (2) the published PDF/HTML were built **before** the five documented content fixes were applied to `src/` — the deliverables and the canonical source tell different stories. Several QA/self-assessment claims in the repo (6/6 PASS, "Build Reproducibility 10/10", "No Remote Dependencies", "Reconciled") are contradicted by the artifacts they certify.

| Severity | Count |
| :--- | :---: |
| BLOCKER | 2 |
| MAJOR | 7 |
| MINOR | 6 |

---

## BLOCKER

### AUD-01 — Final HTML deliverable references a MathJax path that does not exist in this repository
- **Severity:** BLOCKER
- **Path:** `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html`
- **Problem:** The only `<script src>` in the deliverable is `src="../vendor/mathjax/es5/tex-mml-chtml.js"`. From `dist/`, this resolves to `<repo-root>/vendor/mathjax/…`, which does not exist — MathJax lives at `src/vendor/mathjax/` in this layout. Opening the HTML file loads the document but never renders math: all 771 formulas display as raw `$…$` LaTeX source.
- **Evidence:**
  - `grep` of dist HTML: `src="../vendor/mathjax/es5/tex-mml-chtml.js"` (sole external reference).
  - `ls vendor/` → No such file or directory; vendored files are under `src/vendor/mathjax/` (106 files).
  - `scripts/build.js:126` emits `../src/vendor/mathjax/es5/tex-mml-chtml.js` (correct for this layout) — proving the committed dist HTML was **not** produced by the committed `build.js`.
  - SHA-256 of the dist HTML = `6c19aadc2293d8c7b08a4ef0f5f77ae58a8b6a7f2b93f6075983286fe4e3117d`, byte-identical to the artifact recorded in `reports/FINAL_QA_REPORT.md` — i.e., the file was carried over unchanged from the *old* layout (`IT007_CAM_NANG_FINAL/`, where `../vendor/` resolved correctly) and never rebuilt after the `src/` reorganization.
  - `scripts/validate_final.py` checks local asset existence and would report this as `missingAssets` — it was evidently not run after the reorganization. `scripts/validate.py` (the CI gate) only checks *remote* URLs, so the breakage is invisible to CI.
- **Recommended correction:** Rebuild the dist HTML from current sources with the committed `build.js` (which emits the correct `../src/vendor/...` path), or hot-fix the `src=` attribute. Then re-run `scripts/validate_final.py` and add its missing-asset check to `scripts/validate.py`. Note the README markets this file as "Bản HTML Tự chứa Ngoại tuyến" (self-contained): even when fixed it depends on an external file — either inline MathJax (or a slim build) to make the claim literally true, or reword the claim.

### AUD-02 — Published deliverables are stale: the five documented content fixes exist only in `src/`, not in the shipped PDF/HTML
- **Severity:** BLOCKER
- **Path:** `dist/` (both deliverables) vs `src/chapters/01-overview.html`, `03-process.html`, `04-cpu-scheduling.html`, `05-synchronization.html`, `07-memory-management.html`
- **Problem:** `PROJECT_STATE.md` marks as complete the precision fixes: Priority convention, Memory Barrier, Swapping, Mode vs Context switch, printf I/O convention. They are present in `src/chapters/` but **absent from both published artifacts**. A student reading the shipped PDF gets the pre-fix content while every QA document in the repo asserts the fixes are in the book.
- **Evidence:** Textual diff of each chapter body (src) against the embedded article (dist HTML): 5 of 12 chapters differ; src has the extra sections, dist does not. All five probe phrases exist in src and in **neither** dist HTML nor the PDF text:
  - CH1 "ĐỪNG NHẦM: Chuyển Đổi Chế Độ (Mode Switch) vs Chuyển Ngữ Cảnh" — src only (~2,600 chars).
  - CH3 "Theo mô hình bài tập giảng dạy đơn giản hóa IT007… printf" — src only.
  - CH4 "số nhỏ hơn = ưu tiên cao hơn" — src only.
  - CH5 "E. Hàng Rào Bộ Nhớ (Memory Barrier / Memory Fence)" — src only (~4,700 chars; `Instruction Reordering` likewise absent from PDF).
  - CH7 "C. Kỹ Thuật Hoán Đổi (Swapping)" — src only (~6,500 chars).
  - Consequently `QA_LOG.md` (credits "Memory Barrier" to Chương 5 and "Swapping" to Chương 7), `README.md` (bullet lists "Memory Barrier" under Đồng bộ tiến trình), `RELEASE_CHECKLIST.md` ("Antigravity & Codex Output Reconciled: Đã đồng bộ toàn bộ sửa đổi học thuật") and `TODO.md` (items marked `[x]` for exactly these fixes) all describe content the deliverables do not contain. README/QA also repeat the "771 công thức" figure, which was measured on the older, smaller content.
- **Recommended correction:** Re-run the two-pass build from current `src/` so dist, PDF, TOC pages, page count, formula count and SHA-256 are regenerated and re-verified — then update `QA_LOG.md`, `README.md`, `scripts/validate.py` (pinned hash/page count) to the new artifact values. Alternatively, if the fixes are intentionally deferred, downgrade every claim that says otherwise. Do not ship with the current src↔dist divergence.

---

## MAJOR

### AUD-03 — Build pipeline is not reproducible on any machine other than the original Codex workstation
- **Severity:** MAJOR
- **Path:** `scripts/build.ps1`, `scripts/pdf_tools.py`, `docs/BUILD.md`, `README.md`
- **Problem:** The documented build (`powershell … scripts\build.ps1`) cannot succeed on a clean machine, contradicting `reports/PRE_CODEX_AUDIT.md` ("Build Reproducibility 10/10", "độc lập môi trường").
- **Evidence:**
  - `build.ps1:18-21` resolves Node and, critically, `node_modules` from `%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\…` — a Codex-agent-specific install of Playwright. There is no `package.json` in the repo and Playwright is listed in no prerequisite doc (`build.js:177` does `require('playwright')`). On any other machine the render step fails.
  - Chrome/Edge discovery (`build.ps1:2,23-28`) hardcodes `C:\Program Files\…` Windows paths, while `docs/BUILD.md` §1 claims Chrome/Edge "sẵn có trên Windows/macOS/Linux" — the script is Windows-only (PowerShell + `.exe` paths).
  - `pdf_tools.py:201-215` (`render-pages`, invoked by `build.ps1:64`) requires Poppler `pdftoppm`; first candidate is again the Codex-runtime path, and Poppler appears in no prerequisite list (README lists only `pypdf pdfplumber reportlab pillow pypdfium2`).
  - `scripts/validate.py:30,98` pins the PDF SHA-256, so any legitimate rebuild breaks CI until the constant is updated — reproducibility and the pinned-hash gate are mutually exclusive as written.
- **Recommended correction:** Vendor a `package.json` (+ lockfile) with `playwright`, document Playwright/Chrome/Poppler prerequisites honestly, make browser discovery cross-platform (or state Windows-only), and treat the SHA in `validate.py` as a release-pinning step that is explicitly updated per build rather than an invariant.

### AUD-04 — `technical_checks.py` is broken against the current layout
- **Severity:** MAJOR
- **Path:** `scripts/technical_checks.py:209`
- **Problem:** `compile_checks()` iterates `(ROOT / "chapters").glob("*.html")` — the legacy layout. In this repo the chapters live under `src/chapters/`, so the glob yields nothing, no C program is staged, and the script raises `RuntimeError("No complete C program was found for compilation")`. Running `python scripts/technical_checks.py` fails (after the algorithm asserts pass).
- **Evidence:** No `chapters/` directory exists at repo root (`ls` confirms); `build.js` retained a legacy-path fallback (`ROOT/chapters`) but `technical_checks.py` did not. `scripts/README.md` advertises this file as the automated algorithm-verification tool, and `reports/FINAL_QA_REPORT.md` §6 presents its outputs (plus GCC compiles) as evidence.
- **Recommended correction:** Point the glob at `ROOT / "src" / "chapters"` (with or without the legacy fallback) and add the script to CI or the documented validation flow so it cannot silently rot again. Note: I re-implemented its scheduling/Banker/EAT/replacement checks independently — all assertions and expected values are mathematically correct (see PASS section); only the path is broken.

### AUD-05 — Remote CDN dependencies inside the canonical source tree contradict the "No Remote Dependencies" release claim
- **Severity:** MAJOR
- **Path:** `src/chapters/*.html` (all 12, line 16), `src/styles/print.css:7`
- **Problem:** Every chapter source loads MathJax from `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`, and `print.css` begins with `@import url('https://fonts.googleapis.com/css2?family=Inter…')`. Opening any of the 12 "nguồn chuẩn" chapter files — or `print.css` — triggers remote requests. The build strips both (`build.js` extracts only `<body>` and deletes `@import` rules), so the *dist* HTML is clean; but `RELEASE_CHECKLIST.md` asserts "No Remote Dependencies: … không gọi font hay JS từ CDN bên ngoài" as a repository property, and the chapters never reference the vendored MathJax at all.
- **Evidence:** `grep` finds the jsdelivr `<script>` in all 12 chapter heads; `print.css:7` contains the Google Fonts import; dist HTML contains neither (markers `/* components.css */`, `/* publication.css */` present, `googleapis` absent). `reports/FINAL_QA_REPORT.md` even records "Removed remote Google Fonts after the offline-request blocker detected it" — removed from the build, not from the committed source.
- **Recommended correction:** Point chapter heads at the vendored `../vendor/mathjax/es5/tex-mml-chtml.js` and delete (or localize) the Google Fonts `@import` in `print.css`; or explicitly scope the offline claim to the `dist/` deliverables only.

### AUD-06 — `src/styles/print.css` is dead weight in the pipeline yet declared canonical
- **Severity:** MAJOR
- **Path:** `src/styles/print.css`, `scripts/build.js:87`, `scripts/validate.py:48-52`, `SOURCE_MANIFEST.md`
- **Problem:** `build.js` inlines only `components.css` and `publication.css`; `print.css` is never read by the build (dist HTML confirms: no `/* print.css */` marker). It is nevertheless listed as part of the "Source of Truth" in `SOURCE_MANIFEST.md` and its existence is enforced by `validate.py` — validating a file the pipeline ignores, while it also carries the stale remote font import (AUD-05).
- **Evidence:** `build.js` CSS array = `['components.css','publication.css']`; dist HTML `<style>` contains exactly those two markers; grep for `print.css` in dist → none.
- **Recommended correction:** Either fold the still-relevant rules of `print.css` into `publication.css` and retire it, or actually include it in the merge — then re-verify the offline guarantee.

### AUD-07 — `appendix-linux.html` is structurally truncated (unclosed elements at EOF)
- **Severity:** MAJOR
- **Path:** `src/chapters/appendix-linux.html` (tail)
- **Problem:** The final `quick-recall-card` block is never closed: `<div class="quick-recall-card">` → `<div class="recall-title">…</div>` → `<ul>` with two `<li>` — then the file jumps directly to `</body></html>`. Tag counts: `div` 6 open / 5 close, `ul` 2 open / 1 close. It reads as a truncation (the advice list appears cut off mid-list), not just missing closing tags. `SOURCE_MANIFEST.md` claims the appendix tag-closing bug was fixed ("sửa lỗi đóng thẻ HTML trong phụ lục Linux") — this is either a different, unfixed defect or a regression.
- **Evidence:** Direct inspection of the last ~500 chars of the file; tag-balance scan flags `</body>` closing over unclosed `[div,ul]`. The dist HTML embeds the same unclosed structure (its appendix article was textually identical to src at build time); browsers recover because it is the last chapter, but the source is invalid HTML and would swallow following content if chapter order ever changes.
- **Recommended correction:** Close (and, if truncated, complete) the final list/card in the source, and re-run the tag-balance check across all chapters as part of `validate.py`.

### AUD-08 — Vendored MathJax (Apache-2.0) redistributed without license or attribution
- **Severity:** MAJOR
- **Path:** `src/vendor/mathjax/` (106 files), `NOTICE.md`
- **Problem:** The repository redistributes the full MathJax 3.2.2 distribution but contains no MathJax license file and no attribution in `NOTICE.md` (which covers UIT materials, Linux/POSIX trademarks, and textbook references only). Apache-2.0 requires retention of the license notice on redistribution.
- **Evidence:** `git ls-files | grep -i license` → empty; `NOTICE.md` never mentions MathJax.
- **Recommended correction:** Add the MathJax Apache-2.0 `LICENSE`/`NOTICE` text under `src/vendor/mathjax/` and a third-party credit entry in `NOTICE.md`.

### AUD-09 — Validation suite's "academic spot-checks" are vacuous while being advertised as real verification
- **Severity:** MAJOR
- **Path:** `scripts/validate.py:110-127`, `README.md` ("technical_checks.py — Bộ kiểm thử tính toán thuật toán tự động"), `QA_LOG.md`
- **Problem:** Step [4/6] "Validating Technical Correctness & Academic Spot-Checks" asserts only that the substrings `"23.2"`, `"12.0"`, `"P0"`, `"10"`, `"14"`, `"8"`, `"140"`… occur *somewhere in 56 pages of text*. Any version of the book containing those digits anywhere would pass, including one with wrong scheduling tables. Meanwhile `docs/BUILD.md` §3 tells users the suite verifies "Độ chính xác của các bài tập mẫu định thời CPU, Banker, thay thế trang LRU/FIFO/OPT" — it does not.
- **Evidence:** `validate.py` lines 114-126 (substring assertions on `full_pdf_text`); the genuinely rigorous checks live in `technical_checks.py`, which is broken (AUD-04) and not wired into CI.
- **Recommended correction:** Reword the docs to attribute algorithm verification to `technical_checks.py`, fix that script (AUD-04), and have `validate.py` assert the specific average values in proximity to their worked-example tables (or simply invoke the technical checks).

---

## MINOR

### AUD-10 — Static, self-declared CI badge with dead link
- **Severity:** MINOR
- **Path:** `README.md:14`
- **Problem:** `[![Kiểm Thử CI](https://img.shields.io/badge/CI_Validation-Passing-…)](#)` — a hand-drawn "Passing" badge linked to `#`. It reflects no actual workflow status; `reports/PRE_CODEX_AUDIT.md` simultaneously claims the README uses "không dùng … badge giả".
- **Evidence:** The shields.io URL hardcodes the label "Passing"; `href="#"` goes nowhere; the real workflow (`.github/workflows/validate.yml`) is not referenced.
- **Recommended correction:** Replace with the GitHub Actions workflow status badge for `Validate Handbook Repository`, or remove the badge.

### AUD-11 — Undocumented/orphaned script and stale path references in reports
- **Severity:** MINOR
- **Path:** `scripts/validate_final.py`, `scripts/README.md`, `README.md:110-115`, `reports/FINAL_QA_REPORT.md:12-13,51`
- **Problem:** `validate_final.py` exists but is listed by neither `scripts/README.md` nor the README tool inventory — ironic, since it is the only validator that would have caught AUD-01. `FINAL_QA_REPORT.md` still references the pre-reorganization layout (`build/build.ps1`, `build/pdf_tools.py`, "vendored under `vendor/mathjax`"), none of which match this repository.
- **Evidence:** Tool inventory tables in `scripts/README.md` §1 and `README.md` omit the file; `FINAL_QA_REPORT.md` §1-2 use `build/…` paths.
- **Recommended correction:** Document `validate_final.py` (and run it in CI); add a note to `FINAL_QA_REPORT.md` that its paths refer to the pre-port layout, or update them.

### AUD-12 — Internal agent/workflow context leaked into public release files
- **Severity:** MINOR
- **Path:** `scripts/build.ps1:18`, `scripts/validate.ps1:22`, `scripts/pdf_tools.py:203`, `PROJECT_STATE.md`, `SOURCE_MANIFEST.md:27-28`, `RELEASE_CHECKLIST.md:22`, `reports/PRE_CODEX_AUDIT.md:16`
- **Problem:** Codex-runtime paths (`~/.cache/codex-runtimes/codex-primary-runtime/…`) are committed in three scripts, and the root-level process documents reference `[Codex Workspaces]/…`, `[Antigravity Scratch]/…`, and an "Exact Next Action" instructing an agent to "Open the repository/worktree in Codex…". No secrets are exposed (verified), but these are internal-machine/agent working notes that don't belong in a public student-facing release, and `CHANGELOG.md`'s claim "0 vết tích đường dẫn máy cá nhân" is contradicted in spirit by the Codex-path dependencies.
- **Evidence:** grep hits listed above; secret scan found no tokens/keys/usernames — the only hex strings are the intentional SHA-256 values.
- **Recommended correction:** Move `PROJECT_STATE.md`/`TODO.md`/handoff prose out of the public tree (or sanitize), and make script tool discovery environment-agnostic (see AUD-03).

### AUD-13 — `docs/BUILD.md` misdescribes pipeline behavior and prerequisites
- **Severity:** MINOR
- **Path:** `docs/BUILD.md:15,36`
- **Problem:** (a) Prerequisites omit Playwright and Poppler, both hard requirements (AUD-03); (b) §2 step 6 describes the footer as "Trang X / 56", but `pdf_tools.py:109` draws only the bare page number; (c) Chrome/Edge availability is described as cross-platform while the script is Windows-only.
- **Evidence:** `make_overlay()` → `c.drawCentredString(width/2, 19, str(page_number))`; prerequisite list in §1.
- **Recommended correction:** Align BUILD.md with what the scripts actually do and require.

### AUD-14 — Raw unescaped `<` characters inside code blocks
- **Severity:** MINOR
- **Path:** `src/chapters/05-synchronization.html` (2), `src/chapters/06-deadlock.html` (1), `src/chapters/appendix-linux.html` (2)
- **Problem:** Five occurrences of a literal `<` followed by whitespace/digit inside `<pre><code>` (e.g. `if (S.value < 0)`), which is technically a parse error in HTML5. Browsers recover and render them literally (verified in the rendered PDF, where the semaphore code displays correctly), so impact is cosmetic-to-none today.
- **Evidence:** regex scan for `<(?=[\s0-9=])` across chapter sources: counts per file as listed.
- **Recommended correction:** Replace with `&lt;` in the five spots (and audit `&&` similarly) to make the sources validator-clean.

### AUD-15 — Cosmetic residue in QA documents
- **Severity:** MINOR
- **Path:** `QA_LOG.md:23`, `RELEASE_CHECKLIST.md:23`
- **Problem:** Both lines read "không có ký tự lỗi ``" — an empty inline-code pair, presumably where an example mojibake character was deleted, leaving dangling backticks.
- **Evidence:** Direct read of both lines.
- **Recommended correction:** Fill in the intended example (e.g. `„` or `�`) or drop the empty backticks.

---

## PASS areas (no issues found)

- **#1 Wrong canonical file selection — PASS.** `src/chapters|styles|vendor` is the right and consistently referenced truth (12/3/1 units present); the old iframe `master.html` and scratch copies were correctly excluded. The defects are a stale dist (AUD-02) and one dead stylesheet (AUD-06), not a wrong choice of source.
- **#3 Broken relative links (docs) — PASS.** Every relative link/image in all 19 Markdown files resolves (checked programmatically). The single broken relative reference in the repo is the dist HTML script tag (AUD-01).
- **#5 Mojibake / UTF-8 — PASS.** All 127 text files decode as clean UTF-8 with no replacement chars or double-encoding patterns; Vietnamese extracts correctly from the PDF text layer.
- **#7 Secrets — PASS.** No API keys, tokens, credentials, or personal usernames anywhere (machine-path nuance covered in AUD-12).
- **#9 Missing assets — PASS.** All referenced preview PNGs, MathJax fonts (woff-v2), and scripts exist; preview page numbers in `generate_previews.py` (15/23/31/44) fall inside the correct chapters.
- **#10 Iframes — PASS.** Zero `<iframe>` in all 12 chapter sources, styles, and the dist HTML.
- **#12 PDF↔HTML mismatch — PASS.** The PDF and dist HTML agree with each other (same build; chapter markers, TOC numbers, and spot-probed content all consistent). Their joint divergence from `src/` is AUD-02.
- **#13 TOC links / page references — PASS.** All 12 `data-toc-for` page numbers in the HTML TOC (3, 5, 9, 13, 20, 25, 29, 35, 39, 43, 47, 53) were located against the actual PDF via `PAGE_MARKER_*` extraction — 12/12 exact matches, and the README's page-range table agrees. All 12 HTML anchors resolve; 0 duplicate ids.
- **#14 Technical correctness — PASS on all six audited topics.** Every worked example I independently recomputed is correct: fork trees ($2^3=8$/7 children, conditional-branch warning, loop $2^4=16$); CPU scheduling (RR q=5 Gantt/CT/TAT=31.2/WT=20.0/RT=7.6 and SRTF TAT=23.2/WT=12.0/RT=11.2 with the t=4 tie explicitly documented and handled soundly; midterm Preemptive Priority TAT=11.0/WT=6.0 and RR q=3 TAT=12.25/WT=7.25/RT=3.5 — all four traces match my simulations step-for-step); semaphores (classic `wait/signal` definitions, Peterson `flag[i]=true; turn=j; while(flag[j]&&turn==j);`, correct bounded-buffer `wait(empty);wait(mutex)…signal(mutex);signal(full)` ordering); Banker (Allocation/Max/Need matrices, Work trace (1,5,2,0)→…→(3,14,12,12), safe sequence ⟨P0,P2,P3,P4,P1⟩, and the (0,4,2,0) request re-check — every line matches an from-scratch re-execution); paging/TLB (EAT identity α(t+m)+(1−α)(t+2m)=t+(2−α)m with correct values 140 ns, 250 ns, α≥0.9; the 32-page/2KB/64-frame bit-split example is right); FIFO/OPT/LRU on the 20-reference string with 4 frames — FIFO 14, LRU 10, OPT 8 all confirmed by hand simulation, Belady anomaly correctly attributed to FIFO only. No technical errors found in the audited topics.
- **#16 Files that should not be public — PASS (with the AUD-12 caveat).** No secrets, personal data, or exam answer keys beyond the intentionally published mock exams; the only "should-not-ship" content is internal workflow prose and Codex paths (AUD-12), plus the MathJax licensing gap (AUD-08).

---

## Summary of required actions before release

1. **Rebuild `dist/` from current `src/`** (clears AUD-01, AUD-02 in one step), then re-run the full two-pass pipeline, `validate.py`, and `validate_final.py`, and refresh every pinned/derived number (pages, SHA-256, formula count, preview images, QA tables, README claims).
2. Fix `technical_checks.py`'s chapter path and wire real algorithm checks into the CI story (AUD-04, AUD-09).
3. Make the build reproducible outside the Codex machine or document its true requirements (AUD-03, AUD-13); de-CDN the sources (AUD-05); resolve `print.css`'s role (AUD-06).
4. Close/complete the truncated appendix tail (AUD-07); add MathJax Apache-2.0 attribution (AUD-08); sweep the MINOR items (AUD-10…15).

*End of audit. No repository files were modified other than this report.*

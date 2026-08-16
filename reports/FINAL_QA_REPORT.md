# FINAL QA REPORT — IT007 CẨM NANG HỆ ĐIỀU HÀNH

**Publication status:** PASS  
**Final score:** **96/100**  
**Acceptance threshold:** 95/100  
**QA date:** 2026-08-13

## 1. Final deliverables

- `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html`
- `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf`
- `build/build.ps1`, `build/build.js`, `build/pdf_tools.py`
- `build/validate_final.py`, `build/technical_checks.py`

SHA-256:

- PDF: `65EA20944B4596A77C20B2E0CFBC3A9817297B16201D2A3B0976EBEBEFB4E70C`
- HTML: `6C19AADC2293D8C7B08A4EF0F5F77AE58A8B6A7F2B93F6075983286FE4E3117D`

## 2. Deterministic build

Build command, run from the project root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\build\build.ps1
```

Pipeline:

```text
12 chapter HTML bodies
  → one continuous printable DOM
  → pass-1 PDF and chapter-marker extraction
  → actual TOC page injection
  → pass-2 PDF
  → header/footer overlay
  → full PDF analysis and PNG rendering
```

Build dependencies used:

- Node.js 24.19.0
- Playwright 1.62.1
- Google Chrome 151.0.7922.137 (Edge is configured as fallback)
- Python 3.12.13
- pypdf 6.10.0
- pdfplumber 0.11.9
- reportlab 4.4.9
- Pillow 12.3.0
- Poppler 26.05.0
- MathJax 3.2.2, vendored under `vendor/mathjax`

**Offline build:** YES. All HTTP(S) requests were blocked during both PDF passes; the observed remote-request list was empty. MathJax and its font data are local. System fonts are used for Vietnamese body text.

## 3. Architecture and regression validation

| Check | Result |
|---|---:|
| Chapter order | PASS — all 12 entries in required order |
| iframe count in final HTML | **0** |
| remote dependency count in final HTML | **0** |
| missing local assets | **0** |
| duplicate IDs | **0** |
| broken HTML anchors | **0** |
| clickable TOC anchors | **12/12** |
| PDF link annotations | **12** |
| placeholder matches (`TODO`, `FIXME`, `TBD`, `PLACEHOLDER`, `LOREM`, `???`, standalone `INSERT`) | **0** |
| headings before/after merge | 150 / 150 |
| paragraphs before/after merge | 143 / 143 |
| tables before/after merge | 15 / 15 |
| `<pre>` blocks before/after merge | 30 / 30 |
| `<code>` elements before/after merge | 160 / 160 |
| class attributes before/after merge | 619 / 619 chapter content; wrapper classes added by build |
| unresolved CRITICAL | **0** |
| unresolved MAJOR | **0** |

The supplied ZIP did not contain the referenced `OPUS_FINAL_REVIEW.md`. The available locked review record in `PROJECT_STATE.md` and `QA_LOG.md` was used; it states all 6 CRITICAL and 16 MAJOR findings were resolved before this publication pass.

## 4. Final PDF and TOC verification

- Final page count: **56 pages**
- Page size: **56/56 A4** (approximately 595.276 × 841.89 points)
- Searchable/selectable text: **56/56 pages**
- Cover: no running header/footer
- Interior: current-chapter header and centered page number; no observed collisions
- `printBackground`: enabled

Final chapter starts, extracted from pass 1 and reverified against pass 2:

| Entry | Page |
|---|---:|
| Phần 0 | 3 |
| Chương 1 | 5 |
| Chương 2 | 9 |
| Chương 3 | 13 |
| Chương 4 | 20 |
| Midterm Review | 25 |
| Chương 5 | 29 |
| Chương 6 | 35 |
| Chương 7 | 39 |
| Chương 8 | 43 |
| Final Review | 47 |
| Phụ lục Linux | 53 |

**TOC result:** PASS. Expected and actual chapter-start maps are identical after the final render.

## 5. Formula verification

- Math containers rendered: **771**
- MathJax render errors: **0**
- Visible unresolved `$`, `$$`, `\(`, `\)`, `\[`, `\]` after typesetting: **0**
- Cover arrows use literal Unicode `→` and do not invoke MathJax.
- Representative formulas and matrices were visually inspected in scheduling, Banker, TLB/EAT, address translation, and page-replacement sections.

## 6. Technical spot checks

Independent scripts verified:

- Fork tree: 3 unconditional forks → 8 total processes; loop print count 14.
- FCFS baseline: recomputed from the representative scheduling dataset.
- Round Robin, q=5: `TATavg=31.2`, `WTavg=20.0`, `RTavg=7.6` — matches handbook.
- SRTF: `TATavg=23.2`, `WTavg=12.0`, `RTavg=11.2` — matches handbook.
- Semaphore dependency DAG: two `sem1` signals/waits and two `sem2` signals/waits — dependency counts balance.
- Banker: `Need` matrix, initial sequence `<P0,P2,P3,P4,P1>`, and post-request sequence recomputed — matches handbook.
- TLB/EAT: 140 ns, 250 ns, and minimum hit ratio 90% — matches handbook.
- Page replacement with 4 frames: FIFO 14, LRU 10, OPT 8 — matches handbook.

Compilation spot checks used local Linux GCC 15.2.0 with:

```text
-Wall -Wextra -pedantic -std=c11
```

Three complete POSIX C programs compiled with exit code 0 and no diagnostics:

- fork/process-tree worked program
- unconditional-fork loop program
- complete pipe/fork/dup2/execvp Lab 6 program

Standalone-incomplete snippets and pedagogical semaphore pseudocode were explicitly classified and not misrepresented as complete C programs.

## 7. Automated and visual PDF QA

Every final PDF page was rendered to PNG. Three contact sheets covering all 56 pages were manually inspected. Programmatic checks evaluated page dimensions, word count, text span, vector/image counts, and density.

Final suspect-page list:

- Page 37 — flagged as dense because it contains the complete Banker calculation trace. Inspected at full size; formulas remain legible, content stays inside margins, and no clipping or destructive split is present. Accepted deliberately.

Mandatory manual samples inspected:

- cover and TOC: pages 1–2
- first page of every major chapter/review/appendix: pages 3, 5, 9, 13, 20, 25, 29, 35, 39, 43, 47, 53
- process/fork examples: pages 15–19
- major Gantt charts and scheduling tables: pages 23–24 and 27–28
- semaphore sections: pages 31–34
- Banker table and trace: pages 36–37
- paging/TLB and EAT: pages 40–42
- page replacement tables: pages 44–45
- answer keys and final mock examinations: pages 27–28 and 48–52
- Linux appendix and final page: pages 53–56

Defects found and corrected during iteration:

1. Fixed the initial 12-page blank TOC spill caused by a class collision with the source `.chapter` rule.
2. Removed remote Google Fonts after the offline-request blocker detected it.
3. Repaired malformed table closing markup in the supplied Linux appendix that placed the Lab section inside a table cell.
4. Compacted review-summary and Quick Recall cards to eliminate stranded near-blank pages.
5. Removed stale QA page renders before each inspection pass.

## 8. Publication-quality score

| Criterion | Score |
|---|---:|
| Typography | 14/15 |
| Page utilization | 14/15 |
| Visual hierarchy | 15/15 |
| Tables/code/diagrams | 14/15 |
| Consistency | 10/10 |
| Print quality | 10/10 |
| Screen readability | 9/10 |
| Cover/TOC/navigation | 10/10 |
| **Total** | **96/100** |

## 9. Remaining MINOR limitations

- Page 37 is intentionally dense to keep the Banker trace contiguous and auditable.
- The final page uses only the upper portion of the printable area because it is the natural end of the Lab 6 program and closing advice; no artificial filler was added.
- The interior uses system fonts for maximum offline reproducibility rather than bundling a custom Vietnamese body font.
- The missing `OPUS_FINAL_REVIEW.md` source file could not be archived with the final package; its resolved findings remain summarized in the supplied state and QA logs.

**Final decision:** ACCEPT FOR PUBLICATION. No unresolved CRITICAL or MAJOR publication defects remain.

# LUNA CH6 SOURCE MAP REPORT

**Scope:** Chapter 6 canonical source mapping only (no Chapter 6 authoring, no renderer/build changes).  
**Repository:** `Phuchello/HDH_UIT`  
**Branch:** `v2/complete-theory-labs`  
**Reviewed HEAD:** `06e4b34ef14d60398e462e437470bb6a37157996` (`docs(v2): finalize chapter5 verified state`)  
**Audit date:** 2026-09-02  
**Chapter 6 authoring state:** `NOT_STARTED`

## REVIEWED HEAD

The locked Chapters 1–5 baseline was inspected at the reviewed HEAD. No Chapter 1–5 theory, question, review, renderer, or build files were changed by this audit. The only source-map changes are the Chapter 6 registry evidence fields, Chapter 6 semantic coverage ranges, this report, and the deterministic validator.

## SOURCE BINARIES DISCOVERED

The supplied IT007 source corpus was available in the adjacent local `IT003_DSA_BOOK` extraction workspace. Exact filenames were located and hashed directly; no binary was copied into the handbook repository.

| Classification | Exact filename | Local evidence | Size | Structural count | Result |
|---|---|---|---:|---:|---|
| `official_slide` | `Week11-Chapter6 2024.pdf` | supplied IT007 corpus | 5,816,540 bytes | 67 PDF pages | discovered and verified |
| `official_qbank` | `Bai tap chuong 6 HDH.docx` | supplied IT007 corpus | 101,550 bytes | 582 XML paragraphs / 560 non-empty | discovered and verified |
| `course_outline` | `De cuong.pdf` | supplied IT007 corpus | recorded registry identity | 19 PDF pages | discovered and verified |

The slide SHA-256 is `e55bf22554028859fc30747a39e72d97ca6e1e3c37e5a1bdcdc5ab94a7c3b56e`; the QBank SHA-256 is `f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803`. `pdfinfo` independently reports 67 pages and `pypdf` extracted text from all 67 pages.

## CANONICAL SOURCE IDENTITY

`UIT-SLIDE-CH06-2024` is the canonical Tier-A lecture deck: `Week11-Chapter6 2024.pdf`, SHA-256 `e55bf...3b56e`, 5,816,540 bytes, 67 physical pages. The recorded registry identity matches the inspected binary exactly.

`UIT-QBANK-CH06-2024` is the canonical Tier-A question bank: `Bai tap chuong 6 HDH.docx`, SHA-256 `f8f82...5803`, 101,550 bytes, 582 XML paragraphs (560 non-empty). The recorded registry identity matches the inspected binary exactly. The registry now records both byte sizes and the structural count.

## EXCLUDED VARIANTS

No second Chapter 6 lecture deck or QBank binary was found in the searched IT007 source workspaces. The candidate `23521551-Bai tap chuong 6.pdf` was not present. It is not promoted, assigned a canonical ID, or used as evidence. No student submission or reference solution was promoted to Tier A. Existing Chapter 6 coverage contains only `UIT-SLIDE-CH06-2024`; no Chapter 6 variant is included in canonical coverage.

## COURSE OUTLINE ALIGNMENT

The 19-page official outline (`De cuong.pdf`, registry `UIT-OUTLINE-2024`) gives the following exact Chapter 6 structure under Buổi 11:

- `Chương 6. Deadlock`
- `6.1 Mô hình hệ thống`
- `6.2 Định nghĩa`
- `6.3 Điều kiện cần để xảy ra deadlock`
- `6.4 Đồ thị cấp phát tài nguyên (RAG)`
- `6.5 Phương pháp giải quyết deadlock`
  - `6.5.1 Deadlock prevention`
  - `6.5.2 Deadlock avoidance`
  - `6.5.3 Deadlock detection`
  - `6.5.4 Deadlock recovery`
  - `6.5.5 Các phương pháp kết hợp để giải quyết deadlock`
- `6.6 Bài tập`

These headings are recorded as outline evidence, not silently replaced by textbook headings.

## PAGE-BY-PAGE / RANGE MAP

Every physical page was inspected by text extraction and classified into the smallest stable semantic ranges below. Ranges are contiguous, gap-free, and cover pages 1–67 exactly. `CONTENT` remains `NOT_WRITTEN` because authoring has not started; `NON_CONTENT` is also `NOT_WRITTEN`.

| Pages | Class | Direct source heading / content | Source depth | V2 destination |
|---:|---|---|---|---|
| 1–3 | `NON_CONTENT` | Cover, objectives, contents | deck front matter | `None (Meta)` |
| 4–7 | `CONTENT` | 6.1.1 problem: semaphore interleaving and deadlock situation | direct slide text/example | `#1-coffman-rag` |
| 8–9 | `CONTENT` | 6.1.2 definition of deadlock and indefinite postponement | direct slide text | `#1-coffman-rag` |
| 10–12 | `CONTENT` | 6.1.3 four necessary Coffman conditions | direct slide text | `#1-coffman-rag` |
| 13–14 | `CONTENT` | 6.2 system model; resource types and instances | direct slide text | `#1-coffman-rag` |
| 15–17 | `CONTENT` | 6.2.1 RAG vertices, request/assignment edges, instances | direct slide text/diagram labels | `#1-coffman-rag` |
| 18–21 | `CONTENT` | 6.2.2 RAG examples: deadlock and cycle without deadlock | direct slide diagrams/examples | `#1-coffman-rag` |
| 22–24 | `CONTENT` | 6.2.3 cycle criteria, single/multiple instances, exercise 1 | direct slide text/exercise | `#1-coffman-rag` |
| 25–26 | `CONTENT` | 6.3 prevention/avoidance/detection/recovery overview | direct slide text | `#1-coffman-rag` |
| 27–31 | `CONTENT` | 6.3.1 prevention: mutual exclusion, hold-and-wait, no preemption, ordering | direct slide text | `#1-coffman-rag` |
| 32–33 | `CONTENT` | 6.3.2 avoidance and maximum-need declaration | direct slide text | `#2-banker` |
| 34–37 | `CONTENT` | safe/unsafe state and relation to deadlock | direct slide text/example | `#2-banker` |
| 38–40 | `CONTENT` | single-instance RAG avoidance and multiple-instance Banker | direct slide text | `#2-banker` |
| 41–44 | `CONTENT` | Banker data structures and Safety example at T0 | direct matrices/vectors | `#2-banker` |
| 45–49 | `CONTENT` | Resource-request algorithm and P1/P4 examples | direct matrices/vectors | `#2-banker` |
| 50–54 | `CONTENT` | detection, Wait-for graph, corresponding RAG, data structures | direct slide text/diagram | `#3-detection-recovery` |
| 55–58 | `CONTENT` | detection algorithm and Allocation/Request/Available example | direct matrices/vectors | `#3-detection-recovery` |
| 59–62 | `CONTENT` | recovery: termination, preemption, victim selection, rollback | direct slide text | `#3-detection-recovery` |
| 63 | `CONTENT` | Chapter 6 summary | direct slide summary | `#3-detection-recovery` |
| 64–66 | `CONTENT` | exercises 2–4: Need, Safe State, Banker requests/sequences | direct slide exercise | `#2-banker` |
| 67 | `NON_CONTENT` | discussion/end | deck end matter | `None (Meta)` |

**Coverage totals:** 67 physical pages = 63 `CONTENT` + 4 `NON_CONTENT`; no gaps, overlaps, or out-of-range pages.

## SOURCE-STRUCTURE CONFLICTS

`SRC-CH6-003` (MINOR, closed/documented): the outline numbers the conceptual sequence as 6.1–6.6, while the lecture deck numbers its corresponding material as 6.1.1–6.3.3 and places the system model after the initial problem/definition. The deck also does not expose a separate `6.5.5 Các phương pháp kết hợp...` heading. This is an organization/numbering difference, not evidence to invent missing content. Future authoring must preserve both labels in citations and must not silently claim that the outline and slide numbering are identical.

## CH5/CH6 BOUNDARY

Chapter 5 is locked at synchronization/liveness scope: deadlock appears as a synchronization failure mode alongside starvation and priority inversion. Chapter 6 is the formal deadlock unit supported by the inspected deck: necessary conditions, resource model, RAG/state analysis, prevention, avoidance/Banker, detection, and recovery. No Chapter 6 theory file was authored and no Chapter 6 material was inserted into Chapter 5.

## ALGORITHM / NUMERICAL LOCATORS

No answers were authored or solved. The following are source locators for later transcription:

| Algorithm/example | Locator | Evidence present |
|---|---:|---|
| Banker data structures (`Available`, `Max`, `Allocation`, `Need`) | p. 41 | direct slide table/text |
| Safety algorithm (`Work`, `Finish`, `Need ≤ Work`) | p. 42 | direct slide pseudocode |
| Safety example at `T0` | pp. 43–44 | Allocation/Max/Available/Need/Work tables |
| Resource-request conditions | pp. 45–46 | `Request ≤ Need`, `Request ≤ Available`, safe-state test |
| Resource-request examples | pp. 47–49 | P1 `(1,0,2)` and P4 `(3,3,0)`; safe-sequence decisions |
| Detection model/data | pp. 50–54 | Wait-for graph, Allocation/Request/Available |
| Detection algorithm | pp. 55–56 | Work/Finish/Allocation and deadlock condition |
| Detection example | pp. 57–58 | Allocation/Request/Available and P2 request |
| Recovery | pp. 59–62 | termination, preemption, victim selection, rollback |

## QBANK IDENTITY AND INVENTORY

The canonical DOCX has 582 XML paragraph elements and 560 non-empty paragraphs. The first eight non-empty content paragraphs after the two document headings are source question wording (definition, necessary conditions, RAG relationship, methods, busy-waiting critique, safe state, Banker algorithms, and recovery). They are not answers or handbook prose.

The remaining non-empty paragraphs form seven source exercise groups:

1. RAG graph deadlock identification (paragraphs 11–14).
2. Four-process RAG, deadlock decision, and safe sequences (15–22).
3. Five-process/multi-instance RAG and safe-sequence enumeration (23–26).
4. Four-resource Banker table, Need/Safety, and P1 request `(0,4,2,0)` (27–275).
5. Five-process R1–R4 Banker state and P3 request `(1,1,0,0)` (276–355).
6. Five-process A–D Banker table and P1/P4 requests (356–415).
7. Final A–D Banker table with Available `(3,3,2,1)` and safety/request questions (416–560).

The six structured Chapter 6 records in `research/data/official_review_questions.yaml` are mapped conceptual locators for future authoring; they remain `MAPPED` / `NOT_WRITTEN` and are not presented as a count of all DOCX paragraphs or exercise rows. Source wording and future handbook answers remain separate.

## EVIDENCE LIMITATIONS

- The binaries are available in the local supplied source corpus but are not committed into this handbook repository, consistent with the existing source-registry practice. Re-running binary checks requires passing the source-root explicitly to `scripts/validate_ch06_source_map.py`.
- Text extraction is used for deterministic page inspection; diagrams are retained as source evidence and are not re-solved in this mapping pass.
- The outline/slide numbering conflict is documented above; no unsupported `6.5.5` slide content is inferred.

## FINDINGS

- `SRC-CH6-001` — **RESOLVED** — canonical slide hash, byte size, and 67-page count match the inspected binary.
- `SRC-CH6-002` — **RESOLVED** — all 67 physical pages have explicit, contiguous semantic classifications (63 CONTENT, 4 NON_CONTENT).
- `SRC-CH6-003` — **CLOSED / MINOR** — outline-versus-slide numbering and the outline-only combined-methods heading are documented as a source-structure conflict.
- `SRC-CH6-004` — **RESOLVED** — canonical QBank hash, byte size, XML counts, eight theory prompts, and seven exercise groups are recorded without promoting any student/reference file.

**OPEN SOURCE BLOCKERS:** `0`  
**OPEN SOURCE MAJORS:** `0`  
**OPEN SOURCE MINORS:** `0`

## FINAL DECISION

**PASS — V2_BATCH3_CH6_SOURCE_MAP_READY_FOR_INDEPENDENT_CHECK**

The canonical Chapter 6 source map is ready for independent review. Chapter 6 authoring remains `NOT_STARTED`. The exact next action is an independent canonical Chapter 6 source-map review before any authoring.

Validation command used:

```text
python scripts/validate_ch06_source_map.py --source-root <local supplied IT007 source corpus>
```

No Chapter 6 content was authored, and no merge to `main` was performed.
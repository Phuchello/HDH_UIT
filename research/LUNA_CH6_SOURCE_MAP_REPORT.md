# LUNA CH6 SOURCE MAP REPORT (INDEPENDENT SOURCE-FIDELITY REPAIR)

**Scope:** Chapter 6 canonical source mapping only (no Chapter 6 authoring, no renderer/build changes).  
**Repository:** `Phuchello/HDH_UIT`  
**Branch:** `v2/complete-theory-labs`  
**Reviewed HEAD:** `24add9b3703472ace8869738e39991d3748f5305` (`fix(v2): repair chapter6 source fidelity map`)  
**Audit date:** 2026-09-03  
**Auditor / Role:** Codex Luna Ultra / Independent Source-Fidelity Auditor  
**Current Phase:** `V2_BATCH3_CH6_SOURCE_MAP_READY_FOR_FINAL_INDEPENDENT_CHECK`  
**Chapter 6 Source Mapping:** `MAPPED — PENDING FINAL INDEPENDENT CHECK`  
**Chapter 6 Authoring state:** `NOT_STARTED`  

---

## REVIEWED HEAD

The locked Chapters 1–5 baseline was inspected at the locked commit checkpoint `06e4b34ef14d60398e462e437470bb6a37157996` (`docs(v2): finalize chapter5 verified state`) and reviewed HEAD `24add9b`. Committed git history since `06e4b34` confirms ZERO changes to any Chapter 1–5 theory, question bank, or midterm review content files.

The only files modified by this final source-identity and CI gate repair are:
- `PROJECT_STATE.md`: Updated to `V2_BATCH3_CH6_SOURCE_MAP_READY_FOR_FINAL_INDEPENDENT_CHECK`.
- `content/sources/registry.yaml`: `#Week08-Chapter6 2024.pdf` promoted to canonical `UIT-SLIDE-CH06-2024`; `Week11-Chapter6 2024.pdf` demoted to immutable variant `UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB`.
- `research/data/source_verification.json`: Variant source ID synchronized.
- `.github/workflows/validate.yml`: Added `fetch-depth: 0` to checkout action to supply full committed history for locked-chapter checks.
- `scripts/validate_ch06_source_map.py`: Hardened with dual-mode validation (CI/Repository Mode vs Evidence Mode) and committed-history diff inspection against locked baseline `06e4b34`.
- `research/LUNA_CH6_SOURCE_MAP_REPORT.md`: This comprehensive independent repair report with complete audit history and resolutions.

---

## SOURCE BINARIES DISCOVERED

All source corpora in user attachment directories, local drive extractions, and OneDrive course archives were physically discovered, independently hashed, and verified.

| Classification | Source ID | Exact filename | Size (bytes) | Structural count | SHA-256 Digest | Status & Provenance |
|---|---|---|---:|---|---|---|
| `official_outline` | `UIT-OUTLINE-2024` | `IT007_HeDieuHanh_14.2024.pdf` | 418,490 | 19 PDF pages | `89547bca603d2486225f1e7c4f3ca767882964d83229ced16dc36b17eea309ab` | **Canonical 2024 Syllabus** (Created 2024-09-11 10:13:32+07:00 by Chi Dung, M365) |
| `source_variant` | `UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG` | `De cuong.pdf` | 452,857 | 19 PDF pages | `8ff13e4ddabee1fde580b84827e3e1c2733d2822ff9ca062d97e43a7f8151cdd` | **Older 2023 Variant** (Created 2023-03-29 by Chi Dung, Word 2019) |
| `official_slide` | `UIT-SLIDE-CH06-2024` | `#Week08-Chapter6 2024.pdf` | 6,008,743 | 67 PDF pages | `5cf9e1a31413a042ddc81c83ee6125d9718519d876a13f4dc30d3a5e041ee947` | **Canonical 2024 Slide** (Created 2024-09-11 10:37:41+07:00; official course material matching syllabus) |
| `source_variant` | `UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB` | `Week11-Chapter6 2024.pdf` | 5,816,540 | 67 PDF pages | `e55bf22554028859fc30747a39e72d97ca6e1e3c37e5a1bdcdc5ab94a7c3b56e` | **Older Semester Variant** (Created 2024-02-15 17:52:03+07:00; content-equivalent earlier export) |
| `official_qbank` | `UIT-QBANK-CH06-2024` | `Bai tap chuong 6 HDH.docx` | 101,550 | 582 XML paragraphs (560 non-empty) | `f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803` | **Canonical Tier-A Blank QBank** (15 source units: 8 theory + 7 exercises) |
| `source_variant` | `UIT-QBANK-CH06-2024-VARIANT-LOCAL-98KB` | `Bai tap chuong 6 HDH.docx` | 98,938 | 582 XML paragraphs | `6e701d3b3b7a7d7bba6bed10882c99d0a00cab14bae2e503c897e6b8abea39d4` | **Local 98.9KB Variant** (Located in OneDrive course folder) |
| `student_submission` | `UIT-QBANK-CH06-2024-VARIANT-STUDENT-23520237` | `Bai-tap-chuong-6-HDH.docx` | 873,751 | 1,092 XML paragraphs (1015 non-empty) | `a77ecee33dc2575c5bf8f0f98f69c4ac5ea885f8fbd04553812e9f9fa0368a38` | **Student Submission** (MSSV: 23520237 - Trần Hải Đăng; contains student answers) |
| `student_submission` | `UIT-REF-CH06-STUDENT-23521551-PDF` | `23521551-Bai tap chuong 6.pdf` | 8,823,935 | 5 PDF pages | `7b734530008dd0ac5a8ff9abeae1471aa08a236a09f67fb1c2a84b63b657de04` | **Student Submission** (MSSV: 23521551 - IT007.P19; photographed handwritten answers) |

---

## CANONICAL SOURCE IDENTITY

1. **Course Outline (`UIT-OUTLINE-2024`)**:
   - `IT007_HeDieuHanh_14.2024.pdf`, SHA-256 `89547bca603d2486225f1e7c4f3ca767882964d83229ced16dc36b17eea309ab`, 418,490 bytes, 19 pages.
   - Metadata confirms creation on 2024-09-11 10:13:32+07:00 for the 2024–2025 academic year.
   - Explicitly schedules: `Buổi 8: Chương 6. Deadlock` and instructs students to read `bộ slide week 8 do giáo viên cung cấp`.

2. **Lecture Deck (`UIT-SLIDE-CH06-2024`)**:
   - `#Week08-Chapter6 2024.pdf`, SHA-256 `5cf9e1a31413a042ddc81c83ee6125d9718519d876a13f4dc30d3a5e041ee947`, 6,008,743 bytes, 67 physical pages.
   - Metadata confirms creation on 2024-09-11 10:37:41+07:00 (exported 24 minutes after the syllabus) by PowerPoint for Microsoft 365, authored by Trần Hoàng Lộc & Nguyễn Thanh Thiện.
   - Distributed in official course materials folder `Tài liệu học tập-20240912`, matching the 2024 syllabus "week 8" designation.

3. **Official Question Bank (`UIT-QBANK-CH06-2024`)**:
   - `Bai tap chuong 6 HDH.docx`, SHA-256 `f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803`, 101,550 bytes, 582 XML paragraphs (560 non-empty).
   - Clean, official blank question bank containing 15 source units (8 theory questions + 7 structured numerical/graph exercises).

---

## EXCLUDED VARIANTS

The following 5 artifacts are cataloged with distinct immutable IDs and explicitly excluded from canonical coverage / Tier-A truth:

1. `UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG` (`De cuong.pdf`, 452,857 bytes, SHA `8ff13e4dd...`): Older 2023 curriculum syllabus (created 2023-03-29). Retained as an immutable variant for historical traceability.
2. `UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB` (`Week11-Chapter6 2024.pdf`, 5,816,540 bytes, SHA `e55bf2255...`): 67-page slide created 2024-02-15 17:52:03+07:00 with Week 11 numbering from the prior academic semester. Content-equivalent earlier export; demoted to variant.
3. `UIT-QBANK-CH06-2024-VARIANT-LOCAL-98KB` (`Bai tap chuong 6 HDH.docx`, 98,938 bytes, SHA `6e701d3b3...`): 98KB local DOCX in course folder.
4. `UIT-QBANK-CH06-2024-VARIANT-STUDENT-23520237` (`Bai-tap-chuong-6-HDH.docx`, 873,751 bytes, SHA `a77ecee33...`): DOCX completed by student Trần Hải Đăng (MSSV 23520237). Classified as `student_submission` (Tier B), never used as Tier-A truth.
5. `UIT-REF-CH06-STUDENT-23521551-PDF` (`23521551-Bai tap chuong 6.pdf`, 8,823,935 bytes, SHA `7b7345300...`): 5-page PDF of photographed handwritten solutions submitted by student 23521551 for class IT007.P19 (GV Phan Đình Duy). Classified as `student_submission` (Tier B), never used as Tier-A truth.

---

## COURSE OUTLINE ALIGNMENT

The authoritative 2024 UIT syllabus (`IT007_HeDieuHanh_14.2024.pdf`, page 5) specifies the following exact Chapter 6 lesson plan:

- **Chương 6. Deadlock**
  - **6.1 Định nghĩa**
  - **6.2 Mô hình hệ thống**
  - **6.3 Phương pháp giải quyết deadlock**
    - **6.3.1 Deadlock prevention**
    - **6.3.2 Deadlock avoidance**
    - **6.3.3 Deadlock detection**
    - **6.3.4 Deadlock recovery**
  - **6.4 Bài tập**

---

## PAGE-BY-PAGE / RANGE MAP

All 67 physical pages of canonical `#Week08-Chapter6 2024.pdf` are mapped into 21 contiguous, gap-free semantic ranges.  
`CONTENT` page count: **63**. `NON_CONTENT` page count: **4**.  
Every range is strictly `MAPPED` and `NOT_WRITTEN`.

| Pages | Class | Direct source heading / content | Source depth | V2 destination | Content status |
|---:|---|---|---|---|---|
| 1–3 | `NON_CONTENT` | Trang bìa, mục tiêu và nội dung buổi học | deck front matter | `None (Meta)` | `NOT_WRITTEN` |
| 4–7 | `CONTENT` | 6.1.1 Vấn đề deadlock: semaphore interleaving & tình huống deadlock | direct slide text | `#1-coffman-rag` | `NOT_WRITTEN` |
| 8–9 | `CONTENT` | 6.1.2 Định nghĩa deadlock và trì hoãn vô hạn định | direct slide text | `#1-coffman-rag` | `NOT_WRITTEN` |
| 10–12 | `CONTENT` | 6.1.3 Bốn điều kiện Coffman: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait | direct slide text | `#1-coffman-rag` | `NOT_WRITTEN` |
| 13–14 | `CONTENT` | 6.2 Mô hình hóa hệ thống: loại tài nguyên và số thực thể | direct slide text | `#1-coffman-rag` | `NOT_WRITTEN` |
| 15–17 | `CONTENT` | 6.2.1 Đồ thị cấp phát tài nguyên RAG: đỉnh, cạnh và ký hiệu thực thể | direct slide diagram | `#1-coffman-rag` | `NOT_WRITTEN` |
| 18–21 | `CONTENT` | 6.2.2 Các ví dụ RAG: đồ thị có deadlock và chu trình không deadlock | direct slide diagram | `#1-coffman-rag` | `NOT_WRITTEN` |
| 22–24 | `CONTENT` | 6.2.3 RAG và deadlock: single/multiple instances, tiêu chí chu trình và Bài tập 1 | direct slide exercise | `#1-coffman-rag` | `NOT_WRITTEN` |
| 25–26 | `CONTENT` | 6.3 Phương pháp giải quyết deadlock: prevention, avoidance, detection, recovery | direct slide text | `#1-coffman-rag` | `NOT_WRITTEN` |
| 27–31 | `CONTENT` | 6.3.1 Ngăn deadlock (Prevention): phá vỡ 4 điều kiện Coffman | direct slide text | `#1-coffman-rag` | `NOT_WRITTEN` |
| 32–33 | `CONTENT` | 6.3.2 Tránh deadlock (Avoidance): yêu cầu thông tin Max và cấp phát an toàn | direct slide text | `#2-banker` | `NOT_WRITTEN` |
| 34–37 | `CONTENT` | 6.3.2.1–6.3.2.2 Trạng thái Safe / Unsafe và mối quan hệ với Deadlock | direct slide text | `#2-banker` | `NOT_WRITTEN` |
| 38–40 | `CONTENT` | 6.3.2.3 Các giải thuật tránh deadlock: RAG single-instance & Banker multiple-instance | direct slide text | `#2-banker` | `NOT_WRITTEN` |
| 41–44 | `CONTENT` | Banker Safety: Cấu trúc dữ liệu Available, Max, Allocation, Need, Work, Finish và ví dụ T0 | direct table/matrix | `#2-banker` | `NOT_WRITTEN` |
| 45–49 | `CONTENT` | Banker Resource-request: 3 bước kiểm tra Request ≤ Need, Request ≤ Available và ví dụ P1/P4 | direct table/matrix | `#2-banker` | `NOT_WRITTEN` |
| 50–54 | `CONTENT` | 6.3.3 Detection: Wait-for graph (single-instance) và cấu trúc Available/Allocation/Request | direct diagram/text | `#3-detection-recovery` | `NOT_WRITTEN` |
| 55–58 | `CONTENT` | 6.3.3.1 Detection algorithm cho đa thực thể và ví dụ P2 request | direct table/matrix | `#3-detection-recovery` | `NOT_WRITTEN` |
| 59–62 | `CONTENT` | 6.3.3.2 Recovery: Termination (chấm dứt tiến trình) và Preemption (lấy lại tài nguyên, rollback, starvation) | direct slide text | `#3-detection-recovery` | `NOT_WRITTEN` |
| 63 | `CONTENT` | Tóm tắt lại nội dung buổi học | direct slide summary | `#3-detection-recovery` | `NOT_WRITTEN` |
| 64–66 | `CONTENT` | 6.4 Bài tập 2–4: Need, Safe State, Banker requests và chuỗi an toàn | direct slide exercise | `#2-banker` | `NOT_WRITTEN` |
| 67 | `NON_CONTENT` | Thảo luận / kết thúc | deck end matter | `None (Meta)` | `NOT_WRITTEN` |

---

## VISUAL AND STRUCTURAL PAGE INSPECTION (SRC-CH6-008)

Visual rendering and structural element inspection (vector curves, lines, bounding boxes, matrix tables) were performed across all diagram-heavy, matrix-heavy, and exercise pages:

1. **RAG / Graph Pages (Pages 15–24)**:
   - **Page 15**: Section header `MÔ HÌNH HÓA HỆ THỐNG / 6.2.1. Đồ thị cấp phát tài nguyên RAG`.
   - **Page 16**: Graph definition $G = (V, E)$. Vertices $V = P \cup R$ ($P = \{P_1, \dots, P_n\}$ processes, $R = \{R_1, \dots, R_m\}$ resources). Edges $E$: Request edge directed from Process $P_i \to R_j$; Assignment edge directed from Resource $R_j \to P_i$.
   - **Page 17**: Visual convention diagram: Process $P_i$ represented by circle; Resource $R_j$ represented by rectangle containing dots (instances). Vector curves verify: $P_i \to R_j$ points to the rectangle boundary; $R_j \to P_i$ originates from an individual dot inside the rectangle to the process circle.
   - **Page 19**: 3 processes ($P_1, P_2, P_3$), 4 resources ($R_1(1), R_2(2), R_3(1), R_4(4)$). State: $P_1$ holds 1 $R_2$, requests 1 $R_1$; $P_2$ holds 1 $R_1, 1 R_2$, requests 1 $R_3$; $P_3$ holds 1 $R_3$. Visual inspection confirms **directed acyclic graph** (no cycle, no deadlock).
   - **Page 20**: Deadlock RAG: $P_3$ requests 1 $R_2$. Visual inspection reveals two cycles:
     - Cycle 1: $P_1 \to R_1 \to P_2 \to R_3 \to P_3 \to R_2 \to P_1$.
     - Cycle 2: $P_2 \to R_3 \to P_3 \to R_2 \to P_2$.
     All instances of $R_1, R_2, R_3$ are exhausted; deadlock occurs for $\{P_1, P_2, P_3\}$.
   - **Page 21**: Cycle without Deadlock RAG: 4 processes ($P_1..P_4$), 2 resources ($R_1(2), R_2(2)$). Visual inspection confirms cycle $P_1 \to R_1 \to P_3 \to R_2 \to P_1$, but $P_2$ holds $R_1$ and $P_4$ holds $R_2$ without requesting any further resources. Once $P_2$ or $P_4$ terminates, cycle is broken. No deadlock!
   - **Page 23**: Summary theorems: No cycle implies No deadlock; Cycle with single instances implies Deadlock; Cycle with multiple instances implies Possibility of deadlock.
   - **Page 24**: Bài tập 1: 4 processes ($P_1..P_4$), 3 resources ($R_1(3), R_2(2), R_3(2)$). Exact matching with QBank Exercise 2 (P17–P25).

2. **Safe-State & Banker Tables (Pages 34–49)**:
   - **Pages 34–36**: 12 file single-resource system with $P_0, P_1, P_2$. Max: $(10, 4, 9)$, Allocation: $(5, 2, 2)$, Need: $(5, 2, 7)$, Available $= 3$. Safe sequence $\langle P_1, P_0, P_2 \rangle$. Page 36 shows $P_2$ requesting 1 file $\to$ Available $= 2$, unsafe state.
   - **Page 37**: Euler diagram: Safe $\subset$ Unsafe; Deadlock $\subset$ Unsafe. Avoidance ensures system never enters Unsafe.
   - **Pages 41–44**: Banker Data Structures and Safety Algorithm:
     - Vectors & Matrices: Available[$m$], Max[$n \times m$], Allocation[$n \times m$], Need[$n \times m$] = Max - Allocation.
     - Safety trace table at $T_0$: 5 processes ($P_0..P_4$), resources $A(10), B(5), C(7)$.
     - Initial Available: $(3, 3, 2)$.
     - Traced Work progression: $(3,3,2) \xrightarrow{+P_1} (5,3,2) \xrightarrow{+P_3} (7,4,3) \xrightarrow{+P_4} (7,4,5) \xrightarrow{+P_0} (7,5,5) \xrightarrow{+P_2} (10,5,7)$. Safe sequence $\langle P_1, P_3, P_4, P_0, P_2 \rangle$.
   - **Pages 45–49**: Resource-Request Algorithm:
     - Condition 1: Request$_i \le$ Need$_i$.
     - Condition 2: Request$_i \le$ Available.
     - Tentative allocation: Available $\leftarrow$ Available - Request$_i$, Allocation$_i \leftarrow$ Allocation$_i$ + Request$_i$, Need$_i \leftarrow$ Need$_i$ - Request$_i$.
     - Page 47–48: $P_1$ requests $(1, 0, 2)$: Valid, tentative state is Safe ($\langle P_1, P_3, P_4, P_0, P_2 \rangle$) implies Granted.
     - Page 49: $P_4$ requests $(3, 3, 0)$: Request$_4 \le$ Available $(3,3,2)$ holds, but tentative Available becomes $(0, 0, 2)$; no process can satisfy Need implies Unsafe state implies $P_4$ must wait!

3. **Wait-For & Detection Graph Pages (Pages 50–58)**:
   - **Page 52**: Wait-for graph for single-instance resources: nodes are processes; directed edge $P_i \to P_j$ means $P_i$ is waiting for $P_j$ to release a resource. Cycle detection runs in $O(n^2)$.
   - **Page 53**: Side-by-side visual diagram: Resource-Allocation Graph vs. Corresponding Wait-for Graph. Resource nodes are collapsed into direct process-to-process dependency edges.
   - **Pages 54–56**: Detection Algorithm for Multiple Instances: Available[$m$], Allocation[$n \times m$], Request[$n \times m$]. Algorithm initializes Finish[$i$] = false if Allocation$_i \ne 0$, else true. Complexity $O(m \cdot n^2)$.
   - **Page 57**: Detection example at $T_0$: $P_0..P_4$, resources $A(7), B(2), C(6)$. Allocation = $[(0,1,0), (2,0,0), (3,0,3), (2,1,1), (0,0,2)]$; Request = $[(0,0,0), (2,0,2), (0,0,0), (1,0,0), (0,0,2)]$; Available = $(0, 0, 0)$. Execution sequence $\langle P_0, P_2, P_3, P_1, P_4 \rangle$ finishes all processes implies No Deadlock.
   - **Page 58**: $P_2$ requests $(0, 0, 1)$: Request[$P_2$] becomes $(0, 0, 1)$. Only $P_0$ can run; after $P_0$ finishes, Work = $(0, 1, 0)$. No other process has Request $\le$ Work implies Deadlock detected for set $\{P_1, P_2, P_3, P_4\}$!

4. **Exercise Pages (Pages 64–66)**:
   - **Page 64 (Bài tập 2)**: Need matrix, Safety test, P1 request $(0,4,2,0)$. Matches QBank Exercise 4 (P31–P370).
   - **Page 65 (Bài tập 3)**: Banker check with Available $(0,3,0,1)$ and $(1,0,0,2)$. Matches QBank Exercise 6 (P449–P508).
   - **Page 66 (Bài tập 4)**: Banker check: Safe state, P1 request $(1,1,0,0)$, P4 request $(0,0,2,0)$. Matches QBank Exercise 7 (P509–P582).

---

## SOURCE-STRUCTURE CONFLICTS

Three distinct structural models exist across the discovered source documents:

1. **Authoritative 2024 Syllabus (`IT007_HeDieuHanh_14.2024.pdf`)**:
   - `6.1 Định nghĩa`
   - `6.2 Mô hình hệ thống`
   - `6.3 Phương pháp giải quyết deadlock`
     - `6.3.1 Deadlock prevention`
     - `6.3.2 Deadlock avoidance`
     - `6.3.3 Deadlock detection`
     - `6.3.4 Deadlock recovery`
   - `6.4 Bài tập`

2. **Canonical 2024 Lecture Deck (`#Week08-Chapter6 2024.pdf`)**:
   - `6.1 Vấn đề deadlock` (6.1.1 Khái niệm, 6.1.2 Định nghĩa, 6.1.3 Bốn điều kiện Coffman)
   - `6.2 Mô hình hóa hệ thống` (6.2.1 Đồ thị RAG, 6.2.2 Ví dụ, 6.2.3 RAG và deadlock, Bài tập 1)
   - `6.3 Phương pháp giải quyết deadlock`:
     - `6.3.1 Ngăn deadlock (Prevention)`
     - `6.3.2 Tránh deadlock (Avoidance)`
     - `6.3.3 Phát hiện deadlock (Detection)`: Includes `6.3.3.1 Giải thuật phát hiện` and `6.3.3.2 Phục hồi deadlock (Recovery)` nested together.
   - Exercises appear at slide 24 (Bài tập 1) and slides 64–66 (Bài tập 2–4).

3. **Older 2023 Outline Variant (`De cuong.pdf`)**:
   - Numbered 6.1 through 6.6 with RAG as 6.4, combined recovery as 6.5.5, and System Model placed before Definition.

**Resolution Policy:** Future Chapter 6 theory authoring will use clear, concept-based section headings aligned with the canonical 2024 outline, keeping numbering distinctions transparently documented without conflation.

---

## CH5/CH6 BOUNDARY

- **Chapter 5 (Synchronization)** covers Process Synchronization, Critical Sections, Peterson's algorithm, Hardware atomic instructions (`SELF_STUDY`), Mutexes, Semaphores, Monitors, and introduces Deadlock only as a synchronization/liveness failure phenomenon alongside starvation and priority inversion.
- **Chapter 6 (Deadlock)** is strictly self-contained: it formally defines Coffman's 4 conditions, RAG, Deadlock Prevention, Avoidance (Banker algorithm), Detection (Wait-for graph & multi-instance matrix algorithm), and Recovery.
- Zero premature Chapter 6 concepts (Coffman, Banker, RAG, Safety algorithm) exist in Chapter 5.
- Zero Chapter 6 authoring files (`content/theory/ch06-deadlock.md`, `content/questions/subjective/ch06.md`) exist at this phase.

---

## ALGORITHM / NUMERICAL LOCATORS

| Algorithm / Problem | Slide Locator | QBank Locator | Mathematical Objects & Parameters |
|---|---:|---|---|
| RAG Deadlock Analysis | pp. 15–24 | Bài tập 1 & 2 (P12–P25) | $V = P \cup R$, Request $P_i \to R_j$, Assignment $R_j \to P_i$ |
| Banker Safety Algorithm | pp. 41–44 | Câu 7 (P10), Bài tập 4–7 | Work = Available, Finish[$i$] = false, Need$_i \le$ Work |
| Banker Resource-Request | pp. 45–49 | Câu 7 (P10), Bài tập 4–7 | Request$_i \le$ Need$_i$, Request$_i \le$ Available, Tentative state test |
| Deadlock Detection (Wait-for) | pp. 50–53 | Câu 7 (P10) | Single-instance cycle detection $O(n^2)$ |
| Deadlock Detection (Matrix) | pp. 54–58 | Câu 7 (P10) | Finish[$i$] = (Allocation$_i$ == 0), Request$_i \le$ Work, $O(m \cdot n^2)$ |
| Deadlock Recovery | pp. 59–62 | Câu 8 (P11) | Process termination criteria, resource preemption, victim selection, rollback, starvation |

---

## QBANK IDENTITY AND INVENTORY

Canonical binary `Bai tap chuong 6 HDH.docx` (101,550 bytes, SHA `f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803`) contains **15 addressable source units**:

### 8 Theory Questions (P4–P11)
1. `QBANK-CH06-01` (P4): Định nghĩa Deadlock.
2. `QBANK-CH06-02` (P5): 4 điều kiện Coffman dẫn đến Deadlock.
3. `QBANK-CH06-03` (P6): Đồ thị cấp phát tài nguyên (RAG) và mối liên hệ với Deadlock.
4. `QBANK-CH06-04` (P7): Các phương pháp giải quyết Deadlock và phân tích ưu nhược điểm.
5. `QBANK-CH06-05` (P8): Phân tích ưu nhược điểm các giải pháp đồng bộ busy waiting (phần cứng và phần mềm).
6. `QBANK-CH06-06` (P9): Khái niệm trạng thái an toàn (Safe State) và mối liên hệ với Deadlock.
7. `QBANK-CH06-07` (P10): Mô tả các giải thuật Banker: Safety, Resource-Request, Detection.
8. `QBANK-CH06-08` (P11): Các giải pháp phục hồi hệ thống sau khi phát hiện Deadlock.

### 7 Structured Exercises (P12–P582)
9. `QBANK-CH06-09` (P12–P16): Xác định Deadlock trên đồ thị cấp phát tài nguyên mẫu (a) và (b).
10. `QBANK-CH06-10` (P17–P25): Vẽ RAG, kiểm tra Deadlock và tìm chuỗi an toàn cho hệ 4 tiến trình, 3 tài nguyên (3,2,2).
11. `QBANK-CH06-11` (P26–P30): Vẽ RAG, đếm và liệt kê tất cả chuỗi an toàn cho hệ 5 tiến trình, 3 tài nguyên (3,3,2).
12. `QBANK-CH06-12` (P31–P370): Giải thuật Banker mẫu: tính ma trận Need, giải thuật an toàn và xử lý yêu cầu P1(0,4,2,0).
13. `QBANK-CH06-13` (P371–P448): Giải thuật Banker: tìm chuỗi an toàn tại t0 và xử lý yêu cầu P3(1,1,0,0) tại t1.
14. `QBANK-CH06-14` (P449–P508): Giải thuật Banker kiểm tra an toàn với 2 vector Available khác nhau (0,3,0,1) và (1,0,0,2).
15. `QBANK-CH06-15` (P509–P582): Giải thuật Banker toàn diện: kiểm tra an toàn, xử lý yêu cầu P1(1,1,0,0) và P4(0,0,2,0).

All 15 units are cataloged in `research/data/official_review_questions.yaml` as `MAPPED` and `NOT_WRITTEN`.

---

## EVIDENCE LIMITATIONS

1. Binaries reside in external/local course corpora (`Downloads` and `OneDrive`) and are not committed into this git repository, strictly following repository hygiene policies.
2. The validator supports two modes: CI/Repository Mode (verifying metadata, structural invariants, and committed locked-file diffs) and Evidence Mode (`--source-root`, performing direct physical re-hashing of external binary files).
3. Visual rendering confirmed diagram and table topologies; exercises will be transcribed and solved only during the authoring phase.
4. Student files (`Bai-tap-chuong-6-HDH.docx` by MSSV 23520237 and `23521551-Bai tap chuong 6.pdf`) are cataloged as reference/submission variants and are never used as canonical truth.

---

## FINDINGS

- `SRC-CH6-001` — **RESOLVED**: Canonical slide hash, byte size, and 67-page count match the inspected binary.
- `SRC-CH6-002` — **RESOLVED**: All 67 physical pages have explicit, contiguous semantic classifications (63 CONTENT, 4 NON_CONTENT).
- `SRC-CH6-003` — **CLOSED / MINOR**: Outline-versus-slide numbering differences transparently documented.
- `SRC-CH6-004` — **RESOLVED**: Canonical QBank hash, byte size, and XML paragraph count verified.
- `SRC-CH6-005` — **RESOLVED (BLOCKER)**: Course-outline binary conflict resolved. Authoritative user-provided syllabus `IT007_HeDieuHanh_14.2024.pdf` (SHA-256 `89547bca...`) established as canonical `UIT-OUTLINE-2024`. Older `De cuong.pdf` (SHA-256 `8ff13e4d...`) registered as variant `UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG`.
- `SRC-CH6-006` — **RESOLVED (MAJOR)**: Missing user-supplied Chapter 6 variants discovered and cataloged: `23521551-Bai tap chuong 6.pdf` (`UIT-REF-CH06-STUDENT-23521551-PDF`) and `Bai-tap-chuong-6-HDH.docx` (`UIT-QBANK-CH06-2024-VARIANT-STUDENT-23520237`). Both classified as `student_submission` (Tier B), separated from canonical sources.
- `SRC-CH6-007` — **RESOLVED (MAJOR)**: QBank source-unit map expanded from 6 to the complete 15 addressable units (`QBANK-CH06-01` through `QBANK-CH06-15`) in `research/data/official_review_questions.yaml`. All are marked `MAPPED` / `NOT_WRITTEN`.
- `SRC-CH6-008` — **RESOLVED (MAJOR)**: Visual page inspection completed for graph pages (15–24), Banker tables (34–49), Wait-for/detection pages (50–58), and exercise pages (64–66). Graph directions, resource dots, cycles, and matrix headers verified.
- `SRC-CH6-009` — **RESOLVED (MAJOR)**: Week08 vs Week11 canonical slide identity investigated and resolved with direct physical lineage analysis:
  - Binary comparison between `#Week08-Chapter6 2024.pdf` (6,008,743 bytes, SHA-256 `5cf9e1a3...`) and `Week11-Chapter6 2024.pdf` (5,816,540 bytes, SHA-256 `e55bf225...`):
    - Metadata reveals `#Week08` was created on 2024-09-11 10:37:41+07:00 (PowerPoint Microsoft 365, authors Trần Hoàng Lộc & Nguyễn Thanh Thiện) in the official course folder `Tài liệu học tập-20240912`.
    - In contrast, `Week11` was created 7 months earlier on 2024-02-15 17:52:03+07:00 with Week 11 numbering from the prior semester.
    - Authoritative 2024 course outline (`IT007_HeDieuHanh_14.2024.pdf`, created 2024-09-11 10:13:32+07:00) explicitly dictates: `Buổi 8: Chương 6. Deadlock` and `bộ slide week 8 do giáo viên cung cấp`.
    - Deep page-by-page text and element analysis across all 67 pages confirms both PDFs are content-equivalent (identical headings, definitions, Coffman conditions, RAG models, Banker tables, detection algorithms, and exercises; differences are restricted to Unicode normalization NFC vs NFD and letter-spacing).
    - Resolution: Promoted `#Week08-Chapter6 2024.pdf` to canonical `UIT-SLIDE-CH06-2024`; demoted `Week11-Chapter6 2024.pdf` to immutable variant `UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB`. Canonical 67-page semantic range map is verified and preserved.
- `ENG-CH6-001` — **RESOLVED (MAJOR)**: False-positive locked-chapter CI guard resolved:
  - Root cause: `scripts/validate_ch06_source_map.py` previously called `git diff --name-only` against the working tree, which was dirtied by transient test artifacts generated by preceding test suites in GitHub Actions CI run #44.
  - Fix: Hardened validator to inspect committed git history between the locked Chapter 5 baseline commit `06e4b34ef14d60398e462e437470bb6a37157996` and `HEAD` (`git diff --name-only 06e4b34..HEAD --`), strictly filtering for locked paths (`content/theory/ch01*..ch05*`, `content/questions/subjective/ch01*..ch05*`, `content/reviews/midterm*`).
  - Added `fetch-depth: 0` to `.github/workflows/validate.yml` to guarantee complete commit history is available in CI.
  - Verification: `git diff --name-only 06e4b34..HEAD` contains ZERO modified files under Chapters 1–5.
- `SRC-CH6-010` — **RESOLVED (MAJOR)**: Canonical coverage identity SSOT sync:
  - Reason: Canonical source promotion (Week11 -> Week08) in `SRC-CH6-009` updated `content/sources/registry.yaml` and the report, but left `research/data/slide_coverage.yaml` exact_filename pointing at the demoted `Week11-Chapter6 2024.pdf` variant.
  - Resolution: Synchronized `research/data/slide_coverage.yaml` under `UIT-SLIDE-CH06-2024` to `#Week08-Chapter6 2024.pdf`. Hardened `scripts/validate_ch06_source_map.py` to assert strict SSOT equality between `slide_coverage.yaml` and `registry.yaml` (`coverage.exact_filename == registry[SLIDE_ID].exact_filename` and `coverage.physical_pages == registry[SLIDE_ID].page_count`).

**OPEN SOURCE BLOCKERS:** `0`  
**OPEN SOURCE MAJORS:** `0`  
**OPEN ENGINEERING MAJORS:** `0`  
**OPEN MINORS:** `0`  

---

## FINAL DECISION

**PASS — V2_BATCH3_CH6_SOURCE_MAP_READY_FOR_FINAL_INDEPENDENT_CHECK**

The canonical Chapter 6 source map is fully verified, with Week08 established as canonical slide, Week11 demoted to variant, dual-mode validation enabled, and CI locked-chapter protection repaired.  
Chapter 6 authoring remains **`NOT_STARTED`**.  
**READY FOR CH6 AUTHORING:** **`NO`** (Pending final independent check).  
**Exact Next Action:** Push repair and verify exact-head GitHub Actions before authoring.
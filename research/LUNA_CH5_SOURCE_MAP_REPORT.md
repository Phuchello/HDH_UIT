# BÁO CÁO ĐỐI SOÁT NGUỒN CHÍNH TẮC CHƯƠNG 5 (LUNA CH5 SOURCE MAP REPORT)

**Thời gian lập:** 2026-08-31  
**Người thực hiện:** Luna Academic Reviewer / Source Fidelity Specialist  
**Nhánh Git:** `v2/complete-theory-labs`  
**Giai đoạn:** `V2_BATCH2_CH5_SOURCE_MAP_READY_FOR_INDEPENDENT_CHECK`  
**Trạng thái Lập bản đồ nguồn:** `COMPLETE — PENDING INDEPENDENT CHECK`  
**Trạng thái Soạn thảo lý thuyết:** `NOT_STARTED`  
**SẴN SÀNG SOẠN THẢO CHƯƠNG 5 (READY FOR CH5 AUTHORING):** **`NO`** *(Đang chờ thẩm định độc lập)*  

---

## 1. Mục Đích Báo Cáo (Objective)

Báo cáo đối soát chi tiết bản đồ nguồn chính tắc (Canonical Source Map) ở cấp độ phân đoạn chính xác (precision range signature) cho **Chương 5: Đồng bộ Tiến trình (Process Synchronization)** trước khi bước vào giai đoạn soạn thảo lý thuyết và ngân hàng câu hỏi.

---

## 2. Bảng Nguồn Slide Chính Tắc Chương 5 (Canonical Slide Corpus)

| Phân Đoạn Slide | Tên Tệp Chính Tắc | Mã Băm SHA-256 | Số Trang Vật Lý | Phân Bổ Nội Dung | Trạng Thái Đăng Ký |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Chương 5 - Phần 1** | `#Week06-Chapter5-1 2024.pdf` | `2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416` | **67** | **63 CONTENT + 4 NON_CONTENT** | `UIT-SLIDE-CH05-1-2024` (official_slide) |
| **Chương 5 - Phần 2** | `#Week07-Chapter5-2 2024.pdf` | `f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2` | **72** | **68 CONTENT + 4 NON_CONTENT** | `UIT-SLIDE-CH05-2-2024` (official_slide) |

---

## 3. Khớp Nối Đề Cương Môn Học (Course Outline Alignment)

So sánh giữa Đề cương chi tiết môn học IT007 và Slide bài giảng chính thức 2024:

| Đề mục Đề cương IT007 | Đề mục Slide Bài giảng 2024 | Ghi chú Khớp nối |
| :--- | :--- | :--- |
| **5.1 Bối cảnh** | 5.1 Bối cảnh & 5.2 Khái niệm Race Condition | Trùng khớp hoàn toàn (Producer/Consumer, PID race, Race Condition) |
| **5.2 Vấn đề Miền găng** | 5.2 Vấn đề Miền găng & 5.3 Các yêu cầu giải pháp | Trùng khớp hoàn toàn (Critical Section, Mutual Exclusion, Progress, Bounded Waiting) |
| **5.3 Các giải pháp phần mềm** | 5.4 Các giải pháp phần mềm & 5.4.3 Peterson | Trùng khớp hoàn toàn (Giải pháp 1, Giải pháp 2, Giải pháp Peterson, kiến trúc hiện đại) |
| **5.4 Các giải pháp phần cứng** | 5.5 Các hỗ trợ từ phần cứng | Trùng khớp (Memory Barrier, test_and_set, compare_and_swap, atomic variables) |
| **5.5 Mutex Locks** | 5.6 Mutex Locks | Trùng khớp hoàn toàn (Acquire/Release, Spinlock vs Non-busy waiting) |
| **5.6 Semaphore** | 5.7 Semaphore | Trùng khớp hoàn toàn (Counting, Binary, Hiện thực Block/Wakeup, Ứng dụng) |
| **5.7 Monitor** | 5.8 Monitor | Trùng khớp hoàn toàn (Cấu trúc Monitor, Biến điều kiện Condition Variables) |
| **5.8 Liveness** | 5.9 Liveness | Trùng khớp (Định nghĩa Liveness, Chờ vô hạn, Bế tắc Deadlock) |
| **5.10 Một số bài toán kinh điển** | 5.10 Bounded-Buffer, 5.11 Readers-Writers, 5.12 Dining-Philosophers | Trùng khớp nội dung bài toán (xem chi tiết xung đột cấu trúc bên dưới) |
| **5.11 Bài tập** | Slide tóm tắt & Bộ bài tập `UIT-QBANK-CH05-2024` | 18 bài tập lý thuyết và bài toán đồng bộ thực hành |

---

## 4. Ghi Nhận Xung Đột Cấu Trúc Nguồn (SOURCE_STRUCTURE_CONFLICT)

Trong quá trình đối soát, hai xung đột cấu trúc độc lập được ghi nhận và giải quyết rõ ràng:

### Xung Đột 1: Xung đột Đánh số & Tổ chức Đề mục (Course Outline vs Canonical Slides)
- **Đề cương môn học IT007:**
  - `5.10` Một số bài toán đồng bộ kinh điển:
    - `5.10.1` Bounded-Buffer (Producer-Consumer)
    - `5.10.2` Readers-Writers
    - `5.10.3` Dining-Philosophers
  - `5.11` Bài tập
- **Slide bài giảng chính thức 2024:**
  - `5.10` Bài toán đồng bộ Bounded-Buffer
  - `5.11` Bài toán đồng bộ Readers-Writers
  - `5.12` Bài toán đồng bộ Dining-Philosophers
- **Đánh giá & Nguyên tắc xử lý:**
  - Phân loại: `SOURCE_STRUCTURE_CONFLICT` (Xung đột tổ chức/đánh số đề mục, không mâu thuẫn về mặt khái niệm khoa học).
  - Nguyên tắc soạn thảo: Văn phong cẩm nang chính tắc sẽ bám sát **tên khái niệm và bản chất thuật toán** (Bounded-Buffer, Readers-Writers, Dining-Philosophers), không phụ thuộc cứng nhắc vào số hiệu tiểu mục.

### Xung Đột 2: Xung đột Phân tách Tệp Nguồn Biến thể (2-Part Canonical vs 3-Part Variant)
- **Kho biến thể cục bộ cũ:** Tồn tại bộ 3 phần (`Week07-Chapter5-1` 58 trang, `Week09-Chapter5-2` 55 trang, `Week10-Chapter5-3` 32 trang).
- **Quyết định giải quyết:**
  - Bộ 3 phần cũ được phân loại là `source_variant` trong [`content/sources/registry.yaml`](content/sources/registry.yaml) và **LOẠI BỎ HOÀN TOÀN** khỏi danh sách `decks` chính tắc trong [`research/data/slide_coverage.yaml`](research/data/slide_coverage.yaml).
  - Bản đồ nguồn chính tắc khóa chặt theo bộ 2 phần chính thức của giảng viên (`#Week06-Chapter5-1 2024.pdf` 67 trang và `#Week07-Chapter5-2 2024.pdf` 72 trang).

---

## 5. Thẩm Định Nguồn Ngân Hàng Câu Hỏi (QBank Provenance Audit)

- **Mã định danh nguồn:** `UIT-QBANK-CH05-2024`
- **Tên tệp gốc vật lý:** `Bai tap chuong 5 HDH.docx`
- **Kích thước tệp:** 56,369 bytes
- **Mã băm SHA-256:** `503cd8fdb619bcfd664cfaa198915bc50d0ba6bb910c74d14ccff5252e646186`
- **Tác giả / Nguồn:** Khoa KTMT - Trường ĐH Công nghệ Thông tin (UIT)
- **Kiểm định cấu trúc đoạn trích xuất:**
  - Số đoạn XML (`extracted_paragraph_count`): **129 đoạn** (bao gồm tiêu đề).
  - Số câu hỏi / bài tập cấu trúc thực tế (`verified_question_count`): **18 mục câu hỏi độc lập**, gồm:
    - **9 câu hỏi lý thuyết ngắn** (Đoạn 3–11): Tranh chấp, Miền găng, 3 yêu cầu giải pháp, Giải pháp ngắt, Giải pháp phần cứng, Mutex lock, Semaphore, Monitor, Đặc điểm bài toán kinh điển.
    - **9 bài tập cấu trúc & giải thuật đồng bộ** (Đoạn 12–129):
      1. *Bài tập 1 (Đoạn 12–35):* Giải thuật Dekker & chứng minh 3 yêu cầu.
      2. *Bài tập 2 (Đoạn 36–46):* Biến thể giải thuật Peterson (turn & flag).
      3. *Bài tập 3 (Đoạn 47–56):* Chỉ thị hoán đổi nguyên tử Swap.
      4. *Bài tập 4 (Đoạn 57–62):* Đồng bộ 2 tiến trình A & B với counting semaphore ($n_b < n_a \le n_b + 3$).
      5. *Bài tập 5 (Đoạn 63–107):* Đồ thị phụ thuộc 4 tiểu trình $T_1, T_2, T_3, T_4$ và nghiệm semaphore.
      6. *Bài tập 6 (Đoạn 108–113):* Biến chia sẻ $X$ tăng đến 20 và hiện tượng race condition.
      7. *Bài tập 7 (Đoạn 114–117):* Rào chắn đồng bộ Barrier cho $P_1 \{A_1; A_2\}$ và $P_2 \{B_1; B_2\}$.
      8. *Bài tập 8 (Đoạn 118–121):* Tổng quát hóa Barrier cho vòng lặp 100 bước.
      9. *Bài tập 9 (Đoạn 122–129):* Cây biểu thức số học song hành và lập lịch semaphore.
- **Quy tắc phân biệt định lượng:**
  $$\text{extracted\_paragraph\_count (128–129)} \neq \text{verified\_question\_count (18)}$$
- **Trạng thái nội dung:** Câu hỏi được lập hồ sơ cấu trúc; **chưa soạn thảo đáp án** trong giai đoạn này.

---

## 6. Bản Đồ Phân Đoạn Chính Xác (Canonical Content Topics & Signatures)

### Phần 1: `#Week06-Chapter5-1 2024.pdf` (67 trang vật lý: 63 CONTENT + 4 NON_CONTENT)

1. `1-3` (3 trang, NON_CONTENT): Trang bìa, mục tiêu & nội dung Phần 1.
2. `4-11` (8 trang, CONTENT): **5.1.1** Producer vs Consumer (shared count, interleaving, lost/inconsistent update motivation).
3. `12-13` (2 trang, CONTENT): **5.1.2** PID allocation race (fork, next_available_pid).
4. `14-16` (3 trang, CONTENT): **5.1.3** Race Condition (definition, shared data, execution-order dependence, inconsistency, need for synchronization).
5. `17-19` (3 trang, CONTENT): **5.2** Critical Section Problem (critical section, entry, exit, remainder).
6. `20-25` (6 trang, CONTENT): **5.3.1** Requirements (Mutual Exclusion, Progress, Bounded Waiting).
7. `26-28` (3 trang, CONTENT): **5.3.2** Solution classification (software/hardware, OS support, busy-waiting vs blocking/sleep-wakeup).
8. `29-30` (2 trang, CONTENT): **5.3.3** Disable Interrupts.
9. `31-36` (6 trang, CONTENT): **5.4.1** Software Solution 1 (turn variable, three-requirement analysis).
10. `37-40` (4 trang, CONTENT): **5.4.2** Software Solution 2 (flag[] array, three-requirement analysis).
11. `41-46` (6 trang, CONTENT): **5.4.3** Peterson's Solution (turn + flag[], Mutual Exclusion, Progress, Bounded Waiting).
12. `47-51` (5 trang, CONTENT): **5.4.4** Peterson and modern architectures (instruction/memory reordering, modern execution assumptions).
13. `52-55` (4 trang, CONTENT): **5.5.1** Memory Barrier.
14. `56` (1 trang, CONTENT - `source_depth: SELF_STUDY`): **5.5.2** test_and_set, **5.5.3** compare_and_swap, **5.5.4** atomic variables.
15. `57-60` (4 trang, CONTENT): **5.6.1** Mutex Locks (acquire/release, busy waiting, spinlock).
16. `61-63` (3 trang, CONTENT): **5.6.2** Mutex without busy waiting (block, wakeup).
17. `64-65` (2 trang, CONTENT): **5.6.3** Using Mutex Locks.
18. `66` (1 trang, CONTENT): Tóm tắt Phần 1 (summary).
19. `67` (1 trang, NON_CONTENT): Thảo luận / Kết thúc Phần 1 (discussion/end).

### Phần 2: `#Week07-Chapter5-2 2024.pdf` (72 trang vật lý: 68 CONTENT + 4 NON_CONTENT)

1. `1-3` (3 trang, NON_CONTENT): Trang bìa, mục tiêu & nội dung Phần 2.
2. `4-15` (12 trang, CONTENT): **5.7.1** Semaphore definition.
3. `16-17` (2 trang, CONTENT): **5.7.2** Semaphore types (Counting, Binary).
4. `18-22` (5 trang, CONTENT): **5.7.3** Semaphore implementation (atomic wait/signal, blocking, queue, wakeup).
5. `23-26` (4 trang, CONTENT): **5.7.4** Semaphore applications (Mutual Exclusion, execution ordering, condition/resource synchronization).
6. `27-29` (3 trang, CONTENT): **5.7.5** Semaphore remarks (wait/signal critical section, atomicity, implementation notes).
7. `30-32` (3 trang, CONTENT): **5.7.6** Problems when using Semaphore (incorrect initialization/order, deadlock-style failures).
8. `33-36` (4 trang, CONTENT): **5.8.1** Monitor.
9. `37-40` (4 trang, CONTENT): **5.8.2** Condition Variable.
10. `41-43` (3 trang, CONTENT): **5.9** Liveness (Liveness definition, indefinite waiting, Progress, Bounded Waiting, Deadlock definition/example).
    - *Ghi chú chuẩn hóa Tier-A:* Slide chính thức mục 5.9 chỉ bao gồm: định nghĩa Liveness, chờ đợi vô hạn, Progress, Bounded Waiting và định nghĩa/ví dụ Deadlock. Tuyệt đối **không đưa Priority Inversion / Priority Inheritance vào diện nội dung Tier-A** từ slide bài giảng.
11. `44-46` (3 trang, CONTENT): **5.10.1** Bounded-Buffer problem statement.
12. `47-50` (4 trang, CONTENT): **5.10.2** Bounded-Buffer solution.
13. `51-53` (3 trang, CONTENT): **5.10.3** Common Bounded-Buffer mistakes.
14. `54-57` (4 trang, CONTENT): **5.11.1** Readers-Writers problem.
15. `58-60` (3 trang, CONTENT): **5.11.2** Readers-Writers solution.
16. `61-63` (3 trang, CONTENT): **5.12.1** Dining-Philosophers problem.
17. `64-70` (7 trang, CONTENT): **5.12.2** Dining-Philosophers solutions (Semaphore, deadlock risk, source-provided avoidance ideas, Monitor/conditions).
18. `71` (1 trang, CONTENT): Tóm tắt Chương 5 (summary).
19. `72` (1 trang, NON_CONTENT): Thảo luận / Kết thúc Chương 5 (discussion/end).

---

## 7. Đánh Giá Tồn Đọng Nguồn (Open Source Issues)

- **OPEN SOURCE BLOCKERS:** **`0`**
- **OPEN SOURCE MAJORS:** **`0`**
- **OPEN SOURCE MINORS:** **`0`**

---

## 8. Kết Quả Kiểm Thử Bằng Bộ Công Cụ Tự Động

Kịch bản kiểm thử [`scripts/validate_ch05_source_map.py`](scripts/validate_ch05_source_map.py) ở chế độ chính xác cao đã xác nhận:

- Khớp 100% chữ ký phân đoạn chính xác (Part 1: 19 mục, Part 2: 19 mục): **PASS**
- Tổng số trang nội dung Part 1 (63 CONTENT, 4 NON_CONTENT = 67): **PASS**
- Tổng số trang nội dung Part 2 (68 CONTENT, 4 NON_CONTENT = 72): **PASS**
- Xác minh từ khóa đại diện cho toàn bộ 32 phân đoạn con: **PASS**
- Khẳng định không tồn tại khẳng định Tier-A chưa được chứng minh (*Priority Inversion / Priority Inheritance*): **PASS (Count = 0)**
- Kiểm tra tính vệ sinh YAML (không trùng lặp khóa): **PASS (Duplicate Keys = 0)**
- Biến thể 58p, 55p, 32p được loại trừ khỏi độ phủ chính tắc: **PASS**
- Trang 56 Phần 1 ghi nhận `SELF_STUDY`: **PASS**
- Chưa soạn thảo tệp lý thuyết Chương 5 (`content/theory/ch05-synchronization.md`): **PASS**
- Validator Exit Code: **`0 (PASS)`**

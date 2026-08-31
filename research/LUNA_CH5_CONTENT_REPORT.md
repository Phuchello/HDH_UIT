# BÁO CÁO SOẠN THẢO NỘI DUNG CHƯƠNG 5 (LUNA CH5 CONTENT REPORT)

**Thời gian lập:** 2026-08-31  
**Người thực hiện:** Senior Operating Systems Author + Source-Faithful Question Author (Codex Luna Ultra)  
**Nhánh Git:** `v2/complete-theory-labs`  
**Giai đoạn:** `V2_BATCH2_CH5_DRAFT_READY_FOR_ENGINEERING_QA`  
**Trạng thái Lập bản đồ nguồn:** `VERIFIED — INDEPENDENT CHECK PASS`  
**Trạng thái Soạn thảo Chương 5:** `CONTENT_DRAFTED`  
**Xác minh học thuật (Academic Verification):** `PASS — BATCH 1 ONLY; CH5 DRAFT — NOT YET VERIFIED`  
**Hành động tiếp theo chính xác (Exact Next Action):** Terra Medium thực hiện kiểm thử hồi quy kỹ thuật/build, sau đó Luna Ultra tiến hành thẩm định học thuật độc lập cho Chương 5.  

---

## 1. Tổng Quan Tiến Độ Soạn Thảo (Drafting Overview)

Toàn bộ nội dung lý thuyết chính tắc và ngân hàng câu hỏi tự luận cho **Chương 5: Đồng bộ Tiến trình (Process Synchronization)** đã được soạn thảo hoàn tất với độ trung thực học thuật cao nhất, bám sát từng trang slide bài giảng chính thức năm 2024 và tệp nhị phân ngân hàng câu hỏi UIT đã được kiểm chứng mã băm SHA-256.

Các tệp nội dung đã tạo lập:
1. **Lý thuyết chính tắc:** [`content/theory/ch05-synchronization.md`](content/theory/ch05-synchronization.md) (11 đề mục lớn + tóm tắt ôn tập).
2. **Ngân hàng tự luận:** [`content/questions/subjective/ch05.md`](content/questions/subjective/ch05.md) (18/18 câu hỏi và bài tập có lời giải chi tiết, kịch bản đan xen lệnh và rubric tự đánh giá).
3. **Bộ kiểm thử nội dung:** [`scripts/validate_ch05_content.py`](scripts/validate_ch05_content.py) (Kiểm tra tự động 100% độ phủ trang, neo điểm đến, và cách ly với Chương 6).

---

## 2. Độ Phủ Slide Chính Tắc (Canonical Slide Coverage)

| Phân Đoạn Slide | Tên Tệp Chính Tắc | Mã Băm SHA-256 | Số Trang Nội Dung | Số Trang Đã Soạn Thảo | Số Trang Còn Thiếu | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Chương 5 - Phần 1** | `#Week06-Chapter5-1 2024.pdf` | `2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416` | **63** | **63** | **0** | `CONTENT_DRAFTED` |
| **Chương 5 - Phần 2** | `#Week07-Chapter5-2 2024.pdf` | `f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2` | **68** | **68** | **0** | `CONTENT_DRAFTED` |
| **TỔNG CỘNG** | — | — | **131** | **131** | **0** | **100% HOÀN TẤT** |

---

## 3. Xử Lý Nội Dung Tự Học (`source_depth: SELF_STUDY`)

- **Vị trí nguồn:** Slide 56 của Phần 1 (`UIT-SLIDE-CH05-1-2024`).
- **Chủ đề:** Các chỉ thị nguyên tử phần cứng (`test_and_set`, `compare_and_swap`, `Atomic Variables`).
- **Cách thức xử lý trong cẩm nang:**
  - Được giữ nguyên nhãn `source_depth: SELF_STUDY` theo đúng phân định trong bài giảng.
  - Được bổ sung phần giải thích cơ chế kỹ thuật sâu (Tier-B enrichment) bao gồm: mã giả hành vi phần cứng, mã C ứng dụng miền găng với biến khóa `lock`, và ứng dụng biến đơn nguyên giải quyết bài toán đếm Producer-Consumer mà không cần dùng Mutex.

---

## 4. Bổ Sung Kỹ Thuật Học Thuật Cao (Tier-B Enrichments)

1. **Phân tích Kiến trúc Hiện đại (Modern Architectures) đối với Peterson:**
   - Phân biệt rõ: Giải thuật Peterson **đúng đắn tuyệt đối về mặt toán học** dưới mô hình Sequential Consistency.
   - Làm rõ hiện tượng *Instruction/Memory Reordering* do trình biên dịch và CPU Out-of-Order (OoO) trên phần cứng thực tế, dẫn đến nhu cầu bắt buộc phải chèn **Memory Barrier**.
2. **Hiện thực Semaphore Mức Nhân (Kernel-Level Semaphore Implementation):**
   - Trình bày mã nguồn `typedef struct { int value; struct process *list; } semaphore;` với cơ chế `block()` và `wakeup()`.
   - Phân tích rõ ý nghĩa giá trị âm của `value` trong mô hình giáo trình ($|value|$ = số tiến trình chờ) và phân biệt với ngữ nghĩa POSIX `sem_wait`.
3. **Cơ chế Nhả khóa và Tái chiếm khóa trong Monitor:**
   - Giải thích bản chất tại sao `condition.wait()` bắt buộc phải giải phóng khóa monitor khi vào hàng đợi ngủ và tái chiếm lại khóa monitor khi được đánh thức bởi `condition.signal()`.

---

## 5. Thẩm Định Nguồn Ngân Hàng Câu Hỏi (QBank Provenance & Coverage)

- **Trạng thái tệp nhị phân chính thức:**
  - Tệp gốc: `Bai tap chuong 5 HDH.docx` (Bản đính kèm chính thức từ người dùng).
  - Kích thước: **56,369 bytes** | SHA-256: `503cd8fdb619bcfd664cfaa198915bc50d0ba6bb910c74d14ccff5252e646186`.
  - Khả dụng trực tiếp trên đĩa: **YES** (Đã kiểm tra mã băm khớp 100%).
- **Thống kê định lượng:**
  - `xml_paragraph_count`: 129 đoạn.
  - `content_paragraph_count`: 128 đoạn.
  - `verified_question_count`: **18 câu hỏi/bài tập**.
  - `drafted_answers`: **18/18 (100%)** tại [`content/questions/subjective/ch05.md`](content/questions/subjective/ch05.md).
- **Chuẩn hóa cấu trúc lời giải:**
  Mỗi câu hỏi đều có đủ 8 trường chuẩn: `QUESTION`, `SOURCE`, `TYPE`, `MINIMUM ANSWER`, `REQUIRED KEY POINTS`, `FULL EXPLANATION`, `COMMON MISSING POINTS`, `COMMON WRONG CLAIMS`, `SELF_CHECK_RUBRIC`.

---

## 6. Xử Lý Xung Đột Cấu Trúc Nguồn (Source Conflicts)

1. **Xung đột Đề cương vs Slide (Numbering Conflict):**
   - Đề cương chia `5.10` thành 3 bài toán nhỏ (`5.10.1`, `5.10.2`, `5.10.3`). Slide tách riêng thành 3 mục lớn (`5.10`, `5.11`, `5.12`).
   - *Xử lý:* Cẩm nang sử dụng trực tiếp **tên khái niệm và thuật giải** làm tiêu đề cấp 2 (`## 9. Bài toán Bounded-Buffer`, `## 10. Bài toán Readers-Writers`, `## 11. Bài toán Dining-Philosophers`), không bị phụ thuộc vào số hiệu đề cương.
2. **Cách ly Ranh giới với Chương 6 (Deadlock):**
   - Chương 5 chỉ trình bày Deadlock ở góc độ hiện tượng đồng bộ và thất bại Liveness.
   - Các nội dung chuyên sâu của Chương 6 (4 điều kiện Coffman, đồ thị cấp phát tài nguyên RAG, thuật toán Banker, thuật toán phát hiện/phục hồi bế tắc) **hoàn toàn không bị xâm nhập** vào Chương 5.

---

## 7. Kết Quả Kiểm Thử Kỹ Thuật (Technical & Academic QA)

- [`scripts/validate_ch05_source_map.py`](scripts/validate_ch05_source_map.py): **PASS**
- [`scripts/validate_ch05_content.py`](scripts/validate_ch05_content.py): **PASS**
- [`scripts/validate_batch1_canonical.py`](scripts/validate_batch1_canonical.py): **PASS**
- [`scripts/check_batch1_numeric.py`](scripts/check_batch1_numeric.py): **PASS**
- `npm test` (`generate_foundation_gate.py`): **PASS**
- Tất cả 131 trang nội dung đều trỏ đến các đề mục và neo hợp lệ: **100% PASS**.

---

## 8. Đánh Giá Tồn Đọng Nội Dung (Open Content Issues)

- **OPEN CONTENT BLOCKERS:** **`0`**
- **OPEN CONTENT MAJORS:** **`0`**
- **OPEN CONTENT MINORS:** **`0`**
- **SẴN SÀNG SOẠN THẢO CHƯƠNG 6:** **`NO`** *(Cần hoàn tất toàn bộ quy trình kiểm toán học thuật và QA kỹ thuật cho Chương 5 trước)*.

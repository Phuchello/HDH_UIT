# BÁO CÁO ĐỐI SOÁT NGUỒN CHÍNH TẮC CHƯƠNG 5 (LUNA CH5 SOURCE MAP REPORT)

**Thời gian lập:** 2026-08-31  
**Người thực hiện:** Luna Academic Reviewer / Source Fidelity Specialist  
**Nhánh Git:** `v2/complete-theory-labs`  
**Trạng thái Cổng:** `V2_BATCH2_CH5_SOURCE_MAP_READY_FOR_INDEPENDENT_CHECK`  
**Trạng thái Nội dung:** `CH5 THEORY NOT AUTHORED (LOCKED FOR INDEPENDENT AUDIT)`  

---

## 1. Mục Đích Báo Cáo (Objective)

Khóa chặt bản đồ nguồn chính tắc (Canonical Source Map) cho **Chương 5: Đồng bộ Tiến trình (Process Synchronization)** trước khi tiến hành soạn thảo lý thuyết và ngân hàng câu hỏi, đảm bảo tuyệt đối không nhầm lẫn giữa bản đính kèm chính tắc của giảng viên và các bản biến thể lưu hành cục bộ.

---

## 2. Bảng Nguồn Slide Chính Tắc Chương 5 (Canonical Slide Corpus)

| Phân Đoạn Slide | Tên Tệp Chính Tắc | Mã Băm SHA-256 | Số Trang Vật Lý | Phân Bổ Nội Dung | Trạng Thái Đăng Ký |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Chương 5 - Phần 1** | `#Week06-Chapter5-1 2024.pdf` | `2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416` | **67** | **63 CONTENT + 4 NON_CONTENT** | `UIT-SLIDE-CH05-1-2024` (official_slide) |
| **Chương 5 - Phần 2** | `#Week07-Chapter5-2 2024.pdf` | `f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2` | **72** | **68 CONTENT + 4 NON_CONTENT** | `UIT-SLIDE-CH05-2-2024` (official_slide) |

### Ghi Chú Quan Trọng Về Phân Đoạn & Trang Tự Học:
1. **Phần 1 - Trang 56 (`SELF_STUDY`):**
   - Nội dung trang 56 gồm các mục: *5.5.2 Lệnh phần cứng: test_and_set*, *5.5.3 Lệnh phần cứng: compare_and_swap*, *5.5.4 Biến đơn nguyên (Atomic Variables)*.
   - Slide ghi rõ yêu cầu: *"Sinh viên tự nghiên cứu các mục trên và trình bày tại lớp"*. Bản đồ nguồn ghi nhận chính xác trạng thái `SELF_STUDY`.
2. **Phần 2 - Phạm Vi Bao Phủ Hoàn Chỉnh (72 trang):**
   - Phần 2 bao gồm trọn vẹn lý thuyết Semaphore (trang 4–32), Monitor & Condition Variables (trang 33–40), Liveness & Priority Inversion (trang 41–43), và 3 bài toán đồng bộ kinh điển: Bounded-Buffer (trang 44–53), Readers-Writers (trang 54–60), Dining-Philosophers (trang 61–70).

---

## 3. Xử Lý Xung Đột Cấu Trúc Nguồn (SOURCE_STRUCTURE_CONFLICT)

Trong kho tài liệu cục bộ tồn tại bộ slide 3 phần cũ gồm:
- `Week07-Chapter5-1 2024.pdf` (58 trang, SHA `7d49c0aa50041c0585ac5959032ea6c3111f5589d8d92936f6e8047035df5bda`)
- `Week09-Chapter5-2 2024.pdf` (55 trang, SHA `d74d9324f6952e8c1d6f001b6ec8f0c75dabe6201e742d05a151227bb5aec7f3`)
- `Week10-Chapter5-3 2024.pdf` (32 trang, SHA `7621b767621b855980337bfd655678e7f5b7017ee51d3feec2dbcb80bda9cd3c`)

**Quyết định giải quyết xung đột:**
- Cả 3 tệp cũ được phân loại là `source_variant` trong [`content/sources/registry.yaml`](content/sources/registry.yaml) (`UIT-SLIDE-CH05-1-2024-VARIANT-LOCAL-58`, `UIT-SLIDE-CH05-2-2024-VARIANT-LOCAL-55`, `UIT-SLIDE-CH05-3-2024-VARIANT-LOCAL-32`).
- Toàn bộ 3 biến thể cũ bị **LOẠI BỎ HOÀN TOÀN** khỏi danh sách `decks` chính tắc trong [`research/data/slide_coverage.yaml`](research/data/slide_coverage.yaml).
- Bản đồ phủ slide chính tắc chỉ tính toán dựa trên bộ 2 phần chính thức (`#Week06-Chapter5-1 2024.pdf` 67 trang và `#Week07-Chapter5-2 2024.pdf` 72 trang).

---

## 4. Bảng Định Tuyến Phân Đoạn Chi Tiết (Detailed Section Breakdown)

### Phần 1: `#Week06-Chapter5-1 2024.pdf` (67 trang)
- **Trang 1–3 (3 trang, NON_CONTENT):** Trang bìa, mục tiêu bài học & nội dung chính.
- **Trang 4–15 (12 trang, CONTENT):** 5.1 Bối cảnh & 5.2 Khái niệm Race Condition.
- **Trang 16–36 (21 trang, CONTENT):** 5.3 Vấn đề Miền găng (Critical Section) & 3 yêu cầu giải pháp (Mutual Exclusion, Progress, Bounded Waiting).
- **Trang 37–51 (15 trang, CONTENT):** 5.4 Các giải pháp phần mềm & Giải pháp Peterson (cổ điển vs hiện đại).
- **Trang 52–55 (4 trang, CONTENT):** 5.5.1 Hỗ trợ phần cứng: Memory Barrier.
- **Trang 56 (1 trang, CONTENT - SELF_STUDY):** 5.5.2-5.5.4 Lệnh phần cứng test_and_set, compare_and_swap & Atomic Variables.
- **Trang 57–65 (9 trang, CONTENT):** 5.6 Mutex Locks: Định nghĩa, Spinlock vs Non-busy waiting & Cách sử dụng.
- **Trang 66 (1 trang, CONTENT):** Tóm tắt lại Phần 1.
- **Trang 67 (1 trang, NON_CONTENT):** Thảo luận / Kết thúc Phần 1.

### Phần 2: `#Week07-Chapter5-2 2024.pdf` (72 trang)
- **Trang 1–3 (3 trang, NON_CONTENT):** Trang bìa, mục tiêu & nội dung Phần 2.
- **Trang 4–32 (29 trang, CONTENT):** 5.7 Semaphore: Định nghĩa, Phân loại (Counting vs Binary), Hiện thực (Block/Wakeup), Ứng dụng & Nhận xét.
- **Trang 33–40 (8 trang, CONTENT):** 5.8 Monitor: Định nghĩa, Biến điều kiện (Condition Variables) & Đồng bộ thứ tự thực thi.
- **Trang 41–43 (3 trang, CONTENT):** 5.9 Liveness: Deadlock, Starvation & Hiện tượng đảo quyền ưu tiên (Priority Inversion) kèm thừa kế ưu tiên (Priority Inheritance).
- **Trang 44–53 (10 trang, CONTENT):** 5.10 Bài toán Đồng bộ Bounded-Buffer (Producer-Consumer).
- **Trang 54–60 (7 trang, CONTENT):** 5.11 Bài toán Readers-Writers (Phát biểu, Phân tích & Lời giải Semaphore).
- **Trang 61–70 (10 trang, CONTENT):** 5.12 Bài toán Bữa ăn các Triết gia Dining-Philosophers (Phát biểu, Phân tích, Nguy cơ Deadlock & Lời giải).
- **Trang 71 (1 trang, CONTENT):** Tóm tắt lại Chương 5.
- **Trang 72 (1 trang, NON_CONTENT):** Thảo luận / Kết thúc Chương 5.

---

## 5. Kết Quả Kiểm Thử Bằng Công Cụ Tự Động

Kịch bản kiểm thử [`scripts/validate_ch05_source_map.py`](scripts/validate_ch05_source_map.py) đã được tích hợp vào hệ thống kiểm toán tự động `scripts/generate_foundation_gate.py` và CI pipeline (`.github/workflows/validate.yml`):

- `UIT-SLIDE-CH05-1-2024` (67 trang, SHA matched): **PASS**
- `UIT-SLIDE-CH05-2-2024` (72 trang, SHA matched): **PASS**
- Độ phủ Phần 1 (63 CONTENT + 4 NON_CONTENT = 67 trang): **PASS**
- Độ phủ Phần 2 (68 CONTENT + 4 NON_CONTENT = 72 trang): **PASS**
- Biến thể 58p, 55p, 32p được phân loại là `source_variant` và loại trừ khỏi độ phủ chính tắc: **PASS**
- Trang 56 Phần 1 ghi nhận `SELF_STUDY`: **PASS**
- Chưa soạn thảo tệp lý thuyết Chương 5 (`content/theory/ch05-synchronization.md`): **PASS**
- Validator Exit Code: **0 (PASS)**

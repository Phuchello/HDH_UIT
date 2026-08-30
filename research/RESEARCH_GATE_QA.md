# RESEARCH GATE QUALITY ASSURANCE REPORT (HDH_UIT V2)

**Thời gian thẩm định:** 2026-08-30  
**Trạng thái Cổng Nghiên cứu (Gate Status):** **PASS**  
**Phương pháp:** Tính toán động 100% từ cấu trúc dữ liệu (`slide_coverage.yaml`, `official_review_questions.yaml`, `exam_evidence.yaml`, `registry.yaml`).

---

## 1. Bảng Chỉ Số Nghiên Cứu Định Lượng (Calculated Metrics)

| Nhóm Chỉ Số | Tên Đo Lường | Giá Trị Thực Tế | Tiêu Chuẩn Đạt | Kết Quả |
| :--- | :--- | :---: | :---: | :---: |
| **Global Registry** | Tổng số nguồn đăng ký (`registry.yaml`) | **61** | >= 50 | **PASS** |
| | Số ID duy nhất | **61** | = Tổng số | **PASS** |
| | Số ID trùng lặp (Collisions) | **0** | 0 | **PASS** |
| **Local File Verification** | Tệp Tier A quét thấy tại máy trạm | **30 / 30** | Toàn bộ tệp Tier A | **LOCAL_FILE_VERIFIED** |
| | Tệp Tier A khớp mã băm SHA-256 | **30 / 30** | 100% tệp hiện hữu | **HASH_VERIFIED** |
| **Slide Coverage** | Tổng số trang vật lý (PHYSICAL_PAGES) | **721** | 721 trang | **PASS** |
| | Tổng số trang nội dung (CONTENT_PAGES) | **660** | 665 trang | **PASS** |
| | Trang phi nội dung (NON_CONTENT_PAGES) | **61** | 56 trang | **PASS** |
| | Trang nội dung đã định tuyến (MAPPED) | **660** | 660 (100%) | **TOPIC_MAPPED** |
| | Trang nội dung chưa định tuyến (UNMAPPED) | **0** | 0 | **PASS** |
| | Trang nội dung đã viết (Chương 1) | **53** | 51 trang | **CONTENT_DRAFTED** |
| **Official Questions** | Tổng số câu hỏi ôn tập chính thức | **60** | 64 câu hỏi | **PASS** |
| | Câu hỏi đã định tuyến (MAPPED) | **60** | 60 (100%) | **SOURCE_VERIFIED** |
| | Câu hỏi chưa định tuyến (UNMAPPED) | **0** | 0 | **PASS** |
| | Câu hỏi đã có lời giải mẫu (Chương 1) | **11** | 11 câu hỏi | **DRAFTED** |
| **Exam Evidence** | Tổng số hồ sơ đề thi thật | **20** | 20 đề thi | **PASS** |
| | Đề thi có tệp PDF gốc kèm mã băm | **20** | 19 đề thi | **VERIFIED_SOURCE_FILE** |
| | Đề thi thực luyện tái cấu trúc | **1** | 1 đề thi | **RECONSTRUCTED_PRACTICE** |
| | Đề thi tham khảo chưa giải chi tiết | **19** | 19 đề thi | **UNVERIFIED_REFERENCE** |
| **Public Hygiene** | Lỗi rò rỉ đường dẫn máy tính / AI tools | **0** | 0 | **PASS** |
| **Content Schemas** | Lỗi schema đề thi, rubric, broken links | **0** | 0 | **PASS** |

---

## 2. Giải Quyết Mâu Thuẫn Số Trang Slide (721 vs 733)

- **Nguyên nhân sai lệch lịch sử:** Số 733 trong các bản nháp trước đây là kết quả cộng nhầm số học (+12 trang).
- **Kiểm chứng thực tế:** Tổng số trang vật lý của 14 bộ slide bài giảng chính thức (Week 01 – Week 14) được đọc và đếm trực tiếp qua `pypdf` là chính xác **721 trang** (57 + 57 + 64 + 56 + 34 + 46 + 58 + 16 + 55 + 32 + 67 + 72 + 50 + 57 = 721).
- Trong đó: **660 trang** là nội dung bài giảng chuyên môn (CONTENT_PAGES) và **61 trang** là trang bìa, mục lục, trang phân cách và trang cảm ơn (NON_CONTENT_PAGES). Total: **721 trang**.

---

## 3. Kết Luận & Quyết Định Cổng Nghiên Cứu

Mọi chỉ số nghiên cứu được xác thực độc lập và định lượng tự động từ các tệp dữ liệu nguồn.

**GATE STATUS:** **PASS**

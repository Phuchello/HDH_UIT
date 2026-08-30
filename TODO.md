# TIẾN ĐỘ THỰC HIỆN DỰ ÁN V2 (TODO V2)

---

## Giai Đoạn 1: Nghiên Cứu Học Thuật & Khóa Bằng Chứng (Research & Evidence Gates)
- [x] Tạo nhánh an toàn `v2/complete-theory-labs` từ `origin/main`.
- [x] Lập danh mục toàn bộ nguồn tài liệu chính thức (`research/SOURCE_LEDGER.md`).
- [x] Xây dựng ma trận phủ 100% Slide bài giảng Week 1–14 (`research/SLIDE_COVERAGE_MATRIX.md`).
- [x] Xây dựng bản đồ cấu trúc Sách Lý Thuyết V2 (`research/THEORY_COVERAGE_MATRIX.md`).
- [x] Ánh xạ 100% câu hỏi ôn tập chính thức (`research/OFFICIAL_REVIEW_QUESTION_MAP.md`).
- [x] Xây dựng ma trận khảo sát 20 đề thi thật UIT 2017–2025 (`research/EXAM_EVIDENCE_MATRIX.md`).
- [x] Phân tích quy luật và xu hướng đề thi (`research/EXAM_PATTERN_ANALYSIS.md`).
- [x] Phân loại các biến thể thực hành Lab 1–6 (`research/LAB_VARIANT_MAP.md`).
- [x] Tổng hợp tài liệu API chuẩn quốc tế man7.org (`research/LAB_SOURCE_LEDGER.md`).
- [x] Lập báo cáo phân tích khoảng cách nội dung V1 vs V2 (`research/CONTENT_GAP_REPORT.md`).

---

## Giai Đoạn 2: Mở Rộng Kiến Trúc Ba Sản Phẩm & Ngân Hàng Tự Luận
- [x] Thiết lập kiến trúc nguồn đơn nhất SSOT (`research/CONTENT_ARCHITECTURE_V2.md`).
- [x] Lập sổ tay nguồn khảo sát câu hỏi tự luận (`research/SUBJECTIVE_SOURCE_LEDGER.md`).
- [x] Xây dựng ma trận 60+ câu hỏi tự luận có barem chấm chi tiết (`research/SUBJECTIVE_QUESTION_MATRIX.md`).
- [x] Khởi tạo cây thư mục nguồn chuẩn hóa `content/` (theory, labs, questions, exams, flashcards, glossary).
- [x] Soạn thảo các tệp nội dung mẫu chuẩn hóa:
  - [x] `content/theory/ch01-overview.md`
  - [x] `content/questions/subjective/ch01.md`
  - [x] `content/labs/lab01-linux-basics.md`
  - [x] `content/exams/midterm/2023-2024-hk1.md`
  - [x] `content/flashcards/ch01-cards.md`
  - [x] `content/glossary/terms.md`
- [x] Xây dựng nguyên mẫu Web Companion tương tác (`web/`):
  - [x] Layout 3 cột phong cách Digital Garden (Explorer, Reading Canvas, Graph/TOC/Backlinks).
  - [x] Thành phần `StudyCard` (Active Recall có Hint, Keypoints, Solution, LocalStorage tracking).
  - [x] Thành phần `SubjectivePractice` (Lưu bản nháp, đối chiếu barem chấm, tự tính điểm).
  - [x] Canvas Đồ thị Tri thức Ngữ nghĩa cục bộ.
  - [x] Tìm kiếm nhanh toàn văn (Ctrl+K).
  - [x] Chế độ Sáng / Tối (Theme Switcher).

---

## Giai Đoạn 3: Triển Khai Soạn Thảo Toàn Bộ Nội Dung Chuẩn Hóa
- [ ] Soạn thảo đầy đủ các chương lý thuyết còn lại trong `content/theory/` (Chương 2 -> Chương 9, Midterm Review, Final Review).
- [ ] Soạn thảo đầy đủ các bài thực hành trong `content/labs/` (Lab 2 -> Lab 6 Case Study `it007sh`).
- [ ] Hoàn thiện toàn bộ ngân hàng câu hỏi tự luận `content/questions/subjective/` (Ch2 -> Ch9).
- [ ] Hoàn thiện các tệp trắc nghiệm, bài tập tính toán và flashcards.

---

## Giai Đoạn 4: Đóng Gói Xuất Bản & Đồng Bộ Ba Sản Phẩm
- [ ] Hoàn thiện bộ công cụ biên dịch tự động Sách Lý Thuyết A4 PDF và Sách Thực Hành A4 PDF từ `content/`.
- [ ] Đóng gói phiên bản phát hành tĩnh cho Web Companion.
- [ ] Bàn giao cho đợt kiểm toán xuất bản cuối cùng trước khi hợp nhất vào `main`.

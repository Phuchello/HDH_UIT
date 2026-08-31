# TIẾN ĐỘ THỰC HIỆN DỰ ÁN V2 (TODO V2)

---

## Giai Đoạn 1: Nghiên Cứu Học Thuật & Khóa Bằng Chứng (Research & Evidence Gates)
- [x] Tạo nhánh an toàn `v2/complete-theory-labs` từ `origin/main`.
- [x] Lập danh mục toàn bộ nguồn tài liệu chính thức (`research/SOURCE_LEDGER.md`).
- [x] Xây dựng ma trận phủ 100% Slide bài giảng Week 1–14 (`research/SLIDE_COVERAGE_MATRIX.md`).
- [x] Xây dựng bản đồ cấu trúc Sách Lý Thuyết V2 (`research/THEORY_COVERAGE_MATRIX.md`).
- [x] Ánh xạ câu hỏi ôn tập chính thức (`research/OFFICIAL_REVIEW_QUESTION_MAP.md`).
- [x] Xây dựng ma trận 20 hồ sơ bằng chứng đề thi UIT 2017–2025 (`research/EXAM_EVIDENCE_MATRIX.md`); evidence-aware: 1 `RECONSTRUCTED_PRACTICE`, 19 `UNVERIFIED_REFERENCE`, 0 `VERIFIED_ARCHIVE`.
- [x] Phân tích quy luật và xu hướng đề thi (`research/EXAM_PATTERN_ANALYSIS.md`).
- [x] Phân loại các biến thể thực hành Lab 1–6 (`research/LAB_VARIANT_MAP.md`).
- [x] Tổng hợp tài liệu API chuẩn quốc tế man7.org (`research/LAB_SOURCE_LEDGER.md`).
- [x] Lập báo cáo phân tích khoảng cách nội dung V1 vs V2 (`research/CONTENT_GAP_REPORT.md`).

---

## Giai Đoạn 2: Xử Lý Kiểm Toán GLM & Hoàn Thiện Nền Tảng SSOT
- [x] **AUD-V2-01:** Xây dựng Sổ đăng ký nguồn bất biến toàn cầu `content/sources/registry.yaml` và `scripts/validate_sources.py`.
- [x] **AUD-V2-02:** Chuyển toàn bộ nguyên mẫu HTML viết tay sang `archive/web-prototype-v2/`; xác lập `content/` là nguồn duy nhất.
- [x] **AUD-V2-03:** Thiết lập bộ sinh web tĩnh tùy biến tất định (`scripts/build_web.py`, `package.json`); Quartz CLI là tùy chọn thông tin, chưa triển khai.
- [x] **AUD-V2-04:** Tự động sinh `search_index.json` và `graph_data.json` từ toàn bộ Markdown trong `content/`; loại bỏ liên kết chết.
- [x] **AUD-V2-05:** Loại bỏ toàn bộ nạp CDN bên ngoài tại runtime; đóng gói KaTeX/MathJax cục bộ.
- [x] **AUD-V2-06 & AUD-V2-07:** Phân loại đề thi chuẩn xác (`RECONSTRUCTED_PRACTICE`), xây dựng schema kiểm tra siêu dữ liệu đề thi.
- [x] **AUD-V2-08:** Thay thế toàn bộ cụm từ "Barem chính thức" thành `SELF_CHECK_RUBRIC` ("Rubric tự kiểm tra gợi ý") kèm lưu ý rõ ràng.
- [x] **AUD-V2-09:** Xóa bỏ 100% đường dẫn máy trạm và công cụ AI; bổ sung công cụ kiểm tra `scripts/check_public_hygiene.py`.
- [x] **AUD-V2-10:** Xây dựng báo cáo kiểm toán nghiên cứu định lượng tự động `research/RESEARCH_GATE_QA.md` (`scripts/verify_research_gates.py`).
- [x] **AUD-V2-11:** Chuẩn hóa ngữ nghĩa các ma trận phủ kiến thức (`SOURCE_VERIFIED`, `TOPIC_MAPPED`, `CONTENT_DRAFTED`, `CONTENT_NOT_WRITTEN`).
- [x] **AUD-V2-12 & AUD-V2-13:** Rà soát và loại bỏ các số liệu suy diễn/võ đoán, bổ sung ngữ cảnh kỹ thuật chính xác cho Chương 1.
- [x] **AUD-V2-14 & AUD-V2-15:** Tinh chỉnh giao diện người đọc trang nhã, nghiêm túc; bổ sung câu từ chối trách nhiệm độc lập.
- [x] **AUD-V2-16:** Cập nhật tài liệu kiến trúc `research/CONTENT_ARCHITECTURE_V2.md`.
- [x] **SSOT Build Demonstration:** Thực nghiệm kiểm chứng cơ chế SSOT và ghi nhận báo cáo `research/SSOT_BUILD_PROOF.md`.
- [x] **Khóa Cổng Nền Tảng:** Thiết lập báo cáo `research/V2_FOUNDATION_GATE.md` đạt chuẩn **PASS** toàn diện.

---

## Giai Đoạn 3: Mở Rộng Soạn Thảo Toàn Diện (Scale Content)
- [ ] Soạn thảo đầy đủ các chương lý thuyết còn lại trong `content/theory/` (Chương 2 -> Chương 9, Midterm Review, Final Review).
- [ ] Soạn thảo đầy đủ các bài thực hành trong `content/labs/` (Lab 2 -> Lab 6 Case Study `it007sh`).
- [ ] Hoàn thiện toàn bộ ngân hàng câu hỏi tự luận `content/questions/subjective/` (Ch2 -> Ch9).
- [ ] Hoàn thiện các tệp trắc nghiệm, bài tập tính toán và flashcards.

---

## Giai Đoạn 4: Đóng Gói Xuất Bản & Phát Hành
- [ ] Hoàn thiện bộ công cụ biên dịch tự động Sách Lý Thuyết A4 PDF và Sách Thực Hành A4 PDF từ `content/`.
- [ ] Đóng gói phiên bản phát hành tĩnh cho Web Companion.
- [ ] Kiểm toán xuất bản cuối cùng trước khi hợp nhất vào `main`.

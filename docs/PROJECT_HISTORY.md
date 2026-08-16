# Lịch Sử Dự Án & Quá Trình Hoàn Thiện (Project History)

Tài liệu này ghi nhận quá trình nghiên cứu, phát triển, kiểm toán học thuật và hoàn thiện kỹ thuật của dự án Cẩm nang Hệ điều hành IT007 UIT.

---

## 1. Dòng Thời Gian Phát Triển

### Giai đoạn 1: Khảo sát & Xây dựng Cấu trúc Sách (Phases A–F)
- Thu thập toàn bộ tài liệu giảng dạy chính thức, slide bài giảng môn Hệ điều hành (IT007) của Trường ĐH Công nghệ Thông tin – ĐHQG-HCM.
- Phân tích ngân hàng câu hỏi tự luận, bài tập thực hành Lab 1–6 (Linux POSIX C), và đề thi giữa kỳ / cuối kỳ từ năm 2017 đến 2025.
- Thiết lập bản đồ đề cương (`CURRICULUM_MAP.md`), phân tích dạng bài thi (`EXAM_PATTERN.md`), bản đồ lab (`LAB_MAP.md`) và sổ tay nghiên cứu chuẩn POSIX (`RESEARCH_LEDGER.md`).

### Giai đoạn 2: Biên soạn & Thiết kế Động cơ In ấn (Phases G–I)
- Xây dựng hệ thống giao diện in ấn A4 chuẩn mực (`styles/components.css`, `styles/print.css`, `styles/publication.css`).
- Soạn thảo tuần tự 12 chương: Phần 0, Chương 1–8, Đề thi giữa kỳ Master Review, Đề thi cuối kỳ Master Review (02 đề mô phỏng kèm đáp án) và Phụ lục Linux Survival Kit.

### Giai đoạn 3: Kiểm toán Đối kháng Toàn diện (Phases J–N)
- Thực hiện đợt kiểm toán học thuật đối kháng độc lập (Adversarial Audit), phát hiện và lập danh mục 33 vấn đề (6 Critical, 16 Major, 8 Minor, 3 Optional).

### Giai đoạn 4: Sửa lỗi Học thuật & Khóa Nội dung (Phase O — Gemini Final Fix)
- Giải quyết dứt điểm 100% các lỗi Critical và Major:
  - Bổ sung toàn bộ lời giải chi tiết và bảng số liệu cho thuật toán SRTF (Chương 4).
  - Khắc phục mâu thuẫn trạng thái khung trang trong thuật toán thay thế trang LRU (Chương 8).
  - Cảnh báo tính chất không xác định (nondeterministic) của thứ tự xuất tiến trình con/cha trong `fork()`.
  - Làm rõ điều kiện áp dụng công thức $2^N$ tiến trình.
  - Bổ sung các bài toán đồng bộ kinh điển (Producer-Consumer, Readers-Writers, Dining Philosophers), Giám sát viên (Monitors) và Biến điều kiện.
  - Thêm giải thuật HRRN, Multilevel Queue (MQ), Multilevel Feedback Queue (MLFQ), và 3 bài toán tính EAT ngược.
  - Cung cấp đề thi thử cuối kỳ số 02 đầy đủ đáp án và code chuẩn cho các bài Lab Linux.

### Giai đoạn 5: Kỹ nghệ Xuất bản & Tạo PDF Hai Lượt (Phase P — Codex Publication Pass)
- Thay thế hoàn toàn 12 `<iframe>` cũ bằng một tài liệu DOM duy nhất liên tục (Single printable DOM).
- Đóng gói thư viện MathJax 3.2.2 cục bộ để render 771 công thức toán học 100% offline.
- Xây dựng cơ chế biên dịch 2 lượt (Two-Pass Build Pipeline) để tạo mục lục tự động khớp từng số trang thực tế.
- Phủ Header chương và Footer số trang chuẩn A4, tối ưu hóa ngắt trang không để bảng biểu hoặc khối code bị chia cắt.
- Xuất bản bản PDF chính thức 56 trang A4 đạt 96/100 điểm chất lượng xuất bản.

### Giai đoạn 6: Đóng gói Kho Lưu Trữ Công Khai (Final Canonical Integration)
- Tái cấu trúc kho lưu trữ sạch sẽ, phân tách rõ ràng `src/`, `dist/`, `docs/`, `scripts/`, `reports/`.
- Quét sạch 100% đường dẫn máy cá nhân và bảo mật dữ liệu.
- Viết bộ test suite tự động `validate.py`, tạo bộ ảnh xem trước sắc nét và chuẩn bị nhánh phát hành `release/it007-handbook-v1`.

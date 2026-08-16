# Nhật Ký Thay Đổi (Changelog)

Toàn bộ các cột mốc phát triển và lịch sử phát hành của dự án Cẩm nang Hệ điều hành IT007 UIT được ghi nhận tại đây.

---

## [v1.0.0] — 2026-08-16 (Ấn Bản Xuất Bản Chính Thức — Publication Ready)

### Hoàn thiện & Đóng gói Kho Lưu Trữ
- **Deliverables**: Phát hành bản PDF chuẩn in ấn A4 (56 trang, SHA-256 xác thực `65EA...`) và bản HTML đơn nhất tự chứa không dùng `<iframe>`.
- **Offline MathJax**: Đóng gói thư viện MathJax 3.2.2 cục bộ để kết xuất 771 công thức LaTeX 100% offline.
- **Bảo mật & Chuẩn hóa**: Rà soát 0 vết tích đường dẫn máy cá nhân, cấu trúc rõ ràng `src/`, `dist/`, `docs/`, `scripts/`, `reports/`.
- **Tự động hóa CI/CD**: Xây dựng bộ test suite `validate.py` 6 bước và GitHub Actions workflow.
- **Tài nguyên trực quan**: Trích xuất bộ ảnh xem trước chất lượng cao (`docs/preview/`).

---

## [v0.9.5] — 2026-08-13 (Kỹ Nghệ Xuất Bản & Tạo PDF Hai Lượt — Codex Pass)
- Thay thế 12 `<iframe>` cũ bằng cấu trúc DOM liên tục (Single-DOM merge).
- Xây dựng pipeline biên dịch hai lượt (Two-Pass Compilation) tự động định vị và tạo số trang mục lục (TOC) chính xác 100%.
- Phủ Header chương và Footer số trang chuẩn ISO A4.
- Đạt 96/100 điểm kiểm toán xuất bản.

---

## [v0.9.0] — 2026-08-13 (Sửa Lỗi Đối Kháng & Khóa Nội Dung — Gemini Final Fix)
- Giải quyết dứt điểm 6 lỗi Critical và 16 lỗi Major từ đợt kiểm toán độc lập:
  - Hoàn thiện bài tập mẫu SRTF kèm Gantt chart và bảng tính chi tiết.
  - Sửa mâu thuẫn trạng thái khung trang LRU (Chương 8).
  - Bổ sung cảnh báo tính không xác định của output `fork()`.
  - Thêm giải thuật đồng bộ kinh điển (Producer-Consumer, Readers-Writers, Dining Philosophers) và Giám sát viên (Monitors).
  - Thêm HRRN, Multilevel Queue (MQ), MLFQ, 3 bài toán tính EAT ngược và đề thi thử số 02.

---

## [v0.5.0] — 2026-08-11 (Bản Thảo Hoàn Chỉnh Toàn Bộ 12 Chương)
- Biên soạn hoàn chỉnh 8 chương lý thuyết, Phần 0, Đề thi giữa kỳ Master Review, Đề thi cuối kỳ Master Review và Phụ lục Linux.
- Xây dựng hệ thống giao diện in ấn Print CSS A4.

---

## [v0.1.0] — 2026-08-06 (Khởi Tạo Dự Án & Khảo Sát Nguồn)
- Tổng hợp tài liệu tham khảo, slide IT007 Khoa KTMT – UIT, ngân hàng câu hỏi và đề thi 2017–2025.
- Thiết lập khung phương pháp sư phạm 11 bước.

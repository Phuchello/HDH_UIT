# Build & Validation Tooling — HDH_UIT

Thư mục này chứa toàn bộ các công cụ, script biên dịch và bộ kiểm thử tự động phục vụ xây dựng cẩm nang Hệ điều hành IT007 UIT.

---

## 1. Danh Sách Công Cụ (Tooling Inventory)

| Tệp tin | Môi trường | Chức năng chính |
| :--- | :--- | :--- |
| `build.js` | Node.js | Đọc 12 tệp chương trong `src/chapters/`, CSS trong `src/styles/`, gộp thành một tài liệu DOM duy nhất (Single-DOM) không dùng `<iframe>`, nhúng MathJax 3.2.2 offline và kết xuất chỉ mục TOC hai lượt. |
| `build.ps1` | PowerShell | Pipeline tự động hóa toàn diện: Pass 1 HTML $\rightarrow$ Trích xuất số trang chương $\rightarrow$ Pass 2 HTML (chèn TOC chuẩn) $\rightarrow$ Render PDF Chromium $\rightarrow$ Phủ Header/Footer $\rightarrow$ Trích xuất phân tích chất lượng. |
| `pdf_tools.py` | Python 3 | Xử lý PDF cấp thấp: ánh xạ số trang mục lục, thêm siêu dữ liệu, thêm header/footer, phân tích mật độ trang và render PNG kiểm tra. |
| `technical_checks.py` | Python 3 | Kiểm thử tính đúng đắn của các thuật toán: cây tiến trình fork, lịch trình FCFS/SJF/SRTF/RR, an toàn Banker, tính toán EAT và thay thế trang FIFO/OPT/LRU. |
| `validate.py` | Python 3 | Bộ kiểm thử toàn diện 6 bước: cấu trúc nguồn, HTML không iframe, PDF 56 trang A4, ký hiệu toán học, tính bảo mật và an toàn kho lưu trữ. |
| `validate.ps1` | PowerShell | Trình thực thi tiện ích cho `validate.py` trên Windows. |
| `generate_previews.py` | Python 3 | Tự động trích xuất các trang tiêu biểu từ bản PDF thành ảnh xem trước PNG phục vụ README và tài liệu. |

---

## 2. Hướng Dẫn Tái Tạo & Biên Dịch (Build Reproduction)

### Chạy bộ kiểm thử tự động
```bash
# Bằng Python
python scripts/validate.py

# Hoặc bằng PowerShell
./scripts/validate.ps1
```

### Tạo lại hình ảnh xem trước từ PDF
```bash
python scripts/generate_previews.py
```

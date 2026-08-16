# Hướng Dẫn Biên Dịch & Xây Dựng (Build & Reproduction Guide)

Tài liệu này hướng dẫn chi tiết cách tái lập (reproduce), biên dịch bản HTML/PDF của Cẩm nang Hệ điều hành IT007 từ mã nguồn và thực hiện kiểm thử chất lượng.

---

## 1. Yêu Cầu Môi Trường (Prerequisites)

- **Node.js**: Phiên bản 18 trở lên (khuyên dùng Node 20+ hoặc 24 LTS).
- **Python**: Phiên bản 3.10 trở lên.
- **Thư viện Python phụ trợ**:
  ```bash
  pip install pypdf pdfplumber reportlab pillow pypdfium2
  ```
- **Trình duyệt phục vụ Render PDF**: Google Chrome hoặc Microsoft Edge (sẵn có trên Windows/macOS/Linux).

---

## 2. Quy Trình Biên Dịch Sách (Full Build Pipeline)

Dự án sử dụng cơ chế biên dịch **Hai Lượt (Two-Pass Compilation)** để tạo mục lục (TOC) chính xác 100% theo từng số trang thực tế trong bản PDF:

### Bước 1: Chạy Pipeline Tự Động Hóa
Từ thư mục gốc của repository, chạy lệnh PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1
```

Pipeline sẽ thực hiện tuần tự:
1. **Pass 1 (Gộp DOM ban đầu)**: Đọc 12 tệp chương nguồn HTML trong `src/chapters/`, kết hợp CSS trong `src/styles/` và nhúng MathJax 3.2.2 offline để xuất ra `dist/master-pass1.html`.
2. **Pass 1 Render**: Gọi Chrome/Edge Headless để xuất ra bản PDF tạm thời `scripts/master-pass1.pdf`.
3. **Trích xuất số trang (TOC Mapping)**: Phân tích `master-pass1.pdf` bằng Python để định vị chính xác trang bắt đầu của từng chương.
4. **Pass 2 (Chèn TOC chuẩn)**: Cập nhật số trang vào Mục lục và xuất ra bản HTML hoàn chỉnh `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html`.
5. **Pass 2 Render**: Render bản PDF thô `scripts/master-final-raw.pdf`.
6. **Hoàn thiện PDF (Finalize)**: Phủ Header (tên chương hiện tại) và Footer (số trang dạng Trang X / 56), chèn metadata XMP/Info và xuất bản deliverable chính thức tại `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf`.

---

## 3. Quy Trình Kiểm Thử Tự Động (Validation Suite)

Để kiểm tra tính toàn vẹn của kho lưu trữ, chạy lệnh:

```bash
# Python
python scripts/validate.py

# PowerShell
./scripts/validate.ps1
```

Bộ kiểm thử sẽ xác nhận 6 tiêu chuẩn:
- Đủ 12 tệp chương nguồn và 3 tệp CSS.
- Bản HTML phân phối đạt chuẩn (0 iframe, 0 remote request, 0 TODO markers).
- Bản PDF đạt chuẩn 56 trang A4, SHA-256 xác thực và toàn bộ trang có thể tìm kiếm văn bản (searchable text).
- Độ chính xác của các bài tập mẫu định thời CPU, Banker, thay thế trang LRU/FIFO/OPT.
- Mục lục 12 chương liên kết chính xác.
- Kho lưu trữ an toàn, không chứa thông tin nhạy cảm.

# RELEASE CHECKLIST — HDH_UIT

Bảng kiểm soát các tiêu chuẩn phát hành công khai cho kho lưu trữ **HDH_UIT** trên GitHub.

---

## 1. Thông Tin Kho Lưu Trữ GitHub (Repository Metadata)

- **Target Repository:** `https://github.com/Phuchello/HDH_UIT`
- **Default Branch:** `main`
- **Release Branch:** `release/it007-handbook-v1`
- **Repository Description:**
  > Cẩm nang Hệ điều hành IT007 – UIT: lý thuyết, bài tập, CPU scheduling, synchronization, deadlock, memory, Linux/POSIX và luyện thi.
- **Repository Topics / Tags:**
  `uit`, `it007`, `operating-systems`, `he-dieu-hanh`, `computer-science`, `linux`, `posix`, `cpu-scheduling`, `semaphore`, `deadlock`, `virtual-memory`, `vietnamese`

---

## 2. Tiêu Chuẩn Kiểm Thử Trước Khi Bàn Giao (Pre-Handoff Checks)

### Release hardening checkpoint — 2026-08-16

- [x] Final HTML rebuilt from canonical sources with local MathJax path and no iframe/remote dependency.
- [x] TOC, anchors, assets, IDs, formulas and A4/searchable PDF validated after a clean rebuild (57 pages).
- [x] CI workflow runs repository, final-deliverable and canonical technical checks; complete staged C programs compile with GCC on Linux.
- [ ] Push checkpoint and confirm the resulting GitHub Actions run before creating any v1.0.0 tag.

- [x] **Canonical Source Identified:** Nguồn chuẩn tại `src/chapters/`, `src/styles/`, `src/vendor/`.
- [x] **Antigravity & Codex Output Reconciled:** Đã đồng bộ toàn bộ sửa đổi học thuật và chế bản in ấn A4.
- [x] **Unicode / Mojibake:** 100% tiếng Việt UTF-8 chuẩn xác, không có ký tự lỗi ``.
- [x] **MathJax Offline Rendering:** 771 công thức toán học hiển thị hoàn hảo từ thư viện vendored MathJax 3.2.2.
- [x] **Broken Assets / Links:** 0 liên kết hỏng, 12/12 mục TOC khớp trang chính xác.
- [x] **No Iframes:** Tệp HTML phân phối là DOM liên tục, không dùng thẻ `<iframe>`.
- [x] **No Remote Dependencies:** Hoàn toàn độc lập ngoại tuyến, không gọi font hay JS từ CDN bên ngoài.
- [x] **Secret Scan:** Quét 0 vết tích đường dẫn người dùng cá nhân, 0 token, 0 credentials.
- [x] **No Machine Junk:** Loại trừ toàn bộ `.env`, `node_modules`, cache, file log và transcript nháp.
- [x] **Deliverables Present:**
  - `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html` (~207 KB)
  - `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf` (~7.66 MB, 56 trang A4)
- [x] **High-Res Preview Assets:** Đã trích xuất các ảnh xem trước từ PDF phục vụ README.
- [x] **README Excellence:** Landing page tiếng Việt đầy đủ lộ trình, mục lục, hướng dẫn build, disclaimer và credit tác giả.

# TODO — HDH_UIT RELEASE MISSION

## Tiến Độ Các Hạng Mục Công Việc

### 1. Khảo Sát & Đối Chiếu Nguồn [HOÀN TẤT]
- [x] Quét toàn bộ máy tính tìm các bản sao IT007 (`IT007_CAM_NANG_FINAL`, `IT007_CAM_NANG`).
- [x] Lập bảng phân loại `SOURCE_MANIFEST.md`.
- [x] Thiết lập cấu trúc thư mục canonical `HDH_UIT`.

### 2. Kiểm Tra Độ Chính Xác Nội Dung (Precision Checks) [ĐANG THỰC HIỆN]
- [x] Kiểm tra quy ước Priority Scheduling: "Luôn đọc quy ước đề bài; số nhỏ = ưu tiên cao trong ví dụ này".
- [x] Kiểm tra phân biệt Chuyển chế độ (Mode switch) vs Chuyển ngữ cảnh tiến trình (Context switch).
- [x] Bổ sung & làm rõ Memory Barrier trong Chương 5.
- [x] Bổ sung & làm rõ Swapping trong Chương 7.
- [x] Kiểm tra mô hình printf blocking trong bài tập trạng thái tiến trình (ghi chú quy ước lớp học).
- [x] Kiểm tra phụ lục Linux Lab mô tả chính xác nội dung thực tế.
- [x] Kiểm tra cây fork(), tính không xác định của output (nondeterministic), exec, wait.
- [x] Kiểm tra thuật toán định thời CPU (FCFS, SJF, SRTF, RR, HRRN, MQ, MLFQ).
- [x] Kiểm tra giải thuật đồng bộ (mutex, semaphore, Producer-Consumer, Readers-Writers, Dining Philosophers).
- [x] Kiểm tra thuật toán Banker (Need = Max - Alloc, Available, Work, Finish, Unsafe != Deadlock).
- [x] Kiểm tra quản lý bộ nhớ & bộ nhớ ảo (Paging, TLB, EAT, FIFO, OPT, LRU, Belady anomaly).

### 3. Tự Động Hóa & Build Pipeline [HOÀN TẤT]
- [x] Chuẩn hóa `scripts/build.js` và `scripts/build.ps1` với đường dẫn tương đối.
- [x] Chuẩn hóa `scripts/validate.py` và `scripts/validate.ps1`.
- [x] Tạo `scripts/generate_previews.py` để trích xuất ảnh xem trước từ PDF thật.

### 4. Tài Liệu Hướng Dẫn & Bộ Tài Liệu Xuất Bản [CHỜ XỬ LÝ]
- [x] Tạo `docs/BUILD.md`.
- [x] Tạo `docs/METHODOLOGY.md`.
- [x] Tạo `docs/PROJECT_HISTORY.md`.
- [x] Tạo `NOTICE.md` và `CHANGELOG.md`.
- [x] Tạo `README.md` ấn tượng cho GitHub.

### 5. Kiểm Thử & Kiểm Toán Trước Bàn Giao (Pre-Codex QA Gate) [CHỜ XỬ LÝ]
- [x] Chạy bộ test suite `validate.py` (HTML, PDF, Metadata, Formulas, No Secrets).
- [x] Lập báo cáo `reports/PRE_CODEX_AUDIT.md` (Đạt $\ge 92/100$).
- [x] Lập `RELEASE_CHECKLIST.md`.

### 6. Git & Phát Hành [CHỜ XỬ LÝ]
- [x] Khởi tạo Git repo nhánh `release/it007-handbook-v1`.
- [x] Commit các tệp tin an toàn với thông điệp rõ ràng.
- [x] Đẩy nhánh `release/it007-handbook-v1` lên `https://github.com/Phuchello/HDH_UIT`.
- [x] Cập nhật `PROJECT_STATE.md` sang trạng thái `READY_FOR_CODEX_FINAL_GITHUB_AUDIT` và dừng lại bàn giao.
- [x] Release hardening: canonical build paths, public claims, clean rebuild and validation have been refreshed; pending action is CI confirmation after publish.

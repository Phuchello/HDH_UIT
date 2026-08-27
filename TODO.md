# TODO — HDH_UIT V2 MASTER RECONSTRUCTION

## Giai Đoạn 1: Nghiên Cứu & Đối Chiếu Nguồn Học Thuật (Research & Evidence Gates)
- [x] Tạo nhánh an toàn `v2/complete-theory-labs` từ `main`.
- [x] Khảo sát và phân loại toàn bộ tài nguyên Tier A (Slide Week 1–14, Docx Bài tập Ch1–Ch9, Lab 1–6, Đề thi BHT CNPM 2017–2025).
- [ ] Lập `research/SOURCE_LEDGER.md` (Toàn bộ nguồn Tier A, B, C).
- [ ] Lập `research/SLIDE_COVERAGE_MATRIX.md` (Kiểm kê 100% tiêu đề, nội dung từng slide từ Week 1 đến Week 14).
- [ ] Lập `research/THEORY_COVERAGE_MATRIX.md` (Bản đồ ánh xạ nội dung Sách Lý Thuyết V2).
- [ ] Lập `research/OFFICIAL_REVIEW_QUESTION_MAP.md` (Bảng phân tích 100% câu hỏi ôn tập chính thức từ thầy Phan Đình Duy và Midterm Review).
- [ ] Lập `research/EXAM_EVIDENCE_MATRIX.md` (Phân loại dạng bài thi tự luận/trắc nghiệm theo bằng chứng thực tế).
- [ ] Lập `research/EXAM_PATTERN_ANALYSIS.md` (Phân tích tần suất và xu hướng đề thi).
- [ ] Lập `research/LAB_VARIANT_MAP.md` (Bản đồ biến thể bài Lab qua các học kỳ: Lab Memory vs Lab Shell `it007sh`).
- [ ] Lập `research/LAB_SOURCE_LEDGER.md` (Chỉ mục tài liệu kỹ thuật POSIX/Linux man pages cho thực hành).
- [ ] Lập `research/CONTENT_GAP_REPORT.md` (Báo cáo chi tiết khoảng cách giữa bản thảo V1 và yêu cầu toàn diện V2).

## Giai Đoạn 2: Tái Cấu Trúc Sách Lý Thuyết (Book A — Theory)
- [ ] Tái cấu trúc thư mục `src/theory/` và `src/shared/`.
- [ ] Soạn thảo Phần 0: Bản đồ môn học & Kỹ năng nền tảng.
- [ ] Soạn thảo Chương 1: Tổng quan về Hệ điều hành (Bổ sung đầy đủ Hệ đa xử lý, Cluster, Hệ phân tán, Storage hierarchy, Dual mode, Timer, Đơn chương/Đa chương/Đa nhiệm, Real-time).
- [ ] Soạn thảo Chương 2: Cấu trúc Hệ điều hành (Bổ sung đầy đủ OS Components, OS Services, System Programs phân loại 6 nhóm, System Call mechanism, Architecture models).
- [ ] Soạn thảo Chương 3: Quản lý Tiến trình (Bổ sung PCB chi tiết, Trạng thái & luồng chuyển, Cây fork, IPC Shared Memory & Message Passing, POSIX Threads, Mô hình đa luồng).
- [ ] Soạn thảo Chương 4: Định thời CPU (Bổ sung Thread scheduling PCS/SCS, Multiprocessor scheduling, Processor Affinity, Load balancing, Real-time scheduling, Linux CFS, Windows scheduler).
- [ ] Soạn thảo Chương Midterm Review: Bảng đặc tính lý thuyết, câu hỏi ngắn, bài tập chuyển trạng thái và Gantt chart.
- [ ] Soạn thảo Chương 5: Đồng bộ Tiến trình (Bổ sung 3 yêu cầu CS, Peterson, Hardware TestAndSet/CompareAndSwap, Memory Barrier, Mutex, Semaphore, Monitor, Condition Variables, 3 bài toán kinh điển).
- [ ] Soạn thảo Chương 6: Deadlock (Bổ sung 4 điều kiện Coffman, RAG, Banker Algorithm, Prevention, Detection, Recovery, Unsafe != Deadlock).
- [ ] Soạn thảo Chương 7: Quản lý Bộ nhớ (Bổ sung Dynamic relocation, MMU, Fixed/Dynamic partitioning, Placement, Paging, TLB, EAT, Swapping).
- [ ] Soạn thảo Chương 8: Bộ nhớ ảo (Bổ sung Demand Paging, Page Fault step-by-step, FIFO, OPT, LRU, Frame allocation, Thrashing, Working set, Belady anomaly).
- [ ] Soạn thảo Chương 9: Linux & Windows Architecture (Nguyên lý thiết kế, Cấu trúc nhân, Quản lý tiến trình, Định thời, IPC, Quản lý bộ nhớ).
- [ ] Soạn thảo Chương Final Review: 02 Đề thi mô phỏng cuối kỳ kèm đáp án chi tiết.

## Giai Đoạn 3: Biên Soạn Sách Thực Hành Độc Lập (Book B — Lab Manual)
- [ ] Tái cấu trúc thư mục `src/lab/`.
- [ ] Soạn thảo Phần Mở Đầu: Hướng dẫn môi trường Linux, Linux Terminal, GCC, GDB, Strace, Makefile.
- [ ] Soạn thảo Lab 1: Giới thiệu Linux & Lệnh cơ bản.
- [ ] Soạn thảo Lab 2: Lập trình Shell Scripting (Bash).
- [ ] Soạn thảo Lab 3: Quản lý Tiến trình & Signal (`fork`, `exec`, `wait`, `kill`, `signal`).
- [ ] Soạn thảo Lab 4: Đa luồng & Giao tiếp Liên tiến trình (`pthread`, `shmget`/`shmat`, `pipe`).
- [ ] Soạn thảo Lab 5: Đồng bộ Tiến trình & Luồng (POSIX Semaphore, Mutex).
- [ ] Soạn thảo Lab 6 Case Study: Xây dựng Trình thông dịch lệnh `it007sh` hoàn chỉnh 7 giai đoạn.

## Giai Đoạn 4: Kiểm Thử Đối Kháng & Bàn Giao Codex
- [ ] Kiểm tra 0 đề cập AI/marketing.
- [ ] Kiểm tra 100% câu hỏi ôn tập chính thức có lời giải.
- [ ] Lập `research/V2_CONTENT_AUDIT.md` và `CODEX_V2_HANDOFF.md`.
- [ ] Chốt trạng thái `V2_CONTENT_LOCKED_READY_FOR_CODEX` và commit đẩy lên GitHub.

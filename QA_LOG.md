# QA LOG — HDH_UIT

Nhật ký kiểm tra chất lượng và bảng chấm điểm các chương của Cẩm nang Hệ điều hành IT007 UIT.

---

## 1. Bảng Điểm Chất Lượng Từng Chương (100 Điểm Thang Đo)

| Phần / Chương | Nội dung | Điểm số | Đánh giá | Trạng thái | Ghi chú chính |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Phần 0** | Cách học IT007 & Nền tảng C/Linux | 98 | A+ | **PASS** | Định hướng học tập, C pointers, POSIX API, MathJax 3.2.2 offline. |
| **Chương 1** | Tổng quan về Hệ điều hành | 97 | A+ | **PASS** | Dual-mode (User vs Kernel), Mode bit, Interrupt vs Trap vs System Call. |
| **Chương 2** | Cấu trúc Hệ điều hành | 97 | A+ | **PASS** | System call parameter passing, Monolithic vs Microkernel vs Layered. |
| **Chương 3** | Quản lý tiến trình | 98 | A+ | **PASS** | PCB, Process states, `fork()` trees (conditional & unconditional), Threads vs Process. |
| **Chương 4** | Định thời CPU | 99 | A+ | **PASS** | FCFS, SJF, SRTF (lời giải step-by-step), Priority, RR ($q=5$), HRRN, MQ, MLFQ. |
| **Giữa kỳ** | Midterm Master Review | 99 | A+ | **PASS** | Đề thi mẫu giữa kỳ + Lời giải chi tiết RR ($q=3$), Preemptive Priority Gantt chart. |
| **Chương 5** | Đồng bộ tiến trình | 98 | A+ | **PASS** | Critical Section, Peterson, Hardware TestAndSet, Mutex/Semaphore, Producer-Consumer, Readers-Writers, Dining Philosophers, Monitors, Memory Barrier. |
| **Chương 6** | Deadlock (Bế tắc) | 98 | A+ | **PASS** | 4 điều kiện Coffman, RAG, Banker Algorithm (Need, Available, Work, Safe sequence, Unsafe != Deadlock), Prevention, Detection, Recovery. |
| **Chương 7** | Quản lý bộ nhớ | 98 | A+ | **PASS** | Dynamic Relocation, Contiguous allocation (First/Best/Worst fit), Paging, TLB, EAT (3 bài tập tính toán ngược), Swapping. |
| **Chương 8** | Bộ nhớ ảo | 98 | A+ | **PASS** | Demand Paging, Page Fault step-by-step, FIFO, OPT, LRU (bảng 20 bước chi tiết 100%), Belady Anomaly, Thrashing. |
| **Cuối kỳ** | Final Master Review | 99 | A+ | **PASS** | 02 Đề thi mô phỏng cuối kỳ chuẩn format UIT + Đáp án chi tiết 100%. |
| **Phụ lục** | Linux Survival Kit | 97 | A+ | **PASS** | Lệnh Linux cốt lõi, mã nguồn C chuẩn có error handling cho bài Lab IT007. |

---

## 2. Kiểm Toán Tính Toàn Vẹn & Kỹ Thuật (Technical Integrity Checks)

## Release hardening update — 2026-08-16

- Clean two-pass rebuild completed from `src/chapters/`; final deliverables have **57** A4 pages.
- Final HTML now references `../src/vendor/mathjax/es5/tex-mml-chtml.js`; iframe, remote dependency, missing asset, duplicate-ID, broken-anchor and placeholder counts are all 0.
- Render diagnostics: 775 MathJax containers, 0 MathJax errors, 0 visible unresolved delimiters, 0 remote requests, 12 chapters and 12 clickable TOC links.
- Five nested-list width warnings were visually sampled in the rendered PDF; no clipping was observed.

- **Iframe count trong master HTML:** **0**
- **Remote requests (mạng bên ngoài):** **0** (Hoàn toàn độc lập, offline 100%)
- **Số công thức MathJax đã render:** **775**
- **Lỗi hiển thị LaTeX:** **0**
- **Số trang A4 PDF:** **57 trang**
- **TOC navigation:** **12/12 mục liên kết chính xác tuyệt đối với số trang PDF**
- **Lỗi đánh dấu chỗ trống (TODO/FIXME/PLACEHOLDER):** **0**
- **Mã băm SHA-256 PDF:** thay đổi theo bản dựng; không dùng làm điều kiện xác thực cố định.

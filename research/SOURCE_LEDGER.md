# SỔ TAY NGUỒN HỌC THUẬT & TÀI LIỆU THAM KHẢO (SOURCE LEDGER)

Tài liệu này quản lý, phân cấp và ghi nhận toàn bộ các nguồn tư liệu học thuật, tài liệu giảng dạy chính thức của UIT, tiêu chuẩn kỹ thuật quốc tế và bằng chứng thực tế phục vụ quá trình tái thiết lập V2 cho hai ấn phẩm: **Sách Lý Thuyết IT007** và **Sách Thực Hành IT007**.

---

## 1. Phân Tầng Thẩm Quyền Nguồn (Evidence & Authority Hierarchy)

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER A: NGUỒN CHÍNH THỨC XÁC LẬP PHẠM VI IT007 UIT                     │
│ (Đề cương môn học, Slide bài giảng 14 tuần, Bộ câu hỏi & bài tập       │
│  chương của Khoa KTMT, Slide Ôn tập Giữa kỳ, Hướng dẫn Lab 1-6)        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Quy định phạm vi kiến thức & cách diễn đạt
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER B: NGUỒN THẨM QUYỀN KỸ THUẬT QUỐC TẾ & CHUẨN KERNEL/POSIX         │
│ (Operating System Concepts - Silberschatz, POSIX.1-2017 / The Open     │
│  Group, Linux Man-pages man7.org, GNU C Library / Bash Docs, MSDN)     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Bảo đảm tính chính xác kỹ thuật 100%
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER C: BẰNG CHỨNG ĐỀ THI & BIẾN THỂ THỰC HÀNH THỰC TẾ                 │
│ (Đề thi BHT CNPM 2017–2025, Duong Computing, SVUIT, Lab Reports)      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Danh Mục Nguồn Tier A (Authoritative for IT007 UIT)

| Mã nguồn | Tên tài liệu / Tệp tin | Nguồn gốc / Tác giả | Học kỳ / Năm | Phân loại | Nội dung / Chuyên đề hỗ trợ |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **A-01** | `IT007_HeDieuHanh_14.2024.pdf` (19 trang) | Khoa Kỹ thuật Máy tính – UIT | 2024–2025 | Đề cương chính thức (Canonical Outline) | Đề cương chi tiết học phần IT007 Hệ điều hành năm học 2024–2025 (tạo ngày 2024-09-11). Quy định cấu trúc 9 chương, chuẩn đầu ra (CLO), thang điểm đánh giá. Phân phối Chương 6 tại Buổi 8 (slide week 8) và Chương 7 Quản lý bộ nhớ tại Buổi 9 với bộ slide week 9: 7.1 Khái niệm cơ sở, 7.2 Các loại địa chỉ nhớ, 7.3 Chuyển đổi giữa các loại địa chỉ nhớ, 7.4 Cấp phát liên tục (7.4.1 Phân vùng tĩnh, 7.4.1 Phân vùng động [lỗi lặp số thứ tự trong đề cương gốc, chuẩn hóa 7.4.2]), 7.5 Cơ chế phân trang, 7.6 Cơ chế swapping, 7.7 Bài tập. |
| **A-01-VARIANT** | `De cuong.pdf` (19 trang) | Khoa Kỹ thuật Máy tính – UIT | 2023 | Biến thể đề cương cũ (Historical Variant) | Đề cương học phần phiên bản cũ (tạo ngày 2023-03-29); lưu giữ dưới dạng biến thể lịch sử `UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG`, không dùng làm căn cứ thẩm quyền chính thức. |
| **A-02** | `Week01-Chapter1 2024.pdf` (57 slides) | Giảng viên IT007 UIT | 2024 | Slide | Tổng quan HDH, Kiến trúc máy tính, Ngắt, Phân cấp bộ nhớ, Cấu trúc bộ xử lý, Dual Mode, Đơn chương/Đa chương/Đa nhiệm, Real-time. |
| **A-03** | `Week02-Chapter2 2024.pdf` (57 slides) | Giảng viên IT007 UIT | 2024 | Slide | Thành phần HDH, Dịch vụ HDH, System Calls, Truyền tham số, System Programs (6 nhóm), Kiến trúc HDH (Monolithic, Layered, Microkernel, Modules). |
| **A-04** | `Week03-Chapter3 2024.pdf` (64 slides) | Giảng viên IT007 UIT | 2024 | Slide | Khái niệm tiến trình, Memory layout, 5 trạng thái & luồng chuyển, PCB, Hàng đợi định thời, Scheduler, Context switch, `fork()`, `exec()`, `wait()`, IPC (Shared Memory, Message Passing), Luồng (Threads). |
| **A-05** | `#Week04-Chapter4-1 2024.pdf` (74 slides) | Giảng viên IT007 UIT | 2024 | Canonical Slide | Động cơ định thời, CPU-I/O Burst Cycle, CPU Scheduler, Dispatcher, Tiêu chuẩn định thời ($TAT, WT, RT$), Giải thuật FCFS, SJF, SRTF, Priority. (`UIT-SLIDE-CH04-1-2024`). |
| **A-05-VARIANT-56** | `Week04-Chapter4-1 2024.pdf` (56 slides) | Giảng viên IT007 UIT | 2024 | Local source variant | Biến thể cục bộ cũ 56 trang (`UIT-SLIDE-CH04-1-2024-VARIANT-LOCAL-56`), loại khỏi phạm vi chính thức. |
| **A-06** | `#Week05-Chapter4-2 2024.pdf` (59 slides) | Giảng viên IT007 UIT | 2024 | Canonical Slide | Giải thuật Round Robin (Quantum), HRRN, Multilevel Queue (MQ), Multilevel Feedback Queue (MLFQ), định thời đa xử lý, realtime. (`UIT-SLIDE-CH04-2-2024`). |
| **A-06-VARIANT-34** | `Week05-Chapter4-2 2024.pdf` (34 slides) | Giảng viên IT007 UIT | 2024 | Local source variant | Biến thể cục bộ cũ 34 trang (`UIT-SLIDE-CH04-2-2024-VARIANT-LOCAL-34`), loại khỏi phạm vi chính thức. |
| **A-07-VARIANT** | `Week06-Chapter4-3 2024.pdf` (46 slides) | Giảng viên IT007 UIT | 2024 | Local source variant | Biến thể cục bộ cũ 46 trang (`UIT-SLIDE-CH04-3-2024-VARIANT-LOCAL-46`), loại khỏi phạm vi chính thức. |
| **A-08** | `#Week06-Chapter5-1 2024.pdf` (67 slides) | Giảng viên IT007 UIT | 2024 | Canonical Slide | Vấn đề tranh chấp (Race condition), Vùng tranh chấp (Critical Section), 3 điều kiện đúng, Giải pháp phần mềm: Peterson, Khóa phần cứng: TestAndSet, CompareAndSwap, Memory Barrier (Self-study p.56), Mutex Locks, Semaphores. (`UIT-SLIDE-CH05-1-2024`). |
| **A-08-VARIANT-58** | `Week07-Chapter5-1 2024.pdf` (58 slides) | Giảng viên IT007 UIT | 2024 | Local source variant | Biến thể cục bộ cũ 58 trang (`UIT-SLIDE-CH05-1-2024-VARIANT-LOCAL-58`), loại khỏi phạm vi chính thức. |
| **A-09** | `#Week08-Midterm Review.pptx` (17 slides) | Khoa KTMT – UIT | 2024 | Canonical user attachment | Khung ma trận ôn tập giữa kỳ Ch1–Ch4, state/fork exercises và scheduling; SHA256 được ghi trong registry (`UIT-SLIDE-MIDTERM-REVIEW-2024`). |
| **A-09-VARIANT-16** | `Week08-Midterm Review.pdf` (16 slides) | Khoa KTMT – UIT | 2024 | Local source variant | Biến thể PDF 16 trang cũ (`UIT-SLIDE-MIDTERM-REVIEW-2024-VARIANT-LOCAL-16PDF`), không thay thế bản PPTX 17 slide. |
| **A-10** | `#Week07-Chapter5-2 2024.pdf` (72 slides) | Giảng viên IT007 UIT | 2024 | Canonical Slide | Bài toán Bounded Buffer, Readers-Writers, Dining Philosophers, Giám sát viên (Monitors), Liveness, Deadlock/Starvation trong đồng bộ, Priority Inversion & Priority Inheritance protocol. (`UIT-SLIDE-CH05-2-2024`). |
| **A-10-VARIANT-55** | `Week09-Chapter5-2 2024.pdf` (55 slides) | Giảng viên IT007 UIT | 2024 | Local source variant | Biến thể cục bộ cũ 55 trang (`UIT-SLIDE-CH05-2-2024-VARIANT-LOCAL-55`), loại khỏi phạm vi chính thức. |
| **A-11-VARIANT-32** | `Week10-Chapter5-3 2024.pdf` (32 slides) | Giảng viên IT007 UIT | 2024 | Local source variant | Biến thể cục bộ cũ 32 trang (`UIT-SLIDE-CH05-3-2024-VARIANT-LOCAL-32`), loại khỏi phạm vi chính thức vì bản canonical Part 2 (72 trang) đã bao hàm Monitors và bài toán kinh điển. |
| **A-12** | `#Week08-Chapter6 2024.pdf` (67 slides) | Giảng viên IT007 UIT (Trần Hoàng Lộc & Nguyễn Thanh Thiện) | 2024 | Canonical Slide | Mô hình tài nguyên, 4 điều kiện Coffman, Đồ thị RAG, Phòng tránh Deadlock (Prevention), Tránh Deadlock (Avoidance), Trạng thái an toàn, Thuật toán Banker, Phát hiện & Phục hồi Deadlock. (`UIT-SLIDE-CH06-2024`). |
| **A-12-VARIANT-WEEK11** | `Week11-Chapter6 2024.pdf` (67 slides) | Giảng viên IT007 UIT (Trần Hoàng Lộc & Nguyễn Thanh Thiện) | 2024 | Local source variant | Biến thể Tuần 11 cũ từ học kỳ trước (`UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB`). |
| **A-13** | `#Week09-Chapter7 2024.pdf` (72 slides) | Giảng viên IT007 UIT (Trần Hoàng Lộc & Nguyễn Thanh Thiện) | 2024 | Canonical Slide | Không gian địa chỉ Logic vs Vật lý, Ràng buộc địa chỉ, MMU, Cấp phát liên tục (First/Best/Worst/Next fit), Phân mảnh nội/ngoại, Phân trang (Paging), Bảng trang, TLB, EAT, Bảng trang 2 cấp/Băm/Nghịch đảo, Bảo vệ & chia sẻ trang, Hoán đổi (Swapping). Khớp chuẩn Tuần 9 theo Đề cương 2024 (`UIT-SLIDE-CH07-2024`). |
| **A-13-VARIANT-WEEK12** | `Week12-Chapter7 2024.pdf` (72 slides) | Giảng viên IT007 UIT (Trần Hoàng Lộc & Nguyễn Thanh Thiện) | 2024 | Local source variant | Biến thể xuất sớm ngày 2024-02-15 với tên tệp Week12 từ học kỳ trước; mắc lỗi kerning/dính khoảng trắng tại 11 trang so với bản Week09 chính thức (`UIT-SLIDE-CH07-2024-VARIANT-WEEK12-72`). |
| **A-14** | `Week13-Chapter8 2024.pdf` (50 slides) | Giảng viên IT007 UIT | 2024 | Slide | Bộ nhớ ảo, Nạp trang theo yêu cầu (Demand Paging), Xử lý lỗi trang (Page Fault), Thuật toán thay thế trang (FIFO, OPT, LRU), Cấp phát khung trang, Nghẽn bộ nhớ (Thrashing), Mô hình Working Set, Belady Anomaly. |
| **A-15** | `Week14-Chapter9 2024.pdf` (57 slides) | Giảng viên IT007 UIT | 2024 | Slide | Nghiên cứu điển hình: Kiến trúc Linux (Lịch sử, Thiết kế, Task struct, CFS, VFS, Buddy allocator) & Kiến trúc Windows (Win32 API, HAL, Kernel, Executive, Process/Thread, VMM). |
| **A-16** | `Cau hoi chuong 1 HDH.docx` (11 mục) | ThS. Phan Đình Duy – UIT | 2024 | Bộ câu hỏi | Bộ câu hỏi tự luận chuẩn hóa ôn tập Chương 1. |
| **A-17** | `Cau hoi chuong 2 HDH.docx` (10 mục) | ThS. Phan Đình Duy – UIT | 2024 | Bộ câu hỏi | Bộ câu hỏi tự luận chuẩn hóa ôn tập Chương 2. |
| **A-18** | `Bai tap chuong 3 HDH.docx` (159 đoạn) | ThS. Phan Đình Duy – UIT | 2024 | Bộ bài tập | Câu hỏi lý thuyết + Bài tập chuyển trạng thái + Bài tập cây `fork()` Chương 3. |
| **A-19** | `Bai tap chuong 4 HDH.docx` (258 đoạn) | Khoa KTMT – UIT | 2024 | Bộ bài tập | Câu hỏi lý thuyết + Bài tập định thời CPU chi tiết (FCFS, SJF, SRTF, RR, Priority, HRRN). |
| **A-20** | `Bai tap chuong 5 HDH.docx` (128 đoạn) | Khoa KTMT – UIT | 2024 | Bộ bài tập | Câu hỏi lý thuyết + Bài tập lập trình giải thuật đồng bộ Semaphore/Mutex. |
| **A-21** | `Bai tap chuong 6 HDH.docx` (560 đoạn) | Khoa KTMT – UIT | 2024 | Bộ bài tập | Câu hỏi lý thuyết + Bài tập đồ thị RAG + Bài tập thuật toán Banker đa dạng kịch bản. |
| **A-22** | `Bai tap chuong 7 HDH.docx` (20 đơn vị nguồn, 88 đoạn XML) | Khoa KTMT – UIT | 2024 | Bộ bài tập chính thức | Bộ câu hỏi và bài tập Chương 7 chính thức đầy đủ 20 đơn vị nguồn (9 lý thuyết + 11 bài tập), SHA-256 `5b03f4e0...` (`UIT-QBANK-CH07-2024`). |
| **A-22-VARIANT-DRIVE** | `Bai tap chuong 7 HDH.docx` (85 đoạn) | Khoa KTMT – UIT | 2024 | Local source variant | Bản tải sớm từ Drive (SHA-256 `f8e523d1...`), bị cắt ngắn tại câu hỏi số 18, thiếu bài tập 19 và 20 (`UIT-QBANK-CH07-2024-VARIANT-DRIVE-85P`). |
| **A-23** | `Bai tap chuong 8 HDH.docx` (329 đoạn) | Khoa KTMT – UIT | 2024 | Bộ bài tập | Câu hỏi lý thuyết + Bài tập bảng thay thế trang 20 bước (FIFO, OPT, LRU, Working Set). |
| **A-24** | `Cau hoi chuong 9 HDH.docx` (7 mục) | Khoa KTMT – UIT | 2024 | Bộ câu hỏi | Bộ câu hỏi tự luận nghiên cứu Linux & Windows. |
| **A-25** | `Lab 1 v2023.pdf` – `Lab 6 v2023.pdf` | Bộ môn HTTT & KTMT – UIT | 2023–2024 | Hướng dẫn Lab | Tài liệu thực hành chính thức: Cài đặt, Shell script, Process, Threads & IPC, Synchronization, Shell `it007sh`. |

---

## 3. Danh Mục Nguồn Tier B (Technical Authority)

| Mã nguồn | Tên tài liệu / Tiêu chuẩn | Tổ chức / Tác giả | Phiên bản / URL | Mục đích áp dụng |
| :--- | :--- | :--- | :--- | :--- |
| **B-01** | *Operating System Concepts* (10th Ed.) | Silberschatz, Galvin, Gagne | Wiley, 2018 | Chuẩn hóa thuật ngữ khoa học máy tính, sơ đồ kiến trúc và giải thuật nền tảng. |
| **B-02** | *Operating Systems: Three Easy Pieces* (OSTEP) | Remzi H. Arpaci-Dusseau & Andrea C. Arpaci-Dusseau | Arpaci-Dusseau Books, 2018 | Trực giác sâu sắc về Virtualization, Concurrency và Persistence. |
| **B-03** | IEEE Std 1003.1-2017 (POSIX.1-2017) | The Open Group / IEEE | `https://pubs.opengroup.org/onlinepubs/9699919799/` | Đặc tả chuẩn các hàm POSIX C API: `fork`, `exec`, `waitpid`, `pipe`, `dup2`, `pthread`, `sem_init`. |
| **B-04** | Linux Manual Pages (man7.org) | Michael Kerrisk et al. | `https://man7.org/linux/man-pages/` | Hành vi chính xác của Linux System Calls và C Library functions. |
| **B-05** | GNU C Library (glibc) Manual | Free Software Foundation | `https://www.gnu.org/software/libc/manual/` | Hành vi quản lý bộ đệm I/O (`printf`, `stdout`), bộ nhớ `malloc`/`mmap`. |
| **B-06** | GNU Bash Reference Manual | Free Software Foundation | `https://www.gnu.org/software/bash/manual/` | Chuẩn cú pháp và hành vi lập trình Shell script (Lab 2). |
| **B-07** | Linux Kernel Documentation | The Linux Kernel Organization | `https://docs.kernel.org/` | Tài liệu kiến trúc nhân Linux: CFS Scheduler, VFS, Memory Management (Chương 9 & Lab). |
| **B-08** | Windows Internals (7th Ed.) | Pavel Yosifovich, Mark Russinovich et al. | Microsoft Press | Tài liệu kiến trúc nhân Windows, luồng thực thi, cơ chế định thời 32 mức ưu tiên. |

---

## 4. Danh Mục Nguồn Tier C (Exam & Lab Evidence)

| Mã nguồn | Tên tài liệu | Đơn vị tổ chức | Học kỳ / Năm | Loại đề | Ghi chú bằng chứng |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **C-01** | `[BHT CNPM] HDH 2018-2019 GK1` | Ban Hỗ Trợ Học Tập CNPM – UIT | HK1 2018-2019 | Giữa kỳ | Đề tự luận + Lời giải chi tiết: Trạng thái tiến trình, Cây `fork()`, Định thời CPU (FCFS, SJF, RR). |
| **C-02** | `[BHT CNPM] HDH 2020-2021 GK1` | BHT CNPM – UIT | HK1 2020-2021 | Giữa kỳ | Đề thi giữa kỳ có cấu trúc 3 câu: Lý thuyết ngắt/dual-mode, Cây `fork()` 3 tầng, Định thời CPU. |
| **C-03** | `[BHT CNPM] HDH 2020-2021 GK2` | BHT CNPM – UIT | HK2 2020-2021 | Giữa kỳ | Đề thi trắc nghiệm kết hợp tự luận tính toán $TAT, WT$. |
| **C-04** | `[BHT CNPM] HDH 2022-2023 GK1` | BHT CNPM – UIT | HK1 2022-2023 | Giữa kỳ | Đề thi giữa kỳ: Câu hỏi đặc điểm ngắt, phân biệt process/thread, bài tập SRTF có thời gian đến khác nhau. |
| **C-05** | `[BHT CNPM] HDH 2022-2023 GK2` | BHT CNPM – UIT | HK2 2022-2023 | Giữa kỳ | Đề thi giữa kỳ: Phân tích lệnh đặc quyền, bài tập `fork()` lồng điều kiện `if`, định thời Priority Preemptive. |
| **C-06** | `[BHT CNPM] HDH 2023-2024 GK1` | BHT CNPM – UIT | HK1 2023-2024 | Giữa kỳ | Đề thi giữa kỳ có đáp án: Khảo sát chi tiết bảng chuyển trạng thái có `printf`. |
| **C-07** | `[BHT CNPM] HDH 2023-2024 GK2` | BHT CNPM – UIT | HK2 2023-2024 | Giữa kỳ | Đề thi giữa kỳ chuẩn hóa mới nhất. |
| **C-08** | `[BHT CNPM] HDH 2024-2025 GK1` | BHT CNPM – UIT | HK1 2024-2025 | Giữa kỳ | Đề thi giữa kỳ cập nhật năm học gần nhất. |
| **C-09** | `[BHTCNPM] HDH 2017-2018 CK2` | BHT CNPM – UIT | HK2 2017-2018 | Cuối kỳ | Đề thi cuối kỳ: Semaphore Producer-Consumer, Thuật toán Banker, Thay thế trang LRU. |
| **C-10** | `[BHTCNPM] HDH 2018-2019 CK2` | BHT CNPM – UIT | HK2 2018-2019 | Cuối kỳ | Đề thi cuối kỳ: Bài toán Readers-Writers, Banker xử lý yêu cầu $Request_i$, Phân mảnh bộ nhớ. |
| **C-11** | `[BHTCNPM] HDH 2019-2020 CK1 (Đề 1, 2, 3)` | BHT CNPM – UIT | HK1 2019-2020 | Cuối kỳ | Bộ 3 đề thi cuối kỳ song song: Đồ thị RAG có chu trình, Tính EAT với TLB 2 cấp, Thay thế trang OPT. |
| **C-12** | `[BHTCNPM] HDH 2020-2021 CK1 (Có đáp án)` | BHT CNPM – UIT | HK1 2020-2021 | Cuối kỳ | Đề thi cuối kỳ đầy đủ barem chấm: Đồng bộ Dining Philosophers, Banker 4 loại tài nguyên, LRU 20 tham chiếu. |
| **C-13** | `[BHTCNPM] HDH 2022-2023 CK1 & CK2` | BHT CNPM – UIT | 2022–2023 | Cuối kỳ | Đề thi cuối kỳ: Đồng bộ xe qua cầu (One-way bridge), EAT tính ngược tỉ lệ hit TLB, Belady anomaly. |
| **C-14** | `[BHTCNPM] HDH 2023-2024 CK1 & CK2` | BHT CNPM – UIT | 2023–2024 | Cuối kỳ | Đề thi cuối kỳ cập nhật: Bài toán đồng bộ Semaphore nhiều điều kiện, Thuật toán thay thế trang có dirty bit. |
| **C-15** | `[BHTCNPM] HDH 2024-2025 CK1` | BHT CNPM – UIT | HK1 2024-2025 | Cuối kỳ | Đề thi cuối kỳ mới nhất. |
| **C-16** | *Duong Computing IT007 Exam Solution Series* | Kênh Duong Computing | 2020–2024 | Video | Bằng chứng về phương pháp giảng giải và các bẫy đề thi sinh viên hay mắc phải. |
| **C-17** | *Tài liệu Lập trình Shell & Ubuntu Reference* | BHT CNPM – UIT | 2020 | Hướng dẫn | Tổng hợp lệnh Linux thực hành và mẫu bài tập Shell. |

---

## 5. Nhật Ký Đồng Bộ & Khắc Phục Bất Đồng Nhất (Audit & SSOT Sync Log)

- `GLOBAL-SRC-001` — **RESOLVED (MAJOR)**: Đồng bộ danh mục nguồn Tier A với sổ đăng ký bất biến `content/sources/registry.yaml`:
  - **Lý do (Reason):** Bảng Tier A trong Sổ tay nguồn ban đầu lưu các biến thể cục bộ cũ của Chương 4 và Chương 5 (56/34/46 trang cho Ch4 và 58/55/32 trang cho Ch5) sau khi các bản đính kèm chính thức người dùng (`#Week04`, `#Week05`, `#Week06`, `#Week07`) đã được xác lập làm chuẩn bất biến.
  - **Khắc phục (Resolution):**
    - Cập nhật **A-05** thành `#Week04-Chapter4-1 2024.pdf` (74 trang) — `UIT-SLIDE-CH04-1-2024`.
    - Cập nhật **A-06** thành `#Week05-Chapter4-2 2024.pdf` (59 trang) — `UIT-SLIDE-CH04-2-2024`.
    - Phân loại rõ các tệp 56, 34, 46 trang thành biến thể cục bộ (`A-05-VARIANT-56`, `A-06-VARIANT-34`, `A-07-VARIANT-46`).
    - Cập nhật **A-08** thành `#Week06-Chapter5-1 2024.pdf` (67 trang) — `UIT-SLIDE-CH05-1-2024`.
    - Cập nhật **A-10** thành `#Week07-Chapter5-2 2024.pdf` (72 trang) — `UIT-SLIDE-CH05-2-2024`.
    - Phân loại rõ các tệp 58, 55, 32 trang thành biến thể cục bộ (`A-08-VARIANT-58`, `A-10-VARIANT-55`, `A-11-VARIANT-32`), trong đó tệp 32 trang được loại khỏi phạm vi chính thức vì phần 2 chính thức (72 trang) đã bao hàm toàn bộ nội dung Monitors và bài toán kinh điển.
    - Bổ sung bộ kiểm tra tự động trong `scripts/validate_sources.py` bảo đảm bảng Tier A luôn đồng nhất 100% với `content/sources/registry.yaml`.


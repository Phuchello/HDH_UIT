# CURRICULUM MAP — HỆ ĐIỀU HÀNH IT007 UIT

Bản đồ môn học IT007 được thiết kế theo đúng Đề cương và Bài giảng chính thức của Trường Đại học Công nghệ Thông tin (UIT) - ĐHQG-HCM.

---

## BỐ CỤC TỔNG THỂ TÀI LIỆU

### PHẦN 0 — CÁCH HỌC IT007 & NỀN TẢNG CẦN BIẾT
- **Mục tiêu**: Định hướng tư duy từ học vẹt → hiểu bản chất; trang bị kỹ năng lập trình C trên Linux, làm việc với terminal, biên dịch GCC, và kỹ năng đọc đề thi UIT.
- **Nội dung trọng tâm**:
  1. Tư duy "Trực giác → Bản chất → Thuật toán → Bài tập → Lab → Đề thi".
  2. Nền tảng C/Linux: Con trỏ, Cấp phát bộ nhớ, System Call, Standard I/O vs System I/O.
  3. Cách vượt qua các bẫy quen thuộc trong đề thi IT007 UIT.

---

### CHƯƠNG 1 — TỔNG QUAN VỀ HỆ ĐIỀU HÀNH
- **Syllabus**: Khái niệm HDH, Chức năng, Phân loại HDH (Đơn chương, Đa chương, Chia sẻ thời gian, Real-time, Đa xử lý), Lịch sử phát triển, Cấu trúc hệ thống máy tính (CPU, RAM, Controller, Interrupt, Dual-mode, Memory Protection).
- **Trọng tâm bài thi/Lab**:
  - Phân biệt Đa chương (Multiprogramming) vs Chia sẻ thời gian (Time-sharing) vs Đa xử lý (Multiprocessing).
  - Luồng xử lý ngắt (Interrupt vector, ISR, Trap vs Hardware Interrupt).
  - Chế độ hoạt động Dual Mode (User mode vs Kernel mode), Chuyển đổi mode qua System Call / Interrupt.

---

### CHƯƠNG 2 — CẤU TRÚC HỆ ĐIỀU HÀNH
- **Syllabus**: Các thành phần chính của HDH (Process Management, Memory Management, Storage Management, I/O Management, Protection & Security), Dịch vụ HDH, System Calls (Lời gọi hệ thống), Chương trình hệ thống (System Programs), Cấu trúc HDH (Monolithic, Layered, Microkernel, Modular), Khái niệm Máy ảo (Virtual Machine).
- **Trọng tâm bài thi/Lab**:
  - Phân biệt Lời gọi hệ thống (System call) vs Hàm thư viện (Library call).
  - Cơ chế truyền tham số cho System Call.
  - So sánh kiến trúc Monolithic vs Microkernel.

---

### CHƯƠNG 3 — QUẢN LÝ TIẾN TRÌNH (PROCESS MANAGEMENT)
- **Syllabus**: Khái niệm Tiến trình (Process), Trạng thái tiến trình (New, Ready, Running, Waiting, Terminated), Khối quản lý tiến trình (PCB), Điều độ tiến trình (Process Scheduling Queues, Schedulers: Long-term, Short-term, Medium-term, Context Switch), Tương tác & Cộng tác giữa các tiến trình (IPC: Shared Memory, Message Passing), Tạo và kết thúc tiến trình (`fork`, `exec`, `wait`, `exit`), Khái niệm Tiểu trình (Thread).
- **Trọng tâm bài thi/Lab**:
  - **Bài tập trọng tâm thi Giữa kỳ**:
    1. Chuỗi chuyển trạng thái tiến trình khi chạy đoạn code C (New → Ready → Running → Waiting → Ready...).
    2. Cây tiến trình (Process Tree) & Tính số lượng tiến trình sinh ra bởi vòng lặp `fork()`.
    3. Output của đoạn chương trình chứa `fork()`, `execvp()`, `wait()`, `printf()` (Lưu ý bộ đệm `printf` buffer và Copy-on-Write).
    4. Địa chỉ ảo `&a` và giá trị `a` trong tiến trình cha và con.
  - **Lab Linux**: Sử dụng `fork()`, `execvp()`, `wait()`, `shm_open()`, `mmap()` trên Linux.

---

### CHƯƠNG 4 — ĐỊNH THỜI CPU (CPU SCHEDULING)
- **Syllabus**: Khái niệm Định thời CPU, Bộ định thời (Scheduler) & Trình điều phối (Dispatcher), Phí tổn Context Switch, Tiêu chuẩn định thời (CPU Utilization, Throughput, Turnaround Time, Waiting Time, Response Time), Các thuật toán định thời:
  - FCFS (First-Come, First-Served)
  - SJF (Shortest Job First - Non-preemptive)
  - SRTF (Shortest Remaining Time First - Preemptive SJF)
  - Priority Scheduling (Preemptive & Non-preemptive)
  - Round Robin (RR - với Quantum Time `q`)
  - HRRN (Highest Response Ratio Next - Mở rộng)
  - Multilevel Queue (MQ) & Multilevel Feedback Queue (MLFQ)
  - Định thời Đa xử lý (Multi-Processor Scheduling) & Real-time Scheduling (EDF, RMS - Mở rộng).
- **Trọng tâm bài thi/Lab**:
  - **Bài tập bắt buộc thi Giữa kỳ**:
    1. Vẽ sơ đồ Gantt chính xác theo từng mốc thời gian (Event-driven timeline).
    2. Tính chi tiết: Completion Time ($CT$), Turnaround Time ($TAT = CT - AT$), Waiting Time ($WT = TAT - BT$), Response Time ($RT = \text{First Exec Time} - AT$).
    3. So sánh hiệu năng giữa các thuật toán (SRTF tối ưu WT trung bình vs Round Robin tối ưu RT).
  - **Lab Linux**: Thuật toán Round Robin bằng C (`roundrobin.c`).

---

### MIDTERM MASTER REVIEW (ÔN THI GIỮA KỲ IT007)
- Hệ thống sơ đồ tư duy Chương 1–4.
- Bộ câu hỏi bẫy trắc nghiệm giữa kỳ UIT.
- Phương pháp giải nhanh bài tập Process Tree & CPU Scheduling.
- 01 Đề thi mô phỏng Giữa kỳ chuẩn cấu trúc UIT (Có đáp án & Lời giải chi tiết 100%).

---

### CHƯƠNG 5 — ĐỒNG BỘ TIẾN TRÌNH (PROCESS SYNCHRONIZATION)
- **Syllabus**: Vấn đề Race Condition (Tranh chấp dữ liệu), Vùng tranh chấp (Critical Section - CS), 3 yêu cầu của giải pháp CS (Mutual Exclusion, Progress, Bounded Waiting), Các giải pháp Busy Waiting (Phần mềm: Luân phiên, Peterson, Dekker; Phần cứng: Disabling Interrupts, TestAndSet, Swap), Semaphore (Khái niệm, Semaphore nguyên tử, Counting Semaphore, Binary Semaphore, Hàng đợi Semaphore), Monitor & Condition Variables, Các bài toán đồng bộ kinh điển:
  - Producer – Consumer (Buffer giới hạn)
  - Readers – Writers (Ưu tiên Reader / Ưu tiên Writer)
  - Dining Philosophers (Triết gia ăn tối)
  - Đồng bộ thứ tự thực thi tiến trình (Dependency Graph).
- **Trọng tâm bài thi/Lab**:
  - **Bài tập trọng tâm thi Cuối kỳ**:
    1. Chứng minh giải pháp CS thỏa mãn / không thỏa mãn 3 điều kiện (Mutual Exclusion, Progress, Bounded Waiting).
    2. Viết mã đồng bộ bằng Semaphore cho sơ đồ phụ thuộc tiến trình (Dependency DAG).
    3. Sửa lỗi Race Condition cho biến dùng chung (Biến $X$ không vượt quá 20).
    4. Cài đặt bài toán Producer-Consumer / Readers-Writers bằng Pseudocode Semaphore.

---

### CHƯƠNG 6 — DEADLOCK (BẾ TẮC)
- **Syllabus**: Định nghĩa Deadlock, 4 điều kiện cần gây ra Deadlock (Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait), Đồ thị cấp phát tài nguyên (Resource Allocation Graph - RAG), Các phương pháp xử lý Deadlock:
  - Phòng ngừa Deadlock (Deadlock Prevention - Triệt tiêu 1 trong 4 điều kiện)
  - Tránh Deadlock (Deadlock Avoidance - Trạng thái an toàn Safe State, Thuật toán Banker cho Single & Multiple Resource Instances)
  - Phát hiện Deadlock (Deadlock Detection)
  - Phục hồi sau Deadlock (Recovery: Process Termination, Resource Preemption).
- **Trọng tâm bài thi/Lab**:
  - **Bài tập trọng tâm thi Cuối kỳ**:
    1. Phân tích đồ thị RAG: Xác định chu trình (Cycle) và kết luận Deadlock.
    2. Thuật toán Banker:
       - Dựng ma trận $Need = Max - Allocation$.
       - Chạy thuật toán Safe Algorithm để tìm chuỗi an toàn (Safe Sequence).
       - Xử lý Yêu cầu tài nguyên $Request_i$: Kiểm tra $Request_i \le Need_i$ và $Request_i \le Available$. Giả lập cấp phát và kiểm tra lại Safe State.

---

### CHƯƠNG 7 — QUẢN LÝ BỘ NHỚ (MEMORY MANAGEMENT)
- **Syllabus**: Khái niệm Địa chỉ logic (Logical/Virtual Address) vs Địa chỉ vật lý (Physical Address), Ràng buộc địa chỉ (Address Binding: Compile time, Load time, Execution time), MMU (Memory Management Unit), Dynamic Loading & Dynamic Linking, Swapping, Cấp phát bộ nhớ liên tục (Contiguous Memory Allocation: Phân vùng cố định & Phân vùng động, Chiến lược First-fit, Best-fit, Worst-fit, Next-fit, Phân mảnh nội Internal Fragmentation & Phân mảnh ngoại External Fragmentation), Kỹ thuật Phân trang (Paging):
  - Bảng trang (Page Table), Trang (Page) vs Khung trang (Frame).
  - Chuyển đổi địa chỉ ($p, d \to f, d$).
  - Bộ đệm chuyển đổi địa chỉ TLB (Translation Lookaside Buffer), Tỷ lệ tìm thấy (Hit ratio $\alpha$), Thời gian truy xuất hiệu dụng (Effective Access Time - EAT).
  - Cấu trúc Bảng trang: Phân trang nhiều cấp (Multi-level Paging), Hashed Page Table, Inverted Page Table.
- **Trọng tâm bài thi/Lab**:
  - **Bài tập trọng tâm thi Cuối kỳ**:
    1. Bài tập Placement Algorithms (First-fit, Best-fit, Worst-fit, Next-fit) trên phân vùng cố định & phân vùng động.
    2. Ánh xạ địa chỉ Logic $\leftrightarrow$ Physical (Tính $p, d, f$ từ địa chỉ dạng số nguyên).
    3. Tính thời gian EAT có TLB: $EAT = \alpha (t_{TLB} + t_{RAM}) + (1 - \alpha) (t_{TLB} + 2 t_{RAM})$ hoặc công thức rút gọn trong đề thi UIT.
    4. Tính số bit địa chỉ logic/vật lý và kích thước Bảng trang nhiều cấp.

---

### CHƯƠNG 8 — BỘ NHỚ ẢO (VIRTUAL MEMORY)
- **Syllabus**: Khái niệm Bộ nhớ ảo, Nạp trang theo yêu cầu (Demand Paging), Xử lý Lỗi trang (Page Fault Walkthrough), Thay thế trang (Page Replacement):
  - Thuật toán FIFO (First-In, First-Out) & Nghịch lý Belady (Belady's Anomaly)
  - Thuật toán OPT (Optimal Page Replacement)
  - Thuật toán LRU (Least Recently Used)
  - Các thuật toán xấp xỉ LRU (Second Chance / Clock, Additional Reference Bits)
  - Cấp phát khung trang (Frame Allocation: Equal, Proportional), Trì trệ hệ thống (Thrashing), Mô hình Tập làm việc (Working-Set Model).
- **Trọng tâm bài thi/Lab**:
  - **Bài tập bắt buộc thi Cuối kỳ**:
    1. Bảng mô phỏng thay thế trang theo chuỗi truy xuất (Reference String) cho FIFO, OPT, LRU với $N$ khung trang.
    2. Đếm chính xác số Lỗi trang (Page Faults) và xác định trang bị thay thế (Victim page) tại mỗi bước.

---

### FINAL MASTER REVIEW (ÔN THI CUỐI KỲ IT007)
- Tổng hợp sơ đồ tư duy toàn bộ môn học (Ch1–8).
- Bộ câu hỏi bẫy trắc nghiệm Cuối kỳ UIT.
- 02 Đề thi mô phỏng Cuối kỳ chuẩn cấu trúc UIT (Có đáp án & Lời giải chi tiết 100%).

---

### PHỤ LỤC — LINUX SURVIVAL KIT CHO IT007
- Hướng dẫn cài đặt môi trường Linux / WSL2.
- Các lệnh Linux bắt buộc cho IT007 (`ps`, `top`, `pstree`, `kill`, `gcc`, `gdb`, `strace`, `man`, `pipe`, `redirection`).
- Hướng dẫn làm bài Lab 1 đến Lab 6 đạt điểm tối đa.

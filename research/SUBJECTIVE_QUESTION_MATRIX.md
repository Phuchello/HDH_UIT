# MA TRẬN NGÂN HÀNG CÂU HỎI TỰ LUẬN CHUẨN HÓA (SUBJECTIVE QUESTION MATRIX)

Tài liệu này hệ thống hóa toàn bộ các câu hỏi tự luận, giải thích lý thuyết, so sánh khái niệm, phân tích đặc tính và bài tập suy luận chuyên sâu của học phần Hệ điều hành (IT007) UIT.

---

## 1. Phân Loại Dạng Câu Hỏi Tự Luận (Subjective Taxonomy)

| Mã Phân Loại | Tên Dạng Câu Hỏi | Mục Tiêu & Yêu Cầu Học Thuật |
| :--- | :--- | :--- |
| `DEFINE` | Định nghĩa chuẩn xác | Nêu định nghĩa chính xác về mặt khoa học máy tính, không diễn giải mơ hồ. |
| `LIST_CHARACTERISTICS` | Liệt kê đặc điểm / đặc tính | Trình bày các tính chất, điều kiện, ưu điểm, nhược điểm và vai trò của cơ chế. |
| `EXPLAIN` | Giải thích cơ chế | Mô tả luồng hoạt động từng bước (step-by-step) của phần cứng / hệ điều hành. |
| `COMPARE` | So sánh & Đối chiếu | Lập bảng đối chiếu sự giống và khác nhau giữa 2 hoặc nhiều khái niệm liên quan. |
| `WHY` | Phân tích động lực / Tại sao | Giải thích nguyên nhân kỹ thuật dẫn đến sự ra đời của một giải thuật hoặc kiến trúc. |
| `TRUE_FALSE_EXPLAIN` | Đúng / Sai có giải thích | Xác định tính đúng/sai của mệnh đề và đưa ra phản ví dụ hoặc lập luận chứng minh. |
| `TRACE` | Lần vết thực thi | Lần vết chuỗi trạng thái tiến trình, không gian biến, hoặc luồng dữ liệu I/O. |
| `SHORT_PROOF_OR_REASONING`| Chứng minh / Lập luận ngắn | Chứng minh tính thỏa mãn của 3 điều kiện Critical Section, hoặc tính an toàn Banker. |
| `ALGORITHM_DESCRIPTION` | Mô tả giải thuật | Trình bày cơ chế lựa chọn, cấu trúc dữ liệu và các bước thực thi của giải thuật. |
| `SYNCHRONIZATION_DESIGN` | Thiết kế đồng bộ hóa | Khai báo Semaphore/Mutex và viết mã C / mã giả giải quyết bài toán tranh chấp. |
| `CALCULATION_WITH_EXPLANATION` | Tính toán có giải thích | Tính toán các chỉ số ($TAT, WT, RT, EAT$, Page Faults) kèm phân tích nguyên nhân. |
| `OS_SPECIFIC` | Chuyên sâu Linux / Windows | Trình bày cơ chế nội tại của nhân Linux (`task_struct`, CFS) hoặc Windows (HAL, 32 levels). |
| `LAB_VIVA` | Câu hỏi vấn đáp thực hành | Câu hỏi kiểm tra bản chất lập trình hệ thống trong các buổi thực hành Lab 1–6. |

---

## 2. Bảng Danh Mục Câu Hỏi Tự Luận Toàn Diện

| Mã ID | Chương | Phân Loại (Taxonomy) | Nội Dung Câu Hỏi Tự Luận | Nguồn Gốc (Source) | Bằng Chứng Đề Thi / Review | Điểm Số | Độ Khó |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **SQ01-01** | Ch 1 | `DEFINE` + `EXPLAIN` | Định nghĩa hệ điều hành dưới 2 góc nhìn: User view và System view? Phân tích vai trò Resource Allocator và Control Program. | `SRC-A01` / `SRC-B01` | `Review Ch1: Mục 1` | 1.0đ | Easy |
| **SQ01-02** | Ch 1 | `COMPARE` | Phân biệt Chương trình hệ thống (System Programs) và Chương trình ứng dụng (Application Programs). Nêu 3 ví dụ cho mỗi loại. | `SRC-A10` | `Week08: Slide 4` | 1.0đ | Easy |
| **SQ01-03** | Ch 1 | `LIST_CHARACTERISTICS` | Trình bày các đặc điểm cơ bản của cơ chế Ngắt (Interrupt)? Phân biệt Ngắt phần cứng (Hardware Interrupt) và Bẫy ngắt/Ngoại lệ (Trap/Exception). | `SRC-A02` / `SRC-A10` | `GK 2018-2019`, `GK 2022-2023` | 1.5đ | Medium |
| **SQ01-04** | Ch 1 | `EXPLAIN` | Trình bày chu trình xử lý ngắt của CPU từ lúc nhận tín hiệu ngắt đến khi khôi phục chương trình bị ngắt. Nêu vai trò của Bảng véc-tơ ngắt (IVT) và ISR. | `SRC-A02` | `Review Ch1: Mục 4` | 1.0đ | Medium |
| **SQ01-05** | Ch 1 | `LIST_CHARACTERISTICS` | Hệ thống lưu trữ được phân cấp dựa trên những yếu tố nào? Nêu thứ tự phân cấp từ nhanh nhất đến chậm nhất và nguyên lý Caching. | `SRC-A10` | `Week08: Slide 4`, `GK 2020-2021` | 1.0đ | Easy |
| **SQ01-06** | Ch 1 | `COMPARE` | Phân biệt các khái niệm bộ xử lý: CPU, Processor, Core, Multicore và Multiprocessor. | `SRC-A10` | `Week08: Slide 4` | 1.0đ | Medium |
| **SQ01-07** | Ch 1 | `COMPARE` | Phân biệt Hệ thống xử lý đa đối xứng (SMP) và Hệ thống xử lý đa bất đối xứng (AMP). Nêu ưu và nhược điểm của từng loại. | `SRC-A02` / `SRC-B01` | `Review Ch1: Mục 7` | 1.0đ | Medium |
| **SQ01-08** | Ch 1 | `LIST_CHARACTERISTICS` | Trình bày đặc điểm của Hệ thống gom cụm (Clustered Systems)? Phân biệt Asymmetric Clustering và Symmetric Clustering. | `SRC-A02` | `Review Ch1: Mục 7` | 1.0đ | Medium |
| **SQ01-09** | Ch 1 | `EXPLAIN` + `LIST_CHARACTERISTICS` | Trình bày bản chất của chế độ hoạt động kép (Dual-Mode Operation)? Phân biệt User Mode và Kernel Mode. Liệt kê 5 ví dụ về Lệnh đặc quyền (Privileged Instructions). | `SRC-A01` / `SRC-A10` | `GK 2018-2019`, `GK 2020-2021`, `GK 2022-2023` | 1.5đ | Medium |
| **SQ01-10** | Ch 1 | `COMPARE` | Lập bảng so sánh 4 môi trường tính toán: Đơn chương (Uniprogramming), Đa chương (Multiprogramming), Đa nhiệm / Chia sẻ thời gian (Time-sharing), và Thời gian thực (Real-time). | `SRC-A01` / `SRC-A02` | `Review Ch1: Mục 9` | 1.5đ | Hard |
| **SQ01-11** | Ch 1 | `COMPARE` | Phân biệt Hệ thống thời gian thực cứng (Hard Real-Time) và Hệ thống thời gian thực mềm (Soft Real-Time). | `SRC-A02` | `GK 2020-2021`, `GK 2023-2024` | 1.0đ | Easy |
| **SQ02-01** | Ch 2 | `LIST_CHARACTERISTICS` | Trình bày trách nhiệm chi tiết của 8 thành phần cốt lõi trong hệ điều hành hiện đại. | `SRC-A02` / `SRC-A10` | `Week08: Slide 6` | 1.5đ | Medium |
| **SQ02-02** | Ch 2 | `LIST_CHARACTERISTICS` | Trình bày các dịch vụ do hệ điều hành cung cấp, phân loại theo 2 nhóm: Dịch vụ hỗ trợ người dùng/chương trình và Dịch vụ đảm bảo hiệu quả hệ thống. | `SRC-A02` / `SRC-A10` | `Week08: Slide 6` | 1.0đ | Medium |
| **SQ02-03** | Ch 2 | `DEFINE` + `EXPLAIN` | Lời gọi hệ thống (System Call) là gì và dùng để làm gì? Trình bày 3 phương pháp truyền tham số từ chương trình người dùng vào Kernel. | `SRC-A02` / `SRC-A10` | `GK 2018-2019`, `GK 2022-2023` | 1.5đ | Medium |
| **SQ02-04** | Ch 2 | `LIST_CHARACTERISTICS` | Chương trình hệ thống (System Programs) gồm những nhóm nào? Kể tên 6 nhóm chính thức theo giáo trình và nêu lệnh minh họa. | `SRC-A02` / `SRC-A10` | `Week08: Slide 6`, `GK 2023-2024` | 1.0đ | Medium |
| **SQ02-05** | Ch 2 | `COMPARE` | Lập bảng so sánh 4 mô hình kiến trúc hệ điều hành: Đơn khối (Monolithic), Phân tầng (Layered), Vi nhân (Microkernel), và Mô-đun nạp động (Modules). Nêu ưu/nhược điểm và ví dụ kinh điển. | `SRC-A02` / `SRC-A10` | `GK 2020-2021`, `GK 2024-2025` | 1.5đ | Hard |
| **SQ03-01** | Ch 3 | `LIST_CHARACTERISTICS` | Một tiến trình trong bộ nhớ bao gồm những thành phần nào? Trình bày vai trò và hướng tăng trưởng của Text, Data, Heap, Stack. | `SRC-A03` / `SRC-A10` | `Week08: Slide 8`, `GK 2018-2019` | 1.0đ | Easy |
| **SQ03-02** | Ch 3 | `EXPLAIN` | Trình bày 5 trạng thái của tiến trình và vẽ sơ đồ chuyển trạng thái. Nêu nguyên nhân kích hoạt từng bước chuyển. | `SRC-A03` / `SRC-A10` | `GK 2018-2019`, `GK 2023-2024` | 1.0đ | Easy |
| **SQ03-03** | Ch 3 | `LIST_CHARACTERISTICS` | Khối điều khiển tiến trình (PCB) là gì? Liệt kê 7 trường thông tin quan trọng nhất trong PCB và giải thích ý nghĩa. | `SRC-A03` / `SRC-A10` | `Week08: Slide 8` | 1.0đ | Medium |
| **SQ03-04** | Ch 3 | `COMPARE` | Phân biệt 3 loại bộ định thời: Bộ định thời dài hạn (Long-term / Job Scheduler), ngắn hạn (Short-term / CPU Scheduler), và trung hạn (Medium-term Scheduler). | `SRC-A03` / `SRC-A04` | `Week08: Slide 8` | 1.0đ | Medium |
| **SQ03-05** | Ch 3 | `COMPARE` | Phân biệt Chuyển đổi chế độ (Mode Switch) và Chuyển ngữ cảnh tiến trình (Context Switch) theo nguyên nhân, thao tác phần cứng/phần mềm và chi phí. | `SRC-A02` / `SRC-A03` | `GK 2022-2023`, `GK 2024-2025` | 1.5đ | Hard |
| **SQ03-06** | Ch 3 | `EXPLAIN` | Trình bày quan hệ thực thi và chia sẻ tài nguyên giữa tiến trình cha và tiến trình con khi gọi `fork()`, `exec()`, `wait()`. Thế nào là tiến trình Zombie và Orphan? | `SRC-A03` / `SRC-B02` | `GK 2018-2019`, `GK 2020-2021` | 1.5đ | Medium |
| **SQ03-07** | Ch 3 | `COMPARE` | So sánh 2 mô hình giao tiếp liên tiến trình (IPC): Bộ nhớ chia sẻ (Shared Memory) và Truyền thông điệp (Message Passing). | `SRC-A03` / `SRC-A10` | `Week08: Slide 8`, `CK 2023-2024` | 1.0đ | Medium |
| **SQ03-08** | Ch 3 | `COMPARE` | So sánh Tiến trình (Process) và Tiểu trình (Thread) theo không gian địa chỉ, quyền sở hữu tài nguyên, đơn vị định thời và chi phí chuyển ngữ cảnh. Nêu 4 lợi ích của đa luồng. | `SRC-A03` / `SRC-A10` | `GK 2022-2023`, `GK 2024-2025` | 1.5đ | Hard |
| **SQ03-09** | Ch 3 | `COMPARE` | So sánh 3 mô hình đa luồng: Many-to-One, One-to-One, và Many-to-Many. Nêu ưu và nhược điểm của từng mô hình. | `SRC-A03` | `GK 2023-2024` | 1.0đ | Medium |
| **SQ04-01** | Ch 4 | `WHY` + `EXPLAIN` | Tại sao cần phải định thời CPU? Phân biệt CPU Scheduler và Dispatcher. Độ trễ phân phối (Dispatch Latency) gồm những thành phần nào? | `SRC-A04` / `SRC-A10` | `Week08: Slide 13` | 1.0đ | Medium |
| **SQ04-02** | Ch 4 | `COMPARE` | Phân biệt Định thời độc quyền (Non-preemptive) và Định thời trưng dụng / ưu tiên (Preemptive). Nêu 4 thời điểm kích hoạt bộ định thời CPU. | `SRC-A04` / `SRC-A10` | `Week08: Slide 13` | 1.0đ | Medium |
| **SQ04-03** | Ch 4 | `DEFINE` | Qbank wording giữ nguyên “5 tiêu chuẩn”; lời giải canonical theo slide trình bày **6** tiêu chí, thêm Fairness (định tính) bên cạnh CPU Utilization, Throughput, Turnaround, Waiting, Response. | `SRC-A04` / `SRC-A10` | Canonical Week04 map; Midterm slide 14 | 1.0đ | Easy |
| **SQ04-04** | Ch 4 | `LIST_CHARACTERISTICS` | Lập bảng đặc tính tổng hợp 8 giải thuật định thời CPU: FCFS, SJF, SRTF, Priority, Round Robin, HRRN, Multilevel Queue, Multilevel Feedback Queue (nêu rõ cơ chế, ưu/nhược điểm, nguy cơ Starvation và cách khắc phục bằng Aging). | `SRC-A04` / `SRC-A05` | `Week08: Slide 13`, `GK 2018-2025` | 2.0đ | Hard |
| **SQ04-05** | Ch 4 | `COMPARE` | Phân biệt 2 phạm vi tranh chấp định thời tiểu trình: Process-Contention Scope (PCS) và System-Contention Scope (SCS). | `SRC-A07` | `Week06 Slide 04-15` | 1.0đ | Medium |
| **SQ04-06** | Ch 4 | `EXPLAIN` | Trình bày cơ chế định thời trên hệ thống đa bộ xử lý (SMP): Tính thân thuộc (Processor Affinity: Soft vs Hard Affinity), Cấu trúc bộ nhớ NUMA, và Cơ chế Cân bằng tải (Load Balancing: Push migration vs Pull migration). | `SRC-A07` / `SRC-B01` | `Week08: Slide 13` | 1.5đ | Hard |
| **SQ04-07** | Ch 4 | `COMPARE` | So sánh 2 giải thuật định thời thời gian thực: Rate-Monotonic Scheduling (RMS) và Earliest-Deadline-First (EDF). | `SRC-A07` | `Week08: Slide 13` | 1.0đ | Hard |
| **SQ04-08** | Ch 4 | `OS_SPECIFIC` | Trình bày các đặc điểm cơ bản của bộ định thời Completely Fair Scheduler (CFS) trên Linux (Virtual Runtime `vruntime`, Cây đỏ đen Red-Black Tree, độ ưu tiên `nice`). | `SRC-A07` / `SRC-B03` | `Week08: Slide 13` | 1.0đ | Medium |
| **SQ04-09** | Ch 4 | `OS_SPECIFIC` | Trình bày cơ chế định thời trên Windows: 32 mức độ ưu tiên, phân chia Real-time vs Variable classes, Dynamic Priority Boost và xử lý Quantum. | `SRC-A07` / `SRC-B04` | `Week08: Slide 13` | 1.0đ | Medium |
| **SQ05-01** | Ch 5 | `DEFINE` | Tình trạng chạy đua (Race Condition) là gì? Vấn đề Vùng tranh chấp (Critical Section) là gì? Trình bày cấu trúc tổng quát của một giải pháp CS. | `SRC-A05` / `SRC-A08` | `CK 2017–2025` | 1.0đ | Easy |
| **SQ05-02** | Ch 5 | `DEFINE` + `SHORT_PROOF` | Trình bày định nghĩa chuẩn xác và ý nghĩa của 3 điều kiện đúng cho giải pháp Critical Section: Mutual Exclusion, Progress, Bounded Waiting. | `SRC-A05` / `SRC-A08` | `CK 2018–2025` | 1.5đ | Medium |
| **SQ05-03** | Ch 5 | `SHORT_PROOF_OR_REASONING` | Trình bày thuật toán Peterson cho 2 tiến trình. Chứng minh thuật toán Peterson thỏa mãn đầy đủ cả 3 điều kiện: Mutual Exclusion, Progress, Bounded Waiting. | `SRC-A08` / `SRC-B01` | `CK 2018-2019`, `CK 2022-2023` | 1.5đ | Hard |
| **SQ05-04** | Ch 5 | `LIST_CHARACTERISTICS` | Trình bày các giải pháp đồng bộ phần cứng: Vô hiệu hóa ngắt (Disable interrupts), Chỉ thị nguyên tử `TestAndSet` và `CompareAndSwap`, Hàng rào bộ nhớ (Memory Barrier). Phân tích ưu và nhược điểm của cơ chế Busy Waiting (Spinlock). | `SRC-A08` / `SRC-B01` | `CK 2022-2023`, `CK 2024-2025` | 1.5đ | Hard |
| **SQ05-05** | Ch 5 | `DEFINE` + `COMPARE` | Semaphore là gì? Trình bày định nghĩa nguyên tử của 2 thao tác `wait(S)` và `signal(S)`. Phân biệt Counting Semaphore và Binary Semaphore (Mutex Lock). | `SRC-A05` / `SRC-A10` | `CK 2017–2025` | 1.5đ | Medium |
| **SQ05-06** | Ch 5 | `EXPLAIN` | Trình bày cách hiện thực Semaphore không bận chờ (Non-busy waiting) bằng cấu trúc danh sách liên kết và 2 hàm `block()` / `wakeup()`. | `SRC-A10` / `SRC-B01` | `CK 2020-2021`, `CK 2024-2025` | 1.0đ | Medium |
| **SQ05-07** | Ch 5 | `SYNCHRONIZATION_DESIGN` | Trình bày đề bài và giải pháp đồng bộ chuẩn bằng Semaphore cho 3 bài toán kinh điển: 1. Bounded Buffer (Producer-Consumer), 2. Readers-Writers (ưu tiên Reader), 3. Dining Philosophers. | `SRC-A05` / `SRC-A11` | `CK 2017-2018`, `CK 2018-2019`, `CK 2020-2021` | 2.0đ | Hard |
| **SQ05-08** | Ch 5 | `LIST_CHARACTERISTICS` | Giám sát viên (Monitor) là gì? Biến điều kiện (Condition Variable) hoạt động như thế nào? Phân biệt ngữ nghĩa đánh thức Signal-and-Wait (Hoare) và Signal-and-Continue (Mesa). | `SRC-A05` / `SRC-A11` | `CK 2022-2023`, `CK 2024-2025` | 1.5đ | Hard |
| **SQ06-01** | Ch 6 | `DEFINE` + `LIST_CHARACTERISTICS` | Deadlock là gì? Trình bày chi tiết 4 điều kiện cần của Coffman để Deadlock có thể xảy ra. | `SRC-A06` / `SRC-A12` | `CK 2017–2025` | 1.0đ | Easy |
| **SQ06-02** | Ch 6 | `EXPLAIN` | Đồ thị cấp phát tài nguyên (Resource Allocation Graph - RAG) là gì? Phát biểu định lý về mối liên hệ giữa chu trình trong RAG và hiện tượng Deadlock cho trường hợp 1 thể hiện (single instance) và nhiều thể hiện (multi instance). | `SRC-A06` / `SRC-A12` | `CK 2017-2018`, `CK 2019-2020` | 1.0đ | Medium |
| **SQ06-03** | Ch 6 | `COMPARE` | Phân biệt 4 phương pháp giải quyết Deadlock: Phòng tránh (Prevention), Tránh (Avoidance), Phát hiện & Phục hồi (Detection & Recovery), và Bỏ qua (Ostrich Algorithm). | `SRC-A06` / `SRC-A12` | `CK 2018-2019`, `CK 2023-2024` | 1.5đ | Medium |
| **SQ06-04** | Ch 6 | `EXPLAIN` | Trình bày các chiến lược Phòng tránh Deadlock (Deadlock Prevention) bằng cách triệt tiêu từng điều kiện trong 4 điều kiện Coffman. Phân tích chi phí và tính khả thi của từng chiến lược. | `SRC-A06` / `SRC-A12` | `CK 2019-2020`, `CK 2022-2023` | 1.5đ | Hard |
| **SQ06-05** | Ch 6 | `DEFINE` + `COMPARE` | Thế nào là Trạng thái an toàn (Safe State)? Phân biệt Trạng thái an toàn, Trạng thái không an toàn (Unsafe State) và Deadlock. Tại sao Unsafe State không đồng nghĩa với Deadlock? | `SRC-A06` / `SRC-A12` | `CK 2017–2025` | 1.0đ | Medium |
| **SQ06-06** | Ch 6 | `ALGORITHM_DESCRIPTION` | Trình bày cấu trúc dữ liệu và các bước thực thi của Thuật toán Banker: Giải thuật Kiểm tra tính An toàn (Safety Algorithm) và Giải thuật Xử lý Yêu cầu tài nguyên (Resource-Request Algorithm). | `SRC-A06` / `SRC-A12` | `CK 2017–2025` | 1.5đ | Hard |
| **SQ06-07** | Ch 6 | `LIST_CHARACTERISTICS` | Trình bày các phương pháp Phục hồi Deadlock sau khi phát hiện: Hủy tiến trình (Process Termination) và Trưng dụng tài nguyên (Resource Preemption: chọn victim, rollback, starvation). | `SRC-A06` / `SRC-A12` | `CK 2020-2021`, `CK 2024-2025` | 1.0đ | Medium |
| **SQ07-01** | Ch 7 | `LIST_CHARACTERISTICS` | Quản lý bộ nhớ là gì? Nêu các yêu cầu đối với việc quản lý bộ nhớ. Phân biệt Địa chỉ logic (Địa chỉ ảo) và Địa chỉ vật lý. Vai trò của phần cứng MMU. | `SRC-A07` / `SRC-A13` | `CK 2017–2025` | 1.0đ | Easy |
| **SQ07-02** | Ch 7 | `COMPARE` | Trình bày 3 thời điểm Ràng buộc địa chỉ (Address Binding): Compile time, Load time, Execution time. Phân biệt Nạp động (Dynamic Loading) và Liên kết động (Dynamic Linking). | `SRC-A07` / `SRC-A13` | `CK 2023-2024` | 1.5đ | Hard |
| **SQ07-03** | Ch 7 | `COMPARE` | Phân biệt Phân mảnh nội (Internal Fragmentation) và Phân mảnh ngoại (External Fragmentation). Nêu nguyên nhân xuất hiện và giải pháp khắc phục cho từng loại. | `SRC-A07` / `SRC-A13` | `CK 2018-2019`, `CK 2023-2024` | 1.0đ | Medium |
| **SQ07-04** | Ch 7 | `COMPARE` | Lập bảng so sánh 4 chiến lược Cấp phát phân vùng bộ nhớ động (Placement Strategies): First-fit, Best-fit, Worst-fit, Next-fit (nêu rõ cơ chế tìm kiếm, ưu điểm, nhược điểm, loại phân mảnh sinh ra). | `SRC-A07` / `SRC-A13` | `CK 2019-2020`, `CK 2020-2021` | 1.0đ | Medium |
| **SQ07-05** | Ch 7 | `EXPLAIN` | Trình bày cơ chế Phân trang (Paging): Cấu trúc địa chỉ logic $(p, d)$, Bảng trang (Page Table), và cơ chế phần cứng ánh xạ sang địa chỉ vật lý $(f, d)$. Tại sao phân trang triệt tiêu phân mảnh ngoại? | `SRC-A07` / `SRC-A13` | `CK 2017–2025` | 1.5đ | Medium |
| **SQ07-06** | Ch 7 | `EXPLAIN` + `CALCULATION_WITH_EXPLANATION` | Bộ đệm chuyển đổi địa chỉ (TLB) là gì? Trình bày cơ chế TLB Hit và TLB Miss. Viết công thức tính Thời gian truy xuất hiệu dụng (EAT) khi có TLB và giải thích các thành phần. | `SRC-A07` / `SRC-A13` | `CK 2017–2025` | 1.5đ | Medium |
| **SQ07-07** | Ch 7 | `LIST_CHARACTERISTICS` | Trình bày cấu trúc các loại Bảng trang nâng cao: Bảng trang phân cấp 2 cấp (Hierarchical Paging), Bảng trang băm (Hashed Page Table), Bảng trang nghịch đảo (Inverted Page Table). Phân tích ưu/nhược điểm từng loại. | `SRC-A07` / `SRC-A13` | `CK 2019-2020`, `CK 2023-2024` | 1.5đ | Hard |
| **SQ07-08** | Ch 7 | `COMPARE` | So sánh Kỹ thuật Phân trang (Paging) và Kỹ thuật Phân đoạn (Segmentation) theo góc nhìn người lập trình, tính liên tục, kích thước khối và loại phân mảnh. | `SRC-A07` / `SRC-A13` | `CK 2019-2020`, `CK 2022-2023` | 1.0đ | Medium |
| **SQ07-09** | Ch 7 | `LIST_CHARACTERISTICS` | Kỹ thuật Hoán đổi (Swapping) là gì? Phân tích vai trò của Swapping đối với Degree of Multiprogramming và chi phí thời gian truyền đĩa (Disk Transfer Time). | `SRC-A07` / `SRC-A13` | `Review Ch7: Mục 9` | 1.0đ | Easy |
| **SQ08-01** | Ch 8 | `WHY` + `LIST_CHARACTERISTICS` | Tại sao cần phải có Bộ nhớ ảo (Virtual Memory)? Nêu 4 lợi ích lớn của bộ nhớ ảo đối với lập trình viên và hệ thống. Cơ chế Copy-on-Write khi gọi `fork()` hoạt động như thế nào? | `SRC-A08` / `SRC-A14` | `CK 2018–2025` | 1.0đ | Medium |
| **SQ08-02** | Ch 8 | `EXPLAIN` | Kỹ thuật Phân trang theo yêu cầu (Demand Paging) là gì? Trình bày chi tiết 6 bước chuẩn xử lý Lỗi trang (Page Fault) của phần cứng và hệ điều hành. | `SRC-A08` / `SRC-A14` | `CK 2017–2025` | 1.5đ | Medium |
| **SQ08-03** | Ch 8 | `COMPARE` | Lập bảng so sánh 3 giải thuật Thay thế trang (Page Replacement Algorithms): FIFO, OPT, LRU theo cơ chế chọn victim, chi phí phần cứng, số lỗi trang và Hiện tượng bất thường Belady (Belady Anomaly). | `SRC-A08` / `SRC-A14` | `CK 2017–2025` | 1.5đ | Hard |
| **SQ08-04** | Ch 8 | `EXPLAIN` | Trình bày giải thuật xấp xỉ LRU: Thuật toán Cơ hội thứ hai (Second-Chance / Clock Algorithm) sử dụng Reference bit và Dirty bit (Modify bit). | `SRC-A08` / `SRC-A14` | `CK 2022-2023`, `CK 2024-2025` | 1.0đ | Medium |
| **SQ08-05** | Ch 8 | `EXPLAIN` | Hiện tượng Nghẽn bộ nhớ (Thrashing) là gì? Nguyên nhân dẫn đến Thrashing? Trình bày 2 giải pháp kiểm soát Thrashing: Mô hình Tập làm việc (Working-Set Model với cửa sổ $\Delta$) và Tần suất lỗi trang (Page-Fault Frequency - PFF). | `SRC-A08` / `SRC-A14` | `CK 2018-2019`, `CK 2022-2023` | 1.5đ | Hard |
| **SQ09-01** | Ch 9 | `OS_SPECIFIC` + `COMPARE` | So sánh triết lý và nguyên tắc thiết kế giữa hệ điều hành Linux (Monolithic Modular, POSIX, Đa người dùng) và Windows (Layered/Microkernel-inspired, Object-oriented, Tương thích Win32/POSIX, Đa nền tảng). | `SRC-A09` / `SRC-A15` | `Review Ch9: Mục 1` | 1.5đ | Hard |
| **SQ09-02** | Ch 9 | `OS_SPECIFIC` + `COMPARE` | So sánh cơ chế Quản lý tiến trình và luồng giữa Linux (`struct task_struct`, `fork()`, `clone()`, Lightweight Process) và Windows (`EPROCESS`, `KPROCESS`, `ETHREAD`, `KTHREAD`, Fiber). | `SRC-A09` / `SRC-A15` / `SRC-B04` | `Review Ch9: Mục 3` | 1.5đ | Hard |
| **SQ09-03** | Ch 9 | `OS_SPECIFIC` + `COMPARE` | So sánh cơ chế Quản lý bộ nhớ ảo giữa Linux (Phân trang đa cấp, Buddy System Allocator, Slab Allocator, Swapping) và Windows (Không gian địa chỉ ảo 2GB/2GB hoặc 8TB, Working Set, Paging File, PFN Database). | `SRC-A09` / `SRC-A15` | `Review Ch9: Mục 5` | 1.5đ | Hard |
| **SQ09-04** | Ch 9 | `OS_SPECIFIC` + `COMPARE` | So sánh cơ chế Giao tiếp liên tiến trình (IPC) giữa Linux (Pipes, FIFOs, POSIX Shared Memory, POSIX Semaphores, Signals, Sockets) và Windows (ALPC - Advanced Local Procedure Calls, Named Pipes, Mailslots, COM). | `SRC-A09` / `SRC-A15` | `Review Ch9: Mục 4` | 1.5đ | Hard |
| **SQLAB-01**| Lab | `LAB_VIVA` | Giải thích tại sao trong hàm xử lý lệnh của shell `it007sh`, tiến trình cha bắt buộc phải gọi `waitpid()` khi thực thi lệnh foreground? Nếu không gọi `waitpid()` thì hiện tượng gì sẽ xảy ra? | `SRC-A11` | `Lab 6 v2023 (it007sh)` | 1.0đ | Medium |
| **SQLAB-02**| Lab | `LAB_VIVA` | Trình bày cơ chế hoạt động của `dup2(fd, STDOUT_FILENO)` khi thực hiện chuyển hướng đầu ra (`> file.txt`). Tại sao sau khi `dup2()`, tiến trình cần phải gọi `close(fd)`? | `SRC-A11` / `SRC-B02` | `Lab 6 v2023 (it007sh)` | 1.0đ | Hard |
| **SQLAB-03**| Lab | `LAB_VIVA` | Phân tích cơ chế hoạt động của đường ống Pipe `pipe(pipefd)` kết nối giữa 2 tiến trình $cmd_1 \mid cmd_2$. Tại sao cả tiến trình cha và 2 tiến trình con đều phải đóng các đầu pipe không sử dụng (`close(pipefd[0])`, `close(pipefd[1])`) để lệnh không bị treo vĩnh viễn? | `SRC-A11` / `SRC-B02` | `Lab 6 v2023 (it007sh)` | 1.5đ | Hard |

---

## 3. Mẫu Khung Lời Giải Chuẩn Hóa Cho Các Câu Hỏi Tự Luận Trọng Tâm

### MẪU 1: CÂU HỎI SO SÁNH TIẾN TRÌNH VÀ TIỂU TRÌNH (`SQ03-08`)

```markdown
### CÂU HỎI:
So sánh Tiến trình (Process) và Tiểu trình (Thread) theo 4 tiêu chí: Không gian địa chỉ, Tài nguyên sở hữu, Đơn vị định thời, và Chi phí chuyển ngữ cảnh. Nêu 4 lợi ích của đa luồng.

### CÁC Ý BẮT BUỘC TRONG ĐÁP ÁN (KEY POINTS):
- [ ] Không gian địa chỉ: Process độc lập; Threads trong cùng process chia sẻ Code, Data, Heap.
- [ ] Tài nguyên: Process sở hữu tài nguyên riêng (files, sockets); Thread chỉ có Stack, PC, Registers, Thread ID.
- [ ] Định thời: Thread là đơn vị cơ bản để CPU định thời thực thi (Basic unit of CPU utilization).
- [ ] Chi phí chuyển ngữ cảnh: Context switch Thread nhanh và nhẹ hơn rất nhiều so với Process.
- [ ] 4 lợi ích của đa luồng: Responsiveness (Khả năng đáp ứng), Resource sharing (Chia sẻ tài nguyên), Economy (Tính kinh tế), Scalability (Khả năng mở rộng trên đa lõi).

### BẢNG ĐỐI CHIẾU SO SÁNH:
| Tiêu chí | Tiến trình (Process) | Tiểu trình (Thread) |
| :--- | :--- | :--- |
| **Định nghĩa** | Chương trình đang trong quá trình thực thi, là đơn vị sở hữu tài nguyên độc lập. | Một luồng thực thi bên trong tiến trình, là đơn vị sử dụng CPU cơ bản. |
| **Không gian địa chỉ** | Mỗi tiến trình có không gian địa chỉ ảo độc lập (Text, Data, Heap, Stack riêng). | Các luồng trong cùng tiến trình chia sẻ chung Text, Data, Heap; mỗi luồng có Stack riêng. |
| **Tài nguyên sở hữu** | Sở hữu toàn bộ tài nguyên: Bảng file descriptors, vùng nhớ, thông tin bảo vệ. | Không sở hữu tài nguyên riêng; chia sẻ tài nguyên chung của tiến trình cha. |
| **Trạng thái riêng** | PCB riêng biệt hoàn toàn do Kernel quản lý. | Có Thread ID, Program Counter (PC), Bộ thanh ghi (Registers) và Ngăn xếp (Stack) riêng. |
| **Chi phí tạo & Chuyển ngữ cảnh** | Rất nặng: Cần cấp phát bộ nhớ mới, sao chép bảng trang, xả TLB và Cache khi context switch. | Rất nhẹ: Không cần đổi bảng trang, không cần xả cache dữ liệu, tạo nhanh hơn gấp 10-30 lần. |
| **Giao tiếp liên luồng/tiến trình** | Phải thông qua các cơ chế IPC (Shared Memory, Pipes, Sockets) do kernel hỗ trợ. | Truy cập trực tiếp các biến toàn cục (Data) và vùng nhớ động (Heap) chia sẻ. |
| **Mức độ cô lập lỗi** | Cao: Một tiến trình sụp đổ (crash) không làm ảnh hưởng đến tiến trình khác. | Thấp: Một luồng bị lỗi truy xuất bộ nhớ (Segfault) có thể làm sụp đổ toàn bộ tiến trình. |

### LỜI GIẢI ĐẠT ĐIỂM TỐI ĐA:
1. **Khái niệm:** Tiến trình (Process) là một chương trình đang thực thi với không gian địa chỉ độc lập. Tiểu trình (Thread) là một dòng điều khiển (flow of control) độc lập bên trong tiến trình và là đơn vị cơ bản được bộ định thời CPU cấp phát thời gian thực thi.
2. **So sánh theo 4 tiêu chí:**
   - *Không gian địa chỉ:* Tiến trình sở hữu không gian nhớ riêng biệt. Các tiểu trình trong cùng tiến trình dùng chung mã lệnh (Text), biến toàn cục (Data) và bộ nhớ động (Heap), nhưng mỗi tiểu trình có ngăn xếp (Stack) riêng để quản lý các lời gọi hàm cục bộ.
   - *Tài nguyên sở hữu:* Tiến trình sở hữu tài nguyên hệ thống (tệp mở, kết nối I/O). Tiểu trình chia sẻ tài nguyên của tiến trình cha và chỉ lưu giữ trạng thái thanh ghi, con trỏ lệnh PC, ngăn xếp và Thread ID.
   - *Đơn vị định thời:* Hệ điều hành định thời CPU trên từng tiểu trình (Thread là đơn vị lập lịch CPU).
   - *Chi phí chuyển ngữ cảnh:* Chuyển ngữ cảnh tiểu trình diễn ra nhanh chóng vì không phải chuyển đổi bảng trang MMU hay xả bộ đệm TLB/Cache.
3. **4 Lợi ích cốt lõi của đa luồng:**
   - *Khả năng đáp ứng (Responsiveness):* Giao diện người dùng vẫn tương tác mượt mà trong khi luồng ngầm thực hiện các tác vụ tính toán nặng hoặc I/O.
   - *Chia sẻ tài nguyên (Resource Sharing):* Các luồng mặc định chia sẻ bộ nhớ và tài nguyên của tiến trình mà không cần thiết lập cơ chế IPC phức tạp.
   - *Tính kinh tế (Economy):* Tạo và hủy luồng tốn ít tài nguyên và thời gian hơn nhiều so với tạo/hủy tiến trình.
   - *Khả năng mở rộng (Scalability):* Tận dụng tối đa sức mạnh tính toán song song thực sự trên các kiến trúc CPU đa lõi (Multicore).

### BAREM ĐIỂM (RUBRIC - 1.5 ĐIỂM):
- **0.25đ:** Nêu đúng định nghĩa và bản chất Process vs Thread.
- **0.75đ:** So sánh chính xác 4 tiêu chí (Không gian nhớ 0.25đ; Tài nguyên 0.2đ; Định thời 0.15đ; Chi phí context switch 0.15đ).
- **0.50đ:** Kể tên và giải thích đúng 4 lợi ích của đa luồng (mỗi ý 0.125đ).

### CÁC SAI LẦM PHỔ BIẾN SINH VIÊN HAY MẤT ĐIỂM:
- ❌ Nhầm lẫn rằng Thread không có Stack riêng (Thread bắt buộc phải có Stack riêng để lưu biến cục bộ và địa chỉ trả về của hàm).
- ❌ Nhầm lẫn rằng Context Switch giữa 2 Thread thuộc cùng 1 Process cũng phải đổi bảng trang nhớ (Chỉ đổi thanh ghi CPU và con trỏ Stack, không đổi bảng trang).
- ❌ Không giải thích được tại sao một luồng bị lỗi có thể kéo theo toàn bộ tiến trình bị Terminated.
```

---

### MẪU 2: CÂU HỎI BẢN CHẤT DUAL-MODE & LỆNH ĐẶC QUYỀN (`SQ01-09`)

```markdown
### CÂU HỎI:
Trình bày bản chất của chế độ hoạt động kép (Dual-Mode Operation) trong hệ điều hành? Phân biệt User Mode và Kernel Mode. Nêu ví dụ về 5 lệnh đặc quyền.

### CÁC Ý BẮT BUỘC TRONG ĐÁP ÁN (KEY POINTS):
- [ ] Mục đích Dual-mode: Bảo vệ phần cứng, bộ nhớ và các tiến trình khác khỏi lỗi hoặc sự phá hoại của ứng dụng.
- [ ] Phần cứng hỗ trợ: Mode bit (0: Kernel Mode / Privileged / Supervisor; 1: User Mode).
- [ ] Cơ chế chuyển đổi: Lệnh System Call / Interrupt chuyển Mode bit từ 1 -> 0; Trả về từ System Call chuyển từ 0 -> 1.
- [ ] Lệnh đặc quyền (Privileged Instructions): Lệnh chỉ được phép thực thi ở Kernel mode; nếu chạy ở User mode sẽ gây ra Bẫy ngắt (Trap / Exception / Illegal Instruction).
- [ ] 5 ví dụ lệnh đặc quyền: 1. Tắt/bật ngắt (`cli`/`sti`), 2. Đổi Mode bit, 3. Thao tác cổng I/O (`in`/`out`), 4. Nạp thanh ghi Base/Limit hoặc CR3 bảng trang, 5. Lệnh dừng CPU (`hlt`).

### BAREM ĐIỂM (RUBRIC - 1.5 ĐIỂM):
- **0.5đ:** Trình bày bản chất bảo vệ và cơ chế phần cứng `Mode bit` (0: Kernel mode, 1: User mode).
- **0.5đ:** Phân tích luồng chuyển đổi qua System Call và xử lý vi phạm lệnh đặc quyền ở User mode.
- **0.5đ:** Kể tên chính xác 5 lệnh đặc quyền (mỗi lệnh 0.1đ).
```

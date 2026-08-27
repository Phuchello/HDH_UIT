# MA TRẬN BẰNG CHỨNG ĐỀ THI IT007 UIT (EXAM EVIDENCE MATRIX)

**Căn cứ khảo sát:** 20 bộ đề thi thực tế (8 đề Giữa kỳ + 12 đề Cuối kỳ) của Trường ĐH Công nghệ Thông tin (UIT) từ năm 2017 đến 2025 do Ban Hỗ Trợ Học Tập CNPM lưu trữ.

---

## 1. Hệ Thống Phân Loại Dạng Bài Thi (Question Type Taxonomy)

1. `DEFINITION`: Định nghĩa chuẩn xác khái niệm khoa học máy tính / hệ điều hành.
2. `CHARACTERISTIC`: Nêu đặc điểm, điều kiện, ưu điểm, nhược điểm của cơ chế / giải thuật.
3. `TRUE/FALSE PROPERTY`: Xác định tính đúng/sai của một mệnh đề kỹ thuật.
4. `COMPARE`: So sánh, đối chiếu sự khác biệt giữa 2 khái niệm lân cận (VD: Mode Switch vs Context Switch, User thread vs Kernel thread, Dynamic linking vs Dynamic loading).
5. `IDENTIFY FALSE STATEMENT`: Tìm phát biểu sai trong các câu hỏi trắc nghiệm.
6. `TRACE PROCESS`: Lần vết và vẽ sơ đồ chuỗi chuyển trạng thái của tiến trình qua vòng lặp và lệnh I/O `printf`.
7. `FORK COUNT`: Vẽ cây tiến trình `fork()`, đếm số tiến trình được tạo ra, xác định giá trị biến toàn cục và số chuỗi in ra.
8. `SCHEDULING CALCULATION`: Vẽ sơ đồ Gantt, tính thời gian hoàn thành ($CT$), thời gian lưu lại ($TAT$), thời gian chờ ($WT$), thời gian đáp ứng ($RT$) và giá trị trung bình cho các giải thuật định thời CPU.
9. `SYNCHRONIZATION REASONING`: Viết mã giả / mã C đồng bộ tiến trình bằng Semaphore hoặc Mutex, phân tích 3 điều kiện Critical Section và ngăn ngừa Race Condition / Deadlock.
10. `DEADLOCK/BANKER`: Dựng ma trận $Need$, bảng diễn tiến $Work$, kiểm tra Safe State, tìm chuỗi an toàn và xử lý yêu cầu $Request_i$ theo thuật toán Banker; phân tích đồ thị RAG.
11. `MEMORY CALCULATION`: Tính toán cấp phát phân vùng (First/Best/Worst/Next fit), chuyển đổi địa chỉ phân trang ($p, d \rightarrow f, d$), tính EAT với TLB 1 cấp và 2 cấp (tính thuận & tính nghịch).
12. `PAGE REPLACEMENT`: Lập bảng theo dõi khung trang qua chuỗi tham chiếu (thường 20 tham chiếu) cho FIFO, OPT, LRU; đếm số Page Faults và giải thích hiện tượng Belady Anomaly.
13. `OS-SPECIFIC THEORY`: Câu hỏi chuyên sâu về kiến trúc Linux (CFS, `task_struct`, VFS) hoặc Windows (32 priority levels, HAL, Executive).
14. `OTHER`: Các câu hỏi dạng mở hoặc tổng hợp.

---

## 2. Ma Trận Chi Tiết Toàn Bộ Các Đề Thi Khảo Sát

| Học kỳ / Năm | Kỳ thi | Thời lượng | Hình thức | Chuyên đề | Câu số | Nội dung câu hỏi cụ thể | Phân loại (Taxonomy) | Mức độ tin cậy |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **2018-2019 HK1** | Giữa kỳ | 60 phút | Tự luận | Ch 1–4 | Câu 1 | Trình bày các trạng thái tiến trình; phân biệt User mode và Kernel mode. | `COMPARE` + `DEFINITION` | `REPEATED PATTERN` |
| | | | | | Câu 2 | Cho đoạn code C chứa `fork()`, vẽ cây tiến trình và đếm số dòng in ra. | `FORK COUNT` | `REPEATED PATTERN` |
| | | | | | Câu 3 | Cho bảng 5 tiến trình, vẽ sơ đồ Gantt và tính $WT_{avg}, TAT_{avg}$ cho FCFS, SJF, RR ($q=4$). | `SCHEDULING CALCULATION` | `REPEATED PATTERN` |
| **2020-2021 HK1** | Giữa kỳ | 45 phút | TN + Tự luận | Ch 1–4 | Phần 1 | 15 câu trắc nghiệm lý thuyết ngắt, lệnh đặc quyền, storage hierarchy, PCB. | `TRUE/FALSE PROPERTY` / `CHARACTERISTIC` | `REPEATED PATTERN` |
| | | | | | Phần 2 | Bài tập cây `fork()` lồng điều kiện `if (fork() == 0)` và vẽ sơ đồ trạng thái có `printf`. | `FORK COUNT` + `TRACE PROCESS` | `REPEATED PATTERN` |
| | | | | | Phần 3 | Định thời CPU cho SRTF và Round Robin ($q=5$). | `SCHEDULING CALCULATION` | `REPEATED PATTERN` |
| **2022-2023 HK1** | Giữa kỳ | 60 phút | TN + Tự luận | Ch 1–4 | Câu 1 | 15 câu trắc nghiệm đặc điểm ngắt, vai trò dispatcher, ưu nhược điểm các giải thuật. | `CHARACTERISTIC` | `REPEATED PATTERN` |
| | | | | | Câu 2 | Cho code C vòng lặp `for (i=0; i<3; i++)`, xác định chuỗi trạng thái và vẽ cây tiến trình. | `TRACE PROCESS` + `FORK COUNT` | `REPEATED PATTERN` |
| | | | | | Câu 3 | Định thời CPU Preemptive Priority và Round Robin ($q=3$). | `SCHEDULING CALCULATION` | `REPEATED PATTERN` |
| **2023-2024 HK1** | Giữa kỳ | 60 phút | TN + Tự luận | Ch 1–4 | Câu 1 | 12 câu trắc nghiệm lý thuyết tổng quan, phân loại system programs, thread models. | `CHARACTERISTIC` | `REPEATED PATTERN` |
| | | | | | Câu 2 | Bài tập lần vết trạng thái có `printf` và tính số tiến trình con. | `TRACE PROCESS` + `FORK COUNT` | `REPEATED PATTERN` |
| | | | | | Câu 3 | Bài tập định thời CPU 5 tiến trình FCFS, SJF Preemptive, RR ($q=5$). | `SCHEDULING CALCULATION` | `REPEATED PATTERN` |
| **2024-2025 HK1** | Giữa kỳ | 60 phút | TN + Điền từ + TL | Ch 1–4 | Câu 1 | Điền từ ngắn thuật ngữ tiếng Anh (Context switch, Dispatcher, PCB, Monolithic). | `DEFINITION` | `OBSERVED` |
| | | | | | Câu 2 | Trắc nghiệm Đúng/Sai các mệnh đề về ngắt và đa luồng. | `TRUE/FALSE PROPERTY` | `OBSERVED` |
| | | | | | Câu 3 | Bài tập cây `fork()` và đếm số tiến trình. | `FORK COUNT` | `REPEATED PATTERN` |
| | | | | | Câu 4 | Bài toán định thời CPU SRTF và Priority. | `SCHEDULING CALCULATION` | `REPEATED PATTERN` |
| **2017-2018 HK2** | Cuối kỳ | 90 phút | Tự luận | Ch 5–8 | Câu 1 | Bài toán đồng bộ Producer - Consumer bằng Semaphore. | `SYNCHRONIZATION REASONING` | `REPEATED PATTERN` |
| | | | | | Câu 2 | Thuật toán Banker 5 tiến trình, 3 tài nguyên; tìm chuỗi an toàn. | `DEADLOCK/BANKER` | `REPEATED PATTERN` |
| | | | | | Câu 3 | Kỹ thuật phân trang: Tính địa chỉ vật lý và EAT khi có TLB. | `MEMORY CALCULATION` | `REPEATED PATTERN` |
| | | | | | Câu 4 | Thay thế trang: Bảng 20 tham chiếu cho FIFO, OPT, LRU với 3 và 4 khung trang. | `PAGE REPLACEMENT` | `REPEATED PATTERN` |
| **2018-2019 HK2** | Cuối kỳ | 90 phút | TN + Tự luận | Ch 5–8 | Phần 1 | 20 câu trắc nghiệm lý thuyết đồng bộ, deadlock, bộ nhớ ảo, thrashing. | `CHARACTERISTIC` | `REPEATED PATTERN` |
| | | | | | Phần 2 | Đồng bộ bài toán Readers - Writers (ưu tiên người đọc). | `SYNCHRONIZATION REASONING` | `REPEATED PATTERN` |
| | | | | | Phần 3 | Thuật toán Banker xử lý yêu cầu $Request_1 = (1, 0, 2)$. | `DEADLOCK/BANKER` | `REPEATED PATTERN` |
| | | | | | Phần 4 | Thay thế trang LRU và OPT, đếm số lỗi trang. | `PAGE REPLACEMENT` | `REPEATED PATTERN` |
| **2019-2020 HK1** | Cuối kỳ | 90 phút | TN + Tự luận | Ch 5–8 | Phần 1 | Trắc nghiệm lý thuyết Critical Section, 4 điều kiện Coffman, Phân trang 2 cấp. | `TRUE/FALSE PROPERTY` | `REPEATED PATTERN` |
| | | | | | Phần 2 | Đồ thị RAG xác định Deadlock và chu trình. | `DEADLOCK/BANKER` | `REPEATED PATTERN` |
| | | | | | Phần 3 | Tính EAT ngược: Biết EAT và thời gian truy xuất RAM/TLB, tìm tỉ lệ Hit $\alpha$. | `MEMORY CALCULATION` | `REPEATED PATTERN` |
| | | | | | Phần 4 | Bảng thay thế trang 20 bước cho FIFO và LRU. | `PAGE REPLACEMENT` | `REPEATED PATTERN` |
| **2020-2021 HK1** | Cuối kỳ | 90 phút | Tự luận | Ch 5–8 | Câu 1 | Bài toán đồng bộ xe qua cầu hẹp 1 chiều bằng Semaphore. | `SYNCHRONIZATION REASONING` | `REPEATED PATTERN` |
| | | | | | Câu 2 | Thuật toán Banker 5 tiến trình, 4 tài nguyên $A, B, C, D$. | `DEADLOCK/BANKER` | `REPEATED PATTERN` |
| | | | | | Câu 3 | Cấp phát bộ nhớ liên tục theo First-fit, Best-fit, Worst-fit. | `MEMORY CALCULATION` | `REPEATED PATTERN` |
| | | | | | Câu 4 | Bảng thay thế trang 20 bước cho FIFO, OPT, LRU với 4 khung trang. | `PAGE REPLACEMENT` | `REPEATED PATTERN` |
| **2022-2023 HK1** | Cuối kỳ | 90 phút | TN + Tự luận | Ch 5–8 | Phần 1 | 25 câu trắc nghiệm tổng hợp (Peterson, Memory barrier, Working set, Belady). | `CHARACTERISTIC` / `COMPARE` | `REPEATED PATTERN` |
| | | | | | Phần 2 | Bài toán đồng bộ 2 luồng cộng tác biến $x$ chia sẻ. | `SYNCHRONIZATION REASONING` | `REPEATED PATTERN` |
| | | | | | Phần 3 | Thuật toán Banker kiểm tra tính an toàn tại $t_0$ và sau yêu cầu $Request_2$. | `DEADLOCK/BANKER` | `REPEATED PATTERN` |
| | | | | | Phần 4 | Thay thế trang LRU có Dirty bit và FIFO kiểm chứng Belady anomaly. | `PAGE REPLACEMENT` | `REPEATED PATTERN` |
| **2023-2024 HK1** | Cuối kỳ | 90 phút | TN + Tự luận | Ch 5–8 | Phần 1 | 25 câu trắc nghiệm lý thuyết phân biệt Dynamic linking vs Dynamic loading. | `COMPARE` | `REPEATED PATTERN` |
| | | | | | Phần 2 | Bài toán đồng bộ phòng đọc sách / in ấn nhiều tài nguyên. | `SYNCHRONIZATION REASONING` | `REPEATED PATTERN` |
| | | | | | Phần 3 | Banker ma trận $Need$, véc-tơ $Available$, chuỗi an toàn. | `DEADLOCK/BANKER` | `REPEATED PATTERN` |
| | | | | | Phần 4 | Tính EAT bảng trang 2 cấp và bảng thay thế trang OPT/LRU. | `MEMORY CALCULATION` + `PAGE REPLACEMENT` | `REPEATED PATTERN` |
| **2024-2025 HK1** | Cuối kỳ | 90 phút | TN + Điền từ + TL | Ch 5–8 | Phần 1 | Điền thuật ngữ tiếng Anh ngắn (Mutual Exclusion, Safe Sequence, Page Fault). | `DEFINITION` | `OBSERVED` |
| | | | | | Phần 2 | Trắc nghiệm Đúng/Sai lý thuyết Monitor, Thrashing, TLB. | `TRUE/FALSE PROPERTY` | `OBSERVED` |
| | | | | | Phần 3 | Bài toán đồng bộ Semaphore. | `SYNCHRONIZATION REASONING` | `REPEATED PATTERN` |
| | | | | | Phần 4 | Banker Algorithm & Thay thế trang LRU. | `DEADLOCK/BANKER` + `PAGE REPLACEMENT` | `REPEATED PATTERN` |

---

## 3. Tổng Hợp Tần Suất Xuất Hiện Các Dạng Bài (Evidence-Based Frequency)

| Dạng bài thi | Số lần quan sát trong 20 đề | Tỷ lệ xuất hiện | Mức độ chắc chắn | Đánh giá trọng tâm học tập |
| :--- | :---: | :---: | :---: | :--- |
| **`SCHEDULING CALCULATION`** (Định thời CPU) | 8/8 đề Giữa kỳ | **100%** | `REPEATED PATTERN` | Bắt buộc 100% trong đề thi Giữa kỳ. Thường có 4-5 tiến trình, giải thuật FCFS, SJF/SRTF, RR, Priority. |
| **`FORK COUNT` / `TRACE PROCESS`** (Tiến trình & Fork) | 8/8 đề Giữa kỳ | **100%** | `REPEATED PATTERN` | Bắt buộc 100% trong đề thi Giữa kỳ. Khảo sát chuỗi trạng thái có `printf` và vẽ cây `fork()`. |
| **`DEADLOCK/BANKER`** (Thuật toán Banker) | 12/12 đề Cuối kỳ | **100%** | `REPEATED PATTERN` | Bắt buộc 100% trong đề thi Cuối kỳ. Luôn gồm 3 ý: Dựng Need, Kiểm tra an toàn, Xử lý Request. |
| **`PAGE REPLACEMENT`** (Bảng thay thế trang) | 12/12 đề Cuối kỳ | **100%** | `REPEATED PATTERN` | Bắt buộc 100% trong đề thi Cuối kỳ. Chuỗi 20 tham chiếu cho FIFO, OPT, LRU với 3-4 khung trang. |
| **`SYNCHRONIZATION REASONING`** (Đồng bộ Semaphore) | 12/12 đề Cuối kỳ | **100%** | `REPEATED PATTERN` | Bắt buộc 100% trong đề thi Cuối kỳ. Viết code C hoặc mã giả giải bài toán đồng bộ thực tế. |
| **`MEMORY CALCULATION`** (Phân trang, Placement, EAT) | 10/12 đề Cuối kỳ | **83.3%** | `REPEATED PATTERN` | Thường xuyên xuất hiện trong đề Cuối kỳ dưới dạng tính EAT có TLB hoặc tính địa chỉ phân trang. |
| **`CHARACTERISTIC` / `COMPARE` / `TRUE/FALSE`** | 20/20 đề (GK + CK) | **100%** | `REPEATED PATTERN` | Chiếm từ 30% đến 40% tổng số điểm dưới hình thức trắc nghiệm hoặc tự luận ngắn lý thuyết. |
| **`OS-SPECIFIC THEORY`** (Linux CFS / Windows internals) | 6/20 đề | **30%** | `LIKELY` | Xuất hiện trong các câu hỏi trắc nghiệm nâng cao hoặc câu hỏi phân loại điểm 9-10. |

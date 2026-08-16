# EXAM PATTERN ANALYSIS — IT007 UIT (2017 - 2025)

Phân tích thống kê từ toàn bộ đề thi Giữa kỳ và Cuối kỳ môn Hệ điều hành IT007 tại UIT.

---

## 1. THỐNG KÊ DẠNG BÀI THI GIỮA KỲ (MIDTERM EXAM)

Giữa kỳ tập trung vào **Chương 1 đến Chương 4**.

| Dạng bài | Tần suất xuất hiện | Mô tả chi tiết | Các bẫy đề thi UIT hay gặp |
| :--- | :--- | :--- | :--- |
| **Trạng thái tiến trình (Process States)** | 100% đề Giữa kỳ | Cho đoạn code C chứa vòng lặp `while/for`, `printf`, `exit`. Yêu cầu liệt kê chuỗi trạng thái (`New -> Ready -> Running -> Waiting -> Ready -> Terminated`). | **Bẫy**: Nhầm lẫn `printf` gây ra IO wait (chuyển sang `Waiting` rồi mới về `Ready`). Quên trạng thái `New` ở đầu hoặc `Terminated` ở cuối. |
| **Cây tiến trình & Đếm Process (`fork`)** | 100% đề Giữa kỳ | Cho chương trình C có `fork()` trong vòng lặp hoặc các câu lệnh `fork()` liên tiếp, kết hợp `if (fork() == 0)`. Tính số process sinh ra, vẽ cây tiến trình, dự đoán chuỗi `printf`. | **Bẫy 1**: `fork()` trong `for(i=0; i<N; i++)` sinh ra $2^N$ process. **Bẫy 2**: Bộ đệm `printf` không dùng `\n` khiến chuỗi in bị nhân đôi khi `fork()`. **Bẫy 3**: `execvp()` thay thế không gian địa chỉ tiến trình con, các lệnh phía sau `execvp` KHÔNG bao giờ chạy nếu `execvp` thành công! |
| **Biến dùng chung & Copy-on-Write** | 70% đề Giữa kỳ | Cho đoạn code `fork()`, tiến trình cha giảm `a`, tiến trình con tăng `a`, in ra `a` và `&a`. So sánh giá trị `u, v` (cha) và `x, y` (con). | **Bẫy**: Địa chỉ ảo `&a` ở 2 tiến trình là GIỐNG NHƯNG (`v == y`), nhưng địa chỉ vật lý và giá trị `a` là KHÁC NHAU (`u != x`). |
| **CPU Scheduling (FCFS, SJF, SRTF, RR, Priority)** | 100% đề Giữa kỳ | Cho bảng các tiến trình gồm Arrival Time ($AT$), CPU Burst Time ($BT$), Priority. Vẽ sơ đồ Gantt và tính $WT_{avg}$, $TAT_{avg}$, $RT_{avg}$. | **Bẫy 1**: Quên xét mốc $AT$ (tiến trình đến muộn không được lấy ngay). **Bẫy 2**: SRTF/Preemptive Priority bị ngắt ngay khi có tiến trình mới có $BT$ còn lại ngắn hơn hoặc độ ưu tiên cao hơn xuất hiện. **Bẫy 3**: Nhầm quy ước độ ưu tiên (đề UIT thường quy ước số nhỏ hơn = ưu tiên cao hơn, ví dụ Priority 1 > Priority 2). |

---

## 2. THỐNG KÊ DẠNG BÀI THI CUỐI KỲ (FINAL EXAM)

Cuối kỳ tập trung mạnh vào **Chương 5 đến Chương 8** (cùng một số câu tổng hợp Ch1-4).

| Dạng bài | Tần suất xuất hiện | Mô tả chi tiết | Các bẫy đề thi UIT hay gặp |
| :--- | :--- | :--- | :--- |
| **Đồng bộ tiến trình (Semaphore & CS)** | 100% đề Cuối kỳ | 1. Chứng minh giải pháp CS (Luân phiên, Peterson) thỏa 3 điều kiện. 2. Cho đồ thị phụ thuộc DAG (T1->T2, T1->T3, T2->T4, T3->T4), viết code Semaphore. 3. Sửa bài toán biến $X$ không quá 20. | **Bẫy 1**: Khởi tạo sai giá trị ban đầu của Semaphore (0 hay 1). **Bẫy 2**: Đặt sai vị trí `wait()` và `signal()`. **Bẫy 3**: Nhầm lẫn giữa Binary Semaphore và Mutex Lock. |
| **Phân tích Deadlock & Đồ thị RAG** | 80% đề Cuối kỳ | Cho đồ thị cấp phát tài nguyên RAG hoặc mô tả tiến trình giữ/yêu cầu tài nguyên. Hỏi hệ thống có Deadlock không? Liệt kê tất cả các chuỗi an toàn. | **Bẫy**: Nếu tài nguyên có nhiều thực thể (multiple instances), chu trình (cycle) KHÔNG ĐỒNG NGHĨA với Deadlock. Phải thử rút gọn đồ thị hoặc chạy thuật toán an toàn. |
| **Thuật toán Banker (Deadlock Avoidance)** | 100% đề Cuối kỳ | Cho ma trận $Allocation$, $Max$, vector $Available$. 1. Tính $Need = Max - Allocation$. 2. Tìm chuỗi an toàn. 3. Xử lý yêu cầu $Request_i$. | **Bẫy 1**: Tính sai ma trận $Need$. **Bẫy 2**: Quên kiểm tra 2 điều kiện: $Request \le Need$ VÀ $Request \le Available$ trước khi cho giả lập cấp phát. **Bẫy 3**: Không cập nhật lại $Available = Available - Request$ khi giả lập. |
| **Cấp phát liên tục & Placement (First-fit, Best-fit, Worst-fit, Next-fit)** | 90% đề Cuối kỳ | Cho danh sách phân vùng nhớ và chuỗi tiến trình xin cấp phát. Xác định tiến trình nào được cấp phát, tiến trình nào phải chờ. So sánh Phân vùng cố định vs Phân vùng động. | **Bẫy**: Next-fit tiếp tục tìm từ vị trí phân vùng vừa cấp phát cho tiến trình trước đó, KHÔNG quay lại đầu danh sách. |
| **Ánh xạ địa chỉ Phân trang (Paging)** | 100% đề Cuối kỳ | Cho địa chỉ logic hoặc physical, kích thước trang/frame. Chuyển đổi $Logical \leftrightarrow Physical$. Cho bảng trang 2-3 cấp, tính số bit trang/offset. | **Bẫy 1**: Nhầm kích thước trang $2^k$ (ví dụ $4KB = 2^{12}$ bytes $\Rightarrow offset = 12$ bits). **Bẫy 2**: Quên rằng $offset$ giữ nguyên khi chuyển từ địa chỉ ảo sang địa chỉ vật lý! |
| **Thời gian truy xuất hiệu dụng EAT (TLB)** | 90% đề Cuối kỳ | Cho $t_{RAM}$, $t_{TLB}$, hit ratio $\alpha$. Tính $EAT$. Hoặc cho $EAT$, tính $\alpha$. | **Bẫy 1**: Nếu đề ghi "thời gian tìm trong TLB xem như bằng 0" ($\epsilon = 0$), công thức là $EAT = \alpha \cdot t_{RAM} + (1-\alpha) \cdot 2t_{RAM} = (2-\alpha)t_{RAM}$. **Bẫy 2**: Nếu đề cho $t_{TLB} > 0$, công thức đầy đủ là $EAT = \alpha(t_{TLB} + t_{RAM}) + (1-\alpha)(t_{TLB} + 2t_{RAM}) = t_{TLB} + (2-\alpha)t_{RAM}$. |
| **Thay thế trang (Page Replacement: FIFO, OPT, LRU)** | 100% đề Cuối kỳ | Cho chuỗi truy xuất (Reference string) và $N$ khung trang. Vẽ bảng trạng thái bộ nhớ và tính số Page Fault. | **Bẫy 1**: Trạng thái ban đầu các khung trang trống (ban đầu nạp trang vào khung trống VẪN TÍNH LÀ PAGE FAULT). **Bẫy 2**: Nhầm giữa LRU (nhìn về QUÁ KHỨ) và OPT (nhìn vào TƯƠNG LAI). **Bẫy 3**: Khi trang đã có sẵn trong khung (Hit), KHÔNG tăng số page fault và cập nhật vị trí thời gian cho LRU. |

---

## 3. CÔNG THỨC CHUẨN CẦN NHỚ CHO THI

1. **CPU Scheduling**:
   - $TAT = CT - AT$
   - $WT = TAT - BT$
   - $RT = \text{First\_Time\_Exec} - AT$

2. **Banker's Algorithm**:
   - $Need[i][j] = Max[i][j] - Allocation[i][j]$
   - Điều kiện cấp phát $Request_i$:
     $$\begin{cases} Request_i \le Need_i \\ Request_i \le Available \end{cases}$$

3. **Paging & Address Translation**:
   - Page size = $2^d$ bytes $\Rightarrow$ $d$ bits offset.
   - Logical Address = $p \cdot 2^d + d$ (hoặc ghép bit $p \parallel d$).
   - Physical Address = $f \cdot 2^d + d$ (hoặc ghép bit $f \parallel d$).

4. **TLB & EAT**:
   - $EAT = t_{TLB} + (2 - \alpha) \cdot t_{RAM}$

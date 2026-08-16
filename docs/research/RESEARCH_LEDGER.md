# RESEARCH LEDGER — IT007 UIT

Nhật ký nghiên cứu, kiểm chứng và đối chiếu kiến thức giữa Đề cương UIT ↔ Tiêu chuẩn POSIX ↔ Linux Kernel.

---

## BẢNG NHẬT KÝ NGHIÊN CỨU & KIỂM CHỨNG

| STT | Chủ đề | Nguồn tham chiếu | Ngày kiểm chứng | Kết luận sử dụng trong sách | Chương áp dụng | Mức độ tin cậy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `printf` buffer behavior trong `fork()` | POSIX IEEE Std 1003.1 & C Standard | 2026-08-13 | Khi `printf` không có ký tự `\n`, dữ liệu nằm trong bộ đệm Userspace (`stdout` buffer). Khi gọi `fork()`, bộ đệm này bị nhân đôi sang tiến trình con. Kết quả chuỗi sẽ bị in ra 2 lần ngoại trừ trường hợp flush buffer bằng `fflush(stdout)` hoặc dùng `\n` trước `fork()`. | Chương 3 (Quản lý tiến trình) | **Tier A/B Verified** |
| 2 | Quy ước Độ ưu tiên trong Priority Scheduling | UIT Slide Week 05 & Đề thi 2018-2025 | 2026-08-13 | Đề thi UIT **luôn mặc định quy ước**: Số nguyên nhỏ hơn đại diện cho Độ ưu tiên CAO HƠN (ví dụ Priority 1 > Priority 2 > Priority 3). Nếu đề bài không ghi chú gì khác, áp dụng đúng quy ước này. | Chương 4 (Định thời CPU) | **Tier A Verified** |
| 3 | Công thức EAT có TLB lookup time | Silberschatz OS Concepts & UIT Slide Ch7 | 2026-08-13 | Phân biệt 2 biến thể công thức EAT:<br>1. Nếu đề ghi "thời gian tìm trong TLB bằng 0" ($\epsilon = 0$): $EAT = (2 - \alpha) \cdot t_{RAM}$.<br>2. Nếu đề cho $\epsilon = t_{TLB} > 0$: $EAT = t_{TLB} + (2 - \alpha) \cdot t_{RAM}$. Sách Cẩm nang sẽ trình bày cả 2 trường hợp và chỉ ra cách thế số đúng. | Chương 7 (Quản lý bộ nhớ) | **Tier A/B Verified** |
| 4 | Trạng thái an toàn Safe State vs Deadlock | Silberschatz Ch7 & UIT Slide Ch6 | 2026-08-13 | - **Hệ thống ở trạng thái An toàn (Safe State)** $\Rightarrow$ Chắc chắn KHÔNG bao giờ bị Deadlock.<br>- **Hệ thống ở trạng thái Unsafe State** $\Rightarrow$ CHƯA CHẮC đã bị Deadlock ngay (có khả năng dẫn tới Deadlock nếu các tiến trình đòi tối đa tài nguyên).<br>- **Deadlock** là tập con của Unsafe State. | Chương 6 (Deadlock) | **Tier A/B Verified** |
| 5 | Sự khác biệt giữa Mutex Lock và Binary Semaphore | POSIX Pthreads & Linux Kernel Documentation | 2026-08-13 | - **Mutex Lock**: Có khái niệm "Ownership" (tiến trình/thread nào LOCK thì CHỈ TIẾN TRÌNH/THREAD ĐÓ mới được UNLOCK).<br>- **Binary Semaphore**: Không có Ownership, bất kỳ tiến trình nào cũng có thể gọi `signal()` / `sem_post()` để giải phóng, dùng tốt cho đồng bộ thứ tự (Signal-Wait synchronization). | Chương 5 (Đồng bộ tiến trình) | **Tier B Verified** |
| 6 | Nghịch lý Belady (Belady's Anomaly) | Operating System Concepts & UIT Exams | 2026-08-13 | Nghịch lý Belady xảy ra trên thuật toán FIFO: Tăng số khung trang (Frame) làm TĂNG số lỗi trang (Page Fault). LRU và OPT KHÔNG BAO GIỜ bị ảnh hưởng bởi nghịch lý Belady vì chúng thuộc lớp thuật toán Stack Algorithms. | Chương 8 (Bộ nhớ ảo) | **Tier A/B Verified** |

# BẢN ĐỒ BIẾN THỂ THỰC HÀNH LAB IT007 UIT (LAB VARIANT MAP)

Tài liệu này ghi nhận và phân loại toàn bộ các biến thể bài thực hành Lab IT007 qua các năm học, các chương trình đào tạo (Chuẩn, CLC, Khoa KTMT, Khoa HTTT, Khoa CNPM) tại UIT.

---

## 1. Bản Đồ Biến Thể Chi Tiết Từng Bài Lab (Lab 1 — Lab 6)

| Bài Lab | Biến thể / Năm học | Tên bài thực hành | Mục tiêu học thuật chính | API & Công cụ bắt buộc | Hình thức nộp / Đánh giá | Mức độ tin cậy | Ghi chú lịch sử / Đặc thù |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **Lab 1** | Chuẩn (v2023–2024) | Giới thiệu Linux & Môi trường thực hành | Làm quen terminal, hệ thống tệp Linux, quản lý phân quyền tệp/thư mục, lệnh quản lý tiến trình. | `bash`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`, `chmod`, `chown`, `grep`, `find`, `ps`, `top`, `kill`, `gcc` | Báo cáo PDF + Trả lời câu hỏi chuẩn bị | `OBSERVED` | Áp dụng thống nhất cho toàn bộ các lớp IT007. |
| **Lab 2** | Chuẩn (v2023–2024) | Lập trình Shell Script (Bash) | Xây dựng kịch bản tự động hóa trên Linux: Biến, điều kiện `if-else`, vòng lặp `for`/`while`/`until`, hàm, xử lý chuỗi, đọc ghi tệp và tham số dòng lệnh `$1, $2, $@`. | Bash scripting, `read`, `expr`, `test`, `[ ]`, `$?`, `case-esac` | Source code `.sh` + Báo cáo kết quả chạy | `OBSERVED` | Bài tập viết shell script tính toán, quản lý người dùng và duyệt thư mục. |
| **Lab 3** | Chuẩn (v2023–2024) | Quản lý Tiến trình (Process Management) | Lập trình C trên Linux để tạo lập và điều khiển tiến trình: Không gian nhớ tiến trình cha/con, nạp chương trình mới, đồng bộ chờ tiến trình con, bắt tín hiệu Signal cơ bản. | `fork()`, `execvp()`, `execlp()`, `wait()`, `waitpid()`, `exit()`, `getpid()`, `getppid()`, `signal()`, `kill()` | Source code `.c` + Báo cáo chụp màn hình + Vấn đáp | `OBSERVED` | Bài tập kinh điển: Chương trình tạo cây tiến trình, sao chép file, xử lý tín hiệu SIGINT/SIGUSR1. |
| **Lab 4** | Chuẩn (v2023–2024) | Đa luồng & Giao tiếp Liên tiến trình (Threads & IPC) | Lập trình đa luồng với thư viện POSIX Threads; giao tiếp dữ liệu giữa các tiến trình độc lập qua Shared Memory và Đường ống Pipe. | `pthread_create()`, `pthread_join()`, `pthread_exit()`, `pipe()`, `shmget()`, `shmat()`, `shmdt()`, `shmctl` hoặc POSIX `shm_open()`, `mmap()` | Source code `.c` + Báo cáo kiểm tra bộ nhớ chia sẻ | `OBSERVED` | Trọng tâm: So sánh hiệu năng giữa Multi-thread và Multi-process; truyền dữ liệu qua Pipe và Shared Memory. |
| **Lab 5** | Chuẩn (v2023–2024) | Đồng bộ Tiến trình & Luồng (Synchronization) | Nhận diện hiện tượng Race Condition trong thực tế; áp dụng POSIX Semaphore và Mutex Lock để đồng bộ hóa tài nguyên chia sẻ và giải quyết bài toán Bounded Buffer. | `sem_init()`, `sem_wait()`, `sem_post()`, `sem_destroy()`, `pthread_mutex_init()`, `pthread_mutex_lock()`, `pthread_mutex_unlock()` | Source code `.c` + Phân tích kết quả chạy khi có/không đồng bộ | `OBSERVED` | Bài tập hiện thực hóa mô hình Producer-Consumer ($sells \le products \le sells + MSSV$) và bài toán đồng bộ mảng. |
| **Lab 6** | **Biến thể A (Hiện hành P19.1 — v2023–2024)** | **Bài Thực Hành Tổng Hợp: Trình thông dịch lệnh `it007sh`** | Xây dựng một Command Line Shell hoàn chỉnh hỗ trợ chạy lệnh con, chuyển hướng I/O (`>`, `<`), đường ống Pipe (`|`), bắt tín hiệu Ctrl+C/Ctrl+\, và chạy lệnh nối tiếp (`;`). | `fork()`, `execvp()`, `waitpid()`, `open()`, `dup2()`, `pipe()`, `close()`, `sigaction()`, `strtok_r()` | Source code `it007sh.c` + Makefile + Video demo + Vấn đáp | `REPEATED PATTERN` | **Đây là biến thể chính thức của tài liệu Lab 6 v2023**. Sách Thực Hành V2 sẽ xây dựng bài học Case Study 7 giai đoạn chuyên sâu cho biến thể này. |
| **Lab 6** | Biến thể B (Lịch sử / Một số lớp HTTT) | Mô phỏng Quản lý Bộ nhớ & Thuật toán Thay thế trang | Lập trình C mô phỏng giải thuật cấp phát bộ nhớ liên tục (First-fit, Best-fit, Worst-fit) và giải thuật thay thế trang (FIFO, LRU). | C programming, structs, dynamic array, file I/O | Source code `.c` + Báo cáo so sánh số lỗi trang | `OBSERVED` | Cần đưa vào phần Bài tập mở rộng nâng cao để sinh viên thuộc mọi hệ đào tạo đều có tài liệu tham khảo. |

---

## 2. Kết Luận Kiến Trúc Cho Sách Thực Hành V2 (Book B)

Sách Thực Hành V2 (**THỰC HÀNH HỆ ĐIỀU HÀNH — IT007**) sẽ được tổ chức như sau:
1. **Phần Mở Đầu**: Hướng dẫn toàn diện về môi trường Linux (Ubuntu/WSL), Terminal, Trình biên dịch GCC, Trình gỡ lỗi GDB, Công cụ theo dõi System Call Strace, và Tệp tự động hóa Makefile.
2. **Chương Lab 1**: Thực hành Linux cơ bản & Quản trị hệ thống tệp.
3. **Chương Lab 2**: Lập trình kịch bản Bash Shell từ cơ bản đến nâng cao.
4. **Chương Lab 3**: Lập trình Quản lý Tiến trình (`fork`, `exec`, `waitpid`, `signal`).
5. **Chương Lab 4**: Lập trình Đa luồng (POSIX Threads) & Giao tiếp Liên tiến trình (Pipe, Shared Memory).
6. **Chương Lab 5**: Lập trình Đồng bộ hóa (Semaphore, Mutex) giải quyết Race Condition.
7. **Chương Lab 6 (Special Case Study)**: Xây dựng Trình thông dịch lệnh `it007sh` hoàn chỉnh qua **7 giai đoạn kiến trúc** có sơ đồ File Descriptor và bảng kiểm thử độc lập.
8. **Phụ lục Nâng cao**: Mô phỏng giải thuật Thay thế trang & Quản lý bộ nhớ (Biến thể Lab 6B).

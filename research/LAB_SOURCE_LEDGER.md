# SỔ TAY TÀI LIỆU KỸ THUẬT & API THỰC HÀNH LINUX (LAB SOURCE LEDGER)

Tài liệu này tổng hợp toàn bộ các liên kết tài liệu kỹ thuật chuẩn quốc tế (POSIX.1-2017, Linux Man-Pages man7.org, GNU glibc Manual) cho từng hàm C API, System Call và công cụ được sử dụng trong **Sách Thực Hành Hệ Điều Hành IT007 (Book B)**.

---

## 1. Danh Mục System Calls & POSIX C APIs Sử Dụng Trong Lab

| Tên Hàm / Lệnh | Header File | Chuẩn Đặc Tả | Tài Liệu Kỹ Thuật (Man Page / Spec URL) | Vai Trò & Chức Năng Trong Bài Lab |
| :--- | :--- | :--- | :--- | :--- |
| `fork()` | `<unistd.h>` | POSIX.1-2001, SVr4, 4.3BSD | [`man 2 fork`](https://man7.org/linux/man-pages/man2/fork.2.html) | Nhân bản tiến trình hiện tại tạo ra một tiến trình con độc lập với không gian nhớ bản sao (Copy-on-Write). |
| `execvp()` / `execlp()` | `<unistd.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 exec`](https://man7.org/linux/man-pages/man3/exec.3.html) | Thay thế toàn bộ không gian nhớ của tiến trình hiện tại bằng một chương trình thực thi mới. |
| `wait()` / `waitpid()` | `<sys/wait.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 2 waitpid`](https://man7.org/linux/man-pages/man2/waitpid.2.html) | Tạm dừng tiến trình cha chờ tiến trình con thay đổi trạng thái (kết thúc), thu hồi tài nguyên PCB tránh Zombie. |
| `exit()` / `_exit()` | `<stdlib.h>` / `<unistd.h>` | C89, C99, POSIX.1-2001 | [`man 3 exit`](https://man7.org/linux/man-pages/man3/exit.3.html) | Chấm dứt tiến trình bình thường, dọn dẹp buffer stdio và trả mã thoát `status` cho tiến trình cha. |
| `getpid()`, `getppid()`| `<unistd.h>` | POSIX.1-2001, 4.3BSD, SVr4 | [`man 2 getpid`](https://man7.org/linux/man-pages/man2/getpid.2.html) | Lấy định danh tiến trình hiện tại (PID) hoặc định danh tiến trình cha (PPID). |
| `pipe()` | `<unistd.h>` | POSIX.1-2001, 4.3BSD | [`man 2 pipe`](https://man7.org/linux/man-pages/man2/pipe.2.html) | Tạo kênh truyền thông đơn hướng (Unidirectional data channel) gồm đầu đọc `pipefd[0]` và đầu ghi `pipefd[1]`. |
| `dup()`, `dup2()` | `<unistd.h>` | POSIX.1-2001, SVr4, 4.3BSD | [`man 2 dup2`](https://man7.org/linux/man-pages/man2/dup2.2.html) | Nhân bản file descriptor, cho phép chuyển hướng I/O tiêu chuẩn (`stdin = 0`, `stdout = 1`, `stderr = 2`) sang file hoặc pipe. |
| `open()`, `close()` | `<fcntl.h>`, `<unistd.h>` | POSIX.1-2001, SVr4, 4.3BSD | [`man 2 open`](https://man7.org/linux/man-pages/man2/open.2.html) | Mở/tạo tệp tin với các cờ `O_RDONLY`, `O_WRONLY`, `O_CREAT`, `O_TRUNC` và đóng descriptor giải phóng bảng tệp. |
| `signal()`, `sigaction()`| `<signal.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 2 sigaction`](https://man7.org/linux/man-pages/man2/sigaction.2.html)| Đăng ký hàm xử lý tín hiệu bất đồng bộ (Signal Handler) cho các tín hiệu `SIGINT` (Ctrl+C), `SIGQUIT` (Ctrl+\), `SIGCHLD`. |
| `kill()` | `<signal.h>` | POSIX.1-2001, 4.3BSD, SVr4 | [`man 2 kill`](https://man7.org/linux/man-pages/man2/kill.2.html) | Gửi tín hiệu Signal đến một tiến trình hoặc một nhóm tiến trình cụ thể qua PID. |
| `pthread_create()` | `<pthread.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 pthread_create`](https://man7.org/linux/man-pages/man3/pthread_create.3.html) | Tạo một luồng thực thi mới bên trong tiến trình hiện tại chạy hàm mục tiêu `start_routine`. |
| `pthread_join()` | `<pthread.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 pthread_join`](https://man7.org/linux/man-pages/man3/pthread_join.3.html) | Tạm dừng luồng hiện tại chờ luồng mục tiêu kết thúc và thu hồi tài nguyên luồng. |
| `pthread_mutex_init()`| `<pthread.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 pthread_mutex_init`](https://man7.org/linux/man-pages/man3/pthread_mutex_init.3.html) | Khởi tạo khóa Mutex phục vụ loại trừ tương hỗ giữa các luồng. |
| `pthread_mutex_lock()`| `<pthread.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 pthread_mutex_lock`](https://man7.org/linux/man-pages/man3/pthread_mutex_lock.3.html) | Khóa Mutex. Nếu Mutex đang bị khóa bởi luồng khác, luồng gọi sẽ bị block chờ đến khi được mở khóa. |
| `pthread_mutex_unlock()`| `<pthread.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 pthread_mutex_unlock`](https://man7.org/linux/man-pages/man3/pthread_mutex_unlock.3.html) | Mở khóa Mutex, đánh thức các luồng đang chờ tranh chấp. |
| `sem_init()` | `<semaphore.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 sem_init`](https://man7.org/linux/man-pages/man3/sem_init.3.html) | Khởi tạo Semaphore không tên với giá trị ban đầu `value` và cờ chia sẻ `pshared` (0: giữa các luồng, 1: giữa các tiến trình). |
| `sem_wait()` | `<semaphore.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 sem_wait`](https://man7.org/linux/man-pages/man3/sem_wait.3.html) | Thao tác giảm nguyên tử $S.value$. Nếu $S.value \le 0$, luồng bị block vào hàng đợi Semaphore. |
| `sem_post()` | `<semaphore.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 sem_post`](https://man7.org/linux/man-pages/man3/sem_post.3.html) | Thao tác tăng nguyên tử $S.value$, đánh thức luồng đang bị block trên Semaphore. |
| `sem_destroy()` | `<semaphore.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 sem_destroy`](https://man7.org/linux/man-pages/man3/sem_destroy.3.html) | Hủy Semaphore không tên và giải phóng tài nguyên. |
| `shmget()`, `shmat()` | `<sys/shm.h>` | System V IPC, POSIX.1-2001 | [`man 2 shmget`](https://man7.org/linux/man-pages/man2/shmget.2.html) | Cấp phát và gắn kết vùng nhớ chia sẻ (System V Shared Memory) vào không gian địa chỉ ảo của tiến trình. |
| `shm_open()`, `mmap()` | `<sys/mman.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 shm_open`](https://man7.org/linux/man-pages/man3/shm_open.3.html) | Tạo đối tượng bộ nhớ chia sẻ chuẩn POSIX hiện đại và ánh xạ vào RAM. |
| `strtok_r()` | `<string.h>` | POSIX.1-2001, POSIX.1-2008 | [`man 3 strtok_r`](https://man7.org/linux/man-pages/man3/strtok_r.3.html) | Hàm phân tách chuỗi an toàn trong môi trường đa luồng (Reentrant string tokenizer) phục vụ phân tích lệnh trong Shell `it007sh`. |

---

## 2. Tài Liệu Tiêu Chuẩn & Sách Tham Khảo Kỹ Thuật

1. **IEEE Std 1003.1-2017 / POSIX.1-2017**: Tiêu chuẩn quốc tế của IEEE và The Open Group cho hệ thống phần mềm mở.
2. **The Linux Programming Interface (TLPI)** — *Michael Kerrisk*: Cẩm nang toàn diện nhất về lập trình hệ thống Linux và POSIX API.
3. **Advanced Programming in the UNIX Environment (APUE - 3rd Ed.)** — *W. Richard Stevens & Stephen A. Rago*: Tác phẩm kinh điển về kiến trúc tiến trình, tín hiệu và IPC trên môi trường UNIX/Linux.
4. **GNU C Library Manual**: `https://www.gnu.org/software/libc/manual/html_node/`
5. **GNU Bash Reference Manual**: `https://www.gnu.org/software/bash/manual/bash.html`

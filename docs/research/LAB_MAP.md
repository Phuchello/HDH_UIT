# LAB MAP — HỆ ĐIỀU HÀNH IT007 UIT

Bản đồ liên kết giữa **Lý thuyết môn học** ↔ **System Call POSIX/Linux** ↔ **Bài thực hành Lab IT007 UIT**.

---

## BẢNG ÁNH XÁ LÝ THUYẾT - SYSTEM CALL - LAB

| Bài Lab UIT | Nội dung chính | System Calls / Cụm hàm POSIX | Lý thuyết liên quan (Chương) | Bản chất Kernel & Hệ thống xử lý gì? |
| :--- | :--- | :--- | :--- | :--- |
| **Lab 1** | Làm quen môi trường Linux, Shell commands, Terminal, GCC | `man`, `ls`, `grep`, `ps`, `top`, `kill`, `chmod` | Chương 1 & Chương 2 (Dịch vụ HDH, Interface) | Shell đọc lệnh từ `stdin`, parse chuỗi, gọi `fork()` + `execve()` để chạy các chương trình tiện ích hệ thống trong `/bin` hoặc `/usr/bin`. |
| **Lab 2** | Lập trình Shell script Bash (`.sh`), Xử lý chuỗi, Vòng lặp, Kiểm tra ngày tháng | Bash syntax, `if`, `while`, `for`, `read`, `expr` | Chương 2 (Chương trình hệ thống) | Trình thông dịch Bash đọc và thực thi script dạng từng dòng, xử lý biến và trả về exit status code `$?`. |
| **Lab 3** | Quản lý Tiến trình, Tạo tiến trình con, Tương tác tín hiệu (Signal), Bộ nhớ chia sẻ (Shared Memory) | `fork()`, `execvp()`, `wait()`, `waitpid()`, `exit()`, `signal()`, `SIGINT`, `shm_open()`, `ftruncate()`, `mmap()`, `shm_unlink()` | Chương 3 (Quản lý Tiến trình & IPC) | - `fork()` tạo một PCB mới, sao chép không gian địa chỉ virtual memory (Copy-on-Write).<br>- `execvp()` nạp file ELF mới ghi đè lên Segment Code/Data/Stack của tiến trình con.<br>- `wait()` đưa tiến trình cha sang trạng thái `Waiting` cho đến khi tiến trình con phát ra `SIGCHLD`.<br>- `shm_open()` + `mmap()` map chung một vùng Page Table RAM vật lý cho 2 tiến trình khác nhau truy cập trực tiếp. |
| **Lab 4** | Mô phỏng các thuật toán Định thời CPU (FCFS, SJF, Round Robin) bằng C | C Structs, Arrays, Queues, Input/Output file parsing (`input.txt` -> `output.txt`) | Chương 4 (Định thời CPU) | Xây dựng mô hình Ready Queue hàng đợi mô phỏng CPU Scheduler của Kernel (tương tự scheduler CFS trên Linux). Tính toán các chỉ số $WT$, $TAT$, $RT$. |
| **Lab 5** | Đồng bộ tiến trình, Giải quyết Race Condition bằng Semaphore / Mutex / Condition Variable | Pthread library (`pthread_create`, `pthread_join`), POSIX Semaphore (`sem_open`, `sem_wait`, `sem_post`, `sem_destroy`), Mutex (`pthread_mutex_lock`, `pthread_mutex_unlock`) | Chương 5 (Đồng bộ tiến trình) | - `sem_wait()` (tương đương `P()` / `wait()`) giảm giá trị semaphore. Nếu $\le 0$, Kernel treo Thread vào Wait Queue của Semaphore.<br>- `sem_post()` (tương đương `V()` / `signal()`) tăng giá trị semaphore và Đánh thức (Wakeup) Thread trong Wait Queue sang Ready Queue. |
| **Lab 6** | Xây dựng một BỘ ĐỌC VÀ THỰC THI DÒNG LỆNH (Simple Shell) tích hợp Pipe & History | `fork()`, `execvp()`, `waitpid()`, `pipe()`, `dup2()`, `close()`, `termios`, Raw mode | Chương 2 & 3 & 6 (Shell, Redirection, Pipe, IPC) | - `pipe(pipefd)` tạo một buffer trong Kernel space với 2 file descriptor: `pipefd[0]` (đọc) và `pipefd[1]` (ghi).<br>- `dup2(pipefd[1], STDOUT_FILENO)` chuyển hướng chuẩn stdout của lệnh 1 vào đầu ghi pipe.<br>- `dup2(pipefd[0], STDIN_FILENO)` chuyển hướng chuẩn stdin của lệnh 2 vào đầu đọc pipe. |

---

## CHI TIẾT SYSTEM CALL CẦN NẮM VỮNG CHO LAB & THI

### 1. `fork()`
- **Cú pháp**: `pid_t fork(void);`
- **Trả về**:
  - `= 0` trong tiến trình con (Child).
  - `> 0` (PID tiến trình con) trong tiến trình cha (Parent).
  - `< 0` nếu lỗi.
- **Bản chất**: Tạo tiến trình mới nhân bản từ tiến trình hiện tại.

### 2. `execvp()`
- **Cú pháp**: `int execvp(const char *file, char *const argv[]);`
- **Bản chất**: Thay thế hoàn toàn hình ảnh chương trình (Code, Data, Stack) của tiến trình gọi bằng chương trình mới. Nếu thành công, KHÔNG BAO GIỜ TRẢ VỀ.

### 3. `wait()` / `waitpid()`
- **Cú pháp**: `pid_t wait(int *wstatus);` / `pid_t waitpid(pid_t pid, int *wstatus, int options);`
- **Bản chất**: Tạm dừng tiến trình cha cho đến khi tiến trình con kết thúc. Giúp dọn dẹp PCB của tiến trình con, tránh bị hiện tượng Tiến trình ma (Zombie Process).

### 4. `pipe()` & `dup2()`
- **Cú pháp**: `int pipe(int pipefd[2]);` / `int dup2(int oldfd, int newfd);`
- **Bản chất**: Nối `stdout` của tiến trình này vào `stdin` của tiến trình khác thông qua Kernel Buffer.

### 5. `shm_open()` & `mmap()`
- **Cú pháp**: `int fd = shm_open(name, flags, mode);` / `void *ptr = mmap(..., fd, 0);`
- **Bản chất**: Tạo vùng nhớ vật lý dùng chung (Shared Memory) giữa các tiến trình độc lập mà không qua cơ chế chép thông điệp.

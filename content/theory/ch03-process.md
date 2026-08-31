---
id: "theory-ch03-process"
title: "Chương 3: Tiến trình và Tiểu trình"
book: "theory"
chapter: 3
order: 3
slug: "ch03-process"
summary: "Process, bố cục bộ nhớ, trạng thái, PCB, scheduler, fork/exec/wait/exit, IPC và mô hình thread."
prerequisites:
  - "theory-ch02-structure"
related:
  - "sub-ch03"
  - "theory-ch04-cpu-scheduling"
exam_relevance:
  frequent_topics:
    - "Process và memory layout"
    - "Process states, PCB và context switch"
    - "fork/exec/wait/exit, cây tiến trình, zombie/orphan"
    - "IPC shared memory/message passing"
    - "Thread properties và mô hình many-to-one/one-to-one/many-to-many"
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH03-2024"
  - "UIT-QBANK-CH03-2024"
  - "UIT-SLIDE-MIDTERM-REVIEW-2024"
  - "SILBERSCHATZ-OSC10"
  - "POSIX-FORK"
  - "POSIX-EXEC"
  - "POSIX-WAITPID"
  - "POSIX-PIPE"
  - "POSIX-PTHREAD"
last_updated: "2026-08-31"
---

# Chương 3: Tiến trình và Tiểu trình

## Phạm vi và mục tiêu

Theo `UIT-SLIDE-CH03-2024`, slide 4–63 và qbank `UIT-QBANK-CH03-2024`, Câu 1–8 / Mục 3, chương này giải thích một chương trình trở thành thực thể được OS quản lý như thế nào. Các chi tiết gọi hàm Linux/POSIX được đánh dấu là làm rõ từ `POSIX-FORK`, `POSIX-EXEC`, `POSIX-WAITPID`, `POSIX-PIPE` và `POSIX-PTHREAD`.

## 1. Process và bố cục không gian nhớ

Program là file/thủ tục tĩnh; **process** là một instance đang thực thi, có trạng thái CPU, không gian địa chỉ và tài nguyên riêng. Cùng một program có thể có nhiều process.

```
địa chỉ cao  ┌──────────────┐
             │ stack (mỗi thread riêng) │
             ├──────────────┤
             │     heap ↑   │ cấp phát động
             ├──────────────┤
             │ BSS/data     │ biến toàn cục, static (BSS thường zero-init)
             ├──────────────┤
             │ text/rodata  │ mã lệnh, hằng chỉ đọc
địa chỉ thấp └──────────────┘
```

Text thường dùng chung giữa các instance; data chứa biến đã khởi tạo; BSS là vùng biến tĩnh/ toàn cục chưa khởi tạo; heap tăng theo cấp phát; stack chứa frame gọi hàm, tham số và biến cục bộ của **từng thread**. Layout và hướng tăng là mô hình điển hình, có thể thay đổi bởi ABI/ASLR.

## 2. Trạng thái, hàng đợi và PCB

### 2.1 Năm trạng thái kinh điển

```
new ──admit──> ready ──dispatch──> running ──exit──> terminated
                  ▲                  │
       I/O done ──┘                  ├─ I/O/event wait ─> waiting
                  └──── preempt ─────┘
```

- **New:** đang được tạo.
- **Ready:** đã sẵn sàng, chờ CPU trong ready queue.
- **Running:** đang giữ CPU.
- **Waiting/blocked:** chờ I/O, lock hoặc sự kiện; không thể chạy dù CPU rảnh.
- **Terminated:** đã kết thúc, chờ OS thu hồi/ghi nhận trạng thái.

Chuyển running→ready có thể do preemption; running→waiting do yêu cầu I/O; waiting→ready khi sự kiện hoàn tất. Một OS có thể thêm suspended states nhưng không thay thế mô hình 5 trạng thái khi trả lời qbank.

### 2.2 Process Control Block (PCB)

PCB là bản ghi kernel dùng để dừng và tiếp tục process. Các nhóm trường chính:

| Nhóm | Nội dung ví dụ |
| --- | --- |
| Định danh | PID, PPID, user/credential. |
| Trạng thái & thanh ghi | state, program counter, general registers, stack pointer, flags/mode. |
| Thông tin scheduling | priority, queue pointers, CPU time, affinity. |
| Quản lý bộ nhớ | base/limit hoặc page/segment tables, address-space metadata. |
| Accounting | thời gian CPU, giới hạn, job/process number. |
| I/O & file | thiết bị cấp phát, open-file descriptors, pending I/O. |
| Quan hệ/IPC | parent/child, signal, IPC endpoints và quyền. |

Không phải mọi hệ điều hành đặt tên trường giống nhau; điểm cốt lõi là PCB phải đủ để khôi phục execution context và quản lý tài nguyên.

## 3. Scheduler và context switch

| Bộ điều phối | Quyết định | Tần suất/độ nhanh | Tác động |
| --- | --- | --- | --- |
| Long-term (job scheduler) | Job nào được nạp thành process resident. | Thưa, chậm hơn. | Kiểm soát degree of multiprogramming và cân bằng CPU/I/O jobs. |
| Short-term (CPU scheduler) | Process ready nào nhận CPU tiếp. | Rất thường xuyên, cần nhanh. | Chọn algorithm; ảnh hưởng response/waiting. |
| Medium-term | Tạm suspend/swap process rồi đưa trở lại. | Trung gian. | Điều chỉnh memory pressure và degree of multiprogramming. |

Dispatcher trao CPU cho process đã chọn: context switch, đổi mode/address space nếu cần, nhảy tới PC mới. **Context switch** lưu state của P vào PCB/stack và khôi phục state của Q; chi phí gồm lưu/khôi phục register, cache/TLB perturbation, kiểm tra quyền và scheduler/dispatcher time. Nó là overhead, không tạo thêm tiến độ ứng dụng; thời gian cụ thể phụ thuộc kiến trúc.

## 4. Tạo lập process: fork, exec, wait, exit

`fork()` (POSIX) tạo process con gần như bản sao: trả 0 ở con, PID con ở cha, -1 khi lỗi. Cơ chế copy-on-write giúp tránh sao chép ngay toàn bộ page. `exec*()` thay image hiện tại bằng chương trình mới trong **chính process đó**; khi thành công nó không tạo PID mới và PID của process được giữ nguyên, còn text/data/stack được nạp lại. `wait()`/`waitpid()` thu hồi trạng thái con và đồng bộ; `exit()` kết thúc process và gửi trạng thái cho cha.

### Cây process và ví dụ có thứ tự

```c
pid_t p = fork();
if (p == 0) {                 /* child */
    execlp("echo", "echo", "child", (char *)0);
    _exit(127);               /* chỉ chạy nếu exec lỗi */
}
if (p > 0) { waitpid(p, NULL, 0); }
```

Cha gọi `waitpid` nên không thoát trước con trong ví dụ. Trong bài trace, phải tách nhánh theo giá trị trả về của **từng** fork; số process tăng theo số fork được thực thi ở mỗi nhánh, không phải theo số dòng.

```
P0 (fork #1)
├── P1 (child branch)
└── P0 (parent branch; wait P1)
```

### Zombie và orphan

Zombie là child đã `exit` nhưng entry trạng thái chưa được parent thu hồi bằng wait; nó không tiếp tục chạy nhưng giữ một phần metadata. Orphan là child còn chạy khi parent kết thúc; trên Linux/POSIX, một process “reaper” (thường PID 1 hoặc subreaper) nhận nuôi và có thể wait. Đây là hành vi hệ thống cụ thể, không nên suy ra mọi OS giống Linux.

## 5. IPC

| Cơ chế | Luồng dữ liệu | Đồng bộ/bảo vệ | Ưu/nhược |
| --- | --- | --- | --- |
| Shared memory | Các process map chung vùng nhớ; đọc/ghi trực tiếp. | Ứng dụng phải dùng semaphore/mutex/atomic để tránh race. | Nhanh cho dữ liệu lớn; khó thiết kế đúng. |
| Message passing | OS truyền message qua mailbox/queue/socket. | Kernel kiểm soát endpoint và thứ tự theo API. | Cô lập, hợp phân tán; copy/overhead cao hơn. |
| Pipe (POSIX) | Byte stream một chiều giữa các descriptor; named pipe có tên. | `read`/`write` có thể block; descriptor inheritance qua fork. | Đơn giản cho pipeline; không phù hợp mọi topology. |

Shared memory là cơ chế chia sẻ dữ liệu, không tự là giải pháp đồng bộ. Pipe là API cụ thể của message/stream IPC, không phải mọi IPC.

## 6. Threads

Thread là đơn vị thực thi trong process. Các thread cùng process chia sẻ text, data, heap, open files và address space; mỗi thread sở hữu PC, register set, stack và scheduling state riêng. Vì vậy thread tạo/đổi context nhẹ hơn process nhưng lỗi/race có thể lan trong cùng address space.

**Lợi ích:** responsiveness (UI không bị chặn), resource sharing, economy (nhẹ hơn process), scalability trên multicore. Cái giá là đồng bộ, debug khó và cần xử lý race/exception.

| Mô hình | Ánh xạ user threads : kernel threads | Ưu điểm | Giới hạn |
| --- | --- | --- | --- |
| Many-to-one | Nhiều : 1 | User library nhanh, portable. | Một blocking syscall chặn cả process; không chạy song song đa core. |
| One-to-one | 1 : 1 | Blocking thread không chặn thread khác; song song thật. | Tạo/quản lý kernel thread tốn tài nguyên; OS có thể giới hạn số lượng. |
| Many-to-many | Nhiều : nhiều (pool kernel) | Cân bằng song song và chi phí. | Runtime/kernel phối hợp phức tạp. |

User-level scheduling (PCS) chọn thread trong process; kernel-level scheduling (SCS) chọn kernel thread trên CPU. Tên và chi tiết mapping phụ thuộc runtime/OS.

## 7. Kiểm tra nhanh

- Phân biệt “process terminated” và “zombie” bằng câu hỏi: còn chạy không, còn metadata không?
- Với `fork` + `exec`, dòng nào tạo PID mới và dòng nào thay image?
- Liệt kê những gì hai thread chia sẻ và hai thứ mỗi thread bắt buộc có riêng.

Ngân hàng câu hỏi: [[sub-ch03]] · Định thời CPU tiếp theo: [[theory-ch04-cpu-scheduling]]

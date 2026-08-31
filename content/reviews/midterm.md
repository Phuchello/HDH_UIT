---
id: "review-midterm"
title: "Ôn tập Giữa kỳ IT007 — Chương 1–4"
book: "review"
chapter: "midterm"
order: 5
slug: "midterm"
summary: "Bản ôn tập dựng từ slide Midterm Review và câu hỏi Chương 1–4; gồm recall, lý thuyết, so sánh, fork và scheduling."
prerequisites:
  - "theory-ch01-overview"
  - "theory-ch02-structure"
  - "theory-ch03-process"
  - "theory-ch04-cpu-scheduling"
related:
  - "sub-ch01"
  - "sub-ch02"
  - "sub-ch03"
  - "sub-ch04"
sources:
  - "UIT-SLIDE-MIDTERM-REVIEW-2024"
  - "UIT-QBANK-CH01-2024"
  - "UIT-QBANK-CH02-2024"
  - "UIT-QBANK-CH03-2024"
  - "UIT-QBANK-CH04-2024"
  - "SILBERSCHATZ-OSC10"
last_updated: "2026-08-31"
---

# Ôn tập Giữa kỳ IT007 — Chương 1–4

## Cách dùng và giới hạn bằng chứng

Khung này được tổng hợp từ canonical PPTX `UIT-SLIDE-MIDTERM-REVIEW-2024`, slide 2–16, và các qbank Chương 1–4 đã đăng ký. Tài liệu lịch sử chỉ cho biết phong cách quan sát được; không có tuyên bố “UIT luôn hỏi”, điểm số hay barem chính thức nếu không có locator xác minh. Hãy trả lời theo cơ chế và đặc tính trước, sau đó mới dùng mẹo nhận diện.

## Format shown in the official 2024 Midterm Review

Slide 2 của bộ `UIT-SLIDE-MIDTERM-REVIEW-2024` trình bày một format lịch sử của đợt ôn tập này:

| Phần | Cấu trúc thể hiện trên slide | Điểm thể hiện trên slide |
| --- | --- | ---: |
| Tự luận | Câu ngắn + tạo tiến trình: 3 câu | 1.5 |
| Tự luận | Định thời CPU: 2 câu | 2.5 |
| Trắc nghiệm (MCQ) | 12 câu, mỗi câu 0.5 | 6.0 |

Tổng format được trình bày là 10 điểm. Đây là thông tin **đặc thù của slide ôn tập 2024**, không phải cam kết cho mọi học kỳ; không dùng nó để suy ra thời lượng, barem hay cấu trúc kỳ thi khác nếu không có nguồn xác minh.

## Chương 1 — Source prompts

Canonical slide 5 có **9 question bullets**. Các bullet dưới đây là occurrence riêng biệt trong review, có thể trỏ về lời giải qbank nhưng không làm mất locator slide:

1. Computer-system structure: các thành phần và vai trò của hệ thống máy tính (`UIT-SLIDE-MIDTERM-REVIEW-2024`, slide 5, bullet 1).
2. User view và system view của hệ điều hành (slide 5, bullet 2).
3. System programs so với application programs (slide 5, bullet 3).
4. Interrupt, trap/exception và chu trình xử lý (slide 5, bullet 4).
5. Storage hierarchy và caching/locality (slide 5, bullet 5).
6. Single-processor, SMP/AMP và clustered systems (slide 5, bullet 6).
7. Dual mode, mode bit và privileged instruction (slide 5, bullet 7).
8. Timer, protection và lý do OS lấy lại CPU (slide 5, bullet 8).
9. Hard real-time so với soft real-time (slide 5, bullet 9).

## Chương 2 — Source prompts

Canonical slide 7 có **5 question bullets**:

1. OS structures và ví dụ monolithic/microkernel (slide 7, bullet 1).
2. System programs: nhóm chức năng và ví dụ (slide 7, bullet 2).
3. OS services cho user/program và system-efficiency services (slide 7, bullet 3).
4. System calls, API và cách truyền tham số (slide 7, bullet 4).
5. Protection/security boundary và sự khác nhau giữa component, service, system program (slide 7, bullet 5).

## Chương 3 — Source prompts

Canonical slide 9 có **6 question bullets**:

1. Process và program; process address space (slide 9, bullet 1).
2. Process states và state-transition diagram (slide 9, bullet 2).
3. PCB và context switch (slide 9, bullet 3).
4. Vì sao process hợp tác/cooperating (slide 9, bullet 4).
5. Parent/child và thứ tự thực thi (slide 9, bullet 5).
6. Threads: lợi ích và mô hình mapping (slide 9, bullet 6).

Slide 10 có **1 compound state-transition exercise**: từ chuỗi sự kiện arrival, I/O, preemption và termination, vẽ trạng thái/giải thích từng cạnh (`MIDTERM-REVIEW-10`). Slide 11 có **1 compound fork/output/process-tree exercise** (`MIDTERM-REVIEW-11`): đếm process theo từng nhánh, thứ tự output chỉ kết luận khi có `wait`/đồng bộ; `exec` không tạo PID mới.

## Chương 4 — Source prompts

Canonical slide 14 có **10 question bullets**:

1. Vì sao cần scheduling và các loại scheduler.
2. Định nghĩa CPU scheduling và scheduler chịu trách nhiệm.
3. Chi phí scheduling/dispatch.
4. Các tiêu chí đánh giá (slide nêu sáu; qbank wording “năm” được giữ nguyên ở qbank).
5. Tên các thuật toán scheduling.
6. Đặc tính, ưu/nhược của FCFS/SJF/SRTF/RR/Priority/HRRN/MQ/MFQ.
7. Multiprocessor scheduling và load balancing.
8. Real-time scheduling.
9. Linux CFS.
10. Windows scheduling.

Solaris không phải prompt của Midterm Review; nó chỉ là phần đọc thêm trong canonical Chương 4 Part 2.

Slide 15 có **1 compound scheduling calculation exercise** (`MIDTERM-REVIEW-15`): giải FCFS, preemptive SJF và RR với `q=10`, ghi arrival/burst, decision mode, tie-break và CT/TAT/WT/RT.

## Reference to external exercise set

Slides 12 và 16 chỉ tham chiếu các bài tập còn lại. Chúng được ghi là `REFERENCE_TO_EXTERNAL_EXERCISE_SET` trong question manifest, không được biến thành câu hỏi tự phát hay gán đáp án không có source locator.

## A. Core-property recall

1. OS có hai góc nhìn nào? — User view (tiện dụng/phản hồi) và system view (resource allocator/control program).
2. IVT và ISR là gì? — IVT ánh xạ vector tới địa chỉ ISR; ISR phục vụ sự kiện.
3. Ba tiêu chí storage hierarchy? — access time/speed, capacity, cost per bit.
4. CPU, processor và core khác nhau thế nào? — processor là đơn vị được lập lịch; core là engine bên trong package; “CPU” cần nói rõ cấp phần cứng.
5. PCB giữ những nhóm trường nào? — identity/state/registers, scheduling, memory, accounting, I/O/file và quan hệ/IPC.
6. TAT, WT, RT? — `CT−AT`, thời gian trong ready queue, và thời điểm chạy đầu−AT.

## B. Short theory answers

### B1. Interrupt

Nêu nguồn và tính đồng bộ của hardware interrupt/trap, sau đó viết chuỗi `save state → IVT → ISR → restore`. System call là trap có chủ đích; page fault là exception được kernel xử lý. Locator: `UIT-SLIDE-CH01-2024`, slide 14–22.

### B2. System call

System call là điểm vào kernel có bảo vệ; API là giao diện thư viện có thể bọc nhiều call; ordinary function call không tự đổi đặc quyền. Ba cách truyền tham số: register, block/table trong memory, stack. Locator: `UIT-SLIDE-CH02-2024`, slide 23–35.

### B3. Process lifecycle

Vẽ `new → ready → running → waiting → ready` và `running → terminated`; giải thích PCB, scheduler và context switch. Ready chờ CPU, waiting chờ event. Locator: `UIT-SLIDE-CH03-2024`, slide 4–27.

### B4. Scheduler

Phân biệt scheduler (chọn) và dispatcher (trao CPU). Nêu CPU/I-O burst, dispatch latency và **sáu** metrics trên slide (response, turnaround, waiting, utilization, fairness, throughput); fairness thường được nhận xét định tính. Locator: `UIT-SLIDE-CH04-1-2024`, slide 4–22.

## C. Comparison questions

| Cặp cần phân biệt | Trục trả lời |
| --- | --- |
| Multiprogramming vs time-sharing | CPU utilization/throughput so với response/interactive; timer preemption. |
| SMP vs AMP vs cluster | Bình đẳng/chung memory; chủ–tớ; nhiều nút qua network. |
| Process vs thread | Address space/isolation so với shared memory; PC/register/stack riêng. |
| Monolithic vs microkernel | Kernel boundary, IPC, fault isolation, performance. |
| MLQ vs MLFQ | Queue cố định/không di chuyển so với feedback promotion/demotion/boost. |
| SJF vs SRTF | Non-preemptive shortest burst so với preemptive shortest remaining. |

Khi bảng so sánh dùng thuật ngữ “Linux hybrid” hoặc “SJF luôn tối ưu”, phải ghi phạm vi và giả định; các mệnh đề tuyệt đối là dấu hiệu cần kiểm tra nguồn.

## D. Process/fork trace

### Bài tập

```c
int main(void) {
    pid_t p = fork();
    if (p == 0) { puts("child"); _exit(0); }
    if (p > 0) { waitpid(p, NULL, 0); puts("parent"); }
}
```

**Đáp án kiểm tra:** Có hai process; child in trước, parent in sau nhờ `waitpid`. Nếu `fork` nằm trong vòng lặp, tính số lần fork ở từng nhánh rồi dựng cây; không đếm số dòng mã. `exec` thay image chứ không tạo PID mới. Locator: `UIT-QBANK-CH03-2024`, Câu 5–6 / Mục 3; chi tiết POSIX tại `POSIX-FORK`, `POSIX-WAITPID`.

## E. CPU scheduling practice

### E1. FCFS/SJF/SRTF

Với P1(0,7), P2(2,4), P3(4,1), P4(5,4), SRTF và tie giữ process đang chạy cho:

```
| P1 | P2 | P3 | P2 | P4 | P1 |
0    2    4    5    7    11   16
```

CT lần lượt P1=16, P2=7, P3=5, P4=11; WT = 9,1,0,2; `WTavg = 3.00` và `TATavg = 7.00` khi dùng đúng công thức và BT. Kiểm tra: tổng WT=12 nên `WTavg=3.00`; tổng TAT=28 nên `TATavg=7.00`. Ghi rõ arrival/tie; đổi quy ước có thể đổi Gantt.

### E2. RR và quantum

Với q nhỏ, response thường tốt nhưng context-switch overhead cao; q lớn tiến gần FCFS. Đề phải cho biết quy tắc process đến đúng lúc quantum hết.

### E3. MLFQ

Nêu số queue, algorithm mỗi queue, promotion/demotion, boost và xử lý job mới. Chỉ nói “ưu tiên queue cao” là chưa đủ một lời giải.

## F. Terminology quick check

- **Bootstrap:** firmware nạp kernel.
- **Mode bit:** trong quy ước slide IT007, 0 kernel/1 user; ghi rõ phạm vi.
- **Privileged instruction:** chỉ kernel được phép; user vi phạm tạo exception.
- **System program:** tiện ích user-space gọi system call.
- **Dispatch latency:** thời gian từ quyết định đến khi task mới bắt đầu chạy.
- **Zombie:** child đã exit, chưa wait; **orphan:** child còn chạy, parent đã exit.
- **Aging:** tăng ưu tiên theo thời gian chờ, không phải rút ngắn burst.

## G. Mixed MCQ / True-False có giải thích

1. **Đ/S:** “API luôn là một system call.” — **Sai:** API có thể là wrapper hoặc nhiều call.
2. **Đ/S:** “Ready process đang chờ I/O.” — **Sai:** waiting/blocked mới chờ event; ready chờ CPU.
3. **Đ/S:** “SJF không preemptive và SRTF preemptive.” — **Đúng** theo định nghĩa cơ bản.
4. **MCQ:** Cấu trúc nào đặt service ở user space để cô lập lỗi? — **Microkernel**, với chi phí IPC có thể tăng.
5. **MCQ:** Metric từ arrival đến completion? — **Turnaround time**.
6. **Đ/S:** “Timer giúp user process giữ CPU vô hạn.” — **Sai:** timer giúp kernel preempt/lấy lại quyền.

## Checklist trước khi nộp bài

- Có nêu **định nghĩa + đặc tính + cơ chế + ưu/nhược** thay vì chỉ mẹo?
- Mọi con số Gantt có arrival, BT, quantum và tie-break?
- Mọi claim về Linux/Windows/đề thi có nguồn hoặc được gắn `INSUFFICIENT_EVIDENCE`?
- Nếu cần tự chấm, dùng Complete/Mostly complete/Partial; không tự gán điểm hay gọi là barem chính thức.

Các ngân hàng chi tiết: [[sub-ch01]], [[sub-ch02]], [[sub-ch03]], [[sub-ch04]]

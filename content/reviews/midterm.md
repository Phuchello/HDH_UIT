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

Canonical slide 5 có **9 question bullets**. `source_question` dưới đây giữ wording tiếng Việt theo bản PPTX; phần trong ngoặc chỉ là hướng trả lời, không phải câu hỏi thay thế:

1. **Định nghĩa hệ điều hành?** — nêu vai trò resource allocator/control program.
2. **Cấu trúc hệ thống máy tính gồm những phần nào?** — CPU, bộ nhớ, I/O và bus/interconnect.
3. **Chương trình hệ thống và chương trình ứng dụng khác nhau như thế nào?** — phân biệt tiện ích hỗ trợ hệ thống với phần mềm phục vụ người dùng.
4. **Những đặc điểm cơ bản của ngắt?** — nguồn, tính đồng bộ/bất đồng bộ và chu trình xử lý.
5. **Hệ thống lưu trữ được phân cấp dựa trên những yếu tố nào?** — tốc độ truy cập, dung lượng và chi phí/bit.
6. **Phân biệt các khái niệm cơ bản về bộ xử lý?** — CPU, processor, core theo đúng cấp phần cứng.
7. **Đặc điểm của hệ thống đơn bộ xử lý, hệ thống đa bộ xử lý, hệ thống gom cụm?** — so sánh đơn, SMP/AMP và cluster.
8. **Có những chế độ hoạt động nào bên trong hệ điều hành?** — kernel/supervisor và user theo mode bit của slide.
9. **Đặc điểm của hệ thống đơn chương, đa chương và đa nhiệm?** — tiến hóa từ một chương trình đến nhiều chương trình/interactive sharing.

## Chương 2 — Source prompts

Canonical slide 7 có **5 question bullets**:

1. **Hệ điều hành bao gồm những thành phần nào? Cụ thể từng thành phần?**
2. **Cấu trúc hệ thống gồm những loại nào? Cho ví dụ từng loại (theo sách tham khảo)**
3. **Chương trình hệ thống gồm những chương trình nào?**
4. **Lời gọi hệ thống là gì và dùng để làm gì?**
5. **Hệ điều hành cung cấp những dịch vụ nào?**

Các nội dung về protection/security, API và ranh giới component/service/system program là phần giải thích bổ trợ trong đáp án; chúng không được ghi thành `source_question` mới.

## Chương 3 — Source prompts

Canonical slide 9 có **6 question bullets**:

1. **Một tiến trình chứa những thành phần gì?**
2. **Tiến trình có những trạng thái nào? Cách tiến trình chuyển trạng thái?**
3. **Tại sao phải cộng tác giữa các tiến trình?**
4. **PCB là gì? Dùng để làm gì?**
5. **Tiểu trình là gì?**
6. **Trình tự thực thi của tiến trình cha và tiến trình con?**

Slide 10 và 11 dưới đây là hai bài nguồn độc lập; phần enrichment chỉ nằm trong đáp án, không thay thế wording của sáu bullet trên.

## Chương 4 — Source prompts

Canonical slide 14 có **10 question bullets**:

1. **Tại sao phải định thời? Có những loại bộ định thời nào?**
2. **Định thời CPU là gì? Bộ định thời nào chịu trách nhiệm thực hiện việc này?**
3. **Phí tổn gây ra khi định thời là gì?**
4. **Trình bày các tiêu chuẩn định thời CPU?** (slide nêu sáu; qbank wording “năm” được giữ nguyên ở qbank).
5. **Kể tên các giải thuật định thời CPU?**
6. **Mô tả và nêu ưu điểm, nhược điểm của từng giải thuật định thời sau: FCFS, SJF, SRTF, RR, Priority Scheduling, HRRN, MQ, MFQ.**
7. **Đặc điểm của định thời trên hệ thống có nhiều bộ xử lý? Khi nào cần phải thực hiện cân bằng tải?**
8. **Đặc điểm định thời theo thời gian thực?**
9. **Mô tả các đặc điểm cơ bản của bộ định thời CFS trên Linux?**
10. **Mô tả các đặc điểm cơ bản của định thời trên Windows?**

Solaris không phải prompt của Midterm Review; nó chỉ là phần đọc thêm trong canonical Chương 4 Part 2.

Slide 15 có **1 compound scheduling calculation exercise** (`MIDTERM-REVIEW-15`): dữ liệu canonical gồm P1(AT=0,BT=10), P2(AT=2,BT=29), P3(AT=4,BT=3), P4(AT=5,BT=7), P5(AT=7,BT=12); giải FCFS, SRTF và RR với `q=10`, ghi CT/TAT/WT/RT.

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

### Slide 10 — Source-faithful state-transition answer

**Source question (verbatim):** “Cho đoạn chương trình sau: Hỏi trong quá trình thực thi thì tiến trình khi chạy từ chương trình trên đã trải qua những trạng thái nào? Vẽ sơ đồ chuyển trạng thái trong quá trình thực thi?”

Đây là đúng đoạn mã xuất hiện trên slide (giữ nguyên cả việc slide không chép các `#include`):

```c
/* test.c */
int main(int argc, char** argv)
{
    int a;
    for (int i = 1; i < 5; i++)
    {
        if (i % 2 == 0)
            printf("Hello world\n");
        else
            a = 5*9;
    }
    exit(0);
}
```

Trình tự tối thiểu cần vẽ là `New → Ready → Running → Terminated`. Nếu scheduler trưng dụng CPU, có thể có cạnh `Running → Ready → Running`; lời gọi `printf` có thể đi qua `Waiting/Blocked` tùy runtime và đích I/O. Chỉ từ source này không thể khẳng định một lần chuyển `Waiting` tất định, vì slide không cung cấp hành vi buffering/thiết bị. Biến `a` chỉ là phép tính trong user mode; `exit(0)` kết thúc process.

### Slide 11 — Source-faithful fork/output answer

**Source question (verbatim):** “Cho đoạn chương trình sau: Hỏi khi chạy thì tiến trình được tạo ra từ chương trình trên sẽ in ra màn hình những gì? Vẽ cây tiến trình và những từ được in ra khi thực thi đoạn chương trình trên?”

Đoạn mã canonical của slide 11 là:

```c
#include <stdio.h>
#include <unistd.h>

int main()
{
    int i;
    for (i = 0; i < 4; i++)
    {
        fork();
        printf("hello\n");
    }
    return 0;
}
```

Mỗi vòng lặp, mọi process đi tới vòng đó đều gọi `fork()` đúng một lần. Sau bốn lần `fork`, số process là `2 → 4 → 8 → 16`; vì vậy `FINAL_PROCESS_COUNT = 16`, `NEW_CHILDREN_CREATED = 15`, và số lần các process thực thi `printf` là `TOTAL_PRINTF_EXECUTIONS = 2 + 4 + 8 + 16 = 30`.

Một cây cha–con logic hợp lệ (các nhãn chỉ là ID sư phạm, không phải PID thật) là:

```text
P0
├── P1          (child created by P0 at fork #1)
│   ├── P3      (child created by P1 at fork #2)
│   │   ├── P7  (child created by P3 at fork #3)
│   │   │   └── P15
│   │   └── P11
│   ├── P5
│   │   └── P13
│   └── P9
├── P2          (child created by P0 at fork #2)
│   ├── P6
│   │   └── P14
│   └── P10
├── P4          (child created by P0 at fork #3)
│   └── P12
└── P8          (child created by P0 at fork #4)
```

Sơ đồ trên là **cây process literal**; sơ đồ doubling `2/4/8/16` là **các nhánh thực thi theo từng vòng**. Topology trừu tượng này suy ra được vì mọi process đều thực hiện `fork()` ở mỗi vòng còn lại; PID thật và thứ tự lập lịch/output là không xác định. Với terminal thông thường và line-buffered stdout, kết quả quan sát là 30 dòng `hello`. Khi redirect sang file, full buffering có thể làm bản sao buffer đã chứa dữ liệu đi qua `fork`, nên số dòng thực tế phụ thuộc trạng thái buffer.

## E. CPU scheduling practice

### Slide 15 — Source-faithful solution (canonical dataset)

**Source question (verbatim):** “Cho 5 tiến trình với thời gian vào hàng đợi ready và thời gian cần CPU tương ứng như bảng sau: Vẽ giản đồ Gantt và tính thời gian đợi trung bình, thời gian đáp ứng trung bình và thời gian lưu lại trong hệ thống (turnaround time) trung bình cho các giải thuật sau: FCFS; SJF preemptive; RR với quantum time = 10”

**Dữ liệu và giả định của slide:** P1(AT=0, BT=10), P2(AT=2, BT=29), P3(AT=4, BT=3), P4(AT=5, BT=7), P5(AT=7, BT=12); không có context-switch overhead đáng kể, không có tie cần quy ước thêm. Ba thuật toán là FCFS, SJF trưng dụng/SRTF và Round Robin `q=10`.

**FCFS**

`P1 0–10 | P2 10–39 | P3 39–42 | P4 42–49 | P5 49–61`

| Process | CT | TAT | WT | RT |
| --- | ---: | ---: | ---: | ---: |
| P1 | 10 | 10 | 0 | 0 |
| P2 | 39 | 37 | 8 | 8 |
| P3 | 42 | 38 | 35 | 35 |
| P4 | 49 | 44 | 37 | 37 |
| P5 | 61 | 54 | 42 | 42 |

`WTavg = 24.4`, `RTavg = 24.4`, `TATavg = 36.6`.

**SJF trưng dụng (SRTF)**

`P1 0–4 | P3 4–7 | P1 7–13 | P4 13–20 | P5 20–32 | P2 32–61`

| Process | CT | TAT | WT | RT |
| --- | ---: | ---: | ---: | ---: |
| P1 | 13 | 13 | 3 | 0 |
| P2 | 61 | 59 | 30 | 30 |
| P3 | 7 | 3 | 0 | 0 |
| P4 | 20 | 15 | 8 | 8 |
| P5 | 32 | 25 | 13 | 13 |

`WTavg = 10.8`, `RTavg = 10.2`, `TATavg = 23.0`.

**Round Robin (`q=10`)**

`P1 0–10 | P2 10–20 | P3 20–23 | P4 23–30 | P5 30–40 | P2 40–50 | P5 50–52 | P2 52–61`

| Process | CT | TAT | WT | RT |
| --- | ---: | ---: | ---: | ---: |
| P1 | 10 | 10 | 0 | 0 |
| P2 | 61 | 59 | 30 | 8 |
| P3 | 23 | 19 | 16 | 16 |
| P4 | 30 | 25 | 18 | 18 |
| P5 | 52 | 45 | 33 | 23 |

`WTavg = 19.4`, `RTavg = 13.0`, `TATavg = 31.6`.

The older P1(0,7), P2(2,4), P3(4,1), P4(5,4) SRTF calculation below remains an explicitly labelled **additional practice fixture**, not the Slide 15 source dataset.

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

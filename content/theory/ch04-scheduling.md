---
id: "theory-ch04-cpu-scheduling"
title: "Chương 4: Định thời CPU"
book: "theory"
chapter: 4
order: 4
slug: "ch04-cpu-scheduling"
summary: "CPU–I/O burst, tiêu chí đánh giá, FCFS/SJF/SRTF/Priority/RR/HRRN, MLQ/MLFQ, đa xử lý, real-time và scheduler hệ điều hành."
prerequisites:
  - "theory-ch03-process"
related:
  - "sub-ch04"
  - "theory-ch01-overview"
exam_relevance:
  frequent_topics:
    - "CPU/I-O burst, scheduler, dispatcher và dispatch latency"
    - "FCFS, SJF, SRTF, Priority, RR, HRRN"
    - "Multilevel Queue và Multilevel Feedback Queue"
    - "Thread/multiprocessor scheduling, affinity và load balancing"
    - "RMS, EDF, Linux CFS, Windows và Solaris"
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH04-1-2024"
  - "UIT-SLIDE-CH04-2-2024"
  - "UIT-SLIDE-CH04-3-2024"
  - "UIT-QBANK-CH04-2024"
  - "UIT-SLIDE-MIDTERM-REVIEW-2024"
  - "SILBERSCHATZ-OSC10"
last_updated: "2026-08-31"
---

# Chương 4: Định thời CPU

## Phạm vi và cách giải bài

Nội dung bám `UIT-SLIDE-CH04-1-2024`, slide 4–54; `UIT-SLIDE-CH04-2-2024`, slide 3–32; `UIT-SLIDE-CH04-3-2024`, slide 3–44 và qbank `UIT-QBANK-CH04-2024`, Câu 1–5 / Mục 4. Khi làm bài số, luôn ghi giả định: thời điểm đến, burst, preemptive hay không, quantum, quy tắc tie-break và thời điểm process mới vào ready queue. Không có tie-break “toàn cầu” nếu đề không nêu.

## 1. Vì sao cần định thời?

Một process thường luân phiên **CPU burst** (thực thi) và **I/O burst** (chờ thiết bị). Khi process chuyển waiting, CPU scheduler chọn một process ready khác để tránh CPU rỗi; khi I/O hoàn tất hoặc timer hết quantum, process trở lại ready queue. Scheduler là bộ chọn; dispatcher thực hiện context switch, chuyển mode/address space (nếu cần), nạp thanh ghi và nhảy tới PC. Khoảng từ quyết định đến lúc process mới chạy là **dispatch latency**.

### Tiêu chí

| Tiêu chí | Công thức/ý nghĩa | Hướng tối ưu |
| --- | --- | --- |
| CPU utilization | Tỷ lệ thời gian CPU thực thi công việc hữu ích. | Cao hơn, nhưng không đánh đổi response vô hạn. |
| Throughput | Số process hoàn tất trong một đơn vị thời gian. | Cao hơn. |
| Turnaround (TAT) | `completion − arrival`. | Thấp hơn. |
| Waiting (WT) | Tổng thời gian trong ready queue; với một CPU burst `WT = TAT − BT`. | Thấp hơn. |
| Response (RT) | `lần chạy đầu − arrival`. | Thấp hơn, quan trọng cho tương tác. |

Không có thuật toán tối ưu đồng thời mọi tiêu chí; workload và chính sách hệ thống quyết định trade-off.

## 2. Các thuật toán cơ bản

### 2.1 FCFS — First-Come, First-Served

**Định nghĩa/selection:** chọn process đến ready queue trước; thường non-preemptive. **Cơ chế:** chạy đến hết CPU burst hoặc block. **Ưu:** đơn giản, công bằng theo arrival, overhead thấp. **Hạn chế:** convoy effect làm process ngắn chờ sau process dài; response kém. Starvation không thường xảy ra nếu queue hữu hạn; aging không phải thành phần bắt buộc.

**Ví dụ:** P1(AT=0,BT=5), P2(AT=1,BT=2), P3(AT=2,BT=1) ⇒ `P1 0–5 | P2 5–7 | P3 7–8`; WT lần lượt 0,4,5. Nếu đề cho preemptive FCFS thì đó là chính sách khác; không tự đổi.

### 2.2 SJF — Shortest Job First

**Selection:** trong các process ready, chọn burst CPU kế tiếp ngắn nhất; bản cơ bản non-preemptive. **Cơ chế:** cần ước lượng burst nếu chưa biết. **Ưu:** tối ưu WT trung bình trong mô hình single CPU, biết chính xác burst và không có overhead. **Hạn chế:** burst tương lai khó biết; process dài có thể starvation. **Aging:** tăng ưu tiên theo thời gian chờ để giảm starvation; đó là bổ sung chính sách.

**Worked example:** P1(0,7), P2(2,4), P3(4,1). P1 chạy 0–7; tại 7 chọn P3 7–8 rồi P2 8–12 (nếu không có quy tắc khác). Đừng dùng SJF khi đề nói “shortest **remaining**”.

**Tie:** nếu burst bằng nhau, dùng arrival/ID chỉ khi đề hoặc quy ước lớp học cho phép; nếu không, ghi “đồng hạng, cần giả định”.

### 2.3 SRTF — Shortest Remaining Time First

**Selection:** process có remaining CPU time nhỏ nhất; preemptive SJF. **Cơ chế:** mỗi khi process mới đến hoặc event xảy ra, so sánh remaining time và có thể preempt. **Ưu:** thường giảm WT/TAT của job ngắn và response tốt hơn SJF. **Hạn chế:** context switch nhiều, cần estimate; job dài có thể starvation. Aging/capping priority có thể giảm starvation nhưng không nằm trong định nghĩa SRTF.

**Ví dụ có kiểm tra:** P1(0,7), P2(2,4), P3(4,1), P4(5,4). Với tie giữ process đang chạy: `P1 0–2 | P2 2–4 | P3 4–5 | P2 5–7 | P4 7–11 | P1 11–16`; CT = 16,7,5,11; WT = 9,1,0,2; WTavg = 3.25 và TATavg = 7.00. Nếu tie-break khác, Gantt/WT có thể đổi.

### 2.4 Priority scheduling

**Selection:** process có priority cao nhất; có bản non-preemptive và preemptive. Hướng “số nhỏ ưu tiên cao” hay ngược lại phải ghi theo đề. **Ưu:** biểu đạt importance/deadline. **Hạn chế:** priority thấp starvation; aging tăng priority dần khi chờ. Priority không tự đồng nghĩa với response tốt hay deadline đúng.

**Ví dụ:** P1 priority 2 chạy, P2 priority 1 đến sau. Nếu hệ quy ước 1 cao và preemptive, P2 chiếm ngay; nếu non-preemptive, P1 chạy hết burst. Đây là hai đáp án khác nhau hợp lệ theo hai giả định.

### 2.5 Round Robin (RR)

**Selection:** ready queue vòng tròn, mỗi process tối đa time quantum `q`, hết q thì preempt và xếp cuối hàng nếu còn việc. **Ưu:** response công bằng, phù hợp time-sharing. **Hạn chế:** q quá lớn gần FCFS; q quá nhỏ làm context-switch overhead tăng và throughput giảm. Starvation thấp nếu queue được phục vụ tuần tự; aging không cần thiết trong RR thuần túy.

**Worked example:** P1=5, P2=3, P3=1 đến cùng lúc, q=2 ⇒ `P1 0–2 | P2 2–4 | P3 4–5 | P1 5–7 | P2 7–8 | P1 8–9`. Nếu process đến trong lát, thứ tự “enqueue trước hay sau process hết quantum” phải nêu rõ.

### 2.6 HRRN — Highest Response Ratio Next

**Selection:** non-preemptive, chọn process có `RR = (WT + BT) / BT = 1 + WT/BT` cao nhất khi CPU rảnh. **Ưu:** cân bằng job ngắn và job đã chờ lâu; giảm starvation tự nhiên. **Hạn chế:** cần biết BT và tính lại tại mỗi lần chọn; không preemptive nên job dài đang chạy vẫn giữ CPU. **Aging:** thành phần `WT` chính là cơ chế ưu tiên thời gian chờ.

**Ví dụ:** tại thời điểm chọn, A(WT=4,BT=4) có RR=2; B(WT=1,BT=2) có RR=1.5 ⇒ chọn A. Tie giữa RR bằng nhau cần quy tắc arrival/ID được ghi rõ.

## 3. Multilevel Queue và MLFQ

### 3.1 Multilevel Queue (MLQ)

Ready queue chia thành các lớp cố định (ví dụ interactive và batch); scheduler giữa lớp có thể strict priority hoặc time-slice, bên trong lớp dùng RR/FCFS. Process thường **không đổi lớp**. Ưu: phản ánh loại workload; hạn chế: lớp thấp có starvation và phân loại cứng.

### 3.2 Multilevel Feedback Queue (MLFQ)

Process có thể di chuyển giữa các queue theo hành vi: job dùng hết quantum bị hạ cấp; job I/O-bound/nhường CPU sớm có thể giữ hoặc được nâng cấp; periodic priority boost chống starvation.

```
Q0 (q nhỏ, ưu tiên cao) → Q1 → Q2 (q lớn/FCFS)
          dùng hết q: hạ cấp   nhường sớm: giữ/nâng tùy policy
```

**Thông số bắt buộc:** số queue, algorithm mỗi queue, quy tắc promotion/demotion, priority boost và xử lý process mới. MLFQ linh hoạt, response tốt cho interactive nhưng khó chứng minh fairness nếu policy không đầy đủ. Không tự gán một bộ tham số là “chuẩn UIT”.

## 4. Thread, đa xử lý và load balancing

Thread scheduling có thể theo **PCS** (process contention scope: cạnh tranh trong process) hoặc **SCS** (system contention scope: cạnh tranh với mọi kernel thread). Trên SMP, scheduler phải chọn CPU và thread.

- **Processor affinity:** soft affinity cố gắng giữ thread trên CPU cũ để tận dụng cache; hard affinity ràng buộc tập CPU được phép.
- **Load balancing:** phân phối runnable threads; *push migration* CPU bận đẩy việc ra, *pull migration* CPU rỗi kéo việc vào. Cân bằng quá thường xuyên cũng tốn cache locality.
- **Multiprocessor policies:** global queue đơn giản nhưng tranh chấp; per-CPU queues mở rộng tốt nhưng cần migration.

Các trade-off trên là nguyên lý; implementation Linux/Windows/Solaris có chính sách khác nhau.

## 5. Real-time scheduling

Task real-time có computation time, period/deadline và yêu cầu đúng hạn. **RMS (Rate Monotonic Scheduling)** là fixed priority: period ngắn hơn ⇒ priority cao hơn, thường cho periodic tasks độc lập. **EDF (Earliest Deadline First)** là dynamic priority: deadline gần nhất chạy trước. Cả hai cần giả định về preemption, thời gian chuyển ngữ cảnh và tài nguyên; không tự kết luận schedulable nếu thiếu dữ liệu. Hard real-time coi deadline là điều kiện bắt buộc; soft real-time tối ưu xác suất/chất lượng đúng hạn.

## 6. Scheduler thực tế — đọc đúng mức nguồn

- **Linux CFS:** mô hình hóa fairness bằng virtual runtime (`vruntime`), thường chọn runnable task có `vruntime` nhỏ nhất trong cấu trúc cây cân bằng; weight/nice và kernel version ảnh hưởng chi tiết. “CFS luôn chạy theo FCFS” là sai.
- **Windows:** hệ thống ưu tiên nhiều mức, có dynamic priority boost và quantum/feedback; chi tiết phụ thuộc phiên bản và lớp thread. Không giản lược thành “32 mức cố định” nếu không chỉ rõ tài liệu.
- **Solaris:** có nhiều lớp scheduler (ví dụ time-sharing, real-time) với priority/quantum riêng. Hãy trình bày đúng depth của slide/read-more, không suy ra hành vi mọi bản phát hành.

## 7. Quy trình giải bài định thời

1. Vẽ timeline sự kiện arrival/I-O và ghi ready queue ở từng mốc.
2. Áp selection rule, đánh dấu preemption/quantum và tie-break.
3. Tính CT, TAT, WT, RT từng process; kiểm tra `TAT = WT + BT` khi chỉ có một CPU burst.
4. Báo cáo average và nêu giả định. Gantt là bằng chứng, không thay thế giải thích cơ chế.

Ngân hàng câu hỏi: [[sub-ch04]] · Nền tảng process: [[theory-ch03-process]]

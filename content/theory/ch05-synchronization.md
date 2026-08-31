---
id: "theory-ch05-synchronization"
title: "Chương 5: Đồng bộ Tiến trình"
book: "theory"
chapter: 5
order: 5
slug: "ch05-synchronization"
summary: "Race Condition, Miền găng (Critical Section), 3 yêu cầu giải pháp, Giải pháp Peterson & kiến trúc hiện đại, Memory Barrier, Hỗ trợ phần cứng (test_and_set, compare_and_swap, atomic variables), Mutex Locks, Semaphore, Monitor & Condition Variables, Liveness (Deadlock, Starvation, Priority Inversion & Inheritance protocol), 3 Bài toán kinh điển (Bounded-Buffer, Readers-Writers, Dining-Philosophers)."
prerequisites:
  - "theory-ch03-process"
  - "theory-ch04-cpu-scheduling"
related:
  - "sub-ch05"
  - "theory-ch06-deadlock"
exam_relevance:
  frequent_topics:
    - "Khái niệm Race Condition và lần vết Interleaving Producer-Consumer / PID"
    - "3 yêu cầu vùng tranh chấp: Mutual Exclusion, Progress, Bounded Waiting"
    - "Phân tích 3 giải pháp phần mềm (Turn, Flag, Peterson)"
    - "Hiện tượng Memory Reordering & Memory Barrier trên kiến trúc hiện đại"
    - "Mutex Lock (Spinlock vs Non-busy waiting)"
    - "Semaphore (wait/signal, Counting vs Binary, Block/Wakeup, Deadlock risk)"
    - "Monitor và Condition Variables (cơ chế giải phóng/tái chiếm khóa khi wait)"
    - "Liveness, Deadlock, Starvation, Priority Inversion & Priority Inheritance protocol"
    - "3 Bài toán kinh điển: Bounded-Buffer, Readers-Writers, Dining-Philosophers"
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH05-1-2024"
  - "UIT-SLIDE-CH05-2-2024"
  - "UIT-QBANK-CH05-2024"
  - "SILBERSCHATZ-OSC10"
last_updated: "2026-08-31"
---

# Chương 5: Đồng bộ Tiến trình

> **Căn cứ nguồn học liệu chính tắc:**
> Nội dung chương bám sát hai slide bài giảng chính thức năm 2024 của Khoa Kỹ thuật Máy tính - Trường Đại học Công nghệ Thông tin (ĐHQG-HCM): `UIT-SLIDE-CH05-1-2024` (67 trang) và `UIT-SLIDE-CH05-2-2024` (72 trang), cùng Bộ bài tập chính thức `UIT-QBANK-CH05-2024` (129 đoạn trích xuất XML / 18 câu hỏi cấu trúc).

---

## 1. Bối cảnh và Race Condition

*(Nguồn: `UIT-SLIDE-CH05-1-2024`, Slide 4–16)*

Trong môi trường thực thi đa nhiệm (multiprogramming) hoặc đa luồng (multithreading), các tiến trình chia sẻ tài nguyên bộ nhớ (biến toàn cục, cấu trúc dữ liệu kernel, vùng nhớ dùng chung). Việc các tiến trình thực thi đồng thời và đan xen lệnh máy có thể dẫn đến hiện tượng dữ liệu bị mất tính nhất quán nếu không được điều phối tuần tự.

### 1.1 Vấn đề Producer – Consumer với biến đếm `count`

Xét bài toán Producer – Consumer chia sẻ một bộ đệm vòng có dung lượng tối đa $N$ phần tử:
- Biến nguyên `count` lưu số lượng phần tử hiện có trong bộ đệm (khởi tạo `count = 0`).
- **Tiến trình Producer** thêm phần tử vào bộ đệm và tăng `count`:
  ```c
  while (true) {
      /* sản xuất một item */
      while (count == BUFFER_SIZE)
          ; /* do nothing - chờ đệm có chỗ trống */
      buffer[in] = next_produced;
      in = (in + 1) % BUFFER_SIZE;
      count++;
  }
  ```
- **Tiến trình Consumer** lấy phần tử khỏi bộ đệm và giảm `count`:
  ```c
  while (true) {
      while (count == 0)
          ; /* do nothing - chờ đệm có phần tử */
      next_consumed = buffer[out];
      out = (out + 1) % BUFFER_SIZE;
      count--;
  }
  ```

Ở mức ngôn ngữ bậc cao, thao tác `count++` và `count--` có vẻ là một thao tác đơn lẻ. Tuy nhiên, ở mức hợp ngữ/mã máy, mỗi lệnh được biên dịch thành 3 thao tác phần cứng tách biệt:

$$\text{Producer: } \begin{cases} \text{register}_1 = \text{count} & \text{(1. Nạp từ RAM vào thanh ghi)} \\ \text{register}_1 = \text{register}_1 + 1 & \text{(2. Tăng giá trị thanh ghi)} \\ \text{count} = \text{register}_1 & \text{(3. Ghi lại vào RAM)} \end{cases}$$

$$\text{Consumer: } \begin{cases} \text{register}_2 = \text{count} & \text{(1. Nạp từ RAM vào thanh ghi)} \\ \text{register}_2 = \text{register}_2 - 1 & \text{(2. Giảm giá trị thanh ghi)} \\ \text{count} = \text{register}_2 & \text{(3. Ghi lại vào RAM)} \end{cases}$$

Giả sử ban đầu `count = 5`. Nếu hai tiến trình thực thi đan xen (interleaving) do bộ lập lịch CPU thực hiện chuyển ngữ cảnh (context switch) giữa chừng:

| Thời điểm ($T$) | Tiến trình | Thao tác thực thi | Giá trị thanh ghi nội bộ | Biến `count` trong RAM |
| :---: | :---: | :--- | :---: | :---: |
| $T_0$ | Producer | $\text{register}_1 = \text{count}$ | $\text{register}_1 = 5$ | `5` |
| $T_1$ | Producer | $\text{register}_1 = \text{register}_1 + 1$ | $\text{register}_1 = 6$ | `5` |
| $T_2$ | Consumer | $\text{register}_2 = \text{count}$ *(bị switch sang Consumer)* | $\text{register}_2 = 5$ | `5` |
| $T_3$ | Consumer | $\text{register}_2 = \text{register}_2 - 1$ | $\text{register}_2 = 4$ | `5` |
| $T_4$ | Producer | $\text{count} = \text{register}_1$ *(switch lại Producer)* | $\text{register}_1 = 6$ | **`6`** |
| $T_5$ | Consumer | $\text{count} = \text{register}_2$ *(ghi đè sau cùng)* | $\text{register}_2 = 4$ | **`4`** |

**Kết luận:** Sau khi sản xuất 1 item và tiêu thụ 1 item, giá trị đúng của `count` phải là `5`. Nhưng do sự đan xen không được kiểm soát, giá trị cuối cùng bị sai thành `4` (hoặc `6` nếu Producer ghi sau cùng).

### 1.2 Tranh chấp cấp phát PID trong Kernel

*(Nguồn: Slide 12–13)*

Không chỉ xảy ra ở không gian người dùng, race condition còn xuất hiện trực tiếp trong nhân hệ điều hành. Khi hai tiến trình cha đồng thời gọi lời gọi hệ thống `fork()`:
- Kernel quản lý biến toàn cục `next_available_pid` để cấp định danh tiến trình tiếp theo.
- Cả hai lời gọi `fork()` cùng đọc giá trị `next_available_pid = 2615`.
- Nếu không có cơ chế đồng bộ hóa, cả hai tiến trình con mới sinh sẽ được cấp cùng một PID `2615`, dẫn đến vi phạm tính toàn vẹn của bảng tiến trình (Process Table).

### 1.3 Định nghĩa Tình trạng Tranh chấp (Race Condition)

> **Định nghĩa chuẩn (`UIT-SLIDE-CH05-1-2024`, Slide 14–16):**
> **Tình trạng tranh chấp (Race Condition)** là tình huống mà nhiều tiến trình/tiểu trình cùng truy xuất và thao tác đồng thời trên dữ liệu chia sẻ, trong đó kết quả cuối cùng của việc thực thi phụ thuộc vào **thứ tự truy xuất và đan xen lệnh cụ thể** của các tiến trình.

Để ngăn chặn Race Condition, hệ điều hành bắt buộc phải đảm bảo tại một thời điểm, **chỉ có duy nhất một tiến trình** được phép thao tác trên phần dữ liệu chia sẻ đó. Cơ chế này được gọi là **đồng bộ hóa tiến trình (Process Synchronization)**.

---

## 2. Vấn đề Miền găng và 3 Yêu cầu Giải pháp

*(Nguồn: `UIT-SLIDE-CH05-1-2024`, Slide 17–30)*

### 2.1 Cấu trúc Mã nguồn Tiến trình

Đoạn mã của một tiến trình truy xuất và thao tác trên tài nguyên dùng chung được chia thành 4 phân đoạn chuẩn:

```c
do {
    /* 1. ENTRY SECTION (Vùng vào) */
    // Tiến trình xin phép truy xuất tài nguyên dùng chung.
    
    /* 2. CRITICAL SECTION (Miền găng / Vùng tranh chấp) */
    // Tiến trình thao tác trực tiếp trên dữ liệu/tài nguyên chia sẻ.
    
    /* 3. EXIT SECTION (Vùng ra) */
    // Tiến trình thông báo đã hoàn thành và giải phóng quyền truy xuất.
    
    /* 4. REMAINDER SECTION (Vùng còn lại) */
    // Tiến trình thực hiện các thao tác xử lý độc lập khác.
} while (true);
```

### 2.2 Ba Tiêu chí Bắt buộc của Giải pháp Miền găng

Một giải pháp giải quyết bài toán miền găng được coi là đúng đắn và an toàn khi và chỉ khi thỏa mãn đồng thời cả 3 điều kiện sau:

1. **Loại trừ tương hỗ (Mutual Exclusion):**
   Nếu tiến trình $P_i$ đang thực thi bên trong miền găng của nó, thì không có bất kỳ tiến trình $P_j$ ($j \neq i$) nào khác được phép thực thi bên trong miền găng của nó tại cùng một thời điểm.
2. **Tiến triển (Progress):**
   Nếu hiện tại không có tiến trình nào đang thực thi trong miền găng và có một số tiến trình đang muốn vào miền găng, thì chỉ những tiến trình **không ở trong remainder section** mới được tham gia vào việc quyết định xem tiến trình nào sẽ được vào miền găng tiếp theo, và quyết định này **không thể bị trì hoãn vô thời hạn**.
3. **Chờ đợi có giới hạn (Bounded Waiting):**
   Phải tồn tại một cận trên (giới hạn số lần) về số lượt các tiến trình khác được phép vào miền găng sau khi một tiến trình đã đưa ra yêu cầu vào và trước khi yêu cầu đó được chấp thuận.
   > **Lưu ý phân biệt học thuật:** Bounded Waiting là giới hạn về **số lượt bị vượt mặt** (tránh tình trạng một tiến trình bị đói tài nguyên - starvation vĩnh viễn), **hoàn toàn không đồng nghĩa với giới hạn thời gian thực thi (execution time)** bên trong miền găng của một tiến trình.

### 2.3 Phân loại Giải pháp Đồng bộ

| Nhóm giải pháp | Cơ chế chính | Ưu điểm | Hạn chế |
| :--- | :--- | :--- | :--- |
| **Phần mềm (Software)** | Sử dụng biến chia sẻ và thuật toán luận lý (Dekker, Peterson). | Không yêu cầu phần cứng đặc biệt. | Dễ gặp lỗi trên kiến trúc hiện đại, tiêu tốn CPU do busy waiting. |
| **Phần cứng (Hardware)** | Chỉ thị nguyên tử phần cứng (`test_and_set`, `compare_and_swap`, `Memory Barrier`). | Đơn giản, tốc độ thực thi rất nhanh. | Khó lập trình cho bài toán phức tạp, có thể gây busy waiting. |
| **Hệ điều hành (OS Level)** | Cung cấp các cấu trúc trừu tượng bậc cao (Mutex Lock, Semaphore, Monitor). | Linh hoạt, hỗ trợ cơ chế đưa tiến trình vào hàng đợi ngủ (block/wakeup). | Chi phí context switch khi chuyển đổi trạng thái tiến trình. |

### 2.4 Đánh giá Giải pháp Vô hiệu hóa Ngắt (Disable Interrupts)

*(Nguồn: Slide 29–30)*

Một giải pháp phần cứng đơn giản ở mức nhân là: Trước khi vào miền găng, CPU thực thi lệnh tắt toàn bộ ngắt (`cli`); khi ra khỏi miền găng, bật ngắt trở lại (`sti`).

- **Vì sao không áp dụng cho User Process?**
  Nếu cho phép chương trình người dùng vô hiệu hóa ngắt, một ứng dụng độc hại hoặc bị treo có thể không bao giờ bật lại ngắt, khiến hệ điều hành mất hoàn toàn quyền điều khiển (mất timer interrupt), làm sụp đổ toàn bộ hệ thống.
- **Hạn chế trên Hệ thống Đa xử lý (Multiprocessor):**
  Lệnh tắt ngắt chỉ có hiệu lực trên lõi CPU đang thực thi lệnh đó. Các tiến trình chạy trên các lõi CPU khác vẫn truy xuất đồng thời vào bộ nhớ chia sẻ. Việc truyền tín hiệu tắt ngắt liên lõi (Inter-Processor Interrupt - IPI) có chi phí trễ quá lớn và làm suy giảm nghiêm trọng thông lượng của hệ thống.

---

## 3. Giải pháp Phần mềm và Giải pháp Peterson

*(Nguồn: `UIT-SLIDE-CH05-1-2024`, Slide 31–51)*

Xét hai tiến trình $P_0$ và $P_1$. Ký hiệu $P_i$ là tiến trình đang xét và $P_j$ là tiến trình đối phương ($j = 1 - i$).

### 3.1 Giải pháp Phần mềm 1: Dùng biến `turn`

- **Biến chia sẻ:** `int turn = 0;` (`turn = i` cho phép $P_i$ vào).
- **Cấu trúc tiến trình $P_i$:**
  ```c
  do {
      while (turn != i)
          ; /* busy waiting */
      /* CRITICAL SECTION */
      turn = j;
      /* REMAINDER SECTION */
  } while (true);
  ```
- **Phân tích 3 tiêu chí:**
  - **Mutual Exclusion:** **THỎA MÃN.** Tại một thời điểm, biến `turn` chỉ nhận một giá trị duy nhất ($0$ hoặc $1$), do đó không thể có chuyện cả $P_0$ và $P_1$ cùng vượt qua vòng lặp `while`.
  - **Progress:** **VI PHẠM.** Thuật toán ép buộc hai tiến trình phải luân phiên nghiêm ngặt (Strict Alternation). Giả sử `turn = 0`, $P_0$ vào miền găng, ra gán `turn = 1` rồi vào remainder section rất lâu. Nếu $P_1$ chạy xong và gán `turn = 0`, lúc này $P_0$ không muốn vào nữa nhưng $P_1$ muốn vào tiếp thì $P_1$ bị chặn vĩnh viễn ở `while (turn != 1)` dù miền găng đang trống!
  - **Bounded Waiting:** **THỎA MÃN.** Mỗi tiến trình chỉ phải chờ tối đa 1 lượt.

### 3.2 Giải pháp Phần mềm 2: Dùng mảng `flag[2]`

- **Biến chia sẻ:** `boolean flag[2];` (khởi tạo `flag[0] = flag[1] = false;`). `flag[i] = true` thể hiện $P_i$ muốn vào miền găng.
- **Cấu trúc tiến trình $P_i$:**
  ```c
  do {
      flag[i] = true;
      while (flag[j])
          ; /* busy waiting */
      /* CRITICAL SECTION */
      flag[i] = false;
      /* REMAINDER SECTION */
  } while (true);
  ```
- **Phân tích 3 tiêu chí:**
  - **Mutual Exclusion:** **THỎA MÃN.** $P_i$ chỉ vào miền găng khi `flag[j] == false`.
  - **Progress & Bounded Waiting:** **VI PHẠM (Nguy cơ Deadlock).** Nếu $P_0$ gán `flag[0] = true`, ngay lúc đó context switch sang $P_1$ và $P_1$ gán `flag[1] = true`. Khi đó cả hai cùng chạy đến lệnh `while (flag[j])`. Do cả hai cờ đều bằng `true`, cả $P_0$ và $P_1$ đều lặp vô hạn và không tiến trình nào có thể vào được miền găng.

### 3.3 Giải thuật Peterson

*(Nguồn: Slide 41–46)*

Giải thuật Peterson kết hợp cả hai biến `turn` và mảng `flag[2]`, tạo nên lời giải phần mềm hoàn chỉnh cho bài toán 2 tiến trình.

- **Biến chia sẻ:**
  ```c
  int turn;
  boolean flag[2] = {false, false};
  ```
- **Cấu trúc tiến trình $P_i$ ($i \in \{0, 1\}, j = 1 - i$):**
  ```c
  do {
      flag[i] = true;              // Bày tỏ ý định muốn vào
      turn = j;                    // Nhường quyền ưu tiên cho đối phương
      while (flag[j] && turn == j)
          ; /* busy waiting */
      
      /* CRITICAL SECTION */
      
      flag[i] = false;             // Báo hiệu đã rời khỏi miền găng
      
      /* REMAINDER SECTION */
  } while (true);
  ```

#### Chứng minh tính đúng đắn của Giải thuật Peterson:

1. **Loại trừ tương hỗ (Mutual Exclusion):**
   Để cả hai tiến trình $P_0$ và $P_1$ cùng có mặt trong miền găng, điều kiện thoát vòng lặp của cả hai phải cùng đúng tại một thời điểm:
   - $P_0$ thoát khi: `flag[1] == false` HOẶC `turn == 0`.
   - $P_1$ thoát khi: `flag[0] == false` HOẶC `turn == 1`.
   
   Vì cả hai cùng muốn vào, `flag[0] == flag[1] == true`. Do đó, $P_0$ chỉ vào được nếu `turn == 0`, và $P_1$ chỉ vào được nếu `turn == 1`. Tuy nhiên, `turn` là một biến nguyên đơn lẻ trong bộ nhớ, tại một thời điểm nó chỉ có thể nhận giá trị $0$ hoặc $1$, không thể vừa bằng $0$ vừa bằng $1$. Tiến trình nào thực hiện phép gán `turn = ...` sau cùng sẽ thiết lập giá trị và nhường quyền cho tiến trình kia vào trước. Vậy tính loại trừ tương hỗ được đảm bảo.

2. **Tiến triển (Progress):**
   Nếu $P_j$ không muốn vào miền găng (`flag[j] == false`), điều kiện `while (flag[j] && turn == j)` của $P_i$ lập tức sai, $P_i$ vào miền găng ngay mà không bị cản trở. Nếu cả hai cùng muốn vào và cùng gán `turn`, giá trị `turn` cuối cùng sẽ là $0$ hoặc $1$, giúp chính xác một tiến trình thoát khỏi `while` để vào miền găng.

3. **Chờ đợi có giới hạn (Bounded Waiting):**
   Khi $P_j$ rời miền găng, nó gán `flag[j] = false`, giải phóng cho $P_i$. Nếu $P_j$ muốn quay lại miền găng ngay, nó phải thực hiện `turn = i`, trao lại quyền ưu tiên cho $P_i$. Do đó, $P_i$ chỉ phải chờ tối đa 1 lượt vào của $P_j$.

### 3.4 Giải thuật Peterson trên Kiến trúc Phần cứng Hiện đại

*(Nguồn: Slide 47–51)*

> **Đánh giá bản chất kỹ thuật:**
> Về mặt toán học và lý thuyết, giải thuật Peterson **hoàn toàn đúng đắn** dưới giả định mô hình bộ nhớ tuần tự nhất quán (Sequential Consistency). Tuy nhiên, trên các bộ xử lý hiện đại (x86, ARM, RISC-V) và trình biên dịch tối ưu:
> - **Memory Reordering:** Trình biên dịch và CPU Out-of-Order có thể hoán đổi thứ tự thực thi của hai lệnh không phụ thuộc dữ liệu: `flag[i] = true;` và `turn = j;` có thể bị ghi vào Store Buffer theo thứ tự ngược lại hoặc bị trì hoãn hiển thị sang lõi CPU khác.
> - Hậu quả: Hai lõi CPU có thể cùng đọc thấy `flag` của đối phương là `false` trước khi lệnh ghi `true` kịp lan truyền, dẫn đến vi phạm Mutual Exclusion. Do đó, việc triển khai trên phần cứng thực tế bắt buộc phải sử dụng **Memory Barrier**.

---

## 4. Hỗ trợ Phần cứng và Memory Barrier

*(Nguồn: `UIT-SLIDE-CH05-1-2024`, Slide 52–56)*

### 4.1 Rào chắn Bộ nhớ (Memory Barrier)

**Memory Barrier (hoặc Memory Fence)** là chỉ thị phần cứng buộc CPU và trình biên dịch phải hoàn tất mọi thao tác đọc/ghi trước rào chắn trước khi thực thi bất kỳ thao tác đọc/ghi nào sau rào chắn:

```c
// Tiến trình 1 (Core 1)
flag[0] = true;
memory_barrier(); // Đảm bảo flag[0] hiển thị cho toàn hệ thống trước khi gán turn
turn = 1;

// Tiến trình 2 (Core 2)
flag[1] = true;
memory_barrier(); // Đảm bảo flag[1] hiển thị cho toàn hệ thống trước khi gán turn
turn = 0;
```

### 4.2 Các Chỉ thị Nguyên tử Phần cứng (`source_depth: SELF_STUDY`)

*(Nguồn: Slide 56 ghi nhận nội dung Tự học; phần dưới đây chuẩn hóa cơ chế kỹ thuật phục vụ thi cử)*

Phần cứng hiện đại cung cấp các chỉ thị nguyên tử (Atomic Instructions - thực thi trọn vẹn trong một chu kỳ bus/cache, không thể bị ngắt giữa chừng).

#### 1. Chỉ thị `test_and_set`

- Định nghĩa hành vi phần cứng:
  ```c
  boolean test_and_set(boolean *target) {
      boolean rv = *target; // Lưu lại giá trị cũ
      *target = true;       // Gán giá trị mới là true
      return rv;            // Trả về giá trị cũ
  }
  ```
- Giải pháp miền găng với biến khóa `lock` (khởi tạo `lock = false`):
  ```c
  do {
      while (test_and_set(&lock))
          ; /* busy waiting */
      
      /* CRITICAL SECTION */
      
      lock = false;
      
      /* REMAINDER SECTION */
  } while (true);
  ```

#### 2. Chỉ thị `compare_and_swap` (CAS)

- Định nghĩa hành vi phần cứng:
  ```c
  int compare_and_swap(int *value, int expected, int new_value) {
      int temp = *value;
      if (*value == expected)
          *value = new_value;
      return temp;
  }
  ```
- Giải pháp miền găng với `lock = 0`:
  ```c
  do {
      while (compare_and_swap(&lock, 0, 1) != 0)
          ; /* busy waiting */
      
      /* CRITICAL SECTION */
      
      lock = 0;
      
      /* REMAINDER SECTION */
  } while (true);
  ```

#### 3. Biến đơn nguyên (Atomic Variables)

Biến đơn nguyên (như `atomic_int` trong C11 hoặc `atomic_t` trong Linux Kernel) sử dụng trực tiếp các lệnh nguyên tử của CPU để thực hiện các phép toán cơ bản (như `fetch_and_add`) mà không cần khóa mutex. Thao tác đếm trong bài toán Producer-Consumer được giải quyết an toàn bằng:
```c
atomic_int count = 0;
// Producer:
atomic_fetch_add(&count, 1);
// Consumer:
atomic_fetch_sub(&count, 1);
```

---

## 5. Mutex Locks

*(Nguồn: `UIT-SLIDE-CH05-1-2024`, Slide 57–65)*

### 5.1 Khái niệm & Hoạt động

**Mutex (Mutual Exclusion Lock)** là công cụ đồng bộ hóa phần mềm đơn giản nhất do hệ điều hành cung cấp để bảo vệ miền găng.
- Cấu trúc: Một biến boolean `available` thể hiện trạng thái khóa khả dụng (`true`) hay đang bị chiếm giữ (`false`).
- Hai hàm cơ bản:
  ```c
  acquire() {
      while (!available)
          ; /* busy waiting */
      available = false;
  }

  release() {
      available = true;
  }
  ```
- Mẫu sử dụng chuẩn:
  ```c
  acquire(&mutex);
  /* CRITICAL SECTION */
  release(&mutex);
  ```

### 5.2 Spinlock vs Mutex không Busy Waiting

1. **Spinlock (Khóa xoay):**
   - Định nghĩa: Mutex lock mà trong đó tiến trình phải liên tục lặp kiểm tra trong hàm `acquire()`.
   - **Ưu điểm:** Không mất chi phí chuyển ngữ cảnh (Context switch overhead).
   - **Khi nào nên dùng?** Sử dụng trên hệ thống đa xử lý (Multiprocessor) khi thời gian thực thi trong miền găng **cực kỳ ngắn** (ngắn hơn thời gian thực hiện hai lần context switch).

2. **Mutex Lock không Busy Waiting (Blocking / Sleep & Wakeup):**
   - Khi không thể lấy được khóa, tiến trình tự chuyển trạng thái sang `Waiting/Blocked`, đưa PCB vào hàng đợi `wait_queue` của khóa và gọi hàm lập lịch `yield()` / `sleep()`.
   - Khi tiến trình đang giữ khóa gọi `release()`, nó sẽ đánh thức một tiến trình trong `wait_queue` chuyển về trạng thái `Ready`.

> **Lưu ý chuẩn xác kỹ thuật:**
> - Khác với Semaphore, Mutex có khái niệm **quyền sở hữu (Ownership)**: Chỉ luồng đã gọi `acquire()` mới có quyền gọi `release()`.
> - Chuẩn POSIX (`pthread_mutex_unlock`) không đảm bảo các luồng đang chờ sẽ được đánh thức theo thứ tự FIFO nghiêm ngặt.

---

## 6. Semaphore và Hiện thực

*(Nguồn: `UIT-SLIDE-CH07-2-2024`, Slide 4–32)*

### 6.1 Định nghĩa Semaphore của Dijkstra

**Semaphore** $S$ là một biến nguyên (integer variable), ngoài việc khởi tạo, chỉ có thể được truy xuất thông qua hai thao tác nguyên tử chuẩn: `wait(S)` (còn gọi là phép toán $P$) và `signal(S)` (còn gọi là phép toán $V$).

- **Định nghĩa kinh điển theo Dijkstra:**
  ```c
  wait(S) {
      while (S <= 0)
          ; /* busy waiting */
      S--;
  }

  signal(S) {
      S++;
  }
  ```

### 6.2 Phân loại Semaphore

1. **Counting Semaphore (Semaphore tổng quát / đếm):**
   Giá trị của $S$ có thể nhận giá trị nguyên không âm bất kỳ ($S \in [0, N]$). Thường dùng để quản lý việc cấp phát một tập hợp gồm $N$ thực thể tài nguyên giống nhau.
2. **Binary Semaphore (Semaphore nhị phân):**
   Giá trị của $S$ chỉ nhận giá trị $0$ hoặc $1$. Hoạt động tương đương như một Mutex Lock (dùng cho bài toán loại trừ tương hỗ).

### 6.3 Hiện thực Semaphore không Busy Waiting

Để loại bỏ hiện tượng tiêu tốn chu kỳ CPU do lặp vô ích, hệ điều hành hiện thực Semaphore đi kèm một hàng đợi tiến trình:

```c
typedef struct {
    int value;
    struct process *list; // Hàng đợi liên kết chứa các PCB đang chờ
} semaphore;
```

Hàm `wait(S)` và `signal(S)` được hiện thực mức nhân như sau:

```c
void wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        // Hết tài nguyên: thêm tiến trình này vào S->list
        add_to_queue(S->list, current_process);
        block(); // Chuyển tiến trình sang trạng thái Waiting
    }
}

void signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        // Còn tiến trình đang đợi trong hàng đợi: lấy ra và đánh thức
        struct process *P = remove_from_queue(S->list);
        wakeup(P); // Chuyển tiến trình P sang trạng thái Ready
    }
}
```

> **Ý nghĩa của giá trị `S->value` trong mô hình Slide:**
> - Khi `S->value >= 0`: Đại diện cho **số lượng thực thể tài nguyên đang khả dụng**.
> - Khi `S->value < 0`: Độ lớn $|S\text{->value}|$ đại diện cho **số lượng tiến trình đang bị khóa và chờ đợi trong hàng đợi `S->list`**.
> 
> *Ghi chú chuẩn hóa POSIX:* Với giao thức chuẩn POSIX (`sem_wait`), giá trị quan sát được qua `sem_getvalue()` không bao giờ âm; tiến trình sẽ block nếu giá trị bằng $0$.

### 6.4 Các Dạng Ứng dụng Cơ bản của Semaphore

#### 1. Đảm bảo Loại trừ Tương hỗ (Mutual Exclusion)
Khởi tạo `semaphore mutex = 1;`:
```c
wait(&mutex);
/* CRITICAL SECTION */
signal(&mutex);
```

#### 2. Đồng bộ Thứ tự Thực thi (Execution Ordering)
Muốn câu lệnh $S_1$ của tiến trình $P_1$ **luôn luôn thực thi trước** câu lệnh $S_2$ của tiến trình $P_2$:
- Khởi tạo `semaphore synch = 0;`
- Mã nguồn $P_1$:
  ```c
  S1;
  signal(&synch); // Báo hiệu S1 đã xong
  ```
- Mã nguồn $P_2$:
  ```c
  wait(&synch);   // Chờ S1 hoàn thành mới được chạy tiếp
  S2;
  ```

#### 3. Quản lý Tài nguyên Đa thực thể
Khởi tạo `semaphore resources = N;` (với $N$ là số lượng tài nguyên khả dụng).

---

## 7. Monitors và Condition Variables

*(Nguồn: `UIT-SLIDE-CH07-2-2024`, Slide 33–40)*

### 7.1 Cấu trúc Trừu tượng của Monitor

Mặc dù Semaphore rất mạnh mẽ, việc sử dụng sai thứ tự các lệnh `wait()` và `signal()` có thể dễ dàng dẫn đến bế tắc hoặc vi phạm miền găng. **Monitor** là một cấu trúc đồng bộ hóa bậc cao được tích hợp ở mức ngôn ngữ lập trình (như Java `synchronized`, C# `Monitor`):

```
┌─────────────────────────────────────────────────────────┐
│                      MONITOR                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │   Shared Variables (Dữ liệu dùng chung)           │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │   Operations / Procedures (Hàm thao tác)          │  │
│  │   - procedure P1(...) { ... }                     │  │
│  │   - procedure P2(...) { ... }                     │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │   Initialization Code (Mã khởi tạo)               │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

> **Nguyên lý cốt lõi của Monitor:**
> Tại một thời điểm, **chỉ duy nhất một tiến trình được phép hoạt động bên trong monitor**. Tính loại trừ tương hỗ được tự động bảo đảm bởi trình biên dịch mà lập trình viên không cần gọi các lệnh lock/unlock thủ công.

### 7.2 Biến Điều kiện (Condition Variables)

Để cho phép tiến trình tạm dừng và chờ đợi các điều kiện logic bên trong monitor, cơ chế **Biến điều kiện (Condition Variable)** được sử dụng:
- Khai báo: `condition x, y;`
- Hai thao tác cơ bản:
  1. `x.wait()`: Tiến trình gọi lệnh này sẽ bị tạm dừng và đưa vào hàng đợi của biến điều kiện $x$.
     > **Cơ chế bắt buộc:** Khi gọi `x.wait()`, tiến trình **bắt buộc phải tự động giải phóng khóa monitor** để tiến trình khác có thể vào monitor thay đổi điều kiện. Sau khi được đánh thức, tiến trình **phải tái chiếm lại khóa monitor** trước khi tiếp tục thực thi lệnh tiếp theo.
  2. `x.signal()`: Đánh thức chính xác một tiến trình đang bị khóa trong hàng đợi của $x$. Nếu không có tiến trình nào đang chờ trên $x$, lệnh `signal()` không có tác dụng gì (khác hoàn toàn với Semaphore vốn sẽ tăng biến đếm).

---

## 8. Liveness và Deadlock

*(Nguồn: `UIT-SLIDE-CH07-2-2024`, Slide 41–43)*

### 8.1 Khái niệm Liveness

**Liveness (Tính sống động)** là tập hợp các đặc điểm/thuộc tính mà một hệ thống đồng bộ phải thỏa mãn để đảm bảo các tiến trình thực sự tiếp tục tiến triển trong quá trình thực thi, không bị rơi vào trạng thái "bị kẹt" vĩnh viễn.

### 8.2 Các Dạng Thất bại Liveness Điển hình

1. **Deadlock (Bế tắc):**
   Hiện tượng hai hay nhiều tiến trình chờ đợi vô hạn một sự kiện mà sự kiện đó chỉ có thể được tạo ra bởi chính một trong các tiến trình đang chờ trong nhóm.
   - **Ví dụ kinh điển với Semaphore nhị phân:**
     Khởi tạo `semaphore S = 1, Q = 1;`
     
     $$\begin{array}{c|c}
     \textbf{Tiến trình } P_0 & \textbf{Tiến trình } P_1 \\ \hline
     \text{wait}(S); & \text{wait}(Q); \\
     \text{wait}(Q); & \text{wait}(S); \\
     \dots & \dots \\
     \text{signal}(S); & \text{signal}(Q); \\
     \text{signal}(Q); & \text{signal}(S);
     \end{array}$$
     
     Nếu $P_0$ thực thi $\text{wait}(S)$ thành công và $P_1$ thực thi $\text{wait}(Q)$ thành công, sau đó $P_0$ gọi $\text{wait}(Q)$ (bị block do $Q=0$) và $P_1$ gọi $\text{wait}(S)$ (bị block do $S=0$). Cả hai tiến trình đều giữ một khóa và chờ khóa của đối phương $\rightarrow$ **Deadlock**.

2. **Starvation (Đói tài nguyên / Chờ đợi vô hạn):**
   Tình trạng một tiến trình không bao giờ được cấp tài nguyên hoặc không bao giờ được thoát ra khỏi hàng đợi của Semaphore do liên tục bị các tiến trình khác vượt mặt (ví dụ hàng đợi ưu tiên hoặc hàng đợi LIFO).

3. **Priority Inversion (Nghịch đảo Độ ưu tiên):**
   Hiện tượng xảy ra trên hệ thống lập lịch theo độ ưu tiên:
   - Tiến trình ưu tiên thấp ($L$) đang nắm giữ một khóa tài nguyên mà tiến trình ưu tiên cao ($H$) đang cần.
   - Tiến trình $H$ bị block để chờ $L$ nhả khóa.
   - Một tiến trình ưu tiên trung bình ($M$) xuất hiện (không cần khóa). Vì $M$ có độ ưu tiên cao hơn $L$, $M$ chiếm quyền CPU và chạy liên tục, ngăn không cho $L$ chạy để nhả khóa.
   - Hậu quả: Tiến trình $H$ (ưu tiên cao nhất) bị trì hoãn vô thời hạn bởi tiến trình $M$ (ưu tiên trung bình) $\rightarrow$ Đảo ngược trật tự ưu tiên của hệ thống.

4. **Priority Inheritance Protocol (Giao thức Thừa kế Độ ưu tiên):**
   - **Giải pháp:** Khi tiến trình $H$ phải chờ tài nguyên do tiến trình $L$ nắm giữ, tiến trình $L$ sẽ **tạm thời được thừa kế mức độ ưu tiên cao bằng $H$**.
   - Nhờ đó, các tiến trình trung bình $M$ không thể chiếm quyền CPU của $L$. Tiến trình $L$ hoàn thành miền găng nhanh chóng, nhả khóa và trả lại độ ưu tiên ban đầu, giúp $H$ lấy khóa và thực thi ngay lập tức.

---

## 9. Bài toán Bounded-Buffer

*(Nguồn: `UIT-SLIDE-CH07-2-2024`, Slide 44–53)*

### 9.1 Mô tả Bài toán & Thiết kế Đồng bộ

Một bộ đệm chung có $N$ vị trí lưu trữ. Producer sản xuất dữ liệu ghi vào đệm; Consumer lấy dữ liệu ra khỏi đệm.
- **Yêu cầu an toàn:**
  - Producer không được ghi khi đệm đầy ($count = N$).
  - Consumer không được đọc khi đệm rỗng ($count = 0$).
  - Thao tác thêm/bớt phần tử vào bộ đệm phải loại trừ tương hỗ.

### 9.2 Khởi tạo Semaphore

```c
#define BUFFER_SIZE 10

semaphore mutex = 1; // Bảo vệ loại trừ tương hỗ khi thao tác trên buffer
semaphore empty = BUFFER_SIZE; // Đếm số vị trí trống khả dụng (khởi tạo = N)
semaphore full = 0;  // Đếm số vị trí có dữ liệu (khởi tạo = 0)
```

### 9.3 Mã nguồn Giải pháp Chuẩn

```c
// TIẾN TRÌNH PRODUCER
do {
    // 1. Sản xuất item trong next_produced
    
    wait(&empty); // Chờ có ít nhất 1 ô trống (empty > 0)
    wait(&mutex); // Khóa miền găng để ghi vào buffer
    
    // Thêm next_produced vào buffer
    buffer[in] = next_produced;
    in = (in + 1) % BUFFER_SIZE;
    
    signal(&mutex); // Mở khóa miền găng
    signal(&full);  // Tăng số lượng phần tử có sẵn cho Consumer
} while (true);

// TIẾN TRÌNH CONSUMER
do {
    wait(&full);  // Chờ có ít nhất 1 phần tử (full > 0)
    wait(&mutex); // Khóa miền găng để đọc từ buffer
    
    // Lấy item từ buffer vào next_consumed
    next_consumed = buffer[out];
    out = (out + 1) % BUFFER_SIZE;
    
    signal(&mutex); // Mở khóa miền găng
    signal(&empty); // Báo hiệu đã giải phóng 1 ô trống cho Producer
    
    // 2. Tiêu thụ item trong next_consumed
} while (true);
```

> **Bẫy đề thi quan trọng:**
> Nếu Producer đảo thứ tự gọi thành:
> ```c
> wait(&mutex);
> wait(&empty);
> ```
> Khi bộ đệm đầy (`empty = 0`), Producer lấy `mutex` thành công rồi bị block ở `wait(&empty)`. Consumer muốn vào lấy item để giải phóng ô trống nhưng bị chặn ở `wait(&mutex)` $\rightarrow$ **DEADLOCK**. Quy tắc bắt buộc: **Phải chờ điều kiện tài nguyên (`empty`/`full`) trước khi lấy khóa miền găng (`mutex`)**.

---

## 10. Bài toán Readers – Writers

*(Nguồn: `UIT-SLIDE-CH07-2-2024`, Slide 54–60)*

### 10.1 Mô tả Bài toán & Yêu cầu

Một cơ sở dữ liệu/tệp tin được chia sẻ giữa nhiều tiến trình:
- **Readers:** Chỉ đọc dữ liệu, không sửa đổi. Nhiều Reader được phép đọc đồng thời.
- **Writers:** Ghi và cập nhật dữ liệu. Đòi hỏi loại trừ tương hỗ tuyệt đối (khi một Writer đang ghi, không Reader hay Writer nào khác được truy xuất).

### 10.2 Giải pháp First Readers – Writers (Ưu tiên Reader)

- **Biến chia sẻ & Semaphore:**
  ```c
  semaphore rw_mutex = 1; // Khóa loại trừ tương hỗ cho Writer và Reader đầu/cuối
  semaphore mutex = 1;    // Bảo vệ biến đếm read_count
  int read_count = 0;     // Đếm số lượng Reader đang đọc dữ liệu
  ```
- **Mã nguồn Writer:**
  ```c
  do {
      wait(&rw_mutex);
      /* WRITING SECTION (Ghi dữ liệu) */
      signal(&rw_mutex);
  } while (true);
  ```
- **Mã nguồn Reader:**
  ```c
  do {
      wait(&mutex);
      read_count++;
      if (read_count == 1)
          wait(&rw_mutex); // Reader đầu tiên vào: chặn toàn bộ Writer
      signal(&mutex);
      
      /* READING SECTION (Đọc dữ liệu) */
      
      wait(&mutex);
      read_count--;
      if (read_count == 0)
          signal(&rw_mutex); // Reader cuối cùng ra: nhả khóa cho Writer
      signal(&mutex);
  } while (true);
  ```

> **Đánh giá giải pháp:** Giải pháp trên ưu tiên Reader. Nếu các Reader liên tục đến gối đầu nhau, `read_count` không bao giờ về $0$, dẫn đến các tiến trình Writer bị **đói tài nguyên (Starvation)** vĩnh viễn.

---

## 11. Bài toán Dining – Philosophers

*(Nguồn: `UIT-SLIDE-CH07-2-2024`, Slide 61–70)*

### 11.1 Phát biểu Bài toán

Năm triết gia ngồi quanh một bàn ăn tròn, dành trọn đời luân phiên giữa hai trạng thái: **Suy nghĩ (Thinking)** và **Ăn (Eating)**. Trên bàn có 5 chiếc đĩa và 5 chiếc đũa (`chopstick[0..4]`). Để ăn, mỗi triết gia $i$ cần phải cầm được cả 2 chiếc đũa nằm ngay bên trái và bên phải của mình: chiếc đũa $i$ và chiếc đũa $(i + 1) \% 5$.

```
           Triết gia 0
         [Đũa 0]   [Đũa 1]
    Triết gia 4        Triết gia 1
    [Đũa 4]               [Đũa 2]
         Triết gia 3   Triết gia 2
                [Đũa 3]
```

### 11.2 Giải pháp Naive và Nguy cơ Bế tắc

Khởi tạo mảng Semaphore: `semaphore chopstick[5] = {1, 1, 1, 1, 1};`
```c
// Mã nguồn Triết gia thứ i (0 <= i <= 4):
do {
    wait(&chopstick[i]);                 // Nhặt đũa bên trái
    wait(&chopstick[(i + 1) % 5]);       // Nhặt đũa bên phải
    
    /* EATING (Ăn) */
    
    signal(&chopstick[i]);               // Đặt đũa bên trái xuống
    signal(&chopstick[(i + 1) % 5]);     // Đặt đũa bên phải xuống
    
    /* THINKING (Suy nghĩ) */
} while (true);
```

> **Kịch bản Deadlock:**
> Nếu đồng thời cả 5 triết gia cùng cảm thấy đói và mỗi người đều thực hiện thành công lệnh `wait(&chopstick[i])` để cầm chiếc đũa bên trái của mình:
> - Mỗi chiếc đũa đều có giá trị $0$.
> - Sau đó cả 5 triết gia cùng gọi lệnh `wait(&chopstick[(i+1)%5])` để lấy đũa bên phải $\rightarrow$ Tất cả đều bị block vĩnh viễn $\rightarrow$ **DEADLOCK TOÀN PHẦN**.

### 11.3 Các Giải pháp Tránh Deadlock

1. **Giới hạn số người ăn:** Chỉ cho phép tối đa 4 triết gia cùng ngồi vào bàn ăn tại một thời điểm (dùng `semaphore dining_limit = 4;`).
2. **Nhặt đũa nguyên tử (Atomic pickup):** Chỉ cho phép một triết gia nhặt đũa khi **cả hai chiếc đũa** đều đang khả dụng (thực hiện kiểm tra trong miền găng).
3. **Giải pháp bất đối xứng (Asymmetric solution):**
   - Triết gia có chỉ số lẻ ($1, 3$) nhặt đũa trái trước, đũa phải sau.
   - Triết gia có chỉ số chẵn ($0, 2, 4$) nhặt đũa phải trước, đũa trái sau.
   - Phá vỡ điều kiện chờ vòng tròn (Circular Wait), triệt tiêu hoàn toàn khả năng xảy ra deadlock.
4. **Giải pháp sử dụng Monitor:**
   Quản lý 3 trạng thái của mỗi triết gia `enum {THINKING, HUNGRY, EATING} state[5];` và sử dụng mảng biến điều kiện `condition self[5];` để đồng bộ.

---

## Tóm tắt và Hướng dẫn Ôn tập

### Bảng Ma trận So sánh Công cụ Đồng bộ Hóa

| Tiêu chí | Mutex Lock (Spinlock) | Mutex Lock (Blocking) | Semaphore | Monitor |
| :--- | :--- | :--- | :--- | :--- |
| **Bản chất cơ chế** | Vòng lặp kiểm tra bận liên tục | Đưa tiến trình vào hàng đợi ngủ | Biến nguyên + hàng đợi chờ | Cấu trúc dữ liệu trừu tượng ADT |
| **Mức độ hỗ trợ** | Phần cứng / Kernel | Hệ điều hành | Hệ điều hành | Ngôn ngữ lập trình / Trình biên dịch |
| **Quyền sở hữu (Ownership)** | Có (chỉ luồng lock mới unlock) | Có | Không (luồng khác có thể signal) | Tự động quản lý theo hàm |
| **Tiêu tốn CPU khi chờ** | Rất cao (100% Core) | Bằng 0 (nhường CPU) | Bằng 0 | Bằng 0 |
| **Trường hợp áp dụng tối ưu** | Miền găng cực ngắn trên đa CPU | Miền găng dài, I/O bound | Quản lý đa tài nguyên / Thứ tự | Lập trình ứng dụng phức tạp, hướng đối tượng |

---
*Cẩm nang IT007 Hệ điều hành — Biên soạn phục vụ học tập và nghiên cứu chuẩn mực.*

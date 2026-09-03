---
title: "Chương 6: Bế tắc (Deadlock)"
description: "Khảo sát toàn diện về vấn đề bế tắc (deadlock): 4 điều kiện Coffman, đồ thị cấp phát tài nguyên (RAG), các chiến lược ngăn ngừa, giải thuật tránh bế tắc Banker, phát hiện và phục hồi bế tắc."
chapter: 6
order: 6
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH06-2024"
  - "UIT-QBANK-CH06-2024"
---

# Chương 6: Bế tắc (Deadlock)

> **Mục tiêu học tập (CLO Alignment):**
> 1. Nắm vững bản chất của hiện tượng bế tắc (Deadlock) trong hệ thống đa chương và đa nhiệm.
> 2. Phân tích 4 điều kiện cần Coffman và đánh giá khả năng vi phạm từng điều kiện.
> 3. Xây dựng và phân tích Đồ thị cấp phát tài nguyên (Resource-Allocation Graph – RAG), phân biệt sự khác nhau giữa hệ thống đơn thực thể (Single-instance) và đa thực thể (Multiple-instances).
> 4. Hiểu rõ sự khác biệt bản chất giữa Ngăn chặn bế tắc (Prevention), Tránh bế tắc (Avoidance), Phát hiện bế tắc (Detection) và Bỏ qua (Ostrich Algorithm).
> 5. Thực thi thành thạo Giải thuật Banker (Banker's Algorithm) bao gồm Giải thuật An toàn (Safety Algorithm) và Giải thuật Yêu cầu Tài nguyên (Resource-Request Algorithm).
> 6. Nắm vững cơ chế Phát hiện bế tắc (Detection) và các giải pháp Phục hồi hệ thống (Recovery).

---

## 6.1. Vấn Đề Bế Tắc & Định Nghĩa

### 6.1.1. Khởi nguyên bài toán & Ví dụ Semaphore xen kẽ
*(Căn cứ: Slide pp. 4–7)*

Trong một hệ thống tính toán đồng thời, nhiều tiến trình cùng cạnh tranh một tập hợp hữu hạn các tài nguyên hệ thống (CPU, bộ nhớ, thiết bị ngoại vi, tệp tin, biến khóa Semaphore, Mutex...). Khi một tiến trình yêu cầu tài nguyên mà tài nguyên đó chưa khả dụng, tiến trình buộc phải chuyển sang trạng thái chờ đợi (`WAITING` / `BLOCKED`). 

Hiện tượng bế tắc xảy ra khi các tiến trình trong tập hợp đang chờ đợi những sự kiện mà chỉ có thể được kích hoạt bởi chính các tiến trình khác cũng đang chờ đợi trong cùng tập hợp đó.

#### Ví dụ minh họa kinh điển: Xen kẽ hai Semaphore
Xét hai tiến trình $P_0$ và $P_1$ cùng chia sẻ hai biến Semaphore nhị phân $S$ và $Q$, đều được khởi tạo giá trị ban đầu là `1`:

```c
/* Khởi tạo hệ thống */
semaphore S = 1;
semaphore Q = 1;

/* Tiến trình P0 */
void Process_P0() {
    wait(S);        // P0 chiếm giữ thành công S (S giảm từ 1 xuống 0)
    wait(Q);        // P0 yêu cầu Q và bị chặn nếu Q = 0
    /* Vùng tranh chấp (Critical Section) */
    signal(S);
    signal(Q);
}

/* Tiến trình P1 */
void Process_P1() {
    wait(Q);        // P1 chiếm giữ thành công Q (Q giảm từ 1 xuống 0)
    wait(S);        // P1 yêu cầu S và bị chặn nếu S = 0
    /* Vùng tranh chấp (Critical Section) */
    signal(Q);
    signal(S);
}
```

**Kịch bản dẫn đến Deadlock:**
1. Bộ điều phối CPU cho $P_0$ thực thi lệnh `wait(S)`. $S$ trở thành `0`. $P_0$ nắm giữ $S$.
2. Xảy ra chuyển ngữ cảnh (Context Switch), CPU chuyển sang thực thi $P_1$.
3. $P_1$ thực thi lệnh `wait(Q)`. $Q$ trở thành `0`. $P_1$ nắm giữ $Q$.
4. $P_1$ tiếp tục gọi `wait(S)`. Vì $S = 0$, $P_1$ bị chặn và đưa vào hàng đợi chờ của $S$.
5. CPU chuyển lại cho $P_0$. $P_0$ gọi `wait(Q)`. Vì $Q = 0$, $P_0$ bị chặn và đưa vào hàng đợi chờ của $Q$.

**Hậu quả:** Cả $P_0$ và $P_1$ đều rơi vào trạng thái ngủ đông vô hạn định. $P_0$ chờ $P_1$ nhả $Q$, trong khi $P_1$ lại chờ $P_0$ nhả $S$. Không tiến trình nào có thể tự giải phóng tài nguyên mình đang giữ vì chúng đều bị treo ở lệnh `wait()`. Đây chính là hiện tượng **Bế tắc (Deadlock)**.

---

### 6.1.2. Định nghĩa Deadlock & Trì hoãn vô hạn định
*(Căn cứ: Slide pp. 8–9)*

> **Định nghĩa học thuật chính thức (Formal Definition):**
> Một tập hợp các tiến trình rơi vào trạng thái **Bế tắc (Deadlock)** khi và chỉ khi mọi tiến trình trong tập hợp đó đều đang chờ đợi một sự kiện (event) mà sự kiện này chỉ có thể được tạo ra bởi một tiến trình khác cũng nằm trong chính tập hợp đó.

Sự kiện được chờ đợi ở đây thường là việc giải phóng tài nguyên (Resource Release) thông qua thao tác hệ thống như `signal()`, `unlock()`, hoặc giải phóng bộ nhớ/thiết bị.

#### Phân biệt Deadlock và Đói tài nguyên (Starvation)
Cần phân biệt rõ ràng hai khái niệm thường bị nhầm lẫn trong các đề thi:
- **Deadlock (Bế tắc):** Là trạng thái bế tắc cấu trúc. Các tiến trình bị khóa cứng lẫn nhau. Thời gian chờ đợi là **vô hạn** và hệ thống không thể tự thoát ra nếu không có sự can thiệp từ bên ngoài (hệ điều hành hoặc quản trị viên).
- **Starvation (Đói tài nguyên / Trì hoãn vô hạn định - Indefinite Postponement):** Tiến trình không bị khóa cấu trúc, tài nguyên vẫn liên tục được cấp phát và giải phóng, nhưng do thuật toán điều phối bất công (ví dụ: Priority Scheduling không có Aging, SJF với luồng tiến trình ngắn đến liên tục), một tiến trình có mức ưu tiên thấp có thể phải chờ đợi rất lâu hoặc không xác định được thời điểm được phục vụ.

---

### 6.1.3. Bốn điều kiện cần Coffman (The Four Coffman Conditions)
*(Căn cứ: Slide pp. 10–12; Căn cứ lý thuyết quốc tế: Coffman et al., 1971)*

Năm 1971, Edward G. Coffman Jr. cùng các cộng sự đã chỉ ra rằng, một trạng thái bế tắc xảy ra trong hệ thống tính toán **chỉ khi đồng thời thỏa mãn cả 4 điều kiện sau đây**:

| STT | Tên điều kiện | Thuật ngữ tiếng Anh | Bản chất cơ chế hoạt động |
|:---:|:---|:---|:---|
| **1** | **Loại trừ lẫn nhau** | Mutual Exclusion | Tại một thời điểm, tài nguyên không thể chia sẻ (non-sharable). Chỉ duy nhất một tiến trình được phép sử dụng một thực thể tài nguyên. Nếu tiến trình khác yêu cầu, tiến trình đó phải chờ. |
| **2** | **Giữ và chờ** | Hold and Wait | Một tiến trình đang nắm giữ ít nhất một tài nguyên lại đang chờ cấp phát thêm tài nguyên mới mà tài nguyên mới này đang bị tiến trình khác nắm giữ. |
| **3** | **Không lưu quyền** | No Preemption | Tài nguyên không thể bị hệ thống tự ý thu hồi cưỡng bức từ tiến trình đang giữ nó. Tài nguyên chỉ được giải phóng một cách tự nguyện bởi chính tiến trình đó sau khi hoàn thành nhiệm vụ. |
| **4** | **Chờ đợi vòng tròn** | Circular Wait | Tồn tại một chuỗi vòng khép kín các tiến trình $\{P_0, P_1, \dots, P_n\}$ sao cho $P_0$ chờ tài nguyên đang bị giữ bởi $P_1$, $P_1$ chờ $P_2$, ..., $P_{n-1}$ chờ $P_n$, và $P_n$ chờ tài nguyên đang bị giữ bởi $P_0$. |

> [!IMPORTANT]
> **Điểm mấu chốt học thuật (Crucial Theoretical Invariant):**
> 4 điều kiện Coffman là **ĐIỀU KIỆN CẦN (Necessary Conditions)** để xảy ra Deadlock, chứ **KHÔNG PHẢI ĐIỀU KIỆN ĐỦ (Not always Sufficient)** cho mọi mô hình tài nguyên:
> - Nếu một trong 4 điều kiện bị triệt tiêu $\implies$ Deadlock **chắc chắn không thể xảy ra**.
> - Nếu cả 4 điều kiện cùng tồn tại $\implies$ Deadlock **có thể xảy ra**, nhưng chưa thể khẳng định 100% nếu tài nguyên có nhiều thực thể (multiple instances).

---

## 6.2. Mô Hình Hóa Hệ Thống & Đồ Thị Cấp Phát Tài Nguyên (RAG)

### 6.2.1. Mô hình tài nguyên hệ thống
*(Căn cứ: Slide pp. 13–14)*

Hệ thống tính toán gồm:
- Một tập hợp $n$ tiến trình: $P = \{P_1, P_2, \dots, P_n\}$.
- Một tập hợp $m$ loại tài nguyên: $R = \{R_1, R_2, \dots, R_m\}$.
- Mỗi loại tài nguyên $R_j$ sở hữu $W_j$ thực thể (instances) giống hệt nhau ($W_j \ge 1$).

Một tiến trình khi sử dụng tài nguyên bắt buộc phải trải qua chu trình tuần tự gồm 3 bước:
1. **Yêu cầu (Request):** Tiến trình gửi yêu cầu cấp phát. Nếu tài nguyên chưa sẵn sàng, tiến trình bị chặn chuyển sang trạng thái chờ.
2. **Sử dụng (Use):** Tiến trình nắm giữ và vận hành tài nguyên (thực thi trên CPU, in ấn, đọc/ghi tệp...).
3. **Giải phóng (Release):** Tiến trình kết thúc sử dụng và hoàn trả tài nguyên lại cho hệ điều hành.

---

### 6.2.2. Định nghĩa Đồ thị cấp phát tài nguyên (RAG)
*(Căn cứ: Slide pp. 15–17)*

Đồ thị cấp phát tài nguyên (Resource-Allocation Graph – RAG) là một đồ thị có hướng $G = (V, E)$ được định nghĩa như sau:

#### 1. Tập hợp các đỉnh $V = P \cup R$:
- **Tập đỉnh tiến trình $P$:** Mỗi tiến trình $P_i$ được biểu diễn bằng một hình tròn chứa nhãn $P_i$.
- **Tập đỉnh tài nguyên $R$:** Mỗi loại tài nguyên $R_j$ được biểu diễn bằng một hình chữ nhật (hoặc hình vuông). Bên trong hình chữ nhật chứa các dấu chấm tròn nhỏ (dots), mỗi chấm đại diện cho một thực thể (instance) khả dụng của tài nguyên đó.

#### 2. Tập hợp các cạnh có hướng $E$:
- **Cạnh yêu cầu (Request Edge):** Cạnh có hướng đi từ tiến trình đến tài nguyên:
  $$P_i \to R_j$$
  Ý nghĩa: Tiến trình $P_i$ đang yêu cầu 1 thực thể của loại tài nguyên $R_j$ và đang chờ được phục vụ (mũi tên hướng vào khung viền chữ nhật của $R_j$).
- **Cạnh cấp phát (Assignment Edge):** Cạnh có hướng đi từ tài nguyên đến tiến trình:
  $$R_j \to P_i$$
  Ý nghĩa: Một thực thể cụ thể bên trong tài nguyên $R_j$ đã được cấp phát và hiện đang thuộc quyền sở hữu của $P_i$ (mũi tên bắt đầu từ dấu chấm thực thể bên trong $R_j$ hướng tới vòng tròn $P_i$).

---

### 6.2.3. Phân tích các đồ thị mẫu & Định lý Chu trình trong RAG
*(Căn cứ: Slide pp. 18–24)*

#### Trường hợp 1: Đồ thị RAG có Deadlock
Xét hệ thống gồm 3 tiến trình $\{P_1, P_2, P_3\}$ và 4 tài nguyên $\{R_1(1), R_2(2), R_3(1), R_4(3)\}$:
- $P_1$ nắm giữ 1 thực thể $R_2$, yêu cầu 1 thực thể $R_1$.
- $P_2$ nắm giữ 1 thực thể $R_2$, 1 thực thể $R_1$, yêu cầu 1 thực thể $R_3$.
- $P_3$ nắm giữ 1 thực thể $R_3$, yêu cầu 1 thực thể $R_2$.

```
    [ R1 (1) ] <------ P2
        ^              |  \
        |              |   \
        P1             v    v
        ^          [ R3 (1) ]
        |              |
    [ R2 (2) ] <------- P3
```

Trong đồ thị này, xuất hiện hai chu trình khép kín:
1. $\text{Cycle 1}: P_1 \to R_1 \to P_2 \to R_3 \to P_3 \to R_2 \to P_1$
2. $\text{Cycle 2}: P_2 \to R_3 \to P_3 \to R_2 \to P_2$

Vì các tài nguyên $R_1, R_3$ chỉ có 1 thực thể, và cả 2 thực thể của $R_2$ đều bị kẹt giữ trong các chu trình chờ, không tiến trình nào có thể nhận đủ tài nguyên để hoàn thành. Hệ thống rơi vào **Deadlock**.

#### Trường hợp 2: Đồ thị RAG có chu trình nhưng KHÔNG BỊ DEADLOCK
Xét hệ thống gồm 4 tiến trình $\{P_1, P_2, P_3, P_4\}$ và 2 tài nguyên $\{R_1(2), R_2(2)\}$:
- $P_1$ yêu cầu 1 thực thể $R_1$.
- $P_3$ nắm giữ 1 thực thể $R_1$, yêu cầu 1 thực thể $R_2$.
- $P_2$ nắm giữ 1 thực thể $R_1$, không yêu cầu gì thêm.
- $P_4$ nắm giữ 1 thực thể $R_2$, không yêu cầu gì thêm.

```
         P2 (giữ R1)
             ^
             |
    P1 ---> [ R1 (2) ] <--- P3
    ^                        |
    |                        v
    +------------------- [ R2 (2) ] <--- P4 (giữ R2)
```

**Phân tích:**
- Đồ thị xuất hiện chu trình: $P_1 \to R_1 \to P_3 \to R_2 \to P_1$.
- Tuy nhiên, $P_2$ và $P_4$ không bị chặn bởi bất kỳ tài nguyên nào.
- Khi $P_4$ kết thúc, nó giải phóng thực thể $R_2$. Thực thể này được cấp ngay cho $P_3$, giúp $P_3$ hoàn thành nhiệm vụ và giải phóng toàn bộ tài nguyên (trong đó có 1 thực thể $R_1$).
- $R_1$ được cấp tiếp cho $P_1$. Chu trình bị phá vỡ. **Hệ thống hoàn toàn KHÔNG bị Deadlock**.

#### Định lý nền tảng về mối liên hệ RAG và Deadlock (Slide p. 23)
Từ hai trường hợp trên, ta đúc kết thành định lý cốt lõi:

> [!IMPORTANT]
> **Định lý Mối liên hệ Chu trình RAG & Deadlock:**
> 1. **Nếu đồ thị RAG KHÔNG chứa chu trình (No cycle):** Hệ thống **chắc chắn KHÔNG có Deadlock**.
> 2. **Nếu đồ thị RAG CÓ chứa chu trình (Cycle exists):**
>    - **Trường hợp mỗi loại tài nguyên chỉ có DUY NHẤT 1 thực thể ($W_j = 1, \forall j$):** Chu trình là **điều kiện cần và đủ** $\implies$ **Hệ thống CHẮC CHẮN bị Deadlock**.
>    - **Trường hợp có loại tài nguyên chứa NHIỀU thực thể ($W_j > 1$):** Chu trình chỉ là **điều kiện cần** $\implies$ Hệ thống **CÓ THỂ bị Deadlock hoặc KHÔNG**. Phải phân tích sâu chuỗi tiến trình để đưa ra kết luận.

---

## 6.3. Bốn Chiến Lược Xử Lý Bế Tắc (Handling Deadlocks)
*(Căn cứ: Slide pp. 25–26)*

Về mặt lý thuyết và thực tiễn thiết kế hệ điều hành, có 4 phương pháp chính để đối phó với bế tắc:

```
                          CÁC PHƯƠNG PHÁP XỬ LÝ DEADLOCK
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
1. DEADLOCK PREVENTION         2. DEADLOCK AVOIDANCE          3. DETECTION & RECOVERY
(Ngăn ngừa tĩnh)               (Tránh bế tắc động)            (Phát hiện & Phục hồi)
Triệt tiêu ít nhất 1 trong     Duy trì hệ thống luôn          Để deadlock xảy ra,
4 điều kiện Coffman.           nằm trong Safe State           định kỳ quét tìm và
                               (Giải thuật Banker).           thu hồi / hủy tiến trình.
```

> [!NOTE]
> **Ghi chú kỹ thuật Tier-B (Chiến lược thứ tư — Bỏ qua bế tắc):**
> Bên cạnh 3 chiến lược chủ động được nêu trong giáo trình chính quy, tài liệu chuẩn học thuật (Silberschatz et al., Tanenbaum) ghi nhận chiến lược thứ tư là **Bỏ qua bế tắc (The Ostrich Algorithm)**: xem như vấn đề không bao giờ phát sinh. Trong thực tế kỹ thuật, nhiều hệ điều hành đa nhiệm thông dụng lựa chọn không chạy các giải thuật tránh hay phát hiện bế tắc tốn kém trong không gian nhân (kernel) đối với tài nguyên dùng chung nhằm tối ưu hóa thông lượng và độ trễ, thay vào đó dựa vào sự can thiệp từ quản trị viên hoặc tiến trình giám sát khi xảy ra sự cố.

---

## 6.4. Ngăn Chặn Bế Tắc (Deadlock Prevention)
*(Căn cứ: Slide pp. 27–31)*

Ngăn chặn bế tắc là phương pháp thiết kế cấu trúc hệ thống nhằm bảo đảm rằng **ít nhất một trong bốn điều kiện Coffman không bao giờ có thể xảy ra đồng thời**.

### 1. Phá vỡ điều kiện "Loại trừ lẫn nhau" (Mutual Exclusion)
- **Cơ chế:** Thiết kế tài nguyên sao cho có thể chia sẻ được đồng thời (Sharable resources).
- **Thực tế:** Các tài nguyên chỉ đọc (Read-only files, shared memory segments) có thể áp dụng.
- **Hạn chế:** Nhiều tài nguyên về bản chất vật lý bắt buộc phải là độc quyền (máy in, đầu ghi từ, các vùng nhớ cập nhật dữ liệu). Do đó, **không thể triệt tiêu hoàn toàn** điều kiện này trong thực tế.

### 2. Phá vỡ điều kiện "Giữ và chờ" (Hold and Wait)
Hệ điều hành có thể áp dụng một trong hai giao thức sau:
- **Giao thức 1 (Cấp phát toàn bộ trước):** Một tiến trình phải yêu cầu và được cấp phát toàn bộ tất cả tài nguyên nó cần trước khi bắt đầu thực thi lệnh đầu tiên.
- **Giao thức 2 (Giải phóng trước khi yêu cầu mới):** Tiến trình chỉ được phép yêu cầu thêm tài nguyên mới khi nó hiện tại không nắm giữ bất kỳ tài nguyên nào (phải giải phóng hết tài nguyên đang giữ trước khi gửi yêu cầu mới).
- **Hạn chế nghiêm trọng:**
  - Hiệu suất sử dụng tài nguyên (Resource Utilization) cực kỳ thấp: Một tài nguyên chỉ dùng trong 5 giây cuối của tiến trình chạy 1 giờ nhưng vẫn phải bị giữ từ đầu đến cuối.
  - Nguy cơ đói tài nguyên cao (Starvation): Tiến trình cần nhiều tài nguyên phổ biến sẽ phải chờ đợi vô tận vì hiếm khi tất cả tài nguyên cùng rảnh rỗi một lúc.

### 3. Phá vỡ điều kiện "Không lưu quyền" (No Preemption)
- **Cơ chế:** Nếu một tiến trình đang nắm giữ một số tài nguyên mà lại yêu cầu thêm một tài nguyên khác đang bận (không thể cấp phát ngay), thì **toàn bộ tài nguyên mà tiến trình đó đang nắm giữ sẽ bị hệ thống cưỡng bức thu hồi (preempted)** và đưa vào danh sách tài nguyên rảnh.
- Tiến trình bị tạm dừng (preempted) và chỉ được khởi động lại khi nó có thể lấy lại đồng thời cả các tài nguyên cũ đã mất lẫn tài nguyên mới vừa yêu cầu.
- **Áp dụng:** Phù hợp với các tài nguyên mà trạng thái có thể lưu và phục hồi dễ dàng như CPU registers, bộ nhớ trong (Memory pages). Không thể áp dụng cho các thiết bị như máy in hay ổ băng từ đang ghi dở.

### 4. Phá vỡ điều kiện "Chờ đợi vòng tròn" (Circular Wait)
Đây là giải pháp ngăn ngừa có tính khả thi và được áp dụng phổ biến nhất trong thực tế.
- **Cơ chế:** Thiết lập một thứ tự tuyến tính toàn cục (Global Linear Ordering) cho tất cả các loại tài nguyên bằng một ánh xạ 1-1 vào tập số tự nhiên:
  $$F: R \to \mathbb{N}$$
  *Ví dụ:* $F(\text{Tape Drive}) = 1, F(\text{Disk}) = 5, F(\text{Printer}) = 12$.
- **Quy tắc bắt buộc:** Một tiến trình có thể yêu cầu tài nguyên $R_j$ bất kỳ khi và chỉ khi:
  1. $R_j$ có số thứ tự lớn hơn tất cả các tài nguyên mà tiến trình đang nắm giữ: $F(R_j) > F(R_i), \forall R_i \text{ đang giữ}$.
  2. Hoặc, nếu muốn yêu cầu tài nguyên có số thứ tự nhỏ hơn ($F(R_j) \le F(R_i)$), tiến trình bắt buộc phải giải phóng tất cả các tài nguyên đang giữ có chỉ số $\ge F(R_j)$.
- **Chứng minh:** Vì mọi yêu cầu tài nguyên đều tuân theo thứ tự tăng dần đơn điệu của hàm $F$, nên không bao giờ có thể hình thành một chu trình phụ thuộc vòng kín $P_0 \to P_1 \to \dots \to P_0$. Chu trình bị triệt tiêu hoàn toàn.

---

## 6.5. Tránh Bế Tắc (Deadlock Avoidance) & Trạng Thái An Toàn

### 6.5.1. Khái niệm thông tin yêu cầu tối đa & Trạng thái An toàn (Safe State)
*(Căn cứ: Slide pp. 32–37)*

Khác với Ngăn ngừa (Prevention) hạn chế quyền yêu cầu tài nguyên của tiến trình thông qua các quy định tĩnh, **Tránh bế tắc (Avoidance)** cho phép tiến trình yêu cầu tự do nhưng hệ điều hành sẽ **năng động kiểm tra trước mỗi quyết định cấp phát**.

> **Yêu cầu thông tin tiên nghiệm (A priori information):**
> Mỗi tiến trình khi đăng ký vào hệ thống phải khai báo trước **Số lượng thực thể tối đa (Maximum Demand)** của mỗi loại tài nguyên mà nó có thể sẽ yêu cầu trong suốt vòng đời của mình.

#### Định nghĩa Trạng thái An toàn (Safe State)
Một trạng thái hệ thống được gọi là **An toàn (Safe)** nếu tồn tại ít nhất một **Chuỗi an toàn (Safe Sequence)** gồm toàn bộ các tiến trình của hệ thống:
$$\langle P_1, P_2, \dots, P_n \rangle$$

Sao cho đối với mỗi tiến trình $P_i$, số tài nguyên tối đa mà nó còn có thể yêu cầu thêm ($\text{Need}_i = \text{Max}_i - \text{Allocation}_i$) hoàn toàn có thể được đáp ứng bởi:
$$\text{Need}_i \le \text{Available} + \sum_{k=1}^{i-1} \text{Allocation}_k$$
*(Tức là bằng số tài nguyên hiện đang rảnh rỗi cộng với toàn bộ tài nguyên sẽ được hoàn trả bởi các tiến trình $P_k$ đứng trước nó sau khi chúng hoàn thành).*

```
                       TOÀN BỘ KHÔNG GIAN TRẠNG THÁI HỆ THỐNG
     ┌───────────────────────────────────────────────────────────────────┐
     │                                                                   │
     │  ┌────────────────── TRẠNG THÁI AN TOÀN (SAFE) ────────────────┐  │
     │  │                                                             │  │
     │  │   Tồn tại ít nhất một chuỗi an toàn: ⟨P₁, P₂, ..., Pₙ⟩      │  │
     │  │   Hệ thống bảo đảm 100% KHÔNG BAO GIỜ xảy ra bế tắc.        │  │
     │  │                                                             │  │
     │  └─────────────────────────────────────────────────────────────┘  │
     │                                                                   │
     │  ┌──────────────── TRẠNG THÁI KHÔNG AN TOÀN (UNSAFE) ──────────┐  │
     │  │                                                             │  │
     │  │   Tiềm ẩn nguy cơ bế tắc (vulnerable state).                │  │
     │  │                                                             │  │
     │  │        ┌──────── TRẠNG THÁI BẾ TẮC (DEADLOCK) ───────┐      │  │
     │  │        │                                             │      │  │
     │  │        │   Các tiến trình bị khóa cứng lẫn nhau      │      │  │
     │  │        │   (Tập con nguy hiểm nhất bên trong Unsafe) │      │  │
     │  │        │                                             │      │  │
     │  │        └─────────────────────────────────────────────┘      │  │
     │  │                                                             │  │
     │  └─────────────────────────────────────────────────────────────┘  │
     │                                                                   │
     └───────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Mối liên hệ bản chất giữa Safe, Unsafe và Deadlock:**
> 1. **Phân hoạch không gian trạng thái:** Không gian trạng thái hệ thống được phân hoạch thành hai miền rời nhau hoàn toàn: $\text{Safe State} \cap \text{Unsafe State} = \emptyset$. Trạng thái Safe và Unsafe loại trừ lẫn nhau (Disjoint).
> 2. $\text{Safe State} \implies \text{Hệ thống KHÔNG CÓ Deadlock}$.
> 3. $\text{Deadlock State} \subset \text{Unsafe State}$ ($\text{Deadlock State} \implies \text{Hệ thống đang ở trạng thái Unsafe}$). Bế tắc là tập con thực sự bên trong miền Unsafe.
> 4. $\text{Unsafe State} \not\implies \text{Chắc chắn Deadlock}$. Trạng thái Unsafe chỉ là trạng thái **tiềm ẩn rủi ro bế tắc** (vulnerable state). Nếu các tiến trình không đồng thời yêu cầu đạt mức tối đa (`Max`), hệ thống vẫn có thể may mắn hoàn thành mà không xảy ra bế tắc.
> 5. **Bản chất của Giải thuật Tránh bế tắc:** Đảm bảo hệ thống **luôn luôn duy trì trong trạng thái An toàn (Safe State)**. Nếu một yêu cầu cấp phát đẩy hệ thống vào trạng thái Unsafe, hệ thống sẽ tạm hoãn yêu cầu đó lại dù tài nguyên hiện đang có sẵn.

---

### 6.5.2. Giải thuật Banker Toàn diện (The Banker's Algorithm)
*(Căn cứ: Slide pp. 41–49; Edsger Dijkstra, 1965)*

Giải thuật Banker (Thuật toán của người chủ nhà băng) được thiết kế bởi Dijkstra, áp dụng cho hệ thống có nhiều loại tài nguyên và mỗi loại tài nguyên có thể có nhiều thực thể.

#### 1. Cấu trúc dữ liệu nền tảng
Giả sử hệ thống có $n$ tiến trình ($P_0, \dots, P_{n-1}$) và $m$ loại tài nguyên ($R_0, \dots, R_{m-1}$):

| Cấu trúc | Kích thước | Ý nghĩa toán học |
|:---|:---:|:---|
| `Available` | Vector $1 \times m$ | Số lượng thực thể hiện đang rảnh rỗi của từng loại tài nguyên. $\text{Available}[j] = k$ nghĩa là có $k$ thực thể $R_j$ sẵn sàng cấp phát. |
| `Max` | Ma trận $n \times m$ | Nhu cầu tối đa của mỗi tiến trình. $\text{Max}[i][j] = k$ nghĩa là tiến trình $P_i$ có thể yêu cầu tối đa $k$ thực thể $R_j$. |
| `Allocation`| Ma trận $n \times m$ | Số thực thể hiện đang được cấp phát cho mỗi tiến trình. $\text{Allocation}[i][j] = k$ nghĩa là $P_i$ hiện đang nắm giữ $k$ thực thể $R_j$. |
| `Need` | Ma trận $n \times m$ | Số thực thể còn lại mà tiến trình có thể sẽ yêu cầu thêm. |

**Công thức xác định ma trận Need:**
$$\text{Need}[i][j] = \text{Max}[i][j] - \text{Allocation}[i][j]$$

---

#### 2. Giải thuật An toàn (Safety Algorithm)
Dùng để kiểm tra xem trạng thái hiện tại của hệ thống có an toàn hay không:

- **Bước 1:** Khởi tạo hai cấu trúc làm việc:
  $$\text{Work} = \text{Available} \quad (\text{vector độ dài } m)$$
  $$\text{Finish}[i] = \text{false} \quad (\forall i = 0, 1, \dots, n-1)$$
- **Bước 2:** Tìm một chỉ số tiến trình $i$ thỏa mãn đồng thời hai điều kiện:
  $$\begin{cases} \text{Finish}[i] == \text{false} \\ \text{Need}_i \le \text{Work} \quad (\forall j: \text{Need}[i][j] \le \text{Work}[j]) \end{cases}$$
  - Nếu tìm thấy $i \implies$ Chuyển sang **Bước 3**.
  - Nếu không tìm thấy $i$ nào thỏa mãn $\implies$ Chuyển sang **Bước 4**.
- **Bước 3:** Giả định tiến trình $P_i$ được cấp đủ tài nguyên để hoàn thành và giải phóng toàn bộ tài nguyên nó đang nắm giữ:
  $$\text{Work} = \text{Work} + \text{Allocation}_i$$
  $$\text{Finish}[i] = \text{true}$$
  Quay lại **Bước 2** để tìm tiến trình tiếp theo.
- **Bước 4:** Đánh giá kết quả:
  - Nếu $\text{Finish}[i] == \text{true}$ với mọi $i = 0, 1, \dots, n-1$:
    $$\implies \text{Hệ thống ở TRẠNG THÁI AN TOÀN (Safe State)}$$
    Chuỗi các tiến trình được chọn ở Bước 2 chính là **Chuỗi an toàn (Safe Sequence)**.
  - Ngược lại (tồn tại ít nhất một $i$ có $\text{Finish}[i] == \text{false}$):
    $$\implies \text{Hệ thống ở TRẠNG THÁI KHÔNG AN TOÀN (Unsafe State)}$$

---

#### 3. Giải thuật Yêu cầu Tài nguyên (Resource-Request Algorithm)
Khi tiến trình $P_i$ phát sinh một yêu cầu cấp phát với vector $\text{Request}_i$:

- **Bước 1:** Kiểm tra tính hợp lệ về mặt cam kết tối đa:
  $$\text{Nếu } \text{Request}_i \le \text{Need}_i \implies \text{Chuyển sang Bước 2}$$
  $$\text{Nếu } \text{Request}_i > \text{Need}_i \implies \text{Báo lỗi (Error: Tiến trình vượt quá nhu cầu tối đa đã khai báo)}$$
- **Bước 2:** Kiểm tra tính sẵn sàng của tài nguyên hệ thống:
  $$\text{Nếu } \text{Request}_i \le \text{Available} \implies \text{Chuyển sang Bước 3}$$
  $$\text{Nếu } \text{Request}_i > \text{Available} \implies P_i \text{ phải CHỜ ĐỢI (tài nguyên hiện chưa đủ)}$$
- **Bước 3:** Giả lập cấp phát tài nguyên thử nghiệm (Tentative Allocation):
  $$\text{Available} = \text{Available} - \text{Request}_i$$
  $$\text{Allocation}_i = \text{Allocation}_i + \text{Request}_i$$
  $$\text{Need}_i = \text{Need}_i - \text{Request}_i$$
- **Bước 4:** Thực thi **Giải thuật An toàn (Safety Algorithm)** trên trạng thái vừa giả lập:
  - **Nếu trạng thái mới là AN TOÀN:** Chấp thuận yêu cầu $\implies$ Cấp phát tài nguyên thật sự cho $P_i$.
  - **Nếu trạng thái mới là KHÔNG AN TOÀN:** Từ chối cấp phát $\implies$ **Khôi phục lại trạng thái cũ (Rollback)** và bắt buộc $P_i$ phải chuyển sang trạng thái chờ.

---

## 6.6. Phát Hiện Bế Tắc (Deadlock Detection)
*(Căn cứ: Slide pp. 50–58)*

Nếu một hệ thống không áp dụng Prevention hay Avoidance, bế tắc hoàn toàn có thể xảy ra. Khi đó, hệ điều hành cần một cơ chế định kỳ chạy giải thuật để kiểm tra xem hệ thống có đang bị bế tắc hay không.

### 6.6.1. Trường hợp đơn thực thể: Đồ thị Đợi (Wait-For Graph)
- **Cơ chế:** Rút gọn từ đồ thị RAG bằng cách loại bỏ các nút tài nguyên, chỉ giữ lại các nút tiến trình:
  - Cạnh $P_i \to P_j$ xuất hiện trong đồ thị Đợi khi và chỉ khi $P_i$ đang chờ một tài nguyên mà $P_j$ đang nắm giữ.
- **Định lý:** Trong hệ thống đơn thực thể, **hệ thống bị bế tắc khi và chỉ khi đồ thị Đợi (Wait-For Graph) chứa chu trình**.
- **Chi phí:** Các giải thuật phát hiện chu trình trên đồ thị có hướng (như DFS) có độ phức tạp thuật toán là $O(n^2)$ với $n$ là số lượng tiến trình.

---

### 6.6.2. Trường hợp đa thực thể: Giải thuật Ma trận Phát hiện Deadlock
Sử dụng các cấu trúc: `Available` (vector $m$), `Allocation` (ma trận $n \times m$), và **`Request`** (ma trận $n \times m$ mô tả số tài nguyên mà mỗi tiến trình *thực tế đang gửi yêu cầu và bị chặn*).

> [!IMPORTANT]
> **Sự khác biệt cốt tử giữa Giải thuật Banker và Giải thuật Phát hiện Bế tắc:**
> - **Giải thuật Banker (Avoidance):** Sử dụng ma trận $\text{Need} = \text{Max} - \text{Allocation}$ nhằm dự đoán tình huống xấu nhất rằng tiến trình có thể đòi hỏi toàn bộ nhu cầu tối đa trong tương lai.
> - **Giải thuật Phát hiện (Detection):** Sử dụng ma trận **$\text{Request}$** hiện hành (những gì tiến trình đang thật sự đòi hỏi ngay lúc này). Nó KHÔNG quan tâm đến `Max` hay tương lai.
> - **Khởi tạo vector Finish trong Phát hiện:**
>   - Nếu tiến trình $P_i$ có $\text{Allocation}_i \ne 0 \implies \text{Finish}[i] = \text{false}$.
>   - Nếu tiến trình $P_i$ có $\text{Allocation}_i == 0$ (không giữ tài nguyên nào) $\implies \text{Finish}[i] = \text{true}$ (tiến trình này không thể tham gia vào việc gây bế tắc cho ai).

#### Thuật toán phát hiện:
1. $\text{Work} = \text{Available}$. Với mọi $i$:
   $$\text{Finish}[i] = \begin{cases} \text{true}, & \text{nếu } \text{Allocation}_i == 0 \\ \text{false}, & \text{ngược lại} \end{cases}$$
2. Tìm chỉ số $i$ sao cho:
   $$\text{Finish}[i] == \text{false} \quad \text{và} \quad \text{Request}_i \le \text{Work}$$
   Nếu tìm thấy:
   $$\text{Work} = \text{Work} + \text{Allocation}_i; \quad \text{Finish}[i] = \text{true}; \quad \text{lặp lại bước 2.}$$
3. Nếu tồn tại bất kỳ $i$ nào có $\text{Finish}[i] == \text{false}$, thì **hệ thống đang bị bế tắc và tập hợp các tiến trình có $\text{Finish}[i] == \text{false}$ chính là các tiến trình bị Deadlock**.

---

## 6.7. Phục Hồi Sau Bế Tắc (Deadlock Recovery)
*(Căn cứ: Slide pp. 59–62)*

Khi giải thuật phát hiện xác định hệ thống đã rơi vào bế tắc, hệ điều hành phải can thiệp để phá vỡ bế tắc thông qua một trong hai giải pháp:

### 1. Thu hồi bằng cách Hủy tiến trình (Process Termination)
- **Phương án 1 (Hủy toàn bộ):** Hủy bỏ tất cả các tiến trình bị bế tắc.
  - *Ưu điểm:* Chắc chắn phá vỡ bế tắc 100%.
  - *Nhược điểm:* Chi phí cực kỳ tốn kém vì mọi công việc tính toán dở dang đều bị mất.
- **Phương án 2 (Hủy từng tiến trình một):** Lần lượt hủy từng tiến trình và chạy lại giải thuật phát hiện bế tắc cho đến khi chu trình bế tắc bị phá vỡ.
  - *Tiêu chí chọn nạn nhân (Victim Selection):*
    1. Tiến trình có mức ưu tiên (Priority) thấp nhất.
    2. Tiến trình mới chạy trong thời gian ngắn, dữ liệu tạo ra ít nhất.
    3. Tiến trình đang nắm giữ ít tài nguyên nhất hoặc nắm giữ loại tài nguyên dễ thu hồi.
    4. Tiến trình cần thêm nhiều tài nguyên nhất để hoàn thành.
    5. Tiến trình tương tác (Interactive) hay tiến trình xử lý theo lô (Batch).

### 2. Thu hồi bằng cách Cưỡng bức tài nguyên (Resource Preemption)
Thu hồi tài nguyên từ một số tiến trình và cấp phát lại cho các tiến trình khác cho đến khi bế tắc được giải quyết. Khi áp dụng phương án này, hệ điều hành phải giải quyết 3 bài toán:
1. **Lựa chọn nạn nhân (Selecting a victim):** Chọn tiến trình bị thu hồi tài nguyên sao cho tổng chi phí thiệt hại là nhỏ nhất.
2. **Quay lui trạng thái (Rollback):** Tiến trình bị mất tài nguyên không thể tiếp tục bình thường. Nó phải được quay lui (rollback) về một trạng thái an toàn trong quá khứ (Checkpoint) và khởi động lại từ thời điểm đó.
3. **Hiện tượng đói tài nguyên (Starvation):** Nếu một tiến trình liên tục bị chọn làm nạn nhân để thu hồi tài nguyên, nó sẽ không bao giờ có thể hoàn thành.
   - *Giải pháp:* Đưa số lần bị chọn làm nạn nhân vào hàm tính toán chi phí (Cost Factor/Aging). Càng bị chọn nhiều lần thì chi phí chọn nó ở các lần sau càng tăng lên, buộc hệ thống phải chọn tiến trình khác.

---

## 6.8. Tổng Kết Kiến Thức Trọng Tâm & Bảng Đối Sánh

| Tiêu chí | Ngăn chặn (Prevention) | Tránh bế tắc (Avoidance) | Phát hiện & Phục hồi (Detection) |
|:---|:---|:---|:---|
| **Cơ chế chính** | Triệt tiêu 1 trong 4 điều kiện Coffman từ đầu. | Động kiểm tra trạng thái an toàn trước khi cấp phát. | Định kỳ kiểm tra chu trình và tiến hành phục hồi. |
| **Yêu cầu thông tin** | Không cần thông tin tương lai, chỉ áp đặt quy tắc. | Phải biết trước nhu cầu tối đa (`Max`) của mỗi tiến trình. | Chỉ cần biết tài nguyên hiện giữ và đang yêu cầu (`Request`). |
| **Hiệu suất sử dụng tài nguyên** | Rất thấp (do cấp phát sớm hoặc cưỡng chế nhả tài nguyên). | Trung bình đến cao (linh hoạt hơn Prevention). | Cao nhất (tài nguyên cấp phát ngay khi có sẵn). |
| **Chi phí tính toán** | Không đáng kể trong quá trình chạy. | Khá cao (mỗi lần yêu cầu phải chạy Safety Algorithm). | Trung bình (chỉ chạy định kỳ hoặc khi CPU bị nghẽn). |

---

## 6.9. Bộ Câu Hỏi Ôn Tập & Rèn Luyện Tư Duy

Học viên đối chiếu toàn bộ các dạng bài tập thực chiến và câu hỏi lý thuyết chuyên sâu tại:
👉 **[Ngân hàng Câu hỏi Tự luận & Bài tập Chương 6](../questions/subjective/ch06.md)**

Danh mục 15 đơn vị câu hỏi chuẩn hóa bao gồm:
- **Câu hỏi lý thuyết (QBANK-CH06-01 đến QBANK-CH06-08):** Định nghĩa Deadlock, 4 điều kiện Coffman, đồ thị RAG, phân tích ưu nhược điểm các phương pháp giải quyết, phân tích đồng bộ busy waiting, Trạng thái an toàn, giải thuật Banker và cơ chế phục hồi.
- **Bài tập phân tích RAG (QBANK-CH06-09 đến QBANK-CH06-11):** Nhận diện deadlock trên đồ thị (a)-(b), vẽ RAG hệ 4 tiến trình tìm chuỗi an toàn, đếm và liệt kê toàn bộ 24 chuỗi an toàn hệ 5 tiến trình.
- **Bài tập Giải thuật Banker (QBANK-CH06-12 đến QBANK-CH06-15):** Tính ma trận Need, lần vết chuỗi an toàn, xử lý yêu cầu cấp phát tức thời và giải thích trạng thái Unsafe.

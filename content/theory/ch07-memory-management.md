---
id: "ch07-memory-management"
title: "Chương 7: Quản Lý Bộ Nhớ (Memory Management)"
description: "Khảo sát toàn diện về kiến trúc quản lý bộ nhớ: không gian địa chỉ logic/vật lý, cơ chế phần cứng MMU, các mô hình cấp phát liên tục (First/Best/Next/Worst Fit), phân mảnh bộ nhớ, cơ chế phân trang cốt lõi, phần cứng TLB và thời gian hiệu dụng EAT, cấu trúc bảng trang nâng cao và cơ chế swapping."
chapter: 7
order: 7
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH07-2024"
  - "UIT-QBANK-CH07-2024"
related:
  - "sub-ch07"
review_topics:
  - "Ràng buộc địa chỉ và cặp thanh ghi Base/Limit của MMU"
  - "Phân mảnh nội trong phân vùng cố định vs Phân mảnh ngoại trong phân vùng động"
  - "Thuật toán cấp phát First Fit, Best Fit, Next Fit, Worst Fit"
  - "Quy trình chuyển đổi địa chỉ phân trang (p, d) thành (f, d)"
  - "Cơ chế hoạt động của TLB và tính toán thời gian truy xuất hiệu dụng EAT"
  - "Cấu trúc bảng trang đa cấp và cơ chế hoán vị Swapping"
source_emphasized_topics:
  - "Bản đồ phân rã bit địa chỉ logic và địa chỉ vật lý"
  - "Bài toán tính toán EAT và bài toán giải ngược hit-ratio"
  - "So sánh ưu nhược điểm các cấu trúc bảng trang: Phân cấp, Băm, Nghịch đảo"
---

# Chương 7: Quản Lý Bộ Nhớ (Memory Management)

> **Mục tiêu học tập (CLO Alignment):**
> 1. Phân biệt được sự khác nhau bản chất giữa địa chỉ logic (địa chỉ ảo) và địa chỉ vật lý; giải thích được cơ chế phần cứng MMU (Memory Management Unit) với cặp thanh ghi Base/Limit.
> 2. Đánh giá được 3 thời điểm ràng buộc địa chỉ (Compile time, Load time, Execution time) cùng các kỹ thuật nạp động (Dynamic Loading) và liên kết động (Dynamic Linking).
> 3. Phân biệt sâu sắc giữa phân mảnh nội (Internal fragmentation) và phân mảnh ngoại (External fragmentation); nắm vững điều kiện tiên quyết của kỹ thuật Gom cụm (Compaction).
> 4. Thực thi chính xác vết thực thi của 4 chiến lược cấp phát lỗ trống liên tục: First Fit, Best Fit, Next Fit, Worst Fit trên chuỗi yêu cầu thực tế.
> 5. Nắm vững cơ chế phân trang (Paging): giải thích được tại sao độ dời $d$ không đổi qua bảng trang; quy tắc phân tách trường bit nhị phân của $(p, d)$ sang $(f, d)$.
> 6. Phân tích được vai trò của bộ nhớ đệm TLB (Translation Lookaside Buffer); dẫn xuất và tính toán thành thạo Thời gian truy xuất hiệu dụng (EAT) cho cả chiều xuôi lẫn chiều giải ngược hit-ratio $\alpha$.
> 7. Khảo sát các cấu trúc bảng trang nâng cao (Bảng trang 2 cấp, Bảng băm, Bảng trang nghịch đảo), cơ chế bảo vệ và chia sẻ mã tái nhập (Reentrant code).
> 8. Trình bày được nguyên lý và phân tích chi phí trễ I/O của cơ chế Hoán vị (Swapping).

---

## 0. Bản Đồ Nhận Thức 80/20 (Chapter Entry Map)

Quản lý bộ nhớ là một trong những nhiệm vụ phức tạp và quan trọng nhất của hệ điều hành. Trong kiến trúc máy tính Von Neumann, CPU chỉ có thể nạp lệnh và thao tác trực tiếp với các thanh ghi nội bộ và bộ nhớ chính (RAM). Mọi chương trình muốn thực thi đều bắt buộc phải được đưa vào RAM.

```
                  ┌────────────────────────────────────────────────────────┐
                  │          BÀI TOÁN CỐT LÕI CỦA QUẢN LÝ BỘ NHỚ           │
                  │  RAM vật lý có hạn và cố định, nhưng nhiều tiến trình  │
                  │  cần chạy đồng thời, địa chỉ thay đổi và cần an toàn.   │
                  └───────────────────────────┬────────────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
┌───────────────────┐               ┌───────────────────┐                ┌───────────────────┐
│ 1. ĐỊA CHỈ & MMU  │               │ 2. CẤP PHÁT       │                │ 3. PHÂN TRANG     │
│ - Logic vs Vật lý │               │    LIÊN TỤC       │                │ - Trang & Khung   │
│ - 3 thời điểm bind│               │ - Phân vùng tĩnh  │                │ - Ánh xạ (p,d)->  │
│ - Cặp Base/Limit  │               │ - Phân vùng động  │                │          (f,d)    │
└─────────┬─────────┘               │ - 4 thuật toán Fit│                └─────────┬─────────┘
          │                         │ - Phân mảnh       │                          │
          │                         └───────────────────┘                          │
          ▼                                                                        ▼
┌───────────────────┐                                                    ┌───────────────────┐
│ 4. HOÁN VỊ        │                                                    │ 5. TLB & EAT      │
│ - Swapping ra đĩa │                                                    │ - Cache bảng trang│
│ - Chi phí trễ I/O │                                                    │ - Dẫn xuất EAT    │
└───────────────────┘                                                    │ - Bảng đa cấp     │
                                                                         └───────────────────┘
```

### 20% Kiến thức cốt lõi mở khóa 80% bài toán thực chiến:
1. **Mô hình ánh xạ địa chỉ phân trang:** Khắc sâu quy tắc chuyển đổi $[p \mid d] \to [f \mid d]$; độ dời $d$ được bảo toàn giữa địa chỉ logic và địa chỉ vật lý nhờ kích thước trang bằng kích thước khung trang.
2. **Vết thực thi 4 giải thuật Fit:** Hiểu rõ vị trí con trỏ của Next Fit (quét tiếp từ vị trí trước) và tiêu chuẩn tối ưu cục bộ của Best Fit vs Worst Fit.
3. **Dẫn xuất công thức EAT:** Tách bạch 2 nhánh xác suất Hit và Miss; không học vẹt công thức mà hiểu rõ số lần truy xuất RAM thực tế.

---

## 1. Khái niệm địa chỉ

### 7.1. Khái niệm cơ sở & Yêu cầu quản lý bộ nhớ
*(Căn cứ: Slide pp. 5–10; Đề cương mục 7.1; QBank `QBANK-CH07-01`)*

Bộ nhớ chính (RAM) là một mảng lớn gồm các từ nhớ (words) hoặc bytes, mỗi vị trí có một địa chỉ vật lý duy nhất. Trong hệ điều hành đa nhiệm (Multitasking), nhiều tiến trình cùng cư trú đồng thời trong bộ nhớ. Để hệ thống vận hành ổn định và hiệu quả, hệ điều hành phải đáp ứng **5 yêu cầu quản lý bộ nhớ kinh điển**:

1. **Tái định vị (Relocation):** Khi một tiến trình bị hoán vị ra đĩa rồi nạp lại vào RAM, nó có thể không được đặt vào đúng vị trí bộ nhớ vật lý ban đầu. Hệ thống phải cho phép mã lệnh và dữ liệu của tiến trình tham chiếu chính xác dù tiến trình nằm ở bất kỳ đâu trong RAM.
2. **Bảo vệ (Protection):** Mỗi tiến trình phải được bảo vệ để không bị các tiến trình khác cố ý hoặc vô ý đọc/ghi đè lên không gian nhớ của mình. Tiến trình người dùng tuyệt đối không được truy cập trái phép vào vùng nhớ của Kernel.
3. **Chia sẻ (Sharing):** Mặc dù phải bảo vệ không gian riêng, hệ điều hành vẫn phải cho phép nhiều tiến trình cùng truy cập an toàn vào một vùng nhớ chung (ví dụ: chia sẻ thư viện dùng chung `libc`, chia sẻ bộ nhớ dùng chung Shared Memory trong giao tiếp liên tiến trình IPC).
4. **Tổ chức logic (Logical Organization):** Chương trình của con người được cấu trúc thành các module logic (hàm, mảng dữ liệu, ngăn xếp Stack, vùng nhớ Heap). Hệ điều hành và phần cứng nên hỗ trợ tổ chức bộ nhớ phản ánh đúng cấu trúc logic này (tiền đề cho cơ chế phân đoạn và phân trang).
5. **Tổ chức vật lý (Physical Organization):** Bộ nhớ máy tính phân cấp thành RAM (tốc độ cao, đắt tiền, mất dữ liệu khi mất điện) và bộ nhớ phụ / Đĩa (tốc độ chậm, dung lượng lớn, lưu trữ bền vững). Hệ điều hành phải đảm nhận việc luân chuyển dữ liệu và mã lệnh nhịp nhàng giữa hai tầng lưu trữ này.

---

### 7.2. Các loại địa chỉ nhớ & Cơ chế phần cứng MMU
*(Căn cứ: Slide pp. 11–16; Đề cương mục 7.2; QBank `QBANK-CH07-02`)*

Trong vòng đời từ mã nguồn đến khi thực thi, lệnh và dữ liệu trải qua 3 dạng biểu diễn địa chỉ:

| Loại địa chỉ | Giai đoạn xuất hiện | Bản chất & Ví dụ |
| :--- | :--- | :--- |
| **Địa chỉ ký hiệu (Symbolic Address)** | Mã nguồn (Source code) | Tên biến, nhãn hàm do lập trình viên đặt: `int count;`, `goto loop_start;`. |
| **Địa chỉ tái định vị (Relocatable Address)** | Tệp đối tượng sau biên dịch (Object module) | Vị trí tương đối tính từ điểm bắt đầu module: "cách đầu module 14 bytes" (`offset 0x000E`). |
| **Địa chỉ tuyệt đối (Absolute Address)** | Bộ nhớ thực thi (Loaded in RAM) | Vị trí vật lý chính xác trên thanh RAM: `0x7FFF0014`. |

```
Mã nguồn (.c) ──[Trình biên dịch/Compiler]──> Tệp Object (.o, địa chỉ tái định vị)
                                                         │
                                               [Trình liên kết/Linker]
                                                         ▼
                                              Chương trình thực thi (.exe)
                                                         │
                                                [Trình nạp/Loader]
                                                         ▼
                                                 Bộ nhớ RAM vật lý
```

#### Phân biệt bản chất: Địa chỉ Logic vs Địa chỉ Vật lý
- **Địa chỉ Logic (Logical Address / Virtual Address):** Là địa chỉ do CPU phát sinh khi đang thực thi chỉ thị lệnh. Tập hợp tất cả các địa chỉ logic mà một chương trình tạo ra hợp thành **Không gian địa chỉ logic (Logical Address Space)**.
- **Địa chỉ Vật lý (Physical Address):** Là địa chỉ thực tế mà bộ điều khiển bộ nhớ (Memory Controller) nhìn thấy và đặt lên các đường bus địa chỉ của thanh RAM. Tập hợp tất cả các địa chỉ vật lý tương ứng hợp thành **Không gian địa chỉ vật lý (Physical Address Space)**.

> [!MENTALMODEL]
> **Ẩn dụ Mô hình Khách sạn:**
> - **Địa chỉ logic** giống như *Số phòng khách sạn* (Phòng 301, Tầng 3, phòng số 1 tính từ cầu thang). Khi khách đi lại trong khách sạn, họ chỉ cần nhớ số phòng tương đối này.
> - **Địa chỉ vật lý** giống như *Tọa độ GPS mặt đất* (Kinh độ $10.8700^\circ\text{N}$, Vĩ độ $106.8030^\circ\text{E}$).
> - **Bộ chuyển đổi MMU** đóng vai trò như viên lễ tân: Khi nhận yêu cầu "Vào phòng 301", lễ tân lấy tọa độ móng của tòa nhà (Base Register) cộng với độ dời của phòng để chỉ đến vị trí vật lý chính xác.

#### Cơ chế phần cứng MMU & Cặp thanh ghi Base / Limit
Việc chuyển đổi từ địa chỉ logic sang địa chỉ vật lý trong thời gian thực thi được thực hiện hoàn toàn bởi thiết bị phần cứng chuyên trách gọi là **MMU (Memory Management Unit)**.

Trong mô hình cấp phát liên tục cơ bản, MMU sử dụng hai thanh ghi phần cứng:
- **Thanh ghi Cơ sở (Base Register hay Relocation Register):** Chứa địa chỉ vật lý nhỏ nhất bắt đầu vùng nhớ của tiến trình.
- **Thanh ghi Giới hạn (Limit Register):** Chứa kích thước không gian địa chỉ logic của tiến trình (phạm vi hợp lệ).

```
                      ĐỊA CHỈ LOGIC
                         [ CPU ]
                            │
                            ▼
                     ┌─────────────┐
                     │ Địa chỉ <   │      KHÔNG (Trap: Lỗi truy cập bộ nhớ)
                     │   Limit?    │ ───────────> [ BẪY NGẮT SEGFAULT ]
                     └──────┬──────┘
                            │ ĐÚNG
                            ▼
                         [  +  ] <──── Thanh ghi Base (Relocation Register)
                            │
                            ▼
                      ĐỊA CHỈ VẬT LÝ
                         [ RAM ]
```

> [!EXECUTIONTRACE]
> **Vết thực thi an toàn của phần cứng MMU:**
> 1. CPU phát sinh địa chỉ logic $L$.
> 2. Phần cứng so sánh: Kiểm tra điều kiện $0 \le L < \text{Limit}$.
> 3. Nếu $L \ge \text{Limit}$: CPU lập tức kích hoạt bẫy ngắt lỗi định địa chỉ (Trap Addressing Error / Segmentation Fault), hệ điều hành can thiệp và tiêu diệt tiến trình vi phạm.
> 4. Nếu $L < \text{Limit}$: Bộ cộng phần cứng tính:
>    $$\text{Địa chỉ vật lý} = L + \text{Base}$$
>    Địa chỉ này được gửi lên bus địa chỉ để đọc/ghi thanh RAM.

> [!RECALLCHECKPOINT] id="rc-ch07-logical-vs-physical" concept_id="ch07-address-binding"
> **Nhiệm vụ thu hồi kín sách (Closed-book Recall):**
> 1. Nêu sự khác nhau bản chất giữa địa chỉ logic và địa chỉ vật lý.
> 2. Thành phần phần cứng nào thực hiện ánh xạ địa chỉ khi tiến trình đang chạy?
> 3. Trình bày điều kiện kiểm tra an toàn của cặp thanh ghi Base và Limit trong MMU.
> <!-- rubric -->
> - [0.3 điểm] Nêu rõ địa chỉ logic do CPU phát sinh; địa chỉ vật lý là vị trí thực tế trên bus phần cứng RAM.
> - [0.3 điểm] Chỉ định chính xác MMU (Memory Management Unit) thực hiện chuyển đổi phần cứng trong thời gian thực thi.
> - [0.4 điểm] Trình bày đúng điều kiện an toàn: Địa chỉ logic < Limit thì Physical = Logical + Base; ngược lại phát sinh ngắt bẫy lỗi (Trap / Segfault).

---

### 7.3. Ràng buộc địa chỉ (Address Binding)
*(Căn cứ: Slide pp. 17–22; Đề cương mục 7.3; QBank `QBANK-CH07-03`)*

Ràng buộc địa chỉ (Address Binding) là quá trình ánh xạ không gian địa chỉ của chương trình từ dạng này sang dạng khác (từ logic sang vật lý). Quá trình này có thể diễn ra tại một trong 3 thời điểm:

```
+──────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| Thời điểm ràng buộc  | Cơ chế hoạt động                        | Đánh giá & Điều kiện phần cứng       |
+──────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| 1. Compile Time      | Trình biên dịch sinh mã trực tiếp gắn   | Rất cứng nhắc. Nếu vùng nhớ nạp thay |
| (Thời điểm biên dịch)| với địa chỉ vật lý tuyệt đối trong RAM. | đổi, bắt buộc phải biên dịch lại toàn|
|                      |                                         | bộ mã nguồn.                         |
+──────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| 2. Load Time         | Trình biên dịch giữ địa chỉ tái định vị | Linh hoạt hơn: có thể nạp vào bất kỳ |
| (Thời điểm nạp)      | (bắt đầu từ 0). Trình nạp (Loader) ánh  | đâu trong RAM. Nhưng một khi đã nạp  |
|                      | xạ sang địa chỉ vật lý khi nạp vào RAM. | thì KHÔNG THỂ di chuyển tiến trình.  |
+──────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| 3. Execution Time    | Ràng buộc bị trì hoãn cho đến khi chỉ thị| Tối ưu nhất: tiến trình có thể di    |
| (Thời điểm thực thi) | thực sự chạy trên CPU. Địa chỉ được MMU | dời giữa các vùng nhớ khi đang chạy. |
|                      | cộng Base Register trong từng chu kỳ.   | Bắt buộc phải có hỗ trợ phần cứng MMU.|
+──────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
```

---

### 7.3.1. Nạp động và Liên kết động (Dynamic Loading & Dynamic Linking)
*(Căn cứ: Slide pp. 23–27; Đề cương mục 7.3; QBank `QBANK-CH07-04`)*

- **Nạp động (Dynamic Loading):** Một thủ tục (routine/function) chỉ được nạp vào RAM khi nó thực sự được gọi trong quá trình chạy. Toàn bộ các thủ tục chưa dùng tới vẫn nằm trên đĩa cứng ở định dạng tái định vị.
  - *Lợi ích:* Tiết kiệm không gian bộ nhớ khi chương trình chứa nhiều đoạn mã xử lý lỗi hiếm khi xảy ra hoặc các tính năng tùy chọn. Không đòi hỏi sự hỗ trợ đặc biệt từ hệ điều hành (do lập trình viên thiết kế qua cấu trúc chương trình).
- **Liên kết động (Dynamic Linking):** Việc liên kết thư viện hệ thống bị trì hoãn cho đến thời điểm thực thi chương trình.
  - *Cơ chế hoạt động:* Trong mã nhị phân của chương trình, trình liên kết chèn một đoạn mã ngắn gọi là **Stub**. Khi hàm thư viện được gọi lần đầu, Stub kiểm tra xem hàm đó đã có trong RAM chưa. Nếu chưa, nó yêu cầu hệ điều hành nạp thư viện vào RAM. Sau đó Stub tự thay thế chính nó bằng địa chỉ thực của hàm thư viện.
  - *Lợi ích vượt trội:* Hàng trăm tiến trình cùng gọi thư viện chuẩn `printf()` chỉ cần dùng chung **MỘT bản sao duy nhất** của thư viện trong RAM (Shared Libraries / `.so` trên Linux, `.dll` trên Windows). Dễ dàng nâng cấp bản vá thư viện mà không cần biên dịch lại ứng dụng.

---

## 2. Cấp phát liên tục

### 7.4. Các mô hình cấp phát liên tục (Contiguous Allocation)
*(Căn cứ: Slide pp. 28–32; Đề cương mục 7.4)*

Trong cơ chế cấp phát liên tục, mỗi tiến trình được cấp phát một khối bộ nhớ đơn nhất, liên tục không đứt quãng trong không gian địa chỉ vật lý.

---

### 7.4.1. Phân vùng cố định (Static Partitioning) & Phân mảnh nội
*(Căn cứ: Slide pp. 33–36; Đề cương mục 7.4.1; QBank `QBANK-CH07-06`)*

Bộ nhớ được chia thành các phân vùng có kích thước xác định trước ngay khi khởi động hệ thống (các phân vùng có thể bằng nhau hoặc khác nhau). Mỗi phân vùng chỉ chứa đúng một tiến trình tại một thời điểm.

```
+─────────────────────── Bộ nhớ RAM ───────────────────────+
| Vùng HĐH | Phân vùng 1 (100K) | Phân vùng 2 (300K)       |
| (Kernel) | [Tiến trình P1: 80K] [Tiến trình P2: 210K]    |
|          | (Lãng phí: 20K)     | (Lãng phí: 90K)         |
|          | <--- Mảnh nội ----> | <--- Mảnh nội --------> |
+──────────────────────────────────────────────────────────+
```

> [!IMPORTANT]
> **Định nghĩa Phân mảnh nội (Internal Fragmentation):**
> Phân mảnh nội là hiện tượng vùng nhớ trống nằm **bên trong** một phân vùng đã được cấp phát cho tiến trình nhưng tiến trình không sử dụng hết, và phần dư thừa này **không thể** được cấp phát cho bất kỳ tiến trình nào khác.
> - *Nguyên nhân:* Kích thước phân vùng cấp phát lớn hơn kích thước thực tế mà tiến trình yêu cầu.

---

### 7.4.2. Phân vùng động (Dynamic Partitioning) & Phân mảnh ngoại
*(Căn cứ: Slide pp. 37–39; Đề cương mục 7.4.2 chuẩn hóa từ lỗi typo 7.4.1 nguồn; QBank `QBANK-CH07-05`)*

Hệ điều hành không chia trước bộ nhớ. Khi một tiến trình được nạp, hệ điều hành tìm một khối nhớ trống vừa khít với kích thước của tiến trình để cấp phát. Sau một thời gian hoạt động với các tiến trình nạp vào và kết thúc giải phóng, bộ nhớ bị phân tách thành các vùng nhớ bị chiếm giữ xen kẽ với các khối nhớ trống gọi là các **Lỗ trống (Holes)**.

```
+────────────────────────── Bộ nhớ RAM ──────────────────────────+
| P1 (200K) | Lỗ trống 1 (50K) | P2 (300K) | Lỗ trống 2 (70K)    |
| (Đang chạy)| (Chưa dùng)      | (Đang chạy)| (Chưa dùng)         |
+────────────────────────────────────────────────────────────────+
  Yêu cầu P3 (100K) tới -> TỔNG TRỐNG = 50K + 70K = 120K > 100K
  NHƯNG P3 VẪN BỊ TỪ CHỐI VÌ KHÔNG CÓ KHỐI LIÊN TỤC NÀO ĐỦ 100K!
```

> [!IMPORTANT]
> **Định nghĩa Phân mảnh ngoại (External Fragmentation):**
> Phân mảnh ngoại là hiện tượng tổng dung lượng bộ nhớ còn trống trong hệ thống là **đủ** để thỏa mãn yêu cầu của tiến trình mới, nhưng các vùng trống này bị phân tán thành các mảnh nhỏ rời rạc, **không liên tục**, khiến hệ thống không thể cấp phát cho tiến trình.
> - *Nguyên nhân:* Các tiến trình vào/ra hệ thống động tạo ra các lỗ trống kích thước khác nhau xen kẽ giữa các vùng bộ nhớ đang bị chiếm giữ.

> [!NOTE]
> **Quy tắc 50% (50-Percent Rule) [TIER_B_ENRICHMENT]:**
> Phân tích thống kê kinh điển của Donald Knuth chứng minh rằng: với chiến lược First Fit, trong điều kiện hệ thống dừng ổn định, cứ mỗi $N$ khối bộ nhớ được cấp phát sẽ có khoảng $0.5 N$ khối nhớ bị phân mảnh ngoại lãng phí. Nghĩa là khoảng một phần ba (khoảng 33%) tổng bộ nhớ có thể không sử dụng được!

> [!RECALLCHECKPOINT] id="rc-ch07-fragmentation" concept_id="ch07-fragmentation"
> **Nhiệm vụ thu hồi kín sách (Closed-book Recall):**
> 1. Phân biệt sự khác nhau căn bản về vị trí và nguyên nhân giữa phân mảnh nội và phân mảnh ngoại.
> 2. Phân vùng cố định gây ra loại phân mảnh nào? Phân vùng động gây ra loại phân mảnh nào?
> <!-- rubric -->
> - [0.5 điểm] Nêu rõ phân mảnh nội nằm bên trong phân vùng do cấp phát dư; phân mảnh ngoại nằm rải rác ngoài các phân vùng do các lỗ trống không liên tục.
> - [0.5 điểm] Khẳng định chính xác: Phân vùng cố định sinh ra phân mảnh nội; phân vùng động sinh ra phân mảnh ngoại.

---

### 7.4.3. Bốn chiến lược cấp phát lỗ trống (Placement Strategies)
*(Căn cứ: Slide pp. 37–39, 67; Đề cương mục 7.4.2; QBank `QBANK-CH07-06`, `QBANK-CH07-10`)*

Khi có một danh sách các lỗ trống tự do (Free Hole List), hệ điều hành có thể chọn một trong 4 thuật toán sau để chọn lỗ trống cấp cho tiến trình:

1. **First Fit (Khớp đầu tiên):** Quét danh sách lỗ trống từ đầu, cấp phát lỗ trống **đầu tiên** tìm thấy có kích thước đủ lớn ($\text{Hole Size} \ge \text{Process Size}$).
2. **Best Fit (Khớp tốt nhất):** Quét toàn bộ danh sách, chọn lỗ trống **nhỏ nhất** trong số các lỗ đủ lớn (lỗ có kích thước gần nhất với yêu cầu của tiến trình).
   - *Đặc điểm:* Để lại lỗ trống dư thừa nhỏ nhất có thể, nhưng dễ tạo ra vô số mảnh vụn li ti vô dụng.
3. **Worst Fit (Khớp tồi nhất):** Quét toàn bộ danh sách, chọn lỗ trống **lớn nhất** có trong hệ thống.
   - *Ý tưởng:* Lỗ trống còn lại sau khi cấp phát vẫn có kích thước tương đối lớn, hy vọng có thể tái sử dụng cho tiến trình khác.
4. **Next Fit (Khớp kế tiếp):** Giống First Fit, nhưng không quét lại từ đầu danh sách mà **bắt đầu quét từ vị trí con trỏ cấp phát của lượt trước**, quay vòng (wrap-around) về đầu danh sách nếu chạm đáy.

---

#### Vết thực thi chuẩn mực: Bài tập mẫu Slide 67 & QBANK-CH07-10
*(Bảo toàn số liệu chính thức UIT: 4 phân vùng trống $600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$; chuỗi tiến trình $P_1(212\text{KB}), P_2(417\text{KB}), P_3(112\text{KB}), P_4(426\text{KB})$).*

##### 1. Chiến lược First Fit:
- Trạng thái ban đầu: $[\text{H}_1: 600\text{K}, \text{H}_2: 500\text{K}, \text{H}_3: 200\text{K}, \text{H}_4: 300\text{K}]$.
- $P_1(212\text{K})$: Quét từ đầu $\implies$ gặp $\text{H}_1(600\text{K})$ đủ lớn. Cấp vào $\text{H}_1$. Còn lại $\text{H}_1 = 600 - 212 = 388\text{K}$.
  - Danh sách lỗ: $[388\text{K}, 500\text{K}, 200\text{K}, 300\text{K}]$.
- $P_2(417\text{K})$: Quét từ đầu: $388\text{K} < 417\text{K}$ (bỏ qua) $\implies$ gặp $\text{H}_2(500\text{K})$ đủ lớn. Cấp vào $\text{H}_2$. Còn lại $\text{H}_2 = 500 - 417 = 83\text{K}$.
  - Danh sách lỗ: $[388\text{K}, 83\text{K}, 200\text{K}, 300\text{K}]$.
- $P_3(112\text{K})$: Quét từ đầu $\implies$ gặp $\text{H}_1(388\text{K})$ đủ lớn. Cấp vào $\text{H}_1$. Còn lại $\text{H}_1 = 388 - 112 = 276\text{K}$.
  - Danh sách lỗ: $[276\text{K}, 83\text{K}, 200\text{K}, 300\text{K}]$.
- $P_4(426\text{K})$: Quét từ đầu: $276\text{K} < 426\text{K}$, $83\text{K} < 426\text{K}$, $200\text{K} < 426\text{K}$, $300\text{K} < 426\text{K}$. Không có lỗ nào đủ lớn!
- **Kết luận First Fit:** $P_1 \to \text{Phân vùng 1}$, $P_2 \to \text{Phân vùng 2}$, $P_3 \to \text{Phân vùng 1}$. $P_4$ phải chờ.

##### 2. Chiến lược Best Fit:
- Trạng thái ban đầu: $[\text{H}_1: 600\text{K}, \text{H}_2: 500\text{K}, \text{H}_3: 200\text{K}, \text{H}_4: 300\text{K}]$.
- $P_1(212\text{K})$: Các lỗ đủ lớn gồm $600\text{K}, 500\text{K}, 300\text{K}$. Nhỏ nhất là $\text{H}_4(300\text{K})$. Cấp vào $\text{H}_4$. Còn lại $\text{H}_4 = 300 - 212 = 88\text{K}$.
  - Danh sách lỗ: $[600\text{K}, 500\text{K}, 200\text{K}, 88\text{K}]$.
- $P_2(417\text{K})$: Các lỗ đủ lớn gồm $600\text{K}, 500\text{K}$. Nhỏ nhất là $\text{H}_2(500\text{K})$. Cấp vào $\text{H}_2$. Còn lại $\text{H}_2 = 500 - 417 = 83\text{K}$.
  - Danh sách lỗ: $[600\text{K}, 83\text{K}, 200\text{K}, 88\text{K}]$.
- $P_3(112\text{K})$: Các lỗ đủ lớn gồm $600\text{K}, 200\text{K}$. Nhỏ nhất là $\text{H}_3(200\text{K})$. Cấp vào $\text{H}_3$. Còn lại $\text{H}_3 = 200 - 112 = 88\text{K}$.
  - Danh sách lỗ: $[600\text{K}, 83\text{K}, 88\text{K}, 88\text{K}]$.
- $P_4(426\text{K})$: Lỗ đủ lớn duy nhất là $\text{H}_1(600\text{K})$. Cấp vào $\text{H}_1$. Còn lại $\text{H}_1 = 600 - 426 = 174\text{K}$.
  - Danh sách lỗ cuối: $[174\text{K}, 83\text{K}, 88\text{K}, 88\text{K}]$.
- **Kết luận Best Fit:** Cả 4 tiến trình được cấp phát thành công! ($P_1 \to 300\text{K}, P_2 \to 500\text{K}, P_3 \to 200\text{K}, P_4 \to 600\text{K}$).

##### 3. Chiến lược Next Fit:
- Trạng thái ban đầu: $[\text{H}_1: 600\text{K}, \text{H}_2: 500\text{K}, \text{H}_3: 200\text{K}, \text{H}_4: 300\text{K}]$. Con trỏ tại $\text{H}_1$.
- $P_1(212\text{K})$: Bắt đầu tại $\text{H}_1(600\text{K}) \implies$ đủ lớn, cấp vào $\text{H}_1$. Còn $\text{H}_1 = 388\text{K}$. Con trỏ dừng tại $\text{H}_1$.
- $P_2(417\text{K})$: Quét tiếp từ sau $\text{H}_1 \implies$ gặp $\text{H}_2(500\text{K})$ đủ lớn, cấp vào $\text{H}_2$. Còn $\text{H}_2 = 83\text{K}$. Con trỏ dừng tại $\text{H}_2$.
- $P_3(112\text{K})$: Quét tiếp từ sau $\text{H}_2 \implies$ gặp $\text{H}_3(200\text{K})$ đủ lớn, cấp vào $\text{H}_3$. Còn $\text{H}_3 = 88\text{K}$. Con trỏ dừng tại $\text{H}_3$.
- $P_4(426\text{K})$: Quét tiếp từ sau $\text{H}_3 \implies$ kiểm tra $\text{H}_4(300\text{K}) < 426\text{K}$, quay vòng kiểm tra $\text{H}_1(388\text{K}) < 426\text{K}$, $\text{H}_2(83\text{K}) < 426\text{K}$, $\text{H}_3(88\text{K}) < 426\text{K}$. Không có lỗ nào đủ lớn!
- **Kết luận Next Fit:** $P_1 \to \text{Phân vùng 1}$, $P_2 \to \text{Phân vùng 2}$, $P_3 \to \text{Phân vùng 3}$. $P_4$ phải chờ.

##### 4. Chiến lược Worst Fit:
- Trạng thái ban đầu: $[\text{H}_1: 600\text{K}, \text{H}_2: 500\text{K}, \text{H}_3: 200\text{K}, \text{H}_4: 300\text{K}]$.
- $P_1(212\text{K})$: Lỗ lớn nhất là $\text{H}_1(600\text{K})$. Cấp vào $\text{H}_1$. Còn $\text{H}_1 = 388\text{K}$.
  - Danh sách lỗ: $[388\text{K}, 500\text{K}, 200\text{K}, 300\text{K}]$.
- $P_2(417\text{K})$: Lỗ lớn nhất là $\text{H}_2(500\text{K})$. Cấp vào $\text{H}_2$. Còn $\text{H}_2 = 83\text{K}$.
  - Danh sách lỗ: $[388\text{K}, 83\text{K}, 200\text{K}, 300\text{K}]$.
- $P_3(112\text{K})$: Lỗ lớn nhất hiện tại là $\text{H}_1(388\text{K})$. Cấp vào $\text{H}_1$. Còn $\text{H}_1 = 388 - 112 = 276\text{K}$.
  - Danh sách lỗ: $[276\text{K}, 83\text{K}, 200\text{K}, 300\text{K}]$.
- $P_4(426\text{K})$: Lỗ lớn nhất hiện tại là $\text{H}_4(300\text{K}) < 426\text{K}$. Không cấp phát được!
- **Kết luận Worst Fit:** $P_1 \to \text{Phân vùng 1}$, $P_2 \to \text{Phân vùng 2}$, $P_3 \to \text{Phân vùng 1}$. $P_4$ phải chờ.

> [!ERRORDIAGNOSIS]
> **Các lỗi sai kinh điển khi thi giải thuật Fit:**
> 1. **Quên cập nhật kích thước lỗ trống:** Sau khi cấp phát cho $P_1$, kích thước lỗ $\text{H}_1$ giảm xuống. Nhiều sinh viên vẫn lấy số liệu $600\text{K}$ ban đầu để xét cho các tiến trình sau.
> 2. **Quên con trỏ Next Fit:** Nhầm Next Fit thành First Fit (quay lại đầu danh sách sau mỗi tiến trình). Cần nhớ: Next Fit chỉ quay đầu khi đã chạm đáy danh sách.
> 3. **Nhầm tưởng Best Fit là tối ưu toàn cục:** Best Fit chỉ là một quy tắc lựa chọn cục bộ (chọn phân vùng trống nhỏ nhất vừa đủ kích thước tại thời điểm xét). Nó không đảm bảo tối ưu toàn cục về hiệu quả sử dụng bộ nhớ trong chuỗi cấp phát và giải phóng động lâu dài, bởi nó có xu hướng để lại các mảnh vụn rất nhỏ khó tái sử dụng cho các yêu cầu kế tiếp.

> [!RECALLCHECKPOINT] id="rc-ch07-fit-algorithms" concept_id="ch07-fit-algorithms"
> **Nhiệm vụ thu hồi kín sách (Closed-book Recall):**
> 1. Trình bày sự khác biệt giữa First Fit và Next Fit về điểm bắt đầu duyệt danh sách.
> 2. Vì sao Best Fit có xu hướng tạo ra nhiều mảnh vụn nhỏ hơn Worst Fit?
> <!-- rubric -->
> - [0.5 điểm] First Fit luôn bắt đầu quét từ đầu danh sách lỗ trống; Next Fit quét tiếp từ vị trí con trỏ cấp phát của lượt trước đó.
> - [0.5 điểm] Best Fit chọn lỗ nhỏ nhất vừa khít nên phần dư thừa để lại có kích thước tối thiểu, tạo thành các mảnh vụn nhỏ li ti khó tái sử dụng.

> [!TRANSFERPROBLEM] id="tp-ch07-fit-allocation" concept_id="ch07-fit-algorithms"
> **Bài toán chuyển giao độc lập (Transfer Challenge):**
> Cho hệ thống có 4 phân vùng trống ban đầu theo thứ tự: $400\text{KB}, 700\text{KB}, 300\text{KB}, 500\text{KB}$.
> Chuỗi sự kiện diễn ra như sau:
> 1. Cấp phát lần lượt cho $P_1(280\text{KB})$ và $P_2(350\text{KB})$.
> 2. Ngay sau đó, tiến trình $P_1$ kết thúc và giải phóng toàn bộ bộ nhớ của mình.
> 3. Hệ thống tiếp tục nhận yêu cầu cấp phát cho $P_3(380\text{KB})$.
> **Yêu cầu:** Xác định vị trí phân vùng được cấp phát cho $P_3$ theo hai giải thuật: **First Fit** và **Best Fit**.
> <!-- solution -->
> **Lời giải chi tiết:**
> - Ban đầu: $[\text{H}_1: 400\text{K}, \text{H}_2: 700\text{K}, \text{H}_3: 300\text{K}, \text{H}_4: 500\text{K}]$.
> 
> *Với First Fit:*
> - $P_1(280\text{K})$: Cấp vào $\text{H}_1(400\text{K})$, còn $120\text{K}$. Trạng thái: $[\text{P}_1(280\text{K}), 120\text{K}, 700\text{K}, 300\text{K}, 500\text{K}]$.
> - $P_2(350\text{K})$: Quét từ đầu: $120\text{K} < 350\text{K}$, gặp $\text{H}_2(700\text{K})$ cấp vào $\text{H}_2$, còn $350\text{K}$.
> - $P_1$ giải phóng: Phân vùng 1 khôi phục thành lỗ trống $400\text{K}$.
>   - Danh sách lỗ hiện tại: $[\text{H}_1: 400\text{K}, \text{H}_2: 350\text{K}, \text{H}_3: 300\text{K}, \text{H}_4: 500\text{K}]$.
> - $P_3(380\text{K})$: Quét từ đầu $\implies$ gặp ngay $\text{H}_1(400\text{K})$ đủ lớn!
>   - **Kết quả First Fit:** $P_3$ được nạp vào Phân vùng 1 (còn dư $20\text{K}$).
> 
> *Với Best Fit:*
> - $P_1(280\text{K})$: Lỗ nhỏ nhất đủ chứa là $\text{H}_3(300\text{K})$. Cấp vào $\text{H}_3$, còn $20\text{K}$.
> - $P_2(350\text{K})$: Lỗ nhỏ nhất đủ chứa là $\text{H}_1(400\text{K})$. Cấp vào $\text{H}_1$, còn $50\text{K}$.
> - $P_1$ giải phóng: Lỗ tại $\text{H}_3$ khôi phục thành $300\text{K}$.
>   - Danh sách lỗ hiện tại: $[50\text{K}, 700\text{K}, 300\text{K}, 500\text{K}]$.
> - $P_3(380\text{K})$: Các lỗ đủ lớn gồm $700\text{K}$ và $500\text{K}$. Nhỏ nhất là $\text{H}_4(500\text{K})$.
>   - **Kết quả Best Fit:** $P_3$ được nạp vào Phân vùng 4 (còn dư $120\text{K}$).

---

### 7.4.4. Kỹ thuật Gom cụm (Compaction)
*(Căn cứ: Slide p. 39; Đề cương mục 7.4.2)*

Gom cụm là giải pháp duy nhất trong cấp phát liên tục để khắc phục phân mảnh ngoại: Hệ thống di dời tất cả các tiến trình đang chiếm giữ bộ nhớ dồn về một đầu (ví dụ dồn về đáy RAM), gom tất cả các lỗ trống nhỏ rải rác lại thành một khối bộ nhớ tự do khổng lồ duy nhất.

> [!IMPORTANT]
> **Điều kiện tiên quyết của Gom cụm:**
> Gom cụm **CHỈ KHẢ THI** nếu hệ thống áp dụng cơ chế **Ràng buộc địa chỉ tại thời điểm thực thi (Execution-time binding)** có hỗ trợ phần cứng thanh ghi tái định vị (Relocation Register). Khi di chuyển tiến trình, hệ điều hành chỉ cần cập nhật giá trị mới vào thanh ghi Base của tiến trình đó. Nếu dùng Compile-time hoặc Load-time binding, việc di chuyển tiến trình sẽ phá hủy toàn bộ con trỏ tuyệt đối bên trong mã máy.
> - *Hạn chế:* Chi phí đọc/ghi toàn bộ nội dung bộ nhớ cực kỳ tốn thời gian (I/O latency), làm hệ thống tạm ngừng phản hồi trong quá trình gom dồn.

---

## 3. Phân trang & TLB

### 7.5. Cơ chế phân trang cốt lõi (Paging Fundamentals)
*(Căn cứ: Slide pp. 40–47; Đề cương mục 7.5; QBank `QBANK-CH07-07`)*

Phân trang là giải pháp đột phá loại bỏ hoàn toàn cơ chế cấp phát liên tục:
- **Không gian địa chỉ logic** của tiến trình được chia thành các khối cố định bằng nhau gọi là **Trang (Pages)**.
- **Bộ nhớ vật lý (RAM)** được chia thành các khối có kích thước hoàn toàn bằng kích thước của trang, gọi là **Khung trang (Frames)**.
- Hệ điều hành duy trì một **Bảng phân trang (Page Table)** cho mỗi tiến trình để theo dõi trang logic nào của tiến trình đang nằm ở khung trang vật lý nào trong RAM.

```
TIẾN TRÌNH (Địa chỉ Logic)               BẢNG PHÂN TRANG               BỘ NHỚ VẬT LÝ (RAM)
┌────────────────────────┐              ┌───────────────┐              ┌────────────────────────┐
│ Trang 0 (Page 0)       │              │ Trang │ Khung │              │ Khung 0 (Frame 0)      │
├────────────────────────┤              ├───────┼───────┤              ├────────────────────────┤
│ Trang 1 (Page 1)       │              │   0   │   2   │              │ Khung 1 (Trang 2)      │
├────────────────────────┤              │   1   │   4   │              ├────────────────────────┤
│ Trang 2 (Page 2)       │              │   2   │   1   │              │ Khung 2 (Trang 0)      │
├────────────────────────┤              │   3   │   5   │              ├────────────────────────┤
│ Trang 3 (Page 3)       │              └───────┴───────┘              │ Khung 3 (Trống)        │
└────────────────────────┘                                             ├────────────────────────┤
                                                                       │ Khung 4 (Trang 1)      │
                                                                       ├────────────────────────┤
                                                                       │ Khung 5 (Trang 3)      │
                                                                       └────────────────────────┘
```

#### Mô hình nhận thức: Vì sao độ dời $d$ không đổi?
Địa chỉ do CPU phát sinh được chia thành 2 phần:
- **Số trang ($p$ - Page number):** Dùng làm chỉ số để tra vào Bảng phân trang nhằm tìm ra số khung trang vật lý ($f$ - Frame number).
- **Độ dời ($d$ - Offset):** Vị trí tương đối của byte cần truy xuất tính từ đầu trang.

$$\text{Địa chỉ Logic: } [p \mid d] \xrightarrow{\text{Tra bảng trang } p \to f} \text{Địa chỉ Vật lý: } [f \mid d]$$

> [!NOTE]
> **Bản chất của việc độ dời $d$ không đổi:**
> Vì kích thước trang $S$ **hoàn toàn bằng** kích thước khung trang $S$, khoảng cách từ byte dữ liệu tới byte đầu tiên của trang trong không gian logic chính là khoảng cách từ byte đó tới byte đầu tiên của khung trang trong không gian vật lý. Do đó, phần cứng chỉ cần thay thế số trang $p$ bằng số khung $f$, còn trường độ dời $d$ được bảo toàn hoàn toàn giữa địa chỉ logic và địa chỉ vật lý!

#### Quy tắc phân tách bit nhị phân
Các hệ thống đánh địa chỉ theo cơ số nhị phân theo quy ước kiến trúc thường chọn kích thước trang là **lũy thừa của 2** (ví dụ $4\text{KB} = 2^{12}\text{ bytes}$, $2\text{KB} = 2^{11}\text{ bytes}$), cho phép số trang $p$ và độ dời $d$ được trích xuất trực tiếp từ các trường bit của địa chỉ mà không cần tính toán số học.
- Nếu không gian địa chỉ logic có kích thước $2^m$ bytes và kích thước trang là $2^n$ bytes:
  - $n$ bit thấp nhất biểu diễn độ dời $d$ ($d = n\text{ bit}$).
  - $m - n$ bit cao biểu diễn số trang $p$ ($p = m - n\text{ bit}$).
- *Ý nghĩa kiến trúc:* Phần cứng trích xuất số trang và độ dời trực tiếp bằng thao tác dịch bit (bit-shift) và mặt nạ bit (bit-mask), hoàn toàn không tốn một chu kỳ tính toán số học chia/lấy dư nào của ALU.

#### Phân mảnh trong cơ chế phân trang
- **Phân mảnh ngoại:** Bị **LOẠI BỎ HOÀN TOÀN**! Vì bất kỳ khung trang trống nào trong RAM cũng có thể được cấp cho bất kỳ trang nào của tiến trình.
- **Phân mảnh nội:** **VẪN TỒN TẠI**, nhưng chỉ xảy ra ở trang cuối cùng của tiến trình nếu kích thước tiến trình không chia hết cho kích thước trang. Vùng lãng phí trung bình là nửa trang ($S/2$).

---

### 7.5.3. Quy trình chuyển đổi địa chỉ phân trang
*(Căn cứ: Slide pp. 43–47; Đề cương mục 7.5.1; QBank `QBANK-CH07-15`)*

Quy trình chuyển đổi toán học tổng quát:
1. Xác định số trang: $p = \lfloor L / S \rfloor$ (hoặc lấy các bit cao).
2. Xác định độ dời: $d = L \pmod S$ (hoặc lấy các bit thấp).
3. Tra bảng trang tại mục $p$ để lấy số khung $f$.
4. Tính địa chỉ vật lý: $\text{Physical Address} = f \times S + d$.

> [!WORKEDEXAMPLE]
> **Bài toán mẫu chuẩn đơn trị QBANK-CH07-15 (P70–P75 docx):**
> Cho kích thước trang $S = 2\text{KB} = 2048\text{ bytes}$. Địa chỉ logic cần chuyển đổi là $L = 3254$. Bảng phân trang của tiến trình có mục: Trang 1 được nạp vào Khung 4.
> 
> **Các bước giải chi tiết:**
> - Bước 1: Tìm số trang $p$ và độ dời $d$:
>   $$p = \lfloor 3254 / 2048 \rfloor = 1$$
>   $$d = 3254 \pmod{2048} = 3254 - 2048 = 1206$$
> - Bước 2: Tra bảng trang tại mục $p = 1 \implies$ Khung trang $f = 4$.
> - Bước 3: Tính địa chỉ vật lý:
>   $$\text{Physical Address} = f \times S + d = 4 \times 2048 + 1206 = 8192 + 1206 = 9398$$
> *(Kết quả duy nhất chính xác: 9398).*

> [!RECALLCHECKPOINT] id="rc-ch07-paging-translation" concept_id="ch07-paging-translation"
> **Nhiệm vụ thu hồi kín sách (Closed-book Recall):**
> 1. Trình bày công thức tính số trang $p$, độ dời $d$ và địa chỉ vật lý từ địa chỉ logic $L$ và kích thước trang $S$.
> 2. Tại sao cơ chế phân trang loại bỏ được phân mảnh ngoại nhưng vẫn còn phân mảnh nội?
> <!-- rubric -->
> - [0.5 điểm] Viết đúng công thức: $p = \lfloor L/S \rfloor$, $d = L \pmod S$, $\text{PA} = f \times S + d$.
> - [0.5 điểm] Giải thích đúng: loại bỏ phân mảnh ngoại vì trang nạp vào khung bất kỳ; còn phân mảnh nội vì trang cuối không dùng hết.

> [!TRANSFERPROBLEM] id="tp-ch07-paging-hex" concept_id="ch07-paging-translation"
> **Bài toán chuyển giao Hex trực tiếp (Transfer Challenge):**
> Một hệ thống phân trang sử dụng địa chỉ 32-bit với kích thước trang $4\text{KB} = 2^{12}\text{ bytes} = 0x1000$.
> CPU phát sinh địa chỉ logic dạng thập lục phân: `0x0041A7C8`.
> Bảng phân trang hiện tại ghi nhận trang tương ứng đang được ánh xạ vào khung trang vật lý có chỉ số $f = 0x000F2$.
> **Yêu cầu:** Xác định số trang $p$, độ dời $d$ và địa chỉ vật lý (dưới dạng Hex) mà không cần đổi sang hệ thập phân.
> <!-- solution -->
> **Lời giải chi tiết:**
> - Kích thước trang $4\text{KB} = 2^{12}\text{ bytes} \implies$ độ dời $d$ chiếm đúng $12\text{ bit} = 3\text{ chữ số Hex}$.
> - Phân tách địa chỉ logic `0x0041A7C8`:
>   - 3 chữ số Hex cuối cùng là độ dời: $d = \text{0x7C8}$.
>   - Các chữ số Hex còn lại là số trang: $p = \text{0x0041A}$.
> - Tra bảng trang với $p = \text{0x0041A} \implies$ Khung $f = \text{0x000F2}$.
> - Ghép trực tiếp khung $f$ và độ dời $d$:
>   $$\text{Địa chỉ vật lý} = [f \mid d] = \text{0x000F2} \times 0x1000 + 0x7C8 = \text{0x000F27C8}$$

---

### 7.5.4. Bộ nhớ đệm chuyển đổi nhanh (TLB — Translation Lookaside Buffer)
*(Căn cứ: Slide pp. 48–51; Đề cương mục 7.5.2; QBank `QBANK-CH07-08`)*

Trong hệ thống phân trang cơ bản, bảng phân trang được lưu trong RAM. Điều này dẫn đến **Vấn đề truy xuất bộ nhớ hai lần (Double Memory Access)**:
1. Lần 1: CPU phải đọc RAM để tra Bảng phân trang nhằm tìm khung $f$.
2. Lần 2: CPU đọc RAM lần nữa để lấy dữ liệu thực tế tại địa chỉ $(f, d)$.
$\implies$ Tốc độ truy xuất bộ nhớ của toàn bộ hệ thống bị chậm đi một nửa (50%)!

Để khắc phục, phần cứng trang bị một bộ nhớ đệm tốc độ cực cao gọi là **TLB (Translation Lookaside Buffer)**. TLB là bộ nhớ liên kết (Associative Memory), cho phép tra cứu song song đồng thời tất cả các mục chỉ trong 1 chu kỳ xung nhịp.

```
                    ĐỊA CHỈ LOGIC: [ p | d ]
                              │
               ┌──────────────┴──────────────┐
               │ Tra cứu TLB song song       │
               ▼                             ▼
       ┌───────────────┐             ┌───────────────┐
       │    TLB HIT    │             │   TLB MISS    │
       │ (Tìm thấy p)  │             │(Không thấy p) │
       └───────┬───────┘             └───────┬───────┘
               │ Lấy ngay f                  │ Đọc Page Table trong RAM
               ▼                             ▼
       ┌───────────────┐             ┌───────────────┐
       │   Đọc RAM     │             │ Nạp (p,f)     │
       │  lấy dữ liệu  │             │   vào TLB     │
       └───────────────┘             └───────┬───────┘
                                             ▼
                                     ┌───────────────┐
                                     │   Đọc RAM     │
                                     │  lấy dữ liệu  │
                                     └───────────────┘
```

> [!EXECUTIONTRACE]
> **Vết thực thi phần cứng qua 2 nhánh:**
> - **Nhánh 1: TLB Hit (Trúng TLB):**
>   CPU gửi $p \to$ TLB tìm thấy ngay mục $(p, f) \to$ lấy $f$ ghép với $d \to$ truy xuất RAM lấy dữ liệu.
>   *Tổng số lần truy xuất RAM:* **1 lần**.
> - **Nhánh 2: TLB Miss (Trượt TLB):**
>   CPU gửi $p \to$ TLB không tìm thấy $\to$ CPU phát tín hiệu truy xuất bảng phân trang trong RAM lấy $f \to$ ghi đè cập nhật mục $(p, f)$ vào TLB $\to$ truy xuất RAM lấy dữ liệu.
>   *Tổng số lần truy xuất RAM:* **2 lần**.

> [!WARNING]
> **Phân biệt bản chất: TLB Miss vs Page Fault [TIER_B_ENRICHMENT]:**
> - **TLB Miss (Trượt TLB):** Là sự kiện trượt bộ nhớ đệm phần cứng (Hardware Cache Miss) khi bản ghi chuyển đổi địa chỉ cho trang $p$ không có sẵn trong TLB. Quá trình tra cứu bảng trang (page-table walk) sau đó trong mô hình phân trang chuẩn sẽ đọc bảng trang trong RAM để lấy số khung $f$ và nạp vào TLB. (Trong hệ thống bộ nhớ ảo, nếu mục bảng trang chỉ ra trang chưa nạp vào RAM, sự kiện Page Fault mới được kích hoạt).
> - **Page Fault (Lỗi trang — Khảo sát chuyên sâu ở Chương 8):** Là ngoại lệ/bẫy phần cứng (Hardware Exception / Trap) được chuyển giao cho hệ điều hành xử lý khi CPU truy xuất vào một trang hợp lệ nhưng hiện chưa cư trú trong RAM vật lý (bit present/valid = 0). Hệ điều hành phải can thiệp điều khiển I/O để nạp trang từ thiết bị lưu trữ thứ cấp (backing store) vào RAM, có độ trễ lớn hơn đáng kể so với việc tra cứu bộ nhớ thông thường.

---

### 7.5.5. Thời gian truy xuất hiệu dụng (EAT — Effective Access Time)
*(Căn cứ: Slide pp. 52–54, 69; Đề cương mục 7.5.3; QBank `QBANK-CH07-08`, `12`, `16`, `17`, `18`)*

Gọi:
- $\alpha$: Tỷ lệ tìm thấy trong TLB (Hit ratio, $0 \le \alpha \le 1$).
- $\epsilon$: Thời gian tra cứu bảng TLB.
- $t_{\text{RAM}}$: Thời gian một chu kỳ truy xuất bộ nhớ RAM.

Thời gian truy xuất cho từng trường hợp:
- Khi TLB Hit: $T_{\text{Hit}} = \epsilon + t_{\text{RAM}}$.
- Khi TLB Miss: $T_{\text{Miss}} = \epsilon + 2 \times t_{\text{RAM}}$ (1 lần đọc bảng trang + 1 lần đọc dữ liệu).

Vì Hit và Miss là hai biến cố xung khắc toàn phần, thời gian truy xuất kỳ vọng trung bình EAT là:
$$\text{EAT} = \alpha \times T_{\text{Hit}} + (1 - \alpha) \times T_{\text{Miss}}$$
$$\text{EAT} = \alpha(\epsilon + t_{\text{RAM}}) + (1 - \alpha)(\epsilon + 2 t_{\text{RAM}})$$
$$\text{EAT} = \epsilon + (2 - \alpha) \times t_{\text{RAM}}$$

*(Nếu đề bài giả định thời gian tra TLB không đáng kể, $\epsilon \approx 0$: $\text{EAT} = (2 - \alpha) \times t_{\text{RAM}}$).*

> [!WORKEDEXAMPLE]
> **Bài toán mẫu QBANK-CH07-16 (Slide 69 tương tự):**
> Cho thời gian truy xuất RAM $t_{\text{RAM}} = 124\text{ns}$, thời gian tra cứu TLB $\epsilon = 34\text{ns}$, tỷ lệ trúng TLB $\alpha = 95\% = 0.95$.
> 
> **Lời giải:**
> - Thời gian truy xuất thông thường (không có TLB): $T_{\text{normal}} = 2 \times 124 = 248\text{ns}$.
> - Thời gian hiệu dụng khi có TLB:
>   $$\text{EAT} = 34 + (2 - 0.95) \times 124 = 34 + 1.05 \times 124 = 34 + 130.2 = 164.2\text{ns}$$

> [!WORKEDEXAMPLE]
> **Bài toán giải ngược tìm hit-ratio QBANK-CH07-18 (P80 docx):**
> *Đề bài:* Biết thời gian truy xuất trong bộ nhớ thường không sử dụng TLB là $250\text{ns}$. Thời gian tìm kiếm trong bảng TLB là $26\text{ns}$. Hỏi xác suất tìm thấy trong TLB bằng bao nhiêu nếu thời gian truy xuất hiệu dụng là $182\text{ns}$?
> 
> **Phân tích và giải chi tiết:**
> - Thời gian truy xuất thường không dùng TLB gồm 2 lần đọc RAM:
>   $$T_{\text{no-TLB}} = 2 \times t_{\text{RAM}} = 250\text{ns} \implies t_{\text{RAM}} = 125\text{ns}$$
> - Áp dụng công thức EAT:
>   $$\text{EAT} = \epsilon + (2 - \alpha) \times t_{\text{RAM}}$$
>   $$182 = 26 + (2 - \alpha) \times 125$$
>   $$156 = (2 - \alpha) \times 125 \implies 2 - \alpha = \frac{156}{125} = 1.248$$
>   $$\alpha = 2 - 1.248 = 0.752 = 75.2\%$$
> *(Kết quả: Xác suất tìm thấy trong TLB là $75.2\%$).*

> [!RECALLCHECKPOINT] id="rc-ch07-eat-derivation" concept_id="ch07-eat-calculation"
> **Nhiệm vụ thu hồi kín sách (Closed-book Recall):**
> 1. Viết công thức tổng quát tính EAT khi có xét đến thời gian tra TLB $\epsilon$ và thời gian RAM $t_{\text{RAM}}$.
> 2. Vì sao trong trường hợp TLB Miss, số lần truy xuất RAM lại là 2 lần?
> <!-- rubric -->
> - [0.5 điểm] Viết đúng công thức: $\text{EAT} = \epsilon + (2 - \alpha) \times t_{\text{RAM}}$ (hoặc triển khai qua hai nhánh Hit/Miss).
> - [0.5 điểm] Giải thích rõ: 1 lần đọc bảng phân trang trong RAM để lấy frame number, và 1 lần đọc ô nhớ thực sự để lấy dữ liệu.

---

## 4. Cấu trúc bảng trang nâng cao

### 7.5.6. Bảng trang phân cấp (Hierarchical Paging)
*(Căn cứ: Slide pp. 55–56, 70; Đề cương mục 7.5.4; QBank `QBANK-CH07-13`, `14`)*

Trên các kiến trúc hiện đại có không gian địa chỉ lớn (ví dụ 32-bit):
- Với trang $4\text{KB} = 2^{12}\text{ bytes}$, không gian 32-bit có tới $2^{20} \approx 1\text{ triệu trang}$.
- Nếu mỗi mục bảng trang chiếm 4 bytes $\implies$ Bảng phân trang chiếm $4\text{MB}$ bộ nhớ vật lý liên tục cho **mỗi tiến trình**!
- Giải pháp: **Phân trang cho chính bảng phân trang** (Bảng trang 2 cấp - Two-Level Page Table).

```
ĐỊA CHỈ LOGIC 32-BIT (Phân trang 2 cấp):
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│     p1 (Outer Page)     │     p2 (Inner Page)     │       d (Offset)        │
│          9 bit          │         11 bit          │         12 bit          │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

> [!WORKEDEXAMPLE]
> **Bài toán mẫu Slide 70 & QBANK-CH07-13:**
> Một máy tính có địa chỉ 32-bit, sử dụng bảng trang 2 cấp. Trường địa chỉ cấp 1 có 9 bit, cấp 2 có 11 bit, phần còn lại là độ dời.
> 
> **Lời giải:**
> 1. Số bit của độ dời: $d = 32 - (9 + 11) = 12\text{ bit}$.
> 2. Kích thước một trang: $S = 2^{12}\text{ bytes} = 4096\text{ bytes} = 4\text{KB}$.
> 3. Tổng số trang ảo tối đa: Số bit chỉ số trang $= 9 + 11 = 20\text{ bit} \implies 2^{20} = 1,048,576\text{ trang}$.
> 4. Bảng trang ngoài (Cấp 1) có $2^9 = 512\text{ mục}$. Mỗi bảng trang Cấp 2 có $2^{11} = 2048\text{ mục}$.

---

### 7.5.7. Bảng trang băm và Bảng trang nghịch đảo
*(Căn cứ: Slide pp. 57–58)*

```
+───────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| Cấu trúc bảng trang   | Nguyên lý tổ chức                       | Ưu điểm & Nhược điểm chính           |
+───────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| 1. Bảng trang phân cấp| Phân trang nhiều tầng (2 cấp, 3 cấp).   | Tiết kiệm RAM cho bảng trang, nhưng  |
| (Hierarchical)        | Chỉ nạp bảng cấp 2 khi tiến trình dùng. | Miss tốn $k+1$ lần đọc RAM.          |
+───────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| 2. Bảng trang băm     | Dùng hàm băm băm số trang $p$. Xử lý    | Thích hợp cho không gian địa chỉ     |
| (Hashed Page Table)   | xung đột bằng danh sách liên kết.       | lớn (> 32 bit, 64-bit).              |
+───────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
| 3. Bảng trang nghịch  | Chỉ có số mục bằng số KHUNG TRANG trong | Tiết kiệm RAM tối đa vì bảng không   |
| đảo (Inverted)        | RAM. Mỗi mục lưu `(PID, Page Number)`.  | phụ thuộc số trang ảo; nhưng tra cứu |
|                       |                                         | rất chậm (phải quét hoặc dùng băm).  |
+───────────────────────+─────────────────────────────────────────+──────────────────────────────────────+
```

---

### 7.5.8. Bảo vệ bộ nhớ và Chia sẻ trang
*(Căn cứ: Slide pp. 59–62; Đề cương mục 7.5.5; QBank `QBANK-CH07-01`)*

- **Bit Hợp lệ / Bất hợp lệ (Valid / Invalid Bit):** Mỗi mục trong bảng phân trang có một bit kiểm soát.
  - `Valid (1)`: Trang thuộc không gian địa chỉ hợp lệ của tiến trình và đang nằm trong RAM.
  - `Invalid (0)`: Trang không thuộc không gian địa chỉ của tiến trình, hoặc chưa được cấp phát $\implies$ phát sinh lỗi truy cập.
- **Các bit quyền (Protection Bits):** Read-only, Read-Write, Execute. Nếu tiến trình cố tình ghi vào vùng chỉ đọc (ví dụ vùng mã lệnh code segment), phần cứng kích hoạt bẫy ngắt bảo vệ.
- **Chia sẻ trang (Shared Pages):** Cơ chế chia sẻ mã tái nhập (Reentrant Code / Pure Code). Mã tái nhập là mã không bao giờ tự sửa đổi chính nó trong khi chạy (ví dụ: trình biên dịch C, trình soạn thảo, thư viện chuẩn). Nhiều tiến trình cùng trỏ các mục bảng phân trang của mình vào **cùng một khung trang vật lý** chỉ đọc, trong khi dữ liệu riêng của từng tiến trình nằm ở các khung trang độc lập.

---

## 5. Swapping

### 7.6. Cơ chế hoán vị bộ nhớ (Swapping)
*(Căn cứ: Slide pp. 63–66; Đề cương mục 7.6; QBank `QBANK-CH07-09`)*

Khi tổng nhu cầu bộ nhớ của tất cả các tiến trình trong hệ thống vượt quá dung lượng RAM vật lý hiện có, hệ điều hành áp dụng kỹ thuật **Hoán vị (Swapping)**:
- **Swap-out:** Chuyển toàn bộ một tiến trình tạm thời không hoạt động (đang ở trạng thái `WAITING` hoặc độ ưu tiên thấp) từ RAM ra vùng lưu trữ thứ cấp trên đĩa gọi là **Backing Store (Swap space)**.
- **Swap-in:** Nạp lại tiến trình từ Backing Store vào RAM khi tiến trình sẵn sàng thực thi (`READY`).

```
                    ┌────────────────────────┐
                    │      BỘ NHỚ RAM        │
                    │ ┌────────────────────┐ │
                    │ │  Tiến trình P1     │ │
                    │ └────────────────────┘ │
                    │        │ Swap-out      │
                    │        ▼               │
                    └────────┼───────────────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │     BACKING STORE      │
                    │      (Ổ đĩa cứng)      │
                    │ ┌────────────────────┐ │
                    │ │  Tiến trình P1     │ │
                    │ └────────────────────┘ │
                    │        │ Swap-in       │
                    │        ▼               │
                    └────────┼───────────────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │      BỘ NHỚ RAM        │
                    │ ┌────────────────────┐ │
                    │ │  Tiến trình P1     │ │
                    │ └────────────────────┘ │
                    └────────────────────────┘
```

#### Phân tích độ trễ I/O của Swapping
Chi phí thời gian chuyển đổi ngữ cảnh phát sinh do hoán vị chủ yếu nằm ở **thời gian truyền dữ liệu (Transfer time)** qua bus đĩa, chứ không phải thời gian tìm kiếm (Seek time):
- Giả sử tiến trình có dung lượng $100\text{MB}$.
- Ổ đĩa có tốc độ truyền dữ liệu thực tế $50\text{MB/s}$, thời gian tìm kiếm trung bình $8\text{ms}$.
- Thời gian truyền: $100\text{MB} / 50\text{MB/s} = 2\text{ giây} = 2000\text{ms}$.
- Tổng thời gian Swap-out: $8\text{ms} + 2000\text{ms} = 2008\text{ms}$.
- Nếu hoán vị 2 chiều (Swap-out tiến trình cũ và Swap-in tiến trình mới): tốn hơn **4 giây**!
- *Kết luận sư phạm:* Hoán vị toàn bộ tiến trình có độ trễ quá lớn. Điều này lý giải tại sao các hệ điều hành hiện đại chuyển sang cơ chế **Hoán vị từng trang (Paging Swap / Virtual Memory)** trong Chương 8.

> [!NOTE]
> **Swapping trên Hệ điều hành di động (iOS / Android) [TIER_B_ENRICHMENT]:**
> Cả Android và iOS đều không sử dụng kỹ thuật Swapping truyền thống ra bộ nhớ flash vì:
> 1. Bộ nhớ Flash (eMMC / UFS) có giới hạn số lần ghi (Write Endurance); swapping liên tục sẽ làm chai và hỏng chip nhớ rất nhanh.
> 2. Băng thông giữa CPU và Flash trên thiết bị di động bị giới hạn công suất tiêu thụ điện.
> Thay vào đó, khi thiếu RAM, Android dùng cơ chế *Low Memory Killer (LMK)* để kết liễu các tiến trình nền ít dùng; còn iOS yêu cầu ứng dụng tự giải phóng bộ nhớ (Free up cached objects), nếu không sẽ bị hủy cưỡng bức.

> [!RECALLCHECKPOINT] id="rc-ch07-swapping" concept_id="ch07-swapping"
> **Nhiệm vụ thu hồi kín sách (Closed-book Recall):**
> 1. Trình bày mục đích và cơ chế cơ bản của kỹ thuật Hoán vị (Swapping).
> 2. Trong tổng thời gian hoán vị một tiến trình, thành phần thời gian nào chiếm tỷ trọng áp đảo?
> <!-- rubric -->
> - [0.5 điểm] Nêu rõ chuyển tiến trình không hoạt động ra đĩa (Backing Store) và nạp lại khi cần chạy để tăng mức độ đa chương.
> - [0.5 điểm] Khẳng định thời gian truyền dữ liệu (Transfer time) chiếm tỷ trọng áp đảo (hơn 99%) so với thời gian tìm kiếm (Seek time).

---

## 6. Bài tập Slide

### 7.7. Tuyển tập bài tập Slide chính thức
*(Căn cứ: Slide pp. 67–71)*

Phần này tổng hợp 5 bài tập thực hành nằm tại phần kết thúc của Slide chính thức UIT (`#Week09-Chapter7 2024.pdf`), giúp người học đối soát toàn diện kỹ năng trước khi làm ngân hàng câu hỏi tự luận.

#### Bài 1 (Slide 67): Cấp phát liên tục với 4 thuật toán Fit
- Cho 4 phân vùng: $600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$.
- Cấp phát lần lượt cho: $P_1(212\text{KB}), P_2(417\text{KB}), P_3(112\text{KB}), P_4(426\text{KB})$.
- *Kết quả tóm tắt:* Chỉ có **Best Fit** nạp được cả 4 tiến trình. First Fit, Next Fit và Worst Fit đều để $P_4$ phải chờ. Lời giải chi tiết từng bước xem tại mục 7.4.3.

#### Bài 2 (Slide 68): Xác định số bit địa chỉ
- Hệ thống có 12 trang logic, kích thước trang $2\text{KB}$, bộ nhớ vật lý 32 khung.
- Độ dời: $d = \log_2(2048) = 11\text{ bit}$.
- Số bit trang logic: $p = \lceil \log_2(12) \rceil = 4\text{ bit} \implies$ Địa chỉ logic: $4 + 11 = 15\text{ bit}$.
- Số bit khung vật lý: $f = \log_2(32) = 5\text{ bit} \implies$ Địa chỉ vật lý: $5 + 11 = 16\text{ bit}$.

#### Bài 3 (Slide 69): Tính EAT cơ bản
- Thời gian RAM $200\text{ns}$, bảng trang trong RAM. Không có TLB: $2 \times 200 = 400\text{ns}$.
- Có TLB với hit-ratio $75\%$, tra TLB $\approx 0$:
  $$\text{EAT} = 0.75 \times 200 + 0.25 \times 400 = 150 + 100 = 250\text{ns}$$

#### Bài 4 (Slide 70): Bảng phân trang 2 cấp
- Địa chỉ 32-bit, cấp 1 có 9 bit, cấp 2 có 11 bit.
- Offset $d = 32 - (9 + 11) = 12\text{ bit} \implies$ Kích thước trang $= 2^{12} = 4\text{KB}$.
- Bảng cấp 1 có $2^9 = 512\text{ mục}$. Mỗi bảng cấp 2 có $2^{11} = 2048\text{ mục}$. Tổng số trang ảo tối đa là $2^{20} = 1,048,576\text{ trang}$.

#### Bài 5 (Slide 71): Phân tích địa chỉ ảo 4 trường
- Địa chỉ ảo 32-bit gồm 4 trường $a, b, c, d$ (3 cấp bảng trang và 1 offset).
- Số lượng trang ảo phụ thuộc vào $a, b, c$ ($2^{a+b+c}$ trang), hoặc tương đương phụ thuộc vào kích thước trang do $d$ quy định ($2^{32-d}$ trang).

---

## 7. Thử thách giải trình 3 phút (Teach-Back Challenge)

Hãy thử gấp sách vở và giải thích lưu loát 9 câu hỏi then chốt sau cho một người bạn:

1. **Vì sao địa chỉ logic và địa chỉ vật lý lại tách biệt nhau?**
2. **Cơ chế phần cứng MMU thực hiện bảo vệ và dịch địa chỉ như thế nào thông qua cặp Base/Limit?**
3. **Bản chất của phân mảnh nội và phân mảnh ngoại khác nhau ở điểm nào?**
4. **Bốn thuật toán First Fit, Best Fit, Next Fit, Worst Fit khác nhau cơ bản ở chiến lược tìm kiếm ra sao?**
5. **Vì sao cơ chế phân trang loại bỏ triệt để phân mảnh ngoại?**
6. **Bảng phân trang chuyển đổi $(p, d)$ thành $(f, d)$ như thế nào và tại sao độ dời $d$ không đổi?**
7. **Bộ đệm TLB giải quyết bài toán gì và luồng phần cứng khi Hit/Miss diễn ra như thế nào?**
8. **Dẫn xuất công thức tính Thời gian truy xuất hiệu dụng (EAT) từ hai biến cố Hit và Miss?**
9. **Tại sao hoán vị toàn bộ tiến trình (Swapping) lại tốn kém độ trễ I/O nghiêm trọng?**

---

## 8. Hướng dẫn ôn tập & Điểm ôn tập ngắt quãng (Spaced Review Hook)

> [!REVIEWHOOK]
> **Kế hoạch ôn tập ngắt quãng khuyến nghị:**
> - **Lần 1 (Ngay sau khi học):** Hoàn thành toàn bộ các trạm thu hồi kín sách (Recall Checkpoints) và bài toán chuyển giao (Transfer Problems) trên trang này.
> - **Lần 2 (Sau 1 ngày):** Mở [Ngân hàng tự luận Chương 7](questions/subjective/ch07.html) để làm 20 câu hỏi nguồn chính thức UIT.
> - **Lần 3 (Theo thông báo hàng đợi):** Kích hoạt chế độ **Ôn tập (Review Mode)** trên thanh công cụ hoặc truy cập [Hàng đợi ôn tập toàn môn (Review Hub)](../review/index.html) để ôn lại các thẻ nhớ và bài toán đến hạn theo thuật toán thích ứng SM-2.

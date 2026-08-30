---
id: "theory-ch01-overview"
title: "Chương 1: Tổng quan về Hệ điều hành & Kiến trúc Máy tính"
book: "theory"
chapter: 1
order: 1
slug: "ch01-overview"
summary: "Định nghĩa hệ điều hành, kiến trúc phân tầng 4 lớp, cơ chế ngắt phần cứng và ngoại lệ, phân cấp bộ nhớ lưu trữ, kiến trúc đa bộ xử lý và gom cụm, chế độ hoạt động kép Dual-Mode, lệnh đặc quyền và 4 môi trường tính toán."
prerequisites: []
related:
  - "theory-ch02-structure"
  - "theory-ch03-process"
  - "sub-ch01"
  - "glossary-dual-mode"
  - "glossary-interrupt"
exam_relevance:
  midterm_weight: "20%"
  final_weight: "5%"
  frequent_topics:
    - "Phân biệt User Mode và Kernel Mode"
    - "Cơ chế xử lý ngắt, Bảng véc-tơ ngắt (IVT) và ISR"
    - "Phân cấp hệ thống lưu trữ (Storage Hierarchy) và nguyên lý Caching"
    - "Phân loại Lệnh đặc quyền vs Lệnh không đặc quyền"
    - "So sánh 4 môi trường tính toán: Đơn chương, Đa chương, Chia sẻ thời gian, Thời gian thực"
sources:
  - "SRC-A01 (Week01-Chapter1 2024.pdf)"
  - "SRC-A10 (Week08-Midterm Review.pdf)"
  - "SRC-B01 (Silberschatz Ch1)"
last_updated: "2026-08-30"
---

# Chương 1: Tổng quan về Hệ điều hành & Kiến trúc Máy tính

## 1. Bản chất & Vai trò của Hệ điều hành

Một hệ thống máy tính hiện đại là một tổ hợp phức tạp gồm phần cứng xử lý (CPU), bộ nhớ (RAM), các thiết bị ngoại vi và các chương trình ứng dụng. Nếu không có một lớp phần mềm trung gian điều phối, mỗi ứng dụng người dùng sẽ phải tự quản lý từng xung nhịp đồng hồ, tự lập trình giao tiếp với đĩa cứng, và trực tiếp tranh chấp tài nguyên bộ nhớ với các chương trình khác.

Hệ điều hành (Operating System - OS) là chương trình đóng vai trò làm trung gian giữa người sử dụng máy tính và phần cứng máy tính.

```
+-------------------------------------------------------------+
|                      Người Dùng (Users)                     |
+-------------------------------------------------------------+
|        Chương Trình Ứng Dụng (Compilers, Browsers, Apps)     |
+-------------------------------------------------------------+
|        Chương Trình Hệ Thống (Shells, GUI, System Daemons)  |
+-------------------------------------------------------------+
|               HỆ ĐIỀU HÀNH (Kernel & Core Services)          |
+-------------------------------------------------------------+
|          Phần Cứng Máy Tính (CPU, Memory, I/O Devices)       |
+-------------------------------------------------------------+
```

### Hai Góc Nhìn Cốt Lõi về Hệ Điều Hành
1. **Góc nhìn người dùng (User View):** Người dùng quan tâm đến sự tiện lợi, dễ sử dụng, hiệu năng đáp ứng nhanh và khả năng bảo mật thông tin cá nhân.
2. **Góc nhìn hệ thống (System View):**
   - **Bộ phân phối tài nguyên (Resource Allocator):** Quản lý CPU time, không gian RAM, không gian lưu trữ và các thiết bị I/O sao cho công bằng và hiệu quả.
   - **Chương trình kiểm soát (Control Program):** Kiểm soát quá trình thực thi các chương trình ứng dụng nhằm ngăn ngừa lỗi và việc sử dụng máy tính không đúng mục đích.

> [!CHARACTERISTICS]
> ### Đặc tính: Hệ Điều Hành (Operating System)
> - **Mục đích:** Cung cấp môi trường thuận tiện để người dùng chạy ứng dụng và tối ưu hóa hiệu suất khai thác phần cứng.
> - **Cơ chế cốt lõi:** Nhân hệ điều hành (Kernel) luôn thường trực trong RAM từ khi máy khởi động đến khi tắt.
> - **Cam kết (Guarantees):** Cách ly lỗi phần mềm, phân bổ tài nguyên công bằng, bảo vệ hệ thống khỏi các hành vi phá hoại.
> - **Không cam kết (Non-guarantees):** Không tự động sửa lỗi logic bên trong mã nguồn của chương trình ứng dụng.

---

## 2. Hoạt Động Khởi Động & Cơ Chế Ngắt (Interrupts)

### 2.1. Quá trình Khởi động (Bootstrap Process)
Khi máy tính được cấp nguồn hoặc khởi động lại (Reboot):
1. CPU nạp chương trình khởi động nhỏ gọi là **Bootstrap Program** (thường lưu trữ trong ROM hoặc EEPROM, được gọi là Firmware/BIOS/UEFI).
2. Bootstrap Program khởi tạo tất cả các thành phần phần cứng (CPU registers, Device controllers, RAM).
3. Bootstrap Program định vị và nạp **Kernel của Hệ điều hành** từ đĩa cứng vào bộ nhớ chính (RAM).
4. Kernel khởi tạo các cấu trúc dữ liệu nội tại, kích hoạt tiến trình gốc (`init` hoặc `systemd` trên Linux) và chuyển sang trạng thái chờ sự kiện.

### 2.2. Cơ chế Ngắt: Trái tim điều khiển của Hệ điều hành
Hệ điều hành hiện đại là một hệ thống **hoạt động theo sự kiện ngắt (Interrupt-driven)**. Nếu không có tiến trình thực thi, không có thiết bị I/O yêu cầu và không có ngắt xảy ra, CPU sẽ rơi vào trạng thái chờ (Idle).

```
                      +-------------------+
                      | Tín hiệu Ngắt     |
                      +---------+---------+
                                |
                                v
               +---------------------------------+
               | 1. CPU tạm dừng lệnh hiện tại   |
               +----------------+----------------+
                                |
                                v
               +---------------------------------+
               | 2. Lưu trạng thái (PC, Regs)    |
               +----------------+----------------+
                                |
                                v
               +---------------------------------+
               | 3. Tra cứu Bảng véc-tơ (IVT)     |
               +----------------+----------------+
                                |
                                v
               +---------------------------------+
               | 4. Nhảy đến nạp thực thi ISR    |
               +----------------+----------------+
                                |
                                v
               +---------------------------------+
               | 5. Khôi phục PC & Registers     |
               +---------------------------------+
```

> [!NOTE]
> ### Phân biệt Ngắt Phần Cứng và Bẫy Ngắt (Trap / Exception)
> - **Ngắt phần cứng (Hardware Interrupt):** Tín hiệu điện tử bất đồng bộ do thiết bị ngoại vi (bàn phím, chuột, card mạng, đĩa cứng) gửi qua bus hệ thống đến CPU.
> - **Bẫy ngắt / Ngoại lệ (Trap / Software Interrupt / Exception):** Tín hiệu đồng bộ sinh ra trực tiếp bởi CPU do lỗi phần mềm (chia cho 0, truy xuất bộ nhớ không hợp lệ) hoặc do chương trình chủ động thực hiện lời gọi hệ thống [[system-call]].

---

## 3. Phân Cấp Hệ Thống Lưu Trữ (Storage Hierarchy)

Hệ thống lưu trữ trong máy tính được thiết kế theo cấu trúc kim tự tháp dựa trên **3 tiêu chí cốt lõi**:
1. **Tốc độ truy xuất (Speed / Access time)**
2. **Dung lượng lưu trữ (Capacity / Size)**
3. **Giá thành trên một bit (Cost per bit)**

```
             /\
            /  \     Thanh ghi CPU (Registers) - < 1 ns, Vài KB
           /----\
          / Cache\   Bộ đệm Cache (L1, L2, L3) - 1-10 ns, Vài MB
         /--------\
        / Bộ nhớ   \ Bộ nhớ chính (RAM) - 50-100 ns, Vài GB
       /  chính     \
      /--------------\
     / Ổ đĩa thể rắn  \ Ổ SSD (NVM) - 10-100 us, Hàng trăm GB
    /------------------\
   /   Ổ đĩa từ tính    \ Ổ đĩa cứng (HDD) - 5-10 ms, Hàng TB
  /----------------------\
 /  Lưu trữ quang / Băng  \ Băng từ (Tape) - Giây/Phút, Cực lớn
/--------------------------\
```

### Nguyên lý Cục bộ (Locality of Reference) & Caching
- **Cục bộ không gian (Spatial Locality):** Nếu một ô nhớ được truy xuất, các ô nhớ liền kề có xác suất cao sẽ được truy xuất tiếp theo.
- **Cục bộ thời gian (Temporal Locality):** Nếu một ô nhớ vừa được truy xuất, nó có khả năng cao sẽ được truy xuất lại trong tương lai gần.
- **Caching:** Kỹ thuật sao chép dữ liệu từ tầng lưu trữ chậm sang tầng lưu trữ nhanh hơn tạm thời để giảm thiểu thời gian chờ của CPU.

---

## 4. Chế Độ Hoạt Động Kép (Dual-Mode Operation)

Để ngăn chặn các chương trình người dùng phá hoại hệ điều hành hoặc xâm phạm không gian nhớ của người dùng khác, phần cứng CPU cung cấp cơ chế **Chế độ hoạt động kép (Dual-Mode)**:

1. **User Mode (Chế độ người dùng - Mode bit = 1):** Mã lệnh ứng dụng thực thi trong không gian bị hạn chế, không được phép thực thi trực tiếp các chỉ thị nguy hiểm.
2. **Kernel Mode (Chế độ nhân / Supervisor / Privileged - Mode bit = 0):** Hệ điều hành thực thi với toàn quyền truy xuất phần cứng và bộ nhớ.

```
       USER MODE (Mode bit = 1)                 KERNEL MODE (Mode bit = 0)
+------------------------------------+   +------------------------------------+
| Ứng dụng gọi System Call           |   |                                    |
| (ví dụ: open(), read(), write())   |   |                                    |
|                                    |   |                                    |
| Trap / Syscall Instruction --------+-->| Chuyển Mode bit 1 -> 0             |
|                                    |   | Tra cứu bảng véc-tơ System Call    |
|                                    |   | Thực thi hàm phục vụ nhân          |
| Nhận kết quả và tiếp tục <---------+---| Chuyển Mode bit 0 -> 1             |
+------------------------------------+   +------------------------------------+
```

### Lệnh Đặc Quyền (Privileged Instructions)
Các chỉ thị phần cứng có khả năng gây nguy hại đến an toàn hệ thống chỉ được phép thực thi trong Kernel Mode:
- Chỉ thị bật/tắt ngắt CPU (`cli`, `sti` trên x86).
- Chỉ thị thay đổi giá trị `Mode bit`.
- Chỉ thị thao tác trực tiếp với các cổng vào/ra phần cứng (I/O instructions: `in`, `out`).
- Chỉ thị nạp lại thanh ghi quản lý bộ nhớ (`CR3`, Base/Limit registers).
- Chỉ thị dừng hoạt động của CPU (`hlt`).

> [!WARNING]
> Nếu một chương trình chạy ở User Mode cố tình thực thi một lệnh đặc quyền, phần cứng CPU sẽ lập tức coi đó là lệnh bất hợp pháp và kích hoạt một **Trap (Exception)** báo về cho Kernel để hủy tiến trình vi phạm (Illegal Instruction Exception / Segmentation Fault).

---

## 5. Các Môi Trường Tính Toán (Computing Environments)

| Môi Trường | Cơ Chế Điều Phối | Mức Độ Khai Thác CPU | Khả Năng Tương Tác | Trọng Tâm Thiết Kế |
| :--- | :--- | :--- | :--- | :--- |
| **Đơn chương (Uniprogramming)** | Mỗi thời điểm chỉ nạp và chạy 1 chương trình duy nhất. Khi chương trình chờ I/O, CPU bị rảnh rỗi hoàn toàn. | Rất thấp ($\le 20\%$) | Không hỗ trợ đa nhiệm | Đơn giản, dùng cho các vi điều khiển cũ hoặc MS-DOS. |
| **Đa chương (Multiprogramming)** | Nạp đồng thời nhiều tiến trình vào RAM. Khi tiến trình hiện tại chờ I/O, CPU lập tức chuyển sang thực thi tiến trình khác. | Rất cao ($80\% - 95\%$) | Thấp (chủ yếu xử lý hàng loạt - Batch systems) | Tối đa hóa hiệu suất sử dụng CPU (CPU Utilization). |
| **Chia sẻ thời gian / Đa nhiệm (Time-Sharing / Multitasking)** | CPU phân chia thời gian thành các lượng tử thời gian (Time Quantum) cực nhỏ và luân chuyển liên tục qua ngắt đồng hồ (Timer). | Cao | Rất cao (Tương tác thời gian thực với người dùng) | Tối thiểu hóa thời gian đáp ứng (Response Time $< 1$s). |
| **Thời gian thực (Real-Time)** | Xử lý dữ liệu và phản hồi trong các ràng buộc thời gian nghiêm ngặt (Deadlines). Gồm *Hard Real-Time* (bắt buộc tuyệt đối) và *Soft Real-Time* (ưu tiên cao). | Trung bình | Tùy biến theo sự kiện cảm biến/điều khiển | Đảm bảo tính tất định và độ trễ phản hồi (Deterministic Latency). |

---

## 6. Câu Hỏi Tự Luyện & Liên Kết Tri Thức

- Xem toàn bộ câu hỏi tự luận có barem chấm tại: [[ch01-subjective]]
- Luyện tập flashcard thuật ngữ: [[ch01-flashcards]]
- Chuyển sang chương tiếp theo: [[theory-ch02-structure]]

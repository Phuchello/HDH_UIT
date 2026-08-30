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
  - "sub-ch01"
  - "glossary-terms"
exam_relevance:
  frequent_topics:
    - "Phân biệt User Mode và Kernel Mode"
    - "Cơ chế xử lý ngắt, Bảng véc-tơ ngắt (IVT) và ISR"
    - "Phân cấp hệ thống lưu trữ (Storage Hierarchy) và nguyên lý Caching"
    - "Phân loại Lệnh đặc quyền vs Lệnh không đặc quyền"
    - "So sánh 4 môi trường tính toán: Đơn chương, Đa chương, Chia sẻ thời gian, Thời gian thực"
sources:
  - "UIT-SLIDE-CH01-2024"
  - "UIT-SLIDE-MIDTERM-REVIEW-2024"
  - "SILBERSCHATZ-OSC10"
last_updated: "2026-08-30"
---

# Chương 1: Tổng quan về Hệ điều hành & Kiến trúc Máy tính

## 1. Bản chất & Vai trò của Hệ điều hành

Một hệ thống máy tính hiện đại là một tổ hợp gồm phần cứng xử lý (CPU), bộ nhớ (RAM), các thiết bị ngoại vi và các chương trình ứng dụng. Nếu không có một lớp phần mềm trung gian điều phối, mỗi ứng dụng người dùng sẽ phải tự quản lý việc giao tiếp với phần cứng và trực tiếp tranh chấp tài nguyên bộ nhớ với các chương trình khác.

Hệ điều hành (Operating System - OS) là chương trình đóng vai trò làm trung gian giữa người sử dụng máy tính và phần cứng máy tính.

```
+-------------------------------------------------------------+
|                      Người Dùng (Users)                     |
+-------------------------------------------------------------+
|        Chương Trình Ứng Dụng (Compilers, Browsers, Apps)     |
+-------------------------------------------------------------+
|        Chương Trình Hệ Thống (Shells, System Daemons)       |
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
> - **Cơ chế cốt lõi:** Lõi hệ điều hành (Kernel) thường trực trong bộ nhớ chính để điều phối và quản lý tài nguyên (trong các hệ thống hiện đại, một số thành phần không trọng yếu của kernel có thể được tải động qua kernel modules hoặc nạp theo nhu cầu).
> - **Cam kết (Guarantees):** Phân tách không gian địa chỉ ứng dụng, điều phối tài nguyên có kiểm soát.
> - **Không cam kết (Non-guarantees):** Không tự động sửa chữa các lỗi logic bên trong mã nguồn ứng dụng của người dùng.

---

## 2. Hoạt Động Khởi Động & Cơ Chế Ngắt (Interrupts)

### 2.1. Quá trình Khởi động (Bootstrap Process)
Khi máy tính được cấp nguồn hoặc khởi động lại (Reboot):
1. CPU nạp chương trình khởi động nhỏ gọi là **Bootstrap Program** (thường lưu trữ trong ROM hoặc EEPROM, được gọi là Firmware/BIOS/UEFI).
2. Bootstrap Program kiểm tra và khởi tạo các thành phần phần cứng cơ bản.
3. Bootstrap Program định vị và nạp **Kernel của Hệ điều hành** từ đĩa cứng vào bộ nhớ chính (RAM).
4. Kernel khởi tạo các cấu trúc dữ liệu nội tại, kích hoạt tiến trình gốc (`init` hoặc `systemd` trên Linux) và chuyển sang trạng thái sẵn sàng phục vụ sự kiện.

### 2.2. Cơ chế Ngắt: Trái tim điều khiển của Hệ điều hành
Hệ điều hành hiện đại là một hệ thống **hoạt động theo sự kiện ngắt (Interrupt-driven)**. Khi không có tiến trình thực thi và không có thiết bị I/O yêu cầu, CPU thường ở trạng thái chờ (Idle) để tiết kiệm năng lượng.

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
               +----------------+----------------+
```

> [!NOTE]
> ### Phân biệt Ngắt Phần Cứng và Bẫy Ngắt (Trap / Exception)
> - **Ngắt phần cứng (Hardware Interrupt):** Tín hiệu điện tử bất đồng bộ do thiết bị ngoại vi (bàn phím, chuột, card mạng, đĩa cứng) gửi qua bus hệ thống đến CPU.
> - **Bẫy ngắt / Ngoại lệ (Trap / Software Interrupt / Exception):** Tín hiệu đồng bộ sinh ra trực tiếp bởi CPU do điều kiện phát sinh từ lệnh đang chạy (lỗi chia cho 0, truy xuất bộ nhớ ngoài giới hạn) hoặc do chương trình chủ động thực hiện Lời gọi hệ thống (System Call).

---

## 3. Phân Cấp Hệ Thống Lưu Trữ (Storage Hierarchy)

Hệ thống lưu trữ trong máy tính được thiết kế theo cấu trúc phân cấp dựa trên **3 tiêu chí cốt lõi**:
1. **Tốc độ truy xuất (Speed / Access time)**
2. **Dung lượng lưu trữ (Capacity / Size)**
3. **Giá thành trên một bit (Cost per bit)**

```
             /\
            /  \     Thanh ghi CPU (Registers) - Nhanh nhất, Dung lượng nhỏ
           /----\
          / Cache\   Bộ đệm Cache (L1, L2, L3) - Rất nhanh
         /--------\
        / Bộ nhớ   \ Bộ nhớ chính (RAM) - Truy xuất ngẫu nhiên, dễ bay hơi
       /  chính     \
      /--------------\
     / Ổ đĩa thể rắn  \ Ổ SSD (NVM) - Bất biến, nhanh hơn đĩa từ
    /------------------\
   /   Ổ đĩa từ tính    \ Ổ đĩa cứng (HDD) - Dung lượng lớn, chi phí thấp
  /----------------------\
 /  Lưu trữ quang / Băng  \ Băng từ (Tape) - Lưu trữ lưu trữ dài hạn
/--------------------------\
```

### Nguyên lý Cục bộ (Locality of Reference) & Caching
- **Cục bộ không gian (Spatial Locality):** Nếu một ô nhớ được truy xuất, các ô nhớ liền kề có xác suất cao sẽ được truy xuất tiếp theo.
- **Cục bộ thời gian (Temporal Locality):** Nếu một ô nhớ vừa được truy xuất, nó có khả năng cao sẽ được truy xuất lại trong tương lai gần.
- **Caching:** Kỹ thuật sao chép dữ liệu từ tầng lưu trữ chậm sang tầng lưu trữ nhanh hơn tạm thời để giảm thiểu độ trễ truy cập của CPU.

---

## 4. Chế Độ Hoạt Động Kép (Dual-Mode Operation)

Để ngăn chặn các chương trình người dùng gây mất ổn định cho hệ điều hành hoặc can thiệp trái phép vào không gian nhớ của tiến trình khác, phần cứng CPU cung cấp cơ chế **Chế độ hoạt động kép (Dual-Mode)**:

1. **User Mode (Chế độ người dùng):** Mã lệnh ứng dụng thực thi trong không gian bị hạn chế, không được phép thực thi trực tiếp các chỉ thị nhạy cảm.
2. **Kernel Mode (Chế độ nhân / Supervisor / Privileged):** Hệ điều hành thực thi với toàn quyền truy xuất phần cứng và bộ nhớ.

*Lưu ý:* Trong mô hình quy ước giảng dạy của môn học (theo kiến trúc x86 quy chuẩn), trạng thái này thường được điều khiển qua `Mode bit` (quy ước: `0` là Kernel Mode, `1` là User Mode).

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
Các chỉ thị phần cứng có khả năng thay đổi cấu hình bảo vệ hoặc can thiệp sâu vào tài nguyên hệ thống chỉ được phép thực thi trong Kernel Mode:
- Chỉ thị bật/tắt ngắt CPU (`cli`, `sti` trên x86).
- Chỉ thị thay đổi giá trị của bit trạng thái chế độ CPU (`Mode bit`).
- Chỉ thị thao tác trực tiếp với các cổng vào/ra phần cứng (I/O instructions: `in`, `out`).
- Chỉ thị nạp lại thanh ghi quản lý bộ nhớ (`CR3`, Base/Limit registers).
- Chỉ thị dừng CPU (`hlt`).

> [!WARNING]
> Nếu một chương trình chạy ở User Mode cố tình thực thi một lệnh đặc quyền, phần cứng CPU sẽ phát hiện vi phạm và kích hoạt một **Trap (Exception)** báo về cho Kernel. Hệ điều hành thường xử lý trường hợp này bằng cách ghi log lỗi và chấm dứt (Terminate) tiến trình vi phạm.

---

## 5. Các Môi Trường Tính Toán (Computing Environments)

| Môi Trường | Cơ Chế Điều Phối | Mục Tiêu Tối Ưu | Khả Năng Tương Tác |
| :--- | :--- | :--- | :--- |
| **Đơn chương (Uniprogramming)** | Mỗi thời điểm chỉ nạp 1 chương trình vào bộ nhớ. CPU chờ khi có thao tác I/O. | Đơn giản hóa kiến trúc điều khiển | Thấp |
| **Đa chương (Multiprogramming)** | Nạp đồng thời nhiều tiến trình vào bộ nhớ. Khi tiến trình hiện tại chờ I/O, CPU chuyển sang thực thi tiến trình khác. | Tối đa hóa hiệu suất sử dụng CPU (CPU Utilization) | Thấp (xử lý theo lô) |
| **Chia sẻ thời gian (Time-Sharing / Multitasking)** | CPU phân chia thời gian luân phiên qua ngắt đồng hồ định kỳ (Timer Interrupt). | Tối thiểu hóa thời gian đáp ứng (Response Time) | Cao (tương tác trực tiếp) |
| **Thời gian thực (Real-Time)** | Ràng buộc thời hạn hoàn thành nghiêm ngặt. Gồm *Hard Real-Time* và *Soft Real-Time*. | Đảm bảo tính tất định và thời hạn deadline | Theo sự kiện điều khiển |

---

## 6. Câu Hỏi Tự Luyện & Liên Kết Tri Thức

- Ngân hàng câu hỏi tự luận: [[sub-ch01]]
- Bộ thẻ nhớ ôn tập: [[flashcards-ch01]]
- Từ điển thuật ngữ liên quan: [[glossary-terms]]

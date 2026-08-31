---
id: "theory-ch02-structure"
title: "Chương 2: Cấu trúc và dịch vụ Hệ điều hành"
book: "theory"
chapter: 2
order: 2
slug: "ch02-structure"
summary: "Thành phần, dịch vụ, system call, system programs và các kiểu cấu trúc kernel."
prerequisites:
  - "theory-ch01-overview"
related:
  - "sub-ch02"
  - "theory-ch03-process"
exam_relevance:
  frequent_topics:
    - "Tám thành phần và chín dịch vụ OS"
    - "System Call, API và truyền tham số"
    - "Sáu nhóm system programs"
    - "Monolithic, layered, microkernel, modules và hybrid"
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH02-2024"
  - "UIT-SLIDE-MIDTERM-REVIEW-2024"
  - "UIT-QBANK-CH02-2024"
  - "SILBERSCHATZ-OSC10"
last_updated: "2026-08-31"
---

# Chương 2: Cấu trúc và dịch vụ Hệ điều hành

## Mục tiêu và phạm vi nguồn

Chương này đi theo `UIT-SLIDE-CH02-2024`, slide 4–56 và qbank `UIT-QBANK-CH02-2024`, Câu 1–7 / Mục 2. Giáo trình `SILBERSCHATZ-OSC10` chỉ dùng để làm rõ ranh giới API–system call và trade-off kiến trúc; tên sản phẩm cụ thể không được suy ra thành tuyên bố chính thức của UIT.

## 1. Các thành phần của OS

Một kernel không phải là một chương trình đơn lẻ. Các thành phần dưới đây phối hợp qua cấu trúc dữ liệu và system call.

| Thành phần | Trách nhiệm cốt lõi | Ví dụ đối tượng quản lý |
| --- | --- | --- |
| Quản lý tiến trình | Tạo/kết thúc, lập lịch, đồng bộ và giao tiếp tiến trình. | PCB, ready queue, context. |
| Quản lý bộ nhớ chính | Theo dõi vùng dùng/tự do, cấp phát/thu hồi, bảo vệ và ánh xạ. | Frame, page table, địa chỉ logic. |
| Quản lý file | Tên, thư mục, quyền, mở/đóng, đọc/ghi và ánh xạ file–thiết bị. | inode/FCB, file descriptor. |
| Quản lý I/O | Cung cấp giao diện thống nhất, driver, buffering/caching/spooling. | device queue, driver. |
| Quản lý lưu trữ phụ | Cấp phát block, lập lịch đĩa, theo dõi dung lượng và độ tin cậy. | block, free-space list. |
| Networking/distributed | Giao tiếp máy–máy, giao thức và tài nguyên phân tán khi nền tảng hỗ trợ. | socket, message, remote service. |
| Protection | Kiểm soát tiến trình/chủ thể nào được truy cập đối tượng nào. | mode, ACL, capability. |
| Security | Xác thực, kiểm soát đặc quyền, toàn vẹn và chống lạm dụng. | credential, audit. |
| Command interpreter/UI | Nhận lệnh hoặc thao tác đồ họa, gọi dịch vụ và hiển thị kết quả. | shell, desktop UI. |

Slide có thể gom protection và security thành một cụm; khi trả lời qbank hãy nêu cả hai chức năng và nói rõ cách gom.

## 2. Dịch vụ OS

### Dịch vụ hướng người dùng

1. **User interface:** CLI, GUI hoặc batch.
2. **Program execution:** nạp, khởi tạo, chạy và kết thúc chương trình.
3. **I/O operations:** đọc/ghi thiết bị với kiểm tra quyền và trạng thái.
4. **File-system manipulation:** tạo/xóa/mở/đóng/đọc/ghi và thư mục.
5. **Communication:** trao đổi dữ liệu giữa tiến trình hoặc qua mạng.
6. **Error detection:** phát hiện lỗi CPU, bộ nhớ, I/O, chương trình và ghi nhận phù hợp.

### Dịch vụ bảo đảm vận hành hiệu quả

7. **Resource allocation:** quyết định CPU, RAM, thiết bị, file và khóa cho các yêu cầu cạnh tranh.
8. **Accounting:** ghi nhận mức sử dụng để theo dõi, tính phí hoặc điều chỉnh chính sách.
9. **Protection and security:** cách ly và kiểm tra quyền trước khi truy cập tài nguyên.

“Dịch vụ” là khả năng OS cung cấp; “thành phần” là bộ phận thực hiện. Ví dụ, file management là thành phần, còn tạo/mở/đọc file là dịch vụ.

## 3. System call, API và truyền tham số

### 3.1 Ba khái niệm không đồng nhất

| Khái niệm | Ai định nghĩa? | Vai trò |
| --- | --- | --- |
| Ordinary function call | Ngôn ngữ/ABI của chương trình | Nhảy tới mã đã liên kết trong cùng không gian (thường không đổi đặc quyền). |
| API | Thư viện/chuẩn lập trình | Giao diện ổn định như `open`, `read`, `pthread_create`; có thể bọc một hoặc nhiều system call. |
| System call | Kernel/kiến trúc OS | Điểm vào được bảo vệ để user code yêu cầu dịch vụ nhân qua trap/instruction đặc biệt. |

Ví dụ `printf` là hàm thư viện; thư viện có thể gọi `write` system call. Tên API không chứng minh có đúng một trap hay có cùng tên trên mọi OS.

### 3.2 Nhóm system call

Các nhóm trong slide gồm process control (create, load, execute, wait, terminate), file management, device management, information maintenance, communications và protection. Nhóm là cách phân loại học tập; một lời gọi thực tế có thể liên quan nhiều tài nguyên.

### 3.3 Ba cách truyền tham số

1. **Thanh ghi:** đặt một số tham số nhỏ trực tiếp trong register; nhanh nhưng giới hạn số lượng/kích thước.
2. **Block/table trong bộ nhớ:** đặt tham số trong vùng nhớ, truyền địa chỉ vùng đó qua register; phù hợp cấu trúc dài.
3. **Stack:** đẩy tham số vào stack rồi trap; quy ước calling convention quyết định thứ tự và ai dọn stack.

Kernel phải kiểm tra con trỏ/vùng nhớ user trước khi đọc/ghi; truyền địa chỉ không tự cấp quyền truy cập.

## 4. System programs — một lớp thực sự của hệ thống

System programs là các chương trình tiện ích cung cấp môi trường thuận tiện cho phát triển và chạy chương trình; chúng thường chạy ở user mode và **gọi** kernel, không phải bản thân kernel.

| Nhóm | Công việc | Ví dụ loại tiện ích |
| --- | --- | --- |
| File management | Tạo, sao chép, đổi tên, xóa, hiển thị và phân quyền file. | `cp`, `mv`, `chmod`. |
| Status information | Xem ngày giờ, người dùng, tài nguyên, log và trạng thái hệ thống. | `ps`, `free`, `uname`. |
| File modification | Soạn thảo/chuyển đổi nội dung văn bản hoặc dữ liệu. | editor, filter. |
| Programming-language support | Compiler, assembler, linker, debugger, interpreter. | `gcc`, `ld`, `gdb`. |
| Program loading/execution | Loader, runtime, job control, script runner. | shell, loader. |
| Communications | Mail, remote login, truyền file, pipeline và network tools. | `ssh`, `ftp`, pipe utility. |

Một shell là system program thực hiện parse lệnh rồi dùng system call như `fork`, `exec`, `wait`; shell không phải là kernel.

## 5. Cấu trúc thiết kế OS

### 5.1 Cơ chế và trade-off

| Cấu trúc | Cách tổ chức | Ưu điểm | Hạn chế/điểm cần phân biệt |
| --- | --- | --- | --- |
| Simple/monolithic | Nhiều dịch vụ chạy trong cùng không gian kernel, gọi trực tiếp nhau. | Nhanh, giao tiếp đơn giản. | Biên bảo vệ lớn; lỗi một driver có thể ảnh hưởng kernel; khó kiểm thử. |
| Layered | Chia lớp, lớp trên chỉ dùng dịch vụ lớp dưới theo hợp đồng. | Dễ hiểu, kiểm thử và thay thế. | Khó chọn ranh giới; có overhead/giới hạn phụ thuộc. |
| Microkernel | Kernel tối thiểu (IPC, scheduling, address spaces); service ở user space. | Cô lập lỗi, linh hoạt, dễ mở rộng. | IPC/context switch thêm chi phí; thiết kế protocol phức tạp. |
| Modules | Kernel lõi hỗ trợ module nạp động, mỗi module phục vụ chức năng. | Mở rộng linh hoạt gần hiệu năng monolithic. | Module vẫn có thể chạy đặc quyền; ABI và độ tin cậy là rủi ro. |
| Hybrid | Kết hợp ý tưởng nhiều cấu trúc, một số dịch vụ ở kernel, một số tách biệt. | Cân bằng tương thích, hiệu năng và cô lập. | Ranh giới thực tế phức tạp; nhãn “hybrid” cần nêu nguồn/phạm vi. |

“Monolithic” nói về cách các dịch vụ liên kết trong kernel, không có nghĩa code không modular. “Hybrid” không phải giấy phép gán nhãn cho mọi OS; hãy mô tả thành phần cụ thể và ghi rằng đó là cách phân loại kiến trúc.

### 5.2 Luồng gọi minh họa

```
Ứng dụng → API/thư viện → trap/system-call entry → kernel service → driver → thiết bị
             (user)                  (mode switch)          (privileged)
```

Mỗi mũi tên là một hợp đồng: API kiểm tra kiểu/tiện ích, entry kiểm tra quyền và số hiệu, kernel kiểm tra đối số rồi gọi driver.

## 6. Tự kiểm tra

- Vì sao `printf` không đồng nghĩa với một system call duy nhất?
- Hãy lập bảng “thành phần” và “dịch vụ” cho ví dụ đọc file.
- Nêu một lý do microkernel tăng độ tin cậy và một lý do nó có thể chậm hơn.

Ngân hàng câu hỏi nguồn-backed: [[sub-ch02]] · Nối sang quản lý tiến trình: [[theory-ch03-process]]

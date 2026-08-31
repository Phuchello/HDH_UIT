---
id: "theory-ch01-overview"
title: "Chương 1: Tổng quan về Hệ điều hành và Kiến trúc máy tính"
book: "theory"
chapter: 1
order: 1
slug: "ch01-overview"
summary: "Từ vai trò của hệ điều hành đến bootstrap, ngắt, lưu trữ, bộ xử lý, dual-mode và các môi trường tính toán."
prerequisites: []
related:
  - "sub-ch01"
  - "glossary-terms"
  - "flashcards-ch01"
exam_relevance:
  frequent_topics:
    - "Định nghĩa và hai góc nhìn về hệ điều hành"
    - "Interrupt vector, ISR, trap và exception"
    - "Storage hierarchy, locality và caching"
    - "Single/multiprocessor, SMP/AMP và clustered systems"
    - "Dual-mode, privileged instruction và timer"
sources:
  - "UIT-OUTLINE-2024"
  - "UIT-SLIDE-CH01-2024"
  - "UIT-SLIDE-MIDTERM-REVIEW-2024"
  - "SILBERSCHATZ-OSC10"
last_updated: "2026-08-30"
---

# Chương 1: Tổng quan về Hệ điều hành và Kiến trúc máy tính

## Mục tiêu học tập

Sau chương này, người học có thể định nghĩa hệ điều hành theo góc nhìn người dùng và hệ thống; mô tả bootstrap và chu trình phục vụ ngắt; giải thích các tiêu chí của storage hierarchy và caching; phân biệt CPU, processor, core, SMP, AMP và clustered system; và giải thích dual-mode, lệnh đặc quyền, timer cùng các môi trường tính toán. Các mô tả lớp học dưới đây dựa trên `UIT-SLIDE-CH01-2024` (slide 4–56) và slide ôn tập (`UIT-SLIDE-MIDTERM-REVIEW-2024`, slide 3–15); các ghi chú triển khai được đánh dấu là làm rõ theo giáo trình `SILBERSCHATZ-OSC10`.

## 1. Hệ điều hành là gì?

Hệ điều hành (Operating System, OS) là phần mềm trung gian cung cấp môi trường thực thi và điều phối tài nguyên giữa người dùng/chương trình ứng dụng và phần cứng. Mục tiêu lớp học gồm (1) tạo môi trường thuận tiện để chạy chương trình và (2) sử dụng tài nguyên máy tính hiệu quả, an toàn.

### Hai góc nhìn

| Góc nhìn | Câu hỏi chính | Hệ điều hành làm gì? |
| --- | --- | --- |
| Người dùng (user view) | Máy có dễ dùng, đáp ứng nhanh, ổn định không? | Cung cấp UI, thực thi chương trình, I/O và phản hồi lỗi. |
| Hệ thống (system view) | Làm sao chia sẻ tài nguyên đúng và hiệu quả? | Là resource allocator và control program: phân phối CPU/RAM/thiết bị, cô lập lỗi và bảo vệ. |

### Tổ chức bốn thành phần của hệ thống máy tính

```
Users → Application programs → Operating system (kernel + services) → Hardware
          compiler, browser       scheduler, memory, files          CPU, RAM, I/O
```

Phần cứng cung cấp năng lực tính toán; OS quản lý các tài nguyên dùng chung; chương trình ứng dụng biến dịch vụ đó thành chức năng cho người dùng. Không nên đồng nhất OS với kernel: kernel là phần lõi, còn system programs và giao diện có thể ở ngoài kernel.

> [!CHARACTERISTICS]
> **Đặc tính cần nhớ:** OS phải bảo vệ không gian địa chỉ và trạng thái thiết bị, nhưng không bảo đảm sửa lỗi logic của ứng dụng. “Kernel thường trú” là mô hình giảng dạy kinh điển; hệ hiện đại có thể nạp module hoặc thành phần theo nhu cầu.

## 2. Bootstrap và hoạt động theo ngắt

### 2.1 Bootstrap

Khi bật máy, firmware (BIOS/UEFI) chạy bootstrap program, kiểm tra và khởi tạo tối thiểu phần cứng, tìm thiết bị khởi động, nạp kernel vào RAM rồi chuyển quyền cho kernel. Kernel tiếp tục khởi tạo cấu trúc dữ liệu, driver và tiến trình hệ thống đầu tiên (ví dụ `init`/`systemd` trên Linux). Đây là trình tự khái quát của `UIT-SLIDE-CH01-2024`, slide 14–16; chi tiết firmware phụ thuộc nền tảng.

### 2.2 Interrupt, vector và ISR

Interrupt là tín hiệu làm thay đổi luồng thực thi bình thường để CPU phục vụ sự kiện. Với hardware interrupt, thiết bị phát tín hiệu **bất đồng bộ** so với lệnh đang chạy. Với trap/exception, CPU phát tín hiệu **đồng bộ** do lệnh hiện tại gây ra (lỗi chia 0, vi phạm địa chỉ) hoặc do chương trình chủ động yêu cầu dịch vụ hệ thống (system call).

Interrupt Vector Table (IVT) ánh xạ số hiệu/vector của sự kiện tới địa chỉ bắt đầu của Interrupt Service Routine (ISR). Chu trình khái quát:

1. Phần cứng xác định sự kiện và vector, CPU tạm dừng tại điểm được định nghĩa bởi kiến trúc.
2. CPU/nhân lưu PC, thanh ghi trạng thái và các thanh ghi cần thiết vào vùng ngữ cảnh (thường gắn với stack/PCB).
3. Tra IVT để lấy địa chỉ ISR và chuyển sang ngữ cảnh đặc quyền.
4. ISR lưu thêm trạng thái nếu cần, xác nhận thiết bị/giải quyết sự kiện rồi gọi phần lập lịch hoặc driver.
5. Lệnh return-from-interrupt khôi phục trạng thái và tiếp tục chương trình bị gián đoạn.

| Loại | Nguồn | Đồng bộ? | Ví dụ | Điểm phân biệt |
| --- | --- | --- | --- | --- |
| Hardware interrupt | Thiết bị/bộ điều khiển | Không đồng bộ với lệnh hiện tại | Bàn phím, timer, hoàn tất I/O | Không phải do lệnh ứng dụng trực tiếp gây ra. |
| Trap/exception | CPU hoặc instruction syscall | Đồng bộ | Chia 0, page fault, system call | Liên quan đến instruction đang xét; page fault là exception có thể được OS phục vụ. |

## 3. Storage hierarchy và caching

Các tầng lưu trữ được sắp theo ba tiêu chí: thời gian truy cập/tốc độ, dung lượng và chi phí trên mỗi bit. Thanh ghi và cache nhanh nhưng nhỏ/đắt; RAM chậm hơn nhưng lớn hơn và dễ bay hơi; SSD/HDD/tape chậm hơn, lớn và bền hơn. Không có tầng nào đồng thời tối ưu cả ba tiêu chí.

```
Nhanh, nhỏ, đắt/bit: registers → cache → RAM → SSD → HDD → tape: chậm, lớn, rẻ/bit
```

Caching sao chép tạm dữ liệu từ tầng chậm sang tầng nhanh. Nó hiệu quả nhờ locality of reference: **temporal locality** (vừa dùng sẽ sớm dùng lại) và **spatial locality** (địa chỉ lân cận có khả năng được dùng). Cache hit tiết kiệm một lần truy cập tầng chậm; cache miss phải nạp block và có thể thay thế mục cũ. Chính sách và kích thước cache là tham số thiết kế, không phải lời hứa mọi truy cập đều nhanh.

## 4. CPU, processor, core và hệ đa xử lý

Trong ngữ cảnh môn học, *processor* là đơn vị xử lý có thể được hệ điều hành lập lịch; CPU thường chỉ chip/đơn vị thực thi. *Core* là một engine thực thi bên trong một processor/package; một package có thể có nhiều core. Cách gọi chính xác phụ thuộc tài liệu phần cứng.

| Mô hình | Đặc điểm | Ưu điểm | Giới hạn |
| --- | --- | --- | --- |
| Single-processor | Một đơn vị xử lý thực thi tại một thời điểm. | Đơn giản, ít tranh chấp. | Thông lượng và khả năng chịu lỗi hạn chế. |
| SMP (symmetric multiprocessing) | Nhiều CPU/core bình đẳng, dùng chung bộ nhớ và có thể chạy kernel. | Chia tải, thông lượng và độ tin cậy tốt hơn. | Cần đồng bộ, nhất quán cache và lập lịch đa CPU. |
| AMP (asymmetric multiprocessing) | Một CPU chủ điều phối; CPU phụ đảm nhiệm công việc được phân công. | Thiết kế/điều khiển chuyên biệt. | Có điểm nghẽn ở CPU chủ, ít linh hoạt hơn. |
| Clustered system | Nhiều máy/nút kết nối, phối hợp dịch vụ hoặc dự phòng. | Mở rộng và chịu lỗi ở cấp nút. | Chi phí mạng, đồng thuận và quản trị phức tạp. |

SMP/AMP là mô hình **trong một hệ đa xử lý**; clustered system là phối hợp nhiều hệ thống. Không nên gọi mọi Linux hay Windows là “SMP” chỉ từ tên hệ điều hành: đó là thuộc tính cấu hình phần cứng/kernel.

## 5. Dual-mode, lệnh đặc quyền và timer

CPU tách **User mode** (mã ứng dụng bị giới hạn) và **Kernel mode** (nhân được phép thực thi thao tác nhạy cảm). Mode bit là quy ước của mô hình slide; slide IT007 dùng `0 = kernel`, `1 = user`, nhưng kiến trúc khác có thể dùng bit/level khác. Vì vậy hãy ghi rõ “theo quy ước môn học” khi trả lời.

Privileged instructions có thể tắt/bật ngắt, thay đổi thanh ghi bảo vệ/bản đồ nhớ, truy cập cổng I/O hoặc dừng CPU. Nếu mã user thực hiện, phần cứng không thực thi lệnh mà phát exception; kernel quyết định ghi log, gửi tín hiệu hoặc kết thúc tiến trình tùy chính sách. Không khẳng định mọi hệ điều hành luôn terminate ngay.

Timer là phần cứng phát interrupt định kỳ để kernel lấy lại quyền điều khiển, giới hạn một tiến trình chiếm CPU vô hạn và hỗ trợ preemptive scheduling/time-sharing. Chu kỳ timer là tham số hệ thống; không tự suy ra một quantum cố định từ slide.

## 6. Các môi trường tính toán

| Môi trường | Cơ chế | Mục tiêu/đặc điểm |
| --- | --- | --- |
| Uniprogramming | Một chương trình trong bộ nhớ; CPU có thể rỗi khi chương trình chờ I/O. | Đơn giản, tương tác và sử dụng CPU thấp. |
| Multiprogramming | Nhiều chương trình resident; khi một chương trình chờ I/O, OS chạy chương trình khác. | Tăng CPU utilization và throughput. |
| Time-sharing/multitasking | Timer preemption chia CPU thành các lát nhỏ cho nhiều tác vụ. | Response time tốt cho người dùng tương tác. |
| Real-time | Tác vụ có deadline và yêu cầu tính đúng hạn. | Hard real-time: trễ deadline là thất bại yêu cầu; soft real-time: trễ làm giảm chất lượng nhưng không nhất thiết làm hệ thống sai. Mức phân loại chỉ dùng khi nguồn hỗ trợ. |

Multiprogramming tập trung giữ CPU bận; time-sharing thêm mục tiêu phản hồi và tính tương tác. Hai khái niệm có thể cùng tồn tại trong một hệ thống.

## 7. Kiểm tra nhanh

- Giải thích bằng hai câu vì sao một hardware interrupt là bất đồng bộ còn system call trap là đồng bộ.
- Khi so sánh SMP với AMP, nêu rõ ai chạy kernel và điểm nghẽn điều phối.
- Viết thứ tự `firmware → bootstrap → kernel → init/system services` và chỉ ra bước IVT/ISR trong xử lý ngắt.

Ngân hàng tự luận: [[sub-ch01]] · Flashcards: [[flashcards-ch01]] · Thuật ngữ: [[glossary-terms]]

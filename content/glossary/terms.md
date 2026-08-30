---
id: "glossary-terms"
title: "Từ Điển Thuật Ngữ Hệ Điều Hành Song Ngữ (IT007 Glossary)"
type: "glossary"
slug: "glossary"
summary: "Tra cứu nhanh định nghĩa chuẩn xác các thuật ngữ khoa học máy tính và hệ điều hành song ngữ Anh - Việt có ví dụ thực tế và liên kết tri thức."
sources:
  - "SRC-B01 (Silberschatz Glossary)"
  - "SRC-B02 (POSIX.1-2017)"
last_updated: "2026-08-30"
---

# Từ Điển Thuật Ngữ Hệ Điều Hành (IT007 Glossary)

| Thuật ngữ Tiếng Anh | Thuật ngữ Tiếng Việt | Định nghĩa Bản chất Kỹ thuật | Liên kết Chuyên đề |
| :--- | :--- | :--- | :--- |
| **Asymmetric Multiprocessing (AMP)** | Xử lý đa bất đối xứng | Mô hình đa bộ xử lý trong đó một CPU chủ (Master) đảm nhiệm điều phối và chạy mã Kernel, các CPU tớ (Slave) chỉ chạy tiến trình người dùng. | [[theory-ch01-overview]] |
| **Belady's Anomaly** | Hiện tượng bất thường Belady | Hiện tượng nghịch lý trong thuật toán thay thế trang FIFO, khi tăng số khung trang cấp phát cho tiến trình lại làm tăng số lần xảy ra Lỗi trang (Page Fault). | [[theory-ch08-virtual-memory]] |
| **Bounded Buffer** | Bộ đệm hữu hạn | Bài toán đồng bộ kinh điển giữa tiến trình Producer và Consumer chia sẻ một bộ đệm có sức chứa cố định $N$ phần tử. | [[theory-ch05-synchronization]] |
| **Context Switch** | Chuyển ngữ cảnh | Thao tác phần cứng và hệ điều hành lưu trạng thái của tiến trình hiện tại (vào PCB) và khôi phục trạng thái của tiến trình khác để CPU thực thi. | [[theory-ch03-process]] |
| **Critical Section (CS)** | Vùng tranh chấp / Miền găng | Đoạn mã trong tiến trình truy xuất và thao tác trên tài nguyên bộ nhớ chia sẻ mà tại một thời điểm chỉ được phép có tối đa một tiến trình thực thi. | [[theory-ch05-synchronization]] |
| **Deadlock** | Bế tắc | Tình trạng hai hoặc nhiều tiến trình bị chặn vô hạn định do mỗi tiến trình đều đang giữ một tài nguyên và chờ tài nguyên khác do tiến trình kia nắm giữ. | [[theory-ch06-deadlock]] |
| **Demand Paging** | Phân trang theo yêu cầu | Kỹ thuật quản lý bộ nhớ ảo trong đó một trang nhớ chỉ được nạp từ đĩa vào RAM khi có lệnh thực sự truy xuất đến nó. | [[theory-ch08-virtual-memory]] |
| **Dispatch Latency** | Độ trễ phân phối | Khoảng thời gian từ khi bộ định thời quyết định dừng tiến trình hiện tại đến khi bộ phân phối (Dispatcher) nạp và bắt đầu chạy tiến trình mới. | [[theory-ch04-cpu-scheduling]] |
| **Dual-Mode Operation** | Chế độ hoạt động kép | Cơ chế bảo vệ phần cứng chia hoạt động CPU thành User Mode (Mode bit = 1) và Kernel Mode (Mode bit = 0). | [[theory-ch01-overview]] |
| **Effective Access Time (EAT)**| Thời gian truy xuất hiệu dụng| Giá trị thời gian trung bình có trọng số để CPU truy xuất một ô nhớ khi xét đến tỉ lệ trúng/trượt của bộ đệm TLB hoặc tỷ lệ lỗi trang. | [[theory-ch07-memory-management]] |
| **Hard Real-Time** | Thời gian thực cứng | Hệ thống bắt buộc các tác vụ phải hoàn thành chính xác trước thời hạn deadline; nếu trễ hạn sẽ dẫn đến sự sụp đổ nghiêm trọng của hệ thống. | [[theory-ch01-overview]] |
| **Interrupt Vector Table (IVT)**| Bảng véc-tơ ngắt | Mảng con trỏ trong bộ nhớ chứa địa chỉ bắt đầu của các chương trình phục vụ ngắt (ISR) tương ứng với từng số hiệu ngắt. | [[theory-ch01-overview]] |
| **Mutual Exclusion** | Loại trừ tương hỗ | Điều kiện bắt buộc trong đồng bộ hóa: Nếu tiến trình $P_i$ đang thực thi trong Critical Section thì không có tiến trình nào khác được vào CS. | [[theory-ch05-synchronization]] |
| **Page Fault** | Lỗi trang | Bẫy ngắt (Trap) phát sinh khi CPU truy xuất một trang nhớ có bit trạng thái hợp lệ/bất hợp lệ mang giá trị $i$ (Invalid - chưa nạp vào RAM). | [[theory-ch08-virtual-memory]] |
| **Privileged Instruction** | Lệnh đặc quyền | Chỉ thị máy chỉ được phép thực thi trong Kernel Mode (như lệnh tắt ngắt, đổi mode bit, thao tác I/O). | [[theory-ch01-overview]] |
| **Race Condition** | Tình trạng chạy đua | Hiện tượng nhiều tiến trình cùng truy xuất và thao tác đồng thời trên dữ liệu chia sẻ, kết quả cuối cùng phụ thuộc vào thứ tự thực thi của các lệnh. | [[theory-ch05-synchronization]] |
| **Safe State** | Trạng thái an toàn | Trạng thái hệ thống tồn tại ít nhất một chuỗi an toàn $\langle P_1, P_2, \dots, P_n \rangle$ đảm bảo mọi tiến trình đều có thể hoàn thành mà không bị Deadlock. | [[theory-ch06-deadlock]] |
| **Semaphore** | Biến đồng bộ Semaphore | Biến nguyên tử nguyên dương được khởi tạo để điều phối đồng bộ tiến trình thông qua 2 thao tác không thể phân chia `wait()` ($P$) và `signal()` ($V$). | [[theory-ch05-synchronization]] |
| **Symmetric Multiprocessing (SMP)**| Xử lý đa đối xứng | Kiến trúc đa xử lý trong đó mọi CPU đều bình đẳng, cùng chạy chung một bản sao của nhân hệ điều hành và chia sẻ bộ nhớ chính. | [[theory-ch01-overview]] |
| **System Call** | Lời gọi hệ thống | Giao diện lập trình cung cấp cách thức để chương trình người dùng yêu cầu các dịch vụ từ nhân hệ điều hành. | [[theory-ch02-structure]] |
| **Thrashing** | Hiện tượng nghẽn bộ nhớ | Trạng thái hệ thống trong đó CPU dành phần lớn thời gian để nạp và hoán đổi trang nhớ thay vì thực thi lệnh của tiến trình, làm sụp đổ hiệu suất. | [[theory-ch08-virtual-memory]] |
| **Translation Lookaside Buffer (TLB)**| Bộ đệm chuyển đổi địa chỉ | Bộ nhớ kết hợp (Associative Memory) tốc độ cao dùng để lưu tạm các mục chuyển đổi từ số trang logic sang số khung trang vật lý. | [[theory-ch07-memory-management]] |
| **Working-Set Model** | Mô hình tập làm việc | Mô hình kiểm soát hiện tượng Thrashing dựa trên nguyên lý cục bộ, xác định tập các trang nhớ được tiến trình truy xuất trong cửa sổ thời gian $\Delta$. | [[theory-ch08-virtual-memory]] |
| **Zombie Process** | Tiến trình thây ma | Tiến trình con đã kết thúc thực thi (`exit()`) nhưng tiến trình cha chưa gọi `wait()` để thu hồi mã trạng thái thoát trong PCB. | [[theory-ch03-process]] |

# BÁO CÁO PHÂN TÍCH KHOẢNG CÁCH NỘI DUNG V1 VS V2 (CONTENT GAP REPORT)

Tài liệu này đánh giá toàn diện các khiếm khuyết học thuật, điểm nén kiến thức quá mức và các chuyên đề còn thiếu trong bản thảo V1 (56 trang), từ đó xác lập các yêu cầu tái thiết lập bắt buộc cho hai ấn phẩm **Sách Lý Thuyết V2 (Book A)** và **Sách Thực Hành V2 (Book B)**.

---

## 1. Tổng Quan Kết Quả Kiểm Toán Độc Lập

Bản thảo V1 (56 trang A4) đạt độ ổn định cao về mặt kỹ thuật in ấn và độ chính xác của các bài tập tính toán mẫu (Gantt chart SRTF, bảng Banker, bảng thay thế trang LRU 20 bước). Tuy nhiên, một đợt kiểm toán học thuật toàn diện đối chiếu với 14 bộ Slide bài giảng chính thức, Slide Ôn tập Giữa kỳ và Đề cương chi tiết IT007 cho thấy:

1. **Quá thiên lệch về giải bài tập tính toán, thiếu hụt nền tảng lý thuyết học thuật**: Bản V1 tập trung giải quyết các bài toán cơ học để lấy điểm thi mà bỏ qua nhiều khái niệm cấu trúc máy tính, cơ chế phần cứng và bảng đặc tính so sánh.
2. **Bỏ sót hoàn toàn Chương 9 (Nghiên cứu điển hình Linux & Windows)**: Đề cương chính thức IT007 có Chương 9, nhưng V1 hoàn toàn không có chương này.
3. **Thiếu hụt các chuyên đề lý thuyết nâng cao trong Chương 1, 2, 4**:
   - Chương 1: Thiếu Hệ thống đa bộ xử lý (AMP vs SMP), Hệ thống gom cụm (Clustered systems: Asymmetric vs Symmetric), UMA vs NUMA.
   - Chương 2: Thiếu mục Chương trình hệ thống (System Programs) phân loại 6 nhóm chính thức.
   - Chương 4: Thiếu Định thời tiểu trình (PCS vs SCS), Định thời đa bộ xử lý (Processor Affinity, Push/Pull Migration), Định thời Real-time (RMS, EDF), Bộ định thời CFS của Linux và Bộ định thời Windows 32 mức ưu tiên.
4. **Phần thực hành Linux bị thu nhỏ thành phụ lục tóm tắt**: Bài Lab 6 (Xây dựng shell `it007sh`) là bài tập lớn trọng tâm nhưng chỉ được đề cập sơ lược, không đủ để sinh viên tự thực hành và hiểu sâu cơ chế File Descriptor / Pipeline / Signal.
5. **Lạm dụng ngôn ngữ tiếp thị và cấu trúc "Mẹo thi / Bẫy UIT"**: Sử dụng quá nhiều cụm từ như *"chinh phục A/A+"*, *"Master Review"*, *"11 bước sư phạm"*, *"Bẫy UIT"* ở khắp nơi, làm giảm tính học thuật và trang trọng của cuốn sách.

---

## 2. Bảng Phân Tích Khoảng Cách Chi Tiết Từng Chương

| Chuyên đề | Hiện trạng trong V1 | Khiếm khuyết & Thiếu sót học thuật | Kế hoạch giải quyết trong V2 (Book A & Book B) |
| :--- | :--- | :--- | :--- |
| **Phần 0: Nền tảng** | 2 trang: Lời khuyên chung và code C ngắn. | Thiếu hướng dẫn có hệ thống về con trỏ, struct, quản lý bộ nhớ động và chuẩn POSIX. | Tái cấu trúc thành Phần 0 chuyên sâu về tư duy hệ thống và kỹ năng lập trình C chuẩn POSIX. |
| **Chương 1: Tổng quan** | 4 trang: Khái niệm HDH, Dual mode, Ngắt. | - Thiếu 2 góc nhìn User view vs System view.<br>- Thiếu phân loại bộ xử lý: Core vs Multicore vs Multiprocessor.<br>- Thiếu AMP vs SMP, Clustered systems.<br>- Thiếu bảng so sánh 4 môi trường tính toán. | Soạn thảo lại toàn diện: Bổ sung 4 bảng đặc tính so sánh, phân tích sâu cơ chế phần cứng và trả lời 100% câu hỏi ôn tập Ch1. |
| **Chương 2: Cấu trúc HDH** | 4 trang: System call, Monolithic vs Microkernel. | - Bỏ sót hoàn toàn 6 nhóm System Programs.<br>- Thiếu chi tiết trách nhiệm 8 thành phần HDH.<br>- Thiếu phân loại 2 nhóm dịch vụ HDH và 3 phương pháp truyền tham số. | Bổ sung mục riêng về 6 nhóm System Programs (có lệnh minh họa); lập bảng trách nhiệm 8 thành phần và 2 nhóm dịch vụ. |
| **Chương 3: Quản lý Tiến trình**| 7 trang: PCB, State, Fork trees. | - Quá tập trung vào bài tập cây fork.<br>- Thiếu phân tích sâu các hàng đợi định thời và 3 loại Scheduler.<br>- Thiếu cơ chế Message Passing chi tiết và 3 mô hình đa luồng (Many-to-One, One-to-One, Many-to-Many). | Cân đối lại tỷ trọng: Giữ vững bài tập fork nhưng bổ sung đầy đủ lý thuyết hàng đợi, IPC Message Passing, và bảng so sánh Process vs Thread. |
| **Chương 4: Định thời CPU** | 5 trang: FCFS, SJF, SRTF, RR, Priority. | - Quá thiên về vẽ sơ đồ Gantt tính toán.<br>- Thiếu Thread scheduling (PCS vs SCS).<br>- Thiếu Multiprocessor scheduling, Processor Affinity, Load balancing.<br>- Thiếu Real-time scheduling (RMS, EDF).<br>- Thiếu Linux CFS và Windows 32-level Priority scheduler. | Tái cấu trúc thành chương chuyên khảo sâu: Bổ sung đầy đủ 4 chuyên đề nâng cao bị thiếu; lập bảng tổng hợp 8 thuật toán định thời với ưu/nhược điểm và starvation. |
| **Midterm Review** | 4 trang: Tóm tắt mẹo thi và 1 đề thi thử. | Lạm dụng từ ngữ "Master Review"; thiếu các câu hỏi lý thuyết tính chất chính thức của slide Week 8. | Tái thiết lập thành Bản ôn tập Giữa kỳ chuẩn hóa: Bảng đặc tính lý thuyết 4 chương đầu, câu hỏi tự luận ngắn, bài tập trạng thái tiến trình và đề thi mẫu chuẩn format UIT. |
| **Chương 5: Đồng bộ Tiến trình**| 6 trang: Peterson, Semaphore, 3 bài toán. | - Thiếu phân tích sâu ngữ nghĩa Hoare vs Mesa của Monitor.<br>- Thiếu phân tích liveness (Deadlock vs Starvation quan hệ trong đồng bộ). | Hoàn thiện định nghĩa hình thức 3 điều kiện CS; giải thích rõ ngữ nghĩa Monitor và bổ sung mã C mẫu có kiểm tra lỗi. |
| **Chương 6: Deadlock** | 4 trang: 4 điều kiện, RAG, Banker. | - Thiếu phân tích triết lý thuật toán Đà điểu (Ostrich algorithm).<br>- Thiếu chi tiết đồ thị Wait-for Graph cho single instance detection. | Bổ sung phân tích triết lý xử lý Deadlock trong các HDH thực tế; chuẩn hóa bài tập Banker và đồ thị RAG. |
| **Chương 7: Quản lý Bộ nhớ** | 4 trang: Placement, Paging, TLB. | - Thiếu chi tiết 3 thời điểm Binding và Dynamic Linking.<br>- Thiếu Bảng trang phân cấp 2 cấp, Bảng trang băm, Bảng trang nghịch đảo và Phân đoạn (Segmentation). | Bổ sung đầy đủ các cấu trúc bảng trang nâng cao, phân đoạn (Segmentation) và 3 bài toán tính EAT (thuận và nghịch). |
| **Chương 8: Bộ nhớ ảo** | 4 trang: Demand Paging, FIFO, OPT, LRU. | - Thiếu phân tích sâu cơ chế Working-Set Model ($\Delta$) và Page-Fault Frequency (PFF).<br>- Thiếu chi tiết cơ chế Copy-on-Write khi `fork()`. | Bổ sung giải pháp giải quyết Thrashing (Working set & PFF); giữ vững bảng thay thế trang 20 bước chi tiết 100%. |
| **Chương 9: Linux & Windows** | **HOÀN TOÀN THIẾU (0 trang)** | **Bỏ sót toàn bộ chuyên đề Chương 9 của đề cương chính thức UIT.** | **Xây dựng mới 100% Chương 9**: Nghiên cứu sâu kiến trúc nhân Linux (`task_struct`, CFS, VFS, Buddy) và kiến trúc nhân Windows (HAL, Executive, EPROCESS, 32-level Priority). |
| **Final Review** | 6 trang: 02 Đề thi mô phỏng. | Cần chuẩn hóa format đề thi bám sát cấu trúc đề thi 2022–2025 có thêm phần trắc nghiệm/điền từ thuật ngữ tiếng Anh. | Cập nhật 02 Đề thi thử Cuối kỳ toàn diện kèm đáp án chi tiết và barem điểm chính xác. |
| **Phần Thực Hành / Lab** | 4 trang phụ lục tóm tắt lệnh Linux. | Quá sơ sài, không thể dùng làm sách hướng dẫn thực hành độc lập; thiếu hoàn toàn hướng dẫn từng bước cho Lab 1–6 và case study shell `it007sh`. | **Tách riêng thành cuốn BOOK B (THỰC HÀNH HỆ ĐIỀU HÀNH)**: Hướng dẫn chi tiết Lab 1–6, trong đó Lab 6 là Case Study 7 giai đoạn xây dựng shell `it007sh` từ đầu với sơ đồ File Descriptor. |

---

## 3. Kế Hoạch Chuyển Đổi Sang Mô Hình Hai Ấn Phẩm Độc Lập

```
┌────────────────────────────────────────────────────────────────────────┐
│ BOOK A: HỆ ĐIỀU HÀNH — IT007 (LÝ THUYẾT · BÀI TẬP · ÔN THI)            │
│ Quy mô dự kiến: ~120 – 150 trang A4                                    │
│ Mục tiêu: Tự học toàn diện từ số 0 mà không cần đến lớp nghe giảng,    │
│           bao phủ 100% đề cương, slide bài giảng và ngân hàng đề thi. │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ BOOK B: THỰC HÀNH HỆ ĐIỀU HÀNH — IT007 (LINUX · PROCESS · IPC · SHELL) │
│ Quy mô dự kiến: ~80 – 100 trang A4                                     │
│ Mục tiêu: Cẩm nang thực hành cầm tay chỉ việc, chuẩn POSIX/Linux C,    │
│           Case Study 7 giai đoạn xây dựng Shell it007sh hoàn chỉnh.    │
└────────────────────────────────────────────────────────────────────────┘
```

# Phương Pháp Sư Phạm & Nguyên Tắc Biên Soạn (Methodology)

Cẩm nang **IT007 – Hệ điều hành UIT** được biên soạn dựa trên phương pháp sư phạm 11 bước đa tầng (Multi-layered Pedagogical Framework), giải quyết bài toán cốt lõi: chuyển hóa các khái niệm trừu tượng của hệ điều hành thành trực giác trực quan, hiểu bản chất phần cứng và làm chủ kỹ năng giải bài tập/luyện thi.

---

## 1. Khung 11 Bước Sư Phạm Chuẩn Hóa

Mỗi chương trong cẩm nang đều tuân thủ chặt chẽ cấu trúc 11 tầng nhận thức:

```
[1. VÌ SAO CẦN KHÁI NIỆM NÀY] (Động lực kỹ thuật, vấn đề thực tế)
       ↓
[2. MÔ HÌNH TRỰC GIÁC] (Ẩn dụ đời sống, hình dung dễ nhớ)
       ↓
[3. ĐỊNH NGHĨA CHUẨN XÁC ACADEMIC] (Định nghĩa chuẩn POSIX / Khoa học máy tính)
       ↓
[4. CƠ CHẾ HOẠT ĐỘNG TỪNG BƯỚC] (Step-by-step trace)
       ↓
[5. HÌNH DUNG TRONG PHẦN CỨNG & BỘ NHỚ] (Thanh ghi, RAM, Bảng trang, PCB)
       ↓
[6. VÍ DỤ MINH HỌA NHỎ] (Toy example có số liệu trực quan)
       ↓
[7. BÀI TẬP WORKED EXAMPLE CHUẨN ĐỀ THI UIT] (Có sơ đồ Gantt / Bảng tính đầy đủ)
       ↓
[8. SAI LẦM PHỔ BIẾN — ĐỪNG NHẦM] (Phân biệt các khái niệm hay bị nhầm lẫn)
       ↓
[9. BẪY ĐỀ THI UIT] (Các điểm gài bẫy kinh điển trong đề thi tự luận/trắc nghiệm)
       ↓
[10. LIÊN HỆ LINUX LAB & SYSTEM CALLS] (Code C mẫu, POSIX API: fork, wait, pipe, semaphore)
       ↓
[11. BẢNG ÔN TẬP NHANH 1 TRANG — QUICK RECALL] (Kích hoạt trí nhớ chủ động Active Recall)
```

---

## 2. Các Trụ Cột Học Thuật Then Chốt

### A. Bản chất kiến trúc máy tính trước, Công thức sau
- Không yêu cầu người học học vẹt công thức tính $TAT, WT, RT$ hay EAT mà giải thích rõ: $TAT$ là tổng thời gian từ lúc tiến trình vào hệ thống đến khi kết thúc; $WT$ là thời gian tiến trình phải nằm chờ trong hàng đợi Ready; $RT$ là thời gian từ lúc đến đến lần đầu tiên nhận CPU.

### B. Bài tập từng bước, không giải tắt
- Các bài tập định thời CPU (FCFS, SJF, SRTF, Priority, Round Robin, HRRN) đều có sơ đồ Gantt chi tiết kèm bảng tính $CT, TAT, WT, RT$ và giá trị trung bình chính xác.
- Thuật toán Banker trình bày đầy đủ bảng tính ma trận $Need$, bảng diễn tiến véc-tơ $Work$ qua từng bước cấp phát an toàn.
- Thuật toán thay thế trang (FIFO, OPT, LRU) trình bày đầy đủ bảng nạp trang 20 bước và đếm số lỗi trang (Page Faults) chính xác 100%.

### C. Độc lập Ngoại tuyến & Trải nghiệm Đọc Hoàn Hảo
- Sách được dàn trang in ấn chuẩn A4 với CSS hiện đại, phông chữ tối ưu độ tương phản, hỗ trợ ngắt trang thông minh tránh cắt vụn bảng biểu và khối mã nguồn C.
- Toàn bộ công thức toán học được hiển thị bằng thư viện MathJax 3.2.2 offline tích hợp sẵn trong kho lưu trữ.

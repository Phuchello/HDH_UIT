# PHÂN TÍCH QUY LUẬT & XU HƯỚNG ĐỀ THI IT007 UIT (EXAM PATTERN ANALYSIS)

Tài liệu này tổng hợp phân tích định lượng và định tính về cấu trúc đề thi, quy luật ra đề và xu hướng đổi mới hình thức kiểm tra môn Hệ điều hành (IT007) tại UIT từ năm 2017 đến 2025.

---

## 1. Cấu Trúc Đề Thi Giữa Kỳ (Midterm Exam Structure)

Đề thi Giữa kỳ IT007 kéo dài từ **45 đến 60 phút**, bao quát nội dung từ **Chương 1 đến Chương 4**.

```
ĐỀ THI GIỮA KỲ IT007 (10 ĐIỂM)
├── PHẦN 1: LÝ THUYẾT & ĐẶC TÍNH CƠ BẢN (3.0 – 4.0 điểm)
│   ├── Trắc nghiệm hoặc Đúng/Sai (10–15 câu)
│   ├── Điền thuật ngữ tiếng Anh ngắn gọn (Context Switch, Dispatcher, PCB)
│   └── Câu hỏi tự luận ngắn: Đặc điểm ngắt, Dual-mode, Lệnh đặc quyền, Storage hierarchy
├── PHẦN 2: QUẢN LÝ TIẾN TRÌNH & CÂY FORK (2.5 – 3.0 điểm)
│   ├── Dạng 1: Lần vết chuỗi trạng thái tiến trình (New -> Ready -> Running -> Waiting) với vòng lặp và printf
│   └── Dạng 2: Vẽ cây tiến trình fork(), đếm số tiến trình con/cháu, tính số chuỗi in ra
└── PHẦN 3: BÀI TOÁN ĐỊNH THỜI CPU (3.5 – 4.0 điểm)
    ├── Cho bảng 4–5 tiến trình với Arrival Time và Burst Time
    ├── Vẽ sơ đồ Gantt cho 2–3 giải thuật (FCFS, SJF Preemptive / SRTF, Round Robin, Priority Preemptive)
    └── Lập bảng tính toán chi tiết: CT, TAT, WT, RT và tính giá trị trung bình chính xác
```

---

## 2. Cấu Trúc Đề Thi Cuối Kỳ (Final Exam Structure)

Đề thi Cuối kỳ IT007 kéo dài **90 phút** (đôi khi 75 phút), tập trung trọng tâm vào **Chương 5 đến Chương 8** (và một phần kiến thức tổng hợp Chương 1–4, 9).

```
ĐỀ THI CUỐI KỲ IT007 (10 ĐIỂM)
├── PHẦN 1: LÝ THUYẾT TRẮC NGHIỆM / ĐIỀN TỪ (2.0 – 3.0 điểm)
│   ├── Trắc nghiệm Đúng/Sai, Chọn câu sai, So sánh khái niệm (Dynamic Linking vs Loading)
│   └── Thuật ngữ tiếng Anh: Mutual Exclusion, Safe Sequence, Belady Anomaly, Page Fault
├── PHẦN 2: BÀI TOÁN ĐỒNG BỘ TIẾN TRÌNH (2.5 – 3.0 điểm)
│   ├── Đặt bài toán thực tế (Xe qua cầu 1 chiều, Producer-Consumer mở rộng, Phòng đọc/in ấn)
│   └── Yêu cầu: Khai báo Semaphores/Mutex và viết mã giả/mã C đồng bộ hóa thỏa mãn 3 điều kiện CS
├── PHẦN 3: DEADLOCK & THUẬT TOÁN BANKER (2.0 – 2.5 điểm)
│   ├── Ý a: Dựng ma trận Need = Max - Allocation (bắt buộc)
│   ├── Ý b: Áp dụng thuật toán kiểm tra tính an toàn (Safety algorithm), tìm chuỗi an toàn Work
│   └── Ý c: Xử lý yêu cầu cấp phát Request_i theo 3 bước điều kiện
└── PHẦN 4: QUẢN LÝ BỘ NHỚ & BỘ NHỚ ẢO (2.5 – 3.0 điểm)
    ├── Ý a: Cấp phát phân vùng (First/Best/Worst fit) hoặc Tính địa chỉ phân trang / Tính EAT với TLB
    └── Ý b: Lập bảng thay thế trang 20 tham chiếu cho FIFO, OPT, LRU với 3-4 khung trang (đếm số Page Faults)
```

---

## 3. Xu Hướng Đổi Mới Đề Thi Gần Đây (2022–2025)

1. **Bổ sung phần Điền thuật ngữ tiếng Anh (English Short-Answer)**: Đề thi từ năm học 2023–2024 và 2024–2025 có thêm dạng câu hỏi yêu cầu sinh viên điền thuật ngữ tiếng Anh chuẩn xác (tối đa 1–2 từ) để đánh giá khả năng đọc hiểu tài liệu gốc.
2. **Khắt khe trong trình bày bài tập tính toán**:
   - Bài toán định thời CPU: Bắt buộc vẽ sơ đồ Gantt rõ mốc thời gian, không được viết tắt bảng $TAT, WT$.
   - Bài toán Banker: Bắt buộc trình bày từng bước cập nhật véc-tơ $Work$ qua từng tiến trình được cấp phát, không được ghi mỗi chuỗi an toàn.
   - Bài toán thay thế trang: Bắt buộc vẽ đầy đủ ma trận các khung trang qua từng bước tham chiếu, đánh dấu rõ bước nào xảy ra Lỗi trang (*Page Fault*) và bước nào trúng (*Hit*).
3. **Bài toán đồng bộ đa dạng hóa ngữ cảnh**: Không chỉ hỏi bài toán Bounded Buffer nguyên bản mà chuyển thành các bài toán thực tế (Quản lý hàng đợi giao thông, Đồng bộ luồng cộng tác tính toán, Quản lý tài nguyên in ấn).

---

## 4. Ma Trận Phân Bổ Điểm Số & Trọng Tâm Ôn Luyện

| Chuyên đề môn học | Tỷ trọng điểm Giữa kỳ | Tỷ trọng điểm Cuối kỳ | Đánh giá mức độ ưu tiên |
| :--- | :---: | :---: | :--- |
| **Chương 1: Tổng quan & Kiến trúc** | 20% | 5% | Trọng tâm Giữa kỳ (Lý thuyết nền tảng) |
| **Chương 2: Cấu trúc HDH & System Calls** | 15% | 5% | Trọng tâm Giữa kỳ (Phân loại System Programs) |
| **Chương 3: Quản lý Tiến trình & Fork** | 30% | 10% | Cực kỳ quan trọng (Chiếm 30% Giữa kỳ) |
| **Chương 4: Định thời CPU** | 35% | 10% | Cực kỳ quan trọng (Chiếm 35% Giữa kỳ) |
| **Chương 5: Đồng bộ Tiến trình** | - | 25% | Trọng tâm Cuối kỳ số 1 |
| **Chương 6: Deadlock & Banker** | - | 20% | Trọng tâm Cuối kỳ số 2 |
| **Chương 7: Quản lý Bộ nhớ & Paging** | - | 15% | Trọng tâm Cuối kỳ số 3 |
| **Chương 8: Bộ nhớ ảo & Thay thế trang** | - | 20% | Trọng tâm Cuối kỳ số 4 |
| **Chương 9: Linux & Windows Case Studies**| - | 5% | Trắc nghiệm mở rộng & Điểm 9-10 |

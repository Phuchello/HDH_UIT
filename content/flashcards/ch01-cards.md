---
id: "flashcards-ch01"
title: "Thẻ Nhớ Flashcards — Chương 1: Tổng Quan HDH"
type: "flashcards"
chapter: 1
order: 1
slug: "ch01-flashcards"
summary: "Bộ thẻ nhớ Active Recall ôn luyện định nghĩa, lệnh đặc quyền, cơ chế ngắt và các thông số kỹ thuật của Chương 1."
related:
  - "theory-ch01-overview"
  - "sub-ch01"
last_updated: "2026-08-30"
---

# Thẻ Nhớ Ôn Tập (Flashcards): Chương 1

> [!STUDYCARD] id="fc-01-mode-bit"
> **Mặt trước (Câu hỏi):** `Mode bit` trong CPU mang giá trị gì ở User Mode và Kernel Mode?
> <!-- hint -->
> Gợi ý: Giá trị 0 thường biểu thị mức quyền lực cao nhất.
> <!-- answer -->
> - **Kernel Mode (Supervisor / Privileged):** `Mode bit = 0`
> - **User Mode (Không đặc quyền):** `Mode bit = 1`

---

> [!STUDYCARD] id="fc-02-storage-criteria"
> **Mặt trước (Câu hỏi):** Nêu 3 tiêu chí phân cấp hệ thống lưu trữ (Storage Hierarchy).
> <!-- hint -->
> Gợi ý: Xét về tốc độ, kích thước và chi phí kinh tế.
> <!-- answer -->
> 1. **Tốc độ truy xuất (Access Speed)**
> 2. **Dung lượng lưu trữ (Capacity)**
> 3. **Giá thành trên một bit (Cost per bit)**

---

> [!STUDYCARD] id="fc-03-multiprogramming-goal"
> **Mặt trước (Câu hỏi):** Mục tiêu thiết kế tối thượng của Hệ thống Đa chương (Multiprogramming) là gì?
> <!-- hint -->
> Gợi ý: Tận dụng thời gian CPU khi tiến trình phải chờ I/O.
> <!-- answer -->
> **Tối đa hóa hiệu suất khai thác CPU (Maximize CPU Utilization)** bằng cách luôn duy trì một tiến trình sẵn sàng chạy trên CPU khi tiến trình khác chờ thao tác vào/ra (I/O).

---

> [!STUDYCARD] id="fc-04-trap-definition"
> **Mặt trước (Câu hỏi):** Bẫy ngắt (Trap) khác Ngắt phần cứng (Hardware Interrupt) ở điểm cốt lõi nào?
> <!-- hint -->
> Gợi ý: Nguồn gốc phát sinh tín hiệu là từ bên trong CPU hay từ thiết bị ngoại vi.
> <!-- answer -->
> - **Trap (Software Interrupt):** Tín hiệu **đồng bộ** do chính CPU sinh ra khi gặp lỗi lệnh (chia 0, segfault) hoặc do tiến trình gọi System Call.
> - **Hardware Interrupt:** Tín hiệu **bất đồng bộ** do thiết bị phần cứng ngoại vi (bàn phím, đĩa cứng, card mạng) gửi đến CPU qua bus hệ thống.

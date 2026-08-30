# TRẠNG THÁI DỰ ÁN V2 (PROJECT STATE V2)

**Dự án:** CẨM NANG HỆ ĐIỀU HÀNH — IT007 UIT (V2 TRIPLE-PRODUCT EXPANSION)  
**Nhánh Git làm việc:** `v2/complete-theory-labs`  
**Giai đoạn hiện tại:** `V2_CANONICAL_ARCHITECTURE_AND_WEB_PROTOTYPE_LOCKED`  
**Tác giả / Biên soạn:** Võ Trọng Phúc  
**Thời gian cập nhật:** 2026-08-30  

---

## 1. Mô Hình Kiến Trúc Ba Sản Phẩm (Triple-Product Architecture)

Một kho dữ liệu nguồn duy nhất (**Single Source of Truth** tại thư mục `content/`) cung cấp đồng thời cho cả 3 sản phẩm:

```
                               ┌──────────────────────────┐
                               │   CANONICAL DATA TREE    │
                               │        (content/)        │
                               └────────────┬─────────────┘
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
│       BOOK A:         │       │       BOOK B:         │       │      PRODUCT C:       │
│     THEORY BOOK       │       │       LAB BOOK        │       │     WEB COMPANION     │
│   (A4 Print PDF)      │       │    (A4 Print PDF)     │       │   (Digital Garden)    │
│  - Ch01 -> Ch09       │       │  - Lab 1 -> Lab 6     │       │  - Full Search        │
│  - Midterm / Final    │       │  - it007sh Case Study │       │  - Local Graph        │
│  - Deep Explanations  │       │  - POSIX C Specs      │       │  - Active Recall Cards│
└───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

---

## 2. Tình Trạng Nghiên Cứu & Bằng Chứng (Research Deliverables)

| Tệp Nghiên Cứu | Nội Dung Khảo Sát | Trạng Thái |
| :--- | :--- | :---: |
| [`research/CONTENT_ARCHITECTURE_V2.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/CONTENT_ARCHITECTURE_V2.md) | Kiến trúc dữ liệu nguồn đơn nhất `content/` cho Sách Lý Thuyết, Sách Thực Hành và Web. | `LOCKED` |
| [`research/SUBJECTIVE_SOURCE_LEDGER.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/SUBJECTIVE_SOURCE_LEDGER.md) | Sổ tay kiểm kê toàn bộ nguồn câu hỏi tự luận (Tier A, Tier B, Tier C, SVUIT, Duong Computing). | `LOCKED` |
| [`research/SUBJECTIVE_QUESTION_MATRIX.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/SUBJECTIVE_QUESTION_MATRIX.md) | Ma trận 60+ câu hỏi tự luận có barem chấm, key points, bảng so sánh và phân loại taxonomy. | `LOCKED` |
| [`research/SOURCE_LEDGER.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/SOURCE_LEDGER.md) | Danh mục toàn bộ 25 tài liệu Tier A, 8 tiêu chuẩn Tier B và 17 nguồn Tier C. | `LOCKED` |
| [`research/SLIDE_COVERAGE_MATRIX.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/SLIDE_COVERAGE_MATRIX.md) | Ma trận đối chiếu 100% slide Week 1–14 với mục tiêu `MISSING = 0, PARTIAL = 0`. | `LOCKED` |
| [`research/THEORY_COVERAGE_MATRIX.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/THEORY_COVERAGE_MATRIX.md) | Bản đồ cấu trúc 10 chuyên đề Sách Lý Thuyết V2 (Book A). | `LOCKED` |
| [`research/OFFICIAL_REVIEW_QUESTION_MAP.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/OFFICIAL_REVIEW_QUESTION_MAP.md) | Ánh xạ 100% câu hỏi ôn tập chính thức của ThS. Phan Đình Duy & Slide Week 8. | `LOCKED` |
| [`research/EXAM_EVIDENCE_MATRIX.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/EXAM_EVIDENCE_MATRIX.md) | Ma trận bằng chứng 20 đề thi thật UIT (2017–2025) theo taxonomy 14 dạng bài. | `LOCKED` |
| [`research/EXAM_PATTERN_ANALYSIS.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/EXAM_PATTERN_ANALYSIS.md) | Phân tích quy luật, ma trận điểm số và xu hướng đề thi mới nhất. | `LOCKED` |
| [`research/LAB_VARIANT_MAP.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/LAB_VARIANT_MAP.md) | Bản đồ biến thể thực hành Lab 1–6 (Chính thức v2023 `it007sh` vs Lịch sử). | `LOCKED` |
| [`research/LAB_SOURCE_LEDGER.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/LAB_SOURCE_LEDGER.md) | Sổ tay tra cứu 22 System Calls & POSIX APIs chuẩn man7.org. | `LOCKED` |
| [`research/CONTENT_GAP_REPORT.md`](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/CONTENT_GAP_REPORT.md) | Báo cáo chi tiết các khoảng cách học thuật giữa bản thảo V1 và yêu cầu V2. | `LOCKED` |

---

## 3. Tình Trạng Prototype Web Companion (`web/`)

- [x] **Layout 3 Cột (Quartz-inspired):** Sidebar Explorer + Search bên trái, Reading Canvas trung tâm, Local Graph + TOC + Backlinks bên phải.
- [x] **Hệ Thống Thành Phần Tương Tác:**
  - `StudyCard`: Thẻ ghi nhớ Active Recall (Gợi ý, Từ khóa, Lời giải, Lưu trạng thái `localStorage`).
  - `SubjectivePractice`: Khung tự luyện viết câu trả lời, lưu bản nháp, đối chiếu barem chấm và tự tính điểm.
  - `KnowledgeGraph`: Canvas hiển thị đồ thị tri thức ngữ nghĩa cục bộ có tương tác click chuyển trang.
  - `FullTextSearch`: Thanh tìm kiếm nhanh toàn bộ tài liệu (Ctrl+K).
  - `ThemeManager`: Chuyển đổi Dark / Light mode lưu cấu hình trình duyệt.
- [x] **Các Trang Nguyên Mẫu Đã Dựng Hoàn Chỉnh:**
  - Trang chủ (`web/index.html`)
  - Lý thuyết Chương 1 (`web/theory/ch01-overview.html`)
  - Ngân hàng Tự luận Chương 1 (`web/questions/ch01-subjective.html`)
  - Thực hành Lab 1 (`web/labs/lab01-linux-basics.html`)
  - Đề thi Giữa kỳ HK1 2023–2024 (`web/exams/midterm-2023-2024-hk1.html`)
  - Từ điển Thuật ngữ Song ngữ (`web/glossary/index.html`)

# TRẠNG THÁI DỰ ÁN V2 (PROJECT STATE V2)

**Dự án:** CẨM NANG HỆ ĐIỀU HÀNH — IT007 UIT (V2 TRIPLE-PRODUCT EXPANSION)  
**Nhánh Git làm việc:** `v2/complete-theory-labs`  
**Giai đoạn hiện tại (Current Phase):** `V2_FOUNDATION_LOCKED_READY_TO_SCALE_CONTENT`  
**Hành động tiếp theo chính xác (Exact Next Action):** Soạn thảo chính thức các Chương 2–9 (`content/theory/`), Bài Lab 2–6 (`content/labs/`) và các ngân hàng câu hỏi còn lại từ kho bằng chứng đã khóa trong `registry.yaml`.  
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
│   (A4 Print PDF)      │       │    (A4 Print PDF)     │       │   (Quartz 4 SSG)      │
│  - Ch01 -> Ch09       │       │  - Lab 1 -> Lab 6     │       │  - Full Search        │
│  - Midterm / Final    │       │  - it007sh Case Study │       │  - Local Graph        │
│  - Deep Explanations  │       │  - POSIX C Specs      │       │  - Offline KaTeX      │
└───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

---

## 2. Tình Trạng Nghiên Cứu & Khóa Bằng Chứng (Research Deliverables)

| Tệp Nghiên Cứu | Nội Dung Khảo Sát | Trạng Thái |
| :--- | :--- | :---: |
| [`research/CONTENT_ARCHITECTURE_V2.md`](research/CONTENT_ARCHITECTURE_V2.md) | Kiến trúc dữ liệu nguồn đơn nhất `content/` cho Sách Lý Thuyết, Sách Thực Hành và Web. | `SOURCE_VERIFIED` |
| [`research/V2_FOUNDATION_GATE.md`](research/V2_FOUNDATION_GATE.md) | Báo cáo chốt khóa toàn bộ cổng nền tảng sau kiểm toán GLM. | `LOCKED` |
| [`research/RESEARCH_GATE_QA.md`](research/RESEARCH_GATE_QA.md) | Báo cáo kiểm toán nghiên cứu định lượng tự động qua script. | `PASS` |
| [`research/SSOT_BUILD_PROOF.md`](research/SSOT_BUILD_PROOF.md) | Báo cáo thực nghiệm chứng minh cơ chế nguồn đơn nhất tất định. | `PASS` |
| [`research/GLM_V2_ARCHITECTURE_AUDIT.md`](research/GLM_V2_ARCHITECTURE_AUDIT.md) | Nhật ký xử lý 100% các phát hiện kiểm toán GLM (8 Blockers, 7 Majors). | `RESOLVED` |
| [`content/sources/registry.yaml`](content/sources/registry.yaml) | Sổ đăng ký 61 mã định danh tài liệu nguồn bất biến toàn cầu. | `SOURCE_VERIFIED` |
| [`research/SUBJECTIVE_SOURCE_LEDGER.md`](research/SUBJECTIVE_SOURCE_LEDGER.md) | Sổ tay kiểm kê toàn bộ nguồn câu hỏi tự luận (Tier A, Tier B, Tier C). | `SOURCE_VERIFIED` |
| [`research/SUBJECTIVE_QUESTION_MATRIX.md`](research/SUBJECTIVE_QUESTION_MATRIX.md) | Ma trận 60+ câu hỏi tự luận có barem chấm, key points, bảng so sánh và phân loại taxonomy. | `SOURCE_VERIFIED` |
| [`research/SOURCE_LEDGER.md`](research/SOURCE_LEDGER.md) | Danh mục toàn bộ 25 tài liệu Tier A, 8 tiêu chuẩn Tier B và 17 nguồn Tier C. | `SOURCE_VERIFIED` |
| [`research/SLIDE_COVERAGE_MATRIX.md`](research/SLIDE_COVERAGE_MATRIX.md) | Ma trận đối chiếu slide Week 1–14 với mã định danh nguồn bất biến. | `TOPIC_MAPPED` |
| [`research/THEORY_COVERAGE_MATRIX.md`](research/THEORY_COVERAGE_MATRIX.md) | Bản đồ cấu trúc 10 chuyên đề Sách Lý Thuyết V2 (Book A). | `TOPIC_MAPPED` |
| [`research/OFFICIAL_REVIEW_QUESTION_MAP.md`](research/OFFICIAL_REVIEW_QUESTION_MAP.md) | Ánh xạ câu hỏi ôn tập chính thức của ThS. Phan Đình Duy & Slide Week 8. | `SOURCE_VERIFIED` |
| [`research/EXAM_EVIDENCE_MATRIX.md`](research/EXAM_EVIDENCE_MATRIX.md) | Ma trận bằng chứng 20 đề thi thật UIT (2017–2025) theo taxonomy 14 dạng bài. | `SOURCE_VERIFIED` |
| [`research/EXAM_PATTERN_ANALYSIS.md`](research/EXAM_PATTERN_ANALYSIS.md) | Phân tích quy luật, ma trận điểm số và xu hướng đề thi mới nhất. | `SOURCE_VERIFIED` |
| [`research/LAB_VARIANT_MAP.md`](research/LAB_VARIANT_MAP.md) | Bản đồ biến thể thực hành Lab 1–6 (Chính thức v2023 `it007sh` vs Lịch sử). | `SOURCE_VERIFIED` |
| [`research/LAB_SOURCE_LEDGER.md`](research/LAB_SOURCE_LEDGER.md) | Sổ tay tra cứu 22 System Calls & POSIX APIs chuẩn man7.org. | `SOURCE_VERIFIED` |
| [`research/CONTENT_GAP_REPORT.md`](research/CONTENT_GAP_REPORT.md) | Báo cáo chi tiết các khoảng cách học thuật giữa bản thảo V1 và yêu cầu V2. | `SOURCE_VERIFIED` |

---

## 3. Tình Trạng SSOT & Web Companion (`public/site/`)

- [x] **Cơ Chế Biên Dịch Tự Động SSOT (`scripts/build_web.py`):** Toàn bộ trang web trong `public/site/` được sinh tự động 100% từ thư mục `content/`.
- [x] **Layout 3 Cột (Quartz-inspired):** Sidebar Explorer + Search bên trái, Reading Canvas trung tâm, Local Graph + TOC + Backlinks bên phải.
- [x] **Hệ Thống Thành Phần Tương Tác:**
  - `StudyCard`: Thẻ ghi nhớ Active Recall (Gợi ý, Từ khóa, Lời giải, Lưu trạng thái `localStorage`).
  - `SubjectivePractice`: Khung tự luyện viết câu trả lời, lưu bản nháp, đối chiếu barem chấm và tự tính điểm.
  - `KnowledgeGraph`: Canvas hiển thị đồ thị tri thức ngữ nghĩa cục bộ sinh tự động từ frontmatter `related`.
  - `FullTextSearch`: Tìm kiếm toàn văn tức thời từ `search_index.json` sinh động.
  - `ThemeManager`: Chuyển đổi Dark / Light mode lưu cấu hình trình duyệt.
  - `No Remote CDN`: KaTeX / MathJax được phục vụ hoàn toàn ngoại tuyến từ kho lưu trữ.

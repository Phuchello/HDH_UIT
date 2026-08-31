# TRẠNG THÁI DỰ ÁN V2 (PROJECT STATE V2)

**Dự án:** CẨM NANG HỆ ĐIỀU HÀNH — IT007 UIT (V2 TRIPLE-PRODUCT EXPANSION)  
**Nhánh Git làm việc:** `v2/complete-theory-labs`  
**Giai đoạn hiện tại (Current Phase):** `V2_THEORY_BATCH1_DRAFTED_READY_FOR_ENGINEERING_QA`
**Sẵn sàng mở rộng nội dung (Ready to Scale Content):** `YES` (Đã vượt qua cổng kiểm toán nền tảng tự động `scripts/generate_foundation_gate.py`)  
**Hành động tiếp theo chính xác (Exact Next Action):** Terra Medium performs engineering/build regression, then Luna Ultra performs independent academic review.
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
│   (A4 Print PDF)      │       │    (A4 Print PDF)     │       │ (Custom SSG Engine)   │
│  - Ch01 -> Ch09       │       │  - Lab 1 -> Lab 6     │       │  - Full Search        │
│  - Midterm / Final    │       │  - it007sh Case Study │       │  - Local Graph        │
│  - Deep Explanations  │       │  - POSIX C Specs      │       │  - Offline KaTeX      │
└───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

---

## 2. Báo Cáo Kiểm Toán & Khóa Cổng Định Lượng (Machine-Audited Gates)

| Báo Cáo / Tệp Dữ Liệu | Vai Trò & Phương Pháp Kiểm Toán | Trạng Thái |
| :--- | :--- | :---: |
| [`research/V2_FOUNDATION_GATE.md`](research/V2_FOUNDATION_GATE.md) | Báo cáo chốt khóa toàn bộ cổng nền tảng sinh tự động bởi script. | `LOCKED` |
| [`research/RESEARCH_GATE_QA.md`](research/RESEARCH_GATE_QA.md) | Báo cáo kiểm toán nghiên cứu định lượng tự động tính toán 100% từ cấu trúc dữ liệu. | `PASS` |
| [`research/GATE_NEGATIVE_TESTS.md`](research/GATE_NEGATIVE_TESTS.md) | Báo cáo kiểm thử phủ định 11 kịch bản lỗi cố ý (11/11 phát hiện chính xác). | `PASS` |
| [`research/SSOT_BUILD_PROOF.md`](research/SSOT_BUILD_PROOF.md) | Báo cáo thực nghiệm chứng minh cơ chế nguồn đơn nhất tất định. | `PASS` |
| [`research/data/slide_coverage.yaml`](research/data/slide_coverage.yaml) | Dữ liệu cấu trúc 14 slide decks (721 trang vật lý: 665 content, 56 non-content). | `VERIFIED` |
| [`research/data/official_review_questions.yaml`](research/data/official_review_questions.yaml) | Dữ liệu cấu trúc 60 câu hỏi ôn tập chính thức phân theo từng chương. | `VERIFIED` |
| [`research/data/exam_evidence.yaml`](research/data/exam_evidence.yaml) | Dữ liệu cấu trúc 20 hồ sơ đề thi: 1 `RECONSTRUCTED_PRACTICE`, 19 `UNVERIFIED_REFERENCE`, 0 `VERIFIED_ARCHIVE`; có đối soát mã băm/tệp khi khả dụng. | `EVIDENCE-AWARE` |
| [`content/sources/registry.yaml`](content/sources/registry.yaml) | Sổ đăng ký 61 mã định danh tài liệu nguồn bất biến toàn cầu. | `VERIFIED` |
| [`research/GLM_V2_ARCHITECTURE_AUDIT.md`](research/GLM_V2_ARCHITECTURE_AUDIT.md) | Nhật ký xử lý 100% các phát hiện kiểm toán GLM (8 Blockers, 7 Majors). | `RESOLVED` |

---

## 3. Quy Trình Kiểm Thử Tự Động & Lệnh Phát Triển

- **Chạy toàn bộ kiểm thử và cập nhật cổng:** `npm test` (hoặc `npm run validate:v2`)
- **Biên dịch Web tĩnh:** `npm run web:build`
- **Khởi chạy Web cục bộ:** `npm run web:serve`

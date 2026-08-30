# KIẾN TRÚC NỘI DUNG NGUỒN ĐƠN NHẤT V2 (CONTENT ARCHITECTURE V2)
## Single Source of Truth (SSOT) cho Sách Lý Thuyết, Sách Thực Hành và Web Tri Thức

**Dự án:** Cẩm nang Hệ điều hành IT007 UIT — Tái cấu trúc V2  
**Tác giả:** Võ Trọng Phúc  
**Mục tiêu:** Một kho dữ liệu nội dung chuẩn hóa duy nhất (`content/`) cung cấp đồng thời cho cả 3 sản phẩm:
1. **Sách Lý Thuyết A4 PDF / HTML** (Book A: *Hệ điều hành — IT007: Lý thuyết · Bài tập · Ôn thi*)
2. **Sách Thực Hành A4 PDF / HTML** (Book B: *Thực hành Hệ điều hành — IT007: Linux · Process · Thread · IPC · Synchronization · Shell*)
3. **Web Tri Thức Tương Tác** (Product C: *IT007 Interactive Web Companion*)

---

## 1. Nguyên Tắc Cốt Lõi (Core Principles)

```
                       ┌──────────────────────────────────────┐
                       │        CANONICAL CONTENT TREE        │
                       │             (content/)               │
                       │  - Markdown + Frontmatter            │
                       │  - Semantic Wikilinks [[concept]]    │
                       │  - Structured Rubrics & Cards        │
                       │  - Immutable Source Registry         │
                       └──────────────────┬───────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        ▼                                 ▼                                 ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│   PRODUCT A:     │            │   PRODUCT B:     │            │   PRODUCT C:     │
│  THEORY BOOK     │            │    LAB BOOK      │            │  WEB COMPANION   │
│  (A4 Print PDF)  │            │  (A4 Print PDF)  │            │ (Quartz SSG)     │
│  - Deep Theory   │            │  - Lab 1 -> 6    │            │ - Full Search    │
│  - Worked Ex     │            │  - it007sh Study │            │ - Local Graph    │
│  - Review Matrix │            │  - POSIX C Specs │            │ - Offline KaTeX  │
└──────────────────┘            └──────────────────┘            └──────────────────┘
```

1. **Không sao chép song song (Zero Content Duplication):** Mọi nội dung bài học, bài tập tự luận, đề thi, thẻ nhớ và từ điển thuật ngữ chỉ được viết tại một tệp nguồn duy nhất trong `content/`. Thư mục `public/site/` là sản phẩm biên dịch tĩnh (Build Output), tuyệt đối không sửa đổi thủ công.
2. **Ngữ nghĩa hóa siêu dữ liệu (Semantic Frontmatter):** Mọi tệp nội dung đều có phần đầu YAML mô tả định danh (`id`), phân loại (`type`), quan hệ tri thức (`related`), phân loại đề thi (`classification`), nguồn gốc câu hỏi (`answer_provenance`) và liên kết nguồn (`sources`).
3. **Đăng ký nguồn bất biến toàn cầu (`content/sources/registry.yaml`):** Mọi trích dẫn nguồn phải đối chiếu với mã định danh duy nhất (`UIT-SLIDE-CH01-2024`, `POSIX-FORK`, `BHT-EXAM-GK-2023-2024-HK1`). Cấm tuyệt đối các mã mơ hồ cục bộ (`SRC-A01`, `A-01`).
4. **Liên kết hai chiều (Semantic Wikilinks):** Sử dụng cú pháp `[[ten-khai-niem]]` để xây dựng đồ thị tri thức (Knowledge Graph) phục vụ việc tra cứu và gợi ý kiến thức liên quan trên Web. Mọi liên kết phải trỏ tới các trang tài liệu thực sự tồn tại.
5. **Khả chuyển in ấn & hiển thị số (Dual-Render Compatibility):** Các thành phần giao diện mở rộng (như Thẻ ghi nhớ `StudyCard`, Khung tự chấm `SubjectivePractice`, Callouts) được thiết kế theo cú pháp chuẩn để vừa hiển thị tương tác trên Web vừa dàn trang tĩnh hoàn hảo khi xuất PDF A4.
6. **Độc lập ngoại tuyến (Zero Remote Dependencies):** Không tải font hay thư viện toán học từ CDN bên ngoài tại runtime. KaTeX / MathJax được đóng gói sẵn trong kho mã nguồn.

---

## 2. Cấu Trúc Cây Thư Mục Nguồn `content/`

```
content/
├── theory/                                # Nội dung Sách Lý Thuyết & Chuyên đề
│   ├── 00-intro.md                        # Phần 0: Nền tảng C/POSIX & Bản đồ IT007
│   ├── ch01-overview.md                   # Chương 1: Tổng quan & Kiến trúc Máy tính
│   ├── ch02-structure.md                  # Chương 2: Cấu trúc HDH, Dịch vụ & System Calls
│   ├── ch03-process.md                    # Chương 3: Quản lý Tiến trình, Luồng & IPC
│   ├── ch04-cpu-scheduling.md             # Chương 4: Định thời CPU & Hệ thống Đa xử lý
│   ├── midterm-review.md                  # Ôn tập Giữa kỳ tổng hợp
│   ├── ch05-synchronization.md            # Chương 5: Đồng bộ Tiến trình & Bài toán kinh điển
│   ├── ch06-deadlock.md                   # Chương 6: Deadlock & Thuật toán Banker
│   ├── ch07-memory-management.md          # Chương 7: Quản lý Bộ nhớ, Phân trang & TLB
│   ├── ch08-virtual-memory.md             # Chương 8: Bộ nhớ ảo & Thay thế trang
│   ├── ch09-linux-windows.md              # Chương 9: Kiến trúc Nhân Linux & Windows
│   └── final-review.md                    # Ôn tập Cuối kỳ tổng hợp
│
├── labs/                                  # Hướng dẫn Sách Thực Hành Lab
│   ├── 00-setup-environment.md            # Hướng dẫn cài đặt Ubuntu/WSL2 & GCC Toolchain
│   ├── lab01-linux-basics.md              # Lab 1: Linux FHS & Quản trị tệp tin
│   ├── lab02-shell-scripting.md           # Lab 2: Lập trình Bash Shell
│   ├── lab03-process-management.md        # Lab 3: Quản lý Tiến trình & System Calls C
│   ├── lab04-threads-ipc.md               # Lab 4: Đa luồng POSIX Threads & IPC
│   ├── lab05-synchronization.md           # Lab 5: Đồng bộ hóa Mutex & Semaphore
│   └── lab06-it007sh-shell.md             # Lab 6: Xây dựng Shell it007sh hoàn chỉnh (7 giai đoạn)
│
├── questions/                             # Ngân Hàng Câu Hỏi Tự Luyện & Đánh Giá
│   ├── subjective/                        # Ngân hàng câu hỏi tự luận theo từng chương
│   │   ├── ch01.md -> ch09.md
│   │   ├── midterm.md
│   │   └── final.md
│   ├── mcq/                               # Trắc nghiệm lý thuyết & điền từ ngắn
│   └── calculations/                      # Bài tập tính toán step-by-step
│
├── exams/                                 # Lưu trữ đề thi thật & Đề thi mô phỏng
│   ├── midterm/                           # Đề thi Giữa kỳ (2018 - 2025)
│   └── final/                             # Đề thi Cuối kỳ (2017 - 2025)
│
├── flashcards/                            # Dữ liệu thẻ nhớ Active Recall
├── glossary/                              # Từ điển thuật ngữ song ngữ Anh - Việt
│   └── terms.md
└── sources/                               # Sổ đăng ký nguồn bất biến
    └── registry.yaml
```

---

## 3. Kiến Trúc Biên Dịch & Quy Trình Phát Triển (Build Pipeline)

```
+-------------------------------------------------------------+
|                      content/ (Markdown)                    |
+------------------------------+------------------------------+
                               |
               +---------------+---------------+
               |                               |
               v                               v
+------------------------------+ +------------------------------+
|   PDF & Print HTML Pipeline  | |     Quartz Web Generator     |
|     (scripts/build.js)       | |    (scripts/build_web.py)    |
+--------------+---------------+ +--------------+---------------+
               |                               |
               v                               v
+------------------------------+ +------------------------------+
|            dist/             | |        public/site/          |
|  - Book A: Theory A4 PDF     | |  - Static HTML Pages         |
|  - Book B: Lab A4 PDF        | |  - search_index.json         |
|                              | |  - graph_data.json           |
+------------------------------+ +------------------------------+
```

### Bộ Lệnh Chuẩn (Standard Commands):
- **Cài đặt phụ thuộc:** `npm install`
- **Biên dịch Web:** `npm run web:build` (hoặc `python scripts/build_web.py`)
- **Khởi chạy Web cục bộ:** `npm run web:serve` (hoặc `python -m http.server 8080 --directory public/site`)
- **Xác thực toàn bộ quy chuẩn:** `npm run validate`

---

## 4. Bộ Tiêu Chuẩn Kiểm Thử Tự Động (Validation Suite)

Mỗi lần cập nhật nội dung, hệ thống bắt buộc phải vượt qua 4 chốt kiểm tra:
1. `python scripts/validate_sources.py`: Đảm bảo 100% mã trích dẫn nguồn tồn tại trong `registry.yaml`, không có ID trùng lặp.
2. `python scripts/check_public_hygiene.py`: Đảm bảo 0 đường dẫn máy trạm hoặc công cụ AI bị rò rỉ trong kho mã nguồn.
3. `python scripts/validate_v2_content.py`: Kiểm tra tính toàn vẹn của schema đề thi, rubric tự chấm điểm và liên kết nội bộ.
4. `python scripts/build_web.py`: Biên dịch tất định toàn bộ trang web không có lỗi liên kết chết.

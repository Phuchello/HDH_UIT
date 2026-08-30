# KIẾN TRÚC NỘI DUNG NGUỒN ĐƠN NHẤT V2 (CONTENT ARCHITECTURE V2)
## Single Source of Truth (SSOT) cho Sách Lý Thuyết, Sách Thực Hành và Web Companion

**Dự án:** Cẩm nang Hệ điều hành IT007 UIT — Tái cấu trúc V2  
**Tác giả:** Võ Trọng Phúc  
**Mục tiêu:** Một kho dữ liệu nội dung chuẩn hóa duy nhất (`content/`) cung cấp đồng thời cho cả 3 sản phẩm:
1. **Sách Lý Thuyết A4 PDF / HTML** (Book A: *Hệ điều hành — IT007: Lý thuyết · Bài tập · Ôn thi*)
2. **Sách Thực Hành A4 PDF / HTML** (Book B: *Thực hành Hệ điều hành — IT007: Linux · Process · Thread · IPC · Synchronization · Shell*)
3. **Web Tri Thức Tương Tác** (Product C: *IT007 Interactive Web Companion & Digital Garden*)

---

## 1. Nguyên Tắc Cốt Lõi (Core Principles)

```
                       ┌──────────────────────────────────────┐
                       │        CANONICAL CONTENT TREE        │
                       │             (content/)               │
                       │  - Markdown + Frontmatter            │
                       │  - Semantic Wikilinks [[concept]]    │
                       │  - Structured Rubrics & Cards        │
                       └──────────────────┬───────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        ▼                                 ▼                                 ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│   PRODUCT A:     │            │   PRODUCT B:     │            │   PRODUCT C:     │
│  THEORY BOOK     │            │    LAB BOOK      │            │  WEB COMPANION   │
│  (A4 Print PDF)  │            │  (A4 Print PDF)  │            │ (Quartz Garden)  │
│  - Deep Theory   │            │  - Lab 1 -> 6    │            │ - Full Search    │
│  - Worked Ex     │            │  - it007sh Study │            │ - Local Graph    │
│  - Review Matrix │            │  - POSIX C Specs │            │ - Study Cards    │
└──────────────────┘            └──────────────────┘            └──────────────────┘
```

1. **Không sao chép song song (Zero Content Duplication):** Nội dung chương, câu hỏi tự luận, đề thi, flashcard và từ điển thuật ngữ chỉ được viết tại một tệp nguồn duy nhất trong `content/`.
2. **Ngữ nghĩa hóa siêu dữ liệu (Semantic Frontmatter):** Mọi tệp nội dung đều có phần đầu YAML mô tả định danh (`id`), phân loại (`type`), độ ưu tiên thi cử (`exam_relevance`), quan hệ tri thức (`related`, `prerequisites`) và liên kết nguồn (`sources`).
3. **Liên kết hai chiều (Semantic Wikilinks):** Sử dụng cú pháp `[[ten-khai-niem]]` để xây dựng đồ thị tri thức (Knowledge Graph) phục vụ việc tra cứu và gợi ý kiến thức liên quan trên Web Companion.
4. **Khả chuyển in ấn & hiển thị số (Dual-Render Compatibility):** Các thành phần giao diện mở rộng (như Hộp so sánh, Worked Example, Thẻ ghi nhớ `StudyCard`, Khung tự chấm `SubjectivePractice`) được thiết kế theo cú pháp chuẩn để vừa hiển thị tương tác trên Web vừa dàn trang tĩnh hoàn hảo khi xuất PDF A4.

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
├── labs/                                  # Nội dung Sách Thực Hành & Case Study
│   ├── 00-environment.md                  # Hướng dẫn Môi trường Linux/WSL/GCC/GDB
│   ├── lab01-linux-basics.md              # Lab 1: Lệnh Linux & Quản trị Hệ thống tệp
│   ├── lab02-shell-scripting.md           # Lab 2: Lập trình Shell Script (Bash)
│   ├── lab03-process-management.md        # Lab 3: Lập trình Tiến trình & Tín hiệu Signal
│   ├── lab04-threads-ipc.md               # Lab 4: Đa luồng POSIX Threads & Shared Memory
│   ├── lab05-synchronization.md           # Lab 5: Đồng bộ hóa Semaphore & Mutex Lock
│   ├── lab06-it007sh.md                   # Lab 6: Xây dựng Trình thông dịch lệnh it007sh (7 giai đoạn)
│   └── appendix-memory-simulation.md      # Phụ lục: Mô phỏng Thuật toán Thay thế trang
│
├── questions/                             # Ngân hàng Câu hỏi Chuẩn hóa
│   ├── subjective/                        # Câu hỏi Tự luận có Barem chấm & Key points
│   │   ├── ch01-subjective.md
│   │   ├── ch02-subjective.md
│   │   ├── ch03-subjective.md
│   │   ├── ch04-subjective.md
│   │   ├── ch05-subjective.md
│   │   ├── ch06-subjective.md
│   │   ├── ch07-subjective.md
│   │   ├── ch08-subjective.md
│   │   ├── ch09-subjective.md
│   │   ├── midterm-subjective.md
│   │   └── final-subjective.md
│   ├── mcq/                               # Trắc nghiệm, Đúng/Sai, Điền thuật ngữ tiếng Anh
│   │   ├── ch01-mcq.md ... ch09-mcq.md
│   │   └── english-terms-mcq.md
│   └── calculations/                      # Các dạng Bài tập Tính toán có Lời giải
│       ├── process-state-trace.md
│       ├── fork-tree-problems.md
│       ├── cpu-scheduling-gantt.md
│       ├── synchronization-code.md
│       ├── banker-safety-request.md
│       ├── memory-placement-eat.md
│       └── page-replacement-tables.md
│
├── exams/                                 # Lưu trữ Đề thi Thật & Đề Mô phỏng
│   ├── midterm/                           # Đề thi Giữa kỳ (2018–2025)
│   │   ├── 2023-2024-hk1.md
│   │   ├── 2024-2025-hk1.md
│   │   └── mock-midterm-01.md
│   ├── final/                             # Đề thi Cuối kỳ (2017–2025)
│   │   ├── 2023-2024-hk1.md
│   │   ├── 2024-2025-hk1.md
│   │   ├── mock-final-01.md
│   │   └── mock-final-02.md
│   └── patterns/                          # Phân tích Ma trận Đề thi & Quy luật chấm điểm
│       └── exam-trend-analysis.md
│
├── flashcards/                            # Dữ liệu Thẻ nhớ Active Recall
│   ├── ch01-flashcards.md ... ch09-flashcards.md
│   └── high-yield-formula-cards.md
│
├── glossary/                              # Từ điển Thuật ngữ Song ngữ Anh - Việt
│   └── os-terms-dictionary.md
│
└── sources/                               # Chỉ mục Tài liệu Trích dẫn & Đối chiếu
    ├── tier-a-official-sources.md
    ├── tier-b-technical-specs.md
    └── tier-c-exam-evidence.md
```

---

## 3. Đặc Tả Cú Pháp Frontmatter Chuẩn Hóa

### A. Tệp Chuyên đề Lý thuyết (`content/theory/*.md`)
```yaml
---
id: "theory-ch01-overview"
title: "Chương 1: Tổng quan về Hệ điều hành & Kiến trúc Máy tính"
book: "theory"
chapter: 1
order: 1
slug: "ch01-overview"
summary: "Định nghĩa HDH, kiến trúc phân tầng, cơ chế ngắt, phân cấp bộ nhớ, đa xử lý, chế độ kép Dual-Mode và các môi trường tính toán."
prerequisites: ["theory-00-intro"]
related:
  - "theory-ch02-structure"
  - "theory-ch03-process"
  - "glossary-dual-mode"
  - "glossary-interrupt"
exam_relevance:
  midterm_weight: "20%"
  final_weight: "5%"
  frequent_topics:
    - "Phân biệt User mode vs Kernel mode"
    - "Cơ chế xử lý ngắt và bảng véc-tơ IVT"
    - "Phân cấp bộ nhớ và 3 tiêu chí phân cấp"
    - "Lệnh đặc quyền vs Lệnh không đặc quyền"
sources:
  - "A-02 (Week01-Chapter1 2024.pdf)"
  - "A-16 (Cau hoi chuong 1 HDH.docx)"
  - "B-01 (Silberschatz Ch1)"
last_updated: "2026-08-30"
---
```

### B. Tệp Câu hỏi Tự luận (`content/questions/subjective/*.md`)
```yaml
---
id: "sub-q01-08"
chapter: 1
question_type: "EXPLAIN"
question: "Trình bày bản chất của chế độ hoạt động kép (Dual-Mode Operation) trong hệ điều hành? Phân biệt User Mode và Kernel Mode. Nêu ví dụ về 4 lệnh đặc quyền."
source_id: "A-02 / A-16"
source_locator: "Slide W01: 38-46; Cau hoi Ch1: Mục 8"
exam_evidence:
  frequency: "REPEATED PATTERN"
  observed_in: ["GK 2018-2019", "GK 2020-2021", "GK 2022-2023", "GK 2024-2025"]
difficulty: "MEDIUM"
core_concepts:
  - "[[dual-mode]]"
  - "[[mode-bit]]"
  - "[[privileged-instructions]]"
  - "[[system-call]]"
---
```

---

## 4. Đặc Tả Các Khối Giao Diện Mở Rộng (Custom UI / Callout Blocks)

Để hỗ trợ cả rendering Web lẫn in ấn PDF A4, các thành phần sư phạm được định nghĩa theo cú pháp Markdown Callouts chuẩn GitHub Flavored Markdown có mở rộng:

### 1. Bảng Đặc tính Khái niệm (`> [!CHARACTERISTICS]`)
```markdown
> [!CHARACTERISTICS]
> ### Đặc tính: Chế độ hoạt động kép (Dual-Mode)
> - **Mục đích:** Bảo vệ tài nguyên phần cứng, ngăn chương trình người dùng phá hoại hoặc độc chiếm hệ thống.
> - **Cơ chế:** Dựa vào `Mode bit` do phần cứng CPU quản lý (0: Kernel Mode, 1: User Mode).
> - **Ưu điểm:** Hệ thống ổn định, an toàn, cô lập lỗi giữa các ứng dụng.
> - **Nhược điểm:** Phí tổn chuyển đổi chế độ (Mode switch latency) khi thực thi System Call.
> - **Cam kết (Guarantees):** Lệnh đặc quyền chỉ chạy được khi Mode bit = 0.
> - **Không cam kết (Non-guarantees):** Không tự động bảo vệ lỗi logic bên trong chính ứng dụng người dùng.
```

### 2. Thẻ Tự Học & Active Recall (`> [!STUDYCARD]`)
```markdown
> [!STUDYCARD] id="card-mode-switch"
> **Câu hỏi:** Mode Switch khác Context Switch ở những điểm cốt lõi nào?
> <!-- hint -->
> Gợi ý: Xét không gian địa chỉ tiến trình và việc nạp lại PCB.
> <!-- keypoints -->
> - [ ] Mode switch chỉ đổi Mode bit (User <-> Kernel), vẫn chạy trên cùng tiến trình.
> - [ ] Context switch chuyển đổi quyền CPU sang tiến trình khác, phải lưu/nạp lại toàn bộ PCB.
> - [ ] Chi phí: Mode switch rất nhẹ; Context switch nặng hơn rất nhiều (ảnh hưởng cache/TLB).
> <!-- answer -->
> Mode switch xảy ra khi tiến trình gọi System Call hoặc có ngắt, CPU chuyển sang Kernel mode để thực thi dịch vụ nhưng vẫn nằm trong ngữ cảnh của tiến trình đó. Context switch xảy ra khi bộ định thời đổi sang tiến trình mới, buộc HDH phải lưu trạng thái của P1 vào PCB1 và khôi phục trạng thái P2 từ PCB2.
```

### 3. Khung Luyện Tập Tự Luận & Barem Chấm Tự Động (`> [!SUBJECTIVEPRACTICE]`)
```markdown
> [!SUBJECTIVEPRACTICE] id="prac-q03-process-thread"
> **Đề bài:** So sánh Tiến trình (Process) và Tiểu trình (Thread) theo 4 tiêu chí: Không gian địa chỉ, Tài nguyên sở hữu, Đơn vị định thời, và Chi phí chuyển ngữ cảnh.
>
> <!-- rubric max_score=2.0 -->
> - **[0.5 điểm] Không gian địa chỉ:** Process có không gian nhớ ảo độc lập; Threads trong cùng tiến trình chia sẻ chung Code, Data, Heap.
> - **[0.5 điểm] Tài nguyên:** Process sở hữu tài nguyên riêng (files mở, bộ nhớ); Threads chỉ sở hữu riêng Stack, Registers, PC, Thread ID.
> - **[0.5 điểm] Định thời:** Thread là đơn vị cơ bản để CPU định thời thực thi (Basic unit of CPU utilization).
> - **[0.5 điểm] Chi phí chuyển ngữ cảnh:** Chuyển ngữ cảnh Thread nhanh và nhẹ hơn nhiều so với Process vì không phải đổi bảng trang và xả cache.
```

---

## 5. Kiến Trúc Pipeline Biên Dịch Đa Xuất Xưởng (Multi-Target Build Pipeline)

```
                              ┌────────────────────────┐
                              │    content/ (SSOT)     │
                              └───────────┬────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
      ┌───────────────────────┐                       ┌───────────────────────┐
      │  WEB COMPANION SSG    │                       │  BOOK COMPILER (CLI)  │
      │  - Parse Markdown/YAML│                       │  - Order by chapter   │
      │  - Build Search Index │                       │  - Resolve Wikilinks  │
      │  - Gen Semantic Graph │                       │  - Inject Offline Math│
      │  - Client-Side React/ │                       │  - Two-Pass TOC Map   │
      │    Vanilla JS Modules │                       │  - Playwright PDF Gen │
      └───────────┬───────────┘                       └───────────┬───────────┘
                  ▼                                               ▼
      ┌───────────────────────┐                       ┌───────────────────────┐
      │   web/dist (Static)   │                       │   dist/BOOK_A.pdf     │
      │   - Interactive App   │                       │   dist/BOOK_B.pdf     │
      │   - LocalStorage State│                       │   (Publication Grade) │
      └───────────────────────┘                       └───────────────────────┘
```

1. **Web Companion Target:**
   - Đọc cây thư mục `content/`.
   - Sinh cây thư mục tệp tĩnh HTML/JS/CSS với thanh công cụ bên trái (Explorer + Search), nội dung học tập trung tâm, và thanh trắc nghiệm/bản đồ tri thức bên phải.
   - Tích hợp KaTeX hiển thị công thức offline, Highlight.js tô màu cú pháp C/Bash, và Cytoscape.js / D3.js hiển thị đồ thị tri thức ngữ nghĩa.
   - Quản lý trạng thái tiến độ tự học của sinh viên qua `localStorage` trên trình duyệt (hoàn toàn riêng tư, không cần máy chủ backend).

2. **Book A & Book B Target:**
   - Tập hợp các tệp `content/theory/*.md` thành ấn phẩm **Sách Lý Thuyết A4**.
   - Tập hợp các tệp `content/labs/*.md` thành ấn phẩm **Sách Thực Hành A4**.
   - Kế thừa động cơ in ấn CSS A4 đã được kiểm duyệt vi phẫu ở bản phát hành V1, đảm bảo không có trang ngắt vụn và mục lục khớp số trang chính xác 100%.

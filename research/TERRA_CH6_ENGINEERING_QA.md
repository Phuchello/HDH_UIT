# BÁO CÁO THẨM ĐỊNH KỸ THUẬT CHƯƠNG 6 — TERRA ENGINEERING QA
# HDH_UIT V2 — CHAPTER 6 INDEPENDENT ENGINEERING QA CLOSEOUT

**Người thực hiện:** Terra Medium (Build / Renderer / Structural QA Engineer)  
**Thời gian:** 2026-09-03  
**Chế độ thẩm định:** `ENGINEERING QA ONLY — NO ACADEMIC REWRITE`  
**Trạng thái kiểm tra chung:** **PASS (ALL GATES PASSED)**  

---

## 1. REVIEWED HEAD & BASELINE

- **Starting Remote HEAD:** `8151088819e56fe24757cb317fcfdc431b7b8761`
- **Branch:** `v2/complete-theory-labs`
- **Locked Academic Baseline:**
  - Chapter 6 Source Map: `VERIFIED / LOCKED`
  - Chapter 6 Authoring: `CONTENT_DRAFTED`
  - Resolved Academic Findings: `ACAD-CH6-001`, `ACAD-CH6-002`, `PROV-CH6-001`, `VALIDATOR-CH6-001`
  - Locked Chapters 1–5: Nguyên vẹn 100% (0 changed files since baseline `06e4b34ef14d60398e462e437470bb6a37157996`)

---

## 2. SCOPE

Thẩm định độc lập toàn diện về mặt kỹ thuật, kiến trúc build, bộ sinh web tĩnh (custom static generator `scripts/build_web.py`), chất lượng DOM/HTML xuất bản, tính toàn vẹn của chỉ mục tìm kiếm và đồ thị tri thức cho Chương 6 (Bế tắc - Deadlock):
1. Xác nhận dứt điểm khiếm khuyết khối code chưa đóng (`ENG-CH6-003`).
2. Tái hiện, phân tích nguyên nhân gốc, sửa chữa kiến trúc slug và viết test cho lỗi trùng lặp HTML ID (`ENG-CH6-004`).
3. Tái hiện, sửa chữa bộ phân tích cú pháp nội dòng `inline()` để hiển thị đúng liên kết in đậm `**[label](url)**` (`ENG-CH6-005`).
4. Tái hiện, khắc phục hiện tượng escape HTML hai lần (`&amp;amp;`) trong mục lục TOC (`ENG-CH6-006`).
5. Kiểm thử hồi quy toàn cục bộ sinh web (`scripts/stress_test_web_renderer.py`, `scripts/validate_site_routes.py`, `scripts/verify_html_integrity.py`).

---

## 3. ENG-CH6-003 CONFIRMATION (Unclosed Code Fence)

- **Trạng thái:** **RESOLVED & VERIFIED**
- **Xác nhận:**
  - Khối fenced code ASCII diagram tại mục 6.3 trong `content/theory/ch06-deadlock.md` đã được đóng chính xác bằng ` ``` ` trước hộp thoại `> [!NOTE]`.
  - Bộ kiểm tra `scripts/validate_ch06_content.py` đã được tích hợp bộ lọc kiểm tra cân bằng số lượng code fence (`len(fences) % 2 == 0`).
  - Trong tệp HTML xuất bản `public/site/theory/ch06-deadlock.html`, tiêu đề `<h2 id="6-4-ngan-chan-be-tac-deadlock-prevention">` và hộp thoại `<div class="callout note">` được render chuẩn mực thành các phần tử DOM độc lập, không bị nuốt vào khối `<pre><code>`.

---

## 4. ENG-CH6-004 — MAJOR — OPEN -> RESOLVED (Duplicate Generated Heading IDs)

### A. Tái hiện (Reproduction):
Trong `public/site/questions/subjective/ch06.html`, mỗi câu hỏi trong số 15 đơn vị câu hỏi đều tái sử dụng các tiêu đề cố định:
- `#### 1. Đề bài gốc (Source Question)`
- `#### 2. Lời giải chuẩn mực (Handbook Solution)`
- `#### 3. Rubric tự kiểm tra của handbook (Self-Check Rubric)`
- `#### 4. Bẫy đề thi & Lưu ý thực tế (Pitfalls & Practical Advice)`

Hàm `slugify(title)` trước đây được gọi trực tiếp mà không theo dõi các slug đã xuất hiện trong tài liệu. Kết quả: `id="1-e-bai-goc-source-question"` xuất hiện lặp lại 15 lần trong cùng một trang HTML, vi phạm chuẩn W3C HTML và gây xung đột định tuyến anchor.

### B. Nguyên nhân gốc (Root Cause):
Trong hàm `markdown_to_html()` của `scripts/build_web.py`, quá trình gán ID tiêu đề chỉ đơn thuần chuyển đổi tiêu đề thành slug mà không có trạng thái lưu vết (seen slugs registry) theo phạm vi từng trang (per-document scope).

### C. Giải pháp khắc phục (Fix):
Cải tiến hàm `markdown_to_html()` trong `scripts/build_web.py`:
1. Khởi tạo từ điển `seen_slugs = {}` ở đầu mỗi lượt render trang.
2. Với mỗi tiêu đề có `base_slug = slugify(title)`:
   - Lần đầu xuất hiện: gán `heading_id = base_slug`, lưu `seen_slugs[base_slug] = 1`.
   - Các lần xuất hiện tiếp theo: tự động đánh chỉ số tăng dần `base_slug-2`, `base_slug-3`, ... kèm vòng lặp kiểm tra tránh xung đột với các tiêu đề đã có sẵn hậu tố số tương ứng.
3. Giải pháp mang tính hệ thống toàn cục, áp dụng tự động cho mọi trang Markdown trong dự án.

### D. Kiểm thử hồi quy (Regression Test):
- Tích hợp kiểm tra trùng lặp ID vào `scripts/validate_site_routes.py` thông qua `LinkParser.duplicate_ids`. Nếu bất kỳ trang HTML nào có `id` trùng lặp, bài kiểm tra sẽ báo lỗi lập tức.
- Thêm kiểm tra `fixture HTML IDs are strictly unique` và `fixture repeated subsection slug disambiguation` trong `scripts/stress_test_web_renderer.py`.
- Tạo công cụ kiểm định chuyên dụng `scripts/verify_html_integrity.py`.
- **Kết quả thực tế:** `questions/subjective/ch06.html` có 0 ID trùng lặp trên tổng số 97 ID. Các ID được phân tách hoàn hảo: `1-e-bai-goc-source-question`, `1-e-bai-goc-source-question-2`, v.v.

---

## 5. ENG-CH6-005 — MAJOR — OPEN -> RESOLVED (Bold-Wrapped Markdown Link Not Rendered)

### A. Tái hiện (Reproduction):
Tại cuối bài lý thuyết `content/theory/ch06-deadlock.md`:
```markdown
👉 **[Ngân hàng Câu hỏi Tự luận & Bài tập Chương 6](../../questions/subjective/ch06.md)**
```
Trang HTML xuất bản hiển thị cú pháp thô bên trong thẻ `<strong>`:
```html
👉 <strong>[Ngân hàng Câu hỏi Tự luận &amp; Bài tập Chương 6](../../questions/subjective/ch06.md)</strong>
```
Người đọc không thể nhấp vào liên kết vì không có thẻ `<a>`.

### B. Nguyên nhân gốc (Root Cause):
Hàm `inline()` trong `scripts/build_web.py` trước đây chỉ hỗ trợ cú pháp Wikilink `[[target|label]]`, hoàn toàn không có bộ xử lý cho cú pháp liên kết chuẩn Markdown `[label](url)`. Cú pháp in đậm `\*\*(.+?)\*\*` được áp dụng, đóng băng đoạn văn bản liên kết Markdown dạng thô thành nội dung của thẻ `<strong>`.

### C. Giải pháp khắc phục (Fix):
Bổ sung bộ xử lý liên kết chuẩn Markdown `mdlink` vào hàm `inline()` trong `scripts/build_web.py` trước bước phân tích `**bold**`:
1. Regex `r"\[([^\]]+)\]\(([^)]+)\)"` bắt cặp `[label](target)`.
2. Hàm `mdlink()` tự động chuẩn hóa đường dẫn tương đối, giải quyết đuôi `.md` thành `.html`, ánh xạ qua bảng `routes` toàn cục để tính toán đường dẫn tương đối tối ưu nhất (ví dụ `../../questions/subjective/ch06.md` từ `theory/ch06-deadlock.html` được chuyển thành `../questions/subjective/ch06.html`).
3. Chuỗi sau khi được biến đổi thành `**<a href="...">label</a>**` tiếp tục đi qua bộ phân tích `**bold**` để trở thành `<strong><a href="...">label</a></strong>`.

### D. Kiểm thử hồi quy (Regression Test):
- Thêm bài test `test_bold_wrapped_link()` và kiểm tra trong `scripts/stress_test_web_renderer.py` với fixture `👉 **[Ngân hàng liên kết đậm](../questions/fixture-questions.md)**`.
- Kiểm tra trực tiếp trên `public/site/theory/ch06-deadlock.html`: xác nhận thẻ `<a href="../questions/subjective/ch06.html">Ngân hàng Câu hỏi Tự luận &amp; Bài tập Chương 6</a>` xuất hiện bên trong thẻ `<strong>`, không còn ký tự `[Ngân hàng` thô nào.

---

## 6. ENG-CH6-006 — MINOR — OPEN -> RESOLVED (TOC Double HTML Escaping)

### A. Tái hiện (Reproduction):
Trong mục lục TOC của `public/site/theory/ch06-deadlock.html`, tiêu đề chứa ký tự `&`:
`Bộ Câu Hỏi Ôn Tập & Rèn Luyện Tư Duy`
bị hiển thị thành:
`&amp;amp;` trong mã nguồn HTML, và hiển thị trên giao diện người dùng thành chữ `&amp;` thay vì `&`.

### B. Nguyên nhân gốc (Root Cause):
Tại dòng 542 của `scripts/build_web.py`, mục lục TOC được trích xuất từ chuỗi `rendered` (đã qua xử lý `inline()`, trong đó `&` đã được escape thành `&amp;`). Đoạn mã sinh TOC sau đó lại gọi `html.escape(m.group(2))` một lần nữa, dẫn đến việc `&amp;` bị escape thành `&amp;amp;`.

### C. Giải pháp khắc phục (Fix):
Tại bước sinh TOC trong hàm `page()` của `scripts/build_web.py`, thiết lập hàm `format_toc_label(raw_html)`:
1. Loại bỏ các thẻ HTML nội dòng (nếu có trong tiêu đề) bằng `re.sub(r"<[^>]+>", "", raw_html)`.
2. Gọi `html.unescape()` để hoàn nguyên các thực thể đã escape về dạng ký tự gốc.
3. Gọi `html.escape()` đúng 1 lần duy nhất trên chuỗi ký tự thuần.
Biện pháp này đảm bảo:
- Thoát ký tự chuẩn mực (`&` -> `&amp;`, `<` -> `&lt;`, `>` -> `&gt;`, `"` -> `&quot;`).
- Triệt tiêu hoàn toàn nguy cơ XSS.
- Không bao giờ xảy ra lỗi double escaping `&amp;amp;`.

### D. Kiểm thử hồi quy (Regression Test):
- Thêm kiểm tra `fixture TOC ampersand single escaping` trong `scripts/stress_test_web_renderer.py`.
- Tích hợp kiểm tra toàn bộ 18 trang HTML trong `scripts/verify_html_integrity.py`: 0 lỗi `&amp;amp;` trên toàn site.

---

## 7. THEORY ROUTE INSPECTION (`public/site/theory/ch06-deadlock.html`)

- **HTML ID Uniqueness:** 100% duy nhất, 0 trùng lặp.
- **TOC Links:** Toàn bộ các thẻ `<a class="toc-link" href="#...">` đều phân giải chính xác đến một phần tử tiêu đề có ID tương ứng trong trang.
- **Raw Markdown Artifacts:** Quét sạch toàn bộ các ký tự rò rỉ: 0 raw `##`, 0 raw `###`, 0 raw `[...](...)`.
- **Callouts & Blocks:** Tất cả 6 callout (`studycard`, `note`, `important`, `warning`, `tip`) đều được bao bọc và đóng thẻ hợp lệ (`<div class="callout ...">...</div>`).
- **MathJax Delimiters:** 44 công thức MathJax khối (`$$...$$`) và các công thức nội dòng (`$...$`) được giữ nguyên vẹn cấu trúc cho thư viện MathJax xử lý.
- **Liên kết điều hướng:** Liên kết chuyển sang ngân hàng câu hỏi tự luận hoạt động hoàn hảo: `href="../questions/subjective/ch06.html"`.

---

## 8. QBANK ROUTE INSPECTION (`public/site/questions/subjective/ch06.html`)

- **Ranh giới 15 câu hỏi (QBANK-CH06-01 đến 15):** Toàn bộ 15 đơn vị câu hỏi đều hiện diện đầy đủ, cấu trúc rõ ràng với các thẻ H3 riêng biệt.
- **Phân tách ID tiêu đề trùng lặp:** 97 ID trên toàn trang đều duy nhất. Các tiêu đề lặp lại như `1. Đề bài gốc` hay `3. Rubric tự kiểm tra` được sinh tự động thành `1-e-bai-goc-source-question`, `1-e-bai-goc-source-question-2`, v.v.
- **Bảng ma trận giải thuật Banker (Q12–15):** 17 bảng HTML (`<table>`) render ngoài khối code, hiển thị bảng ma trận `Allocation`, `Max`, `Need`, `Available` trực quan, đẹp mắt và không làm vỡ bố cục tài liệu.
- **Tính toán 24 chuỗi an toàn (Q11):** Bảng phân tích và danh sách chuỗi an toàn hiển thị mạch lạc, không bị tràn khung hay lỗi định dạng.

---

## 9. TOC / ANCHOR INSPECTION

- **Same-page anchor resolution:** `validate_site_routes.py` xác nhận 0 liên kết neo bị hỏng trên 18 trang HTML.
- **TOC Display:** Hiển thị đúng ký tự `&` trực quan cho tiêu đề `Bộ Câu Hỏi Ôn Tập & Rèn Luyện Tư Duy`, không còn hiện tượng hiển thị mã thực thể `&amp;`.

---

## 10. SEARCH / GRAPH / ROUTE INSPECTION

- **`search_index.json`:**
  - Chứa đầy đủ 2 tài liệu Chương 6: `theory/ch06-deadlock` và `questions/subjective/ch06`.
  - Văn bản tìm kiếm (`searchable_text`) được làm sạch các thẻ code/markdown, hỗ trợ tìm kiếm toàn văn offline.
- **`graph_data.json`:**
  - Các nút `theory/ch06-deadlock` và `questions/subjective/ch06` được tạo lập trong đồ thị tri thức với tọa độ hợp lệ và liên kết chuẩn.

---

## 11. GLOBAL RENDERER REGRESSION RESULTS

Đã chạy toàn bộ bộ kiểm thử hồi quy trên các trang hiện có (Chương 1 đến 5, Review, Lab, Exam, Glossary):
- Các trang hiện hữu giữ nguyên ngữ nghĩa học thuật 100%.
- Không có bất kỳ tác dụng phụ nào làm thay đổi nội dung các chương 1–5 đã khóa.
- `scripts/stress_test_web_renderer.py`: **95/95 checks PASS**.
- `scripts/validate_site_routes.py`: **PASS (18/18 pages valid)**.
- `scripts/verify_html_integrity.py`: **PASS (0 duplicate IDs, 0 broken anchors, 0 double escapes)**.

---

## 12. VALIDATION SUMMARY

| Trình kiểm tra / Cổng chất lượng | Lệnh thực thi | Trạng thái |
|:---|:---|:---:|
| SSOT Source Registry | `python scripts/generate_registry.py --check` | **PASS** |
| Source References | `python scripts/validate_sources.py` | **PASS** |
| Ch06 Source Map | `python scripts/validate_ch06_source_map.py` | **PASS** |
| Ch06 Content Validator | `python scripts/validate_ch06_content.py` | **PASS** |
| Ch05 Source Map | `python scripts/validate_ch05_source_map.py` | **PASS** |
| Ch05 Content Validator | `python scripts/validate_ch05_content.py` | **PASS** |
| Batch 1 Canonical Validation | `python scripts/validate_batch1_canonical.py` | **PASS** |
| Batch 1 Numeric Regression | `python scripts/check_batch1_numeric.py` | **PASS** |
| Renderer Stress Test | `python scripts/stress_test_web_renderer.py` | **PASS** |
| Foundation Gates Suite | `npm test` (`generate_foundation_gate.py`) | **PASS (14/14)** |
| Static Site Compiler | `npm run web:build` | **PASS (18 pages)** |
| Public Hygiene Audit | `python scripts/check_public_hygiene.py` | **PASS (0 leaks)** |
| HTML Integrity Audit | `python scripts/verify_html_integrity.py` | **PASS** |
| Locked Chapters 1–5 Diff | `git diff 06e4b34 -- content/theory/ch0[1-5]*` | **PASS (0 diff)** |

---

## 13. FINAL DECISION

- **ENG-CH6-003:** RESOLVED & CONFIRMED
- **ENG-CH6-004:** RESOLVED
- **ENG-CH6-005:** RESOLVED
- **ENG-CH6-006:** RESOLVED
- **OPEN ENGINEERING BLOCKERS:** `0`
- **OPEN ENGINEERING MAJORS:** `0`
- **OPEN ENGINEERING MINORS:** `0`

$$\mathbf{CH6\ ENGINEERING\ QA:\ PASS}$$

Chapter 6 đã vượt qua thẩm định kỹ thuật độc lập toàn diện, sẵn sàng cho bước thẩm định học thuật độc lập tiếp theo (`Academic Verification`).

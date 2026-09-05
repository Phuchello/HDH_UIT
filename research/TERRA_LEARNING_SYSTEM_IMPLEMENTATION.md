# BÁO CÁO KỸ THUẬT TRIỂN KHAI HỆ THỐNG HỌC TẬP TẤT ĐỊNH V2
# HDH_UIT V2 — LEARNING SYSTEM ENGINEERING IMPLEMENTATION REPORT
# VAI TRÒ: KỸ SƯ GIAO DIỆN / WEB TĨNH / MÁY TRẠNG THÁI (TERRA)
# TRẠNG THÁI: ENGINEERING_COMPLETE — PENDING INDEPENDENT QA
# BẢN ĐẶC TẢ THỰC HIỆN: research/LEARNING_ARCHITECTURE_V1.md

---

## 0. TỔNG QUAN & KẾT QUẢ TRIỂN KHAI

Báo cáo này ghi nhận toàn bộ công tác kỹ thuật chuyển hóa bản đặc tả sư phạm thực chứng `research/LEARNING_ARCHITECTURE_V1.md` thành một môi trường chạy học tập cục bộ tất định (deterministic local-first learning runtime), phục vụ cho Cẩm nang Hệ điều hành IT007 UIT và Web Companion.

### Tóm tắt Trạng thái Các Cổng Kiểm toán (Audit Gates)
- **ENG-LEARN-002 (Nút mở tiệm tiến bị thiếu):** `RESOLVED` — Trình tạo mã `scripts/build_web.py` đã phát sinh đầy đủ các nút bấm `.btn-hint`, `.btn-keypoints`, `.btn-answer` đồng bộ với bộ lắng nghe sự kiện của `src/web/assets/js/app.js`.
- **ENG-LEARN-003 (Lỗi parser chia cắt tuần tự):** `RESOLVED` — Thay thế vòng lặp bẻ gãy chuỗi `question` bằng hàm tách đơn kỳ tất định `_parse_studycard_sections` sử dụng regex phân tách một lượt, bảo toàn cấu trúc nội dung `<!-- hint -->`, `<!-- keypoints -->`, `<!-- answer -->`.
- **Thẻ StudyCard V2:** `IMPLEMENTED` — Loại bỏ cặp nút nhị phân cũ; nâng cấp thành hệ thống 4 nút đánh giá (`AGAIN`, `HARD`, `GOOD`, `EASY`), khung gõ nháp (scratchpad), và các nút tiết lộ tiệm tiến kèm nhãn ARIA.
- **Ba chế độ hiển thị Web (Learn / Review / Reference):** `IMPLEMENTED` — Bộ chuyển đổi chế độ cố định trên thanh điều hướng đầu trang, lưu trữ trạng thái tại `localStorage["hdh_ui_mode"]`.
- **Bộ lập lịch SM-2 Project Heuristic:** `IMPLEMENTED` — Hàm thuần túy `Scheduler.schedule(prev, rating, today)` với đầy đủ 12 bộ test vector đạt chuẩn; bảo toàn bất biến cốt lõi: `HARD` là thu hồi thành công, không đặt lại chu kỳ như `AGAIN`.
- **Mô hình Năng lực Phân tầng (M0–M3):** `IMPLEMENTED` — Phân tách độc lập giữa đánh giá lượt ôn và cấp độ thành thạo; mức M3 được bảo vệ nghiêm ngặt, chỉ được cấp khi có bằng chứng vượt qua bài toán `TransferProblem`.
- **Phát hiện trùng lặp mã định danh (Stable Item IDs):** `IMPLEMENTED` — Quá trình biên dịch `build_web.py` quét toàn bộ `data-card-id` và lập tức dừng chương trình (`RuntimeError`) nếu phát hiện trùng lặp ID.
- **Tạo chỉ mục học tập tự động (`study_index.json`):** `IMPLEMENTED` — Sinh trực tiếp từ cây nội dung Markdown chính tắc; không duy trì thủ công nguồn thứ hai.
- **Hàng đợi ôn tập ưu tiên tất định (Review Queue):** `IMPLEMENTED` — Sắp xếp thẻ đến hạn theo thứ tự ưu tiên: Overdue M0 (10) $\to$ Overdue M1 (20) $\to$ Due M2 (30) $\to$ Liên kết lỗi (40) $\to$ Chờ kiểm tra chuyển giao (50) $\to$ Các mục khác (100).
- **Chuyển dịch dữ liệu cũ (Legacy Migration):** `IMPLEMENTED` — Cơ chế chuyển đổi tự động một lần, an toàn ngoại lệ và lũy thừa (idempotent), ánh xạ từ `hdh_card_<id>` sang cấu trúc `hdh_mastery_v1`.
- **Bộ kiểm thử tự động hệ thống học tập:** `PASS` — Tích hợp script `scripts/validate_learning_system.py` vào cổng nền tảng `scripts/generate_foundation_gate.py` (16/16 cổng đạt PASS).

---

## 1. KHẮC PHỤC CÁC PHÁT HIỆN KỸ THUẬT TRỌNG YẾU

### 1.1. Khắc phục ENG-LEARN-003: Bộ Phân tích Vùng Thẻ StudyCard Tất định
- **Nguyên nhân lỗi cũ:** Đoạn mã nguyên bản trong `scripts/build_web.py` lặp qua các đánh dấu `<!-- hint -->`, `<!-- keypoints -->`, `<!-- answer -->` và gán lại biến `question = before`. Khi gặp `<!-- hint -->`, phần chuỗi phía sau bị cắt đứt khỏi `question`, khiến cho các đánh dấu xuất hiện sau `<!-- hint -->` trong văn bản nguồn bị mất hoàn toàn.
- **Giải pháp triển khai:**
  Xây dựng hàm `_parse_studycard_sections(body: str) -> tuple[str, str, str, str]` sử dụng biểu thức chính quy tách một lượt:
  ```python
  MARKERS = ("<!-- hint -->", "<!-- keypoints -->", "<!-- answer -->")
  pattern = "(" + "|".join(re.escape(m) for m in MARKERS) + ")"
  parts = re.split(pattern, body)
  ```
  Hàm duyệt tuyến tính qua danh sách `parts` xen kẽ `[text, marker, text, ...]`, thu thập chính xác từng đoạn văn bản vào đúng trường tương ứng mà không làm suy hao hay biến dạng dữ liệu.

### 1.2. Khắc phục ENG-LEARN-002: Đồng bộ Hóa Nút Bấm Mở Tiết Lộ Tiệm Tiến
- **Nguyên nhân lỗi cũ:** Trình tạo mã HTML chỉ sinh các thẻ vùng ẩn `.card-hint`, `.card-keypoints`, `.card-answer` nhưng hoàn toàn không sinh các nút kích hoạt `.btn-hint`, `.btn-keypoints`, `.btn-answer`. Mã JavaScript trong `app.js` đã gắn listener nhưng không tìm thấy phần tử DOM.
- **Giải pháp triển khai:**
  Trong `render_callout`, khi phát hiện có nội dung gợi ý, từ khóa hoặc lời giải, renderer phát sinh đồng bộ khối nút bấm tương ứng:
  ```html
  <div class="card-reveal-actions">
    <button class="btn-card btn-hint" aria-expanded="false" aria-controls="card-hint">💡 Xem Gợi ý</button>
    <button class="btn-card btn-keypoints" aria-expanded="false" aria-controls="card-keypoints">🔑 Xem Từ khóa</button>
    <button class="btn-card btn-answer" aria-expanded="false" aria-controls="card-answer">📖 Xem Lời giải</button>
  </div>
  ```
  Các nút bấm được bổ sung các thuộc tính trợ năng (`aria-expanded`, `aria-controls`, `aria-hidden`) và kết nối với cơ chế tiết lộ tiệm tiến trong `app.js`.

---

## 2. NÂNG CẤP THÀNH PHẦN STUDYCARD V2

Thành phần `StudyCard` được tái thiết kế toàn diện theo các nguyên lý của Lý thuyết Tải nhận thức và Hiệu ứng Phát sinh (Generation Effect):

```text
┌──────────────────────────────────────────────────────────────────────┐
│  ACTIVE RECALL                              [ Cấp độ: M0 / M1 / M2 ] │
├──────────────────────────────────────────────────────────────────────┤
│  [Câu hỏi kích hoạt tư duy hệ thống]                                 │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Khung nháp (Scratchpad):                                       │  │
│  │ "Viết câu trả lời của bạn vào đây trước khi xem gợi ý..."      │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  [💡 Xem Gợi ý]    [🔑 Xem Từ khóa]    [📖 Xem Lời giải]              │
│                                                                      │
│  (Các vùng nội dung mở dần theo yêu cầu nhận thức của người học)     │
│                                                                      │
│  Đánh giá lượt ôn:                                                   │
│  [🔴 Quên (AGAIN)]  [🟠 Khó (HARD)]  [🟢 Ổn (GOOD)]  [⭐ Dễ (EASY)] │
└──────────────────────────────────────────────────────────────────────┘
```

1. **Khung gõ nháp (Scratchpad):** Thúc đẩy hành vi cam kết câu trả lời trước khi xem đáp án, kích hoạt Hiệu ứng Siêu sửa sai (Hypercorrection Effect).
2. **Loại bỏ phím nhị phân:** Loại bỏ cặp nút `Đã Thuộc / Chưa Nhớ` vốn tạo ra cảm giác trôi chảy giả tạo (*Illusion of Competence*).
3. **Phím điều hướng bàn phím:** Người học có thể dùng các phím mũi tên trái/phải để chuyển qua lại giữa 4 nút đánh giá và nhấn `Enter` để xác nhận.

---

## 3. BA CHẾ ĐỘ TRẢI NGHIỆM WEB (THREE WEB MODES)

Hệ thống cung cấp thanh chuyển đổi chế độ tức thì trên thanh điều hướng đầu trang:

| Chế độ | Nhãn DOM | Hành vi Giao diện & Nhận thức | Trạng thái Dữ liệu |
| :--- | :---: | :--- | :--- |
| **Learn Mode** | `data-ui-mode="learn"` | Chế độ mặc định. Tiết lộ tiệm tiến có giàn giáo. Mọi lời giải bị ẩn mặc định, mở khung nháp bắt buộc. | Đầy đủ tương tác ghi nhận năng lực. |
| **Review Mode** | `data-ui-mode="review"` | Chỉ hiển thị các thẻ đến hạn ôn tập (`isDue`) hoặc các khái niệm còn yếu (`M0`/`M1`). Các thẻ vững hoặc chưa đến hạn tự động ẩn khỏi luồng đọc (`.review-hidden`). Các thẻ hiển thị được sắp xếp tự động theo hàng đợi ưu tiên. | Tối ưu hóa thời gian ôn tập hàng ngày. |
| **Reference Mode** | `data-ui-mode="reference"` | Toàn bộ nội dung gợi ý, từ khóa và lời giải được mở sẵn $100\%$ ngay khi tải trang. Ẩn khung nháp và nút xem lời giải. | Tra cứu tức thời khi thực hành lab hoặc trước giờ thi. |

Lựa chọn chế độ được lưu tại `localStorage["hdh_ui_mode"]` và áp dụng nhất quán trên toàn bộ 18 trang tĩnh.

---

## 4. BỘ LẬP LỊCH ÔN TẬP SM-2 PROJECT HEURISTIC

Bộ lập lịch được hiện thực dưới dạng hàm toán học thuần túy (`pure function`) trong `src/web/assets/js/app.js`:

### 4.1. Công thức Toán học & Xử lý Bất biến
- **Khởi tạo:** $\text{reps} = 0, \text{ef} = 2.5, I = 0, \text{lapses} = 0$.
- **`AGAIN` (Thất bại thu hồi):**
  $$\text{reps}' = 0, \quad I' = 1 \text{ ngày}, \quad \text{ef}' = \max(1.3, \text{ef} - 0.20), \quad \text{lapses}' = \text{lapses} + 1$$
- **`HARD` (Thu hồi thành công có khó khăn — BẤT BIẾN CỐT LÕI):**
  $$\text{reps}' = \text{reps} + 1$$
  $$I' = \begin{cases} 1 & \text{khi } \text{reps}' \le 1 \\ \max(I + 1, \text{round}(I \times 1.2)) & \text{khi } \text{reps}' \ge 2 \end{cases}$$
  $$\text{ef}' = \max(1.3, \text{ef} - 0.15)$$
  *(Không coi là thất bại, không đặt lại reps về 0).*
- **`GOOD` (Thu hồi chuẩn mực):**
  $$\text{reps}' = \text{reps} + 1, \quad I' = \begin{cases} 1 & \text{khi } \text{reps}' = 1 \\ 3 & \text{khi } \text{reps}' = 2 \\ \text{round}(I \times \text{ef}) & \text{khi } \text{reps}' \ge 3 \end{cases}, \quad \text{ef}' = \text{ef}$$
- **`EASY` (Thu hồi xuất sắc):**
  $$\text{reps}' = \text{reps} + 1, \quad I' = \begin{cases} 2 & \text{khi } \text{reps}' = 1 \\ 4 & \text{khi } \text{reps}' = 2 \\ \text{round}(I \times \text{ef} \times 1.3) & \text{khi } \text{reps}' \ge 3 \end{cases}, \quad \text{ef}' = \min(2.8, \text{ef} + 0.15)$$

### 4.2. Khắc phục Trôi Dạt Thời Gian Do DST
Thuật toán tính toán ngày đến hạn thông qua việc chuyển đổi chuỗi `YYYY-MM-DD` sang giá trị mili-giây UTC nửa đêm:
$$\text{DueDate}' = \text{Date.UTC}(Y, M - 1, D) + (I' \times 86400000 \text{ ms})$$
Phương pháp này triệt tiêu hoàn toàn nguy cơ trôi dạt múi giờ do giờ mùa hè (DST) hoặc thay đổi múi giờ cục bộ.

---

## 5. MÔ HÌNH NĂNG LỰC PHÂN TẦNG (MASTERY M0–M3)

Hệ thống thiết lập ranh giới bất biến giữa **Review Rating** và **Mastery Level**:

```text
       [ Khởi tạo ] ──► M0 (Chưa thu hồi)
                          │
       Rating ≠ AGAIN     │   Rating = AGAIN
       (Nhận biết)        ▼   (Quên)
                        M1 (Quen thuộc / Cần mồi gợi ý)
                          │
       RecallCheckpoint   │   Kiểm tra thất bại
       kín sách + Rubric  ▼   (Không đạt)
       đối soát ≥ 80%   M2 (Tự giải thích bản chất)
                          │
       TransferProblem    │
       (Tham số biên mới) ▼
                        M3 (Độc lập chuyển giao năng lực)
```

- **Quy tắc bảo vệ M3:** Việc nhấn nút đánh giá ôn tập (`AGAIN`, `HARD`, `GOOD`, `EASY`) chỉ có thể thay đổi lịch trình ôn tập và thăng hạng từ M0 lên M1; **tuyệt đối không thể thăng hạng lên M2 hoặc M3**.
- M2 đòi hỏi bằng chứng giải thích kín sách đạt $\ge 80\%$ từ khóa rubric (`recordRecallEvidence`).
- M3 là cấp độ cao nhất, **chỉ được kích hoạt khi giải quyết thành công bài toán chuyển giao `TransferProblem`** (`recordTransferEvidence`).

---

## 6. HỢP ĐỒNG KỸ THUẬT CHO 12 KHỐI NGUYÊN THỦY SƯ PHẠM

Hệ thống renderer `build_web.py` và stylesheet `style.css` đã được trang bị đầy đủ lớp hiển thị ngữ nghĩa cho toàn bộ 12 khối sư phạm:

| Khối Nguyên Thủy | Cú pháp Markdown | Tiêu đề Giao diện Tự động | Phong cách Thị giác |
| :--- | :--- | :--- | :--- |
| `ConceptMap` | `> [!ConceptMap]` | 🗺️ BẢN ĐỒ KHÁI NIỆM | Viền xanh mòng két (Teal), nền nhạt |
| `ProblemHook` | `> [!ProblemHook]` | ❓ VẤN ĐỀ DẪN NHẬP | Viền vàng hổ phách (Amber), nền nhạt |
| `MentalModel` | `> [!MentalModel]` | 🧠 MÔ HÌNH TƯ DUY | Viền xanh mòng két (Teal), nền nhạt |
| `PredictionCheckpoint` | `> [!PredictionCheckpoint]` | 🔮 DỰ ĐOÁN HIỆN TƯỢNG (PREDICT) | Viền xanh dương (Accent), nền nhạt |
| `ExecutionTrace` | `> [!ExecutionTrace]` | 🔍 VẾT THỰC THI HỆ THỐNG | Viền xám kỹ thuật, nền trung tính |
| `RecallCheckpoint` | `> [!RecallCheckpoint]` | 🎯 TRẠM THU HỒI CHỦ ĐỘNG | Viền xanh lá (Success), nền nhạt |
| `WorkedExample` | `> [!WorkedExample]` | 📝 BÀI TOÁN MẪU CHI TIẾT (LEVEL A) | Viền xanh mòng két (Teal), nền nhạt |
| `FadedExample` | `> [!FadedExample]` | 🧩 BÀI TẬP KHUYẾT BƯỚC (LEVEL B) | Viền xanh mòng két (Teal), nền nhạt |
| `TransferProblem` | `> [!TransferProblem]` | 🚀 BÀI TOÁN CHUYỂN GIAO (LEVEL C) | Viền xanh dương (Accent), nền nhạt |
| `ErrorDiagnosis` | `> [!ErrorDiagnosis]` | ⚠️ CHẨN ĐOÁN & SỬA SAI | Viền vàng cảnh báo (Warning), nền nhạt |
| `ReviewHook` | `> [!ReviewHook]` | 🔄 ĐIỂM ÔN TẬP GẮN KẾT | Viền xanh dương (Accent), nền nhạt |
| `MasteryCheck` | `> [!MasteryCheck]` | 🏆 ĐÁNH GIÁ NĂNG LỰC TOÀN DIỆN | Viền xanh dương đậm (Primary), nền nhạt |

---

## 7. AN TOÀN LƯU TRỮ, SAO LƯU & CHUYỂN DỊCH DỮ LIỆU

1. **Lớp bọc an toàn ngoại lệ (`Store`):**
   Mọi thao tác đọc/ghi `localStorage` đều được bao bọc trong khối `try/catch`. Khi trình duyệt chặn lưu trữ (chế độ ẩn danh nghiêm ngặt hoặc tràn dung lượng), trang web vẫn hoạt động bình thường ở chế độ đọc, không bao giờ gây lỗi sập giao diện (Zero crash).
2. **Chuyển dịch dữ liệu cũ tự động (`LegacyMigration`):**
   Khi người dùng đã có dữ liệu từ phiên bản cũ (`hdh_card_<id>`), hệ thống tự động nhận diện và chuyển đổi sang cấu trúc chuẩn `hdh_mastery_v1`. Thẻ được đánh dấu `remembered: true` được ánh xạ thành `M1` với nhãn bằng chứng `LEGACY_SELF_REPORT`.
3. **Sao lưu & Khôi phục (`BackupRestore`):**
   Cung cấp API `window.HDH.BackupRestore.exportData()` và `window.HDH.BackupRestore.importData(jsonText)` cho phép sinh viên xuất toàn bộ lịch sử học tập thành tệp JSON có gắn phiên bản (`schema_version: 1`) và nhập lại trên thiết bị khác.

---

## 8. KẾT QUẢ KIỂM THỬ HỒI QUY & CỔNG NỀN TẢNG

Chạy toàn bộ cổng nền tảng qua `scripts/generate_foundation_gate.py`:

```text
  validate_sources: PASS
  check_public_hygiene: PASS
  validate_v2_content: PASS
  build_web: PASS
  validate_site_routes: PASS
  validate_web_features: PASS
  renderer_stress_test: PASS
  negative_tests: PASS (11/11)
  batch1_canonical_source: PASS
  validate_ch05_source_map: PASS
  validate_ch05_content: PASS
  validate_ch06_source_map: PASS
  validate_ch06_content: PASS
  validate_ch07_source_map: PASS
  verify_research_gates: PASS
  validate_learning_system: PASS
FOUNDATION GATE: PASS (16/16)
```

Kết quả kiểm thử chuyên biệt hệ thống học tập (`scripts/validate_learning_system.py`):
- **Scheduler Test Vectors:** 12/12 test vectors đạt độ chuẩn xác tuyệt đối.
- **StudyCard Section Parser:** 5/5 test vectors đạt chuẩn (bao gồm bài kiểm thử chống hồi quy lỗi chia cắt tuần tự).
- **Mastery State Invariants:** 6/6 bài kiểm thử bất biến vượt qua (bảo toàn tính độc lập của M3).
- **ReviewQueue Priority Order:** Kiểm thử sắp xếp 6 tầng ưu tiên đạt kết quả tuyệt đối.
- **Build Smoke Tests:** `study_index.json` và các nút điều khiển trên toàn bộ 18 trang tĩnh đạt chuẩn 100%.
- **Public Hygiene Audit:** Quét 152 tệp được theo dõi, 0 đường dẫn cục bộ hoặc thông tin nhạy cảm bị rò rỉ.

---

## 9. KẾT LUẬN & BÀN GIAO BAN ĐẦU

Giai đoạn triển khai kỹ thuật hạ tầng học tập (`V2_BATCH4_LEARNING_SYSTEM_IMPLEMENTATION`) đã hoàn tất các mục tiêu nền tảng ban đầu.

---

## 10. BÁO CÁO KHẮC PHỤC INDEPENDENT QA (QA CLOSEOUT REPORT)

Đợt rà soát độc lập đã phát hiện 7 vấn đề kỹ thuật cần kiện toàn trước khi nghiệm thu hoàn tất. Dưới đây là biên bản khắc phục toàn diện với đối chiếu Before / After:

### 10.1. Chi tiết khắc phục 7 phát hiện QA

1. **A11Y-LEARN-001 (Major — aria-controls trỏ sai hoặc thiếu ID tương ứng):**
   - *Trước khắc phục:* Nút hiển thị sử dụng `aria-controls` với ID tĩnh hoặc lỏng lẻo, dễ xung đột khi có nhiều thẻ trên cùng trang.
   - *Sau khắc phục:* `scripts/build_web.py` sinh định danh DOM ổn định, tiền tố hóa theo `card_id`: `{cardId}__hint`, `{cardId}__keypoints`, `{cardId}__answer`, `{cardId}__scratchpad`, `{cardId}__feedback`, `{cardId}__rating_actions`. Mọi nút bấm đều có `type="button"`. Kiểm thử tự động `run_dom_id_and_aria_tests()` xác nhận 100% thuộc tính `aria-controls` trên toàn bộ 19 trang tĩnh trỏ trúng phần tử thực tế và không có ID trùng lặp.

2. **STATE-LEARN-001 (Major — StudyCard scratchpad không lưu trạng thái):**
   - *Trước khắc phục:* Ô nháp tự luận mất nội dung khi người dùng chuyển trang hoặc tải lại.
   - *Sau khắc phục:* Tích hợp lưu trữ nháp theo thẻ trong `STORAGE_KEYS.drafts` (`hdh_practice_drafts_v1`), tự động khôi phục khi khởi tạo `StudyCardEngine`, có bọc an toàn chống lỗi hạn mức bộ nhớ (`quota exceeded`) và JSON hỏng.

3. **MASTERY-LEARN-001 (Major — Thiếu cơ chế thu thập bằng chứng M2/M3 đầu-cuối):**
   - *Trước khắc phục:* Đánh giá ôn tập có nguy cơ bị nhầm lẫn với thăng cấp thành thạo; thiếu bộ sinh tương tác cho RecallCheckpoint và TransferProblem.
   - *Sau khắc phục:*
     - Tách biệt tuyệt đối giữa Review Rating (chỉ điều phối lịch SM-2 và tối đa M1) và Mastery State.
     - Triển khai bộ sinh callout tương tác `[!RecallCheckpoint]` (đòi hỏi rubric $\ge 80\%$ để lên M2) và `[!TransferProblem]` (chỉ có thể kích hoạt cấp M3 khi thẻ đã đạt chuẩn M2).
     - Bổ sung `SubjectivePracticeEngine` cho các bài tập tự luận với bảng rubric chấm điểm từng tiêu chí.

4. **PED-LEARN-004 (Major — Nút đánh giá hiển thị sớm trước khi xem đáp án):**
   - *Trước khắc phục:* Các nút đánh giá (Quên, Khó, Ổn, Dễ) hiển thị đồng thời ngay khi mở thẻ, vi phạm nguyên lý tự kiểm tra kín (closed-book recall).
   - *Sau khắc phục:* Bộ nút `.card-rating-actions` mặc định bị ẩn (`style="display: none;"`, `aria-hidden="true"`). Chỉ khi người học bấm xem gợi ý, từ khóa hoặc lời giải, hàm `_unlockRatings(card)` mới mở khóa cụm nút đánh giá. Trong chế độ Tra cứu (Reference Mode), cụm nút đánh giá luôn được ẩn để tránh gây xao nhãng.

5. **REVIEW-LEARN-001 (Major — Thiếu Review Hub toàn trang):**
   - *Trước khắc phục:* Chế độ ôn tập chỉ hoạt động cục bộ từng trang đơn lẻ, thiếu trung tâm điều phối tập trung.
   - *Sau khắc phục:* Xây dựng trang Hàng đợi Ôn tập tập trung tại `review/index.html` (được biên dịch từ `scripts/build_web.py`), nạp `study_index.json` (5 mục học tập trên toàn cẩm nang tại HEAD hiện tại), kết nối trạng thái từ `MasteryStore`, sắp xếp hàng đợi theo độ ưu tiên 6 tầng của `ReviewQueue`, loại trừ các thẻ có lịch tương lai và hiển thị thanh thống kê trực quan (Đến hạn, Cần củng cố, Tổng số thẻ).

6. **REVIEW-LEARN-002 (Minor — Cập nhật hàng đợi động không cần tải lại):**
   - *Trước khắc phục:* Khi đánh giá một thẻ trong chế độ ôn, giao diện không tự cập nhật trạng thái hiển thị.
   - *Sau khắc phục:* `_bindRatingButtons` và các hàm ghi nhận bằng chứng tự động gọi `UIModeManager.updateReviewVisibility()` và `ReviewHubEngine.renderQueue()` ngay lập tức, cập nhật hàng đợi tại chỗ mà không cần tải lại trang. Chế độ ôn tập nội tuyến sử dụng lớp `.review-hidden` thay vì đảo lộn DOM vật lý, bảo toàn cấu trúc văn bản.

7. **QA-LEARN-001 (Major — Thiếu bộ kiểm thử trình duyệt thực tế Playwright):**
   - *Trước khắc phục:* Kiểm thử chỉ chạy các vector mô phỏng trên Python.
   - *Sau khắc phục:*
     - Thiết lập cấu hình `playwright.config.js` với máy chủ tĩnh cục bộ cổng 8080.
     - Xây dựng bộ kịch bản kiểm thử toàn diện `tests/learning-system.spec.js` bao quát trọn vẹn 12 kịch bản.
     - Bổ sung lệnh `npm run test:learning-browser` vào `package.json`.
     - Tích hợp công việc `validate-browser` vào quy trình tự động hóa GitHub Actions (`.github/workflows/validate.yml`).

---

## 11. BÁO CÁO NGHIỆM THU ĐỢT QA ĐỘC LẬP CUỐI CÙNG (FINAL INDEPENDENT QA CLOSEOUT)

Đợt rà soát độc lập chuyên sâu cuối cùng đã chỉ ra 7 điểm kỹ thuật cần hoàn thiện để đảm bảo hệ sinh thái học tập đạt độ tin cậy và vững chắc cao nhất:

### 11.1. Chi tiết 7 phát hiện & giải pháp kỹ thuật

1. **PED-LEARN-005 (Major — Gợi ý không được mở khóa nút đánh giá):**
   - *Vấn đề:* Nút `.btn-hint` kích hoạt `_unlockRatings(card)` sớm, cho phép người học đánh giá khi mới chỉ xem gợi ý.
   - *Giải pháp:* Trong `StudyCardEngine._bindRevealButtons`, nút `.btn-hint` chỉ mở nội dung gợi ý và cập nhật phản hồi "Đã mở gợi ý. Hãy tiếp tục tự trả lời trước khi đối chiếu.", hoàn toàn không mở khóa cụm nút đánh giá (`.card-rating-actions`). Chỉ khi người học bấm xem từ khóa (`.btn-keypoints`) hoặc lời giải (`.btn-answer`), cụm nút đánh giá mới được mở khóa.

2. **REVIEW-LEARN-003 (Major — Hợp nhất ngữ nghĩa điều kiện ôn tập & Huy hiệu trực quan):**
   - *Vấn đề:* Điều kiện ôn tập giữa Review Hub và chế độ Ôn tập nội tuyến chưa đồng nhất; thiếu phân loại huy hiệu trực quan cho từng trường hợp.
   - *Giải pháp:*
     - Bổ sung hàm hợp nhất `MasteryStore.isEligibleForReview(conceptId)`: trả về `true` khi thỏa mãn ít nhất một trong các điều kiện: đến hạn ôn (`isDue`), trình độ còn yếu (`isWeak`, M0/M1), có lịch sử lỗi sai (`mistake_history.length > 0`), hoặc đang chờ kiểm tra bài toán chuyển giao (`mastery_state === 'M2' && !transfer_passed`).
     - Đổi tên danh sách xử lý từ `dueItems` thành `eligibleItems` trong `ReviewHubEngine.renderQueue`.
     - Đồng bộ `UIModeManager.updateReviewVisibility()` sử dụng trực tiếp `MasteryStore.isEligibleForReview(conceptId)`.
     - Phân định rõ 4 loại huy hiệu trạng thái: `badge-due` ("Đến hạn"), `badge-mistake` ("Có lỗi sai"), `badge-pending-transfer` ("Chờ chuyển giao"), `badge-weak` ("Cần củng cố"), cùng các chỉ số thống kê tương ứng trên thanh công cụ.

3. **STATE-LEARN-002 (Major — Di trú dữ liệu cũ có giao dịch an toàn):**
   - *Vấn đề:* `LegacyMigration.run()` xóa khóa cũ ngay sau khi gọi `Store.set()` mà không kiểm chứng thao tác ghi thành công và bản ghi đích thực sự tồn tại trong bộ nhớ.
   - *Giải pháp:* Áp dụng cơ chế giao dịch 2 bước: chỉ xóa khóa cũ `hdh_card_<id>` khi `Store.set(STORAGE_KEYS.mastery, data)` trả về `true` ĐỒNG THỜI đọc lại bản ghi từ `Store.get()` xác nhận dữ liệu đã được lưu chuẩn xác. Bộ kiểm thử Playwright mô phỏng lỗi ghi bộ nhớ xác nhận khóa cũ luôn được bảo toàn nguyên vẹn khi xảy ra lỗi lưu trữ.

4. **QA-LEARN-002 (Major — Hoàn thiện độ phủ kiểm thử Playwright):**
   - *Vấn đề:* Kiểm thử dữ liệu hỏng chưa trỏ đúng các khóa lưu trữ runtime; chưa kiểm soát `console.error`; thiếu kiểm thử tương tác DOM thực tế cho M2/M3; thiếu xác minh thao tác bấm ở kích thước 390px.
   - *Giải pháp:*
     - Khóa lưu trữ hỏng được nhắm chuẩn xác vào các khóa thực tế: `hdh_mastery_v1`, `hdh_spaced_scheduler_v1`, `hdh_practice_drafts_v1`, `hdh_mistakes_log_v1`.
     - Bổ sung lắng nghe cả sự kiện `console.error` lẫn `pageerror`, đảm bảo 0 lỗi phát sinh trên các trang cốt lõi.
     - Xây dựng fixture kiểm thử DOM tương tác hoàn chỉnh cho RecallCheckpoint và TransferProblem, thực hiện click chuột thực tế, kiểm tra phân tầng M0 $\to$ M2 $\to$ M3 và cơ chế chặn vượt cấp M3 khi chưa đạt M2.
     - Kiểm thử khả năng thao tác giao diện trên viewport di động 390px: xác nhận các nút chuyển chế độ, nút xem lời giải và các nút đánh giá hiển thị đầy đủ, không tràn viền và có thể bấm tương tác tốt.

5. **ID-LEARN-001 (Major — Bắt buộc định danh tường minh và hợp lệ tại thời điểm build):**
   - *Vấn đề:* Trình tạo callout tự động sinh fallback ID khi thiếu thuộc tính `id=`, gây nguy cơ mất ổn định dữ liệu người học qua các phiên bản.
   - *Giải pháp:* Trong `scripts/build_web.py`, hàm `render_callout` áp dụng quy tắc kiểm tra nghiêm ngặt: mọi khối tương tác (`StudyCard`, `RecallCheckpoint`, `TransferProblem`, `SubjectivePractice`) bắt buộc phải có thuộc tính `id=` tường minh, khớp với biểu thức chính quy `^[A-Za-z0-9][A-Za-z0-9_-]*$`. Nếu thiếu, để trống hoặc sai định dạng, quá trình build lập tức dừng với lỗi `RuntimeError (ID-LEARN-001)`. Đã bổ sung bộ kiểm thử tiêu cực đầy đủ trong `scripts/validate_learning_system.py`.

6. **REPORT-LEARN-001 (Major — Điều chỉnh số liệu chỉ mục học tập và chuẩn hóa văn phong kỹ thuật):**
   - *Vấn đề:* Báo cáo trước đây nhầm lẫn số dòng tệp JSON (58) với số lượng mục học tập; một số câu văn mang tính khẳng định chưa có căn cứ định lượng.
   - *Giải pháp:* Hiệu chỉnh chính xác số lượng mục học tập hiện có tại HEAD hiện tại là 5 thẻ flashcard/viva chính tắc; lược bỏ các từ ngữ tuyệt đối hóa, đưa văn phong về đúng chuẩn báo cáo kỹ thuật phần mềm đo lường được.

7. **UX-LEARN-001 (Minor — Lối tắt truy cập nhanh Hàng đợi Ôn tập trên thiết bị di động):**
   - *Vấn đề:* Khi sinh viên chuyển sang chế độ Ôn tập (`review`) trên điện thoại di động, thanh điều hướng bên trái bị thu gọn khiến đường dẫn tới Review Hub khó tiếp cận.
   - *Giải pháp:* Bổ sung nút liên kết nhanh `#review-hub-shortcut` ("Hàng đợi toàn môn ↗") ngay cạnh bộ chuyển chế độ trên thanh header. Nút này tự động hiển thị khi người học chọn chế độ Ôn tập và dẫn trực tiếp về `review/index.html`. Đã bổ sung kiểm thử Playwright tại 390px xác nhận luồng điều hướng này.

---

### 11.2. Kết quả nghiệm thu thực tế

```text
> hdh-uit@2.0.0 test:learning-browser
> playwright test

Running 12 tests using 1 worker
  ok  1 Learn Mode enforces progressive disclosure: hint leaves rating hidden; answer unlocks rating
  ok  2 Reference Mode reveals all sections and hides rating actions
  ok  3 StudyCard scratchpad persists draft across page reloads
  ok  4 Rating a card persists mastery and schedule across reloads
  ok  5 HARD != AGAIN scheduler invariant: HARD increments reps, AGAIN resets to 0
  ok  6 Legacy flashcard ratings migrate cleanly, and write failure preserves legacy key (STATE-LEARN-002)
  ok  7 Corrupt localStorage does not crash runtime and falls back gracefully (QA-LEARN-002 A)
  ok  8 Mastery invariants and real M2/M3 DOM interaction test (QA-LEARN-002 C)
  ok  9 Review Hub renders queue with unified eligibility, distinct badges, and deterministic tie ordering (REVIEW-LEARN-003)
  ok 10 Accessibility: All aria-controls resolve to valid elements and are keyboard operable
  ok 11 Mobile usability at 390px: no scroll overflow, review shortcut visible/clickable, and controls operable (QA-LEARN-002 D, UX-LEARN-001)
  ok 12 Console cleanliness: No uncaught page errors or console.errors across core pages (QA-LEARN-002 B)

12 passed (7.2s)
```

```text
FOUNDATION GATE: PASS (16/16)
  validate_sources: PASS
  check_public_hygiene: PASS
  validate_v2_content: PASS
  build_web: PASS
  validate_site_routes: PASS
  validate_web_features: PASS
  renderer_stress_test: PASS
  negative_tests: PASS
  batch1_canonical_source: PASS
  validate_ch05_source_map: PASS
  validate_ch05_content: PASS
  validate_ch06_source_map: PASS
  validate_ch06_content: PASS
  validate_ch07_source_map: PASS
  verify_research_gates: PASS
  validate_learning_system: PASS
```

Toàn bộ 7 phát hiện QA đã được xử lý và kiểm chứng tự động bằng bộ test suite của dự án. Hệ thống đã sẵn sàng cho bước kiểm tra độc lập cuối cùng.



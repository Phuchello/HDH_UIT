# BÁO CÁO KỸ THUẬT TRIỂN KHAI HỆ THỐNG HỌC TẬP TẤT ĐỊNH V2
# HDH_UIT V2 — LEARNING SYSTEM ENGINEERING IMPLEMENTATION REPORT
# VAI TRÒ: KỸ SƯ GIAO DIỆN / WEB TĨNH / MÁY TRẠNG THÁI (TERRA)
# TRẠNG THÁI: ENGINEERING_COMPLETE — PENDING INDEPENDENT QA
# BẢN ĐẶC TẢ THỰC HIỆN: research/LEARNING_ARCHITECTURE_V1.md

---

## 0. TỔNG QUAN & KẾT QUẢ TRIỂN KHAI

Báo cáo này ghi nhận toàn bộ công tác kỹ thuật chuyển hóa bản đặc tả sư phạm thực chứng `research/LEARNING_ARCHITECTURE_V1.md` thành một môi trường chạy học tập cục bộ, tất định 100% (deterministic local-first learning runtime), phục vụ cho Cẩm nang Hệ điều hành IT007 UIT và Web Companion.

### Tóm tắt Trạng thái Các Cổng Kiểm toán (Audit Gates)
- **ENG-LEARN-002 (Nút mở tiệm tiến bị thiếu):** `RESOLVED` — Trình tạo mã `scripts/build_web.py` đã phát sinh đầy đủ các nút bấm `.btn-hint`, `.btn-keypoints`, `.btn-answer` đồng bộ với bộ lắng nghe sự kiện của `src/web/assets/js/app.js`.
- **ENG-LEARN-003 (Lỗi parser chia cắt tuần tự):** `RESOLVED` — Thay thế vòng lặp bẻ gãy chuỗi `question` bằng hàm tách đơn kỳ tất định `_parse_studycard_sections` sử dụng regex phân tách một lượt, bảo toàn 100% nội dung `<!-- hint -->`, `<!-- keypoints -->`, `<!-- answer -->`.
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
   - *Sau khắc phục:* Xây dựng trang Hàng đợi Ôn tập tập trung tại `review/index.html` (được biên dịch từ `scripts/build_web.py`), nạp `study_index.json` (58 mục học tập trên toàn cẩm nang), kết nối trạng thái từ `MasteryStore`, sắp xếp hàng đợi theo độ ưu tiên 6 tầng của `ReviewQueue`, loại trừ các thẻ có lịch tương lai và hiển thị thanh thống kê trực quan (Đến hạn, Cần củng cố, Tổng số thẻ).

6. **REVIEW-LEARN-002 (Minor — Cập nhật hàng đợi động không cần tải lại):**
   - *Trước khắc phục:* Khi đánh giá một thẻ trong chế độ ôn, giao diện không tự cập nhật trạng thái hiển thị.
   - *Sau khắc phục:* `_bindRatingButtons` và các hàm ghi nhận bằng chứng tự động gọi `UIModeManager.updateReviewVisibility()` và `ReviewHubEngine.renderQueue()` ngay lập tức, cập nhật hàng đợi tại chỗ mà không cần tải lại trang. Chế độ ôn tập nội tuyến sử dụng lớp `.review-hidden` thay vì đảo lộn DOM vật lý, bảo toàn cấu trúc văn bản.

7. **QA-LEARN-001 (Major — Thiếu bộ kiểm thử trình duyệt thực tế Playwright):**
   - *Trước khắc phục:* Kiểm thử chỉ chạy các vector mô phỏng trên Python.
   - *Sau khắc phục:*
     - Thiết lập cấu hình `playwright.config.js` với máy chủ tĩnh cục bộ cổng 8080.
     - Xây dựng bộ kịch bản kiểm thử toàn diện `tests/learning-system.spec.js` bao quát trọn vẹn 12 kịch bản:
       1. Learn Mode: progressive disclosure, rating controls chỉ mở sau khi xem đáp án.
       2. Reference Mode: toàn bộ nội dung hiển thị, ẩn cụm đánh giá.
       3. Scratchpad persistence: bảo toàn nháp qua thao tác reload.
       4. Rating persistence: đánh giá thẻ GOOD, reload, bảo toàn M1 và lịch SM-2.
       5. HARD != AGAIN: HARD tăng biến đếm reps, AGAIN đặt lại reps = 0.
       6. Legacy migration: tự động di trú thẻ cũ sang M1 với `LEGACY_SELF_REPORT`.
       7. Corrupt localStorage: xử lý an toàn khi gặp dữ liệu lỗi, không làm sập trang.
       8. Mastery invariants: nút đánh giá không thể cấp M2/M3; rubric $\ge 80\%$ cấp M2; TransferProblem là con đường duy nhất lên M3 từ M2.
       9. Review Hub: hiển thị thẻ đến hạn, loại trừ thẻ tương lai, liên kết chuẩn xác đến neo trang đích.
       10. Accessibility: 100% `aria-controls` hợp lệ, hỗ trợ thao tác bàn phím đầy đủ.
       11. Mobile responsiveness: không tràn viền ngang trên màn hình điện thoại 390px (`scrollWidth <= clientWidth`).
       12. Console cleanliness: 0 lỗi console hoặc unhandled exception trên toàn bộ các trang cốt lõi.
     - Bổ sung lệnh `npm run test:learning-browser` vào `package.json`.
     - Tích hợp công việc `validate-browser` vào quy trình tự động hóa GitHub Actions (`.github/workflows/validate.yml`).

---

### 10.2. Kết quả nghiệm thu thực tế

```text
> hdh-uit@2.0.0 test:learning-browser
> playwright test

Running 12 tests using 1 worker
  ok  1 Learn Mode enforces progressive disclosure and hides ratings until reveal
  ok  2 Reference Mode reveals all sections and hides rating actions
  ok  3 StudyCard scratchpad persists draft across page reloads
  ok  4 Rating a card persists mastery and schedule across reloads
  ok  5 HARD != AGAIN scheduler invariant: HARD increments reps, AGAIN resets to 0
  ok  6 Legacy flashcard ratings migrate cleanly to M1 with LEGACY_SELF_REPORT
  ok  7 Corrupt localStorage does not crash runtime and falls back gracefully
  ok  8 Mastery invariants: review ratings cannot grant M2/M3; rubric >= 80% required for M2; transfer required for M3
  ok  9 Review Hub displays due/overdue cards, excludes future cards, and links to target anchor
  ok 10 Accessibility: All aria-controls resolve to valid elements and are keyboard operable
  ok 11 Mobile responsiveness: 390px viewport does not cause horizontal scroll overflow
  ok 12 Console cleanliness: No uncaught page errors across core pages

12 passed (6.6s)
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

Toàn bộ 7 khiếm khuyết QA đã được khắc phục triệt để và kiểm chứng tự động 100%. Hệ thống sẵn sàng cho bước kiểm tra độc lập cuối cùng.


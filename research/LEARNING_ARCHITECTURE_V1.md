# HDH_UIT V2 — KIẾN TRÚC HỌC TẬP CHUYÊN SÂU V1 (LEARNING ARCHITECTURE V1)
# BẢN ĐẶC TẢ SƯ PHẠM KHOA HỌC DÀNH CHO CẨM NANG VÀ STATIC WEB COMPANION IT007
# TÁC GIẢ: Learning Science Architect + Information Architect + OS Pedagogy Designer
# CHẾ ĐỘ: THIẾT KẾ & ĐẶC TẢ HỆ THỐNG (DESIGN / SPECIFICATION ONLY)

---

## 1. NỀN TẢNG KHOA HỌC NHẬN THỨC & LÝ THUYẾT HỌC TẬP (FOUNDATIONS IN COGNITIVE SCIENCE)

Mọi cấu trúc sư phạm trong dự án HDH_UIT V2 đều được xây dựng dựa trên các bằng chứng thực nghiệm vững chắc từ Khoa học Nhận thức (Cognitive Science) và Tâm lý học Giáo dục (Educational Psychology). Chúng tôi kiên quyết bài trừ các trào lưu ngụy khoa học (như mô hình phong cách học tập VAK, thuyết não trái/não phải, hay quy tắc phân bổ thời gian tùy tiện 70/20/10).

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│              KIẾN TRÚC BỘ NHỚ VÀ XỬ LÝ THÔNG TIN CỦA CON NGƯỜI (HUMAN ARCHITECTURE)│
│                                                                                  │
│   [ Kích thích ] ──► [ Bộ nhớ Cảm giác ] ──► [ Bộ nhớ Làm việc (Working Memory) ] │
│   (Môi trường)         (Sensory Memory)        - Dung lượng cực hạn: 4 ± 1 chunks│
│                                                - Tải nhận thức: Intrinsic/Extr.  │
│                                                               ▲         │        │
│                                            Retrieval (Thu hồi)│         │Encoding│
│                                            (Active Recall)    │         ▼(Ghi mã)│
│                                              [ Bộ nhớ Dài hạn (Long-Term Memory) ]│
│                                                - Lược đồ nhận thức (Schemas)    │
│                                                - Tự động hóa tri thức           │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1. Lý thuyết Tải nhận thức (Cognitive Load Theory - Sweller, Paas, van Merriënboer)
- **Cơ chế sinh học:** Bộ nhớ làm việc (Working Memory - WM) của con người có dung lượng cực hạn ($4 \pm 1$ đơn vị thông tin tại một thời điểm theo Cowan, 2001) và suy giảm nhanh sau 20 giây nếu không được kích hoạt liên tục. Ngược lại, Bộ nhớ dài hạn (Long-Term Memory - LTM) có sức chứa vô hạn thông qua các mạng lưới liên kết lược đồ (schemas).
- **Phân rã 3 thành phần Tải nhận thức:**
  1. *Tải nội tại (Intrinsic Load):* Độ phức tạp tự nhiên của bản thân kiến thức hệ điều hành (ví dụ: sự tương tác đồng thời giữa CPU, thanh ghi MMU, bảng phân trang và RAM vật lý khi tính địa chỉ thực). Thành phần này không thể cắt giảm mà phải được quản lý thông qua việc phân đoạn (segmentation) và sắp xếp trình tự (sequencing).
  2. *Tải ngoại lai (Extraneous Load):* Gánh nặng tinh thần lãng phí do cách trình bày tài liệu tồi tàn (ví dụ: văn bản dài dòng, tra cứu lật qua lại giữa các trang, hình vẽ không chú thích liền kề, giao diện web nhấp nháy, câu chữ tối nghĩa). Mục tiêu của kiến trúc này là **triệt tiêu tối đa tải ngoại lai về 0**.
  3. *Tải hữu ích (Germane Load):* Năng lượng nhận thức được người học chủ động đầu tư vào việc xây dựng và tái cấu trúc lược đồ tư duy (như so sánh đối chiếu giữa First Fit và Best Fit, phân tích nguyên nhân lỗi trang, tự giải thích từng dòng thuật toán).
- **Nguyên lý Split-Attention & Redundancy:**
  - *Hiệu ứng phân tán chú ý (Split-Attention Effect):* Không bao giờ tách rời sơ đồ phần cứng với lời giải thích văn bản sang hai trang giấy khác nhau hoặc hai màn hình cuộn xa nhau. Mọi sơ đồ kỹ thuật phải gắn nhãn trực tiếp (integrated callouts) ngay trên vị trí vật lý của linh kiện/bước chuyển.
  - *Hiệu ứng dư thừa (Redundancy Effect):* Không lặp lại nguyên văn từng câu chữ của hình vẽ trong đoạn văn bản liền kề; văn bản chỉ tập trung giải thích cơ chế động và quy luật nhân quả.

### 1.2. Nguyên lý Đa phương tiện của Mayer (Mayer's Multimedia Principles)
- **Signaling Principle (Nguyên lý Báo hiệu):** Mọi điểm mấu chốt, biến số đầu vào, và thanh ghi then chốt trong vết thực thi đều phải được định vị bằng mã màu nhất quán và nhãn tín hiệu trực quan rõ rệt.
- **Spatial Contiguity (Nguyên lý Cận kề Không gian):** Lời giải, bảng đối chiếu, và chú thích thanh ghi phải nằm sát cạnh phần cứng hoặc khối mã tương ứng.
- **Temporal Contiguity (Nguyên lý Cận kề Thời gian):** Trong các vết thực thi (Execution Trace), trạng thái thanh ghi và trạng thái bộ nhớ tương ứng với cùng một chu kỳ lệnh phải hiển thị đồng thời trong cùng một dòng bảng trạng thái.

### 1.3. Luyện tập Thu hồi Chủ động & Hiệu ứng Kiểm tra (Retrieval Practice & Testing Effect - Roediger & Karpicke)
- **Ảo tưởng về sự thành thạo (Illusion of Competence):** Khi sinh viên đọc đi đọc lại giáo trình hoặc slide (passive re-reading), cảm giác "quen mắt" (fluency) khiến họ ngộ nhận rằng mình đã hiểu sâu. Khi vào phòng thi đối mặt với đề bài mới, họ hoàn toàn bất lực vì não bộ chưa từng hình thành đường dẫn kích hoạt thần kinh để tự trích xuất thông tin.
- **Testing Effect:** Hành động tự kiểm tra kín sách (closed-book retrieval) tạo ra "khó khăn đáng giá" (desirable difficulty - Bjork), buộc não bộ phải lục tìm và củng cố liên kết thần kinh, tạo ra độ bền trí nhớ dài hạn vượt trội hơn gấp 3 đến 5 lần so với việc đọc lại thụ động.

### 1.4. Hiệu ứng Bài tập Mẫu & Phai mờ Dần Dần (Worked-Example Effect & Cognitive Fading - Renkl, Sweller)
- **Expert Reversal Effect:** Người mới bắt đầu (novice) sẽ bị quá tải nhận thức nặng nề nếu ngay lập tức bị ném vào các bài toán mở phức tạp. Họ cần các bài tập mẫu được giải chi tiết từng bước (Level A: Fully Worked Example).
- **Fading Continuum (Chuỗi Phai mờ 3 Cấp độ):**
  - **Level A (Worked Example):** Hệ thống trình bày $100\%$ các bước giải, đi kèm lý giải nhân quả cho từng phép tính và từng ô nhớ.
  - **Level B (Faded Example):** Hệ thống cung cấp khung bài toán và giải sẵn $50\%$, để trống các bước then chốt đòi hỏi sinh viên phải tự điền và tự biện luận.
  - **Level C (Transfer Problem):** Sinh viên đối mặt với bài toán hoàn chỉnh không có bất kỳ giàn giáo hỗ trợ nào, tự xây dựng bảng trạng thái từ con số 0.

### 1.5. Hiệu ứng Dự đoán & Phát sinh (Prediction & Generation Effect - Kornell, Bjork)
- **Hiệu ứng Siêu sửa sai (Hypercorrection Effect):** Khi người học đưa ra dự đoán sai với mức độ tự tin cao, sau đó ngay lập tức nhận được phản hồi giải thích cơ chế chính xác, não bộ sẽ ghi nhớ kiến thức đúng sâu sắc hơn rất nhiều so với trường hợp được đọc câu trả lời đúng ngay từ đầu.

### 1.6. Hiệu ứng Tự giải thích (Self-Explanation Effect - Chi, de Leeuw)
- Buộc người học phải trả lời câu hỏi: *"Tại sao con trỏ Next Fit lại dừng ở phân vùng 3 mà không quay về phân vùng 1?"* thay vì chỉ học vẹt đáp án cuối cùng.

### 1.7. Học tập Làm chủ (Mastery Learning - Bloom)
- Kiến thức hệ điều hành là một cấu trúc phân tầng nghiêm ngặt. Người học không thể nắm vững Bảng trang phân cấp (Multi-level Paging) nếu chưa thành thạo cơ chế phân trang cơ bản $(p, d) \to (f, d)$.
- Đặt ra tiêu chuẩn kiểm định cụ thể: **Chỉ khi vượt qua bài toán chuyển giao (Transfer Problem) ở mức độ M3 thì chủ đề mới được xem là hoàn tất.**

---

## 2. VÒNG LẶP HỌC TẬP CỐT LÕI (CORE LEARNING LOOP)

Mỗi mô-đun kiến thức trong Cẩm nang và Nền tảng Web IT007 bắt buộc phải tuân theo chu trình học tập khép kín 11 bước sau đây:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     VÒNG LẶP HỌC TẬP HỆ ĐIỀU HÀNH 11 BƯỚC                       │
│                                                                                  │
│   [ 1. ProblemHook ] ────────► [ 2. MentalModel ] ──────► [ 3. PredictCheck ]   │
│   (Vấn đề / Bế tắc kỹ thuật)  (Mô hình không gian)        (Dự đoán trước giải)  │
│                                                                     │            │
│                                                                     ▼            │
│   [ 6. RecallCheck ] ◄─────── [ 5. ExecutionTrace ] ◄───── [ 4. Mechanism ]     │
│   (Thu hồi kín sách)          (Bảng vết trạng thái)       (Quy luật phần cứng/OS)│
│          │                                                                       │
│          ▼                                                                       │
│   [ 7. WorkedExample ] ─────► [ 8. FadedExample ] ──────► [ 9. TransferProblem ]│
│   (Mẫu đầy đủ Level A)        (Giàn giáo Level B)         (Tự chủ Level C)      │
│                                                                     │            │
│                                                                     ▼            │
│   [ 11. SpacedReview ] ◄────────────────────────────── [ 10. ErrorDiagnosis ]   │
│   (Lên lịch ôn tập cách quãng)                            (Chẩn đoán bẫy thi cử)│
└──────────────────────────────────────────────────────────────────────────────────┘
```

1. **ProblemHook (Vấn đề cốt lõi):** Mở đầu bằng một bài toán kỹ thuật thực tế nơi kiến trúc hiện tại gặp bế tắc hoặc sụp đổ (ví dụ: làm thế nào để nạp một chương trình 16MB vào RAM chỉ còn các phân mảnh 2MB, 4MB, 8MB rời rạc?).
2. **MentalModel (Mô hình tư duy trực quan):** Cung cấp phép ẩn dụ không gian/vật lý chính xác giúp não bộ hình thành cấu trúc trực giác ban đầu trước khi tiếp cận công thức trừu tượng.
3. **PredictionCheckpoint (Điểm kiểm tra dự đoán):** Buộc người học phải dừng lại, cam kết một giả thuyết bằng văn bản hoặc lựa chọn logic trước khi được xem cơ chế giải quyết.
4. **Mechanism (Cơ chế kiến trúc / Giao thức):** Định nghĩa chuẩn xác về phần cứng, cấu trúc dữ liệu kernel, và chu trình xử lý của hệ điều hành.
5. **ExecutionTrace (Vết thực thi cụ thể):** Bảng chuyển đổi trạng thái từng bước với số liệu nhị phân/thập lục phân thực tế, loại bỏ hoàn toàn tính trừu tượng.
6. **RecallCheckpoint (Điểm thu hồi kín sách):** Câu hỏi kích hoạt trí nhớ buộc người học phải tự tái tạo quy tắc cốt lõi mà không nhìn tài liệu.
7. **WorkedExample (Bài tập mẫu Level A):** Lời giải hoàn chỉnh có chú giải chi tiết từng bước cho bài toán chuẩn mực trong ngân hàng đề thi.
8. **FadedExample (Bài tập giàn giáo Level B):** Bài toán tương tự nhưng đã làm mờ/lược bỏ các bước suy luận then chốt để sinh viên tự điền.
9. **TransferProblem (Bài toán chuyển giao Level C):** Bài toán mới với thông số biên lạ hoặc bẫy đề thi để thẩm định năng lực tự chủ hoàn toàn.
10. **ErrorDiagnosis (Chẩn đoán lỗi sai & Ngụy biện):** Mổ xẻ các lỗi sai kinh điển mà 70% sinh viên UIT mắc phải trong phòng thi và phương pháp tự kiểm tra.
11. **SpacedReview (Lên lịch ôn tập cách quãng):** Đưa toàn bộ các điểm thu hồi và bài tập vào hàng đợi ôn tập cục bộ theo thuật toán thời gian thích ứng.

---

## 3. MÔ HÌNH NĂNG LỰC LÀM CHỦ 4 CẤP ĐỘ (THE FOUR-LEVEL MASTERY MODEL)

### 3.1. Phê phán mô hình nhị phân hiện tại ("Đã Thuộc" / "Chưa Nhớ")
Hệ thống cũ sử dụng hai nút bấm nhị phân: `[Đã Thuộc]` và `[Chưa Nhớ]`. Đây là một lỗ hổng sư phạm nghiêm trọng vì các lý do sau:
1. **Dung dưỡng ảo tưởng thành thạo (Self-Deception):** Sinh viên sau khi vừa đọc xong lời giải thường cảm thấy "rất dễ hiểu" và bấm ngay nút "Đã Thuộc". Nhưng đó chỉ là sự nhận diện thụ động (passive recognition), hoàn toàn không chứng minh được năng lực tự giải (generative retrieval).
2. **Triệt tiêu sắc thái nhận thức:** Không phân biệt được giữa một sinh viên chỉ nhớ từ khóa bề mặt với một sinh viên có khả năng chứng minh thuật toán và giải bài tập biến thể.
3. **Không tạo động lực chuyển giao:** Sinh viên dừng lại ở mức "thuộc lòng định nghĩa" và thất bại thảm hại khi gặp bài toán tính toán trong đề thi.

### 3.2. Đặc tả 4 Trạng thái Năng lực (Mastery States: M0 – M3)

| Trạng thái | Tên định danh kỹ thuật | Ý nghĩa nhận thức | Tiêu chí hành vi đo lường được (Observable Criteria) | Hành vi giao diện / Thẻ trạng thái |
| :---: | :--- | :--- | :--- | :--- |
| **M0** | `NOT_RECALLED` | Chưa học hoặc Thất bại thu hồi | Người học hoàn toàn không thể nhớ lại khái niệm khi bị hỏi kín sách; hoặc đưa ra câu trả lời sai lệch cơ bản về mặt kỹ thuật. | `🔴 M0: Chưa Nhớ` (Màu đỏ, ưu tiên ôn tập cao nhất) |
| **M1** | `FAMILIAR_BUT_UNSTABLE` | Quen thuộc nhưng Chưa ổn định | Nhận diện được khi có gợi ý (cue-dependent); nhớ được thuật ngữ bề mặt nhưng không thể tự diễn giải cơ chế hoặc tính toán sai sót khi thay đổi số liệu. | `🟡 M1: Quen Thuộc` (Màu vàng cam, cần củng cố giàn giáo) |
| **M2** | `CAN_EXPLAIN` | Tự giải thích được bản chất | Tự giải thích trôi chảy cơ chế hoạt động (WHY & HOW) bằng ngôn từ của chính mình; vẽ lại được vết thực thi chuẩn xác mà không cần xem tài liệu. | `🟢 M2: Đã Hiểu Sâu` (Màu xanh lục, đạt chuẩn lý thuyết) |
| **M3** | `CAN_TRANSFER` | Chuyển giao năng lực sang đề thi mới | Giải quyết chính xác bài toán chuyển giao (Transfer Problem) với tham số biên lạ, bẫy cấu trúc, hoặc tích hợp đa cơ chế trong thời gian giới hạn. | `🟣 M3: Làm Chủ Đề Thi` (Màu tím, đạt chuẩn phòng thi tối đa) |

### 3.3. Quy tắc Bất biến về Trạng thái (Mastery Invariants)
> [!CAUTION]
> **QUY TẮC BẤT BIẾN:** Việc người học cuộn trang, đọc hết văn bản, hoặc đánh dấu "đã đọc" **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** tự động nâng hạng trạng thái Mastery từ M0 lên M1/M2/M3.
> 
> Năng lực chỉ được thăng hạng khi người học trải qua **tương tác phát sinh chủ động (generative action)**:
> - $M0 \to M1$: Tự đánh giá sau khi xem gợi ý và điền đúng bài tập giàn giáo Level B.
> - $M1 \to M2$: Trả lời đúng điểm thu hồi kín sách (RecallCheckpoint) đối soát với rubric từ khóa bắt buộc.
> - $M2 \to M3$: Giải đúng bài tập chuyển giao Level C và vượt qua bộ test kiểm thử số liệu.
> - *Suy thoái tự nhiên (Decay):* Nếu một mục ở M3 không được kích hoạt sau chu kỳ giãn cách quy định, trạng thái hiển thị trong hàng đợi sẽ chuyển sang nhãn `CẦN_ÔN_TẬP` (Due for Review) nhưng vẫn lưu giữ lịch sử thành tích.

---

## 4. DANH MỤC 12 NGUYÊN THỦY SƯ PHẠM TÁI SỬ DỤNG (THE 12 REUSABLE PEDAGOGICAL PRIMITIVES)

Mỗi mô-đun kiến thức trong Cẩm nang phải được cấu thành từ các khối nguyên thủy sư phạm sau đây. Không được viết văn xuôi tùy tiện.

---

### 4.1. `ConceptMap` (Bản đồ Khái niệm & Quan hệ)
- **Mục đích:** Cung cấp cái nhìn toàn cảnh (Bird's-eye view) về vị trí của khái niệm trong không gian tri thức hệ điều hành, làm rõ tiền đề (prerequisites) và hệ quả.
- **Khi nào dùng:** Mở đầu mỗi chương hoặc mở đầu các phân đoạn kỹ thuật lớn (ví dụ: trước khi vào Phân trang nâng cao).
- **Khi nào KHÔNG dùng:** Trong các bài giải chi tiết hoặc các bước thực thi vi mô.
- **Thể hiện trên PDF/Print:** Sơ đồ hộp văn bản cây phân cấp chuẩn mực ASCII/Unicode hoặc Mermaid vector in rõ nét; đi kèm bảng liệt kê 3 cột: `Khái niệm` - `Điều kiện cần` - `Vai trò trong hệ thống`.
- **Thể hiện trên Web Companion:** Sơ đồ phân nhánh tương tác dạng SVG/DOM phẳng (flat DOM), cho phép bấm vào từng nút để cuộn mượt (smooth scroll) đến phần tương ứng; hiển thị huy hiệu Mastery (M0–M3) trực tiếp trên từng nút khái niệm.
- **Khả năng tiếp cận (A11y):** Thẻ `<nav aria-label="Bản đồ khái niệm">`, kèm danh sách lồng nhau `<ul>/<li>` cho trình đọc màn hình.
- **Dữ liệu/State:** Đọc trạng thái từ `hdh_mastery_v1` để tô màu các nút (xám: M0, vàng: M1, xanh: M2, tím: M3).
- **Phản mẫu sư phạm (Anti-patterns):** Sơ đồ mạng nhện rối rắm vô định hướng (spaghetti graph); các liên kết không có nhãn định nghĩa ngữ nghĩa (labeled edges).

---

### 4.2. `ProblemHook` (Cái móc Vấn đề Kỹ thuật)
- **Mục đích:** Kích hoạt sự tò mò nhận thức (epistemic curiosity) bằng cách chỉ ra nghịch lý hoặc bế tắc thực tế nếu thiếu cơ chế này.
- **Khi nào dùng:** Luôn luôn là khối nội dung đầu tiên sau tiêu đề của mỗi khái niệm mới.
- **Khi nào KHÔNG dùng:** Trong phần tóm tắt ôn tập cuối chương.
- **Thể hiện trên PDF/Print:** Khung viền nét đứt màu xám đậm (Dashed Callout) với tiêu đề `[VẤN ĐỀ THỰC TẾ CỦA KỸ SƯ OS]`.
- **Thể hiện trên Web Companion:** Thẻ `<aside class="problem-hook" role="region" aria-labelledby="...">` với biểu tượng mỏ neo ⚓ và câu hỏi chốt chặn được bôi đậm.
- **Khả năng tiếp cận:** Tiêu đề cấp con rõ ràng, độ tương phản văn bản đạt chuẩn WCAG AAA.
- **Dữ liệu/State:** Tĩnh (Stateless).
- **Phản mẫu sư phạm:** Mở đầu bằng định nghĩa từ điển sáo rỗng (*"Quản lý bộ nhớ là một thành phần quan trọng của hệ điều hành..."*).

---

### 4.3. `MentalModel` (Mô hình Tư duy Trực quan)
- **Mục đích:** Neo giữ logic phần cứng vào một mô hình không gian/vật lý trực quan, giúp người học giải thích được cơ chế mà không cần học vẹt.
- **Khi nào dùng:** Khi giới thiệu các cơ chế phần cứng trừu tượng (như MMU Relocation Register, Bảng phân trang, TLB Cache).
- **Khi nào KHÔNG dùng:** Khi giải các bài toán số học thuần túy.
- **Thể hiện trên PDF/Print:** Hình minh họa kèm phép so sánh đối ngẫu (Side-by-side comparison): cột trái là Phép ẩn dụ thực tế (Metaphor), cột phải là Cơ chế phần cứng thực tế (Hardware Reality).
- **Thể hiện trên Web Companion:** Thẻ `<div class="mental-model-card">` tích hợp nút chuyển đổi góc nhìn (Toggle Perspective: "Ẩn dụ đời sống" $\leftrightarrow$ "Thanh ghi thực tế").
- **Khả năng tiếp cận:** Văn bản thay thế (alt-text) mô tả đầy đủ cấu trúc tương đồng giữa hai thế giới.
- **Dữ liệu/State:** Tĩnh.
- **Phản mẫu sư phạm:** Sử dụng các phép ẩn dụ sai lệch bản chất kỹ thuật (ví dụ: ví phân trang như việc cắt một cuốn sách nhưng không giải thích được vai trò của bảng chỉ mục).

---

### 4.4. `PredictionCheckpoint` (Điểm Kiểm tra Dự đoán)
- **Mục đích:** Kích hoạt hiệu ứng siêu sửa sai (Hypercorrection Effect). Buộc người học cam kết một phương án logic trước khi xem giải pháp.
- **Khi nào dùng:** Ngay trước khi trình bày một giải thuật phân bổ, một quy tắc chuyển đổi địa chỉ, hoặc một trường hợp biên.
- **Khi nào KHÔNG dùng:** Khi đang liệt kê các thông số kỹ thuật thuần túy.
- **Thể hiện trên PDF/Print:** Khung hộp câu hỏi có dòng chữ in đậm: `DỪNG LẠI! Hãy viết dự đoán của bạn ra giấy trước khi đọc dòng tiếp theo.` Giải pháp được in lộn ngược hoặc đặt ở trang sau.
- **Thể hiện trên Web Companion:** Khung nhập văn bản (Scratchpad Textarea) hoặc 3 nút chọn kịch bản. **Văn bản giải thích cơ chế bên dưới bị ẩn (blurred/locked)** cho đến khi người học bấm nút `Xác nhận Dự đoán`.
- **Khả năng tiếp cận:** Thuộc tính `aria-expanded="false"` chuyển thành `"true"` sau khi mở khóa; thông báo giọng nói `aria-live="polite"` xác nhận câu trả lời.
- **Dữ liệu/State:** Lưu dự đoán tạm thời vào `hdh_prediction_drafts` trong `localStorage`.
- **Phản mẫu sư phạm:** Để đáp án lộ thiên ngay bên dưới câu hỏi khiến mắt người học tự động quét qua mà không hề suy nghĩ.

---

### 4.5. `ExecutionTrace` (Bảng Vết Thực thi Trạng thái)
- **Mục đích:** Cung cấp minh chứng cụ thể, định lượng, không thể chối cãi về cách thức dữ liệu biến đổi qua từng chu kỳ xung nhịp hoặc từng bước thuật toán.
- **Khi nào dùng:** Tất cả các bài toán chuyển đổi địa chỉ, thuật toán cấp phát liên tục (First/Best/Next/Worst Fit), tính EAT, và phân trang.
- **Khi nào KHÔNG dùng:** Giải thích các khái niệm triết lý thiết kế tổng quan.
- **Thể hiện trên PDF/Print:** Bảng dữ liệu đa cột được căn lề chuẩn mực: `Bước` | `Đầu vào (Thanh ghi/Tiến trình)` | `Trạng thái Bộ nhớ/Bảng trang` | `Phép tính / Biện luận logic` | `Đầu ra vật lý`.
- **Thể hiện trên Web Companion:** Bảng dữ liệu tương tác với khả năng làm nổi bật (highlight) dòng hiện tại, đi kèm sơ đồ bộ nhớ đồ họa đồng bộ (visual memory map sync).
- **Khả năng tiếp cận:** Thẻ `<table>` ngữ nghĩa hoàn chỉnh với `<caption>`, `<th scope="col">`, `<th scope="row">`.
- **Dữ liệu/State:** Tĩnh hoặc điều khiển chuyển bước (stepper) lưu bước hiện tại trong session.
- **Phản mẫu sư phạm:** Bỏ qua các bước tính trung gian; chỉ đưa ra trạng thái đầu và trạng thái cuối mà không giải thích sự biến đổi của con trỏ.

---

### 4.6. `RecallCheckpoint` (Điểm Thu hồi Kín sách)
- **Mục đích:** Buộc não bộ thực hiện thao tác trích xuất thông tin tự thân (Generative Retrieval), đánh giá chính xác mức độ hiểu sâu M2.
- **Khi nào dùng:** Kết thúc mỗi phần lý thuyết trọng điểm.
- **Khi nào KHÔNG dùng:** Ngay giữa lúc đang giải thích dở dang một luồng xử lý.
- **Thể hiện trên PDF/Print:** Hộp câu hỏi tự luận với biểu tượng chiếc chìa khóa 🗝️. Đáp án mẫu và danh sách từ khóa bắt buộc nằm ở Phụ lục kiểm tra cuối sách.
- **Thể hiện trên Web Companion:** Thành phần Active Recall Card nâng cấp:
  - Khung câu hỏi hiển thị kín sách.
  - Vùng nhập văn bản tự trả lời (Scratchpad).
  - Nút `Hiện gợi ý (Hint)` (nếu dùng thì tối đa chỉ đạt M1).
  - Nút `Đối soát Rubric`: Mở danh sách **Từ khóa bắt buộc** và **Tiêu chí chấm điểm từng phần**.
  - Bộ 4 nút tự đánh giá chính xác: `[M0: Quên]`, `[M1: Cần Gợi Ý]`, `[M2: Tự Giải Thích Tốt]`, `[M3: Tự Tin Chuyển Giao]`.
- **Khả năng tiếp cận:** Phím tắt điều hướng `1, 2, 3, 4` tương ứng với 4 mức tự đánh giá; thông báo trạng thái qua ARIA.
- **Dữ liệu/State:** Ghi nhận trực tiếp vào `hdh_mastery_v1[conceptId]` và đẩy lịch vào `hdh_spaced_scheduler_v1`.
- **Phản mẫu sư phạm:** Câu hỏi dạng Đúng/Sai (True/False) có xác suất đoán mò 50%; câu hỏi kiểm tra ghi nhớ chi tiết vụn vặt thay vì nguyên lý vận hành.

---

### 4.7. `WorkedExample` (Bài tập Mẫu Toàn vẹn - Level A)
- **Mục đích:** Xây dựng lược đồ nhận thức chuẩn mực cho sinh viên mới tiếp cận dạng bài thi tính toán, hạn chế tối đa tải nhận thức ngoại lai.
- **Khi nào dùng:** Lần đầu tiên xuất hiện một dạng bài tập định lượng (như Bài 1 về Phân vùng động, Bài 3 về EAT trong slide UIT).
- **Khi nào KHÔNG dùng:** Khi sinh viên đã vượt qua bài tập mức độ trung bình.
- **Thể hiện trên PDF/Print:** Lời giải chuẩn 3 pha:
  1. *Pha 1: Tóm tắt đề bài & Trích xuất tham số phần cứng.*
  2. *Pha 2: Lập bảng vết thực thi và công thức áp dụng.*
  3. *Pha 3: Kết luận & Đánh giá phân mảnh / độ trễ.*
- **Thể hiện trên Web Companion:** Thẻ `<div class="worked-example level-a">` với huy hiệu `Level A: Bài Tập Mẫu Chuẩn`, mỗi bước giải có chú giải lề bên cạnh (margin callouts) giải thích lý do tại sao làm như vậy.
- **Khả năng tiếp cận:** Đánh số bước tuần tự `Bước 1: ...`, `Bước 2: ...`.
- **Dữ liệu/State:** Tĩnh.
- **Phản mẫu sư phạm:** Trình bày lời giải tắt theo kiểu làm mẹo của học sinh luyện thi; không viết rõ công thức tổng quát trước khi thay số.

---

### 4.8. `FadedExample` (Bài tập Giàn giáo Phai mờ - Level B)
- **Mục đích:** Chuyển dịch dần trách nhiệm nhận thức từ tài liệu sang não bộ sinh viên, chuẩn bị cho năng lực độc lập giải quyết bài toán.
- **Khi nào dùng:** Ngay sau Bài tập Mẫu Level A.
- **Khi nào KHÔNG dùng:** Khi sinh viên chưa từng xem bài mẫu nào thuộc dạng này.
- **Thể hiện trên PDF/Print:** Bảng tính được điền sẵn 50% (ví dụ: đã giải xong phân vùng 1 và 2), các dòng 3 và 4 để trống kèm dòng kẻ chấm `......` và câu hỏi mồi: `[Tính toán phân vùng 3 tại đây: Kích thước = ? Trạng thái con trỏ = ?]`.
- **Thể hiện trên Web Companion:** Khung điền khuyết tương tác (Interactive Fill-in-the-blanks / Scaffolded Inputs) với cơ chế kiểm tra kết quả từng ô ngay lập tức (instant inline validation) mà không để lộ đáp án của toàn bài.
- **Khả năng tiếp cận:** Các thẻ `<input aria-label="Nhập kích thước phân vùng còn lại">` có nhãn ngữ cảnh cụ thể.
- **Dữ liệu/State:** Lưu bài làm dở dang vào `hdh_practice_drafts_v1`.
- **Phản mẫu sư phạm:** Làm mờ các chi tiết không quan trọng (như đơn vị đo) thay vì làm mờ bước tư duy logic then chốt.

---

### 4.9. `TransferProblem` (Bài toán Chuyển giao Độc lập - Level C)
- **Mục đích:** Thẩm định và xác lập năng lực làm chủ tối cao M3. Người học phải độc lập áp dụng lược đồ vào hoàn cảnh mới lạ.
- **Khi nào dùng:** Khối chốt chặn cuối cùng của mỗi chủ đề bài tập.
- **Khi nào KHÔNG dùng:** Khi người học đang chật vật ở mức M0 hoặc M1.
- **Thể hiện trên PDF/Print:** Đề bài độc lập kèm thông số biên lạ (ví dụ: bảng trang 3 cấp, kích thước trang không phải lũy thừa thông thường, hoặc tiến trình bị từ chối cấp phát), đi kèm khung tự làm và thang điểm rubric tự chấm.
- **Thể hiện trên Web Companion:** Trình luyện tập tự luận nâng cao (Subjective Practice Container) gồm:
  - Đề bài chi tiết.
  - Đồng hồ đếm giờ làm bài chuẩn kỳ thi UIT.
  - Vùng soạn thảo bài giải đầy đủ.
  - Khối Rubric tiêu chí chấm điểm chi tiết (ẩn mặc định, chỉ mở sau khi sinh viên đã nộp bài).
- **Khả năng tiếp cận:** Tiêu chuẩn form đầy đủ, hỗ trợ nộp bài bằng bàn phím `Ctrl + Enter`.
- **Dữ liệu/State:** Tự động lưu bản nháp liên tục; ghi nhận điểm số tự chấm vào `hdh_mastery_v1` để kích hoạt trạng thái M3.
- **Phản mẫu sư phạm:** Cung cấp đề bài y hệt bài mẫu, chỉ thay đổi số liệu một cách vô nghĩa (chỉ là algorithmic drilling chứ không phải cognitive transfer).

---

### 4.10. `ErrorDiagnosis` (Chẩn đoán Lỗi sai & Bẫy Đề thi)
- **Mục đích:** Tận dụng lỗi sai điển hình để tái cấu trúc mô hình nhận thức, biến các quan niệm sai lầm phổ biến thành bài học phòng thủ trong kỳ thi.
- **Khi nào dùng:** Sau mỗi dạng bài tập lớn hoặc các khái niệm dễ gây nhầm lẫn.
- **Khi nào KHÔNG dùng:** Khi chưa giải thích cơ chế đúng (tránh gieo rắc nhầm lẫn quá sớm).
- **Thể hiện trên PDF/Print:** Bảng 3 cột kinh điển: `Quan niệm sai lầm phổ biến` | `Phân tích nguyên nhân gốc rễ` | `Cách khắc phục & Kỹ thuật kiểm tra trong phòng thi`.
- **Thể hiện trên Web Companion:** Thẻ `<div class="error-diagnosis-card">` màu hổ phách/đỏ nhạt, có nút bấm "Xem tư duy sai lầm của 70% sinh viên" để người học tự soi chiếu bài làm của mình.
- **Khả năng tiếp cận:** Đánh dấu cảnh báo `role="alert"` mang tính sư phạm.
- **Dữ liệu/State:** Lưu vết các lỗi người học thường mắc vào `hdh_mistakes_log_v1`.
- **Phản mẫu sư phạm:** Chỉ trích sinh viên bất cẩn mà không giải thích cơ chế nhận thức dẫn đến sự nhầm lẫn đó.

---

### 4.11. `ReviewHook` (Móc Nối Ôn tập Cách quãng)
- **Mục đích:** Tích hợp liền mạch khái niệm vừa học vào hệ thống ôn tập phân tán dài hạn.
- **Khi nào dùng:** Cuối mỗi đơn vị bài học.
- **Khi nào KHÔNG dùng:** Ở đầu trang.
- **Thể hiện trên PDF/Print:** Khung hộp nhỏ ghi rõ: `Lịch ôn tập đề xuất: Ngày +1, Ngày +3, Ngày +7, Ngày +16. Đánh dấu vào ô kiểm khi hoàn thành.`
- **Thể hiện trên Web Companion:** Nút bấm `Thêm vào Hàng đợi Ôn tập Hôm nay` và hiển thị trực quan ngày đến hạn ôn tập tiếp theo dựa trên thuật toán Spaced Review.
- **Khả năng tiếp cận:** Nút bấm tương tác đầy đủ với nhãn trạng thái `aria-live`.
- **Dữ liệu/State:** Đẩy bản ghi vào cấu trúc lập lịch `hdh_spaced_scheduler_v1`.
- **Phản mẫu sư phạm:** Đòi hỏi sinh viên phải tự nhớ ngày để quay lại ôn tập một cách thủ công.

---

### 4.12. `MasteryCheck` (Trạm Kiểm soát Năng lực Chương)
- **Mục đích:** Cung cấp đánh giá chuẩn mực cuối chương (Summative Criterion Check) để xác nhận học phần sẵn sàng cho kỳ thi kết thúc môn.
- **Khi nào dùng:** Duy nhất ở phần kết thúc của mỗi chương.
- **Khi nào KHÔNG dùng:** Trong các bài học riêng lẻ.
- **Thể hiện trên PDF/Print:** Bài kiểm tra tổng hợp kín sách gồm 1 câu hỏi cơ chế cốt lõi và 2 bài toán chuyển giao định lượng.
- **Thể hiện trên Web Companion:** Bảng điều khiển năng lực tổng thể (Mastery Dashboard) của chương hiển thị tỷ lệ % các mục đạt M2/M3, danh sách các khái niệm đang bị suy thoái cần ôn tập gấp.
- **Khả năng tiếp cận:** Cấu trúc tiêu đề phân cấp chuẩn, bảng số liệu có hỗ trợ screen-reader.
- **Dữ liệu/State:** Tổng hợp toàn bộ dữ liệu từ `hdh_mastery_v1` của toàn bộ các thẻ trong chương.
- **Phản mẫu sư phạm:** Chỉ kiểm tra trắc nghiệm lý thuyết thuần túy mà không có bài toán tính toán kỹ thuật.

---

## 5. KIẾN TRÚC BỘ LẬP LỊCH ÔN TẬP CÁCH QUÃNG CỤC BỘ (LOCAL DETERMINISTIC SPACED-REVIEW SCHEDULER)

Hệ thống cam kết: **100% Cục bộ (Local-First), Không Máy chủ (Serverless), Không Tài khoản (Zero-Account), Hoàn toàn Xác định (Deterministic), Tuyệt đối Không sử dụng AI/Chatbot.**

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│             KIẾN TRÚC BỘ LẬP LỊCH CÁCH QUÃNG DỰA TRÊN LOCALSTORAGE              │
│                                                                                  │
│   [ Người học Đánh giá ] ────────► [ Bộ tính toán Khoảng cách ]                 │
│   (Thang điểm 1, 2, 3, 4)            - Tính Hệ số Dễ (EF)                       │
│                                      - Tính Khoảng cách Mới (Interval)           │
│                                      - Tính Ngày đến hạn (Due Date)             │
│                                                     │                            │
│                                                     ▼                            │
│   [ Hàng đợi Ôn tập ] ◄──────────── [ Cập nhật hdh_spaced_scheduler_v1 ]         │
│   (Ưu tiên = Trễ hạn / S)             (Lưu trữ cục bộ an toàn)                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1. Thuật toán Lập lịch Thích ứng Xác định (Deterministic SM-2 Adaptation)
Thay vì sử dụng các khoảng cách cố định tùy tiện ngụy khoa học (như cố định 1-3-7-15 ngày), chúng tôi sử dụng mô hình thích ứng dựa trên thuật toán SM-2 chuẩn hóa, điều chỉnh tự động theo phản hồi thực tế của người học:

#### A. Tham số trạng thái của mỗi thẻ (Item State Vector):
Mỗi đơn vị kiến thức $i$ được lưu giữ bởi bộ 5 tham số:
$$\mathbf{S}_i = \langle M_i, \text{Reps}_i, \text{EF}_i, I_i, \text{DueDate}_i \rangle$$
Trong đó:
- $M_i \in \{\text{M0, M1, M2, M3}\}$: Cấp độ năng lực hiện tại.
- $\text{Reps}_i \in \mathbb{N}$: Số lần ôn tập thành công liên tiếp.
- $\text{EF}_i \in [1.3, 2.8]$: Hệ số Dễ (Easiness Factor), khởi tạo mặc định bằng $2.5$.
- $I_i \in \mathbb{N}$: Khoảng cách ôn tập hiện tại tính bằng số ngày (Interval).
- $\text{DueDate}_i$: Dấu thời gian ngày đến hạn ôn tập (Unix timestamp, chuẩn hóa về 00:00:00 của ngày theo giờ địa phương).

#### B. Thang điểm đánh giá của người học ($q \in \{1, 2, 3, 4\}$):
- $q = 1$ (Tương ứng M0 - Thất bại hoàn toàn): Hoàn toàn không nhớ được cơ chế, quên công thức.
- $q = 2$ (Tương ứng M1 - Khó khăn): Nhớ được sau khi mở xem gợi ý, tính toán còn lúng túng.
- $q = 3$ (Tương ứng M2 - Tự giải thích tốt): Tự suy luận và giải đúng mà không cần bất kỳ trợ giúp nào.
- $q = 4$ (Tương ứng M3 - Chuyển giao xuất sắc): Giải quyết trôi chảy bài toán lạ, chỉ ra được các bẫy biên.

#### C. Hàm chuyển đổi trạng thái toán học:
1. **Cập nhật Hệ số Dễ $\text{EF}'$:**
   $$\text{EF}' = \max\left(1.3, \; \text{EF} + (0.1 - (4 - q) \times (0.08 + (4 - q) \times 0.02))\right)$$
   *(Nếu người học chọn $q = 4$, $\text{EF}$ tăng nhẹ; nếu $q = 1$ hoặc $2$, $\text{EF}$ giảm mạnh để rút ngắn các chu kỳ sau).*

2. **Cập nhật Số lần thành công $\text{Reps}'$ và Khoảng cách mới $I'$:**
   - Nếu $q < 3$ (Thất bại / Khó khăn nghiêm trọng):
     $$\text{Reps}' = 0, \quad I' = 1 \text{ ngày}, \quad M' = \min(M, \text{M1})$$
     *(Thẻ bị đẩy về hàng đợi ôn tập của ngày hôm sau).*
   - Nếu $q \ge 3$ (Thành công):
     $$\text{Reps}' = \text{Reps} + 1$$
     $$I' = \begin{cases} 
       1 \text{ ngày} & \text{khi } \text{Reps}' = 1 \\
       3 \text{ ngày} & \text{khi } \text{Reps}' = 2 \\
       \text{round}(I \times \text{EF}') & \text{khi } \text{Reps}' \ge 3 
     \end{cases}$$
     - Cập nhật cấp độ năng lực:
       - Nếu $q = 3 \implies M' = \max(M, \text{M2})$
       - Nếu $q = 4$ và người học đã giải Transfer Problem $\implies M' = \text{M3}$

3. **Cập nhật Ngày đến hạn mới:**
   $$\text{DueDate}' = \text{Today} + (I' \times 86400000 \text{ ms})$$

### 5.2. Công thức Ưu tiên Hàng đợi Ôn tập (Review Queue Priority Formula)
Hàng ngày, hệ thống quét toàn bộ các thẻ đã lưu trong `localStorage` để tính toán chỉ số ưu tiên (Priority Score):
$$\text{Priority}(i) = \frac{\text{Today} - \text{DueDate}_i}{I_i} + \Delta_{\text{Interleave}}(i)$$
- Các thẻ quá hạn nhiều nhất so với chu kỳ của chính nó sẽ được đẩy lên đầu hàng đợi.
- $\Delta_{\text{Interleave}}(i)$ là hệ số điều chỉnh xen kẽ: ngăn chặn việc xuất hiện liên tiếp 3 thẻ cùng một chủ đề hẹp, chủ động trộn các câu hỏi thuộc các chủ đề khác nhau để kích hoạt khả năng phân biệt.

---

## 6. NGUYÊN LÝ XEN KẼ CHỌN LỌC (SELECTIVE INTERLEAVING SPECIFICATION)

### 6.1. Khi nào NÊN và KHÔNG NÊN Xen kẽ?
Xen kẽ (Interleaving) là việc trộn lẫn các dạng bài tập khác nhau trong cùng một buổi học. Tuy nhiên, theo Rohrer & Taylor (2007), **xen kẽ vô tội vạ sẽ phản tác dụng và gây sụp đổ nhận thức**.

- **KHÔNG ĐƯỢC XEN KẼ KHI:**
  - Người học đang trong giai đoạn đầu hình thành lược đồ (M0 $\to$ M1). Lúc này cần luyện tập khối liên tục (Blocked Practice) để não bộ nhận diện rõ cấu trúc giải thuật.
  - Hai khái niệm hoàn toàn không liên quan về mặt cấu trúc (ví dụ: trộn bài tập Định thời CPU của Chương 4 với bài tập Banker của Chương 6). Điều này chỉ gây nhiễu loạn tinh thần vô ích.
- **BẮT BUỘC XEN KẼ KHI (Selective Interleaving):**
  - Hai hoặc nhiều khái niệm **có đặc điểm bề mặt rất giống nhau nhưng quy luật bản chất bên dưới hoàn toàn khác nhau**. Người học thường xuyên nhầm lẫn trong phòng thi vì không biết *khi nào nên dùng công cụ nào*.

### 6.2. Ma trận Phân biệt Đối kháng trong Hệ Điều Hành IT007

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│              MA TRẬN CÁC CẶP KHÁI NIỆM BẮT BUỘC PHẢI XEN KẼ ĐỐI KHÁNG            │
│                                                                                  │
│   1. Phân mảnh Nội (Internal)       ◄────────►  Phân mảnh Ngoại (External)       │
│      (Dư thừa bên trong phân vùng)              (Lỗ hổng vụn giữa các phân vùng) │
│                                                                                  │
│   2. Chiến lược First Fit           ◄────────►  Next Fit / Best Fit / Worst Fit  │
│      (Quét từ đầu danh sách)                    (Quét tiếp từ con trỏ / Quét tối ưu)│
│                                                                                  │
│   3. Địa chỉ Logic (Virtual)        ◄────────►  Địa chỉ Vật lý (Physical)        │
│      (Phát sinh bởi CPU: p, d)                  (Trỏ vào bus RAM: f, d)          │
│                                                                                  │
│   4. Bảng trang Cấp phát (Paging)   ◄────────►  Phân đoạn (Segmentation)         │
│      (Cố định phần cứng, vô hình)               (Kích thước biến thiên, logic)   │
│                                                                                  │
│   5. TLB Miss                       ◄────────►  Page Fault                       │
│      (Trượt cache CPU, tra RAM)                 (Trang chưa nạp, đọc Disk I/O)   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

Mỗi buổi luyện tập chuyển giao (Transfer Session) bắt buộc phải cấu hình tối thiểu một bài toán xen kẽ đối kháng, yêu cầu sinh viên:
1. Xác định ngay loại vấn đề trước khi áp dụng công thức.
2. Giải thích tại sao phương pháp đối nghịch lại thất bại trong trường hợp này.

---

## 7. HỆ THỐNG GIÀN GIÁO PHAI MỜ BÀI TẬP MẪU (WORKED-EXAMPLE FADING SYSTEM)

Chuỗi phai mờ 3 cấp độ (Level A $\to$ Level B $\to$ Level C) được áp dụng đồng bộ cho tất cả các dạng bài toán kỹ thuật của môn học:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     TIẾN TRÌNH PHAI MỜ NHẬN THỨC (FADING CONTINUUM)             │
│                                                                                  │
│    [ LEVEL A: WORKED EXAMPLE ] ──────────────────────────────────────────────┐   │
│    - Cung cấp: 100% Đề bài + 100% Lời giải + 100% Biện luận từng bước        │   │
│    - Trách nhiệm người học: Đọc hiểu, theo dõi vết thực thi, tự giải thích   │   │
│                                                                              │   │
│                                      ▼                                       │   │
│    [ LEVEL B: FADED EXAMPLE ] ───────────────────────────────────────────────┤   │
│    - Cung cấp: 100% Đề bài + 50% Khung bảng + Các bước neo chặn 1 & 2        │   │
│    - Trách nhiệm người học: Tự tính toán và điền khuyết bước 3 & 4           │   │
│                                                                              │   │
│                                      ▼                                       │   │
│    [ LEVEL C: INDEPENDENT TRANSFER ] ────────────────────────────────────────┘   │
│    - Cung cấp: Đề bài độc lập + Bẫy biên lạ + Không có bất kỳ khung sẵn      │   │
│    - Trách nhiệm người học: 100% Tự vẽ bảng, tự tính toán, tự đối soát      │   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Tiêu chuẩn Thiết kế Giàn giáo:
- **Nguyên tắc Bảo toàn Cấu trúc:** Cả 3 cấp độ bài tập đều phải sử dụng chung một cấu trúc bảng vết thực thi và chung một quy ước ký hiệu. Sự khác biệt duy nhất là **tỷ lệ giàn giáo bị rút bỏ**.
- **Chốt chặn Kiểm tra Hợp lý (Sanity Checks):** Trong Level B, hệ thống cung cấp các câu hỏi kiểm tra tính nhất quán (ví dụ: *"Tổng dung lượng các phân mảnh nội cộng lại có bằng dung lượng trống ban đầu trừ đi dung lượng tiến trình không?"*) để người học tập thói quen tự kiểm tra bài thi.

---

## 8. KIỂM TOÁN VÀ ĐÁNH GIÁ CÁC THÀNH PHẦN GIAO DIỆN HIỆN CÓ (COMPONENT AUDIT)

Dưới đây là kết quả kiểm toán nghiêm ngặt về mặt sư phạm và kiến trúc thông tin đối với các thành phần hiện diện trong mã nguồn `src/web/`:

| Thành phần | Hiện trạng trong mã nguồn | Đánh giá Sư phạm Khoa học | Phán quyết Kiến trúc | Kế hoạch Hành động Chi tiết |
| :--- | :--- | :--- | :---: | :--- |
| **`StudyCard`** | Có câu hỏi, gợi ý, từ khóa, lời giải, nhưng dùng nút nhị phân `[✅ Đã Thuộc]` và `[❌ Chưa Nhớ]`. | **Yếu kém về sư phạm.** Gây ra ảo tưởng thành thạo (Illusion of Competence). Không ghi nhận được mức độ tự giải thích hay chuyển giao; không có liên kết với bộ lập lịch thích ứng. | **`UPGRADE`** | Thay thế bộ nút nhị phân bằng 4 nút chọn Mastery `M0, M1, M2, M3`. Tích hợp vùng nháp (Scratchpad) buộc người học gõ câu trả lời trước khi bấm hiện lời giải. Lưu dữ liệu vào `hdh_mastery_v1` và cập nhật thuật toán SM-2. |
| **`SubjectivePractice`** | Có đề bài, vùng textarea tự làm, nút mở rubric, các checkbox chấm điểm từng phần và bộ tính điểm. | **Rất tốt về mặt sư phạm.** Đã áp dụng nguyên lý tự đánh giá theo tiêu chí chuẩn mực (Criterion-referenced self-assessment). Cần nâng cấp cơ chế phai mờ và phản hồi lỗi. | **`UPGRADE`** | Bổ sung các gợi ý phai mờ (Faded Hints) mở theo từng mức độ; bổ sung chốt chặn cảnh báo lỗi sai phổ biến (Error Diagnosis tags); liên kết điểm số $\ge 80\%$ để tự động xác lập năng lực M3. |
| **`Knowledge Graph`** | Vẽ đồ thị canvas 2D bằng tọa độ tĩnh từ `graph_data.json`, hiển thị các vòng tròn nối với nhau, bấm vào để chuyển link. | **Giá trị sư phạm cực thấp; mang tính trang trí.** Đồ thị hiện tại không thể hiện được thứ tự quan hệ tiên quyết (DAG), không hiển thị tiến độ học tập của người học, chỉ làm tăng tải nhận thức ngoại lai và làm chậm thời gian tải trang. | **`DE-EMPHASIZE`** | Loại bỏ khỏi luồng học tập chính của trang chủ. Nếu giữ lại, phải tái cấu trúc thành **Cây Quan hệ Tiên quyết (Prerequisite Dependency DAG)** có tô màu trạng thái Mastery thực tế của người học, thay vì mạng nhện vô bổ. |
| **`TOC & Navigation`** | Sidebar phân cấp tĩnh theo chương mục, có chỉ mục tìm kiếm client-side. | **Tốt về mặt cấu trúc thông tin.** Tuy nhiên chưa phản ánh được trạng thái học tập của sinh viên. Sinh viên không biết mình đã hoàn thành phần nào ở mức M2 hay M3. | **`UPGRADE`** | Bổ sung huy hiệu tiến độ trực tiếp trên từng mục của sidebar: hiển thị tỷ lệ M2/M3 và chấm đỏ cảnh báo các mục có câu hỏi đến hạn ôn tập (`Due Review Badge`). |
| **`Search Modal`** | Tìm kiếm tĩnh client-side qua `search_index.json`. | **Rất xuất sắc.** Tốc độ tức thì, hoạt động hoàn hảo khi offline, hỗ trợ tra cứu nhanh công thức và định nghĩa trong lúc làm bài tập. | **`KEEP`** | Giữ nguyên kiến trúc; bổ sung thêm nhãn phân loại nội dung trong kết quả tìm kiếm (Lý thuyết / Bài tập mẫu / Thuật toán). |

---

## 9. ĐẶC TẢ KIẾN TRÚC DỮ LIỆU CỤC BỘ (LOCALSTORAGE SCHEMA SPECIFICATION)

Toàn bộ dữ liệu tiến độ của người học được quản lý độc lập dưới 4 khóa `localStorage` với tiền tố chuẩn mực `hdh_`:

```json
{
  "hdh_mastery_v1": {
    "CH07_MMU_LOGICAL_PHYSICAL": {
      "level": "M2",
      "last_updated": 1725372000000,
      "history": [
        {"timestamp": 1725285600000, "rated": 1, "state": "M0"},
        {"timestamp": 1725372000000, "rated": 3, "state": "M2"}
      ]
    }
  },

  "hdh_spaced_scheduler_v1": {
    "CH07_QBANK_03": {
      "reps": 3,
      "ef": 2.5,
      "interval_days": 6,
      "due_timestamp": 1725890400000,
      "last_reviewed": 1725372000000,
      "urgency_score": 1.2
    }
  },

  "hdh_practice_drafts_v1": {
    "CH07_PRACTICE_PAGE_TABLE_CALC": {
      "draft_text": "Ta có không gian địa chỉ 32-bit, kích thước trang 4KB...",
      "checked_rubric": [true, true, false],
      "self_score": 0.75,
      "last_saved": 1725372150000
    }
  },

  "hdh_mistakes_log_v1": {
    "CH07_ERR_INTERNAL_FRAG": {
      "error_id": "CONFUSED_INTERNAL_EXTERNAL",
      "count": 2,
      "last_occurred": 1725372050000,
      "concept_id": "CH07_FRAGMENTATION"
    }
  }
}
```

### Tính năng Bảo vệ & Xuất nhập Dữ liệu (Backup / Restore):
Giao diện tĩnh cung cấp hai chức năng thuần túy client-side trong trang Cài đặt / Ôn tập:
1. **`Xuất Tiến độ (Export Progress)`:** Tải về tệp JSON chứa toàn bộ dữ liệu học tập của 4 khóa trên.
2. **`Nhập Tiến độ (Import Progress)`:** Đọc tệp JSON và khôi phục lại trạng thái ôn tập mà không làm gián đoạn hệ thống.

---

## 10. TỔNG KẾT & QUY TẮC BÀN GIAO SƯ PHẠM (PEDAGOGICAL SIGN-OFF)

1. **Không chatbot, không gọi API ngoài, không thu thập danh tính sinh viên.**
2. **Tiêu chuẩn in ấn PDF:** Mọi thành phần tương tác phải suy giảm êm dịu (graceful degradation) sang dạng hộp văn bản tĩnh có dòng kẻ nháp và phụ lục đối soát.
3. **Tiêu chuẩn Web:** 100% tương thích thiết bị di động, hoạt động hoàn hảo ở chế độ ngoại tuyến (Offline-First / Local-First).
4. **Bản đồ Sư phạm Chương 7 ([CH07_PEDAGOGICAL_BLUEPRINT.md](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/CH07_PEDAGOGICAL_BLUEPRINT.md)) là tài liệu thực thi bắt buộc trước khi bắt đầu bất kỳ dòng văn bản nào của Chương 7.**

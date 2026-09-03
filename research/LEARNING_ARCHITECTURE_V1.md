# HDH_UIT V2 — KIẾN TRÚC HỌC TẬP V1.1 (LEARNING ARCHITECTURE V1.1)
# BẢN ĐẶC TẢ SƯ PHẠM THỰC CHỨNG & THIẾT KẾ TRẢI NGHIỆM HỌC TẬP IT007
# MỤC ĐÍCH: TỐI ƯU HÓA HIỆU QUẢ HỌC TẬP, GIẢM TẢI NHẬN THỨC, HỖ TRỢ IN ẤN PDF VÀ WEB TĨNH

---

## 1. NỀN TẢNG KHOA HỌC NHẬN THỨC (SCIENTIFIC FOUNDATIONS)

Kiến trúc học tập của dự án HDH_UIT V2 được xây dựng dựa trên các nghiên cứu thực nghiệm trong Khoa học Nhận thức (Cognitive Science), Tâm lý học Giáo dục và Thiết kế Đa phương tiện. Hệ thống kiên quyết bác bỏ các giả thuyết chưa được kiểm chứng (như phong cách học tập VAK, thuyết bán cầu não) hoặc các quy tắc phân bổ tùy tiện (như quy tắc 70/20/10).

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   MÔ HÌNH XỬ LÝ THÔNG TIN & TẢI NHẬN THỨC                         │
│                                                                                  │
│   [ Kích thích ] ──► [ Bộ nhớ Cảm giác ] ──► [ Bộ nhớ Làm việc (Working Memory) ] │
│   (Tài liệu/Web)       (Sensory Register)      - Giới hạn: ~4 đơn vị thông tin   │
│                                                - Tải: Nội tại & Ngoại lai        │
│                                                               ▲         │        │
│                                            Thu hồi chủ động   │         │Ghi mã  │
│                                            (Retrieval)        │         ▼(Schema)│
│                                              [ Bộ nhớ Dài hạn (Long-Term Memory) ]│
│                                                - Mạng lưới lược đồ liên kết     │
│                                                - Suy giảm theo thời gian         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1. Lý thuyết Tải nhận thức (Cognitive Load Theory - Sweller, Paas, van Merriënboer)
- **Cấu trúc bộ nhớ:** Bộ nhớ làm việc (Working Memory - WM) của con người có dung lượng hạn chế (khoảng $4 \pm 1$ đơn vị thông tin khi xử lý các yếu tố tương tác, theo Cowan, 2001). Ngược lại, Bộ nhớ dài hạn (Long-Term Memory - LTM) lưu trữ thông tin dưới dạng các lược đồ nhận thức (schemas). Khi một lược đồ được tự động hóa, nó được xử lý như một đơn vị duy nhất trong WM.
- **Phân rã 3 thành phần Tải nhận thức:**
  1. *Tải nội tại (Intrinsic Cognitive Load):* Độ phức tạp cố hữu của bản thân khái niệm kỹ thuật (ví dụ: sự phối hợp giữa CPU, thanh ghi MMU, bảng phân trang và bus địa chỉ). Tải này không thể giảm bớt mà chỉ có thể quản lý thông qua việc phân đoạn (segmentation) và sắp xếp trình tự hợp lý.
  2. *Tải ngoại lai (Extraneous Cognitive Load):* Gánh nặng nhận thức phát sinh do thiết kế trình bày kém (như tra cứu nhảy trang, văn bản dài dòng không ăn nhập với hình ảnh, giao diện rối rắm). Mục tiêu sư phạm là **tối thiểu hóa tối đa tải ngoại lai**.
  3. *Tải hữu ích (Germane Cognitive Load):* Nỗ lực nhận thức của người học nhằm xây dựng và củng cố các lược đồ nhận thức (so sánh đối chiếu, tự giải thích nguyên lý, phân tích lỗi sai).
- **Các hiệu ứng trình bày cần kiểm soát:**
  - *Split-Attention Effect (Hiệu ứng phân tán chú ý):* Tránh việc tách rời hình minh họa và văn bản giải thích. Nhãn linh kiện và bước chuyển trạng thái phải được đặt trực tiếp trên sơ đồ.
  - *Redundancy Effect (Hiệu ứng dư thừa):* Không đọc lại y nguyên từng từ của sơ đồ; văn bản đi kèm chỉ tập trung vào cơ chế nhân quả.

### 1.2. Luyện tập Thu hồi & Hiệu ứng Kiểm tra (Retrieval Practice & Testing Effect)
- **Nghiên cứu nền tảng (Roediger & Karpicke, 2006; Dunlosky et al., 2013):**
  Hành động tự kiểm tra kín sách (Closed-book Retrieval) củng cố các đường dẫn trích xuất thông tin trong trí nhớ dài hạn, tạo ra độ bền trí nhớ vượt trội so với việc đọc lại nhiều lần (Passive Re-reading). Việc đọc lại thường tạo ra cảm giác trôi chảy giả tạo (*Illusion of Competence*), khiến người học ngỡ rằng mình đã nắm vững nhưng lại thất bại khi giải bài tập mới.

### 1.3. Luyện tập Phân tán (Distributed Practice & Spacing Effect)
- **Nghiên cứu nền tảng (Cepeda et al., 2006, 2008):**
  Phân chia các lượt học cách quãng theo thời gian mang lại hiệu quả ghi nhớ lâu dài tốt hơn nhiều so với việc dồn ép trong một thời gian ngắn (*Cramming*). Khoảng cách tối ưu giữa các lần ôn tập phụ thuộc vào thời gian muốn duy trì trí nhớ, không tuân theo các chu kỳ cứng nhắc cố định.

### 1.4. Hiệu ứng Bài tập Mẫu & Phai mờ Dần Dần (Worked-Example Effect & Fading)
- **Nghiên cứu nền tảng (Sweller, 1988; Renkl, 2014; Atkinson et al., 2000):**
  Đối với người học mới (novice), việc nghiên cứu các bài tập mẫu có lời giải chi tiết (Worked Examples) hiệu quả hơn việc tự mày mò giải bài toán mở, do giảm thiểu tải nhận thức ngoại lai. Khi năng lực tăng lên, giàn giáo cần được làm mờ dần (Fading) để tránh hiện tượng đảo ngược chuyên gia (*Expertise Reversal Effect*).

### 1.5. Hiệu ứng Phát sinh & Phân biệt Dự đoán vs Siêu sửa sai
- **Generation Effect (Slamecka & Graf, 1978; Kornell, Hays & Bjork, 2009):** Tự tạo ra câu trả lời hoặc đưa ra dự đoán trước khi xem đáp án kích hoạt mạng lưới ngữ nghĩa và hướng sự chú ý của người học vào thông tin phản hồi.
- **Hypercorrection Effect (Butterfield & Metcalfe, 2001, 2006; Metcalfe, 2017):** Hiện tượng người học sửa chữa sai lầm nhanh và sâu sắc hơn khi lỗi sai đó được cam kết với **mức độ tự tin cao** (*High-confidence error*), thay vì các lỗi sai do đoán mò. Điều này đòi hỏi thiết kế phải cho phép người học bộc lộ quan niệm sai lầm trước khi nhận phản hồi.

### 1.6. Khung Nhận thức ICAP & Tự giải thích (Chi & Wylie, 2014)
- **Phân tầng hoạt động học tập:** Passive (Thụ động: đọc lướt) $\to$ Active (Chủ động: gạch chân, tạm dừng) $\to$ Constructive (Kiến tạo: tự giải thích, suy luận) $\to$ Interactive (Tương tác: tranh luận, đối soát tiêu chí). Học sâu chỉ diễn ra khi người học đạt mức Constructive trở lên.

---

## 2. MA TRẬN BẰNG CHỨNG KHOA HỌC (EVIDENCE MATRIX)

| Nguyên lý Thiết kế | Nguồn Tham chiếu Khoa học | Độ tin cậy Bằng chứng | Giới hạn & Điểm cần lưu ý | Hệ quả Thiết kế Hệ thống |
| :--- | :--- | :---: | :--- | :--- |
| **Retrieval Practice** | Roediger & Karpicke (2006); Dunlosky et al. (2013) | Rất cao (Robust / Meta-analyses) | Cần phản hồi (Feedback) chính xác sau khi thu hồi để tránh củng cố sai lầm. | Bắt buộc có các trạm RecallCheckpoint; ẩn đáp án mặc định; cung cấp rubric từ khóa đối soát ngay sau khi trả lời. |
| **Spaced Practice** | Cepeda et al. (2006, 2008); Pashler et al. (2007) | Rất cao | Không có khoảng cách "vàng" cố định cho mọi người; phụ thuộc vào độ khó nội dung. | Thiết kế thuật toán lên lịch ôn tập thích ứng cục bộ dựa trên phản hồi độ khó của người học; tránh chu kỳ cố định 1-3-7. |
| **Worked-Example Fading** | Renkl & Atkinson (2003); Sweller et al. (2011) | Cao | Nếu duy trì bài mẫu quá lâu sẽ gây phản tác dụng đối với người học đã vững (*Expertise Reversal*). | Chuỗi 3 cấp độ: Level A (Mẫu $100\%$) $\to$ Level B (Khuyết bước $50\%$) $\to$ Level C (Độc lập $0\%$). |
| **Prediction Before Feedback** | Kornell et al. (2009); Richland et al. (2009) | Trung bình - Cao | Có thể gây ức chế nếu câu hỏi dự đoán quá mơ hồ hoặc gây hiểu lầm nghiêm trọng. | Câu hỏi dự đoán phải xoay quanh sự cố kỹ thuật cụ thể; phản hồi phải giải thích trực tiếp cơ chế vì sao đúng/sai. |
| **Hypercorrection** | Butterfield & Metcalfe (2001, 2006); Metcalfe (2017) | Cao (Phạm vi hẹp) | Chỉ xuất hiện khi người học có niềm tin mạnh vào câu trả lời sai; không áp dụng cho đoán mò. | Khối ErrorDiagnosis phải tập trung vào các bẫy đề thi kinh điển mà sinh viên thường tin là mình làm đúng. |
| **Selective Interleaving** | Rohrer & Taylor (2007); Kornell & Bjork (2008) | Trung bình - Cao | Không xen kẽ các chủ đề không liên quan; chỉ xen kẽ các khái niệm có nguy cơ nhầm lẫn bề mặt cao. | Chỉ áp dụng xen kẽ đối kháng giữa các cặp: Phân mảnh nội vs ngoại, First Fit vs Best Fit, Paging vs Segmentation. |
| **Spatial Contiguity** | Mayer (2009, 2021); Fiorella & Mayer (2015) | Rất cao | Tránh làm sơ đồ quá tải chi tiết gây nhiễu chú ý. | Sơ đồ phần cứng MMU, TLB, Bảng phân trang phải có chú thích gắn liền trên hình; không dùng bảng chú giải tách rời. |
| **Cognitive Load Minimal** | Sweller (1988, 2011); van Merriënboer (2019) | Rất cao | Giảm tải ngoại lai không có nghĩa là lược bỏ bài tập khó mang tính thử thách đáng giá (*Desirable difficulty*). | Áp dụng Quy tắc Tối giản Sư phạm: loại bỏ đồ thị trang trí, loại bỏ hình ảnh thừa; giao diện tập trung 1 tác vụ/khung nhìn. |

---

## 3. NGUYÊN TẮC HỌC TẬP CỐT LÕI & QUY TẮC TỐI GIẢN SƯ PHẠM

### 3.1. Nguyên tắc Học tập Cốt lõi (Core Learning Principle)
Hệ thống từ bỏ cấu trúc 11 bước cứng nhắc cho mọi khái niệm. Thay vào đó, toàn bộ kiến trúc vận hành theo chu trình 6 giai đoạn linh hoạt:

$$\mathbf{Map \;\longrightarrow\; Understand \;\longrightarrow\; Retrieve \;\longrightarrow\; Apply \;\longrightarrow\; Diagnose \;\longrightarrow\; Revisit}$$

1. **Map (Định vị):** Nắm bắt vị trí khái niệm trong bức tranh toàn cảnh hệ thống.
2. **Understand (Hiểu bản chất):** Tiếp cận mô hình tư duy và cơ chế vận hành phần cứng/HĐH.
3. **Retrieve (Thu hồi chủ động):** Tự tái tạo quy tắc và giải thích bản chất mà không nhìn tài liệu.
4. **Apply (Ứng dụng giải quyết bài toán):** Đi từ bài mẫu có giàn giáo đến bài toán độc lập.
5. **Diagnose (Chẩn đoán & Sửa sai):** Đối chiếu với các bẫy nhận thức phổ biến.
6. **Revisit (Ôn tập cách quãng):** Tái kích hoạt lược đồ theo lịch trình phân tán.

### 3.2. Quy tắc Tối giản Sư phạm (Pedagogical Minimalism Rule)
> [!IMPORTANT]
> **QUY TẮC TỐI GIẢN SƯ PHẠM:**
> *"Nếu một khối nội dung hoặc thành phần giao diện không làm thay đổi tư duy suy luận, khả năng thu hồi, sự phân biệt khái niệm, hoặc năng lực chuyển giao của người học, HÃY LOẠI BỎ NÓ."*
> 
> Không một khái niệm nào được phép mang gánh nặng của các khối hình thức. Mỗi khái niệm chỉ sử dụng số lượng khối nguyên thủy tối thiểu cần thiết để đạt mục tiêu nhận thức.

---

## 4. MA TRẬN MÔ THỨC SƯ PHẠM THÍCH ỨNG (ADAPTIVE PEDAGOGICAL PATTERNS)

Mỗi nội dung được phân loại vào một trong 6 mô thức sư phạm tương ứng:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   CÁC MÔ THỨC SƯ PHẠM THEO LOẠI NỘI DUNG                         │
│                                                                                  │
│   Mô thức A (Định nghĩa / Phân biệt):                                            │
│   [ MentalModel / Contrast ] ─────────────────────────► [ RecallCheckpoint ]     │
│                                                                                  │
│   Mô thức B (Cơ chế Phần cứng / Giao thức):                                      │
│   [ ProblemHook ] ──► [ MentalModel ] ──► [ ExecutionTrace ] ──► [ RecallCheck ] │
│                                                                                  │
│   Mô thức C (Thuật toán / Chiến lược):                                           │
│   [ PredictCheck ] ─► [ ExecutionTrace ] ─► [ FadedExample ] ─► [ ErrorDiagnosis]│
│                                                                                  │
│   Mô thức D (Kỹ năng Tính toán Định lượng):                                      │
│   [ WorkedExample (Lvl A) ] ─► [ FadedExample (Lvl B) ] ─► [ Transfer (Lvl C) ]  │
│                                                                                  │
│   Mô thức E (Thông số Kiến trúc / Hằng số Phần cứng):                             │
│   [ Concise Technical Fact ] ─────────────────────────► [ Optional Flash Recall ]│
│                                                                                  │
│   Mô thức F (Tổng hợp Toàn Chương):                                              │
│   [ ConceptMap ] ─────────────────────────────────────► [ MasteryCheck ]         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| Mô thức Sư phạm | Loại Khái niệm | Chuỗi Khối Nguyên thủy Đề xuất | Ví dụ trong Chương 7 (Bộ nhớ) |
| :--- | :--- | :--- | :--- |
| **Mô thức A** | Định nghĩa & Phân biệt cặp | `MentalModel` hoặc `Contrast/Compare` $\to$ `RecallCheckpoint` | Phân mảnh nội vs Phân mảnh ngoại; Địa chỉ logic vs Địa chỉ vật lý. |
| **Mô thức B** | Cơ chế phần cứng / Giao thức | `ProblemHook` $\to$ `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint` | Cơ chế MMU thanh ghi Relocation/Limit; Cơ chế TLB Cache; Cơ chế Swapping. |
| **Mô thức C** | Thuật toán phân bổ | `PredictionCheckpoint` $\to$ `ExecutionTrace` $\to$ `FadedExample` $\to$ `TransferProblem` $\to$ `ErrorDiagnosis` | Thuật toán First Fit, Best Fit, Next Fit, Worst Fit. |
| **Mô thức D** | Kỹ năng tính toán định lượng | `WorkedExample (A)` $\to$ `FadedExample (B)` $\to$ `TransferProblem (C)` $\to$ `ErrorDiagnosis` | Dịch địa chỉ phân trang $(p,d) \to (f,d)$; Tính toán EAT; Tính kích thước bảng trang 2 cấp. |
| **Mô thức E** | Thông số kỹ thuật / Hằng số | `Concise Technical Fact` $\to$ `Optional Recall` | Giới hạn kích thước trang $2^n$; Băng thông bus địa chỉ. |
| **Mô thức F** | Tích hợp cấp chương | `ConceptMap` $\to$ `MasteryCheck` | Bản đồ phân cấp toàn chương; Bài thi thử tổng hợp cuối chương. |

---

## 5. BA CHẾ ĐỘ TRẢI NGHIỆM WEB (THREE WEB MODES)

Để đáp ứng các giai đoạn học tập khác nhau và không gây phiền nhiễu cho sinh viên trong giai đoạn ôn thi nước rút, giao diện Web Companion hỗ trợ 3 chế độ độc lập:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         BA CHẾ ĐỘ TRẢI NGHIỆM WEB COMPANION                      │
│                                                                                  │
│   [ CHẾ ĐỘ 1: LEARN MODE ]                                                       │
│   - Đối tượng: Người học lần đầu / Học sâu.                                      │
│   - Hành vi: Tiết lộ tiệm tiến có giàn giáo (Progressive Disclosure).            │
│   - Quy tắc: Ẩn lời giải mặc định, mở khóa sau khi suy nghĩ/nháp.                │
│                                                                                  │
│   [ CHẾ ĐỘ 2: REVIEW MODE ]                                                      │
│   - Đối tượng: Ôn tập hàng ngày / Xử lý câu hỏi đến hạn.                         │
│   - Hành vi: Chỉ hiển thị các mục cần thu hồi, câu hỏi yếu (M0/M1), bài tập lỗi. │
│   - Quy tắc: Tinh gọn tối đa, bỏ qua văn bản lý thuyết dài dòng.                 │
│                                                                                  │
│   [ CHẾ ĐỘ 3: REFERENCE MODE ]                                                   │
│   - Đối tượng: Tra cứu nhanh trong phòng lab / Ôn thi cấp tốc trước giờ G.       │
│   - Hành vi: Toàn bộ nội dung hiển thị mở $100\%$ ngay lập tức.                  │
│   - Quy tắc: KHÔNG bắt buộc dự đoán, KHÔNG ẩn đáp án, tìm kiếm tức thì.          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Quy tắc chuyển đổi:** Nút chuyển chế độ được đặt cố định trên thanh điều hướng đầu trang (`Learn` / `Review` / `Reference`), lưu lựa chọn vào `localStorage["hdh_ui_mode"]`. Mặc định khi truy cập lần đầu là `Learn Mode`. Khi bật `Reference Mode`, toàn bộ các khối tương tác tự động chuyển sang trạng thái mở hoàn toàn.

---

## 6. MÔ HÌNH PHÂN TÁCH NĂNG LỰC (MASTERY) & ĐÁNH GIÁ ÔN TẬP (REVIEW RATING)

> [!CAUTION]
> **LỖ HỔNG THIẾT KẾ CŨ ĐÃ ĐƯỢC KHẮC PHỤC:**
> Trong kiến trúc trước đây, người học có thể tự bấm nút để gán cho mình mức $M3$. Đây là sai lầm sư phạm nghiêm trọng. Hệ thống mới phân tách rạch ròi giữa **Bằng chứng Năng lực (Mastery Evidence)** và **Đánh giá Trải nghiệm Ôn tập (Review Rating)**.

### 6.1. Bốn Cấp độ Năng lực (Mastery Evidence: M0 – M3)
Cấp độ năng lực phản ánh mức độ độc lập và chuyển giao kiến thức được chứng minh qua hành vi:

| Cấp độ | Tên gọi | Định nghĩa Nhận thức | Bằng chứng Hành vi Bắt buộc (Evidence Requirement) |
| :---: | :--- | :--- | :--- |
| **M0** | `NOT_RECALLED` | Chưa học hoặc Không thể thu hồi. | Trả lời sai hoặc bỏ trắng bài kiểm tra kín sách; chưa từng làm bài tập. |
| **M1** | `FAMILIAR` | Nhận diện được khi có mồi gợi ý (*Cue-dependent*). | Trả lời đúng sau khi xem gợi ý (*Hint*); hoặc điền đúng bài tập giàn giáo Level B. |
| **M2** | `CAN_EXPLAIN` | Tự giải thích được bản chất nhân quả (WHY & HOW). | Trả lời đúng câu hỏi `RecallCheckpoint` kín sách, đối soát đạt $\ge 80\%$ từ khóa rubric bắt buộc (Ghi nhận dưới dạng `SELF_ASSESSED_M2` hoặc `VERIFIED_M2`). |
| **M3** | `CAN_TRANSFER` | Độc lập chuyển giao năng lực sang bài toán thi cử mới lạ. | **CHỈ ĐƯỢC XÁC LẬP KHI:** Giải thành công bài toán `TransferProblem` (Level C) với tham số biên mới mà không dùng bất kỳ gợi ý nào. **`RecallCheckpoint` không thể trực tiếp nâng lên M3.** |

### 6.2. Thang Đánh giá Lượt Ôn tập (Review Rating Scale)
Thang đánh giá 4 mức độ dùng để cung cấp tham số cho thuật toán lập lịch ôn tập, hoàn toàn độc lập với danh hiệu Mastery:
- **`AGAIN` (Làm lại):** Không nhớ hoặc giải sai hoàn toàn $\implies$ Đẩy về ôn tập ngay trong ngày/ngày hôm sau.
- **`HARD` (Khó khăn):** Nhớ được nhưng mất nhiều thời gian, còn do dự hoặc cần liếc gợi ý $\implies$ Rút ngắn khoảng cách chu kỳ tới.
- **`GOOD` (Tốt):** Thu hồi chính xác, giải thích tự tin với nỗ lực nhận thức vừa phải $\implies$ Giãn khoảng cách theo hệ số tiêu chuẩn.
- **`EASY` (Dễ dàng):** Kiến thức đã đạt mức tự động hóa cao, giải quyết tức thì $\implies$ Tăng mạnh khoảng cách chu kỳ tới.

### 6.3. Cấu trúc Dữ liệu Mô hình Năng lực (State Schema)
```json
{
  "concept_id": "CH07_PAGE_TRANSLATION",
  "mastery_state": "M2",
  "mastery_evidence": {
    "recall_passed": true,
    "recall_timestamp": 1725372000000,
    "transfer_passed": false,
    "transfer_score": null,
    "verification_mode": "SELF_ASSESSED"
  },
  "review_schedule": {
    "reps": 3,
    "easiness_factor": 2.5,
    "interval_days": 6,
    "due_timestamp": 1725890400000,
    "last_reviewed": 1725372000000
  },
  "review_rating_history": [
    {"timestamp": 1725199200000, "rating": "AGAIN"},
    {"timestamp": 1725285600000, "rating": "GOOD"},
    {"timestamp": 1725372000000, "rating": "GOOD"}
  ],
  "mistake_history": [
    {"error_tag": "ERR_FORGOT_OFFSET", "count": 1, "last_timestamp": 1725199200000}
  ]
}
```

---

## 7. ĐÁNH GIÁ & QUYẾT ĐỊNH THUẬT TOÁN LẬP LỊCH ÔN TẬP CỤC BỘ

### 7.1. So sánh 3 Phương án Thuật toán Lập lịch

| Tiêu chí Đánh giá | Phương án A: Hộp Leitner Xác định Đơn giản | Phương án B: SuperMemo-2 (SM-2 Chuẩn hóa) | Phương án C: FSRS (Free Spaced Repetition) |
| :--- | :--- | :--- | :--- |
| **Bản chất Thuật toán** | 3–5 ngăn cố định, chuyển ngăn theo kết quả Đúng/Sai. | Công thức nhân khoảng cách với Hệ số Dễ thích ứng: $I_n = I_{n-1} \times \text{EF}$. | Mô hình toán học 3 thành phần: Stability, Retrievability, Difficulty với 17 trọng số. |
| **Độ phức tạp triển khai** | Cực thấp ($\sim 30$ dòng mã JS). | Thấp - Trung bình ($\sim 80$ dòng mã JS thuần túy). | Rất cao ($\sim 400+$ dòng mã toán ma trận, gradient descent). |
| **Khả năng chạy Ngoại tuyến** | Hoàn hảo $100\%$. | Hoàn hảo $100\%$. | Khả thi nhưng đòi hỏi bundle toán học phức tạp. |
| **Dung lượng `localStorage`** | Tối thiểu ($< 5\text{KB}$). | Nhỏ ($< 15\text{KB}$ cho toàn bộ môn học). | Lớn hơn đáng kể do ma trận trọng số và log chi tiết. |
| **Hành vi Khởi đầu Lạnh** | Tốt, dễ hiểu cho người mới. | Tốt, tham số mặc định $\text{EF}=2.5$ ổn định ngay từ ngày đầu. | Cần dữ liệu luyện tập lớn để tối ưu hóa trọng số cá nhân. |
| **Tính Kiểm thử & Bảo trì** | Rất dễ viết unit test. | Rất dễ viết unit test kiểm tra tính xác định. | Khó gỡ lỗi khi lịch trình sai lệch. |
| **Độ chính xác Khoa học** | Thấp, khoảng cách bị bó cứng. | Rất cao trong thực tiễn 30 năm ứng dụng giáo dục. | Cao nhất hiện nay trên tập dữ liệu lớn. |

### 7.2. Quyết định Kiến trúc: Lựa chọn Phương án B (SM-2 Project Heuristic)
> [!NOTE]
> **QUYẾT ĐỊNH DỰ ÁN:**
> Dự án lựa chọn **Biến thể SM-2 Xác định (Deterministic SM-2 Project Heuristic)** làm thuật toán lập lịch mặc định.
> - Chúng tôi không tuyên bố thuật toán này là tối ưu tuyệt đối về mặt toán học sinh học, mà định danh rõ ràng đây là **Quy tắc Thực nghiệm của Dự án (Project Heuristic)** nhằm cân bằng hoàn hảo giữa tính khoa học, sự minh bạch và tính gọn nhẹ cục bộ.

#### Chi tiết Thuật toán Dự án (Project Heuristic Formula):
1. **Khởi tạo:** Với mỗi thẻ mới: $\text{Reps} = 0, \text{EF} = 2.5, I = 0$.
2. **Khi người học gửi Đánh giá ($q \in \{\text{AGAIN}, \text{HARD}, \text{GOOD}, \text{EASY}\}$):**
   - Quy đổi điểm đánh giá: $\text{AGAIN} \to 1, \text{HARD} \to 2, \text{GOOD} \to 3, \text{EASY} \to 4$.
   - **Cập nhật Hệ số Dễ $\text{EF}'$:**
     $$\text{EF}' = \max\left(1.3, \; \text{EF} + (0.1 - (4 - q) \times (0.08 + (4 - q) \times 0.02))\right)$$
   - **Cập nhật Chu kỳ $I'$ (Số ngày):**
     - Nếu $q < 3$ ($\text{AGAIN}$ hoặc $\text{HARD}$ nghiêm trọng):
       $$\text{Reps}' = 0, \quad I' = 1 \text{ ngày}$$
     - Nếu $q \ge 3$:
       $$\text{Reps}' = \text{Reps} + 1$$
       $$I' = \begin{cases} 
         1 \text{ ngày} & \text{khi } \text{Reps}' = 1 \\
         3 \text{ ngày} & \text{khi } \text{Reps}' = 2 \\
         \text{round}(I \times \text{EF}') & \text{khi } \text{Reps}' \ge 3 
       \end{cases}$$
       *(Nếu $q = 4$ ($\text{EASY}$), nhân thêm hệ số thưởng $1.15$).*
   - **Cập nhật Ngày đến hạn:** $\text{DueDate}' = \text{Hôm nay} + (I' \times 86400000\text{ ms})$.

---

## 8. QUY CHUẨN TRẢI NGHIỆM IN ẤN PDF & TỐI GIẢN GIAO DIỆN (UX / PDF DESIGN)

### 8.1. Quy chuẩn In ấn & Sử dụng Sách PDF
1. **Không in chữ lộn ngược:** Tuyệt đối không dùng kỹ thuật in văn bản đảo ngược gây khó chịu khi đọc và làm hỏng trải nghiệm người dùng.
2. **Phân tách không gian câu hỏi và lời giải:**
   - Câu hỏi `RecallCheckpoint` hoặc bài tập xuất hiện trực tiếp trong mạch đọc của bài.
   - Đáp án, tiêu chí từ khóa rubric và lời giải hoàn chỉnh được đặt tại **Khối Lời giải Cuối bài** hoặc **Phụ lục Lời giải Cuối chương**. Điều này tạo ra sự ma sát vật lý có chủ đích (*Physical friction*), ngăn ngừa mắt người học liếc thấy đáp án trước khi suy nghĩ.
3. **Tính tương thích Đơn sắc (Grayscale Compatibility):**
   - Mọi sơ đồ phân vùng bộ nhớ, bảng phân trang, và biểu đồ tiến trình phải phân biệt được bằng đường viền nét đứt/gạch chéo/hoa văn (pattern fills) kết hợp độ tương phản sáng tối, không dựa thuần túy vào màu sắc xanh/đỏ để truyền tải thông điệp.
4. **Cận kề không gian:** Nhãn sơ đồ phải nằm liền kề linh kiện; tuyệt đối không để sơ đồ ở trang trước và chú giải số ở trang sau.

### 8.2. Tối giản Giao diện Web (UX Minimalism)
- **Quy tắc Một Tác vụ Nhận thức Trọng tâm:** Tại một thời điểm cuộn trang, màn hình chỉ nên trình bày một tác vụ nhận thức duy nhất (hoặc đọc hiểu cơ chế, hoặc đưa ra dự đoán, hoặc làm bài tập tính toán).
- **Loại bỏ rác thị giác (Visual Clutter):**
  - Không hiệu ứng pháo hoa, không thanh tiến trình gây stress, không bảng xếp hạng đua điểm.
  - Không dùng các biểu tượng emoji bừa bãi; chỉ sử dụng các icon kỹ thuật chức năng chuẩn mực.
  - Khối đồ thị kiến thức (Knowledge Graph) dạng mạng nhện 2D bị loại bỏ khỏi luồng học chính; chỉ duy trì dưới dạng cây sơ đồ tiên quyết (Prerequisite Tree) khi cần tra cứu lộ trình.

---

## 9. KIỂM TOÁN THÀNH PHẦN KỸ THUẬT HIỆN TẠI & BÀN GIAO TRIỂN KHAI

### 9.1. Kiểm toán Thành phần Kỹ thuật (Technical Component Audit)

| Thành phần | Hiện trạng Mã nguồn | Đánh giá Nhận thức | Quyết định | Kế hoạch Nâng cấp |
| :--- | :--- | :--- | :---: | :--- |
| **`StudyCard`** | Renderer tạo ra các vùng ẩn `.card-hint`, `.card-keypoints`, `.card-answer`. CSS có `.card-section { display: none; }`. Nút hành động gồm `✅ Đã Thuộc` và `❌ Chưa Nhớ`. | Nhị phân hóa sai lầm năng lực nhận thức; dung dưỡng ảo tưởng quen thuộc. | **`UPGRADE`** | Thay thế bằng 4 nút Review Rating (`AGAIN`, `HARD`, `GOOD`, `EASY`); tích hợp khung gõ nháp; phân tách trạng thái Mastery $M0$–$M3$. |
| **`SubjectivePractice`** | Textarea làm bài, nút so sánh rubric, checkbox trọng số và bảng tính điểm. | Rất tốt về mặt sư phạm (đánh giá theo tiêu chuẩn). | **`UPGRADE`** | Bổ sung các bước giàn giáo phai mờ (Level B); tích hợp nhãn chẩn đoán lỗi; ghi nhận bằng chứng `SELF_ASSESSED_M2` hoặc `VERIFIED_M3`. |
| **`Knowledge Graph`** | Canvas 2D vẽ đồ thị hình tròn tĩnh từ `graph_data.json`. | Giá trị sư phạm thấp; tăng tải ngoại lai. | **`DE-EMPHASIZE`** | Đưa xuống chân trang hoặc trang chuyên biệt; tái cấu trúc thành cây phụ thuộc tiên quyết (Prerequisite DAG) có màu sắc thể hiện tiến độ Mastery. |
| **`TOC & Sidebar`** | Danh sách điều hướng tĩnh theo thư mục. | Tốt cho định vị nhưng chưa có phản hồi năng lực. | **`UPGRADE`** | Bổ sung huy hiệu tiến độ M2/M3 theo từng chương mục; thêm chấm báo hiệu các mục có câu hỏi đến hạn ôn tập (`Due Badge`). |

### 9.2. Bàn giao Kỹ thuật: Phát hiện Lỗi Renderer Hiện tại
> [!WARNING]
> **HỒ SƠ BÀN GIAO KỸ THUẬT: ENG-LEARN-002 — MAJOR**
> - **Mô tả lỗi:** Trong mã nguồn `scripts/build_web.py` hiện tại, hàm `render_callout` tạo ra các thẻ nội dung ẩn `.card-hint`, `.card-keypoints`, `.card-answer` với CSS ẩn (`display: none`). Tệp JavaScript `src/web/assets/js/app.js` được lập trình để lắng nghe sự kiện bấm trên các nút `.btn-hint`, `.btn-keypoints`, `.btn-answer`. Tuy nhiên, trình tạo mã `build_web.py` **hoàn toàn chưa phát sinh các nút bấm này** vào cây DOM HTML.
> - **Hệ quả:** Người học trên web không có cách nào bấm để mở gợi ý hoặc lời giải của thẻ StudyCard; cơ chế tiết lộ tiệm tiến bị tê liệt một phần.
> - **Kế hoạch xử lý:** Đã ghi nhận vào hồ sơ bàn giao triển khai kỹ thuật (Implementation Handoff). **Không sửa đổi mã nguồn web trong lượt thiết kế của Luna.**

---

## 10. THƯ MỤC THAM KHẢO RÚT GỌN (COMPACT BIBLIOGRAPHY)

1. **Atkinson, R. K., Derry, S. J., Renkl, A., & Wortham, D.** (2000). Learning from examples: Instructional principles from the worked examples research. *Review of Educational Research*, 70(2), 181–214.
2. **Butterfield, B., & Metcalfe, J.** (2001). Errors committed with high confidence are hypercorrected. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 27(6), 1491–1494.
3. **Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D.** (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354–380.
4. **Chi, M. T. H., & Wylie, R.** (2014). The ICAP framework: Linking cognitive engagement to active learning outcomes. *Educational Psychologist*, 49(4), 219–243.
5. **Cowan, N.** (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87–114.
6. **Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T.** (2013). Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology. *Psychological Science in the Public Interest*, 14(1), 4–58.
7. **Fiorella, L., & Mayer, R. E.** (2015). *Learning as a Generative Activity: Eight Learning Strategies that Promote Understanding*. Cambridge University Press.
8. **Kornell, N., Hays, M. J., & Bjork, R. A.** (2009). Unsuccessful retrieval attempts enhance subsequent learning. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 35(4), 989–998.
9. **Mayer, R. E.** (2021). *Multimedia Learning* (3rd ed.). Cambridge University Press.
10. **Metcalfe, J.** (2017). Learning from errors. *Annual Review of Psychology*, 68, 465–489.
11. **Renkl, A.** (2014). Toward an instructionally oriented theory of example-based learning. *Cognitive Science*, 38(1), 1–37.
12. **Roediger, H. L., & Karpicke, J. D.** (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249–255.
13. **Rohrer, D., & Taylor, K.** (2007). The shuffling of mathematics problems improves learning. *Instructional Science*, 35(6), 481–498.
14. **Sweller, J.** (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257–285.
15. **Sweller, J., Ayres, P., & Kalyuga, S.** (2011). *Cognitive Load Theory*. Springer Science & Business Media.

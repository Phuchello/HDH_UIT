# HDH_UIT V2 — KIẾN TRÚC HỌC TẬP V1.2 (LEARNING ARCHITECTURE V1.2)
# BẢN ĐẶC TẢ SƯ PHẠM THỰC CHỨNG & THIẾT KẾ TRẢI NGHIỆM HỌC TẬP IT007
# MỤC ĐÍCH: TỐI ƯU HÓA HIỆU QUẢ HỌC TẬP, GIẢM TẢI NHẬN THỨC, HỖ TRỢ IN ẤN PDF VÀ WEB TĨNH
# CHẾ ĐỘ: THIẾT KẾ & ĐẶC TẢ SƯ PHẠM (FINAL EVIDENCE & PROVENANCE CLOSEOUT)

---

## 0. HỒ SƠ THẨM ĐỊNH & KHẮC PHỤC THIẾT KẾ (DESIGN RECHECK FINDINGS)

> [!NOTE]
> **SCHED-LEARN-001 — MAJOR — RESOLVED: Hiệu chỉnh Toàn diện So sánh FSRS**
> - Phân định rạch ròi giữa **Thời gian chạy Lập lịch (Scheduling Runtime)** (chạy thuần giải tích trong vài micro-giây với bộ tham số mặc định chuẩn, không cần vòng lặp tối ưu, hoạt động ngay từ ngày đầu với dữ liệu trống) và **Tối ưu hóa Tham số (Parameter Optimization / Personalization)** (tùy chọn huấn luyện cá nhân hóa khi đã tích lũy lịch sử đánh giá).
>
> **SCHED-LEARN-002 — MAJOR — RESOLVED: Phân định Rạch ròi Đánh giá HARD vs Lỗi Thu hồi (AGAIN)**
> - Phân tách rõ ràng hành vi toán học của cả 4 mức đánh giá. `AGAIN` là thất bại thu hồi (đặt lại chu kỳ về 1 ngày, tăng biến đếm lapse). `HARD` là thu hồi thành công có khó khăn (tăng số lần thành công, tăng khoảng cách chu kỳ một cách thận trọng, không đặt lại chu kỳ về 1 ngày).
>
> **SCHED-LEARN-003 — MAJOR — RESOLVED: Chuẩn hóa Lịch sử Phiên bản FSRS Có Gắn Nhãn Thời Điểm**
> - Cập nhật chính xác lịch sử tham số của các phiên bản FSRS upstream: FSRS v4 / v4.5 sử dụng 17 tham số; FSRS-5 sử dụng 19 tham số; FSRS-6 sử dụng 21 tham số.
> - Ghi nhận bối cảnh nghiên cứu thực nghiệm (thời điểm 2026-09): các biến thể nghiên cứu/benchmark (như FSRS-7 với 35 tham số) đang được thử nghiệm trong các bài đo lường hiệu năng nhưng không mặc định suy diễn rằng phiên bản Anki stable đã chuyển sang FSRS-7.
> - Đánh giá so sánh được ghi rõ thời điểm (2026-09) và không khẳng định số lượng tham số là bất biến vĩnh viễn.
>
> **EVID-LEARN-002 — MAJOR — RESOLVED: Hiện đại hóa Thuật ngữ Khoa học Nhận thức**
> - Cập nhật theo Lý thuyết Tải nhận thức đương đại (Sweller, van Merriënboer & Paas, 2019): tải nhận thức gồm Tải nội tại (Intrinsic load) và Tải ngoại lai (Extraneous load); Xử lý hữu ích (Germane processing) là nguồn lực nhận thức được người học phân bổ để tiếp nhận tải nội tại và xây dựng lược đồ, không phải là một thành phần tải độc lập thứ ba cộng dồn. Khung ICAP (Chi & Wylie, 2014) được định nghĩa chính xác là một mô hình phân tầng dự báo kết quả học tập ($\text{Interactive} > \text{Constructive} > \text{Active} > \text{Passive}$) phụ thuộc vào điều kiện nhiệm vụ và mức độ chuyên môn của người học.
>
> **EVID-LEARN-003 — MAJOR — RESOLVED: Loại bỏ Trích dẫn Chưa Xác thực & Phân định Nguồn Nghiên cứu**
> - Bãi bỏ hoàn toàn trích dẫn không được kiểm chứng "Ye, J., et al. (2024)".
> - Bổ sung trích dẫn nghiên cứu khoa học phản biện chuẩn mực (Peer-reviewed Research): Ye, Su, & Cao (KDD 2022) về thuật toán đường đi ngẫu nhiên ngắn nhất tối ưu hóa lập lịch giãn cách (dòng nghiên cứu tiền thân MaiMemo/DHP/SSP-MMC).
> - Phân định rõ ràng mục riêng cho Tài liệu Kỹ thuật Triển khai Mã nguồn mở (Non-peer-reviewed Technical Documentation): Tài liệu thuật toán FSRS của Open-Spaced-Repetition và Anki Manual.
>
> **ENG-LEARN-002 — MAJOR — IMPLEMENTATION HANDOFF (Bảo lưu cho Terra)**
> - Bộ tạo mã `scripts/build_web.py` hiện tại chưa phát sinh các nút bấm `.btn-hint`, `.btn-keypoints`, `.btn-answer` mà `src/web/assets/js/app.js` đang lắng nghe. Vấn đề này được ghi nhận trong hồ sơ bàn giao kỹ thuật cho pha triển khai của Terra; không chỉnh sửa mã nguồn renderer trong lượt thiết kế này.

---

## 1. NỀN TẢNG KHOA HỌC NHẬN THỨC (SCIENTIFIC FOUNDATIONS)

Kiến trúc học tập của dự án HDH_UIT V2 được xây dựng dựa trên các nghiên cứu thực nghiệm trong Khoa học Nhận thức (Cognitive Science), Tâm lý học Giáo dục và Thiết kế Đa phương tiện. Hệ thống kiên quyết bác bỏ các giả thuyết chưa được kiểm chứng (như phong cách học tập VAK, thuyết bán cầu não) hoặc các quy tắc phân bổ tùy tiện (như quy tắc 70/20/10).

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   MÔ HÌNH XỬ LÝ THÔNG TIN & TẢI NHẬN THỨC                         │
│                                                                                  │
│   [ Kích thích ] ──► [ Bộ nhớ Cảm giác ] ──► [ Bộ nhớ Làm việc (Working Memory) ] │
│   (Tài liệu/Web)       (Sensory Register)      - Giới hạn: ~4 đơn vị tương tác   │
│                                                - Tải: Nội tại & Ngoại lai        │
│                                                               ▲         │        │
│                                            Thu hồi chủ động   │         │Ghi mã  │
│                                            (Retrieval)        │         ▼(Schema)│
│                                              [ Bộ nhớ Dài hạn (Long-Term Memory) ]│
│                                                - Mạng lưới lược đồ liên kết     │
│                                                - Suy giảm theo thời gian         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1. Lý thuyết Tải nhận thức Đương đại (Cognitive Load Theory - Sweller, Paas, van Merriënboer)
- **Cấu trúc bộ nhớ:** Bộ nhớ làm việc (Working Memory - WM) của con người có dung lượng hạn chế (khoảng $4 \pm 1$ đơn vị thông tin khi xử lý các yếu tố tương tác đồng thời, theo Cowan, 2001). Ngược lại, Bộ nhớ dài hạn (Long-Term Memory - LTM) lưu trữ thông tin dưới dạng các mạng lưới lược đồ nhận thức (schemas). Khi một lược đồ được tự động hóa qua luyện tập, nó được xử lý như một đơn vị duy nhất trong WM.
- **Khung phân tích Tải nhận thức Đương đại (Sweller et al., 2011, 2019):**
  1. *Tải nội tại (Intrinsic Cognitive Load):* Gánh nặng nhận thức phát sinh từ độ phức tạp và mức độ tương tác giữa các phần tử cố hữu của tài liệu học tập (Element Interactivity), phụ thuộc vào mức độ hiểu biết nền tảng của người học. Tải này không thể giảm bớt mà chỉ có thể quản lý thông qua phân đoạn (segmentation) và sắp xếp trình tự hợp lý.
  2. *Tải ngoại lai (Extraneous Cognitive Load):* Gánh nặng nhận thức lãng phí do cách trình bày tài liệu hoặc giao diện không tối ưu (như tra cứu nhảy trang, bố cục phân tán chú ý, văn bản thừa thãi). Mục tiêu thiết kế là **tối thiểu hóa tối đa tải ngoại lai**.
  3. *Xử lý hữu ích (Germane Processing / Cognitive Resources Allocation):* Trong góc nhìn CLT hiện đại, germane không phải là một thành phần tải độc lập thứ ba cộng vào tổng tải. Thay vào đó, nó đại diện cho các nguồn lực nhận thức của bộ nhớ làm việc được người học thực sự phân bổ để tiếp nhận tải nội tại nhằm xây dựng và tự động hóa lược đồ.
- **Kiểm soát các hiệu ứng nhận thức:**
  - *Split-Attention Effect (Hiệu ứng phân tán chú ý):* Không tách rời sơ đồ phần cứng với lời giải thích văn bản sang hai trang giấy hoặc hai màn hình cuộn xa nhau. Mọi sơ đồ kỹ thuật phải gắn nhãn trực tiếp (integrated callouts) ngay trên vị trí vật lý của linh kiện/bước chuyển.
  - *Redundancy Effect (Hiệu ứng dư thừa):* Không đọc lại y nguyên từng từ của sơ đồ; văn bản đi kèm chỉ tập trung vào cơ chế nhân quả.

### 1.2. Luyện tập Thu hồi & Hiệu ứng Kiểm tra (Retrieval Practice & Testing Effect)
- **Nghiên cứu nền tảng (Roediger & Karpicke, 2006; Dunlosky et al., 2013):**
  Hành động tự kiểm tra kín sách (Closed-book Retrieval) củng cố các đường dẫn trích xuất thông tin trong trí nhớ dài hạn, tạo ra độ bền trí nhớ vượt trội so với việc đọc lại nhiều lần (Passive Re-reading). Việc đọc lại thường tạo ra cảm giác trôi chảy giả tạo (*Illusion of Competence*), khiến người học ngộ nhận rằng mình đã nắm vững nhưng lại thất bại khi giải bài tập mới.

### 1.3. Luyện tập Phân tán (Distributed Practice & Spacing Effect)
- **Nghiên cứu nền tảng (Cepeda et al., 2006, 2008):**
  Phân chia các lượt học cách quãng theo thời gian mang lại hiệu quả ghi nhớ lâu dài tốt hơn nhiều so với việc dồn ép trong một thời gian ngắn (*Cramming*). Khoảng cách tối ưu giữa các lần ôn tập phụ thuộc vào khoảng thời gian muốn duy trì trí nhớ mục tiêu, không tuân theo các chu kỳ cứng nhắc cố định.

### 1.4. Hiệu ứng Bài tập Mẫu & Phai mờ Dần Dần (Worked-Example Effect & Fading)
- **Nghiên cứu nền tảng (Sweller, 1988; Renkl, 2014; Atkinson et al., 2000):**
  Đối với người học mới (novice), việc nghiên cứu các bài tập mẫu có lời giải chi tiết (Worked Examples) hiệu quả hơn việc tự mày mò giải bài toán mở, do giảm thiểu tải nhận thức ngoại lai. Khi năng lực tăng lên, giàn giáo cần được làm mờ dần (Fading) để tránh hiện tượng đảo ngược chuyên gia (*Expertise Reversal Effect*).

### 1.5. Hiệu ứng Phát sinh & Phân biệt Dự đoán vs Siêu sửa sai
- **Generation Effect (Slamecka & Graf, 1978; Kornell, Hays & Bjork, 2009):** Tự tạo ra câu trả lời hoặc đưa ra dự đoán trước khi xem đáp án kích hoạt mạng lưới ngữ nghĩa và hướng sự chú ý của người học vào thông tin phản hồi.
- **Hypercorrection Effect (Butterfield & Metcalfe, 2001, 2006; Metcalfe, 2017):** Hiện tượng người học sửa chữa sai lầm nhanh và sâu sắc hơn khi lỗi sai đó được cam kết với **mức độ tự tin cao** (*High-confidence error*), thay vì các lỗi sai do đoán mò. Điều này đòi hỏi thiết kế phải cho phép người học bộc lộ quan niệm sai lầm trước khi nhận phản hồi.

### 1.6. Khung Nhận thức ICAP & Tự giải thích (Chi & Wylie, 2014)
- Khung ICAP phân loại các hành vi học tập thành bốn mức độ: Thụ động (Passive), Chủ động (Active), Kiến tạo (Constructive), và Tương tác (Interactive). Khung lý thuyết dự báo xu hướng kết quả học tập $\text{Interactive} > \text{Constructive} > \text{Active} > \text{Passive}$ trong các điều kiện nhiệm vụ cụ thể, có tính đến ranh giới nhận thức của người mới bắt đầu (vốn cần giàn giáo bài mẫu trước khi tự kiến tạo).

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
| **Cognitive Load Minimal** | Sweller (1988, 2011); Sweller et al. (2019) | Rất cao | Giảm tải ngoại lai không có nghĩa là lược bỏ bài tập khó mang tính thử thách đáng giá (*Desirable difficulty*). | Áp dụng Quy tắc Tối giản Sư phạm: loại bỏ đồ thị trang trí, loại bỏ hình ảnh thừa; giao diện tập trung 1 tác vụ/khung nhìn. |

---

## 3. NGUYÊN TẮC HỌC TẬP CỐT LÕI & QUY TẮC TỐI GIẢN SƯ PHẠM

### 3.1. Nguyên tắc Học tập Cốt lõi (Core Learning Principle)
Hệ thống vận hành theo chu trình 6 giai đoạn thích ứng:

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

Giao diện Web Companion hỗ trợ 3 chế độ độc lập, phù hợp với các giai đoạn học tập khác nhau:

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
> **QUY TẮC BẤT BIẾN:**
> Hệ thống phân tách rạch ròi giữa **Bằng chứng Năng lực (Mastery Evidence)** và **Đánh giá Trải nghiệm Ôn tập (Review Rating)**. Người học không thể tự bấm nút đánh giá lượt ôn để phong tặng cấp độ M3.

### 6.1. Bốn Cấp độ Năng lực (Mastery Evidence: M0 – M3)
Cấp độ năng lực phản ánh mức độ độc lập và chuyển giao kiến thức được chứng minh qua hành vi:

| Cấp độ | Tên gọi | Định nghĩa Nhận thức | Bằng chứng Hành vi Bắt buộc (Evidence Requirement) |
| :---: | :--- | :--- | :--- |
| **M0** | `NOT_RECALLED` | Chưa học hoặc Không thể thu hồi. | Trả lời sai hoặc bỏ trắng bài kiểm tra kín sách; chưa từng làm bài tập. |
| **M1** | `FAMILIAR` | Nhận diện được khi có mồi gợi ý (*Cue-dependent*). | Trả lời đúng sau khi xem gợi ý (*Hint*); hoặc điền đúng bài tập giàn giáo Level B. |
| **M2** | `CAN_EXPLAIN` | Tự giải thích được bản chất nhân quả (WHY & HOW). | Trả lời đúng câu hỏi `RecallCheckpoint` kín sách, đối soát đạt $\ge 80\%$ từ khóa rubric bắt buộc (Ghi nhận dưới dạng `SELF_ASSESSED_M2` hoặc `VERIFIED_M2`). |
| **M3** | `CAN_TRANSFER` | Độc lập chuyển giao năng lực sang bài toán thi cử mới lạ. | **CHỈ ĐƯỢC XÁC LẬP KHI:** Giải thành công bài toán `TransferProblem` (Level C) với tham số biên mới mà không dùng bất kỳ gợi ý nào. **`RecallCheckpoint` không thể trực tiếp gán mức M3.** |

### 6.2. Thang Đánh giá Lượt Ôn tập (Review Rating Scale)
Thang đánh giá 4 mức độ dùng để cung cấp tham số cho thuật toán lập lịch ôn tập, hoàn toàn độc lập với danh hiệu Mastery:
- **`AGAIN` (Quên / Thất bại thu hồi):** Không nhớ hoặc giải sai cơ bản $\implies$ Tái lập chu kỳ ôn tập ngắn hạn.
- **`HARD` (Thu hồi thành công nhưng khó khăn):** Nhớ được câu trả lời đúng nhưng mất nhiều thời gian, phải nỗ lực tư duy cao hoặc ngập ngừng $\implies$ Tăng khoảng cách chu kỳ một cách thận trọng; **KHÔNG coi là thất bại và KHÔNG đặt lại chu kỳ về 1 ngày.**
- **`GOOD` (Thu hồi thành công chuẩn mực):** Thu hồi chính xác, giải thích tự tin với nỗ lực nhận thức vừa phải $\implies$ Giãn khoảng cách theo hệ số tiêu chuẩn.
- **`EASY` (Thu hồi thành công xuất sắc):** Kiến thức đã đạt mức tự động hóa cao, giải quyết tức thì không do dự $\implies$ Tăng mạnh khoảng cách chu kỳ tới.

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
    "last_reviewed": 1725372000000,
    "lapses": 0
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

## 7. ĐÁNH GIÁ THUẬT TOÁN LẬP LỊCH ÔN TẬP & QUYẾT ĐỊNH DỰ ÁN

### 7.1. Đánh giá Khách quan 3 Lớp Thuật toán Lập lịch Ôn tập

Để đưa ra quyết định kiến trúc đúng đắn, chúng tôi so sánh 3 phương án dựa trên 7 tiêu chuẩn kỹ thuật (đánh giá ghi nhận tại thời điểm 2026-09):

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   SO SÁNH CÁC PHƯƠNG ÁN THUẬT TOÁN LẬP LỊCH                      │
│                                                                                  │
│   [ Phương án A: Hộp Leitner Xác định Đơn giản ]                                 │
│   - Cấu trúc: 3–5 ngăn thời gian cố định.                                        │
│   - Ưu điểm: Mã nguồn cực ngắn (~30 dòng JS), trực quan, dễ hiểu.                │
│   - Nhược điểm: Khoảng cách giãn cách bị bó cứng, không phản ánh độ khó mục học. │
│                                                                                  │
│   [ Phương án B: SM-2 Project Heuristic (Biến thể Xác định) ]                    │
│   - Cấu trúc: Nhân khoảng cách với Hệ số Dễ (EF) thích ứng.                      │
│   - Ưu điểm: Đơn giản (~80 dòng JS), tính toán xác định tức thì, không phụ thuộc.│
│   - Nhược điểm: Mô hình kinh nghiệm (heuristic), không tối ưu tham số tự động.   │
│                                                                                  │
│   [ Phương án C: FSRS Hiện đại (Free Spaced Repetition Scheduler) ]              │
│   - Cấu trúc: Mô hình 3 thành phần S (Stability), D (Difficulty), R (Retrievability).│
│     * Lịch sử phiên bản tham số: FSRS v4/v4.5 (17 tham số), FSRS-5 (19 tham số),  │
│       FSRS-6 (21 tham số). Các biến thể nghiên cứu/benchmark (như FSRS-7 với       │
│       35 tham số) được thử nghiệm đo lường hiệu năng nhưng chưa là mặc định Anki.│
│     * Phân định rõ ràng:                                                         │
│       - Scheduling Runtime: Đánh giá giải tích thuần túy bằng công thức đóng trong│
│         vài micro-giây, dùng bộ tham số mặc định chuẩn, KHÔNG cần gradient       │
│         descent trong phiên học, hoạt động ngay từ ngày đầu (Cold start).        │
│       - Parameter Optimization: Quá trình tùy chọn huấn luyện cá nhân hóa tham   │
│         số bằng gradient descent qua log ôn tập lớn (thực hiện offline).         │
│   - Ưu điểm: Mô hình khoa học hiện đại, độ chính xác dự báo thu hồi rất cao.     │
│   - Nhược điểm: Cần nhiều phương trình phi tuyến, bảo trì phức tạp hơn cho web   │
│     tĩnh học thuật đơn giản.                                                     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| Tiêu chuẩn Đánh giá | Phương án A: Leitner Đơn giản | Phương án B: SM-2 Project Heuristic | Phương án C: FSRS Hiện đại (2026-09) |
| :--- | :--- | :--- | :--- |
| **Tính Đơn giản (Simplicity)** | Cực cao | Rất cao | Trung bình (Nhiều phương trình toán phi tuyến) |
| **Độ chuẩn xác Khoa học (Correctness)** | Trung bình | Tốt (Mô hình kinh nghiệm 30 năm) | Rất cao (Mô hình trí nhớ DSR hiện đại) |
| **Hoạt động Ngoại tuyến (Offline Use)** | Hoàn hảo ($100\%$) | Hoàn hảo ($100\%$) | Hoàn hảo ($100\%$ khi dùng tham số mặc định) |
| **Khả năng Bảo trì (Maintainability)** | Cực cao | Rất cao | Trung bình (Cần đồng bộ khi nâng cấp phiên bản) |
| **Hành vi Khởi đầu Lạnh (Cold Start)** | Hoàn hảo | Hoàn hảo với $\text{EF}=2.5$ | Tốt với tham số mặc định chuẩn hóa |
| **Hiệu quả Ôn tập (Review Efficiency)** | Trung bình | Rất tốt | Cao nhất |
| **Tính Kiểm thử được (Testability)** | Cực dễ | Cực kỳ xác định và dễ viết unit test | Cần bộ test kiểm thử số thực phức tạp hơn |

### 7.2. Quyết định Kiến trúc: Lựa chọn Phương án B (SM-2 Project Heuristic)
> [!NOTE]
> **QUYẾT ĐỊNH THIẾT KẾ:**
> Dự án quyết định áp dụng **SM-2 Project Heuristic** cho nền tảng Web Companion IT007:
> 1. **Lý do lựa chọn:** Không phải vì FSRS runtime quá nặng (FSRS runtime hoàn toàn có thể chạy client-side với tham số mặc định), mà vì SM-2 Heuristic mang lại **tính minh bạch thuật toán cao nhất** cho sinh viên ngành Công nghệ Thông tin, mã nguồn tối giản tuyệt đối, hoàn toàn xác định ($100\%$ deterministic), dễ bảo trì và dễ viết bài kiểm thử hồi quy.
> 2. **Định danh trung thực:** Chúng tôi gọi đây là **Project Heuristic (Quy tắc Thực nghiệm Dự án)**, không tuyên bố là mô hình toán tối ưu tuyệt đối.

#### Đặc tả Thuật toán Lập lịch Dự án (Project Heuristic Specification):
1. **Khởi tạo (State Initialization):**
   Mỗi thẻ mới bắt đầu với: $\text{Reps} = 0, \text{EF} = 2.5, I = 0, \text{Lapses} = 0$.
2. **Quy tắc Xử lý 4 Mức Đánh giá:**

   - **Trường hợp 1: `AGAIN` (Quên hoàn toàn / Thất bại thu hồi):**
     $$\text{Reps}' = 0, \quad I' = 1 \text{ ngày}, \quad \text{EF}' = \max(1.3, \; \text{EF} - 0.20), \quad \text{Lapses}' = \text{Lapses} + 1$$
     *(Thẻ bị đẩy về hàng đợi ôn tập của ngày hôm sau để tái thiết lập liên kết).*

   - **Trường hợp 2: `HARD` (Thu hồi thành công với nỗ lực cao / Ngập ngừng):**
     $$\text{Reps}' = \text{Reps} + 1$$
     $$I' = \begin{cases} 
       1 \text{ ngày} & \text{khi } \text{Reps}' \le 1 \\ 
       \max(I + 1, \; \text{round}(I \times 1.2)) & \text{khi } \text{Reps}' \ge 2 
     \end{cases}$$
     $$\text{EF}' = \max(1.3, \; \text{EF} - 0.15)$$
     *(LƯU Ý: Đây là lần thu hồi thành công, chu kỳ được nới rộng một cách thận trọng, KHÔNG đặt lại $\text{Reps}$ về 0).*

   - **Trường hợp 3: `GOOD` (Thu hồi thành công chuẩn mực):**
     $$\text{Reps}' = \text{Reps} + 1$$
     $$I' = \begin{cases} 
       1 \text{ ngày} & \text{khi } \text{Reps}' = 1 \\ 
       3 \text{ ngày} & \text{khi } \text{Reps}' = 2 \\ 
       \text{round}(I \times \text{EF}) & \text{khi } \text{Reps}' \ge 3 
     \end{cases}$$
     $$\text{EF}' = \text{EF}$$

   - **Trường hợp 4: `EASY` (Thu hồi xuất sắc / Nhanh chóng):**
     $$\text{Reps}' = \text{Reps} + 1$$
     $$I' = \begin{cases} 
       2 \text{ ngày} & \text{khi } \text{Reps}' = 1 \\ 
       4 \text{ ngày} & \text{khi } \text{Reps}' = 2 \\ 
       \text{round}(I \times \text{EF} \times 1.3) & \text{khi } \text{Reps}' \ge 3 
     \end{cases}$$
     $$\text{EF}' = \min(2.8, \; \text{EF} + 0.15)$$

3. **Cập nhật Ngày đến hạn (Due Date):**
   $$\text{DueDate}' = \text{Hôm nay} + (I' \times 86400000 \text{ ms})$$

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
> **HỒ SƠ BÀN GIAO KỸ THUẬT: ENG-LEARN-002 — MAJOR — IMPLEMENTATION HANDOFF**
> - **Mô tả lỗi:** Trong mã nguồn `scripts/build_web.py` hiện tại, hàm `render_callout` tạo ra các thẻ nội dung ẩn `.card-hint`, `.card-keypoints`, `.card-answer` với CSS ẩn (`display: none`). Tệp JavaScript `src/web/assets/js/app.js` được lập trình để lắng nghe sự kiện bấm trên các nút `.btn-hint`, `.btn-keypoints`, `.btn-answer`. Tuy nhiên, trình tạo mã `build_web.py` **hoàn toàn chưa phát sinh các nút bấm này** vào cây DOM HTML.
> - **Hệ quả:** Người học trên web không có cách nào bấm để mở gợi ý hoặc lời giải của thẻ StudyCard; cơ chế tiết lộ tiệm tiến bị tê liệt một phần.
> - **Kế hoạch xử lý:** Đã ghi nhận vào hồ sơ bàn giao triển khai kỹ thuật cho Terra. **Không sửa đổi mã nguồn web trong lượt thiết kế của Luna.**

---

## 10. THƯ MỤC THAM KHẢO RÚT GỌN (COMPACT BIBLIOGRAPHY)

### 10.1. Nghiên cứu Khoa học Đã qua Bình duyệt (Peer-Reviewed Research)
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
15. **Sweller, J., van Merriënboer, J. J. G., & Paas, F.** (2019). Cognitive architecture and instructional design: 20 years later. *Educational Psychology Review*, 31(2), 261–292.
16. **Ye, J., Su, J., & Cao, Y.** (2022). A stochastic shortest path algorithm for optimizing spaced repetition scheduling. In *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '22)*, 2281–2290. https://doi.org/10.1145/3534678.3539081 *(Nghiên cứu nền tảng về mô hình tối ưu hóa không gian trạng thái DHP/SSP-MMC cho lập lịch giãn cách).*

### 10.2. Tài liệu Kỹ thuật Triển khai Mã nguồn Mở (Technical Implementation Documentation — Non-Peer-Reviewed)
17. **Open-Spaced-Repetition.** (2024–2026). *The Algorithm of FSRS*. Tài liệu kỹ thuật mã nguồn mở, GitHub: `open-spaced-repetition/fsrs4anki`.
18. **Anki Development Team.** (2024–2026). *FSRS (Free Spaced Repetition Scheduler)*. Anki Manual. https://docs.ankiweb.net/deck-options.html#fsrs

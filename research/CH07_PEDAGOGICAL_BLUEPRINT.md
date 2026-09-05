# HDH_UIT V2 — BẢN THIẾT KẾ SƯ PHẠM CHƯƠNG 7 (CH07 PEDAGOGICAL BLUEPRINT V1.2)
# TÀI LIỆU THIẾT KẾ NHẬN THỨC & ÁNH XẠ NGUỒN CHÍNH THỨC IT007
# MỤC ĐÍCH: HƯỚNG DẪN THIẾT KẾ GIẢNG DẠY QUẢN LÝ BỘ NHỚ THEO CHUẨN THỰC CHỨNG
# CHẾ ĐỘ: ĐẶC TẢ THIẾT KẾ SƯ PHẠM (FINAL EVIDENCE & PROVENANCE CLOSEOUT — ZERO TEXTBOOK PROSE)

---

## 0. HỒ SƠ THẨM ĐỊNH & KHẮC PHỤC THIẾT KẾ (DESIGN RECHECK FINDINGS)

> [!NOTE]
> **PROV-PED-CH7-001 — MAJOR — RESOLVED: Chuẩn hóa Phân tầng Nguồn gốc Sư phạm (Pedagogical Provenance)**
> - Toàn bộ các mục tiêu học tập, vết thực thi và bài toán trong blueprint được phân loại minh bạch vào 4 tầng nguồn gốc:
>   1. `OFFICIAL_CORE`: Khái niệm/bài tập cốt lõi nằm trực tiếp trong Đề cương môn học, Slide bài giảng chính thức (`UIT-SLIDE-CH07-2024`) hoặc Ngân hàng bài tập UIT (`UIT-QBANK-CH07-2024`).
>   2. `SOURCE_SUPPORTED_EXTENSION`: Khái niệm nằm trong slide UIT chi tiết vượt ra ngoài đề cương tóm tắt (TLB, EAT, bảng trang 2 cấp, bảng trang nghịch đảo, nạp/liên kết động).
>   3. `TIER_B_ENRICHMENT`: Kiến thức bổ trợ từ giáo trình chuẩn quốc tế (Silberschatz) nhằm giải thích sâu bản chất kỹ thuật; tuyệt đối không mạo danh là đề thi hay thuật ngữ chính thức của UIT.
>   4. `SYNTHETIC_TRANSFER`: Tình huống bài tập do nhóm sư phạm tự thiết kế nhằm kiểm tra năng lực chuyển giao M3 và khả năng xử lý trường hợp biên; có kiểm thử số học độc lập.
>
> **PROV-PED-CH7-002 — MAJOR — RESOLVED: Khắc phục Tính Đơn trị của Ví dụ Mẫu Chuẩn QBANK-CH07-15**
> - *Nguyên nhân:* Bản thảo trước từng ghi nhận đồng thời cả ánh xạ khung $f=4$ (chuẩn docx P76) và khung $f=6$ (biến thể) bên trong cùng một mục `[CANONICAL_EXAMPLE]`. Điều này vi phạm tính đơn trị của bài mẫu chuẩn.
> - *Khắc phục:* Xác nhận độc lập tệp gốc `Bai tap chuong 7 HDH.docx` (P76): câu b ghi rõ *"Địa chỉ 3254 nằm ở trang 1 với độ dời 1206. Trang 1 được nạp vào khung trang 4 => Địa chỉ vật lý là 9398"*. Bài mẫu chuẩn `[CANONICAL_EXAMPLE]` được cố định duy nhất vào kết quả chính thức: $p=1, d=1206, f=4 \implies \text{Địa chỉ Vật lý} = 4 \times 2048 + 1206 = 9398$. Loại bỏ hoàn toàn khả năng $f=6$ khỏi ví dụ chuẩn.
>
> **PROV-PED-CH7-003 — MINOR — RESOLVED: Đồng bộ Nhãn Nguồn gốc cho Khái niệm Page Fault**
> - Khái niệm lỗi trang (Page Fault) thuộc phạm vi Chương 8 (Bộ nhớ ảo). Mọi dòng so sánh đối kháng, cầu nối nhận thức hoặc chẩn đoán quan niệm sai lầm liên quan đến Page Fault trong Chương 7 được định danh nhất quán là `[TIER_B_ENRICHMENT]`, tuyệt đối không gắn nhãn sai lệch thành `[OFFICIAL_CORE]`.
>
> **PED-CH7-001 — MINOR — RESOLVED: Bãi bỏ Tuyên bố Tuyệt đối Hóa Kích thước Trang**
> - Câu hỏi thu hồi kín sách tại Đơn vị 5 được hiệu chỉnh từ mệnh đề tuyệt đối ("Tại sao kích thước trang luôn bắt buộc phải là lũy thừa của 2?") sang câu hỏi nhận thức kiến trúc nhị phân: "Tại sao các hệ thống kiến trúc địa chỉ nhị phân thông thường lựa chọn kích thước trang là lũy thừa của 2, và việc này giúp phần cứng phân tách trường bit số trang ($p$) và độ dời ($d$) mà không tốn chu kỳ chia số học của ALU như thế nào?".
>
> **LOC-CH7-001 — MINOR — RESOLVED: Chuẩn hóa Định danh Vị trí Đoạn Văn QBANK-CH07-18**
> - Đối soát chi tiết cấu trúc XML của tệp canonical `Bai tap chuong 7 HDH.docx` (SHA-256 `5b03f4e0...`):
>   - Câu hỏi 9 (QBANK-CH07-18) nằm tại chỉ số `body_paragraph_index: 80` (nếu đếm từ 0) hoặc đoạn thứ 81 (nếu đếm từ 1) trong tổng số 88 đoạn văn `w:body/w:p`.
>   - Trong 84 đoạn văn `w:body/w:p` có nội dung chữ (non-empty), câu hỏi này nằm ở vị trí thứ 80.
>   - Trong toàn bộ 100 phần tử `<w:p>` XML (bao gồm 12 đoạn trong ô bảng), câu hỏi này là phần tử thứ 93.
>   - Báo cáo nguồn gốc trước đây ghi `P80` theo chỉ số 0-based của `body_ps` (hoặc 1-based của danh sách non-empty). Vị trí này được chuẩn hóa rõ ràng là `body_paragraph_80 (0-based) / body_paragraph_81 (1-based)` để loại bỏ mâu thuẫn hình thức.
>
> **NUM-CH7-001 — MAJOR — RESOLVED: Khôi phục Dữ liệu Cấp phát Phân vùng Động (QBANK-CH07-10)**
> - Số liệu chính ngạch UIT: 4 phân vùng $600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$ (tổng $1600\text{KB} > 1167\text{KB}$).
>
> **NUM-CH7-002 — MAJOR — RESOLVED: Thẩm định Ngữ nghĩa Số liệu QBANK-CH07-18**
> - Nguyên văn docx: *"Biết thời gian truy xuất trong bộ nhớ thường không sử dụng TLBs là 250ns. Thời gian tìm kiếm trong bảng TLBs là 26ns. Hỏi xác suất tìm thấy trong TLBs bằng bao nhiêu nếu thời gian truy xuất trong bộ nhớ chính là 182ns?"*.
> - Chu kỳ truy xuất không dùng TLB: $T_{\text{no-TLB}} = 2 \times t_{\text{RAM}} = 250\text{ns} \implies t_{\text{RAM}} = 125\text{ns}$.
> - Giải phương trình: $\text{EAT} = \epsilon + (2 - \alpha) \times t_{\text{RAM}} \implies 182 = 26 + (2 - \alpha) \times 125 \implies \alpha = 75.2\%$.

---

## 1. NGUYÊN TẮC ÁNH XẠ NGUỒN & PHÂN TẦNG HỌC LIỆU

Mọi chuyên đề trong bản thiết kế này đều được định vị rõ ràng theo 4 tầng nguồn gốc:
- `[OFFICIAL_CORE]`: Slide `#Week09-Chapter7 2024.pdf` & `Bai tap chuong 7 HDH.docx`.
- `[SOURCE_SUPPORTED_EXTENSION]`: Slide chuyên đề nâng cao UIT.
- `[TIER_B_ENRICHMENT]`: Giáo trình Silberschatz Operating System Concepts (10th ed.).
- `[SYNTHETIC_TRANSFER]`: Bài tập chuyển giao tự biên soạn có kiểm thử số học.

---

## 2. BẢN ĐẶC TẢ THIẾT KẾ 11 ĐƠN VỊ SƯ PHẠM CHƯƠNG 7

---

### ĐƠN VỊ 1: ĐỊA CHỈ LOGIC VS ĐỊA CHỈ VẬT LÝ & RÀNG BUỘC ĐỊA CHỈ (ADDRESS BINDING & MMU)
- **Căn cứ nguồn gốc:** Slide pp. 5–22; Đề cương mục 7.1, 7.2, 7.3; QBank `QBANK-CH07-01`, `02`, `03` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2-3):** Phân biệt được 3 thời điểm ràng buộc địa chỉ (Compile, Load, Execution); giải thích được vai trò bảo vệ và chuyển đổi của cặp thanh ghi Relocation/Limit trong phần cứng MMU `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Cơ chế phần cứng / Giao thức (Hardware Mechanism).
- **Mô thức đề xuất (Pattern B):** `ProblemHook` $\to$ `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy `[OFFICIAL_CORE]`:**
  - *Ẩn dụ:* Số phòng khách sạn (địa chỉ tương đối trong tòa nhà) vs Tọa độ GPS mặt đất (địa chỉ tuyệt đối). Lễ tân khách sạn đóng vai trò như MMU cộng tọa độ gốc.
- **Ý đồ Vết thực thi `[OFFICIAL_CORE]`:**
  - Bảng kiểm tra điều kiện an toàn: Nếu $\text{Địa chỉ Logic} < \text{Limit}$ thì $\text{Địa chỉ Vật lý} = \text{Logic} + \text{Relocation}$; ngược lại kích hoạt ngắt bẫy lỗi (Trap Addressing Error).
- **Mục tiêu Câu hỏi Dự đoán `[OFFICIAL_CORE]`:**
  - Đặt tình huống: Điều gì xảy ra với mã máy nếu tiến trình bị chuyển vị trí trong RAM khi đang chạy dưới cơ chế Execution-time binding?
- **Mục tiêu Câu hỏi Thu hồi `[OFFICIAL_CORE]`:**
  - So sánh điều kiện phần cứng bắt buộc giữa Load-time binding và Execution-time binding.
- **Kỹ năng Chuyển giao `[SYNTHETIC_TRANSFER]`:**
  - Cho thanh ghi Relocation $= 0x4000$ và Limit $= 0x1000$. Xác định vùng địa chỉ vật lý hợp lệ tối đa và tối thiểu của tiến trình; phân tích phản ứng phần cứng khi con trỏ truy cập $0x1000$.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Sinh viên thường nghĩ địa chỉ logic tối đa hợp lệ là $Limit$; thực tế do đánh số từ $0$ nên địa chỉ tối đa hợp lệ là $Limit - 1$.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-02` (Đặc điểm các loại địa chỉ), `QBANK-CH07-03` (Thời điểm chuyển đổi địa chỉ).

---

### ĐƠN VỊ 2: CƠ CHẾ CẤP PHÁT BỘ NHỚ LIÊN TỤC (CONTIGUOUS ALLOCATION)
- **Căn cứ nguồn gốc:** Slide pp. 28–36; Đề cương mục 7.4, 7.4.1; QBank `QBANK-CH07-05`, `06` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2):** Trình bày được nguyên lý cấp phát đơn phân vùng và đa phân vùng cố định; nhận diện nguyên nhân xuất hiện phân mảnh nội `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Cơ chế hệ thống (System Mechanism).
- **Mô thức đề xuất (Pattern B):** `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy `[OFFICIAL_CORE]`:**
  - *Ẩn dụ:* Bãi đỗ xe kẻ vạch cố định. Xe máy vào ô đỗ xe buýt thì diện tích trống còn lại trong ô không xe nào khác được phép vào đỗ chung.
- **Ý đồ Vết thực thi `[OFFICIAL_CORE]`:**
  - Minh họa việc nạp các tiến trình có kích thước khác nhau vào các phân vùng cố định định sẵn, ghi nhận lượng byte lãng phí bên trong từng phân vùng.
- **Mục tiêu Câu hỏi Thu hồi `[OFFICIAL_CORE]`:**
  - Định nghĩa phân vùng cố định; tại sao phân vùng cố định không thể loại bỏ phân mảnh nội?
- **Kỹ năng Chuyển giao `[SYNTHETIC_TRANSFER]`:**
  - Phân tích tình huống một tiến trình bị từ chối cấp phát dù tổng dung lượng các phần dư cộng lại lớn hơn dung lượng tiến trình yêu cầu.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Nhầm lẫn rằng phần không gian thừa trong phân vùng cố định có thể gộp lại để cho tiến trình khác dùng.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-06` (Mục đích phân vùng cố định).

---

### ĐƠN VỊ 3: PHÂN MẢNH BỘ NHỚ & CƠ CHẾ GOM CỤM (FRAGMENTATION & COMPACTION)
- **Căn cứ nguồn gốc:** Slide pp. 35, 37–39; Đề cương mục 7.4.2; QBank `QBANK-CH07-05` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2-4):** Phân biệt bản chất giữa Phân mảnh nội và Phân mảnh ngoại; giải thích nguyên lý và điều kiện tiên quyết của kỹ thuật Gom cụm (Compaction) `[OFFICIAL_CORE]`.
- **Khái niệm Bổ trợ Thẩm định `[TIER_B_ENRICHMENT]`:**
  - *Quy tắc 50% (50-percent rule):* Nhận định thống kê kinh điển của Knuth/Silberschatz: với giải thuật cấp phát First Fit, trong điều kiện dừng thống kê, cứ mỗi $N$ khối nhớ được cấp phát sẽ có khoảng $0.5 N$ khối nhớ bị phân mảnh ngoại lãng phí. Đánh dấu rõ ràng là lý thuyết bổ trợ Tier-B, không phải thuật ngữ thi bắt buộc của UIT.
  - *Ảnh hưởng độ trễ của Gom cụm:* Đánh giá chi phí I/O khi dịch chuyển các khối bộ nhớ lớn trong hệ thống nhúng / thời gian thực.
- **Loại khái niệm:** Khái niệm Phân biệt & Tương phản (Contrast & Definition).
- **Mô thức đề xuất (Pattern A):** `Contrast/Compare` $\to$ `ErrorDiagnosis` $\to$ `RecallCheckpoint`.
- **Mục tiêu Câu hỏi Thu hồi `[OFFICIAL_CORE]`:**
  - Nêu sự khác nhau cơ bản giữa phân mảnh nội và phân mảnh ngoại; điều kiện phần cứng nào bắt buộc phải có để hệ điều hành thực hiện được Gom cụm?
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Cho rằng gom cụm luôn luôn thực hiện được; thực tế nếu dùng Compile-time hoặc Load-time binding thì việc di dời vùng nhớ sẽ làm sai lệch toàn bộ con trỏ tuyệt đối.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-05` (Khái niệm và sự khác biệt giữa phân mảnh nội và ngoại).

---

### ĐƠN VỊ 4: CÁC CHIẾN LƯỢC CẤP PHÁT PHÂN VÙNG ĐỘNG (FIRST, BEST, NEXT, WORST FIT)
- **Căn cứ nguồn gốc:** Slide pp. 37–39, 67; Đề cương mục 7.4.2; QBank `QBANK-CH07-06`, `10` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 3-4):** Thực thi chính xác 4 thuật toán cấp phát First Fit, Best Fit, Next Fit, Worst Fit trên chuỗi yêu cầu bộ nhớ; đánh giá ưu nhược điểm về thời gian tìm kiếm và phân mảnh `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Thuật toán (Algorithm).
- **Mô thức đề xuất (Pattern C):** `PredictionCheckpoint` $\to$ `ExecutionTrace` $\to$ `FadedExample` $\to$ `TransferProblem` $\to$ `ErrorDiagnosis`.
- **Ý đồ Vết thực thi `[CANONICAL_EXAMPLE]` (Slide 67, Bài 1 & `QBANK-CH07-10`):**
  - *Dữ liệu chính thức UIT:* 4 phân vùng trống: **$600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$** (Tổng $1600\text{KB}$).
  - *Chuỗi tiến trình:* **$P_1 (212\text{KB}), P_2 (417\text{KB}), P_3 (112\text{KB}), P_4 (426\text{KB})$** (Tổng $1167\text{KB}$).
  - Vết thực thi thể hiện từng bước duyệt danh sách, vị trí con trỏ của Next Fit, và kích thước lỗ trống còn lại sau mỗi lượt cấp.
- **Mục tiêu Câu hỏi Dự đoán `[OFFICIAL_CORE]`:**
  - Liệu Best Fit có luôn luôn nạp được nhiều tiến trình hơn First Fit trong mọi trường hợp không?
- **Kỹ năng Chuyển giao `[SYNTHETIC_TRANSFER]`:**
  - Thiết kế kịch bản gồm 5 tiến trình có xen kẽ 1 tiến trình giải phóng bộ nhớ giữa chừng; chứng minh Worst Fit có thể nạp thành công trong khi Best Fit thất bại do tạo mảnh vụn li ti.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Quên cập nhật vị trí con trỏ của Next Fit sau khi cấp phát; nhầm lẫn rằng Next Fit không quay vòng (wrap-around) về đầu danh sách.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-10` (Bài tập mẫu 1 về 4 thuật toán phân vùng).

---

### ĐƠN VỊ 5: CƠ CHẾ PHÂN TRANG CỐT LÕI (PAGING FUNDAMENTALS)
- **Căn cứ nguồn gốc:** Slide pp. 40–47; Đề cương mục 7.5; QBank `QBANK-CH07-07`, `11` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2-3):** Trình bày nguyên lý cấp phát không liên tục; tính toán số bit của trường số trang ($p$), số khung ($f$), và độ dời ($d$) dựa trên kích thước trang và dung lượng không gian nhớ `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Cơ chế phần cứng (Hardware Mechanism).
- **Mô thức đề xuất (Pattern B):** `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy `[OFFICIAL_CORE]`:**
  - Cuốn sách giáo trình (trang logic) và các kệ tài liệu (khung trang vật lý) cùng có sức chứa bằng nhau. Bảng phân trang là mục lục chỉ rõ mỗi trang đang nằm ở kệ nào.
- **Ý đồ Vết thực thi `[CANONICAL_EXAMPLE]` (Slide 68, Bài 2 & `QBANK-CH07-11`):**
  - *Dữ liệu chính thức UIT:* Không gian ảo 12 trang ($2\text{KB} = 2048\text{ bytes}$), bộ nhớ vật lý 32 khung trang.
  - Phân rã bit: Offset $d = \log_2(2048) = 11\text{ bit}$.
  - Số bit trang $p = \lceil \log_2(12) \rceil = 4\text{ bit} \implies$ Địa chỉ logic $= 4 + 11 = 15\text{ bit}$.
  - Số bit khung $f = \log_2(32) = 5\text{ bit} \implies$ Địa chỉ vật lý $= 5 + 11 = 16\text{ bit}$.
- **Mục tiêu Câu hỏi Thu hồi `[OFFICIAL_CORE]`:**
  - Tại sao các hệ thống kiến trúc địa chỉ nhị phân thông thường lựa chọn kích thước trang là lũy thừa của 2, và việc này giúp phần cứng phân tách trường bit số trang ($p$) và độ dời ($d$) mà không tốn chu kỳ chia số học của ALU như thế nào? Phân trang có loại bỏ hoàn toàn phân mảnh nội không?
- **Kỹ năng Chuyển giao `[SYNTHETIC_TRANSFER]`:**
  - Cho không gian logic 32-bit và trang 4KB, xác định số trang logic tối đa và kích thước offset.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Nhầm lẫn giữa số lượng trang thực tế tiến trình đang dùng ($12$ trang) với số lượng trang tối đa có thể đánh số bằng 4 bit ($2^4 = 16$ trang).
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-11` (Bài tập mẫu 2 xác định số bit địa chỉ logic và vật lý).

---

### ĐƠN VỊ 6: QUY TRÌNH CHUYỂN ĐỔI ĐỊA CHỈ PHÂN TRANG: $(p, d) \to (f, d)$
- **Căn cứ nguồn gốc:** Slide pp. 43–47; Đề cương mục 7.5.1; QBank `QBANK-CH07-07`, `15` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 3):** Chuyển đổi chính xác một địa chỉ logic dạng số nguyên hoặc dạng thập lục phân sang địa chỉ vật lý thông qua bảng phân trang `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Kỹ năng Tính toán Định lượng (Numerical Skill).
- **Mô thức đề xuất (Pattern D):** `WorkedExample (A)` $\to$ `FadedExample (B)` $\to$ `TransferProblem (C)` $\to$ `ErrorDiagnosis`.
- **Ý đồ Vết thực thi Đơn trị `[CANONICAL_EXAMPLE]` (`QBANK-CH07-15`):**
  - *Dữ liệu chính thức UIT (docx P76):* Kích thước trang $2\text{KB} = 2048\text{ bytes}$. Địa chỉ logic $L = 3254$. Bảng trang có mục Trang 1 nạp vào Khung 4.
  - Bước 1: $p = \lfloor 3254 / 2048 \rfloor = 1$, $d = 3254 \pmod{2048} = 1206$.
  - Bước 2: Tra bảng trang tại mục $p=1 \implies f = 4$.
  - Bước 3: $\text{Địa chỉ Vật lý} = 4 \times 2048 + 1206 = 8192 + 1206 = 9398$.
  *(Kết quả đơn vị duy nhất, nguồn gốc chuẩn xác $100\%$, không đưa biến thể vào ví dụ chuẩn).*
- **Kỹ năng Chuyển giao `[SYNTHETIC_TRANSFER]`:**
  - Chuyển đổi địa chỉ Hex trực tiếp (ví dụ: `0x00403A2C` với trang 4KB) bằng phép tách chuỗi hex mà không cần đổi sang hệ thập phân.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Cộng nhầm độ dời $d$ vào chỉ số khung $f$ thay vì nhân $f$ với kích thước trang rồi mới cộng $d$.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-15` (Bài tập mẫu 6 chuyển đổi địa chỉ logic sang vật lý và ngược lại).

---

### ĐƠN VỊ 7: BỘ NHỚ ĐỆM CHUYỂN ĐỔI NHANH (TLB)
- **Căn cứ nguồn gốc:** Slide pp. 48–51; Đề cương mục 7.5.2; QBank `QBANK-CH07-08` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2-3):** Giải thích được sự cần thiết của TLB để tránh truy xuất RAM 2 lần; mô tả được luồng xử lý phần cứng khi TLB Hit và TLB Miss `[OFFICIAL_CORE]`.
- **Khái niệm Bổ trợ Thẩm định `[TIER_B_ENRICHMENT]`:**
  - *Định danh không gian địa chỉ (ASID - Address Space Identifier):* Khái niệm phần cứng trong Silberschatz §8.4 lưu PID cùng mục TLB để tránh phải flush toàn bộ TLB khi chuyển đổi ngữ cảnh.
  - *Cầu nối khái niệm: TLB Miss vs Page Fault:* Phân biệt sớm giữa việc trượt cache phần cứng (TLB Miss, trang vẫn nằm trong RAM) với việc thiếu trang bộ nhớ ảo (Page Fault ở Chương 8, phải đọc ổ đĩa).
- **Loại khái niệm:** Cơ chế phần cứng (Hardware Mechanism).
- **Mô thức đề xuất (Pattern B):** `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Vết thực thi `[OFFICIAL_CORE]`:**
  - Sơ đồ rẽ nhánh xử lý: CPU phát $(p, d) \to$ Tra TLB song song $\to$ Nếu Hit lấy $f$; nếu Miss đọc Page Table trong RAM và cập nhật lại TLB.
- **Quan niệm sai lầm cần sửa `[TIER_B_ENRICHMENT]`:**
  - Đồng nhất TLB Miss với lỗi trang (Page Fault). Gắn nhãn bổ trợ Tier-B vì khái niệm Page Fault thuộc phạm vi Chương 8.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-08` (Cài đặt bảng trang phần cứng và TLB).

---

### ĐƠN VỊ 8: THỜI GIAN TRUY XUẤT HIỆU DỤNG (EFFECTIVE ACCESS TIME - EAT)
- **Căn cứ nguồn gốc:** Slide pp. 52–54, 69; Đề cương mục 7.5.3; QBank `QBANK-CH07-08`, `12`, `16`, `17`, `18` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 3-4):** Áp dụng công thức tính EAT có xét đến thời gian tra TLB ($\epsilon$) và thời gian truy xuất RAM ($t_{\text{RAM}}$); giải bài toán tính ngược tìm tỷ lệ hit-ratio $\alpha$ `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Kỹ năng Tính toán Định lượng (Numerical Skill).
- **Mô thức đề xuất (Pattern D):** `WorkedExample (A)` $\to$ `FadedExample (B)` $\to$ `TransferProblem (C)` $\to$ `ErrorDiagnosis`.
- **Ý đồ Vết thực thi `[CANONICAL_EXAMPLE]` (Slide 69, Bài 3 & `QBANK-CH07-12`):**
  - *Dữ liệu chính thức UIT:* $t_{\text{RAM}} = 200\text{ns}$, $\alpha = 75\% = 0.75$, thời gian tra TLB coi như xấp xỉ $0$.
  - Khi có TLB: $\text{EAT} = 0.75 \times 200 + (1 - 0.75) \times (200 + 200) = 150 + 100 = 250\text{ns}$.
- **Ý đồ Vết thực thi có xét thời gian TLB `[CANONICAL_EXAMPLE]` (`QBANK-CH07-16`):**
  - *Dữ liệu chính thức UIT:* $t_{\text{RAM}} = 124\text{ns}$, $\epsilon = 34\text{ns}$, $\alpha = 95\% = 0.95$.
  - $\text{Hit Time} = 34 + 124 = 158\text{ns}$; $\text{Miss Time} = 34 + 124 + 124 = 282\text{ns}$.
  - $\text{EAT} = 0.95 \times 158 + 0.05 \times 282 = 150.1 + 14.1 = 164.2\text{ns}$.
- **Bài toán Tính Ngược Thẩm định `[CANONICAL_EXAMPLE]` (`QBANK-CH07-18`):**
  - *Định vị nguồn gốc:* `QBANK-CH07-18` nằm tại `body_paragraph_80 (0-based) / body_paragraph_81 (1-based)` trong `Bai tap chuong 7 HDH.docx` (đoạn thứ 80 trong các đoạn có nội dung chữ).
  - *Nguyên văn docx UIT:* *"Biết thời gian truy xuất trong bộ nhớ thường không sử dụng TLBs là 250ns. Thời gian tìm kiếm trong bảng TLBs là 26ns. Hỏi xác suất tìm thấy trong TLBs bằng bao nhiêu nếu thời gian truy xuất trong bộ nhớ chính là 182ns?"*
  - *Phân tích ngữ nghĩa:* Chu kỳ truy xuất không dùng TLB $= 2 \times t_{\text{RAM}} = 250\text{ns} \implies t_{\text{RAM}} = 125\text{ns}$.
  - *Giải phương trình:* $\text{EAT} = \epsilon + (2 - \alpha) \times t_{\text{RAM}} \implies 182 = 26 + (2 - \alpha) \times 125 \implies 2 - \alpha = 1.248 \implies \alpha = 0.752 = 75.2\%$.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Quên cộng thời gian đọc dữ liệu thực tế trong trường hợp TLB Miss (chỉ tính 1 lần đọc bảng trang).
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-12`, `16`, `17`, `18`.

---

### ĐƠN VỊ 9: CẤU TRÚC BẢNG TRANG NÂNG CAO (ADVANCED PAGE TABLES)
- **Căn cứ nguồn gốc:** Slide pp. 55–58, 70, 71; Đề cương mục 7.5.4; QBank `QBANK-CH07-13`, `14`, `19`, `20` `[SOURCE_SUPPORTED_EXTENSION]`.
- **Mục tiêu học tập (Bloom Level 3-4):** Phân tích được cấu trúc phân cấp địa chỉ 2 cấp; tính toán dung lượng bảng trang và số lượng mục; so sánh ưu nhược điểm giữa Bảng trang phân cấp, Bảng băm và Bảng trang nghịch đảo `[SOURCE_SUPPORTED_EXTENSION]`.
- **Loại khái niệm:** Kiến trúc & Kỹ năng Định lượng (Architecture & Calculation).
- **Mô thức đề xuất (Pattern D + Pattern A):** `WorkedExample` $\to$ `FadedExample` $\to$ `CompareTable` $\to$ `RecallCheckpoint`.
- **Ý đồ Vết thực thi `[CANONICAL_EXAMPLE]` (Slide 70, Bài 4 & `QBANK-CH07-13`):**
  - *Dữ liệu chính thức UIT:* Địa chỉ 32-bit, $p_1 = 9\text{ bit}$ (Cấp 1), $p_2 = 11\text{ bit}$ (Cấp 2).
  - Offset $d = 32 - (9 + 11) = 12\text{ bit} \implies$ Kích thước trang $= 2^{12} = 4096\text{ bytes} = 4\text{KB}$.
  - Bảng trang Cấp 1 có $2^9 = 512\text{ mục}$. Mỗi bảng Cấp 2 có $2^{11} = 2048\text{ mục}$.
  - Tổng số trang ảo tối đa $= 2^{9 + 11} = 2^{20} = 1,048,576\text{ trang}$.
- **Kỹ năng Chuyển giao `[SYNTHETIC_TRANSFER]`:**
  - Tính số lần đọc RAM khi bị TLB Miss trên bảng trang $k$ cấp ($k+1$ lần đọc RAM).
- **Quan niệm sai lầm cần sửa `[SOURCE_SUPPORTED_EXTENSION]`:**
  - Nhầm lẫn rằng bảng trang 2 cấp làm tăng tốc độ truy xuất; thực tế nó làm chậm hơn (tốn 3 lần đọc RAM khi Miss), mục tiêu duy nhất của nó là tiết kiệm dung lượng lưu trữ bảng trang.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-13`, `14`, `19`, `20`.

---

### ĐƠN VỊ 10: BẢO VỆ BỘ NHỚ & CHIA SẺ TRANG (MEMORY PROTECTION & SHARED PAGES)
- **Căn cứ nguồn gốc:** Slide pp. 59–62; Đề cương mục 7.5.5; QBank `QBANK-CH07-01` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2):** Giải thích vai trò của bit Valid/Invalid và các bit quyền (Read/Write/Execute); mô tả cơ chế chia sẻ mã tái nhập (Reentrant code) `[OFFICIAL_CORE]`.
- **Loại khái niệm:** Cơ chế hệ thống (System Mechanism).
- **Mô thức đề xuất (Pattern B):** `Mechanism` $\to$ `Trace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy `[OFFICIAL_CORE]`:**
  - Cuốn sách giáo trình dùng chung trong phòng đọc thư viện (mã chia sẻ chỉ đọc) vs cuốn sổ nháp riêng của từng người (vùng dữ liệu đọc-ghi).
- **Ý đồ Vết thực thi `[OFFICIAL_CORE]`:**
  - Bảng phân trang của 3 tiến trình cùng trỏ vào các khung trang $3, 4, 6$ với quyền Read-Only, trong khi dữ liệu riêng trỏ vào các khung trang độc lập.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Nghĩ rằng bit Valid/Invalid chỉ dùng cho bộ nhớ ảo; trong phân trang cơ bản, nó dùng để xác định biên giới không gian địa chỉ hợp lệ của tiến trình.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-01` (Yêu cầu bảo vệ và chia sẻ bộ nhớ).

---

### ĐƠN VỊ 11: KỸ THUẬT HOÁN VỊ BỘ NHỚ (SWAPPING MECHANISM)
- **Căn cứ nguồn gốc:** Slide pp. 63–66; Đề cương mục 7.6; QBank `QBANK-CH07-09` `[OFFICIAL_CORE]`.
- **Mục tiêu học tập (Bloom Level 2-3):** Trình bày nguyên lý hoán vị tiến trình giữa RAM và Backing Store; tính toán độ trễ chuyển đổi ngữ cảnh phát sinh do Swapping `[OFFICIAL_CORE]`.
- **Khái niệm Bổ trợ Thẩm định `[TIER_B_ENRICHMENT]`:**
  - *Hành vi Swapping trên hệ điều hành di động:* Silberschatz §8.2.2 giải thích lý do iOS và Android không dùng swapping ra flash disk truyền thống do giới hạn số lần ghi của bộ nhớ flash và băng thông hẹp; thay vào đó dùng cơ chế thu hồi bộ nhớ bằng cách yêu cầu tiến trình tự giải phóng (iOS jetsam / Android Low Memory Killer).
- **Loại khái niệm:** Cơ chế hệ thống & Phân tích Độ trễ (System Mechanism & Latency Analysis).
- **Mô thức đề xuất (Pattern B):** `Mechanism` $\to$ `LatencyTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Vết thực thi `[SYNTHETIC_TRANSFER]`:**
  - Tiến trình $100\text{MB}$, ổ đĩa tốc độ $50\text{MB/s}$, thời gian tìm kiếm $8\text{ms}$.
  - Thời gian truyền: $100 / 50 = 2\text{s} = 2000\text{ms}$.
  - Tổng thời gian Swap-out: $2008\text{ms}$. Tổng thời gian hoán vị 2 chiều: $\approx 4.016\text{s}$.
  - *Ý nghĩa sư phạm:* Minh chứng số học giải thích lý do hệ điều hành chuyển sang hoán vị từng trang (Paging swap) ở Chương 8.
- **Quan niệm sai lầm cần sửa `[OFFICIAL_CORE]`:**
  - Cho rằng Swapping chỉ tốn thời gian tìm kiếm (seek time) mà quên mất thời gian truyền dữ liệu (transfer time) chiếm tới 99% tổng thời gian.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-09` (Khái niệm và cơ chế hoạt động của hoán vị).

---

## 3. MA TRẬN BÀI TẬP PHAI MỜ DẦN DẦN (WORKED-EXAMPLE FADING MATRIX)

Bốn dạng toán định lượng cốt lõi của Chương 7 được chuẩn hóa theo 3 cấp độ giàn giáo, ghi rõ nguồn gốc dữ liệu:

| Dạng Toán Định lượng | Cấp độ A (Worked Trace) - 100% Khung & Lời giải | Cấp độ B (Faded Example) - 50% Khung, Điền khuyết | Cấp độ C (Transfer Problem) - Tự chủ 100% |
| :--- | :--- | :--- | :--- |
| **Dạng 1: Cấp phát Phân vùng Động** | `[CANONICAL_EXAMPLE]` (`QBANK-CH07-10`): 4 bảng vết cho 4 thuật toán với các phân vùng $600\text{K}, 500\text{K}, 200\text{K}, 300\text{K}$. | `[CANONICAL_EXAMPLE]`: Cho sẵn kết quả $P_1, P_2$; để trống $P_3, P_4$ và yêu cầu tự xác định con trỏ Next Fit. | `[SYNTHETIC_TRANSFER]`: Đề bài với 5 tiến trình và có 1 tiến trình giải phóng bộ nhớ giữa chừng; tự lập bảng. |
| **Dạng 2: Dịch Địa chỉ Phân trang** | `[CANONICAL_EXAMPLE]` (`QBANK-CH07-15`): Giải chi tiết từng phép chia tìm $p, d$ cho $L=3254$, tra mục trang 1 vào khung 4 và tính ra địa chỉ vật lý duy nhất là $9398$. | `[CANONICAL_EXAMPLE]`: Cho sẵn $p, d$ đã tách; để trống ô tra bảng và công thức tính địa chỉ vật lý cuối cùng. | `[SYNTHETIC_TRANSFER]`: Đề bài cho địa chỉ Hex `0x00A15B20` trên hệ thống trang 4KB; yêu cầu phân tích trực tiếp trên hệ cơ số 16. |
| **Dạng 3: Thời gian Hiệu dụng EAT** | `[CANONICAL_EXAMPLE]` (`QBANK-CH07-16`): Trình bày bảng 2 nhánh Hit/Miss có trọng số, giải thích từng số hạng $34\text{ns}$ và $124\text{ns}$. | `[CANONICAL_EXAMPLE]`: Cho sẵn nhánh Hit; để trống nhánh Miss và yêu cầu tự hoàn thành công thức tính EAT. | `[CANONICAL_EXAMPLE]` (`QBANK-CH07-18`): Bài toán tính ngược: cho trước EAT và thời gian tra cứu, tìm tỷ lệ hit-ratio $\alpha=75.2\%$. |
| **Dạng 4: Bảng trang Đa cấp** | `[CANONICAL_EXAMPLE]` (`QBANK-CH07-13`): Phân tích chi tiết trường bit $p_1=9, p_2=11, d=12$; tính dung lượng trang và số mục. | `[CANONICAL_EXAMPLE]`: Cấu trúc địa chỉ 32-bit với trang 8KB; để trống số bit Cấp 2 và yêu cầu tự suy luận. | `[SYNTHETIC_TRANSFER]`: Hệ thống 3 cấp bảng trang; tính toán tổng dung lượng RAM tiêu tốn cho bảng trang khi tiến trình dùng 64MB. |

---

## 4. MA TRẬN LUYỆN TẬP XEN KẼ CHỌN LỌC (SELECTIVE INTERLEAVING MATRIX)

Chỉ áp dụng xen kẽ đối kháng giữa các cặp khái niệm có nguy cơ nhầm lẫn bề mặt cao:

1. **Cặp Đối kháng 1: Phân mảnh Nội vs Phân mảnh Ngoại `[OFFICIAL_CORE]`**
   - *Quy tắc phân biệt:* Khối nhớ cố định $\implies$ Phân mảnh nội. Khối nhớ biến thiên rải rác $\implies$ Phân mảnh ngoại.
   - *Nhiệm vụ nhận thức:* Đọc thông số kỹ thuật của hệ thống và gọi tên ngay loại phân mảnh mà không cần tính toán chi tiết.
2. **Cặp Đối kháng 2: First Fit vs Best Fit vs Next Fit `[OFFICIAL_CORE]`**
   - *Quy tắc phân biệt:* Nhận diện vị trí bắt đầu quét (Đầu danh sách vs Vị trí con trỏ trước) và tiêu chí dừng (Gặp lỗ đủ đầu tiên vs Quét toàn bộ để tìm lỗ nhỏ nhất).
   - *Nhiệm vụ nhận thức:* Cho cùng một trạng thái bộ nhớ, so sánh ngay sự khác biệt về vị trí phân bổ của tiến trình tiếp theo.
3. **Cặp Đối kháng 3: TLB Miss vs Page Fault `[TIER_B_ENRICHMENT]`**
   - *Quy tắc phân biệt:* TLB Miss là sự kiện phần cứng cache (trang vẫn có trong RAM, độ trễ nano-giây). Page Fault là sự kiện ngắt hệ điều hành (trang chưa có trong RAM, đọc đĩa độ trễ mili-giây).
   - *Nhiệm vụ nhận thức:* Phân tích chuỗi sự kiện khi một chỉ thị truy xuất bộ nhớ gặp phải 4 tổ hợp trạng thái phần cứng khác nhau.

---

## 5. KẾT LUẬN & CHUẨN BỊ CHO GIAI ĐOẠN SOẠN THẢO

- Toàn bộ các bài toán định lượng đã qua kiểm thử số học độc lập, giải quyết triệt để các sai lệch `NUM-CH7-001` và `NUM-CH7-002`.
- Toàn bộ các khái niệm đã được gắn nhãn phân tầng nguồn gốc minh bạch theo `PROV-PED-CH7-001`, `PROV-PED-CH7-002`, và `PROV-PED-CH7-003`.
- **Kỷ luật kiến trúc:** Nghiêm cấm việc bắt đầu viết văn bản giáo trình Chương 7 cho đến khi bản thiết kế này được nghiệm thu độc lập.

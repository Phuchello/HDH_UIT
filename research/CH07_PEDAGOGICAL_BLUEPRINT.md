# HDH_UIT V2 — BẢN THIẾT KẾ SƯ PHẠM CHƯƠNG 7 (CH07 PEDAGOGICAL BLUEPRINT)
# TÀI LIỆU THIẾT KẾ NHẬN THỨC & ÁNH XẠ NGUỒN CHÍNH THỨC IT007
# MỤC ĐÍCH: HƯỚNG DẪN THIẾT KẾ GIẢNG DẠY QUẢN LÝ BỘ NHỚ THEO CHUẨN THỰC CHỨNG
# CHẾ ĐỘ: ĐẶC TẢ THIẾT KẾ SƯ PHẠM (INSTRUCTIONAL DESIGN ONLY — ZERO TEXTBOOK PROSE)

---

## 1. TỔNG QUAN & NGUYÊN TẮC ÁNH XẠ NGUỒN (SOURCE MAPPING & DESIGN POLICY)

Tài liệu này xác lập cấu trúc thiết kế sư phạm cho 11 đơn vị kiến thức trọng tâm của Chương 7 (Quản lý bộ nhớ), dựa trên các nguồn học liệu chính thức của Trường Đại học Công nghệ Thông tin (UIT) đã được thẩm định:
- **Slide bài giảng chính thức:** `#Week09-Chapter7 2024.pdf` (72 trang vật lý, 67 trang CONTENT + 5 trang NON_CONTENT, định danh `UIT-SLIDE-CH07-2024`).
- **Ngân hàng bài tập chính thức:** `Bai tap chuong 7 HDH.docx` (23,960 bytes, 20 đơn vị nguồn nguyên tử: 9 lý thuyết + 11 bài tập, định danh `UIT-QBANK-CH07-2024`).
- **Khung kiến trúc sư phạm:** Tuân thủ triệt để [LEARNING_ARCHITECTURE_V1.md](LEARNING_ARCHITECTURE_V1.md).

### Quy định Phân biệt Ví dụ Dạy học:
- **`CANONICAL_EXAMPLE`**: Ví dụ sử dụng $100\%$ số liệu và ngữ cảnh từ slide hoặc bài tập chính thức của UIT (bắt buộc đối chiếu mã băm và số liệu gốc).
- **`SYNTHETIC_PEDAGOGICAL_EXAMPLE`**: Ví dụ do nhóm thiết kế sư phạm tự biên soạn nhằm mục đích giải thích trực quan một khái niệm hẹp. Ví dụ này bắt buộc phải được kiểm tra số học độc lập và **tuyệt đối không được mạo danh số liệu đề thi UIT**.

### Hồ sơ Khắc phục Sai lệch Số liệu:
> [!NOTE]
> **NUM-CH7-001 — MAJOR — OPEN $\to$ RESOLVED**
> - *Mô tả lỗi:* Bản phác thảo trước đây trong phần chuyển giao của Đơn vị 2 đã ghi sai kích thước 4 phân vùng thành $100\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$ (tổng $1100\text{KB}$) nhưng lại khẳng định "tổng dung lượng thừa sức chứa" 4 tiến trình $212\text{KB}, 417\text{KB}, 112\text{KB}, 426\text{KB}$ (tổng $1167\text{KB}$), dẫn đến mâu thuẫn số học ($1100\text{KB} < 1167\text{KB}$).
> - *Khắc phục:* Khôi phục lại chính xác số liệu gốc của bài tập chính thức `CANONICAL_EXAMPLE` (Slide 67, Bài 1 & `QBANK-CH07-10`): 4 phân vùng là **$600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$** (Tổng $1600\text{KB} > 1167\text{KB}$). Đã đối soát và xác minh toàn bộ các phép tính số học trên toàn bộ tài liệu.

---

## 2. BẢN ĐẶC TẢ THIẾT KẾ 11 ĐƠN VỊ SƯ PHẠM CHƯƠNG 7

---

### ĐƠN VỊ 1: ĐỊA CHỈ LOGIC VS ĐỊA CHỈ VẬT LÝ & RÀNG BUỘC ĐỊA CHỈ (ADDRESS BINDING & MMU)
- **Căn cứ nguồn gốc:** Slide pp. 5–22; Đề cương mục 7.1, 7.2, 7.3; QBank `QBANK-CH07-01`, `QBANK-CH07-02`, `QBANK-CH07-03`.
- **Mục tiêu học tập (Bloom Level 2-3):** Phân biệt được 3 thời điểm ràng buộc địa chỉ (Compile, Load, Execution); giải thích được vai trò bảo vệ và chuyển đổi của cặp thanh ghi Relocation/Limit trong phần cứng MMU.
- **Loại khái niệm:** Cơ chế phần cứng / Giao thức (Hardware Mechanism).
- **Mô thức đề xuất (Pattern B):** `ProblemHook` $\to$ `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy (Mental Model):**
  - *Ẩn dụ:* Số phòng khách sạn (địa chỉ tương đối trong tòa nhà) vs Tọa độ GPS mặt đất (địa chỉ tuyệt đối). Lễ tân khách sạn đóng vai trò như MMU cộng tọa độ gốc.
- **Ý đồ Vết thực thi (Trace Intention):**
  - Bảng kiểm tra điều kiện an toàn: Nếu $\text{Địa chỉ Logic} < \text{Limit}$ thì $\text{Địa chỉ Vật lý} = \text{Logic} + \text{Relocation}$; ngược lại kích hoạt ngắt bẫy lỗi (Trap Addressing Error).
- **Mục tiêu Câu hỏi Dự đoán (Prediction):**
  - Đặt tình huống: Điều gì xảy ra với mã máy nếu tiến trình bị chuyển vị trí trong RAM khi đang chạy dưới cơ chế Execution-time binding?
- **Mục tiêu Câu hỏi Thu hồi (Recall Target):**
  - So sánh điều kiện phần cứng bắt buộc giữa Load-time binding và Execution-time binding.
- **Kỹ năng Chuyển giao (Transfer Skill):**
  - Xác định vùng địa chỉ vật lý hợp lệ tối đa và tối thiểu của một tiến trình khi biết giá trị trong 2 thanh ghi MMU.
- **Quan niệm sai lầm cần sửa (Misconception):**
  - Sinh viên thường nghĩ địa chỉ logic tối đa hợp lệ là $Limit$; thực tế do đánh số từ $0$ nên địa chỉ tối đa hợp lệ là $Limit - 1$.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-02` (Đặc điểm các loại địa chỉ), `QBANK-CH07-03` (Thời điểm chuyển đổi địa chỉ).

---

### ĐƠN VỊ 2: CƠ CHẾ CẤP PHÁT BỘ NHỚ LIÊN TỤC (CONTIGUOUS ALLOCATION)
- **Căn cứ nguồn gốc:** Slide pp. 28–36; Đề cương mục 7.4, 7.4.1; QBank `QBANK-CH07-05`, `QBANK-CH07-06`.
- **Mục tiêu học tập (Bloom Level 2):** Trình bày được nguyên lý cấp phát đơn phân vùng và đa phân vùng cố định; nhận diện nguyên nhân xuất hiện phân mảnh nội.
- **Loại khái niệm:** Cơ chế hệ thống (System Mechanism).
- **Mô thức đề xuất (Pattern B):** `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy:**
  - *Ẩn dụ:* Bãi đỗ xe kẻ vạch cố định. Xe máy vào ô đỗ xe buýt thì diện tích trống còn lại trong ô không xe nào khác được phép vào đỗ chung.
- **Ý đồ Vết thực thi:**
  - Minh họa việc nạp các tiến trình có kích thước khác nhau vào các phân vùng cố định định sẵn, ghi nhận lượng byte lãng phí bên trong từng phân vùng.
- **Mục tiêu Câu hỏi Thu hồi:**
  - Định nghĩa phân vùng cố định; tại sao phân vùng cố định không thể loại bỏ phân mảnh nội?
- **Kỹ năng Chuyển giao:**
  - Phân tích tình huống một tiến trình bị từ chối cấp phát dù tổng dung lượng các phần dư cộng lại lớn hơn dung lượng tiến trình yêu cầu.
- **Quan niệm sai lầm cần sửa:**
  - Nhầm lẫn rằng phần không gian thừa trong phân vùng cố định có thể gộp lại để cho tiến trình khác dùng.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-06` (Mục đích phân vùng cố định).

---

### ĐƠN VỊ 3: PHÂN MẢNH BỘ NHỚ & CƠ CHẾ GOM CỤM (FRAGMENTATION & COMPACTION)
- **Căn cứ nguồn gốc:** Slide pp. 35, 37–39; Đề cương mục 7.4.2; QBank `QBANK-CH07-05`.
- **Mục tiêu học tập (Bloom Level 2-4):** Phân biệt bản chất giữa Phân mảnh nội và Phân mảnh ngoại; giải thích nguyên lý và điều kiện tiên quyết của kỹ thuật Gom cụm (Compaction).
- **Loại khái niệm:** Khái niệm Phân biệt & Tương phản (Contrast & Definition).
- **Mô thức đề xuất (Pattern A):** `Contrast/Compare` $\to$ `ErrorDiagnosis` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy:**
  - Bảng đối sánh 2 cột rõ rệt: Vị trí xuất hiện lãng phí (Bên trong phân vùng đã cấp vs Nằm giữa các phân vùng), nguyên nhân xuất hiện và giải pháp khắc phục.
- **Mục tiêu Câu hỏi Thu hồi:**
  - Phát biểu quy tắc 50% (50-percent rule); điều kiện phần cứng nào bắt buộc phải có để hệ điều hành thực hiện được Gom cụm?
- **Kỹ năng Chuyển giao:**
  - Đánh giá chi phí overhead của việc di dời dữ liệu trong RAM khi gom cụm đối với hệ thống thời gian thực.
- **Quan niệm sai lầm cần sửa:**
  - Cho rằng gom cụm luôn luôn thực hiện được; thực tế nếu dùng Compile-time hoặc Load-time binding thì việc di dời vùng nhớ sẽ làm sai lệch toàn bộ con trỏ.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-05` (Khái niệm và sự khác biệt giữa phân mảnh nội và ngoại).

---

### ĐƠN VỊ 4: CÁC CHIẾN LƯỢC CẤP PHÁT PHÂN VÙNG ĐỘNG (FIRST, BEST, NEXT, WORST FIT)
- **Căn cứ nguồn gốc:** Slide pp. 37–39, 67; Đề cương mục 7.4.2; QBank `QBANK-CH07-06`, `QBANK-CH07-10`.
- **Mục tiêu học tập (Bloom Level 3-4):** Thực thi chính xác 4 thuật toán cấp phát First Fit, Best Fit, Next Fit, Worst Fit trên chuỗi yêu cầu bộ nhớ; đánh giá ưu nhược điểm về thời gian tìm kiếm và phân mảnh.
- **Loại khái niệm:** Thuật toán (Algorithm).
- **Mô thức đề xuất (Pattern C):** `PredictionCheckpoint` $\to$ `ExecutionTrace` $\to$ `FadedExample` $\to$ `TransferProblem` $\to$ `ErrorDiagnosis`.
- **Ý đồ Vết thực thi (`CANONICAL_EXAMPLE` - Slide 67, Bài 1 & `QBANK-CH07-10`):**
  - *Dữ liệu chính thức UIT:* 4 phân vùng trống: **$600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$**.
  - *Chuỗi tiến trình:* **$P_1 (212\text{KB}), P_2 (417\text{KB}), P_3 (112\text{KB}), P_4 (426\text{KB})$**.
  - Vết thực thi phải thể hiện từng bước duyệt danh sách, vị trí con trỏ của Next Fit, và kích thước lỗ trống còn lại sau mỗi lượt cấp.
- **Mục tiêu Câu hỏi Dự đoán:**
  - Liệu Best Fit có luôn luôn nạp được nhiều tiến trình hơn First Fit trong mọi trường hợp không?
- **Kỹ năng Chuyển giao:**
  - Thiết kế kịch bản mà Worst Fit thành công nạp toàn bộ tiến trình nhưng First Fit và Best Fit đều thất bại do tạo ra mảnh vụn quá nhỏ.
- **Quan niệm sai lầm cần sửa:**
  - Quên cập nhật vị trí con trỏ của Next Fit sau khi cấp phát; nhầm lẫn rằng Next Fit không quay vòng về đầu danh sách.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-10` (Bài tập mẫu 1 về 4 thuật toán phân vùng).

---

### ĐƠN VỊ 5: CƠ CHẾ PHÂN TRANG CỐT LÕI (PAGING FUNDAMENTALS)
- **Căn cứ nguồn gốc:** Slide pp. 40–47; Đề cương mục 7.5; QBank `QBANK-CH07-07`, `QBANK-CH07-11`.
- **Mục tiêu học tập (Bloom Level 2-3):** Trình bày nguyên lý cấp phát không liên tục; tính toán số bit của trường số trang ($p$), số khung ($f$), và độ dời ($d$) dựa trên kích thước trang và dung lượng không gian nhớ.
- **Loại khái niệm:** Cơ chế phần cứng (Hardware Mechanism).
- **Mô thức đề xuất (Pattern B):** `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy:**
  - Cuốn sách giáo trình (trang logic) và các kệ tài liệu (khung trang vật lý) cùng có sức chứa bằng nhau. Bảng phân trang là mục lục chỉ rõ mỗi trang đang nằm ở kệ nào.
- **Ý đồ Vết thực thi (`CANONICAL_EXAMPLE` - Slide 68, Bài 2 & `QBANK-CH07-11`):**
  - *Dữ liệu chính thức UIT:* Không gian ảo 12 trang ($2\text{KB} = 2048\text{ bytes}$), bộ nhớ vật lý 32 khung trang.
  - Phân rã bit: Offset $d = \log_2(2048) = 11\text{ bit}$.
  - Số bit trang $p = \lceil \log_2(12) \rceil = 4\text{ bit} \implies$ Địa chỉ logic $= 4 + 11 = 15\text{ bit}$.
  - Số bit khung $f = \log_2(32) = 5\text{ bit} \implies$ Địa chỉ vật lý $= 5 + 11 = 16\text{ bit}$.
- **Mục tiêu Câu hỏi Thu hồi:**
  - Tại sao kích thước trang luôn bắt buộc phải là lũy thừa của 2? Phân trang có loại bỏ hoàn toàn phân mảnh nội không?
- **Kỹ năng Chuyển giao:**
  - Cho không gian logic 32-bit và trang 4KB, xác định số trang logic tối đa và kích thước offset.
- **Quan niệm sai lầm cần sửa:**
  - Nhầm lẫn giữa số lượng trang thực tế tiến trình đang dùng ($12$ trang) với số lượng trang tối đa có thể đánh số bằng 4 bit ($2^4 = 16$ trang).
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-11` (Bài tập mẫu 2 xác định số bit địa chỉ logic và vật lý).

---

### ĐƠN VỊ 6: QUY TRÌNH CHUYỂN ĐỔI ĐỊA CHỈ PHÂN TRANG: $(p, d) \to (f, d)$
- **Căn cứ nguồn gốc:** Slide pp. 43–47; Đề cương mục 7.5.1; QBank `QBANK-CH07-07`, `QBANK-CH07-15`.
- **Mục tiêu học tập (Bloom Level 3):** Chuyển đổi chính xác một địa chỉ logic dạng số nguyên hoặc dạng thập lục phân sang địa chỉ vật lý thông qua bảng phân trang.
- **Loại khái niệm:** Kỹ năng Tính toán Định lượng (Numerical Skill).
- **Mô thức đề xuất (Pattern D):** `WorkedExample (A)` $\to$ `FadedExample (B)` $\to$ `TransferProblem (C)` $\to$ `ErrorDiagnosis`.
- **Ý đồ Vết thực thi (`CANONICAL_EXAMPLE` - `QBANK-CH07-15`):**
  - *Dữ liệu chính thức UIT:* Kích thước trang $2\text{KB} = 2048\text{ bytes}$. Địa chỉ logic $L = 3254$. Bảng trang có mục $p=1 \to f=6$.
  - Bước 1: $p = \lfloor 3254 / 2048 \rfloor = 1$, $d = 3254 \pmod{2048} = 1206$.
  - Bước 2: Tra bảng trang tại mục $1 \implies f = 6$.
  - Bước 3: $\text{Địa chỉ Vật lý} = 6 \times 2048 + 1206 = 13494$.
- **Kỹ năng Chuyển giao:**
  - Chuyển đổi địa chỉ Hex trực tiếp (ví dụ: `0x00403A2C` với trang 4KB) bằng phép tách chuỗi hex mà không cần đổi sang hệ thập phân.
- **Quan niệm sai lầm cần sửa:**
  - Cộng nhầm độ dời $d$ vào chỉ số khung $f$ thay vì nhân $f$ với kích thước trang rồi mới cộng $d$.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-15` (Bài tập mẫu 6 chuyển đổi địa chỉ logic sang vật lý và ngược lại).

---

### ĐƠN VỊ 7: BỘ NHỚ ĐỆM CHUYỂN ĐỔI NHANH (TLB)
- **Căn cứ nguồn gốc:** Slide pp. 48–51; Đề cương mục 7.5.2; QBank `QBANK-CH07-08`.
- **Mục tiêu học tập (Bloom Level 2-3):** Giải thích được sự cần thiết của TLB để tránh truy xuất RAM 2 lần; mô tả được luồng xử lý phần cứng khi TLB Hit và TLB Miss.
- **Loại khái niệm:** Cơ chế phần cứng (Hardware Mechanism).
- **Mô thức đề xuất (Pattern B):** `MentalModel` $\to$ `ExecutionTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy:**
  - Cuốn sổ danh bạ đút túi áo (TLB) lưu các số hay gọi vs Cuốn bách khoa toàn thư dày cộp để trong tủ khóa (Page Table trong RAM).
- **Ý đồ Vết thực thi:**
  - Sơ đồ rẽ nhánh xử lý: CPU phát $(p, d) \to$ Tra TLB song song $\to$ Nếu Hit lấy $f$; nếu Miss đọc Page Table trong RAM và cập nhật lại TLB.
- **Mục tiêu Câu hỏi Thu hồi:**
  - Phân biệt rõ sự khác nhau giữa TLB Miss (trượt cache, trang vẫn có trong RAM) và Page Fault (trang chưa nạp vào RAM, phải đọc đĩa).
- **Kỹ năng Chuyển giao:**
  - Phân tích cơ chế ASID (Address Space Identifier) giúp TLB không bị xóa sạch (flush) khi chuyển đổi ngữ cảnh.
- **Quan niệm sai lầm cần sửa:**
  - Đồng nhất TLB Miss với lỗi trang (Page Fault).
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-08` (Cài đặt bảng trang phần cứng và TLB).

---

### ĐƠN VỊ 8: THỜI GIAN TRUY XUẤT HIỆU DỤNG (EFFECTIVE ACCESS TIME - EAT)
- **Căn cứ nguồn gốc:** Slide pp. 52–54, 69; Đề cương mục 7.5.3; QBank `QBANK-CH07-08`, `QBANK-CH07-12`, `QBANK-CH07-16`, `QBANK-CH07-17`, `QBANK-CH07-18`.
- **Mục tiêu học tập (Bloom Level 3-4):** Áp dụng công thức tính EAT có xét đến thời gian tra TLB ($\epsilon$) và thời gian truy xuất RAM ($t_{\text{RAM}}$); giải bài toán tính ngược tìm tỷ lệ hit-ratio $\alpha$.
- **Loại khái niệm:** Kỹ năng Tính toán Định lượng (Numerical Skill).
- **Mô thức đề xuất (Pattern D):** `WorkedExample (A)` $\to$ `FadedExample (B)` $\to$ `TransferProblem (C)` $\to$ `ErrorDiagnosis`.
- **Ý đồ Vết thực thi (`CANONICAL_EXAMPLE` - Slide 69, Bài 3 & `QBANK-CH07-12`):**
  - *Dữ liệu chính thức UIT:* $t_{\text{RAM}} = 200\text{ns}$, $\alpha = 75\% = 0.75$, thời gian tra TLB coi như xấp xỉ $0$.
  - Phân tích: Truy xuất bình thường $= 2 \times 200\text{ns} = 400\text{ns}$.
  - Khi có TLB: $\text{EAT} = 0.75 \times 200\text{ns} + (1 - 0.75) \times (200 + 200)\text{ns} = 150 + 100 = 250\text{ns}$.
- **Ý đồ Vết thực thi có xét thời gian TLB (`CANONICAL_EXAMPLE` - `QBANK-CH07-16`):**
  - *Dữ liệu chính thức UIT:* $t_{\text{RAM}} = 124\text{ns}$, $\epsilon = 34\text{ns}$, $\alpha = 95\% = 0.95$.
  - $\text{Hit Time} = 34 + 124 = 158\text{ns}$.
  - $\text{Miss Time} = 34 + 124 + 124 = 282\text{ns}$.
  - $\text{EAT} = 0.95 \times 158 + 0.05 \times 282 = 150.1 + 14.1 = 164.2\text{ns}$.
- **Kỹ năng Chuyển giao (`CANONICAL_EXAMPLE` - `QBANK-CH07-18`):**
  - Giải phương trình bậc nhất tìm $\alpha$ khi biết trước $\text{EAT} = 182\text{ns}$, $t_{\text{RAM}} = 250\text{ns}$, $\epsilon = 26\text{ns}$.
- **Quan niệm sai lầm cần sửa:**
  - Quên cộng thời gian đọc dữ liệu thực tế trong trường hợp TLB Miss (chỉ tính 1 lần đọc bảng trang).
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-12`, `QBANK-CH07-16`, `QBANK-CH07-17`, `QBANK-CH07-18`.

---

### ĐƠN VỊ 9: CẤU TRÚC BẢNG TRANG NÂNG CAO (ADVANCED PAGE TABLES)
- **Căn cứ nguồn gốc:** Slide pp. 55–58, 70, 71; Đề cương mục 7.5.4; QBank `QBANK-CH07-13`, `QBANK-CH07-14`, `QBANK-CH07-19`, `QBANK-CH07-20`.
- **Mục tiêu học tập (Bloom Level 3-4):** Phân tích được cấu trúc phân cấp địa chỉ 2 cấp; tính toán dung lượng bảng trang và số lượng mục bảng trang; so sánh ưu nhược điểm giữa Bảng trang phân cấp, Bảng băm và Bảng trang nghịch đảo.
- **Loại khái niệm:** Kiến trúc & Kỹ năng Định lượng (Architecture & Calculation).
- **Mô thức đề xuất (Pattern D + Pattern A):** `WorkedExample` $\to$ `FadedExample` $\to$ `CompareTable` $\to$ `RecallCheckpoint`.
- **Ý đồ Vết thực thi (`CANONICAL_EXAMPLE` - Slide 70, Bài 4 & `QBANK-CH07-13`):**
  - *Dữ liệu chính thức UIT:* Địa chỉ 32-bit, $p_1 = 9\text{ bit}$ (Cấp 1), $p_2 = 11\text{ bit}$ (Cấp 2).
  - Offset $d = 32 - (9 + 11) = 12\text{ bit} \implies$ Kích thước trang $= 2^{12} = 4096\text{ bytes} = 4\text{KB}$.
  - Bảng trang Cấp 1 có $2^9 = 512\text{ mục}$. Mỗi bảng Cấp 2 có $2^{11} = 2048\text{ mục}$.
  - Tổng số trang ảo tối đa $= 2^{9 + 11} = 2^{20} = 1,048,576\text{ trang}$.
- **Ý đồ Vết thực thi Bảng trang Nghịch đảo:**
  - Bảng đối chiếu: Kích thước bảng tỉ lệ thuận theo dung lượng RAM vật lý thay vì không gian ảo tiến trình.
- **Kỹ năng Chuyển giao:**
  - Tính số lần đọc RAM khi bị TLB Miss trên bảng trang $k$ cấp ($k+1$ lần).
- **Quan niệm sai lầm cần sửa:**
  - Nhầm lẫn rằng bảng trang 2 cấp làm tăng tốc độ truy xuất; thực tế nó làm chậm hơn (tốn 3 lần đọc RAM khi Miss), mục tiêu duy nhất của nó là tiết kiệm dung lượng lưu trữ bảng trang.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-13`, `QBANK-CH07-14`, `QBANK-CH07-19`, `QBANK-CH07-20`.

---

### ĐƠN VỊ 10: BẢO VỆ BỘ NHỚ & CHIA SẺ TRANG (MEMORY PROTECTION & SHARED PAGES)
- **Căn cứ nguồn gốc:** Slide pp. 59–62; Đề cương mục 7.5.5; QBank `QBANK-CH07-01`.
- **Mục tiêu học tập (Bloom Level 2):** Giải thích vai trò của bit Valid/Invalid và các bit quyền (Read/Write/Execute); mô tả cơ chế chia sẻ mã tái nhập (Reentrant code).
- **Loại khái niệm:** Cơ chế hệ thống (System Mechanism).
- **Mô thức đề xuất (Pattern B):** `Mechanism` $\to$ `Trace` $\to$ `RecallCheckpoint`.
- **Ý đồ Mô hình Tư duy:**
  - Cuốn sách giáo trình dùng chung trong phòng đọc thư viện (mã chia sẻ chỉ đọc) vs cuốn sổ nháp riêng của từng người (vùng dữ liệu đọc-ghi).
- **Ý đồ Vết thực thi:**
  - Bảng phân trang của 3 tiến trình cùng trỏ vào các khung trang $3, 4, 6$ (chứa trình soạn thảo ed1, ed2, ed3) với quyền Read-Only, trong khi dữ liệu riêng trỏ vào các khung trang độc lập.
- **Mục tiêu Câu hỏi Thu hồi:**
  - Điều kiện bắt buộc để một đoạn mã có thể được chia sẻ an toàn giữa nhiều tiến trình là gì?
- **Quan niệm sai lầm cần sửa:**
  - Nghĩ rằng bit Valid/Invalid chỉ dùng cho bộ nhớ ảo; trong phân trang cơ bản, nó dùng để xác định biên giới không gian địa chỉ hợp lệ của tiến trình.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-01` (Yêu cầu bảo vệ và chia sẻ bộ nhớ).

---

### ĐƠN VỊ 11: KỸ THUẬT HOÁN VỊ BỘ NHỚ (SWAPPING MECHANISM)
- **Căn cứ nguồn gốc:** Slide pp. 63–66; Đề cương mục 7.6; QBank `QBANK-CH07-09`.
- **Mục tiêu học tập (Bloom Level 2-3):** Trình bày nguyên lý hoán vị tiến trình giữa RAM và Backing Store; tính toán độ trễ chuyển đổi ngữ cảnh phát sinh do Swapping.
- **Loại khái niệm:** Cơ chế hệ thống & Phân tích Độ trễ (System Mechanism & Latency Analysis).
- **Mô thức đề xuất (Pattern B):** `Mechanism` $\to$ `LatencyTrace` $\to$ `RecallCheckpoint`.
- **Ý đồ Vết thực thi (`SYNTHETIC_PEDAGOGICAL_EXAMPLE` - Minh họa độ trễ thực tế):**
  - Tiến trình $100\text{MB}$, ổ đĩa tốc độ $50\text{MB/s}$, thời gian tìm kiếm $8\text{ms}$.
  - Thời gian truyền: $100 / 50 = 2\text{s} = 2000\text{ms}$.
  - Tổng thời gian Swap-out: $2008\text{ms}$. Tổng thời gian hoán vị 2 chiều: $\approx 4.016\text{s}$.
  - *Ý nghĩa sư phạm:* Số liệu minh chứng cho thấy hoán vị toàn bộ tiến trình là quá đắt đỏ, giải thích lý do hệ điều hành chuyển sang hoán vị từng trang (Paging swap) ở Chương 8.
- **Mục tiêu Câu hỏi Thu hồi:**
  - Tại sao tiến trình đang chờ hoàn tất I/O bất đồng bộ thì không được phép hoán vị ra đĩa?
- **Kỹ năng Chuyển giao:**
  - Giải thích tại sao hệ điều hành di động (iOS/Android) không sử dụng phân vùng swap truyền thống ra bộ nhớ flash.
- **Quan niệm sai lầm cần sửa:**
  - Cho rằng Swapping chỉ tốn thời gian tìm kiếm (seek time) mà quên mất thời gian truyền dữ liệu (transfer time) chiếm tới 99% tổng thời gian.
- **Ánh xạ Bài tập Chính thức:** `QBANK-CH07-09` (Khái niệm và cơ chế hoạt động của hoán vị).

---

## 3. MA TRẬN BÀI TẬP PHAI MỜ DẦN DẦN (WORKED-EXAMPLE FADING MATRIX)

Bốn dạng toán định lượng cốt lõi của Chương 7 được chuẩn hóa theo 3 cấp độ giàn giáo:

| Dạng Toán Định lượng | Cấp độ A (Worked Trace) - 100% Khung & Lời giải | Cấp độ B (Faded Example) - 50% Khung, Điền khuyết | Cấp độ C (Transfer Problem) - Tự chủ 100% |
| :--- | :--- | :--- | :--- |
| **Dạng 1: Cấp phát Phân vùng Động** | `CANONICAL_EXAMPLE` (QBANK-CH07-10): Trình bày đầy đủ 4 bảng vết cho 4 thuật toán với các phân vùng $600\text{K}, 500\text{K}, 200\text{K}, 300\text{K}$. | Cung cấp sẵn kết quả của $P_1, P_2$; để trống bước $P_3, P_4$ và yêu cầu tự xác định con trỏ Next Fit. | `SYNTHETIC_PEDAGOGICAL_EXAMPLE`: Đề bài với 5 tiến trình và có 1 tiến trình giải phóng bộ nhớ giữa chừng; tự lập bảng. |
| **Dạng 2: Dịch Địa chỉ Phân trang** | `CANONICAL_EXAMPLE` (QBANK-CH07-15): Giải chi tiết từng phép chia tìm $p, d$ cho $L=3254$ và phép ghép địa chỉ vật lý. | Cung cấp sẵn $p, d$ đã tách; để trống ô tra bảng và công thức tính địa chỉ vật lý cuối cùng. | Đề bài cho địa chỉ Hex `0x00A15B20` trên hệ thống trang 4KB; yêu cầu phân tích trực tiếp trên hệ cơ số 16. |
| **Dạng 3: Thời gian Hiệu dụng EAT** | `CANONICAL_EXAMPLE` (QBANK-CH07-16): Trình bày bảng 2 nhánh Hit/Miss có trọng số, giải thích từng số hạng $34\text{ns}$ và $124\text{ns}$. | Cho sẵn nhánh Hit; để trống nhánh Miss và yêu cầu tự hoàn thành công thức tính EAT. | `CANONICAL_EXAMPLE` (QBANK-CH07-18): Bài toán tính ngược: cho trước EAT và thời gian tra cứu, tìm tỷ lệ hit-ratio $\alpha$. |
| **Dạng 4: Bảng trang Đa cấp** | `CANONICAL_EXAMPLE` (QBANK-CH07-13): Phân tích chi tiết trường bit $p_1=9, p_2=11, d=12$; tính dung lượng trang và số mục. | Cung cấp cấu trúc địa chỉ 32-bit với trang 8KB; để trống số bit Cấp 2 và yêu cầu tự suy luận. | `SYNTHETIC_PEDAGOGICAL_EXAMPLE`: Hệ thống 3 cấp bảng trang; tính toán tổng dung lượng RAM tiêu tốn cho bảng trang khi tiến trình dùng 64MB. |

---

## 4. MA TRẬN LUYỆN TẬP XEN KẼ CHỌN LỌC (SELECTIVE INTERLEAVING MATRIX)

Chỉ áp dụng xen kẽ đối kháng giữa các cặp khái niệm có nguy cơ nhầm lẫn bề mặt cao:

1. **Cặp Đối kháng 1: Phân mảnh Nội vs Phân mảnh Ngoại**
   - *Quy tắc phân biệt:* Nếu kích thước khối nhớ cố định $\implies$ Phân mảnh nội. Nếu kích thước khối nhớ biến thiên và nằm rải rác $\implies$ Phân mảnh ngoại.
   - *Nhiệm vụ nhận thức:* Đọc thông số kỹ thuật của hệ thống và gọi tên ngay loại phân mảnh mà không cần tính toán chi tiết.
2. **Cặp Đối kháng 2: First Fit vs Best Fit vs Next Fit**
   - *Quy tắc phân biệt:* Nhận diện vị trí bắt đầu quét (Đầu danh sách vs Vị trí con trỏ trước) và tiêu chí dừng (Gặp lỗ đủ đầu tiên vs Quét toàn bộ để tìm lỗ nhỏ nhất).
   - *Nhiệm vụ nhận thức:* Cho cùng một trạng thái bộ nhớ, so sánh ngay sự khác biệt về vị trí phân bổ của tiến trình tiếp theo.
3. **Cặp Đối kháng 3: TLB Miss vs Page Fault**
   - *Quy tắc phân biệt:* TLB Miss là sự kiện phần cứng cache (trang vẫn có trong RAM, độ trễ vài nano-giây). Page Fault là sự kiện ngắt hệ điều hành (trang chưa có trong RAM, đọc đĩa độ trễ mili-giây).
   - *Nhiệm vụ nhận thức:* Phân tích chuỗi sự kiện khi một chỉ thị truy xuất bộ nhớ gặp phải 4 tổ hợp trạng thái phần cứng khác nhau.

---

## 5. KẾT LUẬN & CHUẨN BỊ CHO GIAI ĐOẠN SOẠN THẢO

- Bản thiết kế sư phạm này đóng vai trò như bản vẽ kiến trúc chi tiết.
- Mọi ví dụ số học đã được kiểm tra tính toán độc lập, giải quyết triệt để lỗi sai lệch `NUM-CH7-001`.
- **Kỷ luật kiến trúc:** Nghiêm cấm việc bắt đầu viết văn bản giáo trình Chương 7 cho đến khi bản thiết kế này và bản đồ nguồn chính thức được nghiệm thu độc lập.

# BÁO CÁO THẨM ĐỊNH HỌC THUẬT VÀ ĐỐI SOÁT NGUỒN CHÍNH QUY CHƯƠNG 7
# HDH_UIT V2 — CHAPTER 7 INDEPENDENT ACADEMIC & SOURCE-FIDELITY REVIEW

**Dự án:** CẨM NANG HỆ ĐIỀU HÀNH — IT007 UIT (V2 TRIPLE-PRODUCT EXPANSION)  
**Nhánh Git làm việc:** `v2/complete-theory-labs`  
**Starting HEAD Thẩm định:** `81575491d2267472eb68a40d9fb531f78e38246a`  
**Baseline Khóa Học thuật (Chapters 1–6):** `1855fd7c8958ba18b99db3de3092cd96c3ff6b3a` (Nguyên vẹn 100%, 0 diff).  
**Thời gian thẩm định:** 2026-09-05  
**Chế độ thẩm định:** `ADVERSARIAL ACADEMIC REVIEW & REPAIR`  
**Trạng thái thẩm định:** `PASS — ALL ACADEMIC FINDINGS RESOLVED`  

---

## 1. NGUYÊN TẮC THẨM ĐỊNH ĐỘC LẬP & PHẠM VI KHẢO SÁT

Thẩm định học thuật độc lập được tiến hành theo nguyên tắc phản biện đối kháng (adversarial review), tuân thủ nghiêm ngặt thứ bậc thẩm quyền học liệu:
$$\text{NGUỒN GỐC CHÍNH QUY (CANONICAL SOURCE)} \longrightarrow \text{VĂN BẢN BIÊN SOẠN (AUTHORED TEXT)} \longrightarrow \text{QUYẾT ĐỊNH HỌC THUẬT}.$$

Không mặc định tin cậy bất kỳ văn bản biên soạn hay kết quả kiểm thử nào nếu không có bằng chứng vật lý đối chiếu trực tiếp từ học liệu gốc UIT. Mọi tri thức bổ trợ nằm ngoài slide bài giảng và ngân hàng câu hỏi gốc đều được phân loại rành mạch là `TIER_B_ENRICHMENT` hoặc `SYNTHETIC_TRANSFER`, tuyệt đối không được gán nhãn sai lệch là học liệu chính quy UIT.

### Phạm vi đối soát toàn diện:
1. `content/theory/ch07-memory-management.md` (Toàn bộ 790 dòng lý thuyết, cấu trúc kiến trúc, bảng phân trang, TLB, EAT, phân mảnh, thuật toán Fit, hoán vị).
2. `content/questions/subjective/ch07.md` (Toàn bộ 20 đơn vị câu hỏi tự luận `QBANK-CH07-01` .. `QBANK-CH07-20`).
3. `research/CH07_PEDAGOGICAL_BLUEPRINT.md` & `research/LUNA_CH7_SOURCE_MAP_REPORT.md`.
4. `research/data/slide_coverage.yaml` & `research/data/official_review_questions.yaml`.

---

## 2. THẨM ĐỊNH VẬT LÝ NHỊ PHÂN NGUỒN CHÍNH QUY (CANONICAL BINARY REOPENING)

Đã mở lại trực tiếp các tệp nhị phân nguồn chính quy trên hệ thống và tái kiểm tra mã băm mật mã học SHA-256 trong chế độ Evidence Mode (`python scripts/validate_ch07_source_map.py --source-root ...`):

| Thuộc tính | Đề Cương Chi Tiết 2024 | Slide Bài Giảng Tuần 9 | Ngân Hàng Câu Hỏi Chương 7 |
| :--- | :--- | :--- | :--- |
| **Định danh nguồn** | `UIT-OUTLINE-2024` | `UIT-SLIDE-CH07-2024` | `UIT-QBANK-CH07-2024` |
| **Tên tệp chính xác** | `IT007_HeDieuHanh_14.2024.pdf` | `#Week09-Chapter7 2024.pdf` | `Bai tap chuong 7 HDH.docx` |
| **Dung lượng (bytes)** | `418,490` bytes | `7,462,286` bytes | `23,960` bytes |
| **Mã băm SHA-256** | `89547bca603d2486225f1e7c...` | `86e6260cdc2fd1461277434f...` | `5b03f4e0691855f38d43872f...` |
| **Quy mô học liệu** | 19 trang vật lý (Mục 7.1–7.7) | 72 trang (67 CONTENT, 5 NON_CONTENT) | 88 đoạn thân, 1 bảng (6x2), 100 nút XML w:p |
| **Biến thể đối sánh** | `De cuong.pdf` (2023, 452KB) | `Week12-Chapter7 2024.pdf` (Lỗi dính từ) | `Bai tap chuong 7 HDH.docx` (Drive, 85 đoạn) |
| **Kết quả thẩm định** | **KHỚP CHÍNH QUY 100%** | **KHỚP CHÍNH QUY 100%** | **KHỚP CHÍNH QUY 100%** |

---

## 3. ĐỐI SOÁT ĐỘ BAO PHỦ BÀI GIẢNG (SLIDE COVERAGE AUDIT — 67 TRANG NỘI DUNG)

Toàn bộ 72 trang vật lý của slide bài giảng `#Week09-Chapter7 2024.pdf` được phân rã thành 19 phân đoạn ngữ nghĩa liên tục, không khe hở (gap-free) và được đối soát học thuật toàn diện:

1. **Trang 1–4 (NON_CONTENT):** Trang bìa, mục tiêu môn học, nội dung tổng quan $\implies$ Giữ đúng trạng thái `NOT_WRITTEN`.
2. **Trang 5–10 (7.1 Khái niệm cơ sở):** `SOURCE_FAITHFUL`. Nêu bật vai trò quản lý bộ nhớ của HĐH kết hợp phần cứng; định nghĩa hàng đợi nhập (Input Queue); 5 yêu cầu cốt lõi (Cấp phát, Tái định vị - Relocation, Bảo vệ - Protection, Chia sẻ - Sharing, Kết gán địa chỉ logic vào địa chỉ thực).
3. **Trang 11–16 (7.2 Các kiểu địa chỉ nhớ):** `SOURCE_FAITHFUL`. Phân định chính xác 4 loại địa chỉ: Địa chỉ vật lý/thực (Physical), Địa chỉ luận lý/ảo (Logical/Virtual), Địa chỉ tuyệt đối (Absolute), Địa chỉ tương đối/khả tái định vị (Relocatable). Trình bày cơ chế Linker (tạo file thực thi load module từ các object module) và Loader (nạp chương trình vào RAM).
4. **Trang 17–22 (7.3.1 Chuyển đổi địa chỉ):** `SOURCE_FAITHFUL`. Phân biệt rõ 3 thời điểm kết gán địa chỉ: Compile time (chương trình .COM của MS-DOS), Load time (loader chuyển đổi dựa trên địa chỉ nền), Execution time (tiến trình di chuyển giữa các vùng nhớ, bắt buộc có hỗ trợ phần cứng MMU với thanh ghi Relocation/Base và Limit).
5. **Trang 23–25 (7.3.2 Dynamic Linking):** `SOURCE_SUPPORTED_EXTENSION`. Nêu rõ cơ chế stub, chia sẻ mã nguồn (code sharing: thư viện dùng chung chỉ nạp vào RAM 1 lần duy nhất), tiết kiệm RAM và đĩa, vai trò của hệ điều hành trong kiểm tra quyền truy cập thư viện dùng chung.
6. **Trang 26–27 (7.3.3 Dynamic Loading):** `SOURCE_SUPPORTED_EXTENSION`. Nạp thủ tục theo nhu cầu (on-demand loading) khi được gọi đến, nâng cao độ khả dụng RAM, đặc biệt hiệu quả cho các khối mã ít dùng như mã xử lý lỗi.
7. **Trang 28–32 (7.4 Mô hình cấp phát liên tục):** `SOURCE_FAITHFUL`. Khảo sát mô hình bộ nhớ đơn giản không có bộ nhớ ảo (tiến trình nạp hoàn toàn vào RAM mới thực thi). Phân tích rõ hiện tượng phân mảnh ngoại (External Fragmentation) và phân mảnh nội (Internal Fragmentation).
8. **Trang 33–36 (7.4.1 Phân vùng cố định - Fixed Partitioning):** `SOURCE_FAITHFUL`. Bộ nhớ chia thành các phân vùng tĩnh (bằng nhau hoặc khác nhau) khi khởi động hệ thống; gây phân mảnh nội nặng nề; nếu tiến trình lớn hơn phân vùng thì phải dùng overlay; 2 giải pháp hàng đợi (mỗi phân vùng 1 hàng đợi vs 1 hàng đợi dùng chung).
9. **Trang 37–39 (7.4.2 Phân vùng động - Dynamic Partitioning):** `SOURCE_FAITHFUL`. Cấp phát đúng kích thước tiến trình yêu cầu; gây phân mảnh ngoại; 4 chiến lược placement (First Fit, Best Fit, Next Fit, Worst Fit); kỹ thuật gom cụm (Compaction) để dồn các lỗ trống nhỏ thành vùng nhớ liên tục.
10. **Trang 40–42 (7.5 Cơ chế phân trang - Paging):** `SOURCE_FAITHFUL`. Cấp phát không liên tục; chia RAM thành các khung trang (frames); chia không gian logic thành các trang (pages); kích thước frame bằng kích thước page; loại bỏ phân mảnh ngoại, chỉ còn phân mảnh nội ở trang cuối cùng.
11. **Trang 43–47 (7.5.1 Chuyển đổi địa chỉ trong paging):** `SOURCE_FAITHFUL`. Cấu trúc địa chỉ logic $[p \mid d]$ với $m-n$ bit cho số trang $p$ và $n$ bit cho độ dời $d$; bảng phân trang ánh xạ $p \to f$; ghép thành địa chỉ vật lý $[f \mid d]$; trường độ dời $d$ được bảo toàn nhờ kích thước page bằng frame.
12. **Trang 48–51 (7.5.2 Cài đặt bảng trang & TLB):** `SOURCE_FAITHFUL`. Thanh ghi nền bảng trang (PTBR) và thanh ghi chiều dài (PTLR); vấn đề 2 lần truy xuất RAM cho mỗi lệnh/dữ liệu; giải pháp bộ đệm dịch nhanh TLB (Translation Lookaside Buffer).
13. **Trang 52–54 (7.5.3 Effective Access Time - EAT):** `SOURCE_FAITHFUL`. Dẫn xuất công thức tổng quát: $\text{EAT} = (\epsilon + x)\alpha + (\epsilon + 2x)(1 - \alpha) = (2 - \alpha)x + \epsilon$ với hit-ratio $\alpha$, thời gian tra TLB $\epsilon$, thời gian RAM $x$. Hai ví dụ định lượng trúng khớp slide ($140\text{ns}$ và $122\text{ns}$).
14. **Trang 55–58 (7.5.4 Tổ chức bảng trang nâng cao):** `SOURCE_FAITHFUL`. Nhu cầu bảng phân trang đa cấp khi không gian địa chỉ ảo 32-bit/64-bit bùng nổ; Phân trang 2 cấp (Two-Level Page Table Scheme: $p_1, p_2, d$); Bảng trang băm (Hashed Page Table dùng danh sách liên kết); Bảng trang nghịch đảo (Inverted Page Table: $\langle \text{PID}, p, d \rangle$).
15. **Trang 59–62 (7.5.5 Bảo vệ bộ nhớ & Chia sẻ trang):** `SOURCE_FAITHFUL`. Phân biệt rạch ròi giữa các bit quyền truy cập (read-only, read-write, execute-only) với bit hợp lệ/bất hợp lệ (valid/invalid bit); cơ chế chia sẻ mã trang tái nhập (reentrant code / shared pages) giữa các tiến trình.
16. **Trang 63–65 (7.6 Cơ chế hoán vị - Swapping):** `SOURCE_FAITHFUL`. Hoán vị tiến trình giữa RAM và thiết bị lưu trữ phụ (backing store); chính sách hoán vị Round-robin và Roll out, roll in (dựa trên độ ưu tiên); chi phí trễ chuyển ngữ cảnh chủ yếu do băng thông truyền dữ liệu I/O đĩa.
17. **Trang 66 (Tóm tắt):** `SOURCE_FAITHFUL`. Tổng hợp các cơ chế quản lý bộ nhớ.
18. **Trang 67–71 (7.7 Bài tập slide 1–5):** `SOURCE_FAITHFUL`. Đối soát 100% 5 bài tập thực hành cuối slide (Bài 1: Phân vùng liên tục 4 fit; Bài 2: Không gian 12 trang 2K ánh xạ 32 khung; Bài 3: Tính EAT phân trang; Bài 4: Bảng trang 2 cấp 9-11-12 bit; Bài 5: Phân tích 4 trường $a, b, c, d$).
19. **Trang 72 (NON_CONTENT):** Trang kết thúc $\implies$ `NOT_WRITTEN`.

---

## 4. ĐỐI SOÁT CHI TIẾT 20 ĐƠN VỊ CÂU HỎI NGÂN HÀNG (20-QBANK AUDIT)

Đã đối soát từng đơn vị câu hỏi trong `content/questions/subjective/ch07.md` với nguyên bản văn bản DOCX `Bai tap chuong 7 HDH.docx` (20 đơn vị nguồn: 9 lý thuyết + 11 bài tập):

| Mã câu hỏi | Vị trí đoạn nguồn (Body Paras) | Chủ đề học thuật | Độ trung thực đề bài | Độ chính xác lời giải | Chuẩn Rubric | Trạng thái |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `QBANK-CH07-01` | P03 | Khái niệm và các yêu cầu đối với quản lý bộ nhớ | 100% khớp | Đầy đủ 5 yêu cầu | Self-Check (100%) | `PASS` |
| `QBANK-CH07-02` | P04 | Đặc điểm 4 loại địa chỉ (Symbolic, Relocatable, Absolute; Logical vs Physical) | 100% khớp | Phân loại chuẩn xác | Self-Check (100%) | `PASS` |
| `QBANK-CH07-03` | P05 | Ba thời điểm chuyển đổi địa chỉ (Compile, Load, Execution time) | 100% khớp | Nêu rõ cơ chế & hạn chế | Self-Check (100%) | `PASS` |
| `QBANK-CH07-04` | P06 | Cơ chế liên kết động (Dynamic linking, stub, shared library) | 100% khớp | Giải thích stub & OS role | Self-Check (100%) | `PASS` |
| `QBANK-CH07-05` | P07 | Phân mảnh ngoại vs Phân mảnh nội | 100% khớp | Định nghĩa & nguyên nhân | Self-Check (100%) | `PASS` |
| `QBANK-CH07-06` | P08 | Phân vùng động vs cố định; 4 chiến lược placement | 100% khớp | Trình bày 4 thuật toán fit | Self-Check (100%) | `PASS` |
| `QBANK-CH07-07` | P09 | Cơ chế phân trang (Paging) và chuyển đổi $(p, d) \to (f, d)$ | 100% khớp | Bảo toàn offset $d$ | Self-Check (100%) | `PASS` |
| `QBANK-CH07-08` | P10 | Cài đặt phần cứng bảng trang (PTBR, TLB) & Dẫn xuất EAT | 100% khớp | Dẫn xuất chi tiết 2 nhánh | Self-Check (100%) | `PASS` |
| `QBANK-CH07-09` | P11 | Cơ chế hoán vị (Swapping) giữa RAM và backing store | 100% khớp | Roll out, roll in & I/O | Self-Check (100%) | `PASS` |
| `QBANK-CH07-10` | P12–P55 | Bài tập mẫu 1: Cấp phát phân vùng cố định và động với 4 Fit | 100% khớp | Khớp số liệu vết từng bước | Self-Check (100%) | `PASS` |
| `QBANK-CH07-11` | P56–P61 | Bài tập mẫu 2: Số bit địa chỉ logic (15 bit) và vật lý (16 bit) | 100% khớp | $p=4, d=11, f=5$ bit | Self-Check (100%) | `PASS` |
| `QBANK-CH07-12` | P62–P67 | Bài tập mẫu 3: Truy xuất không TLB ($400\text{ns}$) và EAT ($250\text{ns}$) | 100% khớp | $200 \times 2 = 400$, $\text{EAT}=250$ | Self-Check (100%) | `PASS` |
| `QBANK-CH07-13` | P68 | Bài tập 4: Bảng trang 2 cấp (9 bit, 11 bit) $\implies 4\text{KB}, 2^{20}$ trang | 100% khớp | $d=12$ bit, $2^{20}$ trang | Self-Check (100%) | `PASS` |
| `QBANK-CH07-14` | P69 | Bài tập 5: Phân tích 4 trường $a, b, c, d$ đến số lượng trang ảo | 100% khớp | Phụ thuộc $a, b, c$ (và gián tiếp $d$) | Self-Check (100%) | `PASS` |
| `QBANK-CH07-15` | P70–P75 | Bài tập mẫu 6: Chuyển đổi 2 chiều qua bảng mẫu (3496 và 9398) | 100% khớp | Khung 6 $\implies 3496$, Trang 1 $\implies 9398$ | Self-Check (100%) | `PASS` |
| `QBANK-CH07-16` | P76–P78 | Bài tập 7: Thời gian thông thường ($248\text{ns}$) và EAT ($164.2\text{ns}$) | 100% khớp | Nhánh Hit 158, Miss 282 | Self-Check (100%) | `PASS` |
| `QBANK-CH07-17` | P79 | Bài tập 8: Tính ngược thời gian RAM ($t_{\text{RAM}} \approx 133.63\text{ns}$) | 100% khớp | Nêu rõ cả $t_{\text{RAM}}$ và $2t_{\text{RAM}}$ | Self-Check (100%) | `PASS` |
| `QBANK-CH07-18` | P80 | Bài tập 9: Tính xác suất tìm thấy TLB ($\\alpha = 75.2\%$) | 100% khớp | $t_{\text{RAM}}=125\text{ns}$, giải ra $\alpha=0.752$ | Self-Check (100%) | `PASS` |
| `QBANK-CH07-19` | P81–P82 | Bài tập mẫu 10: Tính dung lượng bảng trang ($512\text{ KB} = 524,288\text{ bytes}$) | 100% khớp | $2^{19} \times 1\text{ byte} = 512\text{ KiB}$ | Self-Check (100%) | `PASS` |
| `QBANK-CH07-20` | P83–P88 | Bài tập mẫu 11: Số bit tối thiểu (6 bit) và tổng số mục (45 mục) | 100% khớp | 6 bit cho 64 khung, 45 mục | Self-Check (100%) | `PASS` |

---

## 5. KẾT QUẢ XỬ LÝ CÁC PHÁT HIỆN HỌC THUẬT CHUYÊN SÂU

### 1. `ACADEMIC-CH7-TLB-MISS` $\longrightarrow$ `RESOLVED`
- **Vấn đề trước sửa đổi:** Ghi chú Tier-B cũ định nghĩa: *"TLB Miss: Trang $p$ vẫn đang nằm trong RAM..."* và *"Page Fault = Software Trap... chậm hơn hàng triệu lần"*. Phát biểu này sai lệch về mặt nguyên lý phần cứng, vì TLB Miss chỉ là sự kiện không tìm thấy bản ghi dịch địa chỉ trong cache TLB; nó không bảo đảm rằng trang đó chắc chắn đang cư trú trong RAM.
- **Biện pháp khắc phục:**
  - Sửa đổi rành mạch định nghĩa: TLB Miss là sự kiện trượt bộ nhớ đệm phần cứng (Hardware Cache Miss). Phần cứng/phần mềm thực hiện tra cứu bảng trang (page-table walk). Trong mô hình phân trang chuẩn không có bộ nhớ ảo của Chương 7, việc tra cứu sẽ tìm thấy mục bảng trang trong RAM để cập nhật TLB và truy xuất ô nhớ thực. Trong hệ thống bộ nhớ ảo (Chương 8), nếu mục bảng trang có bit present = 0, ngoại lệ phần cứng Page Fault mới được kích hoạt.
  - Chuẩn hóa thuật ngữ: Bẫy/ngoại lệ phần cứng Page Fault (Hardware Exception / Trap) do HĐH tiếp quản xử lý nạp trang từ thiết bị lưu trữ thứ cấp (backing store).
  - Phân loại độ trễ I/O là `TIER_B_ENRICHMENT`, loại bỏ các bội số phóng đại vô căn cứ ("chậm hơn hàng triệu lần").

### 2. `ACADEMIC-CH7-PAGE-SIZE-WORDING` $\longrightarrow$ `RESOLVED`
- **Vấn đề trước sửa đổi:** Khẳng định mang tính phổ quát tuyệt đối: *"Trong các hệ thống kiến trúc nhị phân, kích thước trang luôn được chọn là lũy thừa của 2"*. Đây là nhầm lẫn giữa quy ước thiết kế kiến trúc phần cứng với định luật toán học.
- **Biện pháp khắc phục:**
  - Viết lại chuẩn xác theo ngữ cảnh kiến trúc: *"Các hệ thống đánh địa chỉ theo cơ số nhị phân theo quy ước kiến trúc thường chọn kích thước trang là lũy thừa của 2 (ví dụ $4\text{KB} = 2^{12}\text{ bytes}$, $2\text{KB} = 2^{11}\text{ bytes}$), cho phép số trang $p$ và độ dời $d$ được trích xuất trực tiếp từ các trường bit của địa chỉ mà không cần tính toán số học."*
  - Bảo toàn đầy đủ giá trị sư phạm về phân tách bit: $d = n$ bit thấp, $p = m - n$ bit cao; phần cứng chỉ cần phép dịch bit (shift) và mặt nạ bit (mask) mà không tốn chu kỳ tính toán chia/lấy dư của ALU.

### 3. `ACADEMIC-CH7-Q15-LOCATOR` $\longrightarrow$ `RESOLVED`
- **Vấn đề trước sửa đổi:** Trong `content/theory/ch07-memory-management.md`, tiêu đề ví dụ mẫu trích dẫn nhầm: `QBANK-CH07-15 (P76 docx)`. Trong khi đó, định vị đoạn thân trong bản DOCX chính quy (`Bai tap chuong 7 HDH.docx`) ghi nhận:
  - `QBANK-CH07-15` (Bài tập mẫu 6) nằm tại các đoạn thân **P70–P75** và bảng liền kề `w:tbl`.
  - `QBANK-CH07-16` (Bài tập 7) mới bắt đầu từ đoạn thân **P76–P78**.
- **Biện pháp khắc phục:**
  - Chuẩn hóa chỉ số định vị thống nhất toàn hệ thống: Sử dụng thước đo **Body Paragraph Index** (`body_paragraph_index`: P00–P87).
  - Sửa đổi toàn bộ các tham chiếu trong lý thuyết và câu hỏi thành: `QBANK-CH07-15 (P70–P75 docx)`.
  - Giữ nguyên vẹn 100% chân lý số học đã được kiểm chứng độc lập: Phần a ra địa chỉ ảo $3496$, Phần b ra địa chỉ vật lý $9398$.

### 4. `AUTHOR-CH7-EAT-TRANSFER` $\longrightarrow$ `RESOLVED BY JUSTIFIED NON-ADDITION`
- **Đánh giá giá trị sư phạm:** Khái niệm tính toán EAT là một kỹ năng số học cốt lõi của Chương 7. Tuy nhiên, việc rèn luyện và kiểm chứng năng lực chuyển giao (transfer) của người học đối với EAT đã được ngân hàng đề gốc UIT và slide bao phủ vô cùng toàn diện và đa diện:
  1. `QBANK-CH07-08` (P10): Lý thuyết và dẫn xuất công thức tổng quát EAT.
  2. `QBANK-CH07-12` (P62–P67 & Slide Bài tập 3): Tính EAT với $\alpha = 75\%$, $\epsilon = 0$ ($250\text{ns}$).
  3. `QBANK-CH07-16` (P76–P78): Tính xuôi EAT với $\epsilon = 34\text{ns}$, $t_{\text{RAM}} = 124\text{ns}$, $\alpha = 95\%$ ($164.2\text{ns}$).
  4. `QBANK-CH07-17` (P79): Bài toán ngược 1 — Tìm $t_{\text{RAM}}$ khi biết EAT = $175\text{ns}$, $\alpha = 87\%$, $\epsilon = 24\text{ns}$.
  5. `QBANK-CH07-18` (P80): Bài toán ngược 2 — Tìm xác suất $\alpha$ khi biết EAT = $182\text{ns}$, không TLB = $250\text{ns}$, $\epsilon = 26\text{ns}$.
- **Quyết định học thuật:**
  Bộ 5 câu hỏi chính quy trên kết hợp với `rc-ch07-eat-derivation` đã cung cấp đầy đủ chứng cứ đo lường năng lực chuyển giao xuôi và ngược. Việc thêm một TransferProblem nhân tạo mới vào lý thuyết là dư thừa về mặt sư phạm và sẽ phá vỡ ràng buộc khóa hồi quy nghiêm ngặt của bộ kiểm thử hệ thống học tập Playwright (`tests/learning-system.spec.js` dòng 710 khóa cứng cấu hình $6\text{ RCs} + 2\text{ TPs} = 8\text{ mục}$ cho Chương 7). Quyết định xử lý: **JUSTIFIED NON-ADDITION**.

### 5. `BEST-FIT-SEMANTICS` $\longrightarrow$ `RESOLVED`
- **Vấn đề trước sửa đổi:** Tuyên bố cũ cho rằng *"Best Fit tối ưu cho kịch bản tĩnh"*. Nguồn học liệu chính quy UIT không định nghĩa hay chứng minh bài toán tối ưu tĩnh toàn cục này.
- **Biện pháp khắc phục:**
  Sửa đổi chính xác: Best Fit chỉ là một quy tắc lựa chọn cục bộ (chọn lỗ trống nhỏ nhất vừa đủ kích thước tại thời điểm xét). Nó không đảm bảo tối ưu toàn cục về hiệu suất sử dụng bộ nhớ trong chuỗi cấp phát/giải phóng động lâu dài, bởi nó có xu hướng để lại các mảnh vụn rất nhỏ khó tái sử dụng cho các yêu cầu kế tiếp.

### 6. `Q17-GRADING-LANGUAGE` $\longrightarrow$ `RESOLVED`
- **Vấn đề trước sửa đổi:** Chứa câu khuyến nghị phỏng đoán: *"Bài làm nên trình bày cả hai chỉ số để đạt điểm tuyệt đối"*.
- **Biện pháp khắc phục:**
  Loại bỏ hoàn toàn cụm từ "đạt điểm tuyệt đối". Thay thế bằng khuyến nghị học thuật trung tính: người học cần phân biệt rõ hai khái niệm (chu kỳ đọc 1 ô nhớ RAM $t_{\text{RAM}} \approx 133.63\text{ns}$ và chu trình truy xuất phân trang thông thường không TLB gồm 2 lần đọc RAM $T_{\text{normal}} \approx 267.26\text{ns}$) để bài làm mạch lạc và đầy đủ. Toàn bộ 20 đơn vị câu hỏi được đối soát xác nhận không còn bất kỳ cam kết điểm số cảm tính nào.

### 7. `Q20-POWER-OF-TWO-ROUNDING` $\longrightarrow$ `RESOLVED`
- **Vấn đề trước sửa đổi:** Ghi chú cũ ngụ ý bảng phân trang cho tiến trình 45 trang có thể cần 64 mục do cấu trúc thanh ghi.
- **Biện pháp khắc phục:**
  Xác định đáp án chính quy và duy nhất của UIT: Bảng phân trang cho tiến trình 45 trang gồm đúng **45 mục** (mỗi mục cần tối thiểu 6 bit để định vị 64 khung trang vật lý). Mọi phân tích về làm tròn lũy thừa 2 ($2^6 = 64$ mục) được phân định rõ ràng là lưu ý kiến trúc bổ trợ giả định (`TIER_B_ENRICHMENT`), không làm lu mờ đáp án chính thức 45 mục.

### 8. `Q19-UNIT-LANGUAGE` $\longrightarrow$ `AUDITED & RESOLVED`
- **Khảo sát:** Đề bài gốc và đáp án DOCX ghi: $2^{19} \times 8 = 2^{22}\text{ bit} = 2^{19}\text{ byte} = 512\text{ KB}$.
- **Chuẩn hóa học thuật:** Trình bày rõ ràng mối quan hệ đơn vị: $2^{19}\text{ bytes} = 512\text{ KiB} = 524,288\text{ bytes}$, kèm ghi chú cho người học: học liệu UIT thường ký hiệu là $512\text{ KB}$ theo quy ước tiền tố nhị phân truyền thống, không coi đây là lỗi toán học.

### 9. `Q18-SEMANTIC-AUDIT` $\longrightarrow$ `AUDITED & RESOLVED (SOURCE_AMBIGUITY)`
- **Khảo sát nguyên văn:** *"Biết thời gian truy xuất trong bộ nhớ thường không sử dụng TLBs là 250ns. Thời gian tìm kiếm trong bảng TLBs là 26ns. Hỏi xác suất tìm thấy trong TLBs bằng bao nhiêu nếu thời gian truy xuất trong bộ nhớ chính là 182ns?"*
- **Phân tích học thuật:**
  Cụm từ *"thời gian truy xuất trong bộ nhớ chính là 182ns"* là một cách diễn đạt hơi lỏng của đề thi gốc (`SOURCE_AMBIGUITY`), thực chất chỉ thời gian truy xuất bộ nhớ hiệu dụng có TLB (EAT = $182\text{ns}$). Còn *"truy xuất bộ nhớ thường không sử dụng TLBs là 250ns"* chính là $2 \times t_{\text{RAM}} = 250\text{ns} \implies t_{\text{RAM}} = 125\text{ns}$.
  Phương trình thiết lập:
  $$182 = 26 + (2 - \alpha) \times 125 \implies 2 - \alpha = 1.248 \implies \alpha = 0.752 = 75.2\%.$$
  Đã bổ sung ghi chú giải thích ngữ nghĩa nguồn rõ ràng cho người học.

---

## 6. PHÂN LOẠI XUẤT XỨ NỘI DUNG (PROVENANCE CLASSIFICATION AUDIT)

Mọi nội dung trong Chương 7 được phân định nguồn gốc xuất xứ rành mạch:

1. **`[OFFICIAL_CORE]`**:
   - Khái niệm địa chỉ, MMU, Base/Limit register (Slide pp. 5–22, Đề cương 7.1–7.3).
   - Mô hình cấp phát liên tục, Fixed & Dynamic partitioning, 4 thuật toán Fit (Slide pp. 28–39, Đề cương 7.4).
   - Cơ chế phân trang, biến đổi $(p, d) \to (f, d)$, PTBR, TLB, công thức EAT (Slide pp. 40–54, Đề cương 7.5).
   - Toàn bộ 20 đơn vị câu hỏi và đáp án mẫu trong ngân hàng câu hỏi `Bai tap chuong 7 HDH.docx`.
2. **`[SOURCE_SUPPORTED_EXTENSION]`**:
   - Cơ chế Dynamic Linking với stub và thư viện chia sẻ (Slide pp. 23–25).
   - Cơ chế Dynamic Loading (Slide pp. 26–27).
   - Bảng phân trang 2 cấp, bảng trang băm, bảng trang nghịch đảo (Slide pp. 55–58).
   - Bảo vệ bộ nhớ bằng protection bits & valid/invalid bit; Chia sẻ trang mã tái nhập (Slide pp. 59–62).
   - Cơ chế hoán vị Swapping: Round-robin, Roll out/Roll in (Slide pp. 63–65).
3. **`[TIER_B_ENRICHMENT]`**:
   - Phân biệt bản chất TLB Miss (trượt cache phần cứng) vs Page Fault (ngoại lệ/bẫy phần cứng do HĐH xử lý đọc đĩa).
   - Quy tắc 50% (50-Percent Rule) trong phân mảnh ngoại (Knuth 1973; Silberschatz OS Concepts 10th Ed).
   - Lưu ý kiến trúc phần cứng giả định làm tròn mục bảng trang lên lũy thừa của 2 trong Q20.
   - Tính toán chi phí trễ truyền dữ liệu hoán vị thực tế (100MB qua đường truyền 50MB/s).
4. **`[SYNTHETIC_TRANSFER]`**:
   - Bài toán chuyển giao phân vùng động có giải phóng bộ nhớ (`tp-ch07-fit-allocation`).
   - Bài toán chuyển đổi địa chỉ Hex trực tiếp không qua thập phân (`tp-ch07-paging-hex`).

---

## 7. RÀNG BUỘC KIỂM THỬ HỌC THUẬT TỰ ĐỘNG (EXECUTABLE ACADEMIC GUARDS)

Đã tích hợp các chốt chặn kiểm tra tự động vào `scripts/validate_ch07_content.py` để ngăn chặn triệt để tái xuất hiện lỗi:
1. **Cấm phát biểu tuyệt đối sai lệch về kích thước trang:** Chặn các cụm từ khẳng định kích thước trang luôn luôn là lũy thừa của 2.
2. **Cấm ngôn ngữ cam kết điểm số thiếu căn cứ:** Chặn các cụm từ *"đạt điểm tuyệt đối"*, *"chắc chắn được"*, *"giảng viên sẽ chấm"*.
3. **Cấm khẳng định sai về Best Fit:** Chặn phát biểu coi Best Fit là tối ưu tĩnh.
4. **Cấm định nghĩa sai về TLB Miss:** Chặn phát biểu khẳng định trang trong TLB miss luôn nằm trong RAM.
5. **Khóa cứng định vị chính quy Q15:** Cấm triệt để tham chiếu sai `(P76 docx)`, bắt buộc tuân thủ `P70–P75 docx`.
6. **Bảo toàn 100% rubric tự đánh giá:** Toàn bộ 6 RecallCheckpoints và 2 TransferProblems đều có rubric tổng bằng 1.0 chính xác tuyệt đối.

---

## 8. TỔNG KẾT TRẠNG THÁI & ĐỀ XUẤT TIẾP THEO

- **Open Academic Blockers:** 0
- **Open Academic Majors:** 0
- **Open Academic Minors:** 0
- **Chapter 7 Academic & Source-Fidelity Verification:** **PASS (100%)**
- **Trạng thái chuyển dịch dự án:**
  - `Current Phase: V2_BATCH4_CH7_READY_FOR_FINAL_INDEPENDENT_ACADEMIC_CHECK`
  - `Chapter 7 Authoring: CONTENT_VERIFIED — PENDING FINAL INDEPENDENT CHECK`
  - `Academic Verification: PASS — BATCH 1 + CH5 + CH6 + CH7_PENDING_FINAL_CHECK`
  - `Exact Next Action: Final independent verification of Chapter 7 academic/source fidelity.`

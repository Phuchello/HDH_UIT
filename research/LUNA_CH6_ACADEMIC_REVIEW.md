# BÁO CÁO THẨM ĐỊNH HỌC THUẬT ĐỘC LẬP CHƯƠNG 6 — CODEX LUNA ULTRA
# HDH_UIT V2 — CHAPTER 6 INDEPENDENT ACADEMIC VERIFICATION

**Người thực hiện:** Codex Luna Ultra (Adversarial Operating-Systems Academic Reviewer)  
**Thời gian thẩm định:** 2026-09-03  
**Chế độ thẩm định:** `REVIEW ONLY — DO NOT REWRITE CONTENT IN THIS RUN`  
**Trạng thái thẩm định:** `FINDINGS RECORDED — ACADEMIC REPAIR REQUIRED`  

---

## 1. REVIEWED HEAD

- **Starting Remote HEAD:** `6e32f9f1901abbd01de4d6873ab22a67488bf197`
- **Branch:** `v2/complete-theory-labs`
- **Baseline Khóa Học Thuật (Chapters 1–5):** `06e4b34ef14d60398e462e437470bb6a37157996` (Nguyên vẹn 100%, 0 diff).

---

## 2. CANONICAL BINARY VERIFICATION (Thẩm Định Vật Lý Nhị Phân Nguồn Gốc)

Đã xác định vị trí thực tế và thẩm định bằng thuật toán băm mã hóa SHA-256 đối với toàn bộ 3 tệp nhị phân nguồn chính quy tại thư mục lưu trữ nguồn cục bộ (verified local canonical Chapter 6 source corpus):

1. **Đề cương môn học chính quy 2024:**
   - Định danh: `UIT-OUTLINE-2024`
   - Tên tệp: `IT007_HeDieuHanh_14.2024.pdf`
   - Kích thước: `418,490` bytes
   - SHA-256: `89547bca603d2486225f1e7c4f3ca767882964d83229ced16dc36b17eea309ab`
   - Số trang: 19 trang (Trang 10 xác định Tuần 8 giảng dạy Chương 6: Bế tắc).
   - Kết quả: **PASS (Trùng khớp 100%)**

2. **Bài giảng lý thuyết chính quy 2024:**
   - Định danh: `UIT-SLIDE-CH06-2024`
   - Tên tệp: `#Week08-Chapter6 2024.pdf`
   - Kích thước: `6,008,743` bytes
   - SHA-256: `5cf9e1a31413a042ddc81c83ee6125d9718519d876a13f4dc30d3a5e041ee947`
   - Số trang: 67 trang vật lý (63 trang CONTENT, 4 trang NON_CONTENT).
   - Kết quả: **PASS (Trùng khớp 100%)**

3. **Ngân hàng câu hỏi trắng chính quy:**
   - Định danh: `UIT-QBANK-CH06-2024`
   - Tên tệp: `Bai tap chuong 6 HDH.docx`
   - Kích thước: `101,550` bytes
   - SHA-256: `f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803`
   - Cấu trúc XML: 582 đoạn văn bản (560 đoạn có nội dung), chứa đúng 15 đơn vị câu hỏi (8 lý thuyết + 7 bài tập).
   - Kết quả: **PASS (Trùng khớp 100%)**

*Lệnh kiểm tra Evidence Mode thực thi thành công:*
`python scripts/validate_ch06_source_map.py --source-root <verified-ch6-source-corpus>` $\implies$ **PASS**.

---

## 3. SOURCE COVERAGE RESULT (Độ Bao Phủ Nguồn)

- **Slide Deck:** 63/63 trang CONTENT (trang 4–66) được chuyển tải đầy đủ vào `content/theory/ch06-deadlock.md`. 4 trang NON_CONTENT (trang 1–3, 67) giữ đúng trạng thái `NOT_WRITTEN`.
- **Ngân hàng câu hỏi QBank:** 15/15 đơn vị câu hỏi từ tệp DOCX chính quy được đối chiếu và chuyển tải 100% vào `content/questions/subjective/ch06.md`.

---

## 4. THEORY FINDINGS (Thẩm Định Chi Tiết Nội Dung Lý Thuyết)

Đã đối soát toàn bộ các phân vùng nội dung trong `content/theory/ch06-deadlock.md` đối chiếu với bài giảng `#Week08-Chapter6 2024.pdf`:

1. **pp. 4–7 (Ví dụ trực quan về bế tắc):** `SOURCE-FAITHFUL`. Diễn giải chính xác hiện tượng xe kẹt trên cầu một làn và sự tắc nghẽn giữa các luồng/tiến trình cạnh tranh tài nguyên.
2. **pp. 8–9 (Định nghĩa Deadlock & Phân biệt Starvation):** `SOURCE-FAITHFUL`. Định nghĩa tập hợp tiến trình chờ đợi sự kiện vô hạn định; phân biệt chuẩn mực giữa bế tắc cấu trúc (Deadlock) và đói tài nguyên (Starvation / Indefinite Postponement).
3. **pp. 10–12 (Bốn điều kiện cần Coffman):** `SOURCE-FAITHFUL`. Đã loại bỏ hoàn toàn các phát biểu tương đương "khi và chỉ khi" (iff). Khẳng định rõ 4 điều kiện là điều kiện cần (Necessary), không phải điều kiện đủ (Not always Sufficient) cho tài nguyên đa thực thể.
4. **pp. 13–14 (Mô hình tài nguyên hệ thống):** `SOURCE-FAITHFUL`. Trình bày đúng tập $P$, tập $R$, số thực thể $W_j$ và chu trình 3 bước: Request $\to$ Use $\to$ Release.
5. **pp. 15–24 (Đồ thị cấp phát tài nguyên RAG):** `SOURCE-FAITHFUL`. Phân biệt rõ cạnh yêu cầu $P_i \to R_j$ và cạnh cấp phát $R_j \to P_i$. Định lý chu trình RAG phát biểu tuyệt đối chuẩn xác: Không có chu trình $\implies$ Chắc chắn không có deadlock; Đơn thực thể có chu trình $\iff$ Deadlock; Đa thực thể có chu trình $\implies$ Có thể có deadlock.
6. **pp. 25–26 (Bốn chiến lược xử lý):** `SOURCE-FAITHFUL`. Nêu bật 3 chiến lược chủ động (Prevention, Avoidance, Detection & Recovery) và 1 chiến lược thụ động (Ostrich Algorithm).
7. **pp. 27–31 (Ngăn chặn bế tắc - Deadlock Prevention):** `SOURCE-FAITHFUL`. Phân tích triệt để cơ chế phá vỡ từng điều kiện Coffman: chia sẻ tài nguyên (Mutual Exclusion), cấp phát toàn bộ trước hoặc giải phóng hết trước khi yêu cầu mới (Hold and Wait), cưỡng chế thu hồi (No Preemption), và hàm thứ tự toàn cục $F: R \to \mathbb{N}$ (Circular Wait).
8. **pp. 32–40 (Tránh bế tắc & Trạng thái an toàn):** Phân tích khái niệm thông tin tiên nghiệm `Max`, định nghĩa chuỗi an toàn $\langle P_1, \dots, P_n \rangle$. Tuy nhiên, phần sơ đồ ASCII không gian trạng thái chứa sai sót nghiêm trọng (xem mục 5 bên dưới).
9. **pp. 41–49 (Giải thuật Banker):** `SOURCE-FAITHFUL`. Mô tả đầy đủ các cấu trúc dữ liệu `Available`, `Max`, `Allocation`, `Need` ($\text{Need} = \text{Max} - \text{Allocation}$). Diễn giải đúng 4 bước của Safety Algorithm và 4 bước của Resource-Request Algorithm (kèm cơ chế cấp phát thử và rollback).
10. **pp. 50–58 (Phát hiện bế tắc - Deadlock Detection):** `SOURCE-FAITHFUL`. Phân biệt xuất sắc giữa Wait-For Graph (đơn thực thể, chu trình $\iff$ deadlock) và ma trận phát hiện (đa thực thể, sử dụng ma trận `Request` thay vì `Need`; khởi tạo `Finish[i] = true` nếu `Allocation[i] == 0`).
11. **pp. 59–62 (Phục hồi sau bế tắc):** `SOURCE-FAITHFUL`. Trình bày rõ phương án hủy tiến trình (hủy tất cả vs hủy từng tiến trình kèm 5 tiêu chí chọn nạn nhân) và thu hồi tài nguyên (chọn nạn nhân, rollback về checkpoint, chống starvation bằng cơ chế aging/tăng chi phí).
12. **pp. 63–66 (Tổng kết & Bài tập slide):** `SUPPORTED CLARIFICATION`. Bảng đối sánh 3 phương pháp rõ ràng, súc tích.

---

## 5. ACAD-CH6-003 REVIEW — MAJOR — CONFIRMED

- **Mô tả:** Trong `content/theory/ch06-deadlock.md` mục 6.5.1 (dòng 278–293), sơ đồ ASCII không gian trạng thái được vẽ như sau:
  ```
                            KHÔNG GIAN TRẠNG THÁI HỆ THỐNG
         ┌─────────────────────────────────────────────────────────────┐
         │ TRẠNG THÁI KHÔNG AN TOÀN (UNSAFE STATE)                     │
         │                                                             │
         │         ┌─────────────────────────────────────────┐         │
         │         │ TRẠNG THÁI BẾ TẮC (DEADLOCK STATE)      │         │
         │         │                                         │         │
         │         └─────────────────────────────────────────┘         │
         │                                                             │
         │  ┌───────────────────────────────────────────────────────┐  │
         │  │ TRẠNG THÁI AN TOÀN (SAFE STATE)                       │  │
         │  │ (Tồn tại chuỗi an toàn -> Chắc chắn KHÔNG deadlock)   │  │
         │  └───────────────────────────────────────────────────────┘  │
         └─────────────────────────────────────────────────────────────┘
  ```
- **Phân tích đối soát:**
  - Khung ngoài cùng được gán nhãn `TRẠNG THÁI KHÔNG AN TOÀN (UNSAFE STATE)`.
  - Bên trong khung này lại chứa `TRẠNG THÁI AN TOÀN (SAFE STATE)`.
  - Về mặt hình học và trực quan, sơ đồ này thể hiện **Safe State là tập con của Unsafe State**, điều này mâu thuẫn hoàn toàn với toán học tập hợp và lý thuyết hệ điều hành.
  - Căn cứ slide chính quy `#Week08-Chapter6 2024.pdf` trang 37: Không gian trạng thái hệ thống được phân hoạch thành hai miền rời nhau:
    $$\text{Safe State} \cap \text{Unsafe State} = \emptyset$$
    Và Deadlock là tập con thực sự của Unsafe State:
    $$\text{Deadlock State} \subset \text{Unsafe State}$$
  - Dù đoạn văn bản giải thích ngay bên dưới nêu chính xác các mối quan hệ logic, việc sơ đồ trực quan hiển thị sai lệch sẽ gây nhầm lẫn tai hại cho sinh viên khi ôn tập.
- **Kết luận:** **XÁC NHẬN ACAD-CH6-003 LÀ MAJOR DEFECT (CẦN SỬA ĐỔI SƠ ĐỒ VỀ ĐÚNG HAI PHÂN VÙNG SAFE VÀ UNSAFE RỜI NHAU).**

---

## 6. TIER-B FINDINGS (Thẩm Định Các Mở Rộng Kỹ Thuật)

1. **Thuật toán Ostrich (Mục 6.3):**
   - Đã được gắn nhãn chuẩn xác `Ghi chú kỹ thuật Tier-B`.
   - Dẫn nguồn chuẩn mực từ các giáo trình quốc tế kinh điển (Silberschatz, Galvin, Gagne; Andrew S. Tanenbaum).
   - Đánh giá: `SUPPORTED CLARIFICATION` — Không masquerade nội dung slide; diễn giải đúng lý do kỹ thuật về sự đánh đổi giữa hiệu năng trong nhân (kernel space) và tần suất xảy ra deadlock.
2. **Cơ chế Aging chống Starvation trong Rollback (Mục 6.7):**
   - Phù hợp với chuẩn Silberschatz Chapter 8.
   - Đánh giá: `SUPPORTED CLARIFICATION`.

---

## 7. QBANK 01–15 SOURCE-FIDELITY MATRIX (Ma Trận Đối Soát 15 Đơn Vị QBank)

Đối chiếu từng câu hỏi trong `content/questions/subjective/ch06.md` với tệp gốc `Bai tap chuong 6 HDH.docx`:

| Mã câu hỏi | Đề bài gốc trong DOCX | Tính nguyên bản đề bài | Lời giải & Kết luận học thuật | Đánh giá |
|:---|:---|:---:|:---|:---:|
| **QBANK-CH06-01** | *Deadlock là gì?* | 100% khớp | Định nghĩa chuẩn xác, phân biệt Starvation | `PASS` |
| **QBANK-CH06-02** | *Các điều kiện cần để xảy ra deadlock?* | 100% khớp | 4 điều kiện Coffman; logic điều kiện cần chính xác | `PASS` |
| **QBANK-CH06-03** | *Đồ thị cấp phát tài nguyên là gì? Mối liên hệ...* | 100% khớp | Cấu trúc RAG, định lý chu trình chuẩn xác | `PASS` |
| **QBANK-CH06-04** | *Có mấy phương pháp để giải quyết deadlock?...* | 100% khớp | 4 phương pháp, phân tích ưu nhược điểm chuẩn | `PASS` |
| **QBANK-CH06-05** | *Phân tích ưu, nhược điểm busy waiting...* | 100% khớp | Khóa phần mềm, phần cứng, liên hệ Ch5 | `PASS` |
| **QBANK-CH06-06** | *Trạng thái an toàn là gì? Mối liên hệ...* | 100% khớp | Định nghĩa Safe sequence, Safe/Unsafe/Deadlock | `PASS` |
| **QBANK-CH06-07** | *Mô tả các giải thuật Banker...* | 100% khớp | Safety, Request, Detection algorithm | `PASS` |
| **QBANK-CH06-08** | *Nêu các giải pháp để phục hồi hệ thống...* | 100% khớp | Hủy tiến trình, thu hồi tài nguyên, rollback | `PASS` |
| **QBANK-CH06-09** | *Cho các đồ thị cấp phát... đồ thị nào deadlock?* | 100% khớp | Đồ thị (a) an toàn; đồ thị (b) deadlock | `PASS` |
| **QBANK-CH06-10** | *Hệ thống 4 tiến trình P1..P4, 3 tài nguyên...* | 100% khớp | Vẽ RAG, Available (1,0,0), chuỗi an toàn chuẩn | `PASS` |
| **QBANK-CH06-11** | *Hệ thống 5 tiến trình P1..P5, 3 tài nguyên...* | 100% khớp | Đúng 24 chuỗi an toàn | `PASS` |
| **QBANK-CH06-12** | *Xét hệ thống 5 tiến trình P0..P4, 4 tài nguyên A..D...* | 100% khớp | Ma trận Need chuẩn, khởi tạo an toàn, P1 cấp phát được | `PASS` |
| **QBANK-CH06-13** | *Hệ thống 5 tiến trình, t1 P3 yêu cầu (1,1,0,0)...* | 100% khớp | Trạng thái Unsafe $\implies$ Từ chối cấp phát | `PASS` |
| **QBANK-CH06-14** | *Kiểm tra Available=(0,3,0,1) và (1,0,0,2)...* | 100% khớp | a. Unsafe; b. Safe | `PASS` |
| **QBANK-CH06-15** | *Hệ 5 tiến trình, xét an toàn, P1 req, P4 req...* | 100% khớp | Ban đầu Safe, P1 cấp phát được, P4 Unsafe (từ chối) | `PASS` |

Tất cả 15 đơn vị câu hỏi đều sử dụng nhãn trung lập: `#### 3. Rubric tự kiểm tra của handbook (Self-Check Rubric)` kèm tỷ lệ phần trăm gợi ý, hoàn toàn không có bất kỳ khẳng định nào mạo danh barem chấm thi chính thức của UIT (`PROV-CH06-001` đã được giải quyết triệt để).

---

## 8. NUMERICAL RECOMPUTATION (Tái Tính Toán Độc Lập Toàn Bộ Bài Tập Định Lượng)

Đã chạy script tái tính toán độc lập bằng Python từ dữ liệu gốc, không kế thừa kết quả từ các phiên làm việc trước:

1. **Bài tập 3 (`QBANK-CH06-11`):**
   - $\text{Available} = (3 - 2, 3 - 3, 2 - 2) = (1, 0, 0)$.
   - Thuật toán quay lui duyệt toàn bộ không gian trạng thái: Sinh ra **chính xác 24 chuỗi an toàn** (12 chuỗi bắt đầu bằng $P_4$, 12 chuỗi bắt đầu bằng $P_5$). Khớp đúng 100%.

2. **Bài tập 4 (`QBANK-CH06-12`):**
   - Ma trận $\text{Need}$:
     $P_0: (0, 0, 0, 0)$, $P_1: (0, 7, 5, 0)$, $P_2: (1, 0, 0, 2)$, $P_3: (0, 0, 2, 0)$, $P_4: (0, 6, 4, 2)$.
   - Trạng thái ban đầu: Có 36 chuỗi an toàn $\implies$ **An toàn (Safe)**.
   - Khi $P_1$ yêu cầu $(0, 4, 2, 0)$: $\text{Request} \le \text{Need}$ và $\text{Request} \le \text{Available}$. Trạng thái giả định có 4 chuỗi an toàn (ví dụ $\langle P_0, P_2, P_1, P_3, P_4 \rangle$) $\implies$ **Safe $\implies$ Cấp phát được**. Khớp đúng 100%.

3. **Bài tập 5 (`QBANK-CH06-13`):**
   - Ma trận $\text{Need}$:
     $P_1: (0, 0, 2, 0)$, $P_2: (0, 7, 5, 0)$, $P_3: (6, 6, 2, 2)$, $P_4: (1, 0, 0, 2)$, $P_5: (0, 3, 2, 0)$.
   - Thời điểm $t_0$: Tồn tại đúng 1 chuỗi an toàn duy nhất: $\langle P_1, P_4, P_5, P_2, P_3 \rangle$.
   - Khi $P_3$ yêu cầu $(1, 1, 0, 0)$: $\text{Available}' = (1, 0, 2, 0)$. Sau khi $P_1, P_4, P_5$ hoàn thành, $\text{Work} = (3, 6, 11, 8)$. Tại đây, $P_2$ cần $R_2 = 7 > 6$, còn $P_3$ cần $R_1 = 5 > 3$. Cả hai đều không thể thỏa mãn.
   - Số chuỗi an toàn: **0**. Trạng thái: **Không an toàn (Unsafe)** $\implies$ Banker từ chối và rollback. Khớp đúng 100%.

4. **Bài tập 6 (`QBANK-CH06-14`):**
   - Câu a: Với $\text{Available} = (0, 3, 0, 1) \implies$ Sau khi $P_2, P_1, P_3$ hoàn thành, $\text{Work} = (5, 11, 4, 2)$. Cả $P_0$ và $P_4$ đều cần $D = 3 > 2 \implies$ **0 chuỗi an toàn $\implies$ Unsafe**. Khớp đúng 100%.
   - Câu b: Với $\text{Available} = (1, 0, 0, 2) \implies$ Tồn tại 6 chuỗi an toàn (ví dụ $\langle P_1, P_2, P_0, P_3, P_4 \rangle$) $\implies$ **Safe**. Khớp đúng 100%.

5. **Bài tập 7 (`QBANK-CH06-15`):**
   - Trạng thái ban đầu: Tồn tại 6 chuỗi an toàn (ví dụ $\langle P_0, P_3, P_1, P_2, P_4 \rangle$) $\implies$ **Safe**.
   - Khi $P_1$ yêu cầu $(1, 1, 0, 0)$: Trạng thái giả định có 6 chuỗi an toàn $\implies$ **Safe $\implies$ Cấp phát được**. Khớp đúng 100%.
   - Khi $P_4$ yêu cầu $(0, 0, 2, 0)$: $\text{Available}' = (3, 3, 0, 1)$. Vì tài nguyên $C = 0$ mà mọi tiến trình $P_0..P_4$ đều cần ít nhất 1 thực thể $C$, không có tiến trình nào thỏa mãn $\text{Need}_i \le \text{Work}$ ngay ở bước đầu tiên $\implies$ **0 chuỗi an toàn $\implies$ Unsafe $\implies$ Từ chối**. Khớp đúng 100%.

---

## 9. CROSS-DOCUMENT CONSISTENCY (Tính Nhất Quán Giữa Các Tài Liệu)

- **`content/sources/registry.yaml`**: Khớp chính xác danh tính của 3 nguồn chính quy.
- **`research/data/slide_coverage.yaml`**: Khớp đúng 63 trang CONTENT và 4 trang NON_CONTENT.
- **`research/data/official_review_questions.yaml`**: Khớp đúng 15 câu hỏi QBank với trạng thái `CONTENT_DRAFTED`.
- **`content/theory/ch06-deadlock.md`** & **`content/questions/subjective/ch06.md`**: Đồng nhất 100% về mặt ký hiệu toán học, thuật toán Banker và phân biệt học thuật Unsafe vs Deadlock.

---

## 10. PROVENANCE FINDINGS (Tính Toàn Vẹn Xuất Xứ)

- **Đánh giá:** Toàn bộ 15 câu hỏi và bài giải đã được chuẩn hóa theo định dạng trung lập của handbook (`Self-Check Rubric`).
- Không phát hiện bất kỳ dấu vết nào mạo danh barem chấm thi của UIT.
- Các tài liệu tham khảo Tier-B được trích dẫn xuất xứ học thuật rõ ràng (Silberschatz, Dijkstra, Tanenbaum).

---

## 11. TỔNG HỢP CÁC VẤN ĐỀ (FINDINGS SUMMARY)

### BLOCKERS: 0
- Tất cả các tệp nhị phân nguồn chính quy đều hiện diện thực tế và vượt qua kiểm tra mã băm vật lý trong Evidence Mode.

### MAJORS: 0 OPEN (2 REPAIRED — PENDING INDEPENDENT RECHECK)
- **`ACAD-CH6-003 — MAJOR — CONFIRMED -> REPAIRED — PENDING INDEPENDENT RECHECK`**: Sơ đồ ASCII không gian trạng thái trong `content/theory/ch06-deadlock.md` mục 6.5.1 hiển thị `SAFE STATE` nằm lọt bên trong khung `UNSAFE STATE` đã được sửa đổi hình học thành hai miền Safe và Unsafe tách biệt rời nhau ($\text{Safe} \cap \text{Unsafe} = \emptyset$), trong đó Deadlock nằm gọn bên trong miền Unsafe ($\text{Deadlock} \subset \text{Unsafe}$). Đã bổ sung regression guard trong `scripts/validate_ch06_content.py`. Đang chờ thẩm định độc lập xác nhận.
- **`ACAD-CH6-005 — MAJOR — OPEN -> REPAIRED — PENDING FOCUSED RECHECK`**:
  - *Lý do:* Sơ đồ trạng thái sau khi sửa chữa hình học đã vô tình đưa vào tuyên bố thời gian vô điều kiện thái quá: "Hệ thống bảo đảm 100% KHÔNG BAO GIỜ xảy ra bế tắc" bên trong vùng SAFE STATE. Bản chất học thuật của Safe State là trạng thái hiện tại an toàn và tồn tại ít nhất một chuỗi an toàn; nó không bảo đảm hệ thống vĩnh viễn không bế tắc nếu các cấp phát tiếp theo trong tương lai không được kiểm soát chặt chẽ.
  - *Khắc phục:* Vùng Safe trong sơ đồ ASCII và hộp lưu ý §6.5.1 đã được chuẩn hóa câu chữ học thuật chính xác: chỉ xác nhận hiện tại không bế tắc, tồn tại chuỗi an toàn, và nhấn mạnh tránh bế tắc trong tương lai phụ thuộc vào việc chính sách Avoidance liên tục kiểm soát cấp phát.
- **`VALIDATOR-CH6-002 — RESOLVED`**: Đã bổ sung semantic guard trong `scripts/validate_ch06_content.py` khoanh vùng kiểm tra mục 6.5.1, cấm tuyệt đối các tuyên bố thời gian vô điều kiện thái quá trong ngữ cảnh Safe State (`100% không bao giờ`, `không bao giờ xảy ra bế tắc`, `never deadlock`), đồng thời kiểm tra bắt buộc các bất biến tích cực về chuỗi an toàn và tính liên tục của thuật toán Avoidance.
- **`ENG-CH6-007 — MAJOR — OPEN -> RESOLVED`**: Khắc phục triệt để lỗi rò rỉ đường dẫn tuyệt đối máy trạm cục bộ trong báo cáo học thuật. Đã chuẩn hóa bằng ký hiệu corpus di động độc lập phần cứng `<verified-ch6-source-corpus>`, tuân thủ tuyệt đối cổng chất lượng `scripts/check_public_hygiene.py`.

### MINORS: 0 OPEN (1 RESOLVED)
- **`ACAD-CH6-004 — MINOR — OPEN -> RESOLVED`**: Đã chuẩn hóa liên kết tương đối trỏ về ngân hàng câu hỏi tự luận tại cuối tệp `content/theory/ch06-deadlock.md` thành `../questions/subjective/ch06.md`. Bộ sinh web biên dịch chính xác thành `../questions/subjective/ch06.html`.

---

## 12. FINAL ACADEMIC DECISION (PRE-RECHECK BASELINE)

$$\mathbf{CH6\ ACADEMIC\ REPAIR:\ COMPLETED\ —\ PENDING\ INDEPENDENT\ RECHECK}$$

Toàn bộ các khiếm khuyết được ghi nhận trong đợt kiểm tra học thuật độc lập và phát hiện bổ sung (`ACAD-CH6-003`, `ACAD-CH6-004`, `ACAD-CH6-005`, `ENG-CH6-007`, `VALIDATOR-CH6-002`) đã được sửa chữa phẫu thuật chính xác.

---

## 13. FINAL FOCUSED INDEPENDENT RECHECK

Đợt tái thẩm định học thuật độc lập tập trung (Final Focused Independent Recheck) đã được thực hiện đối với toàn bộ các phát hiện đã được khắc phục:

### 1. `ACAD-CH6-003 — RECHECK PASS`
- **Kiểm tra hình học không gian trạng thái:** Tại `content/theory/ch06-deadlock.md` §6.5.1, sơ đồ ASCII phân hoạch không gian trạng thái thể hiện cấu trúc hình học chuẩn:
  ```
  ALL STATES
  ├── SAFE
  └── UNSAFE
      └── DEADLOCK
  ```
- Hai miền Safe State và Unsafe State là hai khối hộp anh em rời nhau hoàn toàn ($\text{Safe} \cap \text{Unsafe} = \emptyset$).
- Miền Deadlock State nằm gọn hoàn toàn bên trong hộp Unsafe State ($\text{Deadlock} \subset \text{Unsafe}$).
- Tuyệt đối không còn tình trạng `SAFE STATE` bị vẽ lọt bên trong hộp `UNSAFE STATE`.
- Hộp lưu ý `> [!IMPORTANT]` xác nhận đầy đủ 5 mệnh đề nền tảng: Safe và Unsafe rời nhau; Safe suy ra không có Deadlock; Deadlock là tập con thực sự của Unsafe; Unsafe không đồng nghĩa với Deadlock; Bản chất của Avoidance là duy trì trạng thái luôn ở Safe.

### 2. `ACAD-CH6-004 — RECHECK PASS`
- **Kiểm tra liên kết điều hướng:** Cuối tệp `content/theory/ch06-deadlock.md` sử dụng chính xác liên kết tương đối chuẩn sạch `../questions/subjective/ch06.md`.
- **Phân giải HTML:** Bộ sinh web biên dịch thành công liên kết `<a href="../questions/subjective/ch06.html">Ngân hàng Câu hỏi Tự luận &amp; Bài tập Chương 6</a>`. Trang đích `public/site/questions/subjective/ch06.html` tồn tại thực tế và liên kết TOC phân giải hoàn hảo (0 dead links).

### 3. `ACAD-CH6-005 — RECHECK PASS`
- **Kiểm tra tuyên bố thời gian vô điều kiện:** Đã thẩm tra kỹ lưỡng toàn văn vùng SAFE STATE trong sơ đồ ASCII và đoạn văn giải thích đi kèm trong §6.5.1.
- Không còn bất kỳ cụm từ tuyên bố thời gian vô điều kiện thái quá nào như `100% KHÔNG BAO GIỜ xảy ra bế tắc`, `never deadlocks`, hay `deadlock can never occur`.
- Nội dung vùng Safe được định nghĩa chính xác:
  - Tồn tại ít nhất một chuỗi an toàn: $\langle P_1, P_2, \dots, P_n \rangle$.
  - Trạng thái hiện tại không bế tắc và có thứ tự cấp phát bảo đảm mọi tiến trình đều có thể hoàn tất theo nhu cầu tối đa.
  - Hộp lưu ý nhấn mạnh rõ ràng: Trạng thái hiện tại an toàn không bảo đảm hệ thống vĩnh viễn không bế tắc nếu các cấp phát tiếp theo trong tương lai không được kiểm soát; việc tránh bế tắc phụ thuộc vào việc chính sách Avoidance liên tục từ chối các yêu cầu đưa hệ thống sang Unsafe.

### 4. `ENG-CH6-007 — RECHECK PASS`
- **Kiểm tra vệ sinh mã nguồn công khai (Public Hygiene):** Kiểm tra toàn bộ 148 tệp được quản lý bởi git.
- Báo cáo thẩm định không chứa bất kỳ đường dẫn máy trạm tuyệt đối nào (zero local workstation absolute paths). Toàn bộ đã được chuẩn hóa bằng ký hiệu corpus di động `<verified-ch6-source-corpus>`.
- `python scripts/check_public_hygiene.py` đạt kết quả: `PUBLIC HYGIENE AUDIT PASS: Zero local paths or AI tool paths leaked.`

### 5. `VALIDATOR-CH6-002 — RECHECK PASS`
- **Kiểm tra bộ giám sát tự động:** `scripts/validate_ch06_content.py` đã tích hợp thành công rào chắn ngữ nghĩa `VALIDATOR-CH6-002`:
  - Khoanh vùng cục bộ đúng phạm vi Section 6.5.1, không gây ảnh hưởng sai lệch đến các mục khác (như Prevention).
  - Tự động từ chối mọi cụm từ thời gian thái quá trong ngữ cảnh Safe State.
  - Kiểm tra bắt buộc sự hiện diện của định nghĩa chuỗi an toàn và tính liên tục của giải thuật tránh bế tắc.
  - Kiểm thử âm bản (negative mutation test) đã chứng minh validator phát hiện và chặn đứng vi phạm với exit code `1`.

---

## 14. FINAL RECHECK DECISION

$$\mathbf{CH6\ ACADEMIC\ VERIFICATION:\ PASS\ —\ READY\ FOR\ LIFECYCLE\ CLOSEOUT}$$

- **TỔNG KẾT VẤN ĐỀ TỒN ĐỌNG:**
  - **OPEN BLOCKERS:** 0
  - **OPEN MAJORS:** 0
  - **OPEN MINORS:** 0
- **Trạng thái vòng đời nội dung (Content Lifecycle):** `CONTENT_DRAFTED` (Giữ nguyên theo quy trình, không tự ý nâng cấp trong phiên review).
- **Chapter 6 Source Mapping:** `VERIFIED`
- **Chapter 6 Authoring:** `CONTENT_DRAFTED`
- **Xác minh học thuật (Academic Verification):** `PASS — BATCH 1 + CH5 + CH6 REVIEW`
- **Xác minh kỹ thuật (Engineering Verification):** `PASS — CH5 + CH6`
- **Hành động tiếp theo chính xác (Exact Next Action):** Independent lifecycle closeout from CONTENT_DRAFTED to CONTENT_VERIFIED.

---

## 15. LIFECYCLE CLOSEOUT (Thực Hiện Cơ Chế Bởi Terra)

- **Academic review:** PASS (Thực hiện độc lập bởi Codex Luna Ultra)
- **Focused independent recheck:** PASS (Thực hiện độc lập bởi Codex Luna Ultra)
- **Lifecycle promotion (Chuyển đổi trạng thái vòng đời có cấu trúc):**
  - 63 / 63 Ch6 CONTENT slide pages: `CONTENT_DRAFTED -> CONTENT_VERIFIED`
  - 4 / 4 Ch6 NON_CONTENT slide pages: `NOT_WRITTEN` (Bảo toàn nguyên vẹn, không nâng cấp tùy tiện)
  - 15 / 15 Ch6 QBank units: `CONTENT_DRAFTED -> CONTENT_VERIFIED`
- **Open findings:**
  - Open blockers: 0
  - Open majors: 0
  - Open minors: 0
- **Trạng thái vòng đời khóa học thuật (Authoring):** `CONTENT_VERIFIED`
- **Giai đoạn dự án (Project Phase):** `V2_BATCH3_CH6_CONTENT_VERIFIED_LOCKED`

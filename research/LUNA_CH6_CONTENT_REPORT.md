# LUNA CH6 CONTENT DRAFTING AUDIT REPORT

**Báo cáo soạn thảo & Xác thực nội dung Chương 6: Bế tắc (Deadlock)**  
**Mô hình thực hiện:** Codex Luna Ultra  
**Thời gian thực hiện:** 2026-09-03  
**Nhánh Git:** `v2/complete-theory-labs`  

---

## 1. Starting Head
- **Starting Remote Commit:** `8dc47b3f679d67f0daecf61e56795ee107fab355`
- **Locked Base Checkpoint:** `06e4b34ef14d60398e462e437470bb6a37157996` (Chapters 1–5 locked baseline).

---

## 2. Files Created / Modified

### Tệp tạo mới (Created Files):
1. `content/theory/ch06-deadlock.md`:
   - Soạn thảo toàn diện lý thuyết Chương 6 bám sát Đề cương môn học 2024 (`UIT-OUTLINE-2024`) và bao phủ đầy đủ 63 trang nội dung (`UIT-SLIDE-CH06-2024`).
2. `content/questions/subjective/ch06.md`:
   - Soạn thảo ngân hàng 15 đơn vị câu hỏi tự luận và bài tập thực hành từ Ngân hàng đề chính thống (`UIT-QBANK-CH06-2024`), kèm barem điểm chi tiết và lời giải thuật toán chuẩn mực.
3. `scripts/validate_ch06_content.py`:
   - Bộ kiểm tra tự động các ràng buộc học thuật và tính toàn vẹn của nội dung Chương 6 (Coffman, RAG, Banker, Detection, Recovery, phân biệt Request/Need, chống rò rỉ biến thể sinh viên).

### Tệp cập nhật (Modified Files):
1. `PROJECT_STATE.md`:
   - Cập nhật giai đoạn `V2_BATCH3_CH6_CONTENT_DRAFTED_READY_FOR_ENGINEERING_QA`, trạng thái soạn thảo `CONTENT_DRAFTED`.
2. `research/data/slide_coverage.yaml`:
   - Cập nhật 19 mục nội dung (63 trang) của `UIT-SLIDE-CH06-2024` từ `NOT_WRITTEN` sang `CONTENT_DRAFTED`.
   - Giữ nguyên 4 trang phi nội dung (trang 1–3 và trang 67) ở trạng thái `NOT_WRITTEN`.
3. `research/data/official_review_questions.yaml`:
   - Cập nhật toàn bộ 15 câu hỏi (`QBANK-CH06-01` đến `QBANK-CH06-15`) từ `NOT_WRITTEN` sang `CONTENT_DRAFTED`.
4. `scripts/generate_foundation_gate.py`:
   - Đăng ký `validate_ch06_content` vào chuỗi 14 bước kiểm tra cổng nền tảng V2.
5. `scripts/validate_ch06_source_map.py`:
   - Cập nhật kiểm tra trạng thái vòng đời hỗ trợ `CONTENT_DRAFTED` và xác thực liên kết nguồn khi file đã được soạn thảo.
6. `scripts/run_negative_tests.py` & `scripts/verify_research_gates.py`:
   - Tăng cường `encoding="utf-8", errors="replace"` cho các lệnh gọi `subprocess.run` nhằm đảm bảo tính tương thích và ổn định tuyệt đối trên Windows.
7. `research/V2_FOUNDATION_GATE.md` & `research/RESEARCH_GATE_QA.md`:
   - Tự động cập nhật báo cáo nghiệm thu 14/14 cổng kiểm tra nền tảng (`PASS`).

---

## 3. Source Coverage (Bao Phủ Nguồn Căn Cứ)

### A. Đề cương chi tiết môn học (`UIT-OUTLINE-2024`):
- Tệp: `IT007_HeDieuHanh_14.2024.pdf` (19 trang, SHA-256 `89547bca...`).
- Cấu trúc chương tuân thủ chuẩn mực:
  - 6.1 Định nghĩa
  - 6.2 Mô hình hệ thống
  - 6.3 Phương pháp giải quyết deadlock (6.3.1 Prevention, 6.3.2 Avoidance, 6.3.3 Detection, 6.3.4 Recovery)
  - 6.4 Bài tập

### B. Bài giảng chính thống (`UIT-SLIDE-CH06-2024`):
- Tệp: `#Week08-Chapter6 2024.pdf` (67 trang vật lý, SHA-256 `5cf9e1a3...`).
- Phân loại trang:
  - **Trang nội dung (CONTENT):** 63 trang (từ trang 4 đến trang 66) $\to$ Đã biên soạn đầy đủ 100% (`CONTENT_DRAFTED`).
  - **Trang phi nội dung (NON_CONTENT):** 4 trang (trang 1–3 bìa/mục tiêu và trang 67 thảo luận/kết thúc) $\to$ Giữ nguyên không soạn thảo (`NOT_WRITTEN`).
- Không sử dụng tệp biến thể `Week11-Chapter6 2024.pdf` làm chuẩn chính thống.

### C. Ngân hàng câu hỏi gốc (`UIT-QBANK-CH06-2024`):
- Tệp: `Bai tap chuong 6 HDH.docx` (101,550 bytes, SHA-256 `f8f82cc2...`).
- Đã ánh xạ và biên soạn đủ 15 đơn vị câu hỏi: 8 câu lý thuyết + 7 bài tập định lượng.
- Các tài liệu sinh viên (`Bai-tap-chuong-6-HDH.docx`, `23521551 PDF`) được phân loại Tier B/tham khảo, tuyệt đối không đưa vào quyền hạn Tier A.

---

## 4. Theory Coverage (Nội Dung Lý Thuyết Chi Tiết)

Nội dung lý thuyết tại `content/theory/ch06-deadlock.md` được triển khai sâu sắc theo phương pháp sư phạm: **Trực giác $\to$ Quy tắc hình thức $\to$ Biểu diễn trạng thái $\to$ Lần vết thuật toán $\to$ Lỗi phổ biến $\to$ Kinh nghiệm thi cử**:

1. **Khởi nguyên & Ví dụ Semaphore xen kẽ (pp. 4–7):**
   - Phân tích chi tiết kịch bản tranh chấp giữa $P_0$ và $P_1$ trên hai semaphore $S, Q$ dẫn đến bế tắc chéo.
2. **Định nghĩa Deadlock & Trì hoãn vô hạn định (pp. 8–9):**
   - Định nghĩa hình thức về tập tiến trình bị chặn chờ sự kiện tương hỗ; phân biệt rõ Deadlock với Starvation / Indefinite Postponement.
3. **4 điều kiện cần Coffman (pp. 10–12):**
   - Loại trừ lẫn nhau (Mutual Exclusion), Giữ và chờ (Hold and Wait), Không lưu quyền (No Preemption), Chờ đợi vòng tròn (Circular Wait).
   - Nhấn mạnh nguyên lý bất biến: 4 điều kiện là **ĐIỀU KIỆN CẦN**, không phải luôn luôn là điều kiện đủ trong hệ đa thực thể.
4. **Mô hình hóa hệ thống & Đồ thị cấp phát tài nguyên RAG (pp. 13–24):**
   - Định nghĩa đỉnh ($P, R$) và cạnh (Request edge $P \to R$, Assignment edge $R \to P$).
   - Minh họa trực quan trường hợp RAG có chu trình gây Deadlock và trường hợp RAG có chu trình nhưng **KHÔNG BỊ DEADLOCK**.
   - Định lý cốt lõi: Đơn thực thể $\iff$ chu trình tương đương deadlock; Đa thực thể $\implies$ chu trình chỉ là điều kiện cần.
5. **Bốn chiến lược xử lý bế tắc (pp. 25–26):**
   - Prevention, Avoidance, Detection & Recovery, và Ostrich Algorithm.
6. **Ngăn chặn bế tắc (Deadlock Prevention) (pp. 27–31):**
   - Phân tích kỹ thuật phá vỡ từng điều kiện Coffman; cơ chế đánh chỉ số tài nguyên toàn cục $F: R \to \mathbb{N}$ triệt tiêu Circular Wait.
7. **Tránh bế tắc (Deadlock Avoidance) & Trạng thái An toàn (pp. 32–40):**
   - Yêu cầu thông tin tiên nghiệm `Max`.
   - Định nghĩa hình thức Safe State và Chuỗi an toàn (Safe Sequence).
   - Biểu đồ mối quan hệ: Safe $\implies$ No Deadlock, Deadlock $\subset$ Unsafe, Unsafe $\not\implies$ Deadlock.
8. **Giải thuật Banker toàn diện (pp. 41–49):**
   - Cấu trúc: `Available`, `Max`, `Allocation`, `Need = Max - Allocation`.
   - Giải thuật An toàn (Safety Algorithm): `Work`, `Finish`, lần vết step-by-step.
   - Giải thuật Yêu cầu tài nguyên (Resource-Request Algorithm): 2 bước kiểm tra $\le \text{Need}$ và $\le \text{Available}$, giả lập cấp phát, chạy Safety, quyết định cấp phát hay rollback.
9. **Phát hiện bế tắc (Deadlock Detection) (pp. 50–58):**
   - Hệ đơn thực thể: Đồ thị Đợi (Wait-For Graph) và chu trình $O(n^2)$.
   - Hệ đa thực thể: Giải thuật ma trận phát hiện Deadlock.
   - Phân biệt cốt tử: Banker dùng `Need` (tương lai có thể đòi), Detection dùng `Request` (thực tế đang đòi).
10. **Phục hồi sau bế tắc (Deadlock Recovery) (pp. 59–62):**
    - Hủy tiến trình (hủy toàn bộ vs hủy từng tiến trình, tiêu chí chọn nạn nhân).
    - Cưỡng bức thu hồi tài nguyên (chọn victim, rollback trạng thái về checkpoint, chống starvation bằng aging).
11. **Tổng kết & Bảng đối sánh (pp. 63–66):**
    - Bảng ma trận so sánh chi tiết cơ chế, yêu cầu thông tin, hiệu suất và chi phí tính toán.

---

## 5. QBank 15/15 Coverage

| Mã câu | Loại | Vị trí gốc | Chủ đề chính | Kết quả giải thuật & Trạng thái |
|:---|:---:|:---|:---|:---|
| `QBANK-CH06-01` | Lý thuyết | Câu 1 / Mục 6 | Định nghĩa Deadlock | Định nghĩa chuẩn mực, điều kiện hình thức |
| `QBANK-CH06-02` | Lý thuyết | Câu 2 / Mục 6 | 4 điều kiện Coffman | 4 điều kiện cần, cơ chế hoạt động |
| `QBANK-CH06-03` | Lý thuyết | Câu 3 / Mục 6 | Đồ thị RAG & Deadlock | Đỉnh, cạnh, định lý chu trình đơn/đa thực thể |
| `QBANK-CH06-04` | Lý thuyết | Câu 4 / Mục 6 | 4 phương pháp giải quyết | Ma trận ưu nhược điểm: Prevention/Avoidance/Detection/Ostrich |
| `QBANK-CH06-05` | Lý thuyết | Câu 5 / Mục 6 | Đồng bộ Busy-waiting | Phần cứng (nguyên tử) vs phần mềm, liên hệ Ch5 |
| `QBANK-CH06-06` | Lý thuyết | Câu 6 / Mục 6 | Safe State & Deadlock | Safe sequence, không gian trạng thái Safe/Unsafe/Deadlock |
| `QBANK-CH06-07` | Lý thuyết | Câu 7 / Mục 6 | Bộ ba giải thuật Banker | Safety, Resource-Request, Detection (Request vs Need) |
| `QBANK-CH06-08` | Lý thuyết | Câu 8 / Mục 6 | Phục hồi sau Deadlock | Termination, Preemption, Rollback, Starvation |
| `QBANK-CH06-09` | Bài tập 1 | Bài tập 1 / Mục 6 | Đồ thị mẫu (a) và (b) | (a) Không deadlock ($\langle P_2, P_1, P_3 \rangle$); (b) Deadlock |
| `QBANK-CH06-10` | Bài tập 2 | Bài tập 2 / Mục 6 | Vẽ RAG hệ 4 tiến trình | Không deadlock, chuỗi: $\langle P_4, P_2, P_1, P_3 \rangle$ |
| `QBANK-CH06-11` | Bài tập 3 | Bài tập 3 / Mục 6 | Đếm chuỗi an toàn hệ 5 tiến trình | Đúng chính xác 24 chuỗi an toàn, liệt kê chi tiết |
| `QBANK-CH06-12` | Bài tập 4 | Bài tập 4 / Mục 6 | Banker mẫu & Request $P_1(0,4,2,0)$ | An toàn tại $t_0$ ($\langle P_0, P_2, P_3, P_4, P_1 \rangle$); Chấp thuận cấp phát cho $P_1$ |
| `QBANK-CH06-13` | Bài tập 5 | Bài tập 5 / Mục 6 | Banker & Request $P_3(1,1,0,0)$ | $t_0$ an toàn ($\langle P_1, P_4, P_5, P_2, P_3 \rangle$); $t_1$ Unsafe $\implies$ Từ chối $P_3$ |
| `QBANK-CH06-14` | Bài tập 6 | Bài tập 6 / Mục 6 | Banker với 2 vector Available | (a) $(0,3,0,1) \implies$ Unsafe (thiếu $D$); (b) $(1,0,0,2) \implies$ Safe ($\langle P_1, P_2, P_0, P_3, P_4 \rangle$) |
| `QBANK-CH06-15` | Bài tập 7 | Bài tập 7 / Mục 6 | Banker toàn diện: $P_1$ & $P_4$ | Safe tại $t_0$ ($\langle P_0, P_3, P_1, P_2, P_4 \rangle$); Cấp phát $P_1(1,1,0,0)$; Từ chối $P_4(0,0,2,0)$ vì $C=0$ |

---

## 6. Algorithm Trace Checks (Kiểm Tra Lần Vết Giải Thuật)

Tất cả các bài tập định lượng đã được lần vết độc lập bằng mã nguồn Python trước khi soạn thảo, đảm bảo không có sai số:

### Bài tập 2 (`QBANK-CH06-10`):
- $\text{Available} = (3 - 2, 2 - 2, 2 - 2) = (1, 0, 0)$.
- Với $(1, 0, 0)$, chỉ $P_4$ thỏa mãn $\text{Request} \le \text{Available}$.
- $P_4$ hoàn tất $\to \text{Work} = (1, 0, 2) \to P_2$ chạy $\to \text{Work} = (1, 2, 2) \to P_1, P_3$ chạy.
- Chuỗi an toàn: $\langle P_4, P_2, P_1, P_3 \rangle$ hoặc $\langle P_4, P_2, P_3, P_1 \rangle$.

### Bài tập 3 (`QBANK-CH06-11`):
- $\text{Available} = (3 - 2, 3 - 3, 2 - 2) = (1, 0, 0)$.
- Hai ứng viên đầu tiên: $P_4$ hoặc $P_5$.
- Bằng thuật toán quay lui (backtracking), toàn bộ cây trạng thái sinh ra **đúng 24 chuỗi an toàn** (12 chuỗi bắt đầu bằng $P_4$, 12 chuỗi bắt đầu bằng $P_5$).

### Bài tập 5 (`QBANK-CH06-13`):
- Nhu cầu P3 sau yêu cầu: $\text{Need}'(P_3) = (5, 5, 2, 2)$.
- $\text{Available}' = (1, 0, 2, 0)$.
- Lần vết: $P_1$ chạy $\to \text{Work} = (1, 0, 3, 2) \to P_4$ chạy $\to \text{Work} = (3, 3, 8, 6) \to P_5$ chạy $\to \text{Work} = (3, 6, 11, 8)$.
- Đến đây, $P_2$ cần $R_2 = 7 > 6$, và $P_3$ cần $R_1 = 5 > 3$. Cả hai đều kẹt. Trạng thái Unsafe $\implies$ Khẳng định từ chối cấp phát là chuẩn xác 100%.

### Bài tập 6 (`QBANK-CH06-14`):
- Câu a: Với $(0, 3, 0, 1)$, sau khi $P_2, P_1, P_3$ chạy, $\text{Work} = (5, 11, 4, 2)$. Cả $P_0$ và $P_4$ đều cần $D = 3 > 2$. Cả hai kẹt cứng $\implies$ Unsafe.
- Câu b: Với $(1, 0, 0, 2)$, chuỗi an toàn $\langle P_1, P_2, P_0, P_3, P_4 \rangle$ giúp $\text{Work}$ tăng dần đến $(13, 10, 6, 9) \implies$ Safe.

### Bài tập 7 (`QBANK-CH06-15`):
- Câu c: Khi P4 yêu cầu $(0, 0, 2, 0)$, $\text{Available}'$ có $C = 0$. Mọi tiến trình đều cần ít nhất 1 thực thể $C$. Hệ thống tắc nghẽn ngay lập tức tại bước đầu tiên $\implies$ Unsafe.

---

## 7. Numerical Exercise Checks (Bảo Vệ Tính Toán)
- Không có hiện tượng sao chép mù quáng đáp án bài làm sinh viên.
- Tất cả ma trận `Need` đều được tính theo công thức chính xác $\text{Max} - \text{Allocation}$.
- Tổng tài nguyên hệ thống và vector `Available` ban đầu đều khớp đúng với tổng cấp phát.

---

## 8. Tier-B Technical Notes (Ghi Chú Kỹ Thuật)
- Về thuật toán Peterson trên kiến trúc CPU hiện đại: Đã bổ sung ghi chú kỹ thuật về việc CPU hiện đại hỗ trợ out-of-order execution và caching dẫn đến việc cần lệnh phần cứng `Memory Barrier` để giải pháp phần mềm hoạt động đúng.
- Về tính chất của Unsafe State: Nhấn mạnh rõ Unsafe không nhất thiết là Deadlock để tránh quan niệm sai lầm phổ biến của sinh viên trong kỳ thi trắc nghiệm và tự luận.

---

## 9. Findings & Semantic Hotfix Record

### ACAD-CH6-001 — MAJOR — OPEN -> RESOLVED
- **Vấn đề:** Trong lời giải bài tập Banker (QBANK-CH06-13, 14, 15c), trạng thái Unsafe khi giải thuật An toàn không tìm ra chuỗi an toàn bị đánh đồng không chính xác với việc các tiến trình bị bế tắc ngay lập tức hoặc bị chặn vĩnh viễn.
- **Khắc phục:** Loại bỏ hoàn toàn các nhận định sai lệch ("bế tắc ngay lập tức", "chứng minh bế tắc", "bị chặn vĩnh viễn"). Bổ sung phân tích và lưu ý học thuật chuẩn xác: Ma trận Need chỉ đại diện cho nhu cầu tiềm năng tối đa, không phải yêu cầu Request thực tế đang bị chặn; việc không tìm ra chuỗi an toàn chỉ chứng minh trạng thái là Unsafe (tiềm ẩn nguy cơ bế tắc nên Banker phải từ chối cấp phát), chứ không chứng minh hệ thống hiện tại đã bị Deadlock.

### ACAD-CH6-002 — MAJOR — OPEN -> RESOLVED
- **Vấn đề:** Trong QBANK-CH06-02, 4 điều kiện Coffman bị phát biểu theo mệnh đề tương đương "khi và chỉ khi" (iff), vi phạm nguyên lý học thuật vì 4 điều kiện Coffman chỉ là điều kiện cần (necessary conditions), không phải điều kiện đủ đối với tài nguyên đa thực thể.
- **Khắc phục:** Loại bỏ hoàn toàn cụm từ "khi và chỉ khi". Hiệu chỉnh lời giải chuẩn mực: Bế tắc chỉ có thể xảy ra khi đồng thời tồn tại cả 4 điều kiện cần (nếu bế tắc xảy ra thì cả 4 điều kiện bắt buộc đồng thời xuất hiện; nhưng sự hiện diện của 4 điều kiện chưa đủ để khẳng định hệ thống đa thực thể đã bị bế tắc).

### PROV-CH6-001 — MAJOR — OPEN -> RESOLVED
- **Vấn đề:** Bản nháp QBank sử dụng tiêu đề "Barem điểm & Tiêu chí chấm thi" và các mức điểm số cụ thể ("0.25 đ", "0.50 đ", v.v.), vô tình tạo cảm tưởng đây là barem chấm điểm chính thức của UIT dù chưa có tài liệu nguồn chứng minh.
- **Khắc phục:** Chuẩn hóa toàn bộ 15 đơn vị câu hỏi sang định dạng trung lập "Rubric tự kiểm tra của handbook (Self-Check Rubric)", kèm khuyến cáo rõ ràng: *(Trọng số gợi ý của handbook nhằm phục vụ tự đánh giá ôn tập — không phải barem chấm thi chính thức của UIT)*. Chuyển đổi các điểm số tuyệt đối sang tỷ lệ phần trăm gợi ý (Gợi ý: 25%, 50%...).

### VALIDATOR-CH6-001 — MAJOR — OPEN -> RESOLVED
- **Vấn đề:** Bộ kiểm tra `validate_ch06_content.py` chỉ quét từ khóa chung trong file lý thuyết mà không phát hiện được sự mâu thuẫn ngữ nghĩa trong các bài tập QBank hoặc việc gán ghép barem điểm chính thức.
- **Khắc phục:** Tăng cường bộ kiểm tra `scripts/validate_ch06_content.py` với các hàm kiểm tra ngữ nghĩa theo phạm vi từng câu hỏi (section-scoped guards cho QBANK-CH06-02, 13, 14, 15), loại trừ các cụm từ bế tắc sai lệch, bắt buộc sự hiện diện của phân biệt học thuật Unsafe vs Deadlock, và kiểm tra tính toàn vẹn nguồn gốc (Provenance Guard).

- **OPEN BLOCKERS:** `0`
- **OPEN MAJORS:** `0`
- **OPEN MINORS:** `0`

---

## 10. Validation Results (Kết Quả Kiểm Thử Hệ Thống)

### A. Kiểm tra cổng cục bộ:
1. `scripts/generate_registry.py --check`: **PASS** (72 nguồn SSOT nguyên vẹn).
2. `scripts/validate_sources.py`: **PASS** (60 trích dẫn nội dung hợp lệ).
3. `scripts/validate_ch06_source_map.py`: **PASS** (cả chế độ CI và Evidence Mode).
4. `scripts/validate_ch06_content.py`: **PASS** (đáp ứng toàn bộ 10 ràng buộc học thuật).
5. `scripts/validate_ch05_source_map.py`: **PASS**.
6. `scripts/validate_ch05_content.py`: **PASS**.
7. `scripts/validate_batch1_canonical.py`: **PASS**.
8. `scripts/check_batch1_numeric.py`: **PASS**.
9. `scripts/stress_test_web_renderer.py`: **PASS**.
10. `scripts/check_public_hygiene.py`: **PASS** (139 tệp sạch, 0 đường dẫn cục bộ).

### B. Kiểm tra cổng nền tảng V2 (`npm test`):
- **14/14 cổng PASS:**
  - `validate_sources`: PASS
  - `check_public_hygiene`: PASS
  - `validate_v2_content`: PASS
  - `build_web`: PASS
  - `validate_site_routes`: PASS
  - `validate_web_features`: PASS
  - `renderer_stress_test`: PASS
  - `negative_tests`: PASS
  - `batch1_canonical_source`: PASS
  - `validate_ch05_source_map`: PASS
  - `validate_ch05_content`: PASS
  - `validate_ch06_source_map`: PASS
  - `validate_ch06_content`: PASS
  - `verify_research_gates`: PASS
- **Foundation Gate Decision:** **PASS**

### C. Biên dịch Web tĩnh (`npm run web:build`):
- Biên dịch thành công **18 trang tĩnh** vào `public/site`.
- Đã xuất bản đầy đủ tuyến:
  - `theory/ch06-deadlock/index.html`
  - `questions/subjective/ch06/index.html`

---

## 11. Final Decision

**QUYẾT ĐỊNH NGHIỆM THU ĐỢT SOẠN THẢO:**
$$\mathbf{CH6\ CONTENT\ DRAFTED\ —\ READY\ FOR\ ENGINEERING\ QA\ AND\ INDEPENDENT\ ACADEMIC\ REVIEW}$$

*(Tuyệt đối không đánh dấu `CONTENT_VERIFIED` tại bước này. Toàn bộ nội dung giữ nguyên trạng thái `CONTENT_DRAFTED` chờ bước thẩm định học thuật độc lập tiếp theo).*

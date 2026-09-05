# BÁO CÁO THẨM ĐỊNH KỸ THUẬT & SỬA LỖI RENDERING CHƯƠNG 7 (HDH_UIT V2)
# CHAPTER 7 ENGINEERING QA & RENDERING REPAIR CLOSEOUT REPORT

- **Dự án:** CẨM NANG HỆ ĐIỀU HÀNH — IT007 UIT (V2 TRIPLE-PRODUCT EXPANSION)
- **Nhánh Git:** `v2/complete-theory-labs`
- **Vai trò thẩm định:** Engineering QA (Static-site / Validator / Runtime / Numerical QA)
- **Thời gian thẩm định:** 2026-09-05
- **Trạng thái thẩm định:** `ENGINEERING_QA_PASS — READY FOR INDEPENDENT ACADEMIC/SOURCE-FIDELITY REVIEW`

---

## 1. TỔNG QUAN KẾT QUẢ THẨM ĐỊNH (EXECUTIVE SUMMARY)

Đợt thẩm định kỹ thuật cho Chương 7 (Quản lý Bộ nhớ - Memory Management) đã xử lý dứt điểm toàn bộ các khiếm khuyết hiển thị, mã hoá, ràng buộc trường lời giải, triệt tiêu trôi dạt dữ liệu tổng hợp và hoàn tất phạm vi kiểm thử tất định (coverage closeout). Toàn bộ 17 cổng nền tảng (Foundation Gates), 17/17 ca kiểm thử phủ định (Negative Mutation Tests), và 14/14 kịch bản kiểm thử trình duyệt Playwright đều đạt trạng thái **PASS tuyệt đối**.

| Mã định danh | Phân loại | Trọng yếu | Trạng thái | Mô tả khắc phục |
|---|---|---|---|---|
| **ENG-CH7-001** | Markup / Parser | MAJOR | **RESOLVED** | Loại bỏ dòng rò rỉ `> -->` trong 6 khối `RecallCheckpoint`, làm sạch và củng cố parser `build_web.py` triệt tiêu mục rubric ma `-> (0.5đ)`, đưa tổng trọng số rubric về chuẩn 1.0 (100%). |
| **ENG-CH7-002** | Markup / Parser | MAJOR | **RESOLVED** | Loại bỏ rò rỉ `> -->` cuối lời giải trong 2 khối `TransferProblem`, củng cố parser loại bỏ ký tự đóng comment khỏi nội dung hiển thị web. |
| **DOC-CH7-001** | Encoding / Hygiene | MAJOR | **RESOLVED** | Khử sạch 29 ký tự điều khiển C0 (25 ký tự `U+0007` BEL và 4 ký tự `U+000C` FF) trong `content/questions/subjective/ch07.md`. Bổ sung chốt kiểm soát C0 cưỡng chế trong `scripts/check_public_hygiene.py`. |
| **DATA-CH7-001** | Data Consistency | MAJOR | **RESOLVED** | Đồng bộ số liệu tổng hợp trong `research/data/official_review_questions.yaml` (81 verified + 20 drafted + 17 not_written = 118) và `research/data/slide_coverage.yaml` (568 drafted + 96 not_written = 664 trang nội dung). |
| **QA-CH7-001** | Validator | MAJOR | **RESOLVED** | Xây dựng công cụ kiểm tra tất định `scripts/validate_ch07_content.py` bao quát cấu trúc, quy tắc rubric và tính toán lại độc lập toàn bộ 13 bài toán định lượng kinh điển. |
| **QA-CH7-002** | Browser Testing | MAJOR | **RESOLVED** | Bổ sung Scenario 13 trong `tests/learning-system.spec.js` kiểm thử trực tiếp trên trang `/theory/ch07-memory-management.html`: không lỗi console/layout, M2/M3 tương tác thực tế, và study_index.json đủ 8 mục Ch7. |
| **VAL-CH7-001** | Validator Text | MINOR | **RESOLVED** | Cập nhật docstring và thông điệp đầu ra của `scripts/validate_ch07_source_map.py` phù hợp với vòng đời dự án mà không làm suy yếu kiểm tra định danh nguồn. |
| **QA-CH7-003** | Numerical Invariants | MAJOR | **RESOLVED** | Hoàn thiện phủ định lượng: Q10 kiểm tra chính xác thứ tự cấp phát và mảng lỗ trống còn lại cho cả 4 thuật toán; Q14 kiểm tra đẳng thức biểu tượng $2^{a+b+c} = 2^{32-d}$; Q20 kiểm tra đồng thời độ rộng trường frame (6 bit) và số mục bảng trang (45 mục). |
| **QA-CH7-004** | Content Binding | MAJOR | **RESOLVED** | Ràng buộc trực tiếp các tham số nguồn và kết quả tính toán Q10..Q20 vào văn bản Markdown; bổ sung kiểm thử đột biến bắt buộc phát hiện sai lệch số liệu. |
| **QA-CH7-005** | Per-Unit Schema | MAJOR | **RESOLVED** | Phân đoạn QBank theo từng đơn vị câu hỏi `^### QBANK-CH07-XX:`, kiểm tra độc lập cấu trúc 4 phần chuẩn mực cho từng câu hỏi riêng biệt; kiểm thử đột biến loại bỏ phân đoạn bị chặn ngay lập tức. |
| **QA-CH7-006** | Browser Test Fidelity| MAJOR | **RESOLVED** | Chuyển đổi kiểm thử Chế độ Tra cứu (Reference Mode) trong Scenario 13 sang bộ chọn chuẩn `button[data-mode="reference"]`, kiểm tra không điều kiện và xác nhận hiển thị toàn diện không cần tương tác đánh giá. |
| **QA-CH7-007** | Mobile Usability | MAJOR | **RESOLVED** | Bổ sung Scenario 14 trong `tests/learning-system.spec.js` kiểm thử thực tế trên viewport di động 390x844 cho cả trang lý thuyết `/theory/ch07-memory-management.html` và bài tập tự luận `/questions/subjective/ch07.html`. |
| **QA-CH7-008** | Solution-Field Binding| MAJOR | **RESOLVED** | Tách cấu trúc mỗi đơn vị QBank thành 4 trường riêng biệt (`source_question`, `solution`, `rubric`, `exam_traps`). Toàn bộ kết quả tính toán định lượng được kiểm tra cưỡng chế trong trường `solution`, ngăn chặn triệt để rubric/đề bài che lấp sai sót; chuyển đổi kiểm thử phủ định sang đột biến cục bộ từng trường (Q15 phương trình 9398->9999, Q18 phương trình 75.2%->57.2%, Q20 câu giải 45 mục->64 mục, Q16 kết quả EAT 164.2->146.2). |
| **DATA-V2-001** | Summary Drift | MAJOR | **RESOLVED** | Đồng bộ triệt để khối `summary:` trong `research/data/slide_coverage.yaml` theo số liệu thực tế từ bản ghi deck (713 trang vật lý, 665 trang nội dung, 48 trang phi nội dung, 568 trang đã soạn, 97 trang chưa soạn); bổ sung cổng kiểm tra cưỡng chế trong `scripts/verify_research_gates.py` từ chối bất kỳ sự trôi dạt nào giữa summary và bản ghi chi tiết (NEG-17). |
| **STATE-V2-001** | State Consistency | MAJOR | **RESOLVED** | Loại bỏ các số liệu đếm biến động khỏi `PROJECT_STATE.md`, chuyển sang tham chiếu trực tiếp báo cáo tự động `research/RESEARCH_GATE_QA.md` do máy tính toán độc lập. |
| **PUB-CH7-001** | Neutral Reporting | MINOR | **RESOLVED** | Loại bỏ hoàn toàn định danh mô hình/agent khỏi báo cáo và trạng thái dự án, sử dụng chức danh vai trò kỹ thuật chuẩn mực. |

---

## 2. CHI TIẾT CÁC KHIẾM KHUYẾT VÀ GIẢI PHÁP KỸ THUẬT

### 2.1. Sửa lỗi Rubric Marker Bug (ENG-CH7-001) & Transfer Leak (ENG-CH7-002)
- **Nguyên nhân gốc rễ:** Cú pháp callout markdown trong bản thảo Ch7 ghi `> <!-- rubric -->` ở dòng mở đầu và để lại `> -->` ở dòng kết thúc. Parser tách chuỗi của `build_web.py` cắt ở thẻ `-->` đầu tiên, khiến dòng `> -->` ở cuối bị giữ lại. Khi duyệt từng dòng rubric, ký tự `-` của `-->` khiến dòng này bị hiểu lầm là một tiêu chí chấm điểm với trọng số mặc định `0.5`, nâng tổng điểm rubric từ 1.0 lên 1.5 và chặn đứng khả năng đạt chuẩn M2 (>=80%). Tương tự, khối lời giải `TransferProblem` bị rò rỉ ký tự `--&gt;` ở cuối.
- **Biện pháp khắc phục kép (Double-Layer Hardening):**
  1. *Lớp dữ liệu nguồn:* Loại bỏ triệt để toàn bộ 8 dòng `> -->` đứng độc lập trong `content/theory/ch07-memory-management.md`.
  2. *Lớp hiển thị / Trình phân tích:* Trong hàm `render_callout` của `scripts/build_web.py`:
     - Bổ sung bộ lọc loại trừ triệt để bất kỳ dòng nào chỉ chứa `-->`, `->`, `>`, hoặc chứa thẻ đóng HTML comment.
     - Cắt bỏ mọi ký tự `-->` hoặc `--&gt;` ở cuối lời giải của `TransferProblem`.
     - Xác thực lại toàn bộ 6 khối `RecallCheckpoint` (tổng trọng số = 1.0) và 2 khối `TransferProblem` (sạch sẽ 100%).

### 2.2. Khử Ký Tự Điều Khiển C0 & Cổng Bảo Vệ Mã Nguồn (DOC-CH7-001)
- **Nguyên nhân gốc rễ:** Khi tạo sinh nội dung toán học LaTeX từ Python script trong phiên trước, các chuỗi thoát `\alpha`, `\approx`, `\frac` bị diễn giải thành ký tự nhị phân:
  - `\a` -> `0x07` (BEL)
  - `\f` -> `0x0C` (Form Feed)
- **Biện pháp khắc phục:**
  1. Thay thế cơ học chính xác toàn bộ 25 vị trí `\x07lpha` -> `\alpha`, `\x07pprox` -> `\approx`, và 4 vị trí `\x0crac` -> `\frac` trong `content/questions/subjective/ch07.md`.
  2. Tích hợp thuật toán quét nhị phân cưỡng chế vào `scripts/check_public_hygiene.py`, phát hiện và từ chối mọi file mã nguồn/tài liệu chứa byte C0 (`0x00–0x08`, `0x0B`, `0x0C`, `0x0E–0x1F`, `0x7F`).

### 2.3. Ràng Buộc Kết Quả Tính Toán Vào Trường Lời Giải & Kiểm Thử Đột Biến Cục Bộ (QA-CH7-008)
- **Cơ chế phân tách trường:** Hàm `segment_qbank_units()` bóc tách mỗi câu hỏi thành cấu trúc từ điển có định danh trường tường minh:
  ```python
  units[qid] = {
      "source_question": ...,
      "solution": ...,
      "rubric": ...,
      "exam_traps": ...
  }
  ```
- **Ràng buộc trường lời giải:** Tất cả các kiểm tra kết quả tính toán định lượng (Q10..Q20) được chuyển sang kiểm tra trường `solution`. Trường `rubric` hoặc `source_question` tuyệt đối không thể thay thế hoặc che lấp một kết quả tính toán sai trong lời giải.
- **Kiểm thử đột biến cục bộ trường:**
  - `NEG-12`: Đột biến duy nhất phương trình Part B của Q15 (`8192 + 1206 = 9398` -> `8192 + 1206 = 9999`), giữ nguyên kết luận và rubric chứa `9398`. Validator bắt lỗi chính xác và từ chối.
  - `NEG-13`: Đột biến duy nhất phương trình trúng TLB của Q18 (`\alpha = 75.2\%` -> `\alpha = 57.2\%`), giữ nguyên rubric chứa `75.2%`. Validator bắt lỗi chính xác và từ chối.
  - `NEG-14`: Đột biến duy nhất kết luận số mục bảng trang của Q20 (`Bảng phân trang cần có tối thiểu **45 mục**` -> `**64 mục**`), giữ nguyên đề bài và rubric chứa `45`. Validator bắt lỗi chính xác và từ chối.
  - `NEG-16`: Đột biến duy nhất kết quả tính EAT của Q16 (`150.1 + 14.1 = 164.2` -> `146.2`), giữ nguyên rubric chứa `164.2`. Validator bắt lỗi chính xác và từ chối.

### 2.4. Triệt Tiêu Trôi Dạt Dữ Liệu Slide Coverage & Khóa Cổng Tự Động (DATA-V2-001, STATE-V2-001)
- **Đồng bộ hóa Slide Coverage:** Khối `summary:` trong `research/data/slide_coverage.yaml` được đồng bộ chính xác tuyệt đối với tổng hợp từ bản ghi:
  - 12 slide decks
  - 713 trang vật lý (665 trang nội dung, 48 trang phi nội dung)
  - 665 trang đã ánh xạ (0 trang chưa ánh xạ)
  - 568 trang nội dung đã biên soạn (Chapters 1–7)
  - 97 trang nội dung chưa biên soạn (Chapters 8–9: Ch8 có 45 trang, Ch9 có 52 trang)
- **Khóa cổng tự động:** Hàm `verify_gates()` trong `scripts/verify_research_gates.py` đối chiếu tự động toàn bộ 8 trường trong `summary:` với các giá trị tính toán được từ danh sách deck records. Mọi sự sai lệch dù chỉ 1 đơn vị sẽ kích hoạt lỗi `Slide coverage summary drift` và đánh rớt cổng (đã kiểm chứng qua ca kiểm thử đột biến `NEG-17`).
- **Làm sạch trạng thái dự án:** Loại bỏ toàn bộ các con số thống kê đếm thủ công dễ bị lỗi thời khỏi `PROJECT_STATE.md`, chuẩn hóa sang tham chiếu các báo cáo do máy kiểm toán độc lập (`research/RESEARCH_GATE_QA.md`).

---

## 3. TÁI TÍNH TOÁN ĐỘC LẬP & RÀNG BUỘC VĂN BẢN 13 BÀI TOÁN KINH ĐIỂN CHƯƠNG 7 (QA-CH7-001, QA-CH7-003, QA-CH7-008)

Toàn bộ 13 bài toán định lượng đã được tái tính toán độc lập và ràng buộc trực tiếp vào trường `solution` của Markdown:

1. **QBANK-CH07-10 (Chiến lược cấp phát bộ nhớ liên tục):**
   - Lỗ trống ban đầu: `[600, 500, 200, 300]` KB; Tiến trình: `[212, 417, 112, 426]` KB.
   - *First Fit:* Lỗ trung gian `388K`, lỗ cuối cùng `[276, 83, 200, 300]` KB; $P_4$ thất bại.
   - *Best Fit:* Lỗ cuối cùng `[174, 83, 88, 88]` KB; cả 4 tiến trình thành công 100%.
   - *Next Fit:* Lỗ cuối cùng `[388, 83, 88, 300]` KB; $P_4$ thất bại.
   - *Worst Fit:* Lỗ cuối cùng `[276, 83, 200, 300]` KB; $P_4$ thất bại.
2. **QBANK-CH07-11 (Độ rộng địa chỉ phân trang):**
   - $S = 2048 = 2^{11} \implies d = 11\text{ bit}$. 12 trang logic $\implies p = 4\text{ bit} \implies$ Logic $= 15\text{ bit}$.
   - 32 khung vật lý $\implies f = 5\text{ bit} \implies$ Vật lý $= 16\text{ bit}$.
3. **QBANK-CH07-12 (EAT không tải TLB):**
   - $t_{\text{RAM}} = 200\text{ns}, \text{normal} = 400\text{ns}, \alpha = 0.75, \epsilon = 0 \implies \text{EAT} = 250\text{ns}$.
4. **QBANK-CH07-13 (Phân trang hai cấp):**
   - 32-bit: $p_1 = 9, p_2 = 11 \implies d = 12\text{ bit}, S = 4096\text{ bytes} = 4\text{KB}$, số trang $= 2^{20}$.
5. **QBANK-CH07-14 (Công thức số trang biểu tượng):**
   - Phân rã $a \mid b \mid c \mid d$: số trang $= 2^{a+b+c} = 2^{32-d}$ dưới điều kiện $a+b+c+d=32$.
6. **QBANK-CH07-15 (Chuyển đổi địa chỉ):**
   - Phần A: $\text{PA} = 6568, S = 1024 \implies f = 6, d = 424 \implies \text{LA} = 3496$.
   - Phần B: $S = 2048, \text{LA} = 3254 \implies p = 1, d = 1206 \implies \text{PA} = 9398$.
7. **QBANK-CH07-16 (EAT có độ trễ tra bảng TLB):**
   - $t_{\text{RAM}} = 124\text{ns}, \epsilon = 34\text{ns}, \alpha = 0.95 \implies T_{\text{normal}} = 248\text{ns}, T_{\text{Hit}} = 158\text{ns}, T_{\text{Miss}} = 282\text{ns}, \text{EAT} = 164.2\text{ns}$.
8. **QBANK-CH07-17 (Tính ngược $t_{\text{RAM}}$ từ EAT):**
   - $\text{EAT} = 175\text{ns}, \epsilon = 24\text{ns}, \alpha = 0.87 \implies t_{\text{RAM}} \approx 133.63\text{ns}, T_{\text{normal}} \approx 267.26\text{ns}$.
9. **QBANK-CH07-18 (Tính ngược tỷ lệ trúng TLB $\alpha$):**
   - $T_{\text{normal}} = 250\text{ns} \implies t_{\text{RAM}} = 125\text{ns}; \epsilon = 26\text{ns}, \text{EAT} = 182\text{ns} \implies \alpha = 0.752 = 75.2\%$.
10. **QBANK-CH07-19 (Dung lượng bảng phân trang):**
    - 32-bit, trang $8\text{KB} \implies 2^{19}$ mục; 1 byte/mục $\implies$ Dung lượng $= 512\text{ KiB}$ ($524,288\text{ bytes}$).
11. **QBANK-CH07-20 (Độ rộng mục bảng trang & số lượng mục):**
    - 64 khung $\implies 6\text{ bit}$ tối thiểu cho trường frame. 45 trang $\implies$ Bảng phân trang cần tối thiểu $45\text{ mục}$.
12. **Synthetic Transfer 1 (Ánh xạ địa chỉ Hex):**
    - $\text{LA} = \text{0x0041A7C8}, S = 4\text{KB} \implies p = \text{0x0041A}, d = \text{0x7C8}, f = \text{0x000F2} \implies \text{PA} = \text{0x000F27C8}$.
13. **Synthetic Transfer 2 (Độ trễ Swapping):**
    - Tiến trình $100\text{MB}$, băng thông $50\text{MB/s}$, latency $8\text{ms} \implies$ Swap-out $= 2008\text{ms}$, Tổng swap in + out $= 4016\text{ms} = 4.016\text{s}$.

---

## 4. GHI NHẬN CÁC PHÁT HIỆN HỌC THUẬT ĐỂ CHUYỂN GIAO (ACADEMIC FINDINGS)

Tuân thủ nguyên tắc khoá nội dung học thuật trong pha Engineering QA, các phát hiện dưới đây được ghi nhận chuyển giao nguyên trạng cho pha thẩm định học thuật độc lập tiếp theo:

1. `ACADEMIC-CH7-TLB-MISS`:
   - **Phạm vi:** `QBANK-CH07-16` và lý thuyết phần 7.5.3 (Cơ chế TLB).
   - **Ghi nhận:** Khi tính thời gian trượt TLB ($T_{\text{Miss}}$), cẩm nang áp dụng mô hình tuần tự chuẩn Silberschatz: tra TLB trước (tốn $\epsilon$), khi trượt mới đọc bảng trang trong RAM và đọc dữ liệu ô nhớ ($2 \times t_{\text{RAM}}$), tổng là $\epsilon + 2 \times t_{\text{RAM}} = 282\text{ns}$. Một số bài tập trắc nghiệm rút gọn có thể bỏ qua $\epsilon$ trong nhánh trượt ($2 \times t_{\text{RAM}}$). Lời giải cẩm nang hiện tại đã bao quát và diễn giải chi tiết cả hai cách hiểu.
2. `ACADEMIC-CH7-PAGE-SIZE-WORDING`:
   - **Phạm vi:** `QBANK-CH07-13`.
   - **Ghi nhận:** Câu hỏi nguồn hỏi kích thước trang khi trường offset có 12 bit. Cẩm nang ghi nhận đồng thời "$4096\text{ bytes}$" và "$4\text{KB}$" ($2^{12}$ bytes) để sinh viên không bị mất điểm do cách chấm đối chiếu chuỗi của giảng viên.
3. `ACADEMIC-CH7-Q15-LOCATOR`:
   - **Phạm vi:** `QBANK-CH07-15`.
   - **Ghi nhận:** Bài tập 15 trong tệp nguồn `Bai tap chuong 7 HDH.docx` bao gồm 2 câu con độc lập: Câu A (cho PA tính LA) và Câu B (cho LA tính PA). Cẩm nang đã cấu trúc lời giải thành 2 phần rõ rệt với đầy đủ các bước chia lấy nguyên/dư.
4. `AUTHOR-CH7-EAT-TRANSFER`:
   - **Phạm vi:** Khối `TransferProblem` trong `ch07-memory-management.md`.
   - **Ghi nhận:** Hiện tại 2 bài toán chuyển giao trong chương 7 tập trung vào: (1) Cấp phát bộ nhớ động với chuỗi sự kiện giải phóng và nạp mới (`tp-ch07-fit-allocation`); (2) Ánh xạ phân trang trực tiếp trên hệ cơ số 16 Hex (`tp-ch07-paging-hex`). Nếu đợt thẩm định học thuật yêu cầu thêm bài toán tính ngược EAT ở cấp độ chuyển giao, có thể bổ sung một bài toán chuyển giao thứ ba trong các lượt hoàn thiện tiếp theo.

---

## 5. KẾT LUẬN & BÀN GIAO

- Toàn bộ 17 cổng kiểm tra nền tảng (`scripts/generate_foundation_gate.py`) đều đạt **PASS**.
- Toàn bộ 17 ca kiểm thử phủ định (`scripts/run_negative_tests.py`) đều đạt **PASS** (bao gồm 4 ca đột biến trường cục bộ và 1 ca đột biến summary drift).
- Bộ kiểm thử trình duyệt thực tế Chromium Playwright (`tests/learning-system.spec.js`) đạt **14/14 test PASS** (bao gồm Scenario 13 Reference Mode và Scenario 14 Mobile 390px cho Chương 7).
- Bản thảo Chương 7 đã sạch sẽ 100% về mặt markup, encoding, ràng buộc trường lời giải, độ chính xác tính toán và độ bền bỉ kiểm thử.
- Trạng thái sẵn sàng: **BÀN GIAO TIẾN HÀNH ĐỘC LẬP ACADEMIC / SOURCE-FIDELITY REVIEW.**

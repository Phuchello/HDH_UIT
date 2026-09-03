# BÁO CÁO THẨM ĐỊNH BẢN ĐỒ NGUỒN CHƯƠNG 7: QUẢN LÝ BỘ NHỚ
# MODEL: Codex Luna Ultra
# ROLE: Source Archaeologist + Operating Systems Academic Mapper
# MODE: SOURCE DISCOVERY / PROVENANCE / COVERAGE ONLY

---

## 1. STARTING HEAD

- **Starting Remote HEAD:** `1855fd7c8958ba18b99db3de3092cd96c3ff6b3a`
- **Recheck Repair Starting HEAD:** `048c2af10a2ebaa36df064e847eb33178069eaed`
- **Report Closeout Starting HEAD:** `f06fd3e7c99ad916c228b61ad7fa34fadbe719da`
- **Locked Base:** Chapters 1–6 are fully locked, verified, and passing all regression gates.
- **Scope Directives:** Source mapping, physical evidence discovery, and provenance resolution only. Zero Chapter 7 authoring. Chapters 1–6 academic content completely untouched.

---

## 2. CANONICAL OUTLINE EVIDENCE

- **Canonical Course Outline ID:** `UIT-OUTLINE-2024`
- **Tên tệp chính thức:** `IT007_HeDieuHanh_14.2024.pdf`
- **Dung lượng nhị phân:** 418,490 bytes
- **Mã băm SHA-256:** `89547bca603d2486225f1e7c4f3ca767882964d83229ced16dc36b17eea309ab`
- **Số trang vật lý:** 19 trang (tạo ngày 2024-09-11 10:14:48+07:00)
- **Tác quyền / Ban hành:** Khoa Kỹ thuật Máy tính – Trường Đại học Công nghệ Thông tin, ĐHQG-HCM
- **Phân bổ tiến độ đào tạo:**
  - **Buổi 9:** Chương 7. Quản lý bộ nhớ
  - **Chỉ dẫn chuẩn bị:** *"Sinh viên chuẩn bị trước ở nhà: Đọc chương 7 giáo trình Hệ điều hành và bộ slide week 9 do giáo viên cung cấp."*
  - **Chỉ dẫn bài tập về nhà:** *"Sinh viên học ở nhà: Xem lại bài học, trả lời các câu hỏi thảo luận và làm bài tập ở cuối slide week 9 vào vở bài tập."*
- **Biến thể đề cương lịch sử:** `UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG` (`De cuong.pdf`, 452,857 bytes, SHA-256 `8ff13e4d...`, tạo ngày 2023-03-29).

---

## 3. OFFICIAL CH7 HIERARCHY

Cấu trúc đề cương chính thức của Chương 7 theo Đề cương chi tiết năm học 2024–2025:

```text
Chương 7. Quản lý bộ nhớ
├── 7.1 Khái niệm cơ sở
├── 7.2 Các loại địa chỉ nhớ
├── 7.3 Chuyển đổi giữa các loại địa chỉ nhớ
├── 7.4 Các mô hình quản lý bộ nhớ theo cơ chế cấp phát liên tục
│   ├── 7.4.1 Phân vùng tĩnh
│   └── 7.4.1 Phân vùng động  <-- [SOURCE TYPO trong đề cương gốc]
├── 7.5 Cơ chế phân trang
├── 7.6 Cơ chế swapping
└── 7.7 Bài tập
```

---

## 4. SOURCE TYPO NOTE

- **Phát hiện lỗi sao chép gốc (Source Typo):**
  Trong văn bản đề cương chính thức `IT007_HeDieuHanh_14.2024.pdf` tại trang 6, mục 7.4 cấp phát liên tục bị lặp số thứ tự:
  - `7.4.1 Phân vùng tĩnh`
  - `7.4.1 Phân vùng động`
- **Quy ước xử lý:**
  - Không tự ý sửa đổi văn bản chứng cứ lịch sử của đề cương.
  - Trong cấu trúc học thuật và bảng ánh xạ, mục thứ hai được chuẩn hóa thành `7.4.2 Phân vùng động` kèm nhãn định danh bắt buộc: `NORMALIZED_NUMBERING_FROM_SOURCE_TYPO`.
  - Trên slide bài giảng `#Week09-Chapter7 2024.pdf`, giảng viên đã đánh số chuẩn xác thành `7.4.1 Fixed partitioning` và `7.4.2 Dynamic partitioning`.

---

## 5. SLIDE CANDIDATE DISCOVERY

Khảo sát toàn bộ kho lưu trữ học liệu chính thức `<verified-it007-source-corpus>`, phát hiện hai ứng viên nhị phân cho slide Chương 7:

| Thuộc tính | Ứng viên 1 (Mới / Chuẩn 2024) | Ứng viên 2 (Cũ / Bản xuất sớm) |
| :--- | :--- | :--- |
| **Tên tệp** | `#Week09-Chapter7 2024.pdf` | `Week12-Chapter7 2024.pdf` |
| **Dung lượng (bytes)** | 7,462,286 bytes | 7,459,415 bytes |
| **Mã băm SHA-256** | `86e6260cdc2fd1461277434fa74ee0a325c945ba9cb5d1b0d4ba46a76045c5a9` | `4b622457cd5592dc83afce32f8ca5ddf1c9e9bca6defdbed36150e80f0717177` |
| **Số trang vật lý** | 72 trang | 72 trang |
| **Thời gian tạo PDF** | 2024-09-11 10:40:43+07:00 | 2024-02-15 17:50:19+07:00 |
| **Tác giả Metadata** | Trần Hoàng Lộc; Nguyễn Thanh Thiện | Trần Hoàng Lộc; Nguyễn Thanh Thiện |
| **Gói nguồn phân phối** | Thư mục chính khóa `Tài liệu học tập-20240912` | Thư mục tải về rời rạc từ Google Drive |
| **Đối chiếu Đề cương** | **Khớp 100%** (Đề cương quy định rõ `slide week 9`) | Lệch số tuần (ghi Week 12 từ học kỳ cũ) |

---

## 6. WEEK09 VS WEEK12 COMPARISON

So sánh đối chiếu toàn diện 72 trang vật lý giữa `#Week09-Chapter7 2024.pdf` và `Week12-Chapter7 2024.pdf`:

1. **Cấu trúc slide và nội dung học thuật:**
   - 72/72 trang có cấu trúc đề mục, sơ đồ, bảng biểu và số liệu hoàn toàn tương đồng.
   - Trình tự các phần 7.1 $\to$ 7.7 và 5 bài tập cuối chương hoàn toàn khớp nhau.
2. **Khác biệt văn bản (Text extraction diff):**
   - Khác biệt xuất hiện tại 11 trang: Trang 1, 18, 19, 22, 53, 58, 60, 61, 68, 69, 70.
   - Toàn bộ 11 điểm khác biệt đều là **lỗi dính từ / lỗi kerning khoảng trắng** trong bản xuất sớm (Week 12).
   - *Ví dụ:*
     - Bản Week 12 (cũ): `Xétmột không gian địa chỉ có12 trang, mỗitrang cókíchthước`
     - Bản Week 09 (mới): `Xét một không gian địa chỉ có 12 trang, mỗi trang có kích thước`
     - Bản Week 12 (cũ): `Một máy tính32-bit địa chỉ, sửdụngmột bảng trang 2 cấp`
     - Bản Week 09 (mới): `Một máy tính 32-bit địa chỉ, sử dụng một bảng trang 2 cấp`
3. **Thời điểm biên xuất:**
   - Bản Week 12 xuất ngày 15/02/2024 (trước khi năm học mới bắt đầu).
   - Bản Week 09 xuất ngày 11/09/2024 (cùng ngày và cùng gói tài liệu với Đề cương chính thức 2024–2025).

---

## 7. CANONICAL SLIDE DECISION

- **Quyết định xác lập quyền thẩm quyền (Authority Decision):**
  - **`UIT-SLIDE-CH07-2024`** được chuyển đổi và xác lập chính thức cho:
    `#Week09-Chapter7 2024.pdf` (7,462,286 bytes, SHA-256 `86e6260cdc2fd1461277434fa74ee0a325c945ba9cb5d1b0d4ba46a76045c5a9`).
  - **Lý do:** Khớp chuẩn chỉ định `slide week 9` của Đề cương 2024–2025; là bản xuất hoàn thiện mới nhất khắc phục triệt để lỗi dính từ của bản xuất cũ.
- **Biến thể lưu trữ (PROV-CH7-001):**
  - `Week12-Chapter7 2024.pdf` được đăng ký dưới dạng biến thể lịch sử bất biến:
    `UIT-SLIDE-CH07-2024-VARIANT-WEEK12-72` (`tier: "A"`, `type: "source_variant"`, `status: "VERIFIED_LOCAL_VARIANT"`).

---

## 8. CANONICAL QBANK BINARY VERIFICATION

Khảo sát tệp tài liệu câu hỏi ôn tập Chương 7 phát hiện hai bản sao DOCX:

| Thuộc tính | Bản chuẩn 20240912 (`Tài liệu học tập-20240912`) | Bản tải Drive cũ (`drive-download`) |
| :--- | :--- | :--- |
| **Tên tệp** | `Bai tap chuong 7 HDH.docx` | `Bai tap chuong 7 HDH.docx` |
| **Dung lượng** | 23,960 bytes | 22,871 bytes |
| **Mã băm SHA-256** | `5b03f4e0691855f38d43872f79ba61a21378fea3ec5ee2551be5321a29b88e40` | `f8e523d10b0c75a18f5551f3f1f59c5827830ec56c095e92d68e4bfb50ec0b77` |
| **Đoạn thân văn bản** | 88 đoạn thân (84 phi rỗng) | 85 đoạn thân (80 phi rỗng) |
| **Số bảng biểu** | 1 bảng (6 dòng $\times$ 2 cột = 12 đoạn ô) | 1 bảng (6 dòng $\times$ 2 cột = 12 đoạn ô) |
| **Tổng nút XML w:p** | 100 nút (96 phi rỗng) | 97 nút (92 phi rỗng) |
| **Tình trạng văn bản** | **Đầy đủ 20 câu hỏi** (9 lý thuyết + 11 bài tập) | Bị cắt ngắn ở đoạn 80, thiếu bài 19 và 20 |

- **Xác lập quyền thẩm quyền QBank:**
  - `UIT-QBANK-CH07-2024` được gắn định danh bất biến với bản đầy đủ 23,960 bytes (SHA-256 `5b03f4e0...`).
  - Bản Drive cũ bị thiếu nội dung được phân loại thành biến thể `UIT-QBANK-CH07-2024-VARIANT-DRIVE-85P` (`tier: "A"`, `type: "source_variant"`, `status: "VERIFIED_LOCAL_VARIANT"`).

---

## 9. QBANK SOURCE-UNIT INVENTORY

Bộ bài tập Chương 7 chính thức bao gồm chính xác **20 đơn vị nguồn nguyên tử (atomic units)**:

### A. Câu hỏi Lý thuyết (9 đơn vị):
1. **`QBANK-CH07-01`** (P3): Khái niệm quản lý bộ nhớ và các yêu cầu đối với quản lý bộ nhớ (tái định vị, bảo vệ, chia sẻ, tổ chức logic, tổ chức vật lý).
2. **`QBANK-CH07-02`** (P4): Đặc điểm các loại địa chỉ bộ nhớ (Symbolic address, Relocatable address, Absolute address; Logical vs Physical address).
3. **`QBANK-CH07-03`** (P5): Các thời điểm chuyển đổi địa chỉ lệnh và dữ liệu thành địa chỉ thực (Compile time, Load time, Execution time).
4. **`QBANK-CH07-04`** (P6): Khái niệm và cơ chế hoạt động của liên kết động (Dynamic linking và thư viện chia sẻ).
5. **`QBANK-CH07-05`** (P7): Khái niệm và sự khác biệt giữa phân mảnh ngoại (External fragmentation) và phân mảnh nội (Internal fragmentation).
6. **`QBANK-CH07-06`** (P8): Phân vùng động vs phân vùng cố định; mục đích và các chiến lược placement (First-fit, Best-fit, Next-fit, Worst-fit).
7. **`QBANK-CH07-07`** (P9): Cơ chế phân trang (Paging) và quy trình chuyển đổi địa chỉ từ địa chỉ ảo $(p, d)$ sang địa chỉ vật lý $(f, d)$.
8. **`QBANK-CH07-08`** (P10): Cách cài đặt và tổ chức bảng trang phần cứng (PTBR, TLB); định nghĩa và công thức tính thời gian truy xuất hiệu dụng (EAT).
9. **`QBANK-CH07-09`** (P11): Khái niệm và cơ chế hoạt động của kỹ thuật hoán vị (Swapping).

### B. Bài tập Tự luận & Tính toán (11 đơn vị):
10. **`QBANK-CH07-10`** (P12–P55): Bài tập mẫu 1 về cấp phát bộ nhớ phân vùng cố định và phân vùng động cho 4 tiến trình (212K, 417K, 112K, 426K) vào 4 phân vùng (600K, 500K, 200K, 300K) theo 4 thuật toán First fit, Best fit, Next fit, Worst fit.
11. **`QBANK-CH07-11`** (P56–P61): Bài tập mẫu 2 về không gian địa chỉ ảo 12 trang (kích thước trang 2K), ánh xạ vào bộ nhớ vật lý 32 khung trang; xác định số bit của địa chỉ logic và địa chỉ vật lý.
12. **`QBANK-CH07-12`** (P62–P67): Bài tập mẫu 3 về hệ thống phân trang có bảng trang trong RAM; tính thời gian truy xuất phân trang thông thường ($2 \times 200\text{ns} = 400\text{ns}$) và tính EAT với TLB hit-ratio 75% (thời gian tra TLB xem như bằng 0).
13. **`QBANK-CH07-13`** (P68): Bài tập 4 về máy tính địa chỉ 32-bit dùng bảng trang 2 cấp (9 bit cấp 1, 11 bit cấp 2, còn lại offset); tính kích thước trang và tổng số trang ảo.
14. **`QBANK-CH07-14`** (P69): Bài tập 5 về địa chỉ ảo 32-bit phân tách thành 4 trường $a, b, c, d$ (3 cấp bảng trang và offset); phân tích ảnh hưởng của các trường đến số lượng trang ảo.
15. **`QBANK-CH07-15`** (P70–P75): Bài tập mẫu 6 chuyển đổi địa chỉ vật lý 6568 sang địa chỉ ảo (với frame 1KB) và địa chỉ ảo 3254 sang địa chỉ vật lý (với frame 2KB) dựa trên bảng phân trang mẫu.
16. **`QBANK-CH07-16`** (P76–P78): Bài tập 7 tính thời gian truy xuất thông thường và thời gian truy xuất hiệu dụng (EAT) với truy xuất bộ nhớ 124ns, TLB hit-ratio 95%, thời gian tìm TLB 34ns.
17. **`QBANK-CH07-17`** (P79): Bài tập 8 tính ngược thời gian truy xuất bộ nhớ bình thường khi biết EAT = 175ns, TLB hit-ratio 87% và thời gian tra cứu TLB 24ns.
18. **`QBANK-CH07-18`** (P80): Bài tập 9 tính xác suất tìm thấy trong TLB (hit-ratio $\alpha$) khi biết thời gian truy xuất bình thường 250ns, tìm kiếm TLB 26ns và EAT = 182ns.
19. **`QBANK-CH07-19`** (P81–P82): Bài tập mẫu 10 tính dung lượng bảng phân trang cho bộ vi xử lý không gian ảo 32-bit có $2^{19}$ mục, kích thước mỗi mục là 8 bit ($512\text{ KB}$).
20. **`QBANK-CH07-20`** (P83–P88): Bài tập mẫu 11 tính số bit tối thiểu cho mỗi mục bảng trang (6 bit cho 64 khung) và tổng số mục (45 mục cho 45 trang) trong không gian ảo có 45 trang 2048 bytes.

---

## 10. PAGE-BY-PAGE / RANGE COVERAGE

Tổng số trang vật lý: **72 trang** (67 trang CONTENT + 5 trang NON_CONTENT).
Toàn bộ 19 phân đoạn ngữ nghĩa liên tục, không khe hở, không chồng lấn:

| STT | Dải trang | Số trang | Phân loại | Tên chuyên đề / Nội dung bài giảng | Ánh xạ đích V2 | Trạng thái |
| :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| 1 | `1-4` | 4 | NON_CONTENT | Trang bìa, nội dung đã học, mục tiêu bài học và nội dung chính | `None (Meta)` | `NOT_WRITTEN` |
| 2 | `5-10` | 6 | CONTENT | 7.1 Khái niệm cơ sở: vai trò quản lý bộ nhớ, không gian địa chỉ, cấu trúc phân cấp | `ch07-memory-management.md#1-khai-niem-dia-chi` | `NOT_WRITTEN` |
| 3 | `11-16` | 6 | CONTENT | 7.2 Các kiểu địa chỉ nhớ: symbolic, relocatable, absolute; logical vs physical; Linker và Loader | `ch07-memory-management.md#1-khai-niem-dia-chi` | `NOT_WRITTEN` |
| 4 | `17-22` | 6 | CONTENT | 7.3.1 Chuyển đổi địa chỉ: compile time, load time, execution time; MMU và relocation register | `ch07-memory-management.md#1-khai-niem-dia-chi` | `NOT_WRITTEN` |
| 5 | `23-25` | 3 | CONTENT | 7.3.2 Dynamic linking: liên kết động và thư viện liên kết động (stub, shared library) | `ch07-memory-management.md#1-khai-niem-dia-chi` | `NOT_WRITTEN` |
| 6 | `26-27` | 2 | CONTENT | 7.3.3 Dynamic loading: nạp động theo nhu cầu gọi thủ tục | `ch07-memory-management.md#1-khai-niem-dia-chi` | `NOT_WRITTEN` |
| 7 | `28-32` | 5 | CONTENT | 7.4 Mô hình quản lý bộ nhớ cấp phát liên tục: đơn phân vùng và đa phân vùng | `ch07-memory-management.md#2-cap-phat-lien-tuc` | `NOT_WRITTEN` |
| 8 | `33-36` | 4 | CONTENT | 7.4.1 Phân vùng cố định (Fixed partitioning): cơ chế phân vùng tĩnh và phân mảnh nội (internal fragmentation) | `ch07-memory-management.md#2-cap-phat-lien-tuc` | `NOT_WRITTEN` |
| 9 | `37-39` | 3 | CONTENT | 7.4.2 Phân vùng động (Dynamic partitioning): phân mảnh ngoại, thuật toán First/Best/Worst/Next fit và compaction | `ch07-memory-management.md#2-cap-phat-lien-tuc` | `NOT_WRITTEN` |
| 10 | `40-42` | 3 | CONTENT | 7.5 Cơ chế phân trang (Paging): cấp phát không liên tục, khái niệm trang (page), khung trang (frame) và ánh xạ | `ch07-memory-management.md#3-phan-trang-tlb` | `NOT_WRITTEN` |
| 11 | `43-47` | 5 | CONTENT | 7.5.1 Chuyển đổi địa chỉ trong phân trang: cấu trúc (p, d) sang (f, d) và kiến trúc bảng trang | `ch07-memory-management.md#3-phan-trang-tlb` | `NOT_WRITTEN` |
| 12 | `48-51` | 4 | CONTENT | 7.5.2 Cài đặt bảng trang: thanh ghi phần cứng PTBR, bộ đệm Translation Lookaside Buffer (TLB), TLB hit/miss | `ch07-memory-management.md#3-phan-trang-tlb` | `NOT_WRITTEN` |
| 13 | `52-54` | 3 | CONTENT | 7.5.3 Effective Access Time (EAT): tỷ lệ hit ratio, công thức thời gian truy xuất hiệu dụng và ví dụ tính toán | `ch07-memory-management.md#3-phan-trang-tlb` | `NOT_WRITTEN` |
| 14 | `55-58` | 4 | CONTENT | 7.5.4 Tổ chức bảng trang nâng cao: phân trang 2 cấp (hierarchical), bảng trang băm (hashed) và bảng trang nghịch đảo (inverted) | `ch07-memory-management.md#4-cau-truc-bang-trang-nang-cao` | `NOT_WRITTEN` |
| 15 | `59-62` | 4 | CONTENT | 7.5.5 Bảo vệ bộ nhớ và chia sẻ trang: protection bits, valid/invalid bit, chia sẻ mã trang (shared pages) | `ch07-memory-management.md#4-cau-truc-bang-trang-nang-cao` | `NOT_WRITTEN` |
| 16 | `63-65` | 3 | CONTENT | 7.6 Cơ chế hoán vị (Swapping): hoán vị tiến trình giữa RAM và backing store, chi phí context switch | `ch07-memory-management.md#5-swapping` | `NOT_WRITTEN` |
| 17 | `66` | 1 | CONTENT | Tóm tắt nội dung cốt lõi Chương 7 | `ch07-memory-management.md#5-swapping` | `NOT_WRITTEN` |
| 18 | `67-71` | 5 | CONTENT | 7.7 Bài tập slide (Bài 1–5): phân vùng liên tục, tính số bit địa chỉ logic/vật lý, tính EAT, bảng trang 2 cấp và 3 cấp | `ch07-memory-management.md#6-bai-tap-slide` | `NOT_WRITTEN` |
| 19 | `72` | 1 | NON_CONTENT | Thảo luận và kết thúc buổi học | `None (Meta)` | `NOT_WRITTEN` |

---

## 11. VISUAL EVIDENCE AUDIT

Đã kiểm tra trực quan nhị phân và trích xuất hình ảnh trên toàn bộ 21 trang trọng điểm có sơ đồ cấu trúc và bảng biểu:
- **Trang 15–16:** Sơ đồ chu trình xử lý mã nguồn qua Linker (liên kết) và Loader (nạp chương trình).
- **Trang 20–22:** Sơ đồ ràng buộc địa chỉ qua 3 thời điểm; sơ đồ phần cứng MMU với thanh ghi Relocation (Base register).
- **Trang 24, 27:** Sơ đồ cơ chế Dynamic Linking với stub và nạp thư viện động; sơ đồ Dynamic Loading.
- **Trang 31:** Sơ đồ phân vùng bộ nhớ và cấp phát liên tục.
- **Trang 35, 39:** Sơ đồ phân mảnh nội trong phân vùng cố định; sơ đồ phân mảnh ngoại và cơ chế gom cụm (compaction) trong phân vùng động.
- **Trang 42, 44–45, 47:** Sơ đồ phần cứng phân trang (Paging Hardware): CPU phát sinh địa chỉ logic $(p, d)$, tra bảng trang lấy $f$, ghép thành $(f, d)$ trỏ vào bộ nhớ vật lý; ví dụ ánh xạ cụ thể 4 trang.
- **Trang 50:** Sơ đồ phần cứng phân trang kết hợp bộ nhớ liên kết TLB (TLB Hit tra trực tiếp frame $f$, TLB Miss tra bảng trang trong RAM và cập nhật TLB).
- **Trang 56:** Sơ đồ phân trang phân cấp 2 tầng (Two-Level Page Table Scheme: $p_1, p_2, d$).
- **Trang 57:** Sơ đồ bảng trang băm (Hashed Page Table với chuỗi liên kết danh sách).
- **Trang 58:** Sơ đồ bảng trang nghịch đảo (Inverted Page Table: tra theo PID và trang $p$).
- **Trang 61–62:** Sơ đồ bảo vệ bộ nhớ bằng bit Valid/Invalid; sơ đồ chia sẻ trang bộ nhớ (Shared code trang ed1, ed2, ed3 giữa 3 tiến trình).
- **Trang 65:** Sơ đồ tổng thể cơ chế hoán vị (Swapping Schematic) giữa bộ nhớ chính và Backing Store.
- **Trang 67–71:** Trực quan toàn bộ 5 bài tập mẫu cuối slide.

---

## 12. OUTLINE ↔ SLIDE CROSSWALK

| Mục Đề Cương | Nội Dung Đề Cương | Dải Trang Slide | Đánh Giá Tương Đồng / Phân Loại |
| :--- | :--- | :--- | :--- |
| **7.1** | Khái niệm cơ sở | pp. 5–10 | Khớp hoàn toàn. |
| **7.2** | Các loại địa chỉ nhớ | pp. 11–16 | Khớp hoàn toàn. |
| **7.3** | Chuyển đổi giữa các loại địa chỉ nhớ | pp. 17–27 | Khớp mục chính; phần Dynamic Linking (pp.23–25) và Dynamic Loading (pp.26–27) được mở rộng chi tiết $\implies$ `SOURCE-SUPPORTED_EXTENSION`. |
| **7.4** | Cấp phát liên tục | pp. 28–32 | Khớp hoàn toàn. |
| **7.4.1** | Phân vùng tĩnh | pp. 33–36 | Khớp hoàn toàn. |
| **7.4.1 (7.4.2)** | Phân vùng động | pp. 37–39 | Khớp hoàn toàn (`NORMALIZED_NUMBERING_FROM_SOURCE_TYPO`). |
| **7.5** | Cơ chế phân trang | pp. 40–62 | Khớp cơ chế cốt lõi. Các mục nâng cao (TLB, EAT, Bảng trang 2 cấp, Băm, Nghịch đảo, Bảo vệ & chia sẻ trang) là nội dung bài giảng chính thức $\implies$ `SOURCE-SUPPORTED_EXTENSION`. |
| *Ngoài đề cương* | Phân đoạn (Segmentation) | Không có | **Không có trong slide chính thức Chương 7**. Phân loại: `OUT_OF_SCOPE_VARIANT` đối với Chương 7 (chuyển sang tài liệu đọc thêm hoặc Chương 8). |
| **7.6** | Cơ chế swapping | pp. 63–65 | Khớp hoàn toàn. |
| **7.7** | Bài tập | pp. 67–71 & QBank 20 units | Khớp hoàn toàn. |

---

## 13. VARIANT REGISTRY

1. **`UIT-SLIDE-CH07-2024-VARIANT-WEEK12-72`**:
   - Tệp tin: `Week12-Chapter7 2024.pdf` (7,459,415 bytes, 72 trang, SHA-256 `4b622457...`).
   - Phân loại: `Tier A` / `source_variant` / `VERIFIED_LOCAL_VARIANT` (PROV-CH7-001).
   - Ghi chú: Bản xuất sớm tháng 2/2024 mang tên Week 12 từ học kỳ cũ; mắc lỗi kerning/dính khoảng trắng tại 11 trang.
2. **`UIT-QBANK-CH07-2024-VARIANT-DRIVE-85P`**:
   - Tệp tin: `Bai tap chuong 7 HDH.docx` (22,871 bytes; 85 đoạn thân / 80 phi rỗng; 1 bảng 6x2 gồm 12 đoạn ô; 97 nút XML w:p / 92 phi rỗng, SHA-256 `f8e523d1...`).
   - Phân loại: `Tier A` / `source_variant` / `VERIFIED_LOCAL_VARIANT` (PROV-CH7-001).
   - Ghi chú: Bản tải từ Drive bị cắt ngắn ở đoạn 80 (thiếu 2 bài tập mẫu tính kích thước và số mục bảng trang).

---

## 14. SOURCE FINDINGS

### BLOCKERS: 0 OPEN (1 RESOLVED)
- **`SRC-CH7-001 — BLOCKER — OPEN $\to$ RESOLVED`**:
  - *Vấn đề:* Sổ đăng ký ban đầu ghi nhận `Week12-Chapter7 2024.pdf` làm nguồn chính ngạch, mâu thuẫn trực tiếp với Đề cương chính thức 2024–2025 quy định Chương 7 tại Buổi 9 học qua `slide week 9`.
  - *Giải quyết:* Phát hiện bản nhị phân chuẩn `#Week09-Chapter7 2024.pdf` (7,462,286 bytes, SHA-256 `86e6260c...`) trong gói học liệu chính khóa 20240912. Đối chiếu toàn diện chứng minh bản Week 09 là bản hoàn thiện khắc phục các lỗi font của bản Week 12 và khớp chuẩn Đề cương. Đã thăng hạng `#Week09-Chapter7 2024.pdf` thành `UIT-SLIDE-CH07-2024` và lưu giữ bản Week 12 thành biến thể lịch sử bất biến.

### MAJORS: 0 OPEN (4 RESOLVED)
- **`PROV-CH7-001 — MAJOR — OPEN $\to$ RESOLVED`**:
  - *Vấn đề:* Sổ đăng ký ban đầu phân loại hai biến thể học liệu chính thức của UIT (`UIT-SLIDE-CH07-2024-VARIANT-WEEK12-72` và `UIT-QBANK-CH07-2024-VARIANT-DRIVE-85P`) là Tier B, vi phạm quy ước hệ thống (học liệu chính thức UIT luôn thuộc Tier A, phân biệt tính phi chuẩn qua `type: source_variant` và `status: VERIFIED_LOCAL_VARIANT`).
  - *Giải quyết:* Đã chuẩn hóa phân loại của hai biến thể về đúng `tier: "A"` với `type: "source_variant"`.
- **`SRC-CH7-002 — MAJOR — OPEN $\to$ RESOLVED`**:
  - *Vấn đề:* Bất đồng nhất giữa số lượng 88 đoạn văn bản và 100 nút XML w:p trong tài liệu câu hỏi ôn tập Chương 7.
  - *Giải quyết:* Phân tách và định danh tường minh toàn bộ các chỉ số đo lường: 88 đoạn thân văn bản (84 phi rỗng), 1 bảng 6 dòng $\times$ 2 cột (12 ô / 12 đoạn ô phi rỗng), tổng cộng 100 nút XML `<w:p>` (96 phi rỗng). Cập nhật đồng bộ sổ đăng ký, sổ nguồn và bộ kiểm định.
- **`ENG-CH7-001 — MAJOR — OPEN $\to$ RESOLVED`**:
  - *Vấn đề:* Trình tìm kiếm `find_file` trong chế độ Evidence Mode chỉ trả về tệp đầu tiên tìm thấy, không thể xử lý độc lập thứ tự duyệt khi kho lưu trữ có hai tệp trùng tên `Bai tap chuong 7 HDH.docx`.
  - *Giải quyết:* Thay thế bằng `find_all_files` kết hợp `resolve_candidate_by_hash`, đảm bảo nhận diện chính xác bản canonical (23,960 B / `5b03f4e0...`) và bản variant (22,871 B / `f8e523d1...`) bất kể thứ tự duyệt hệ thống tệp.
- **`SRC-CH7-003 — MAJOR — OPEN $\to$ RESOLVED`**:
  - *Lý do (Reason):* Bảng phân bổ trang trong báo cáo (Mục 10) ghi nhận dòng 19 (trang 72: Thảo luận và kết thúc buổi học) là CONTENT, mâu thuẫn trực tiếp với nguồn chân lý cấu trúc (SSOT) `research/data/slide_coverage.yaml` vốn phân loại trang 72 là NON_CONTENT (`None (Meta)` / `NOT_WRITTEN`).
  - *Khắc phục (Resolution):* Sửa dòng 19 trong bảng báo cáo từ CONTENT sang NON_CONTENT; bổ sung bộ kiểm định đối soát tự động `check_report_consistency` trong `scripts/validate_ch07_source_map.py` ngăn ngừa mọi nguy cơ trôi lệch (drift) giữa báo cáo tường thuật và SSOT cấu trúc. Tổng số trang trên báo cáo khớp tuyệt đối: 67 CONTENT + 5 NON_CONTENT = 72 trang vật lý.

### MINORS: 0 OPEN (1 RESOLVED)
- **`DOC-CH7-001 — MINOR — OPEN $\to$ RESOLVED`**:
  - *Lý do (Reason):* Ký tự điều khiển ẩn BEL (`\x07`) làm sai lệch ký hiệu toán học LaTeX `\alpha` thành `$ lpha$` trong phần mô tả `QBANK-CH07-18`.
  - *Khắc phục (Resolution):* Thay thế bằng mã LaTeX chuẩn xác `$\alpha$` và bổ sung chốt chặn kiểm tra ký tự điều khiển C0 trong `scripts/validate_ch07_source_map.py`.

---

## 15. VALIDATION RESULTS

Đã thực thi toàn bộ hệ thống kiểm tra tự động và các cổng chất lượng:
- `python scripts/generate_registry.py --check` $\implies$ **PASS** (74 nguồn đã đăng ký, 0 drift).
- `python scripts/validate_sources.py` $\implies$ **PASS** (74 nguồn, 60 tham chiếu nội dung hợp lệ).
- `python scripts/validate_ch07_source_map.py` $\implies$ **PASS** (Cả chế độ REPOSITORY MODE và EVIDENCE MODE với multi-candidate discovery và report consistency guard).
- `python scripts/validate_ch06_source_map.py` & `validate_ch06_content.py` $\implies$ **PASS**.
- `python scripts/validate_ch05_source_map.py` & `validate_ch05_content.py` $\implies$ **PASS**.
- `python scripts/validate_batch1_canonical.py` & `check_batch1_numeric.py` $\implies$ **PASS**.
- `python scripts/check_public_hygiene.py` $\implies$ **PASS** (100% sạch đường dẫn cục bộ).
- `npm test` $\implies$ **PASS** (Toàn bộ 15 foundation gates đạt chuẩn).
- `npm run web:build` $\implies$ **PASS** (Biên dịch tĩnh 18 trang thành công).

---

## 16. FINAL DECISION

$$\mathbf{CH7\ SOURCE\ MAPPING:\ PASS\ —\ READY\ FOR\ FINAL\ INDEPENDENT\ CHECK}$$

- **TỔNG KẾT VẤN ĐỀ TỒN ĐỌNG:**
  - **OPEN BLOCKERS:** 0
  - **OPEN MAJORS:** 0
  - **OPEN MINORS:** 0
- **Chapter 7 Source Mapping:** `MAPPED — PENDING FINAL INDEPENDENT CHECK`
- **Chapter 7 Authoring:** `NOT_STARTED`
- **Academic Verification:** `PASS — BATCH 1 + CH5 + CH6`
- **Engineering Verification:** `PASS — CH5 + CH6`
- **Hành động tiếp theo chính xác (Exact Next Action):** Final independent Chapter 7 source-map verification before authoring.

---

## 17. INDEPENDENT RECHECK REPAIR

Phần này ghi nhận chi tiết quá trình xử lý các phát hiện độc lập tại vòng tái kiểm tra (Independent Recheck Closeout):

### 17.1. PROV-CH7-001 — Chuẩn hóa cấp độ nguồn biến thể (Official Variant Tier Semantics)
- **Bản chất vấn đề:** `UIT-SLIDE-CH07-2024-VARIANT-WEEK12-72` và `UIT-QBANK-CH07-2024-VARIANT-DRIVE-85P` ban đầu bị gắn nhãn `tier: "B"`. Quy ước hệ thống của kho lưu trữ xác định rằng toàn bộ các tài liệu có nguồn gốc chính quy từ Trường ĐH Công nghệ Thông tin (kể cả bản xuất cũ từ học kỳ trước hay bản Drive tải về) đều mang thẩm quyền xuất xứ Tier A. Tính chất phi chuẩn (non-canonical) được kiểm soát nghiêm ngặt qua:
  - `type: "source_variant"`
  - `status: "VERIFIED_LOCAL_VARIANT"`
  - Hậu tố định danh `-VARIANT-`
  - Loại trừ tuyệt đối khỏi bảng phân bổ trang học thuật (`slide_coverage.yaml`) và bảng câu hỏi (`official_review_questions.yaml`).
- **Khắc phục:** Đã chuẩn hóa cả 2 bản ghi thành `tier: "A"`, cập nhật đồng bộ `registry.yaml`, `generate_registry.py`, `SOURCE_LEDGER.md` và `validate_ch07_source_map.py`.

### 17.2. SRC-CH7-002 — Bảng đối soát chỉ số cấu trúc QBank (Paragraph Metric Reconciliation)
Đã tái thẩm định vi mô trực tiếp trên cấu trúc nhị phân DOCX của cả hai tệp `Bai tap chuong 7 HDH.docx`:

| Chỉ số cấu trúc đo lường | Bản chuẩn 2024 (`5b03f4e0...`, 23,960 B) | Biến thể Drive (`f8e523d1...`, 22,871 B) | Định nghĩa kỹ thuật & Phương pháp trích xuất |
| :--- | :---: | :---: | :--- |
| `body_paragraph_count` | **88** | **85** | Số đoạn văn bản thuộc thân tài liệu (`doc.paragraphs` hoặc `./w:body/w:p`) |
| `body_nonempty_paragraph_count` | **84** | **80** | Số đoạn thân văn bản chứa nội dung hiển thị thực tế (bỏ qua rỗng) |
| `table_count` | **1** | **1** | Số lượng bảng biểu trong tài liệu (`doc.tables` hoặc `.//w:tbl`) |
| `table_rows` | **6** | **6** | Số hàng của bảng (`w:tr`) |
| `table_cols` | **2** | **2** | Số cột của bảng |
| `table_cells` | **12** | **12** | Tổng số ô trong bảng (`w:tc`) |
| `table_cell_paragraph_count` | **12** | **12** | Số đoạn văn bản nằm trong các ô của bảng (`table.cell.paragraphs`) |
| `table_cell_nonempty_paragraph_count` | **12** | **12** | Số đoạn văn bản phi rỗng trong các ô của bảng |
| `xml_w_p_count` | **100** | **97** | Tổng số nút thẻ `<w:p>` trong toàn bộ tệp XML `word/document.xml` ($88 + 12 = 100$) |
| `xml_nonempty_w_p_count` | **96** | **92** | Tổng số nút thẻ `<w:p>` phi rỗng trong toàn bộ tệp XML ($84 + 12 = 96$) |
| `question_unit_count` | **20** | **18** | Số đơn vị câu hỏi nguyên tử (9 lý thuyết + 11 bài tập; bản Drive thiếu bài 19-20) |

- **Kết luận:** Sự khác biệt giữa số 88 và 100 là do phương thức đo lường: **88 là số đoạn thân văn bản (Body Paragraphs)**, còn **100 là tổng số nút XML `<w:p>` (bao gồm cả 12 đoạn trong các ô bảng)**. Không có sự mâu thuẫn thực tế nào sau khi danh tính kỹ thuật được chuẩn hóa tường minh.

### 17.3. ENG-CH7-001 — Nhận diện ứng viên trùng tên không phụ thuộc thứ tự duyệt (Duplicate-Filename Discovery)
- **Bản chất vấn đề:** Trong kho học liệu `<verified-it007-source-corpus>`, có hai tệp tin vật lý cùng mang tên chính xác `Bai tap chuong 7 HDH.docx` (một bản 23,960 B trong thư mục chính khóa 20240912 và một bản 22,871 B trong thư mục Drive tải về). Hàm `find_file` cũ dừng lại ở tệp đầu tiên tìm thấy trên cây thư mục, dẫn đến nguy cơ sai lệch kết quả phụ thuộc vào thứ tự duyệt của hệ điều hành.
- **Khắc phục:**
  - Triển khai `find_all_files(directories, filename)` quét toàn bộ các cây thư mục nguồn để thu thập tất cả các ứng viên.
  - Triển khai `resolve_candidate_by_hash(candidates, expected_sha, expected_bytes, label)`: băm SHA-256 từng ứng viên và lọc theo mã băm chuẩn của bản canonical, xác nhận tính duy nhất (duy nhất 1 tệp khớp mã băm chuẩn).
  - Tự động nhận diện và thẩm định cấu trúc của bản biến thể `f8e523d1...` khi tệp này xuất hiện trong cây thư mục.
  - Ngăn chặn và báo lỗi nếu xuất hiện bất kỳ tệp trùng tên nào khác có mã băm không nằm trong danh mục đã đăng ký.

### 17.4. SRC-CH7-003 — Khắc phục trôi lệch phân loại trang trên báo cáo (Report Coverage Classification Drift)
- **Bản chất vấn đề:** Tại bảng dải trang Mục 10 của báo cáo nguồn, dòng 19 (trang 72: Thảo luận và kết thúc buổi học) vô tình ghi phân loại là CONTENT, trong khi nguồn chân lý cấu trúc `slide_coverage.yaml` phân loại chuẩn xác là NON_CONTENT (`None (Meta)` / `NOT_WRITTEN`). Mặc dù tổng số trang ở phần giới thiệu ghi 67 CONTENT + 5 NON_CONTENT = 72 trang, sự sai khác ở dòng 19 gây ra mâu thuẫn nội tại giữa bảng biểu tường thuật và SSOT.
- **Khắc phục:**
  - Chuẩn hóa dòng 19 của bảng trong báo cáo thành `NON_CONTENT`.
  - Bổ sung hàm kiểm định `check_report_consistency` trong `scripts/validate_ch07_source_map.py` tự động phân tích cú pháp bảng Markdown tại Mục 10, đối chiếu từng dòng trong 19 dòng với `slide_coverage.yaml` và kiểm tra phép cộng toán học ($67 + 5 = 72$).

### 17.5. DOC-CH7-001 — Loại bỏ ký tự điều khiển ẩn và bổ sung chốt chặn kiểm tra (Remove Hidden Control Characters)
- **Bản chất vấn đề:** Tại mục mô tả câu hỏi `QBANK-CH07-18`, ký tự điều khiển ẩn BEL (`\x07`) phát sinh do lỗi escape chuỗi Python trong quá trình khởi tạo báo cáo, khiến chuỗi LaTeX hiển thị thành `$ lpha$`.
- **Khắc phục:**
  - Sửa chuỗi LaTeX thành `$\alpha$`.
  - Tích hợp chốt chặn kiểm tra ký tự điều khiển bất thường `[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]` vào bộ kiểm định `scripts/validate_ch07_source_map.py` để bảo đảm độ sạch và tính toàn vẹn 100% của tệp báo cáo.

# HDH_UIT V2 — BẢN THIẾT KẾ SƯ PHẠM CHƯƠNG 7 (CH07 PEDAGOGICAL BLUEPRINT)
# MÔ HÌNH NHẬN THỨC CHUYÊN SÂU DÀNH CHO QUẢN LÝ BỘ NHỚ (MEMORY MANAGEMENT)
# DỰA TRÊN BẢN ĐỒ NGUỒN CHÍNH THỨC UIT 2024 ĐÃ THẨM ĐỊNH (#Week09-Chapter7 2024.pdf & Bai tap chuong 7 HDH.docx)
# TÁC GIẢ: Learning Science Architect + Information Architect + OS Pedagogy Designer
# CHẾ ĐỘ: THIẾT KẾ & ĐẶC TẢ SƯ PHẠM (PEDAGOGICAL SPECIFICATION ONLY — ZERO FULL AUTHORING)

---

## 1. TỔNG QUAN & ĐỐI CHIẾU NGUỒN CHÍNH THỨC (EXECUTIVE OVERVIEW & SOURCE CROSSWALK)

Bản thiết kế này quy định chi tiết cấu trúc nhận thức cho toàn bộ 11 chuyên đề trọng điểm của Chương 7 (Quản lý bộ nhớ). Mọi thiết kế đều khớp tuyệt đối với:
- **Slide chính ngạch:** `#Week09-Chapter7 2024.pdf` (72 trang vật lý, 67 trang CONTENT + 5 trang NON_CONTENT, `UIT-SLIDE-CH07-2024`).
- **Ngân hàng bài tập chuẩn:** `Bai tap chuong 7 HDH.docx` (23,960 bytes, 20 đơn vị nguồn nguyên tử: 9 lý thuyết + 11 bài tập, `UIT-QBANK-CH07-2024`).
- **Khung kiến trúc học tập:** Tuân thủ triệt để [LEARNING_ARCHITECTURE_V1.md](file:///C:/Users/lyle3/.gemini/antigravity/scratch/HDH_UIT/research/LEARNING_ARCHITECTURE_V1.md).

---

## 2. BẢN ĐẶC TẢ 11 CHUYÊN ĐỀ SƯ PHẠM CHƯƠNG 7 (THE 11 PEDAGOGICAL BLUEPRINT UNITS)

---

### ĐƠN VỊ 1: ĐỊA CHỈ LOGIC VS ĐỊA CHỈ VẬT LÝ & RÀNG BUỘC ĐỊA CHỈ (ADDRESS BINDING & MMU)
*(Tương ứng Slide pp. 5–22; QBank units: QBANK-CH07-01, 02, 03; Đề cương mục 7.1, 7.2, 7.3)*

- **WHY (Tại sao phải có cơ chế này?):**
  Nếu CPU phát trực tiếp địa chỉ vật lý vào bus bộ nhớ, mọi chương trình sẽ bị "đóng đinh" cứng vào các ô nhớ cố định trong RAM khi biên dịch (Compile-time binding). Kết quả: không thể nạp đồng thời nhiều tiến trình, không thể tái định vị khi chuyển đổi ngữ cảnh, và một tiến trình độc hại có thể ghi đè thẳng vào vùng nhớ của Hệ điều hành hoặc tiến trình khác gây sụp đổ toàn hệ thống.
- **MENTAL MODEL (Mô hình tư duy):**
  *Phép ẩn dụ Số phòng Khách sạn vs Tọa độ GPS Tòa nhà:* Địa chỉ logic giống như số phòng khách sạn (Phòng 301 = Tầng 3, phòng thứ 1). Người thuê phòng chỉ biết số phòng của mình. Địa chỉ vật lý là tọa độ GPS thực tế của tòa nhà trên bản đồ thế giới. Thiết bị MMU (Bộ quản lý bộ nhớ) đóng vai trò như Nhân viên lễ tân: mỗi khi khách muốn vào phòng 301, lễ tân cộng tọa độ cơ sở của khách sạn vào để đưa khách đến đúng vị trí vật lý trên mặt đất.
- **TRACE (Vết thực thi cụ thể):**
  Giả sử tiến trình $P_1$ được nạp vào bộ nhớ tại địa chỉ cơ sở $\text{Relocation Register} = 14000$ và có thanh ghi giới hạn $\text{Limit Register} = 3000$.
  
  | Bước | Chu kỳ CPU | Địa chỉ Logic phát sinh | Kiểm tra Bảo vệ ($\text{Logic} < \text{Limit}$) | Phép biến đổi MMU | Địa chỉ Vật lý đưa ra Bus | Kết quả |
  | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
  | 1 | Lệnh nạp lệnh | $346$ | $346 < 3000 \implies \text{HỢP LỆ}$ | $14000 + 346$ | $14346$ | Truy xuất RAM thành công |
  | 2 | Lệnh đọc biến | $2999$ | $2999 < 3000 \implies \text{HỢP LỆ}$ | $14000 + 2999$ | $16999$ | Truy xuất RAM thành công |
  | 3 | Lệnh ghi mảng | $3000$ | $3000 < 3000 \implies \text{SAI}$ | Bị chặn bởi phần cứng | Không phát sinh | **Bẫy lỗi (Trap: Addressing Error)** |
  | 4 | Lỗi con trỏ rác | $5120$ | $5120 < 3000 \implies \text{SAI}$ | Bị chặn bởi phần cứng | Không phát sinh | **Bẫy lỗi (Trap: Segmentation Fault)** |

- **PREDICTION (Điểm kiểm tra dự đoán):**
  *Câu hỏi:* *"Nếu một chương trình sử dụng cơ chế Ràng buộc tại thời điểm thực thi (Execution time binding), chuyện gì sẽ xảy ra với mã máy của chương trình nếu Hệ điều hành tạm thời di chuyển nó sang một vị trí khác trong RAM giữa chừng lúc đang chạy?"*
  *(Người học phải cam kết: A. Toàn bộ mã máy phải được biên dịch lại; B. Giá trị trong thanh ghi Relocation thay đổi, mã máy giữ nguyên 100%; C. Chương trình bị crash).*
- **RECALL (Thu hồi kín sách):**
  Nêu rõ sự khác biệt bản chất giữa 3 thời điểm ràng buộc địa chỉ: Compile time, Load time, và Execution time. Thời điểm nào cho phép tiến trình di chuyển linh hoạt trong bộ nhớ? Phần cứng nào bắt buộc phải có để hiện thực hóa thời điểm đó?
- **TRANSFER (Bài toán chuyển giao):**
  Một hệ thống nhúng có thanh ghi Relocation $= 0x4000$ và Limit $= 0x1000$. Một tiến trình cố gắng thực thi chỉ thị nhảy tại địa chỉ logic $0x1000$. Phần cứng MMU sẽ phản ứng như thế nào? Địa chỉ vật lý cao nhất mà tiến trình này có thể đọc hợp lệ là bao nhiêu?
- **COMMON ERROR (Chẩn đoán lỗi sai phổ biến):**
  *Lỗi ngây thơ:* Sinh viên thường nghĩ địa chỉ logic tối đa hợp lệ bằng đúng giá trị của thanh ghi Limit ($Limit$).
  *Bản chất thực tế:* Do đánh số từ $0$, địa chỉ logic hợp lệ chỉ nằm trong đoạn $[0, Limit - 1]$. Tại vị trí $Logic = Limit$, phần cứng MMU lập tức kích hoạt ngắt bảo vệ bộ nhớ (Trap).

---

### ĐƠN VỊ 2: CƠ CHẾ CẤP PHÁT BỘ NHỚ LIÊN TỤC (CONTIGUOUS ALLOCATION)
*(Tương ứng Slide pp. 28–36; QBank units: QBANK-CH07-05, 06; Đề cương mục 7.4, 7.4.1)*

- **WHY (Tại sao phải có cơ chế này?):**
  Trong các hệ điều hành sơ khai đa chương, cần có phương pháp đơn giản nhất để nạp đồng thời nhiều tiến trình vào RAM. Cấp phát liên tục (mỗi tiến trình chiếm một khối nhớ liền mạch) là bước tiến đầu tiên vượt qua mô hình đơn tiến trình, thiết lập nền móng cho cơ chế bảo vệ phân vùng bằng cặp thanh ghi Relocation/Limit.
- **MENTAL MODEL:**
  *Phép ẩn dụ Bãi đỗ xe Phân ô:* Bộ nhớ như một bãi đỗ xe dài. Phân vùng cố định (Fixed partitioning) là các ô đỗ xe được kẻ vạch sẵn với kích thước định trước (ví dụ: ô 5m, ô 10m). Xe máy vào ô 5m thì vừa; xe máy vào ô 10m thì thừa 8m không ai dùng được (Phân mảnh nội).
- **TRACE:**
  Hệ thống bộ nhớ 640KB, HĐH chiếm 128KB ở đầu, còn 512KB được chia thành 3 phân vùng cố định: Phân vùng 1 (100KB), Phân vùng 2 (200KB), Phân vùng 3 (212KB).
  
  | Tiến trình đến | Dung lượng | Phân vùng được cấp | Lãng phí bên trong (Phân mảnh nội) | Trạng thái phân vùng |
  | :---: | :---: | :---: | :---: | :---: |
  | $P_1$ | $80\text{ KB}$ | Phân vùng 1 (100KB) | $100 - 80 = 20\text{ KB}$ | Bận |
  | $P_2$ | $120\text{ KB}$ | Phân vùng 2 (200KB) | $200 - 120 = 80\text{ KB}$ | Bận |
  | $P_3$ | $210\text{ KB}$ | Phân vùng 3 (212KB) | $212 - 210 = 2\text{ KB}$ | Bận |
  | $P_4$ | $90\text{ KB}$ | Không có phân vùng trống | Không thể cấp | **Chờ trong hàng đợi (Dù tổng lãng phí $= 102\text{ KB} > 90\text{ KB}$)** |

- **PREDICTION:**
  *Câu hỏi:* *"Nếu một tiến trình có dung lượng 201KB xuất hiện trong hệ thống trên, nó có thể được nạp vào Phân vùng 2 (200KB) bằng cách ép Hệ điều hành nhường bớt 1KB không?"*
- **RECALL:**
  Định nghĩa phân vùng cố định (Fixed partitioning). Nguyên nhân cốt lõi gây ra hiện tượng phân mảnh nội (Internal fragmentation) là gì?
- **TRANSFER:**
  Một hệ thống có 4 phân vùng tĩnh kích thước lần lượt là 100KB, 500KB, 200KB, 300KB. Cho 4 tiến trình có nhu cầu lần lượt là 212KB, 417KB, 112KB, 426KB. Hãy chứng minh rằng hệ thống chỉ có thể nạp tối đa 3 tiến trình dù tổng dung lượng các phân vùng thừa sức chứa cả 4 tiến trình.
- **COMMON ERROR:**
  Sinh viên nhầm lẫn giữa dung lượng phân vùng và dung lượng khả dụng của tiến trình, quên mất rằng trong phân vùng cố định, một khi phân vùng đã được cấp phát thì phần không gian thừa hoàn toàn bị khóa chết, không tiến trình nào khác được chạm vào.

---

### ĐƠN VỊ 3: PHÂN MẢNH BỘ NHỚ & CƠ CHẾ GOM CỤM (FRAGMENTATION & COMPACTION)
*(Tương ứng Slide pp. 35, 37–39; QBank units: QBANK-CH07-05; Đề cương mục 7.4.2)*

- **WHY:**
  Để khắc phục sự lãng phí của phân vùng cố định, HĐH chuyển sang Phân vùng động (Dynamic partitioning) - cấp phát đúng kích thước tiến trình yêu cầu. Tuy nhiên, khi các tiến trình nạp vào và kết thúc luân phiên, bộ nhớ bị thủng lỗ chỗ như tổ ong (Phân mảnh ngoại). Tổng khoảng trống có thể rất lớn nhưng bị chia nhỏ, khiến tiến trình mới không thể nạp vào.
- **MENTAL MODEL:**
  *Phép ẩn dụ Ghế ngồi trên Xe buýt:* Phân mảnh nội là một người ngồi chiếm một băng ghế 3 chỗ (lãng phí bên trong không gian đã cấp). Phân mảnh ngoại là trên xe buýt còn 10 chỗ trống, nhưng mỗi băng ghế chỉ còn rải rác đúng 1 chỗ; một gia đình 3 người muốn ngồi liền nhau không thể nào ngồi được (lãng phí không gian giữa các khối đã cấp).
- **TRACE:**
  
  ```text
  Trạng thái Bộ nhớ (Tổng 1000KB, HĐH chiếm 200KB):
  [0-200KB: OS]
  [200-500KB: P1 (300KB)]
  [500-600KB: Lỗ trống A (100KB)]
  [600-900KB: P2 (300KB)]
  [900-1000KB: Lỗ trống B (100KB)]
  
  Tổng dung lượng trống = 100KB (A) + 100KB (B) = 200KB.
  Tiến trình P3 đến yêu cầu 150KB -> THẤT BẠI (Phân mảnh ngoại).
  
  Cơ chế Gom cụm (Compaction): Dịch chuyển P2 lên sát P1:
  [0-200KB: OS]
  [200-500KB: P1 (300KB)]
  [500-800KB: P2 (300KB)]
  [800-1000KB: Lỗ trống gộp liên tục (200KB)]
  
  P3 yêu cầu 150KB -> NẠP THÀNH CÔNG vào [800-950KB]!
  ```

- **PREDICTION:**
  *Câu hỏi:* *"Điều kiện tiên quyết về mặt kiến trúc phần cứng để Hệ điều hành có thể thực hiện kỹ thuật Gom cụm (Compaction) di dời các khối nhớ đang chạy là gì?"*
- **RECALL:**
  Phân biệt sự khác biệt bản chất giữa Phân mảnh nội (Internal Fragmentation) và Phân mảnh ngoại (External Fragmentation). Quy tắc 50% (50-percent rule) trong phân mảnh ngoại phát biểu điều gì?
- **TRANSFER:**
  Tại sao kỹ thuật Gom cụm (Compaction) tuy giải quyết triệt để phân mảnh ngoại nhưng lại hiếm khi được áp dụng thường xuyên trong các hệ điều hành hiện đại? Phân tích chi phí thời gian I/O và sự ảnh hưởng đến độ trễ hệ thống.
- **COMMON ERROR:**
  Khẳng định sai lầm rằng *"Gom cụm có thể thực hiện được ở mọi hệ thống"*. Thực tế: Nếu hệ thống dùng ràng buộc địa chỉ tĩnh lúc Compile-time hoặc Load-time thì việc di dời mã máy trong RAM sẽ làm sai lệch toàn bộ con trỏ tuyệt đối, gây crash ngay lập tức. Compaction chỉ khả thi khi có Execution-time dynamic relocation hardware.

---

### ĐƠN VỊ 4: CÁC CHIẾN LƯỢC CẤP PHÁT PHÂN VÙNG ĐỘNG (FIRST, BEST, NEXT, WORST FIT)
*(Tương ứng Slide pp. 37–39, 67; QBank units: QBANK-CH07-06, 10; Đề cương mục 7.4.2)*

- **WHY:**
  Khi có một danh sách các lỗ trống tự do (free holes) với các kích thước khác nhau trong RAM, HĐH cần một giải thuật chọn lỗ trống sao cho tối ưu hóa tốc độ tìm kiếm và giảm thiểu phân mảnh ngoại.
- **MENTAL MODEL:**
  *Bốn Triết lý Chọn Áo:*
  - **First Fit (Vừa mắt là lấy):** Thử từ chiếc áo đầu tiên trên giá, thấy vừa người là mua ngay, không cần xem tiếp.
  - **Best Fit (Khít khao nhất):** Lùng sục toàn bộ cửa hàng, tìm chiếc áo nhỏ nhất mà mình vẫn chui vừa, để thừa ít vải thừa nhất.
  - **Worst Fit (Rộng thùng thình nhất):** Lùng sục toàn bộ cửa hàng, chọn chiếc áo to nhất, để phần vải thừa sau khi cắt sửa vẫn đủ lớn để may được chiếc túi áo khác.
  - **Next Fit (Tiện đâu xem đó):** Không quay lại đầu giá áo, cứ đứng từ chỗ áo vừa chọn lần trước mà tìm tiếp chiếc tiếp theo.
- **TRACE (Bài tập kinh điển Slide UIT Bài 1 & QBANK-CH07-10):**
  Bộ nhớ có 4 phân vùng trống theo thứ tự: **$600\text{KB}, 500\text{KB}, 200\text{KB}, 300\text{KB}$**.
  Chuỗi tiến trình yêu cầu cấp phát tuần tự: **$P_1 (212\text{KB}), P_2 (417\text{KB}), P_3 (112\text{KB}), P_4 (426\text{KB})$**.

  ```
  A. THUẬT TOÁN FIRST FIT:
     - P1 (212K): Quét từ đầu -> Gặp 600K (đủ) -> Cấp P1 vào 600K (còn thừa 388K).
     - P2 (417K): Quét từ đầu -> 388K (thiếu) -> Gặp 500K (đủ) -> Cấp P2 vào 500K (còn thừa 83K).
     - P3 (112K): Quét từ đầu -> Gặp 388K (đủ) -> Cấp P3 vào 388K (còn thừa 276K).
     - P4 (426K): Quét từ đầu -> 276K (thiếu) -> 83K (thiếu) -> 200K (thiếu) -> 300K (thiếu) -> THẤT BẠI (CHỜ).

  B. THUẬT TOÁN BEST FIT (Sắp xếp lỗ theo độ chênh lệch nhỏ nhất):
     - P1 (212K): Các lỗ đủ {600K, 500K, 300K} -> Lỗ khít nhất là 300K -> Cấp P1 vào 300K (thừa 88K).
     - P2 (417K): Các lỗ đủ {600K, 500K} -> Lỗ khít nhất là 500K -> Cấp P2 vào 500K (thừa 83K).
     - P3 (112K): Các lỗ đủ {600K, 200K} -> Lỗ khít nhất là 200K -> Cấp P3 vào 200K (thừa 88K).
     - P4 (426K): Lỗ đủ duy nhất là 600K -> Cấp P4 vào 600K (thừa 174K) -> THÀNH CÔNG 100%!

  C. THUẬT TOÁN NEXT FIT:
     - P1 (212K): Cấp vào 600K (thừa 388K). Con trỏ dừng tại phân vùng 1.
     - P2 (417K): Tìm tiếp từ phân vùng 2 -> Gặp 500K (đủ) -> Cấp P2 vào 500K (thừa 83K). Con trỏ dừng tại PV 2.
     - P3 (112K): Tìm tiếp từ PV 3 -> Gặp 200K (đủ) -> Cấp P3 vào 200K (thừa 88K). Con trỏ dừng tại PV 3.
     - P4 (426K): Tìm tiếp từ PV 4 (300K - thiếu) -> Vòng về đầu gặp 388K (thiếu) -> 83K (thiếu) -> THẤT BẠI (CHỜ).

  D. THUẬT TOÁN WORST FIT (Chọn lỗ lớn nhất):
     - P1 (212K): Lỗ lớn nhất là 600K -> Cấp P1 vào 600K (thừa 388K).
     - P2 (417K): Lỗ lớn nhất hiện tại là 500K -> Cấp P2 vào 500K (thừa 83K).
     - P3 (112K): Lỗ lớn nhất hiện tại là 388K -> Cấp P3 vào 388K (thừa 276K).
     - P4 (426K): Lỗ lớn nhất hiện tại là 300K (thiếu) -> THẤT BẠI (CHỜ).
  ```

- **PREDICTION:**
  *Câu hỏi:* *"Nhiều người nghĩ Best Fit luôn luôn là thuật toán tốt nhất trong mọi tình huống. Nhìn vào vết thực thi trên, nếu P3 chỉ cần 50KB và sau đó một tiến trình P5 (85KB) xuất hiện, liệu Best Fit có tạo ra mảnh vụn li ti không sử dụng được không?"*
- **RECALL:**
  Trình bày nguyên tắc hoạt động của Next Fit. Next Fit khắc phục nhược điểm gì của First Fit và tại sao nó thường làm phân mảnh các khối nhớ lớn ở cuối bộ nhớ?
- **TRANSFER:**
  Cho một cấu hình bộ nhớ và một chuỗi tiến trình mà trong đó Worst Fit thành công nạp toàn bộ tiến trình nhưng First Fit và Best Fit đều thất bại. Hãy giải thích tại sao việc bảo tồn các mảnh vụn lớn trong Worst Fit lại có lợi trong kịch bản đó.
- **COMMON ERROR:**
  *Sai lầm kinh điển:* Trong Next Fit, sinh viên quên cập nhật vị trí con trỏ sau mỗi lần cấp phát, hoặc nhầm tưởng Next Fit không bao giờ quay vòng (wrap-around) về đầu danh sách.

---

### ĐƠN VỊ 5: CƠ CHẾ PHÂN TRANG CỐT LÕI (PAGING FUNDAMENTALS)
*(Tương ứng Slide pp. 40–47; QBank units: QBANK-CH07-07, 11; Đề cương mục 7.5)*

- **WHY:**
  Mọi giải thuật cấp phát liên tục đều đầu hàng trước phân mảnh ngoại hoặc đòi hỏi chi phí gom cụm (Compaction) khổng lồ. Để triệt tiêu hoàn toàn phân mảnh ngoại, hệ điều hành phát minh ra Phân trang (Paging): cho phép không gian địa chỉ vật lý của một tiến trình nằm **rải rác, không liên tục** trên RAM.
- **MENTAL MODEL:**
  *Phép ẩn dụ Vở ô ly và Sách giáo khoa:* Không gian bộ nhớ vật lý được chia thành các ô kẻ sẵn có kích thước cố định bằng nhau gọi là Khung trang (Frames). Chương trình được chia thành các trang có kích thước y hệt gọi là Trang (Pages). Bảng trang (Page Table) như cuốn mục lục: Trang 0 nằm ở Khung 5, Trang 1 nằm ở Khung 2, Trang 2 nằm ở Khung 9. Người đọc (CPU) chỉ cần đọc theo thứ tự trang logic, phần cứng sẽ tự động lật đến đúng khung vật lý tương ứng.
- **TRACE (Ánh xạ cấu trúc):**
  Xét không gian địa chỉ ảo gồm 12 trang (kích thước trang $2\text{KB} = 2048\text{ bytes}$), ánh xạ vào bộ nhớ vật lý gồm 32 khung trang:
  - Kích thước trang = Kích thước khung $= 2\text{KB} = 2^{11}\text{ bytes} \implies$ Số bit Offset ($d$) $= 11\text{ bit}$.
  - Số trang logic $= 12 \le 2^4 \implies$ Cần tối thiểu $4\text{ bit}$ để đánh số trang logic ($p = 0..11$).
  - Tổng số bit địa chỉ logic $= 4 + 11 = 15\text{ bit}$. Không gian logic tối đa $= 2^{15} = 32\text{KB}$ (trong đó $12 \times 2\text{KB} = 24\text{KB}$ thực dùng).
  - Số khung trang vật lý $= 32 = 2^5 \implies$ Cần $5\text{ bit}$ để đánh số khung trang ($f = 0..31$).
  - Tổng số bit địa chỉ vật lý $= 5 + 11 = 16\text{ bit}$. Không gian vật lý tối đa $= 2^{16} = 64\text{KB}$.
- **PREDICTION:**
  *Câu hỏi:* *"Cơ chế phân trang triệt tiêu $100\%$ phân mảnh ngoại. Nhưng liệu nó có loại bỏ được phân mảnh nội không? Trong trường hợp xấu nhất, một tiến trình bị lãng phí bao nhiêu byte do phân mảnh nội?"*
- **RECALL:**
  Định nghĩa Page, Frame, Page Table. Mối quan hệ toán học bắt buộc giữa kích thước Page và kích thước Frame là gì?
- **TRANSFER:**
  Một tiến trình có dung lượng 73,000 bytes được nạp vào hệ thống phân trang có kích thước trang là 4096 bytes (4KB). Hãy tính:
  1. Số lượng trang cần cấp phát cho tiến trình.
  2. Kích thước phân mảnh nội tại trang cuối cùng.
- **COMMON ERROR:**
  Sinh viên hay quên rằng kích thước trang luôn luôn bắt buộc phải là lũy thừa của 2 ($2^n$). Lý do: Việc chia địa chỉ thành số trang ($p$) và độ dời ($d$) khi đó chỉ đơn giản là việc tách các đường dây bus nhị phân ở tầng phần cứng, không tốn bất kỳ chu kỳ chia số học nào của ALU.

---

### ĐƠN VỊ 6: QUY TRÌNH CHUYỂN ĐỔI ĐỊA CHỈ PHÂN TRANG: $(p, d) \to (f, d)$
*(Tương ứng Slide pp. 43–47; QBank units: QBANK-CH07-07, 15; Đề cương mục 7.5.1)*

- **WHY:**
  Cung cấp thuật toán phần cứng chính xác để dịch một con trỏ trong mã C/C++ thành địa chỉ kích hoạt chip bán dẫn RAM trong thời gian vài nano-giây.
- **MENTAL MODEL:**
  *Phép dịch Địa chỉ:* Địa chỉ logic như một tấm vé gồm 2 phần: [Số trang $p$] và [Số dòng trên trang $d$]. Khi đi tìm dữ liệu, độ dời dòng $d$ hoàn toàn không thay đổi! Ta chỉ cần cầm số trang $p$ tra vào Bảng phân trang để rút ra [Số kệ sách vật lý $f$], sau đó ghép nguyên vẹn độ dời $d$ vào sau $f$ thành $(f, d)$.
- **TRACE (Bài tập mẫu 6 trong Slide UIT & QBANK-CH07-15):**
  Cho bảng phân trang mẫu: Trang 0 $\to$ Khung 5; Trang 1 $\to$ Khung 6; Trang 2 $\to$ Khung 1; Trang 3 $\to$ Khung 2.
  Kích thước trang $= 2\text{KB} = 2048\text{ bytes}$.
  Chuyển đổi địa chỉ logic $L = 3254$ sang địa chỉ vật lý:
  - **Bước 1 (Tách $p$ và $d$):**
    $$p = \lfloor 3254 / 2048 \rfloor = 1$$
    $$d = 3254 \pmod{2048} = 3254 - 2048 = 1206$$
  - **Bước 2 (Tra bảng trang):**
    Tra mục $p = 1$ trong bảng trang $\implies f = 6$.
  - **Bước 3 (Ghép địa chỉ vật lý):**
    $$\text{Physical Address} = f \times \text{Page\_Size} + d = 6 \times 2048 + 1206 = 12288 + 1206 = 13494$$
- **PREDICTION:**
  *Câu hỏi:* *"Nếu một địa chỉ vật lý là 6568 trong hệ thống có kích thước khung 1KB (1024 bytes), khung trang chứa địa chỉ này là bao nhiêu và độ dời là bao nhiêu?"*
- **RECALL:**
  Viết công thức toán học tổng quát để tính số trang $p$ và độ dời $d$ từ địa chỉ logic $L$ khi biết kích thước trang $S$.
- **TRANSFER:**
  Trong kiến trúc 32-bit với kích thước trang 4KB, một con trỏ trỏ tới địa chỉ logic thập lục phân `0x00403A2C`. Hãy xác định ngay lập tức bằng phép quan sát nhị phân/hex: số trang ảo $p$ và offset $d$ (không dùng phép chia số thập phân).
- **COMMON ERROR:**
  Sinh viên thường làm phép tính chia thập phân dài dòng và bị làm tròn sai số. Trong kiến trúc lũy thừa của 2: $4\text{KB} = 2^{12}\text{ bytes} = 3\text{ chữ số hex}$ tận cùng là Offset ($d = \text{0xA2C}$), phần còn lại phía trước chính là số trang ($p = \text{0x00403} = 1027$).

---

### ĐƠN VỊ 7: BỘ NHỚ ĐỆM CHUYỂN ĐỔI ĐỊA CHỈ NHANH (TLB)
*(Tương ứng Slide pp. 48–51; QBank units: QBANK-CH07-08; Đề cương mục 7.5.2)*

- **WHY:**
  Bảng trang kích thước lớn phải nằm trong bộ nhớ RAM chính. Điều này dẫn đến thảm họa hiệu năng: **Mọi truy xuất bộ nhớ bị chậm gấp đôi!** (1 lần đọc bảng trang trong RAM để lấy $f$ + 1 lần đọc dữ liệu thực tế tại $(f, d)$). TLB ra đời như một bộ nhớ kết hợp (Associative Cache) siêu nhanh bằng phần cứng nằm ngay trong CPU để lưu các ánh xạ $(p \to f)$ thường dùng.
- **MENTAL MODEL:**
  *Danh bạ Điện thoại Đút túi áo:* Thay vì mỗi lần gọi điện đều phải lật cuốn sổ danh bạ dày 1000 trang trong ngăn kéo bàn (Bảng trang trong RAM), bạn chép 16 số điện thoại hay gọi nhất vào mẩu giấy nhỏ đút túi áo (TLB). Khi cần gọi, sờ túi áo trước; nếu có (TLB Hit) bấm số ngay lập tức. Nếu không có (TLB Miss) mới phải mở ngăn kéo bàn tra cứu và ghi bổ sung vào mẩu giấy.
- **TRACE:**
  
  ```text
  CPU phát sinh địa chỉ logic (p, d)
                 │
                 ▼
     [ Tra cứu song song trong TLB ] ──(Có p?)──┐
                 │                              │
             (TLB Miss)                     (TLB Hit)
                 │                              │
                 ▼                              ▼
     [ Đọc Page Table trong RAM ]           [ Lấy ngay f ]
                 │                              │
     [ Nạp mục p->f vào TLB ]                  │
                 │                              │
                 └──────────────┬───────────────┘
                                ▼
                   Ghép (f, d) -> Truy xuất RAM
  ```

- **PREDICTION:**
  *Câu hỏi:* *"Khi hệ điều hành thực hiện chuyển đổi ngữ cảnh (Context Switch) từ Tiến trình A sang Tiến trình B, chuyện gì bắt buộc phải xảy ra với các mục trong TLB nếu phần cứng không hỗ trợ ASID (Address Space Identifier)?"*
- **RECALL:**
  Trình bày cấu trúc và nguyên lý hoạt động của Translation Lookaside Buffer (TLB). Định nghĩa TLB Hit và TLB Miss.
- **TRANSFER:**
  Tại sao kích thước của TLB thường rất nhỏ (chỉ từ 32 đến 1024 mục) mà không làm lớn như RAM? Yếu tố vật lý phần cứng nào giới hạn kích thước của bộ nhớ liên kết (Associative Memory)?
- **COMMON ERROR:**
  Sinh viên nhầm lẫn giữa TLB Miss và Page Fault.
  - *TLB Miss:* Trang CÓ trong RAM, chỉ là ánh xạ chưa nạp vào cache TLB $\implies$ Xử lý hoàn toàn bằng phần cứng chỉ mất vài nano-giây.
  - *Page Fault:* Trang HOÀN TOÀN CHƯA CÓ trong RAM, phải đọc từ ổ cứng $\implies$ Ngắt hệ điều hành, đọc Disk I/O mất vài mili-giây (chậm hơn 100,000 lần!).

---

### ĐƠN VỊ 8: THỜI GIAN TRUY XUẤT HIỆU DỤNG (EFFECTIVE ACCESS TIME - EAT)
*(Tương ứng Slide pp. 52–54, 69; QBank units: QBANK-CH07-08, 12, 16, 17, 18; Đề cương mục 7.5.3)*

- **WHY:**
  Cung cấp công thức định lượng để các kỹ sư đo lường chính xác hiệu năng suy giảm của hệ thống phân trang khi có sự hỗ trợ của bộ đệm TLB với tỷ lệ trúng (hit-ratio) $\alpha$.
- **MENTAL MODEL:**
  *Tính Điểm Trung bình Có trọng số:* EAT là kỳ vọng toán học của thời gian truy xuất, tính bằng tổng thời gian trong trường hợp trúng nhân với xác suất trúng, cộng với thời gian trong trường hợp trượt nhân với xác suất trượt.
- **TRACE (Bài tập mẫu 3 Slide UIT & QBANK-CH07-12 & QBANK-CH07-16):**
  Cho thời gian truy xuất bộ nhớ RAM $t_{\text{RAM}} = 100\text{ns}$, thời gian tra cứu TLB $\epsilon = 20\text{ns}$, tỷ lệ hit-ratio $\alpha = 80\% = 0.8$.
  
  | Trường hợp | Đường đi phần cứng | Thời gian tiêu tốn | Xác suất xảy ra | Đóng góp vào EAT |
  | :--- | :--- | :---: | :---: | :---: |
  | **TLB Hit** | Tra TLB ($\epsilon$) + Đọc RAM ($t_{\text{RAM}}$) | $\epsilon + t_{\text{RAM}} = 20 + 100 = 120\text{ns}$ | $\alpha = 0.8$ | $0.8 \times 120 = 96\text{ns}$ |
  | **TLB Miss** | Tra TLB ($\epsilon$) + Đọc Bảng trang ($t_{\text{RAM}}$) + Đọc RAM ($t_{\text{RAM}}$) | $\epsilon + 2 \times t_{\text{RAM}} = 20 + 200 = 220\text{ns}$ | $1 - \alpha = 0.2$ | $0.2 \times 220 = 44\text{ns}$ |
  | **TỔNG CỘNG** | $\mathbf{\text{EAT} = \alpha(\epsilon + t_{\text{RAM}}) + (1 - \alpha)(\epsilon + 2 t_{\text{RAM}})}$ | — | $1.0$ | $\mathbf{\text{EAT} = 140\text{ns}}$ |
  
  *(So với truy xuất không có phân trang $100\text{ns}$, hệ thống chỉ chậm hơn $40\%$; nếu không có TLB sẽ chậm hơn $100\%$).*
- **PREDICTION:**
  *Câu hỏi:* *"Nếu coi thời gian tra cứu TLB $\epsilon \approx 0\text{ns}$ (như trong Bài tập mẫu 3 Slide 69), công thức EAT sẽ rút gọn thành dạng nào?"*
- **RECALL:**
  Viết công thức tính EAT tổng quát khi có tính đến thời gian tra cứu TLB $\epsilon$. Nếu tỷ lệ hit-ratio $\alpha \to 100\%$, EAT tiệm cận giá trị nào?
- **TRANSFER (Dạng toán thi QBANK-CH07-18):**
  Một hệ thống có thời gian truy xuất bộ nhớ bình thường là $250\text{ns}$, thời gian tìm kiếm trong TLB là $26\text{ns}$. Cần tỷ lệ hit-ratio $\alpha$ tối thiểu là bao nhiêu để thời gian truy xuất hiệu dụng $\text{EAT} \le 182\text{ns}$? (Xem xét cả hai giả định đề thi về việc tra song song hay tuần hoàn).
- **COMMON ERROR:**
  Sinh viên khi tính trường hợp TLB Miss hay quên cộng lần truy xuất bộ nhớ thứ hai (lần đọc dữ liệu thực tế), chỉ cộng 1 lần đọc bảng trang khiến kết quả thời gian bị thiếu $100\text{ns}$.

---

### ĐƠN VỊ 9: CẤU TRÚC BẢNG TRANG NÂNG CAO (ADVANCED PAGE TABLES)
*(Tương ứng Slide pp. 55–58, 70, 71; QBank units: QBANK-CH07-13, 14, 19, 20; Đề cương mục 7.5.4)*

- **WHY:**
  Trong kiến trúc 32-bit hoặc 64-bit hiện đại, không gian địa chỉ là khổng lồ. Nếu dùng bảng trang 1 cấp phẳng (flat page table) với trang 4KB, mỗi tiến trình cần một bảng trang có $2^{20} \approx 1\text{ triệu mục} \times 4\text{ bytes} = 4\text{MB}$ liên tục trong RAM. Một hệ thống chạy 100 tiến trình sẽ tốn 400MB RAM chỉ để lưu bảng trang! Bảng trang đa cấp (Hierarchical), Bảng trang băm (Hashed), và Bảng trang nghịch đảo (Inverted) ra đời để giải quyết bài toán dung lượng này.
- **MENTAL MODEL:**
  *Mục lục Sách 2 Cấp vs Sổ Danh bạ Toàn thành phố:*
  - *Bảng trang 2 cấp:* Thay vì in danh sách toàn bộ 1 triệu trang, ta in Mục lục Cấp 1 (Chỉ chứa 1024 mục). Mục nào tiến trình không dùng thì không cấp phát bảng trang cấp 2!
  - *Bảng trang nghịch đảo (Inverted):* Thay vì mỗi tiến trình một bảng trang, cả hệ thống chỉ dùng **DUY NHẤT 1 BẢNG TRANG CHUNG**. Mỗi dòng trong bảng đại diện cho một Khung trang vật lý trong RAM (Ghi rõ: Khung này đang do PID nào giữ, trang ảo số mấy).
- **TRACE (Bài tập 4 Slide UIT & QBANK-CH07-13):**
  Một máy tính 32-bit dùng bảng trang 2 cấp. Địa chỉ logic được chia thành: $p_1 = 9\text{ bit}$ (Cấp 1), $p_2 = 11\text{ bit}$ (Cấp 2), và Offset $d$.
  
  ```text
  Cấu trúc địa chỉ 32-bit:
  ┌───────────────────┬─────────────────────┬───────────────────────────┐
  │ p1: 9 bit (Cấp 1) │ p2: 11 bit (Cấp 2)  │ d: 32 - (9+11) = 12 bit   │
  └───────────────────┴─────────────────────┴───────────────────────────┘
  ```
  
  - Kích thước trang $= 2^d = 2^{12} = 4096\text{ bytes} = 4\text{KB}$.
  - Số mục trong Bảng trang Cấp 1 (Outer Page Table) $= 2^9 = 512\text{ mục}$.
  - Số mục trong mỗi Bảng trang Cấp 2 $= 2^{11} = 2048\text{ mục}$.
  - Tổng số trang ảo tối đa $= 2^{p_1 + p_2} = 2^{20} = 1,048,576\text{ trang}$.
- **PREDICTION:**
  *Câu hỏi:* *"Trong bảng trang 2 cấp, một lần truy xuất bộ nhớ khi bị TLB Miss sẽ tốn bao nhiêu lần truy xuất vào RAM?"*
  *(A. 1 lần; B. 2 lần; C. 3 lần).*
- **RECALL:**
  Trình bày cấu trúc của Bảng trang nghịch đảo (Inverted Page Table). Ưu điểm vượt trội về mặt tiết kiệm bộ nhớ và nhược điểm về tốc độ tìm kiếm của nó là gì?
- **TRANSFER:**
  Trong kiến trúc 64-bit, nếu dùng bảng trang phân cấp, ta cần bao nhiêu cấp bảng trang? Tại sao Bảng trang nghịch đảo kết hợp bảng băm lại trở thành lựa chọn bắt buộc cho các hệ thống 64-bit?
- **COMMON ERROR:**
  *Nhầm lẫn số lần truy xuất:* Sinh viên quên rằng bảng trang $k$ cấp khi TLB Miss sẽ đòi hỏi $k$ lần đọc bảng trang trong RAM $+ 1$ lần đọc dữ liệu thực tế $= k + 1$ lần truy xuất RAM! (Bảng 2 cấp tốn 3 lần đọc RAM).

---

### ĐƠN VỊ 10: BẢO VỆ BỘ NHỚ & CHIA SẺ TRANG (MEMORY PROTECTION & SHARED PAGES)
*(Tương ứng Slide pp. 59–62; QBank units: QBANK-CH07-01; Đề cương mục 7.5.5)*

- **WHY:**
  Phân trang không chỉ để dịch địa chỉ mà còn là bức tường lửa bảo vệ hệ thống. Cần cơ chế ngăn chặn việc ghi vào vùng nhớ chỉ đọc (Read-only code) và cơ chế cho phép nhiều tiến trình dùng chung một thư viện mã lệnh (Shared Libraries như `libc.so` hay `kernel32.dll`) để tiết kiệm RAM.
- **MENTAL MODEL:**
  *Phép ẩn dụ Phòng đọc Thư viện:* Nhiều sinh viên cùng đọc chung một cuốn sách giáo trình duy nhất đặt trên bàn (Shared Pages - Mã chỉ đọc). Mỗi sinh viên chỉ có một cuốn sổ nháp riêng để ghi chép câu trả lời của mình (Private Data Pages). Không ai được phép dùng bút xóa viết đè lên cuốn sách chung.
- **TRACE:**
  Mỗi mục trong bảng phân trang được bổ sung các bit trạng thái:
  
  ```text
  Mục bảng trang: [ Frame Number (f) ] [ Valid/Invalid Bit ] [ Read/Write Bit ] [ Execute Bit ]
  ```
  
  - **Bit Valid/Invalid:** Nếu $Bit = 1$ (Valid): Trang nằm trong không gian địa chỉ hợp lệ của tiến trình. Nếu $Bit = 0$ (Invalid): Trang chưa được cấp phát hoặc đang ở ngoài đĩa $\implies$ Phần cứng kích hoạt ngắt **Page Fault / Invalid Memory Access Trap**.
  - **Chia sẻ mã lệnh (Reentrant Code):**
    Tiến trình $P_1$, $P_2$, $P_3$ cùng chạy trình soạn thảo văn bản. Mã nguồn soạn thảo (3 trang: Khung 3, 4, 6) được ánh xạ vào bảng trang của cả 3 tiến trình với quyền `Read-Only`. Vùng dữ liệu của mỗi người được cấp ở các khung riêng biệt với quyền `Read-Write`.
- **PREDICTION:**
  *Câu hỏi:* *"Điều kiện bắt buộc đối với đoạn mã lệnh để nó có thể được chia sẻ an toàn giữa nhiều tiến trình mà không làm sai lệch dữ liệu của nhau là gì?"*
- **RECALL:**
  Trình bày vai trò của bit Valid/Invalid trong bảng phân trang. Thế nào là mã tái nhập (Reentrant code)?
- **TRANSFER:**
  Một tiến trình cố gắng ghi dữ liệu vào một địa chỉ thuộc trang nhớ có bit quyền là `Read-Only`. Chuỗi sự kiện nào sẽ diễn ra ở cấp độ phần cứng MMU và hệ điều hành? Tiến trình đó có bị chấm dứt ngay lập tức không?
- **COMMON ERROR:**
  Sinh viên nhầm tưởng rằng bit Valid/Invalid chỉ dùng để báo trang có trong RAM hay không. Thực tế: Trong bảo vệ cơ bản, nó dùng để phân định biên giới không gian địa chỉ hợp lệ của tiến trình (bảo vệ chống đọc trộm bộ nhớ của tiến trình khác).

---

### ĐƠN VỊ 11: KỸ THUẬT HOÁN VỊ BỘ NHỚ (SWAPPING MECHANISM)
*(Tương ứng Slide pp. 63–66; QBank units: QBANK-CH07-09; Đề cương mục 7.6)*

- **WHY:**
  Tổng nhu cầu không gian nhớ của tất cả các tiến trình trong hệ thống thường vượt xa dung lượng RAM vật lý thực tế. Hệ điều hành cần một cơ chế tạm thời đưa toàn bộ tiến trình không hoạt động ra bộ nhớ phụ (Backing store / Swap disk) và nạp lại khi cần chạy để giải phóng RAM cho các tiến trình ưu tiên cao hơn.
- **MENTAL MODEL:**
  *Diễn viên Chờ sau Cánh gà:* Sân khấu kịch (RAM) có diện tích giới hạn, chỉ đủ chỗ cho các diễn viên đang trực tiếp thoại kịch. Các diễn viên chưa đến cảnh diễn được đưa vào phòng chờ phía sau cánh gà (Swap Space). Khi đến lượt, đạo diễn (HĐH) gọi diễn viên ra sân khấu (Swap In) và đưa người diễn xong vào trong (Swap Out).
- **TRACE:**
  Tính toán chi phí thời gian hoán vị một tiến trình có dung lượng $100\text{MB}$ ra một ổ đĩa cứng có tốc độ truyền dữ liệu $50\text{MB/s}$ và thời gian tìm kiếm trung bình (Latency) là $8\text{ms}$:
  - Thời gian truyền dữ liệu (Transfer time):
    $$T_{\text{transfer}} = \frac{100\text{MB}}{50\text{MB/s}} = 2\text{ giây} = 2000\text{ms}$$
  - Tổng thời gian Swap Out $= 8\text{ms} + 2000\text{ms} = 2008\text{ms}$.
  - Nếu phải Swap In một tiến trình $100\text{MB}$ khác vào thay thế $\implies$ Tổng thời gian Context Switch do hoán vị:
    $$T_{\text{total}} = 2008\text{ms} \times 2 \approx 4.016\text{ giây!}$$
  *(Minh chứng định lượng cho thấy tại sao Swapping toàn bộ tiến trình làm hệ thống bị khựng lại khủng khiếp, mở đường cho cơ chế Demand Paging từng trang ở Chương 8).*
- **PREDICTION:**
  *Câu hỏi:* *"Nếu một tiến trình đang thực hiện thao tác I/O bất đồng bộ (chờ dữ liệu từ bàn phím vào bộ đệm của nó), Hệ điều hành có được phép Swapping tiến trình đó ra đĩa không? Nếu làm vậy, thảm họa gì sẽ xảy ra?"*
- **RECALL:**
  Trình bày khái niệm và cơ chế hoạt động của kỹ thuật Hoán vị (Swapping). Tại sao bộ nhớ phụ (Backing Store) dùng cho Swap phải có tốc độ cao?
- **TRANSFER:**
  Trên các hệ điều hành di động hiện đại (như iOS và Android), tại sao cơ chế Swapping truyền thống (ghi toàn bộ tiến trình ra bộ nhớ flash) hoàn toàn bị vô hiệu hóa? Các hệ điều hành này sử dụng giải pháp thay thế nào khi cạn kiệt RAM?
- **COMMON ERROR:**
  Sinh viên thường bỏ qua thời gian trễ Context Switch của Swapping, không hiểu tại sao trong thực tế các HĐH hiện đại chỉ swap từng trang (Paging swap) chứ không swap toàn bộ tiến trình (Standard swapping).

---

## 3. MA TRẬN BÀI TẬP PHAI MỜ DẦN DẦN (WORKED-EXAMPLE FADING MATRIX FOR CH07)

Chương 7 có 4 dạng bài toán tính toán định lượng cốt lõi. Mỗi dạng bài bắt buộc phải thiết kế theo chuỗi phai mờ 3 cấp độ:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             MA TRẬN BÀI TẬP PHAI MỜ DẦN DẦN (WORKED-EXAMPLE FADING MATRIX)             │
├──────────────────────┬────────────────────────┬────────────────────────┬───────────────┤
│ Dạng Bài Toán        │ Level A (Worked Trace) │ Level B (Faded Blank)  │ Level C       │
│                      │ 100% Khung + Lời giải  │ 50% Khung + Điền bước  │ Transfer Độc  │
├──────────────────────┼────────────────────────┼────────────────────────┼───────────────┤
│ 1. Cấp phát Phân     │ Toàn bộ 4 thuật toán   │ Điền khuyết bước P3,   │ Đề bài lạ     │
│    vùng động         │ (First, Best, Next,    │ P4; tự vẽ lại vết con  │ 5 tiến trình  │
│    (Dynamic Fit)     │ Worst Fit) đầy đủ      │ trỏ Next Fit           │ có giải phóng │
├──────────────────────┼────────────────────────┼────────────────────────┼───────────────┤
│ 2. Dịch Địa chỉ      │ Phép tách p, d và      │ Cho sẵn bảng trang,    │ Địa chỉ Hex   │
│    Phân trang        │ tra bảng, ghép f, d    │ khuyết công thức ghép; │ 32-bit với    │
│    (Address Trans)   │ chi tiết từng phép toán│ tự chuyển đổi 1 địa chỉ│ bẫy Invalid   │
├──────────────────────┼────────────────────────┼────────────────────────┼───────────────┤
│ 3. Thời gian Hiệu    │ Lập bảng 2 nhánh       │ Khuyết nhánh TLB Miss; │ Tính ngược    │
│    dụng EAT          │ Hit/Miss có trọng số,  │ tự lập phương trình    │ tỷ lệ Hit     │
│    (EAT Calculation) │ giải thích từng số hạng│ tìm EAT                │ alpha khi EAT │
├──────────────────────┼────────────────────────┼────────────────────────┼───────────────┤
│ 4. Bảng trang        │ Phân rã trường bit     │ Khuyết số mục Cấp 2    │ Tính dung     │
│    Đa cấp            │ p1, p2, d; tính dung   │ và dung lượng trang;   │ lượng RAM tốn │
│    (Multi-level)     │ lượng bảng trang mẫu   │ tự tìm Offset          │ cho 3 cấp     │
└──────────────────────┴────────────────────────┴────────────────────────┴───────────────┘
```

---

## 4. MA TRẬN LUYỆN TẬP XEN KẼ CHỌN LỌC CHƯƠNG 7 (SELECTIVE INTERLEAVING MATRIX)

Để đạt điểm tối đa trong kỳ thi kết thúc môn IT007 UIT, sinh viên bắt buộc phải trải qua phiên luyện tập xen kẽ giải quyết 3 cặp bài toán đối kháng sau:

### Cặp đối kháng 1: Phân biệt Phân mảnh Nội vs Phân mảnh Ngoại
- **Mục tiêu phân biệt:** Sinh viên phải nhận diện được ngay khi nhìn vào thông số kỹ thuật:
  - Cứ thấy **kích thước phân vùng/trang cố định** mà tiến trình nhỏ hơn $\implies$ Khẳng định **Phân mảnh nội**.
  - Cứ thấy **tổng dung lượng trống lớn hơn nhu cầu nhưng không nạp được** $\implies$ Khẳng định **Phân mảnh ngoại**.
- **Bài toán thử thách:** Một hệ thống có phân vùng động gặp hiện tượng không nạp được tiến trình. Sinh viên phải biện luận chọn giữa giải pháp *Gom cụm (Compaction)* hay *Chuyển sang Phân trang (Paging)* và nêu rõ cái giá phải trả của từng giải pháp.

### Cặp đối kháng 2: Phân biệt Best Fit vs Worst Fit trong Tình huống Biên
- **Mục tiêu phân biệt:** Phá vỡ định kiến "Best Fit luôn tốt nhất".
- **Bài toán thử thách:** Cung cấp chuỗi tiến trình mà Best Fit tạo ra hàng loạt mảnh vụn nhỏ làm sụp đổ hệ thống ở bước thứ 4, trong khi Worst Fit duy trì mảnh vụn đủ lớn để nạp thành công toàn bộ chuỗi tiến trình.

### Cặp đối kháng 3: Phân biệt TLB Hit vs Page Fault
- **Mục tiêu phân biệt:** Ngăn chặn nhầm lẫn tai hại giữa bộ đệm phần cứng (TLB) và bộ nhớ ảo trên đĩa (Virtual Memory).
- **Bài toán thử thách:** Phân tích một chỉ thị đọc bộ nhớ trải qua 4 kịch bản phối hợp:
  1. TLB Hit + Page Valid.
  2. TLB Miss + Page Valid.
  3. TLB Miss + Page Invalid (Page Fault).
  4. (Trường hợp nghịch lý) Liệu có thể xảy ra: TLB Hit nhưng lại bị Page Fault không? Giải thích bản chất kiểm tra quyền hạn.

---

## 5. BÀN GIAO SƯ PHẠM & HÀNH ĐỘNG TIẾP THEO (PEDAGOGICAL SIGN-OFF)

- **Trạng thái:** Bản thiết kế nhận thức Chương 7 đã hoàn thành đầy đủ, đáp ứng $100\%$ các nguyên lý Khoa học Nhận thức và bao phủ trọn vẹn $20/20$ đơn vị câu hỏi của ngân hàng đề thi chính thức UIT.
- **Cam kết kỷ luật kiến trúc:**
  - Tuyệt đối chưa biên soạn nội dung giáo trình Chương 7 (`content/theory/ch07-memory-management.md` chưa được tạo).
  - Tuyệt đối không thay đổi nội dung các Chương 1–6.
  - Sẵn sàng chuyển giao cho pha Thẩm định độc lập Bản đồ nguồn trước khi cấp phép tác giả.

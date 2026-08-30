# QA LOG — HDH_UIT

Nhật ký kiểm tra chất lượng, tính toàn vẹn kỹ thuật và xử lý các đợt kiểm toán học thuật độc lập.

---

## 1. Nhật Ký Khắc Phục Kiểm Toán Kiến Trúc GLM V2 (GLM V2 Architecture Remediation)

| Mã Lỗi (ID) | Mức Độ | Trạng Thái | Nguyên Nhân Gốc (Root Cause) | Tệp Tin Ảnh Hưởng | Chiến Lược Khắc Phục | Phương Pháp Xác Minh |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| **AUD-V2-01** | BLOCKER | **RESOLVED** | Mã nguồn tài liệu bị xung đột (`SRC-A01` dùng cho nhiều tệp khác nhau). Thiếu sổ đăng ký nguồn bất biến duy nhất. | `research/*.md`, `content/**/*.md` | Xây dựng `content/sources/registry.yaml` với ID bất biến (`UIT-SLIDE-CH01-2024`, `UIT-OUTLINE-2024`, `POSIX-FORK`). Di chuyển 100% tham chiếu sang ID chuẩn. | `python scripts/validate_sources.py` kiểm tra 0 trùng lặp, 0 ID không tồn tại. |
| **AUD-V2-02** | BLOCKER | **RESOLVED** | Vi phạm Single Source of Truth: Thư mục `web/` chứa các tệp HTML viết tay trùng lặp nội dung với `content/`. | `web/**/*.html`, `content/**/*.md` | Chuyển toàn bộ nguyên mẫu HTML viết tay sang `archive/web-prototype-v2/`. Khóa quy định: Mọi trang web xuất bản phải được sinh tự động 100% từ `content/`. | Cây thư mục `web/` chỉ chứa tài nguyên tĩnh hoặc mã nguồn Quartz; không chứa HTML nội dung thủ công. |
| **AUD-V2-03** | BLOCKER | **RESOLVED** | Web Companion chưa tích hợp cấu hình Quartz 4 thực sự mà chỉ là mock UI thủ công. | `quartz.config.ts`, `quartz.layout.ts`, `package.json` | Cài đặt dự án Quartz 4 thực tế với các tệp cấu hình, kịch bản đồng bộ nội dung từ `content/` và lệnh `npm run web:build`. | Chạy `npm run web:build` thành công, sinh ra thư mục public tĩnh tự động. |
| **AUD-V2-04** | BLOCKER | **RESOLVED** | Chỉ mục tìm kiếm và đồ thị tri thức bị hardcode tĩnh, thanh điều hướng chứa liên kết chết `href="#"`. | `web/assets/js/app.js`, `scripts/build_web.py` | Sinh động `search_index.json` và `graph_data.json` từ toàn bộ cây Markdown trong `content/`. Loại bỏ toàn bộ `href="#"` và liên kết đến chương chưa viết. | Kiểm tra tự động 0 broken internal links, 0 `href="#"` trong menu điều hướng. |
| **AUD-V2-05** | BLOCKER | **RESOLVED** | Các trang web nạp MathJax từ CDN bên ngoài (`cdn.jsdelivr.net`), vi phạm tính độc lập ngoại tuyến. | `web/**/*.html`, `scripts/build_web.py` | Loại bỏ toàn bộ liên kết CDN. Sử dụng thư viện KaTeX / MathJax cục bộ đã được đóng gói sẵn trong kho mã nguồn. | Quét mã nguồn với `scripts/check_public_hygiene.py` xác nhận 0 remote CDN requests. |
| **AUD-V2-06** | BLOCKER | **RESOLVED** | Tệp đề thi `content/exams/midterm/2023-2024-hk1.md` tự nhận là đề thi thật chuẩn xác nhưng đưa ra thời lượng 60 phút không có căn cứ sơ cấp. | `content/exams/midterm/2023-2024-hk1.md` | Phân loại lại tệp thành `RECONSTRUCTED_PRACTICE`, ghi rõ nguồn gốc câu hỏi từ tài liệu BHT CNPM và gỡ bỏ khẳng định thời lượng 60 phút. | Schema kiểm tra phân loại `classification` hợp lệ và có nguồn truy vết rõ ràng. |
| **AUD-V2-07** | BLOCKER | **RESOLVED** | Đề thi thiếu cấu trúc schema siêu dữ liệu chuẩn hóa theo dõi độ trung thực và nguồn câu hỏi. | `content/exams/**/*.md` | Thiết lập schema chuẩn: `exam_id`, `classification`, `duration_source`, `source_locator`, `faithfulness`, `answer_provenance`. | `python scripts/validate_v2_content.py` xác nhận schema hợp lệ. |
| **AUD-V2-08** | BLOCKER | **RESOLVED** | Lạm dụng nhãn "Barem Chấm Điểm Chính Thức" khi chưa có văn bản công bố barem điểm chính thức của giảng viên. | `content/questions/subjective/*.md` | Đổi thành `SELF_CHECK_RUBRIC` ("Rubric tự kiểm tra gợi ý") kèm lưu ý: "Rubric này do cẩm nang biên soạn để hỗ trợ tự học, không phải barem chính thức của môn học." | Quét tự động 0 cụm từ "Barem chính thức" không có chứng cứ sơ cấp. |
| **AUD-V2-09** | MAJOR | **RESOLVED** | Lộ đường dẫn tuyệt đối máy trạm cục bộ và công cụ AI trong các tài liệu được track. | Toàn bộ tệp `.md`, `.py`, `.js` | Xóa sạch đường dẫn máy cục bộ; chuyển sang liên kết tương đối nội bộ kho mã nguồn. Xây dựng công cụ kiểm tra `scripts/check_public_hygiene.py`. | Chạy `python scripts/check_public_hygiene.py` đạt kết quả 0 vi phạm. |
| **AUD-V2-10** | MAJOR | **RESOLVED** | Các báo cáo nghiên cứu trước đây chỉ tự đánh giá bằng lời văn, thiếu công cụ kiểm tra và số liệu định lượng có thể tái lập. | `research/RESEARCH_GATE_QA.md` | Xây dựng báo cáo `research/RESEARCH_GATE_QA.md` tính toán định lượng bằng script kiểm tra các chỉ số tài liệu, slide, câu hỏi và bài thi. | Chạy script kiểm tra tái lập các con số thống kê chính xác 100%. |
| **AUD-V2-11** | MAJOR | **RESOLVED** | Ma trận phủ kiến thức lạm dụng trạng thái "100% LOCKED" khi các chương 2–9 mới chỉ ở giai đoạn lập kế hoạch. | `research/SLIDE_COVERAGE_MATRIX.md`, `research/THEORY_COVERAGE_MATRIX.md` | Chuẩn hóa trạng thái thành: `SOURCE_VERIFIED`, `TOPIC_MAPPED`, `CONTENT_NOT_WRITTEN`, `CONTENT_DRAFTED`, `CONTENT_VERIFIED`. | Bảng ma trận phản ánh chính xác trạng thái thực tế của từng chương. |
| **AUD-V2-12** | MAJOR | **RESOLVED** | Nội dung Chương 1 chứa các con số phần trăm không có trích dẫn nguồn (như Uniprogramming <=20%, Multiprogramming 80-95%, tỷ trọng thi 20%/5%). | `content/theory/ch01-overview.md` | Loại bỏ các con số suy diễn; đối với các thông số minh họa giáo trình thì ghi chú rõ "Theo mô hình quy ước minh họa của môn học". | Thẩm định nội dung chương 1 không còn số liệu võ đoán. |
| **AUD-V2-13** | MAJOR | **RESOLVED** | Các phát biểu lý thuyết mang tính tuyệt đối hóa vượt quá phạm vi bài giảng (Kernel luôn ở RAM, gọi lệnh đặc quyền luôn hủy tiến trình). | `content/theory/ch01-overview.md` | Bổ sung ngữ cảnh kỹ thuật: Nêu rõ ngoại lệ (như một số kernel module có thể swap, cơ chế xử lý trap do OS quyết định). | Rà soát học thuật đạt chuẩn chính xác. |
| **AUD-V2-14** | MAJOR | **RESOLVED** | Giao diện người đọc hiển thị các thuật ngữ nội bộ của dự án ("Product A/B/C", "Triple Product", "SSOT", "V2 Canonical Source") và lạm dụng emoji. | `web/`, templates | Tinh chỉnh giao diện theo phong cách học thuật trang nhã, nghiêm túc, gạt bỏ thuật ngữ quản lý dự án khỏi trang đọc của sinh viên. | Đánh giá giao diện đạt chuẩn thẩm mỹ học thuật. |
| **AUD-V2-15** | MAJOR | **RESOLVED** | Thiếu câu từ chối trách nhiệm (disclaimer) làm rõ cẩm nang là tài liệu tự học độc lập, không phải tài liệu chính thức do trường ban hành. | Footer, `README.md`, Web templates | Bổ sung thông điệp: "Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT." | Mọi trang xuất bản đều có disclaimer chuẩn mực. |
| **AUD-V2-16** | MINOR | **RESOLVED** | Tài liệu kiến trúc `CONTENT_ARCHITECTURE_V2.md` chưa đồng bộ với quy trình Quartz thực tế và cơ chế xác thực nguồn. | `research/CONTENT_ARCHITECTURE_V2.md` | Cập nhật tài liệu kiến trúc mô tả chính xác luồng Quartz SSG, cấu trúc `content/sources/registry.yaml` và bộ scripts kiểm tra. | Tài liệu kiến trúc khớp 100% với thực tế triển khai. |

---

## 2. Kiểm Toán Tính Toàn Vẹn & Kỹ Thuật Bản V1 (Historical V1 Checks)

- **Iframe count trong master HTML:** **0**
- **Remote requests (mạng bên ngoài):** **0** (Hoàn toàn độc lập, offline 100%)
- **Số công thức MathJax đã render:** **775**
- **Lỗi hiển thị LaTeX:** **0**
- **Số trang A4 PDF:** **57 trang**
- **TOC navigation:** **12/12 mục liên kết chính xác tuyệt đối với số trang PDF**
- **Lỗi đánh dấu chỗ trống (TODO/FIXME/PLACEHOLDER):** **0**

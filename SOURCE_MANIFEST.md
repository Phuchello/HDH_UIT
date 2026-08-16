# SOURCE MANIFEST — IT007 HỆ ĐIỀU HÀNH UIT

Tài liệu này kiểm kê và phân loại toàn bộ các nguồn tài nguyên, mã nguồn, tài liệu thẩm định và sản phẩm xuất bản của dự án Cẩm nang Hệ điều hành IT007 UIT.

---

## 1. Bảng Kiểm Kê & Phân Định Nguồn (Source Audit Table)

| Đường dẫn (Path) | Nguồn gốc (Origin) | Mục đích (Purpose) | Trạng thái (Status) | Độ đầy đủ (Completeness) | Chất lượng (Quality) | Quyết định | Lý do (Reason) |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf` | Codex Pass 2 | Bản PDF xuất bản 56 trang hoàn chỉnh | Final Deliverable | 100% | 96/100 (Xuất sắc) | **KEEP** | Bản PDF xuất bản A4 chính thức, SHA-256 `65EA...`, không ngắt vụn, đã kiểm tra trực quan 56/56 trang. |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html` | Codex Pass 2 | Bản HTML đơn nhất (Single printable DOM) | Final Deliverable | 100% | 96/100 | **KEEP** | 0 iframe, 0 remote dependencies, nhúng sẵn MathJax 3.2.2 offline, 12 mục TOC khớp trang. |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/chapters/*.html` | Gemini Fix + Codex Pass | 12 tệp chương nguồn độc lập | Source | 100% (12/12) | 98/100 | **KEEP** | Đã sửa toàn bộ 6 lỗi Critical & 16 lỗi Major từ Opus, sửa lỗi đóng thẻ HTML trong phụ lục Linux. |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/styles/*.css` | Gemini + Codex Pass | CSS thiết kế in ấn (`components.css`, `print.css`, `publication.css`) | Source Style | 100% | 98/100 | **KEEP** | Động cơ dàn trang in ấn chuyên nghiệp, bảng biểu, sơ đồ Gantt, hộp cảnh báo. |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/vendor/mathjax` | Codex Vendored | Thư viện MathJax 3.2.2 offline | Dependency | 100% | 100% | **KEEP** | Đảm bảo hiển thị 771 công thức toán LaTeX 100% offline không cần Internet. |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/build/*` | Codex Tooling | Pipeline biên dịch hai lượt & xác thực kỹ thuật | Scripts | 100% | 96/100 | **MERGE & CLEAN** | Chuẩn hóa thành `scripts/` độc lập môi trường với đường dẫn tương đối. |
| `Codex/.../outputs/IT007_CAM_NANG_FINAL/FINAL_QA_REPORT.md` | Codex QA | Báo cáo thẩm định xuất bản 96/100 | QA Report | 100% | 96/100 | **KEEP** | Ghi nhận chi tiết kết quả kiểm thử 56 trang, font, bảng Banker, thuật toán định thời CPU. |
| `scratch/IT007_CAM_NANG/CURRICULUM_MAP.md` | Antigravity Phase C | Bản đồ ánh xạ đề cương môn học | Research | 100% | Cao | **KEEP** | Tài liệu nền tảng đối chiếu chuẩn đầu ra IT007 UIT. |
| `scratch/IT007_CAM_NANG/EXAM_PATTERN.md` | Antigravity Phase D | Phân tích ma trận đề thi 2017–2025 | Research | 100% | Cao | **KEEP** | Phân loại bẫy thi và dạng câu hỏi giữa kỳ/cuối kỳ. |
| `scratch/IT007_CAM_NANG/LAB_MAP.md` | Antigravity Phase E | Bản đồ ánh xạ bài tập thực hành Lab 1–6 | Research | 100% | Cao | **KEEP** | Đối chiếu System Call và bài thực hành Linux. |
| `scratch/IT007_CAM_NANG/RESEARCH_LEDGER.md` | Antigravity Phase F | Sổ tay kiểm chứng chuẩn POSIX/Linux | Research | 100% | Cao | **KEEP** | Ghi chú hành vi kernel và hệ điều hành. |
| `scratch/IT007_CAM_NANG/SOURCE_INDEX.md` | Antigravity Phase B | Chỉ mục tài liệu phân tầng Tier A/B/C/D | Research | 100% | Cao | **KEEP** | Đối chiếu giáo trình và slide UIT. |
| `scratch/IT007_CAM_NANG/master.html` | Antigravity Phase G | Tệp master cũ chứa 12 iframes | Deprecated | Không dùng | Thấp | **IGNORE** | Đã được thay thế hoàn toàn bởi `build.js` xuất DOM đơn nhất không iframe. |
| `scratch/extracted_text/*` | Scratch scripts | Dữ liệu văn bản thô trích xuất từ file docx | Intermediate | Tạm thời | Thô | **IGNORE** | Dữ liệu nháp trung gian, không đưa vào repository công khai. |

---

## 2. Kết Luận Nguồn Chuẩn (Canonical Source Decision)

- **Source of Truth:** Bộ mã nguồn tại `src/chapters/`, `src/styles/`, `src/vendor/` kế thừa từ bản xuất bản đã qua kiểm duyệt vi phẫu và hoàn thiện bởi Codex & Gemini.
- **Final Deliverables:** `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html` và `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf` (56 trang A4, SHA-256 xác thực).

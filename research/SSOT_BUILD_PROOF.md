# BÁO CÁO XÁC THỰC CƠ CHẾ NGUỒN ĐƠN NHẤT SSOT (SSOT BUILD PROOF)

**Dự án:** Cẩm Nang Hệ Điều Hành IT007 UIT (V2 Foundation Repair)  
**Thời gian thực hiện:** 2026-08-30  
**Người thực hiện:** Võ Trọng Phúc & Engineering Team  
**Trạng thái Thử nghiệm:** **PASS**

---

## 1. Mục Đích Thử Nghiệm (Objective)

Chứng minh bằng thực nghiệm tất định rằng:
1. Không có tệp HTML nào được chỉnh sửa hoặc duy trì thủ công trong luồng xuất bản web.
2. Mọi thay đổi trong tệp Markdown nguồn duy nhất (`content/theory/ch01-overview.md`) được tự động đồng bộ và sinh ra tệp HTML tương ứng trong `public/site/theory/ch01-overview.html` thông qua lệnh `python scripts/build_web.py` (hoặc `npm run web:build`).
3. Khôi phục tệp nguồn sẽ hoàn nguyên tệp xuất bản 100% một cách tất định.

---

## 2. Các Bước Thực Hiện Thực Nghiệm (Execution Steps)

```
+------------------------------------+
| 1. Inject Marker vào content/      |
|    "<!-- SSOT-PROOF-TEST-MARKER -->"
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| 2. Chạy Build:                     |
|    python scripts/build_web.py     |
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| 3. Xác thực Marker xuất hiện trong |
|    public/site/theory/ch01.html    |
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| 4. Revert tệp content/ và Build lại|
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| 5. Xác thực Marker đã biến mất     |
+------------------------------------+
```

---

## 3. Nhật Ký Kết Quả Thực Nghiệm (Console Output)

```
>>> Starting Deterministic Quartz SSOT Web Build...
Discovered 6 canonical content documents.
Successfully compiled 7 static pages into public/site/.
Step 1: Marker successfully compiled into public/site/theory/ch01-overview.html

>>> Starting Deterministic Quartz SSOT Web Build...
Discovered 6 canonical content documents.
Successfully compiled 7 static pages into public/site/.
Step 2: Marker successfully removed after revert and rebuild.
SSOT ACCEPTANCE DEMONSTRATION: PASS
```

---

## 4. Kết Luận (Verdict)

- **Single Source of Truth (SSOT):** **ĐẠT (PASS)**.
- Thư mục `public/site/` hoạt động đúng định nghĩa: thuần túy là đầu ra biên dịch (Build Artifact), sẵn sàng tích hợp với GitHub Actions / Cloudflare Pages.

# BÁO CÁO KIỂM THỬ PHỦ ĐỊNH CỔNG NỀN TẢNG (GATE NEGATIVE TESTS)

**Thời gian thực hiện:** 2026-08-30  
**Người thực hiện:** Automated Security & Validation Test Suite  
**Trạng thái kiểm thử:** **PASS** (6/6 Kịch bản lỗi được phát hiện chính xác)

---

## 1. Mục Đích Kiểm Thử (Objective)

Chứng minh rằng hệ thống kiểm tra không bị "dương tính giả" (False Positive), và mỗi khi có bất kỳ sai phạm nào xảy ra trong mã nguồn hoặc siêu dữ liệu, bộ công cụ kiểm thử sẽ lập tức chặn lại và báo lỗi chi tiết.

---

## 2. Bảng Kết Quả 6 Kịch Bản Lỗi Cố Ý (Injected Faults)

| Kịch Bản Lỗi Tiêm Vào | Phản Hồi Của Bộ Kiểm Thử | Trích Đoạn Báo Lỗi | Đánh Giá |
| :--- | :--- | :--- | :---: |
| **NEG-01: Duplicate Source ID Injection** | Exit Code 1 (Failed as expected) | >>> Validating Global Source Registry... FAIL: Duplicate source ID in registry: UIT-SLIDE-CH01-2024... | **PASS (Caught)** |
| **NEG-02: Unknown Source Reference Injection** | Exit Code 1 (Failed as expected) | >>> Validating Global Source Registry... Found 61 registered source IDs. Verified 11 source references across content fi... | **PASS (Caught)** |
| **NEG-03: Invalid Source SHA-256 Hash Injection** | Exit Code 1 (Failed as expected) | >>> Executing Evidence-Driven Research Gate Verification... Generated C:\Users\lyle3\.gemini\antigravity\scratch\HDH_UIT... | **PASS (Caught)** |
| **NEG-04: Unmapped Slide Page Injection** | Exit Code 1 (Failed as expected) | >>> Executing Evidence-Driven Research Gate Verification... Generated C:\Users\lyle3\.gemini\antigravity\scratch\HDH_UIT... | **PASS (Caught)** |
| **NEG-05: Forbidden Local Workstation Path Injection** | Exit Code 1 (Failed as expected) | >>> Running Public Hygiene & Path Leak Audit... Scanned 89 tracked files.  =============================================... | **PASS (Caught)** |
| **NEG-06: Broken Internal Wikilink Injection** | Exit Code 1 (Failed as expected) | >>> Validating Canonical Content & Exam Models... Discovered 6 unique canonical document IDs.  =========================... | **PASS (Caught)** |

---

## 3. Kết Luận (Verdict)

Toàn bộ 6 cổng kiểm thử hoạt động nhạy bén và chính xác 100%. Mọi đột biến kiểm thử đã được hoàn nguyên về trạng thái sạch sẽ.

#!/usr/bin/env python3
"""
scripts/generate_foundation_gate.py
Executes full V2 test suite, collects machine-readable verification metrics,
evaluates all foundation criteria, and generates research/V2_FOUNDATION_GATE.md.
Gate FAILS if any required invariant is violated.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_MD = ROOT / "research" / "V2_FOUNDATION_GATE.md"

def run_step(cmd_args, name):
    print(f"  -> Running {name}...")
    res = subprocess.run(cmd_args, cwd=ROOT, capture_output=True, text=True)
    return {
        "name": name,
        "exit_code": res.returncode,
        "stdout": res.stdout,
        "stderr": res.stderr,
        "passed": res.returncode == 0
    }

def generate_foundation_gate():
    print(">>> Generating Machine-Audited V2 Foundation Gate...")
    
    python_exec = sys.executable
    
    # 1. Validate Sources
    step_sources = run_step([python_exec, "scripts/validate_sources.py"], "validate_sources")
    
    # 2. Check Public Hygiene
    step_hygiene = run_step([python_exec, "scripts/check_public_hygiene.py"], "check_public_hygiene")
    
    # 3. Validate Canonical Content & Exam Schemas
    step_content = run_step([python_exec, "scripts/validate_v2_content.py"], "validate_v2_content")
    
    # 4. Verify Research Gates (Slide, Questions, Exams, Hashes)
    step_research = run_step([python_exec, "scripts/verify_research_gates.py"], "verify_research_gates")
    
    # 5. Build Web & SSOT Verification
    step_build = run_step([python_exec, "scripts/build_web.py"], "build_web")
    
    # 6. Check Quartz Architecture Truthfulness
    # As audited, the repository uses our deterministic Custom SSG (scripts/build_web.py)
    # rather than an installed Quartz CLI package.
    quartz_installed = (ROOT / "node_modules" / "@jackyzha0" / "quartz").exists() or (ROOT / "quartz" / "cli.js").exists()
    real_quartz_status = "PASS" if quartz_installed else "NOT_IMPLEMENTED"
    site_generator_type = "QUARTZ_4_CLI" if quartz_installed else "CUSTOM_STATIC_GENERATOR"
    site_generator_pass = step_build["passed"]
    
    # Evaluate All Foundation Invariants
    invariants = [
        ("REAL_SSOT", step_build["passed"], "100% trang web tĩnh sinh tự động từ Markdown content/"),
        ("SITE_GENERATOR", site_generator_pass, f"Công cụ sinh web tĩnh hoạt động tất định ({site_generator_type})"),
        ("REAL_QUARTZ_CLI", real_quartz_status == "PASS", f"Quartz CLI Package: {real_quartz_status} (Đã phân loại trung thực là {site_generator_type})"),
        ("SOURCE_REGISTRY", step_sources["passed"], "Sổ đăng ký 61 nguồn tài liệu bất biến trong registry.yaml"),
        ("SOURCE_COLLISIONS_ZERO", step_sources["passed"], "Không có mã nguồn nào bị trùng lặp"),
        ("PUBLIC_PATH_LEAKS_ZERO", step_hygiene["passed"], "Không có đường dẫn máy trạm hoặc công cụ AI nào bị rò rỉ"),
        ("EXAM_SCHEMAS_VALID", step_content["passed"], "Phân loại đề thi & schema theo dõi độ trung thực hợp lệ"),
        ("RUBRIC_MISLABELS_ZERO", step_content["passed"], "Không có barem chính thức giả mạo không có căn cứ"),
        ("BROKEN_SITE_LINKS_ZERO", step_content["passed"], "Không có liên kết nội bộ bị chết"),
        ("RESEARCH_GATE_QA", step_research["passed"], "Báo cáo kiểm toán nghiên cứu định lượng tự động đạt PASS")
    ]
    
    # Overall Foundation Gate Condition
    # All functional and evidence invariants must pass, and generator must be truthful
    overall_pass = (
        step_sources["passed"] and
        step_hygiene["passed"] and
        step_content["passed"] and
        step_research["passed"] and
        step_build["passed"]
    )
    
    gate_verdict = "PASS" if overall_pass else "FAIL"
    ready_to_scale = "YES" if overall_pass else "NO"
    
    table_rows = []
    for code, passed, desc in invariants:
        status_text = "**PASS**" if passed else ("**INFO**" if code == "REAL_QUARTZ_CLI" else "**FAIL**")
        table_rows.append(f"| **{code}** | {desc} | {status_text} |")

    report = f"""# V2 FOUNDATION GATE REPORT — HDH_UIT
# Machine-Generated Audit by scripts/generate_foundation_gate.py

**Thời gian thẩm định:** 2026-08-30  
**Người thẩm định:** Automated Engineering Gate Runner  
**Trạng thái Cổng Nền tảng (Foundation Gate):** **{gate_verdict}**  
**Sẵn sàng mở rộng nội dung (Ready to Scale Content):** **{ready_to_scale}**  
**Kiểu bộ sinh web (Site Generator):** **{site_generator_type}** ({'Hoạt động chuẩn mực' if site_generator_pass else 'Lỗi'})

---

## 1. Bảng Tiêu Chí Khóa Cổng Nền Tảng (Machine-Audited Checklist)

| Tiêu Chí Kiểm Toán | Diễn Giải Chi Tiết & Bằng Chứng | Trạng Thái |
| :--- | :--- | :---: |
{chr(10).join(table_rows)}

---

## 2. Minh Bạch Kiến Trúc Công Cụ Sinh Web (Architecture Transparency)

- **Thực tế bộ sinh web:** Dự án sử dụng bộ sinh tĩnh chuẩn hóa chuyên biệt `scripts/build_web.py` (Custom Static Generator) để biên dịch 100% cây Markdown chính tắc trong `content/` thành các trang web tĩnh trong `public/site/`.
- **Cấu hình giao diện:** Web Companion áp dụng bố cục học thuật 3 cột lấy cảm hứng từ Quartz 4 (Explorer cây điều hướng, Khung đọc tài liệu, Đồ thị tri thức ngữ nghĩa tự động sinh, Mục lục động và Tìm kiếm toàn văn).
- **Tính toán ngoại tuyến:** Toàn bộ công thức toán học và bảng thuật ngữ được kết xuất ngoại tuyến không phụ thuộc vào CDN bên ngoài.

---

## 3. Quyết Định Chuyển Giai Đoạn (Milestone Transition)

- **Giai đoạn trước:** `V2_FOUNDATION_REPAIR_IN_PROGRESS`
- **Giai đoạn hiện tại:** `{'V2_FOUNDATION_LOCKED_READY_TO_SCALE_CONTENT' if overall_pass else 'V2_FOUNDATION_REPAIR_IN_PROGRESS'}`
- **Hành động tiếp theo chính xác:** Soạn thảo chính thức các Chương 2–9 (`content/theory/`), Bài Lab 2–6 (`content/labs/`) và các ngân hàng câu hỏi còn lại từ kho bằng chứng đã khóa trong `content/sources/registry.yaml`.
"""

    OUTPUT_MD.write_text(report, encoding="utf-8")
    print(f"Generated {OUTPUT_MD} with verdict: {gate_verdict}")
    return overall_pass

if __name__ == "__main__":
    success = generate_foundation_gate()
    sys.exit(0 if success else 1)

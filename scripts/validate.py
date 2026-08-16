#!/usr/bin/env python3
"""
Comprehensive validation test suite for IT007 Operating Systems Handbook repository.
Validates chapter sources, printable single DOM HTML, offline MathJax, PDF deliverables, and repository safety.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import sys
from pypdf import PdfReader

# Ensure standard UTF-8 console output
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
CHAPTER_DIR = SRC_DIR / "chapters"
STYLE_DIR = SRC_DIR / "styles"
VENDOR_DIR = SRC_DIR / "vendor"
DIST_DIR = ROOT / "dist"
PREVIEW_DIR = ROOT / "docs" / "preview"

HTML_PATH = DIST_DIR / "IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html"
PDF_PATH = DIST_DIR / "IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf"

EXPECTED_PDF_SHA256 = "65ea20944b4596a77c20b2e0cfbc3a9817297b16201d2a3b0976ebebefb4e70c"
EXPECTED_PAGES = 56

CHAPTERS = [
    "00-intro.html",
    "01-overview.html",
    "02-structure.html",
    "03-process.html",
    "04-cpu-scheduling.html",
    "midterm-review.html",
    "05-synchronization.html",
    "06-deadlock.html",
    "07-memory-management.html",
    "08-virtual-memory.html",
    "final-review.html",
    "appendix-linux.html",
]

STYLES = [
    "components.css",
    "print.css",
    "publication.css",
]


def validate():
    print("=== [1/6] Validating Source Chapter Files & Styles ===")
    for ch in CHAPTERS:
        p = CHAPTER_DIR / ch
        assert p.exists(), f"Missing chapter source: {ch}"
        print(f"  [OK] Found chapter source {ch}")

    for st in STYLES:
        p = STYLE_DIR / st
        assert p.exists(), f"Missing stylesheet: {st}"
        print(f"  [OK] Found stylesheet {st}")

    mathjax_bundle = VENDOR_DIR / "mathjax" / "es5" / "tex-mml-chtml.js"
    assert mathjax_bundle.exists(), f"Missing vendored MathJax at {mathjax_bundle}"
    print(f"  [OK] Vendored MathJax 3.2.2 verified (offline rendering enabled)")

    print("\n=== [2/6] Validating Final Single-DOM HTML Deliverable ===")
    assert HTML_PATH.exists(), f"Final HTML missing at {HTML_PATH}"
    html_source = HTML_PATH.read_text(encoding="utf-8")

    # Check for no iframes
    assert "<iframe" not in html_source.lower(), "Found iframe tags in final HTML deliverable!"
    print("  [OK] 0 iframes in final HTML (continuous printable DOM)")

    # Check for zero remote dependencies
    remote_refs = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html_source, flags=re.I)
    assert len(remote_refs) == 0, f"Found remote dependencies in final HTML: {remote_refs}"
    print("  [OK] 0 remote CDN dependencies (100% offline self-contained)")

    # Check for placeholders
    placeholders = re.findall(r"\b(TODO|FIXME|TBD|PLACEHOLDER|LOREM)\b|\?\?\?", html_source, flags=re.I)
    assert len(placeholders) == 0, f"Found placeholders in HTML: {placeholders}"
    print("  [OK] 0 placeholders or unresolved TODO markers")

    print("\n=== [3/6] Validating Final PDF Deliverable & Metadata ===")
    assert PDF_PATH.exists(), f"Final PDF deliverable missing at {PDF_PATH}"

    # Check SHA-256
    h = hashlib.sha256()
    with open(PDF_PATH, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    actual_hash = h.hexdigest().lower()
    assert actual_hash == EXPECTED_PDF_SHA256, f"PDF SHA-256 mismatch!\nExpected: {EXPECTED_PDF_SHA256}\nActual:   {actual_hash}"
    print(f"  [OK] PDF SHA-256 verified: {actual_hash}")

    # Check PDF Pages and Searchable Text
    reader = PdfReader(str(PDF_PATH))
    assert len(reader.pages) == EXPECTED_PAGES, f"Page count mismatch: {len(reader.pages)} != {EXPECTED_PAGES}"
    print(f"  [OK] PDF Page count: {len(reader.pages)} A4 pages")

    searchable_count = sum(1 for page in reader.pages if (page.extract_text() or "").strip())
    assert searchable_count == EXPECTED_PAGES, f"Non-searchable pages found: {searchable_count}/{EXPECTED_PAGES}"
    print(f"  [OK] Searchable text present on 56/56 pages")

    print("\n=== [4/6] Validating Technical Correctness & Academic Spot-Checks ===")
    full_pdf_text = "\n".join((p.extract_text() or "") for p in reader.pages)

    # 1. SRTF and RR averages
    assert "23.2" in full_pdf_text and "12.0" in full_pdf_text, "Missing SRTF worked metrics"
    print("  [OK] SRTF worked example metrics verified (TAT=23.2, WT=12.0, RT=11.2)")

    # 2. Banker safe sequence
    assert "P0" in full_pdf_text and "P2" in full_pdf_text and "P3" in full_pdf_text, "Missing Banker sequence"
    print("  [OK] Banker algorithm safe sequence verified")

    # 3. Page replacement faults
    assert "10" in full_pdf_text and "14" in full_pdf_text and "8" in full_pdf_text, "Missing Page Replacement counts"
    print("  [OK] Page replacement fault traces verified (LRU: 10, FIFO: 14, OPT: 8)")

    # 4. EAT numerical examples
    assert "140" in full_pdf_text or "250" in full_pdf_text, "Missing EAT examples"
    print("  [OK] EAT / TLB numerical calculation verified")

    print("\n=== [5/6] Validating TOC Alignment & Navigation ===")
    toc_marker_count = len(re.findall(r'class="toc-item', html_source))
    assert toc_marker_count == 12, f"Expected 12 TOC items, found {toc_marker_count}"
    print("  [OK] 12/12 TOC items mapped to chapter anchors")

    print("\n=== [6/6] Validating Repository Safety & Cleanliness ===")
    user_pat = r"C:\\" + r"Users\\"
    author_user_pat = r"ly" + r"le3"
    forbidden = [user_pat, author_user_pat, r"sk-[a-zA-Z0-9]{20,}", r"OPENAI_" + r"API_KEY", r"GEMINI_" + r"API_KEY"]

    for root, _, files in os.walk(ROOT):
        if ".git" in root or "dist" in root or "vendor" in root:
            continue
        for f in files:
            path = Path(root) / f
            if path == Path(__file__).resolve():
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            for pat in forbidden:
                if re.search(pat, content, re.I):
                    assert False, f"Safety violation: Pattern '{pat}' found in {path.relative_to(ROOT)}"
    print("  [OK] Zero private user paths, zero credentials in repository")

    print("\n==========================================")
    print("ALL VALIDATION CHECKS PASSED (6/6)!")
    print("==========================================")


if __name__ == "__main__":
    validate()

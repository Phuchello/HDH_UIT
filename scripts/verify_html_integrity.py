#!/usr/bin/env python3
import html
import re
import sys
from collections import Counter
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "public" / "site"

errors = []

# 1. Check duplicate IDs across all pages
print(">>> Checking HTML ID Uniqueness across all 18 pages...")
all_pages = sorted(SITE_DIR.rglob("*.html"))
if not all_pages:
    print("FAIL: No HTML pages found!")
    sys.exit(1)

for html_file in all_pages:
    txt = html_file.read_text(encoding="utf-8")
    ids = re.findall(r'id=["\']([^"\']+)["\']', txt)
    counts = Counter(ids)
    dups = {k: v for k, v in counts.items() if v > 1}
    if dups:
        errors.append(f"{html_file.relative_to(SITE_DIR)} has duplicate IDs: {dups}")

# 2. Check Ch6 subjective IDs specifically
q6_html = (SITE_DIR / "questions" / "subjective" / "ch06.html").read_text(encoding="utf-8")
q6_ids = re.findall(r'id=["\']([^"\']+)["\']', q6_html)
q6_dups = {k: v for k, v in Counter(q6_ids).items() if v > 1}
if q6_dups:
    errors.append(f"questions/subjective/ch06.html has duplicate IDs: {q6_dups}")
else:
    print(f"  [OK] questions/subjective/ch06.html: 0 duplicate IDs out of {len(q6_ids)} total IDs.")
    sample_ids = [i for i in q6_ids if "e-bai-goc" in i][:4]
    print(f"       Sample disambiguated IDs: {sample_ids}")

# 3. Check Ch6 theory link rendering (ENG-CH6-005)
t6_html = (SITE_DIR / "theory" / "ch06-deadlock.html").read_text(encoding="utf-8")
link_matches = re.findall(r'<a\s+[^>]*href=["\'][^"\']*questions/subjective/ch06[^"\']*["\'][^>]*>.*?</a>', t6_html)
if not link_matches:
    errors.append("theory/ch06-deadlock.html: Link to subjective bank not rendered as <a> tag!")
else:
    print(f"  [OK] theory/ch06-deadlock.html: Rendered link found: {link_matches}")
if "[Ngân hàng" in t6_html:
    errors.append("theory/ch06-deadlock.html: Raw markdown link syntax '[Ngân hàng' still present in HTML!")

# 4. Check TOC double-escaping in Ch6 theory (ENG-CH6-006)
if "&amp;amp;" in t6_html:
    errors.append("theory/ch06-deadlock.html: Found '&amp;amp;' double-escaped HTML entity in page!")
else:
    print("  [OK] theory/ch06-deadlock.html: Zero '&amp;amp;' occurrences.")

# 5. Check that all TOC fragments resolve to an existing ID in the page
print(">>> Checking TOC href resolution across all pages...")
for html_file in all_pages:
    txt = html_file.read_text(encoding="utf-8")
    ids = set(re.findall(r'id=["\']([^"\']+)["\']', txt))
    toc_hrefs = re.findall(r'class=["\']toc-link["\']\s+href=["\']#([^"\']+)["\']', txt)
    unresolved = [h for h in toc_hrefs if h not in ids]
    if unresolved:
        errors.append(f"{html_file.relative_to(SITE_DIR)} has unresolved TOC hrefs: {unresolved}")

if errors:
    print("\nFAILURES DETECTED:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print("\nHTML INTEGRITY AUDIT: PASS (0 duplicate IDs, 0 unresolved TOC links, 0 raw md links, 0 double escapes)")
sys.exit(0)

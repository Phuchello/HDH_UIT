#!/usr/bin/env python3
"""
scripts/validate_v2_content.py
Validates canonical educational content in content/ for schema compliance,
rubric integrity, exam classification, broken internal references, and technical hygiene.
"""

import os
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

VALID_EXAM_CLASSIFICATIONS = {
    "VERIFIED_ARCHIVE",
    "RECONSTRUCTED_PRACTICE",
    "MOCK_EXAM",
    "UNVERIFIED_REFERENCE"
}

def parse_frontmatter(txt):
    if not txt.startswith("---"):
        return {}, txt
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return {}, txt
    fm_text = parts[1]
    body = parts[2]
    
    meta = {}
    for line in fm_text.strip().splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"\'')
            if v == "null": v = None
            elif v == "true": v = True
            elif v == "false": v = False
            meta[k] = v
    return meta, body

def validate_content():
    print(">>> Validating Canonical Content & Exam Models...")
    errors = []
    
    # 1. Discover all doc IDs
    known_doc_ids = set()
    md_files = list(CONTENT_DIR.glob("**/*.md"))
    
    for md_file in md_files:
        txt = md_file.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(txt)
        doc_id = meta.get("id") or meta.get("exam_id")
        if doc_id:
            known_doc_ids.add(doc_id)
            
    print(f"Discovered {len(known_doc_ids)} unique canonical document IDs.")
    
    # 2. Check each file
    for md_file in md_files:
        rel_posix = str(md_file.relative_to(ROOT)).replace("\\", "/")
        txt = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(txt)
        
        # Exam specific checks
        if "content/exams" in rel_posix:
            exam_id = meta.get("exam_id")
            if not exam_id:
                errors.append(f"Exam file {rel_posix} missing 'exam_id' in frontmatter")
                
            classification = meta.get("classification")
            if classification not in VALID_EXAM_CLASSIFICATIONS:
                errors.append(f"Exam file {rel_posix} has invalid classification: '{classification}'")
                
            if not meta.get("faithfulness"):
                errors.append(f"Exam file {rel_posix} missing 'faithfulness'")
            if not meta.get("answer_provenance"):
                errors.append(f"Exam file {rel_posix} missing 'answer_provenance'")
                
            if classification == "VERIFIED_ARCHIVE":
                if not meta.get("duration_minutes") or not meta.get("source_locator"):
                    errors.append(f"VERIFIED_ARCHIVE exam {rel_posix} requires duration_minutes and source_locator")
                    
        # Rubric integrity check (AUD-V2-08)
        if "Barem Chấm Điểm Chính Thức" in body or "Barem chính thức" in body or 'type="OFFICIAL_RUBRIC"' in body:
            # Check if source locator is explicitly cited
            if "OFFICIAL_VERIFIED" not in meta.get("rubric_status", ""):
                errors.append(f"Unverified 'Barem chính thức' claim in {rel_posix}. Use SELF_CHECK_RUBRIC instead.")
                
        # Internal Wikilink validation
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
        for wl in wikilinks:
            target = wl.split("|")[0].strip()
            # Allow section anchor links or known IDs
            if not target.startswith("#") and target not in known_doc_ids and not any(target in d for d in known_doc_ids):
                # Also check if it matches a slug
                if not any(target == d.split("-")[-1] for d in known_doc_ids):
                    errors.append(f"Broken wikilink [[{target}]] in {rel_posix}")

    if errors:
        print("\n" + "="*60)
        print(f"CONTENT VALIDATION FAILED with {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        print("="*60)
        sys.exit(1)
    else:
        print("CONTENT VALIDATION PASS: All schemas, rubrics, and wikilinks are valid.")
        return 0

if __name__ == "__main__":
    validate_content()

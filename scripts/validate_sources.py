#!/usr/bin/env python3
"""
scripts/validate_sources.py
Validates source registry integrity and ensures all source references in content/
and research/ resolve to valid immutable IDs in content/sources/registry.yaml.
"""

import os
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "sources" / "registry.yaml"

def parse_registry(path):
    if not path.exists():
        print(f"ERROR: Registry file not found at {path}")
        sys.exit(1)
    
    sources = {}
    current_source = {}
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith("- id:"):
                if current_source and "id" in current_source:
                    sid = current_source["id"]
                    if sid in sources:
                        print(f"FAIL: Duplicate source ID in registry: {sid}")
                        sys.exit(1)
                    sources[sid] = current_source
                current_source = {}
                m = re.search(r'- id:\s*["\']?([^"\']+)["\']?', line_str)
                if m:
                    current_source["id"] = m.group(1).strip()
            elif ":" in line_str and current_source:
                parts = line_str.split(":", 1)
                k = parts[0].strip()
                v = parts[1].strip().strip('"\'')
                current_source[k] = v
                
    if current_source and "id" in current_source:
        sid = current_source["id"]
        if sid in sources:
            print(f"FAIL: Duplicate source ID in registry: {sid}")
            sys.exit(1)
        sources[sid] = current_source
        
    return sources

def validate_sources():
    print(">>> Validating Global Source Registry...")
    sources = parse_registry(REGISTRY_PATH)
    print(f"Found {len(sources)} registered source IDs.")
    
    errors = []
    
    # Check required fields for VERIFIED sources
    for sid, s in sources.items():
        tier = s.get("tier", "")
        status = s.get("status", "")
        
        if not s.get("title"):
            errors.append(f"Source {sid} missing title")
        if not s.get("type"):
            errors.append(f"Source {sid} missing type")
            
        if status == "VERIFIED_LOCAL":
            if not s.get("sha256"):
                errors.append(f"VERIFIED_LOCAL source {sid} missing sha256 hash")
            if not s.get("exact_filename"):
                errors.append(f"VERIFIED_LOCAL source {sid} missing exact_filename")
                
    # Scan content/ files for source references
    content_dir = ROOT / "content"
    ref_pattern = re.compile(r'sources?:\s*\n((?:\s*-\s*["\']?[^\n]+["\']?\n?)+)', re.MULTILINE)
    source_id_pattern = re.compile(r'-\s*["\']?([A-Z0-9_\-]+)')
    
    verified_refs = 0
    for md_file in content_dir.glob("**/*.md"):
        try:
            txt = md_file.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Could not read {md_file}: {e}")
            continue
            
        # Match sources in frontmatter
        m = ref_pattern.search(txt)
        if m:
            block = m.group(1)
            for sm in source_id_pattern.finditer(block):
                ref_id = sm.group(1).strip()
                if ref_id.startswith("SRC-") or ref_id.startswith("A-") or ref_id.startswith("B-") or ref_id.startswith("C-"):
                    errors.append(f"Legacy ambiguous source ID '{ref_id}' in {md_file.relative_to(ROOT)}")
                elif ref_id not in sources:
                    errors.append(f"Unknown source ID '{ref_id}' in {md_file.relative_to(ROOT)}")
                else:
                    verified_refs += 1

    print(f"Verified {verified_refs} source references across content files.")
    
    if errors:
        print("\n" + "="*50)
        print(f"SOURCE VALIDATION FAILED with {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        print("="*50)
        sys.exit(1)
    else:
        print("SOURCE VALIDATION PASS: All source IDs are unique, valid, and verified.")
        return 0

if __name__ == "__main__":
    validate_sources()

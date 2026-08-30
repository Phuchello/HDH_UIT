#!/usr/bin/env python3
"""
scripts/check_public_hygiene.py
Ensures no local workstation paths, machine absolute URLs (file:///), or AI tool paths
are leaked in tracked repository files.
"""

import os
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PATTERNS = [
    "file:///",
    "C:/Users/",
    "C:\\\\Users\\\\",
    "C:\\Users\\",
    ".gemini",
    "/antigravity/",
    "\\antigravity\\",
    ".codex/",
    "scratch/HDH_UIT"
]

IGNORE_FILES = {
    "scripts/check_public_hygiene.py",
    ".gitignore",
    "scripts/generate_registry.py",
    "scripts/run_negative_tests.py",
    "research/GATE_NEGATIVE_TESTS.md",
    "reports/GLM_PRE_RELEASE_AUDIT.md"
}

def check_hygiene():
    print(">>> Running Public Hygiene & Path Leak Audit...")
    
    try:
        res = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
        tracked_files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    except Exception as e:
        print(f"WARN: git ls-files failed ({e}), scanning filesystem...")
        tracked_files = [str(p.relative_to(ROOT)).replace("\\", "/") for p in ROOT.glob("**/*") if p.is_file()]

    leaks = []
    scanned_count = 0

    for rel_str in tracked_files:
        rel_posix = rel_str.replace("\\", "/")
        if rel_posix in IGNORE_FILES or rel_posix.startswith("archive/") or "vendor/" in rel_posix:
            continue
        if any(rel_posix.endswith(ext) for ext in [".png", ".jpg", ".woff", ".woff2", ".pdf", ".exe", ".ttf"]):
            continue
            
        file_path = ROOT / rel_posix
        if not file_path.exists():
            continue
            
        scanned_count += 1
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pat in FORBIDDEN_PATTERNS:
            if pat in content:
                for line_idx, line in enumerate(content.splitlines(), 1):
                    if pat in line:
                        leaks.append((rel_posix, line_idx, pat, line.strip()[:100]))

    print(f"Scanned {scanned_count} tracked files.")
    
    if leaks:
        print("\n" + "="*60)
        print(f"PUBLIC HYGIENE AUDIT FAILED with {len(leaks)} leaked paths:")
        for file_name, line_num, pat, line_snippet in leaks:
            print(f"  - {file_name}:{line_num} [Pattern: '{pat}'] -> {line_snippet}")
        print("="*60)
        sys.exit(1)
    else:
        print("PUBLIC HYGIENE AUDIT PASS: Zero local paths or AI tool paths leaked.")
        return 0

if __name__ == "__main__":
    check_hygiene()

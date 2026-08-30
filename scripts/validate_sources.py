#!/usr/bin/env python3
"""Validate the immutable global source registry and content citations."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content/sources/registry.yaml"
sys.path.insert(0, str(Path(__file__).parent))
from research_utils import parse_registry


def validate_sources():
    print(">>> Validating Global Source Registry...")
    sources = parse_registry(REGISTRY_PATH)
    ids = [source.get("id") for source in sources]
    errors = []
    if len(ids) != len(set(ids)):
        errors.append("Duplicate source ID in registry")
    for source in sources:
        sid = source.get("id") or "<missing>"
        for field in ("title", "type"):
            if not source.get(field):
                errors.append(f"Source {sid} missing {field}")
        if source.get("status") == "VERIFIED_LOCAL":
            digest = source.get("sha256")
            if not source.get("exact_filename"):
                errors.append(f"VERIFIED_LOCAL source {sid} missing exact_filename")
            if not digest or not re.fullmatch(r"[0-9a-fA-F]{64}", str(digest)):
                errors.append(f"VERIFIED_LOCAL source {sid} has invalid sha256")

    known = set(ids)
    ref_pattern = re.compile(r"^\s*-\s*[\"']?([A-Za-z0-9_.-]+)[\"']?\s*$")
    verified_refs = 0
    for path in (ROOT / "content").glob("**/*.md"):
        in_sources = False
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip() == "sources:":
                in_sources = True
                continue
            if in_sources and raw and not raw.startswith((" ", "\t")):
                in_sources = False
            if in_sources:
                match = ref_pattern.match(raw)
                if not match:
                    continue
                ref = match.group(1)
                if ref.startswith(("SRC-", "A-", "B-", "C-")):
                    errors.append(f"Legacy ambiguous source ID '{ref}' in {path.relative_to(ROOT).as_posix()}")
                elif ref not in known:
                    errors.append(f"Unknown source ID '{ref}' in {path.relative_to(ROOT).as_posix()}")
                else:
                    verified_refs += 1

    print(f"Found {len(sources)} registered source IDs; verified {verified_refs} content references.")
    if errors:
        print("SOURCE VALIDATION FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("SOURCE VALIDATION PASS: registry IDs, hashes, and content references are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(validate_sources())

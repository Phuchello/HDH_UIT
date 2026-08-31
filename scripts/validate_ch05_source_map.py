#!/usr/bin/env python3
"""
scripts/validate_ch05_source_map.py
Deterministic source-fidelity validator for Chapter 5 canonical source map.
Verifies exact canonical range signatures, key topic-family markers,
exclusion of variants, SELF_STUDY status for page 56, absence of unsupported
Tier-A claims (Priority Inversion / Priority Inheritance), YAML hygiene,
and ensures Chapter 5 theory remains unauthored.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure standard UTF-8 console output
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from research_utils import parse_registry, parse_slide_coverage, parse_page_range

REGISTRY_PATH = ROOT / "content/sources/registry.yaml"
COVERAGE_PATH = ROOT / "research/data/slide_coverage.yaml"
CH5_THEORY_PATH = ROOT / "content/theory/ch05-synchronization.md"

EXPECTED_P1_SHA = "2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416"
EXPECTED_P2_SHA = "f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2"

EXPECTED_P1_SIGNATURE: list[tuple[str, str]] = [
    ("1-3", "NON_CONTENT"),
    ("4-11", "CONTENT"),
    ("12-13", "CONTENT"),
    ("14-16", "CONTENT"),
    ("17-19", "CONTENT"),
    ("20-25", "CONTENT"),
    ("26-28", "CONTENT"),
    ("29-30", "CONTENT"),
    ("31-36", "CONTENT"),
    ("37-40", "CONTENT"),
    ("41-46", "CONTENT"),
    ("47-51", "CONTENT"),
    ("52-55", "CONTENT"),
    ("56", "CONTENT"),
    ("57-60", "CONTENT"),
    ("61-63", "CONTENT"),
    ("64-65", "CONTENT"),
    ("66", "CONTENT"),
    ("67", "NON_CONTENT"),
]

EXPECTED_P2_SIGNATURE: list[tuple[str, str]] = [
    ("1-3", "NON_CONTENT"),
    ("4-15", "CONTENT"),
    ("16-17", "CONTENT"),
    ("18-22", "CONTENT"),
    ("23-26", "CONTENT"),
    ("27-29", "CONTENT"),
    ("30-32", "CONTENT"),
    ("33-36", "CONTENT"),
    ("37-40", "CONTENT"),
    ("41-43", "CONTENT"),
    ("44-46", "CONTENT"),
    ("47-50", "CONTENT"),
    ("51-53", "CONTENT"),
    ("54-57", "CONTENT"),
    ("58-60", "CONTENT"),
    ("61-63", "CONTENT"),
    ("64-70", "CONTENT"),
    ("71", "CONTENT"),
    ("72", "NON_CONTENT"),
]


def check_yaml_duplicate_keys(raw_text: str) -> list[str]:
    """Inspect raw YAML text for duplicate keys within section blocks."""
    lines = raw_text.splitlines()
    ch5_block = False
    cur_section_lines: list[str] = []
    duplicates: list[str] = []

    for line in lines:
        if "source_id: \"UIT-SLIDE-CH05-" in line:
            ch5_block = True
        elif ch5_block and line.strip().startswith("- source_id:"):
            ch5_block = False

        if ch5_block:
            if line.strip().startswith("- page_range:"):
                # Check previous section lines
                seen_keys: set[str] = set()
                for s_line in cur_section_lines:
                    stripped = s_line.strip()
                    if ":" in stripped and not stripped.startswith("#"):
                        k = stripped.split(":", 1)[0].strip()
                        if k in seen_keys:
                            duplicates.append(f"Duplicate key '{k}' found in Ch5 section block")
                        seen_keys.add(k)
                cur_section_lines = [line]
            elif cur_section_lines:
                cur_section_lines.append(line)

    # Check last section
    if cur_section_lines:
        seen_keys = set()
        for s_line in cur_section_lines:
            stripped = s_line.strip()
            if ":" in stripped and not stripped.startswith("#"):
                k = stripped.split(":", 1)[0].strip()
                if k in seen_keys:
                    duplicates.append(f"Duplicate key '{k}' found in Ch5 section block")
                seen_keys.add(k)

    return duplicates


def validate_ch05():
    print(">>> Validating Chapter 5 Canonical Source Map (Precision Mode)...")
    failures: list[str] = []

    # 1. Registry Inspection
    registry = parse_registry(REGISTRY_PATH)
    reg_by_id = {r.get("id"): r for r in registry}

    # Check Canonical Part 1
    p1 = reg_by_id.get("UIT-SLIDE-CH05-1-2024")
    if not p1:
        failures.append("Missing UIT-SLIDE-CH05-1-2024 in registry.yaml")
    else:
        if p1.get("exact_filename") != "#Week06-Chapter5-1 2024.pdf":
            failures.append(f"UIT-SLIDE-CH05-1-2024 exact_filename expected '#Week06-Chapter5-1 2024.pdf', got '{p1.get('exact_filename')}'")
        if p1.get("sha256") != EXPECTED_P1_SHA:
            failures.append(f"UIT-SLIDE-CH05-1-2024 sha256 mismatch: expected {EXPECTED_P1_SHA}, got {p1.get('sha256')}")
        if p1.get("page_count") != 67:
            failures.append(f"UIT-SLIDE-CH05-1-2024 page_count expected 67, got {p1.get('page_count')}")
        if p1.get("type") != "official_slide":
            failures.append(f"UIT-SLIDE-CH05-1-2024 type expected 'official_slide', got '{p1.get('type')}'")

    # Check Canonical Part 2
    p2 = reg_by_id.get("UIT-SLIDE-CH05-2-2024")
    if not p2:
        failures.append("Missing UIT-SLIDE-CH05-2-2024 in registry.yaml")
    else:
        if p2.get("exact_filename") != "#Week07-Chapter5-2 2024.pdf":
            failures.append(f"UIT-SLIDE-CH05-2-2024 exact_filename expected '#Week07-Chapter5-2 2024.pdf', got '{p2.get('exact_filename')}'")
        if p2.get("sha256") != EXPECTED_P2_SHA:
            failures.append(f"UIT-SLIDE-CH05-2-2024 sha256 mismatch: expected {EXPECTED_P2_SHA}, got {p2.get('sha256')}")
        if p2.get("page_count") != 72:
            failures.append(f"UIT-SLIDE-CH05-2-2024 page_count expected 72, got {p2.get('page_count')}")
        if p2.get("type") != "official_slide":
            failures.append(f"UIT-SLIDE-CH05-2-2024 type expected 'official_slide', got '{p2.get('type')}'")

    # Check Variants are registered as source_variant
    v58 = reg_by_id.get("UIT-SLIDE-CH05-1-2024-VARIANT-LOCAL-58")
    if not v58 or v58.get("type") != "source_variant":
        failures.append("58-page Part 1 variant not properly registered as source_variant")

    v55 = reg_by_id.get("UIT-SLIDE-CH05-2-2024-VARIANT-LOCAL-55")
    if not v55 or v55.get("type") != "source_variant":
        failures.append("55-page Part 2 variant not properly registered as source_variant")

    v32 = reg_by_id.get("UIT-SLIDE-CH05-3-2024-VARIANT-LOCAL-32")
    if not v32 or v32.get("type") != "source_variant":
        failures.append("32-page Part 3 variant not properly registered as source_variant")

    # 2. Slide Coverage Inspection & Exact Range Signature Verification
    coverage_raw = COVERAGE_PATH.read_text(encoding="utf-8")
    dup_keys = check_yaml_duplicate_keys(coverage_raw)
    if dup_keys:
        failures.extend(dup_keys)

    decks = parse_slide_coverage(COVERAGE_PATH)
    deck_by_id = {d.get("source_id"): d for d in decks}

    # Ensure variants are excluded from canonical decks
    for variant_id in [
        "UIT-SLIDE-CH05-1-2024-VARIANT-LOCAL-58",
        "UIT-SLIDE-CH05-2-2024-VARIANT-LOCAL-55",
        "UIT-SLIDE-CH05-3-2024-VARIANT-LOCAL-32",
        "UIT-SLIDE-CH05-3-2024",
    ]:
        if variant_id in deck_by_id:
            failures.append(f"Variant '{variant_id}' must be excluded from canonical decks in slide_coverage.yaml")

    # Validate Part 1 coverage
    d_p1 = deck_by_id.get("UIT-SLIDE-CH05-1-2024")
    if not d_p1:
        failures.append("Missing UIT-SLIDE-CH05-1-2024 in slide_coverage.yaml decks")
    else:
        p1_sections = d_p1.get("sections", [])
        p1_signature = [(str(s.get("page_range")), str(s.get("classification"))) for s in p1_sections]
        if p1_signature != EXPECTED_P1_SIGNATURE:
            failures.append(f"Ch5 Part 1 signature mismatch:\n  Actual:   {p1_signature}\n  Expected: {EXPECTED_P1_SIGNATURE}")

        p1_content_pages = sum(s.get("page_count", 0) for s in p1_sections if s.get("classification") == "CONTENT")
        p1_non_content_pages = sum(s.get("page_count", 0) for s in p1_sections if s.get("classification") == "NON_CONTENT")
        if p1_content_pages != 63:
            failures.append(f"Ch5 Part 1 CONTENT pages expected 63, got {p1_content_pages}")
        if p1_non_content_pages != 4:
            failures.append(f"Ch5 Part 1 NON_CONTENT pages expected 4, got {p1_non_content_pages}")
        if (p1_content_pages + p1_non_content_pages) != 67:
            failures.append(f"Ch5 Part 1 total pages expected 67, got {p1_content_pages + p1_non_content_pages}")

        # Check page coverage continuity 1..67 and SELF_STUDY on page 56
        seen_p1_pages = []
        p56_found = False
        for s in p1_sections:
            pages = parse_page_range(s.get("page_range"))
            seen_p1_pages.extend(pages)
            if 56 in pages:
                p56_found = True
                topic_str = str(s.get("topic", ""))
                notes_str = str(s.get("notes", ""))
                if "SELF_STUDY" not in topic_str and "SELF_STUDY" not in notes_str:
                    failures.append("Page 56 of Ch5 Part 1 must be marked SELF_STUDY")
        if not p56_found:
            failures.append("Page 56 of Ch5 Part 1 not found in section ranges")
        if sorted(seen_p1_pages) != list(range(1, 68)):
            failures.append(f"Ch5 Part 1 pages range gap/overlap: {sorted(seen_p1_pages)[:5]}...{sorted(seen_p1_pages)[-5:]}")

        # Check key topic markers in Part 1
        p1_topics = {str(s.get("page_range")): str(s.get("topic", "")) for s in p1_sections}
        expected_p1_markers = {
            "4-11": ["Producer", "Consumer"],
            "12-13": ["PID"],
            "14-16": ["Race Condition"],
            "17-19": ["Critical Section"],
            "20-25": ["Requirements", "Mutual Exclusion"],
            "26-28": ["Solution classification"],
            "29-30": ["Disable Interrupts"],
            "31-36": ["Software Solution 1"],
            "37-40": ["Software Solution 2"],
            "41-46": ["Peterson"],
            "47-51": ["modern architectures"],
            "52-55": ["Memory Barrier"],
            "56": ["SELF_STUDY"],
            "57-60": ["Mutex Locks"],
            "61-63": ["without busy waiting"],
            "64-65": ["Using Mutex"],
        }
        for prange, markers in expected_p1_markers.items():
            t_str = p1_topics.get(prange, "")
            notes_str = str(next((s.get("notes", "") for s in p1_sections if str(s.get("page_range")) == prange), ""))
            combined = t_str + " " + notes_str
            for m in markers:
                if m.lower() not in combined.lower():
                    failures.append(f"Part 1 range '{prange}' topic missing expected marker '{m}' (topic: '{t_str}')")

    # Validate Part 2 coverage
    d_p2 = deck_by_id.get("UIT-SLIDE-CH05-2-2024")
    if not d_p2:
        failures.append("Missing UIT-SLIDE-CH05-2-2024 in slide_coverage.yaml decks")
    else:
        p2_sections = d_p2.get("sections", [])
        p2_signature = [(str(s.get("page_range")), str(s.get("classification"))) for s in p2_sections]
        if p2_signature != EXPECTED_P2_SIGNATURE:
            failures.append(f"Ch5 Part 2 signature mismatch:\n  Actual:   {p2_signature}\n  Expected: {EXPECTED_P2_SIGNATURE}")

        p2_content_pages = sum(s.get("page_count", 0) for s in p2_sections if s.get("classification") == "CONTENT")
        p2_non_content_pages = sum(s.get("page_count", 0) for s in p2_sections if s.get("classification") == "NON_CONTENT")
        if p2_content_pages != 68:
            failures.append(f"Ch5 Part 2 CONTENT pages expected 68, got {p2_content_pages}")
        if p2_non_content_pages != 4:
            failures.append(f"Ch5 Part 2 NON_CONTENT pages expected 4, got {p2_non_content_pages}")
        if (p2_content_pages + p2_non_content_pages) != 72:
            failures.append(f"Ch5 Part 2 total pages expected 72, got {p2_content_pages + p2_non_content_pages}")

        # Check page coverage continuity 1..72
        seen_p2_pages = []
        for s in p2_sections:
            pages = parse_page_range(s.get("page_range"))
            seen_p2_pages.extend(pages)
        if sorted(seen_p2_pages) != list(range(1, 73)):
            failures.append(f"Ch5 Part 2 pages range gap/overlap: {sorted(seen_p2_pages)[:5]}...{sorted(seen_p2_pages)[-5:]}")

        # Check key topic markers in Part 2
        p2_topics = {str(s.get("page_range")): str(s.get("topic", "")) for s in p2_sections}
        expected_p2_markers = {
            "4-15": ["5.7.1", "Semaphore definition"],
            "16-17": ["5.7.2", "Semaphore types"],
            "18-22": ["5.7.3", "Semaphore implementation"],
            "23-26": ["5.7.4", "Semaphore applications"],
            "27-29": ["5.7.5", "Semaphore remarks"],
            "30-32": ["5.7.6", "Problems when using Semaphore"],
            "33-36": ["5.8.1", "Monitor"],
            "37-40": ["5.8.2", "Condition Variable"],
            "41-43": ["5.9", "Liveness"],
            "44-46": ["5.10.1", "Bounded-Buffer problem"],
            "47-50": ["5.10.2", "Bounded-Buffer solution"],
            "51-53": ["5.10.3", "Bounded-Buffer mistakes"],
            "54-57": ["5.11.1", "Readers-Writers problem"],
            "58-60": ["5.11.2", "Readers-Writers solution"],
            "61-63": ["5.12.1", "Dining-Philosophers problem"],
            "64-70": ["5.12.2", "Dining-Philosophers solutions"],
        }
        for prange, markers in expected_p2_markers.items():
            t_str = p2_topics.get(prange, "")
            for m in markers:
                if m.lower() not in t_str.lower():
                    failures.append(f"Part 2 range '{prange}' topic missing expected marker '{m}' (topic: '{t_str}')")

        # 3. Assert Absence of Unsupported Tier-A Claims
        ch5_deck_text = str(d_p1) + " " + str(d_p2)
        if "priority inversion" in ch5_deck_text.lower():
            failures.append("Unsupported Tier-A claim 'Priority Inversion' found in Chapter 5 canonical slide coverage")
        if "priority inheritance" in ch5_deck_text.lower():
            failures.append("Unsupported Tier-A claim 'Priority Inheritance' found in Chapter 5 canonical slide coverage")

    # 4. Verify Chapter 5 Theory is NOT Authored
    if CH5_THEORY_PATH.exists():
        content = CH5_THEORY_PATH.read_text(encoding="utf-8").strip()
        if len(content) > 100:
            failures.append(f"Chapter 5 theory file '{CH5_THEORY_PATH.name}' must NOT be authored during source-map phase")

    # Output Results
    if failures:
        print("FAIL: Chapter 5 canonical source map precision validation failed:")
        for f in failures:
            print(f"  - {f}")
        return False

    print("PASS: Chapter 5 canonical source map verified with exact precision:")
    print("  [OK] Exact Range Signatures: Part 1 (19 items) & Part 2 (19 items) strictly verified")
    print("  [OK] Range Totals: Part 1 = 63 CONTENT + 4 NON_CONTENT; Part 2 = 68 CONTENT + 4 NON_CONTENT")
    print("  [OK] Topic-family markers verified for all 32 content sub-ranges")
    print("  [OK] Unsupported Tier-A claims (Priority Inversion / Inheritance) count = 0")
    print("  [OK] Duplicate YAML keys in Ch5 coverage = 0")
    print("  [OK] Variants 58p, 55p, 32p properly reclassified and excluded from canonical coverage")
    print("  [OK] Page 56 of Part 1 verified as SELF_STUDY")
    print("  [OK] Chapter 5 theory verified NOT authored")
    return True


if __name__ == "__main__":
    success = validate_ch05()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""Global Source Registry SSOT Canonical Drift Checker (Check-only).

This tool validates content/sources/registry.yaml with strict SSOT guarantees:
- content/sources/registry.yaml is the Single Source of Truth (SSOT).
- Operates in check-only mode: validates canonical source identities and Source Ledger
  against ground truth without modifying any files.
- Zero mutation: no destructive overwrites of locked canonical source IDs.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Ensure standard UTF-8 console output
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content/sources/registry.yaml"
SOURCE_LEDGER_PATH = ROOT / "research/SOURCE_LEDGER.md"

sys.path.insert(0, str(ROOT / "scripts"))
from research_utils import parse_registry  # noqa: E402

# Ground-truth canonical definitions that MUST NOT drift or regress
CANONICAL_GROUND_TRUTH: dict[str, dict[str, str | int]] = {
    "UIT-OUTLINE-2024": {
        "tier": "A",
        "type": "official_outline",
        "exact_filename": "IT007_HeDieuHanh_14.2024.pdf",
        "sha256": "89547bca603d2486225f1e7c4f3ca767882964d83229ced16dc36b17eea309ab",
        "byte_size": 418490,
        "page_count": 19,
    },
    "UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG": {
        "tier": "A",
        "type": "source_variant",
        "exact_filename": "De cuong.pdf",
        "sha256": "8ff13e4ddabee1fde580b84827e3e1c2733d2822ff9ca062d97e43a7f8151cdd",
        "byte_size": 452857,
        "page_count": 19,
    },
    "UIT-SLIDE-CH04-1-2024": {
        "tier": "A",
        "type": "official_slide",
        "exact_filename": "#Week04-Chapter4-1 2024.pdf",
        "sha256": "f2323c438f260d0b5c37322e78eb0eee7af3e036bec109d68de9db31c4714dae",
        "page_count": 74,
    },
    "UIT-SLIDE-CH04-2-2024": {
        "tier": "A",
        "type": "official_slide",
        "exact_filename": "#Week05-Chapter4-2 2024.pdf",
        "sha256": "9221a7e4a42ff88a98ee8f2980d879860ded2abd5e6de04ca35d7f768aee2040",
        "page_count": 59,
    },
    "UIT-SLIDE-CH05-1-2024": {
        "tier": "A",
        "type": "official_slide",
        "exact_filename": "#Week06-Chapter5-1 2024.pdf",
        "sha256": "2ef4be67449ea22aada6e8bd69b49b781bbcb8c6f0eb601b16e9f18a004c7416",
        "page_count": 67,
    },
    "UIT-SLIDE-CH05-2-2024": {
        "tier": "A",
        "type": "official_slide",
        "exact_filename": "#Week07-Chapter5-2 2024.pdf",
        "sha256": "f7e9fc9eb9a35f3a02eb60b2c8e01fa134342d0c5256f47deef4247a0db141d2",
        "page_count": 72,
    },
    "UIT-SLIDE-CH06-2024": {
        "tier": "A",
        "type": "official_slide",
        "exact_filename": "#Week08-Chapter6 2024.pdf",
        "sha256": "5cf9e1a31413a042ddc81c83ee6125d9718519d876a13f4dc30d3a5e041ee947",
        "byte_size": 6008743,
        "page_count": 67,
    },
    "UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB": {
        "tier": "A",
        "type": "source_variant",
        "exact_filename": "Week11-Chapter6 2024.pdf",
        "sha256": "e55bf22554028859fc30747a39e72d97ca6e1e3c37e5a1bdcdc5ab94a7c3b56e",
        "byte_size": 5816540,
        "page_count": 67,
    },
    "UIT-QBANK-CH05-2024": {
        "tier": "A",
        "type": "official_qbank",
        "exact_filename": "Bai tap chuong 5 HDH.docx",
        "sha256": "503cd8fdb619bcfd664cfaa198915bc50d0ba6bb910c74d14ccff5252e646186",
    },
    "UIT-QBANK-CH06-2024": {
        "tier": "A",
        "type": "official_qbank",
        "exact_filename": "Bai tap chuong 6 HDH.docx",
        "sha256": "f8f82cc2a29641fbe7545d172485356dfdd78d7a398c01e1f784afca06a25803",
        "byte_size": 101550,
    },
    "UIT-SLIDE-CH07-2024": {
        "tier": "A",
        "type": "official_slide",
        "exact_filename": "#Week09-Chapter7 2024.pdf",
        "sha256": "86e6260cdc2fd1461277434fa74ee0a325c945ba9cb5d1b0d4ba46a76045c5a9",
        "byte_size": 7462286,
        "page_count": 72,
    },
    "UIT-SLIDE-CH07-2024-VARIANT-WEEK12-72": {
        "tier": "B",
        "type": "source_variant",
        "exact_filename": "Week12-Chapter7 2024.pdf",
        "sha256": "4b622457cd5592dc83afce32f8ca5ddf1c9e9bca6defdbed36150e80f0717177",
        "byte_size": 7459415,
        "page_count": 72,
    },
    "UIT-QBANK-CH07-2024": {
        "tier": "A",
        "type": "official_qbank",
        "exact_filename": "Bai tap chuong 7 HDH.docx",
        "sha256": "5b03f4e0691855f38d43872f79ba61a21378fea3ec5ee2551be5321a29b88e40",
        "byte_size": 23960,
    },
    "UIT-QBANK-CH07-2024-VARIANT-DRIVE-85P": {
        "tier": "B",
        "type": "source_variant",
        "exact_filename": "Bai tap chuong 7 HDH.docx",
        "sha256": "f8e523d10b0c75a18f5551f3f1f59c5827830ec56c095e92d68e4bfb50ec0b77",
        "byte_size": 22871,
    },
}

# Stale legacy IDs that must never be reintroduced
DISALLOWED_STALE_IDS = {
    "UIT-SLIDE-CH05-1-2024-CANONICAL-USER",
    "UIT-SLIDE-CH05-2-2024-CANONICAL-USER",
}


def check_registry_drift(registry_rows: list[dict]) -> list[str]:
    """Verify that committed registry matches canonical ground truth with zero drift."""
    failures: list[str] = []
    reg_by_id = {r.get("id"): r for r in registry_rows}

    # 1. Check for disallowed stale IDs
    for stale_id in DISALLOWED_STALE_IDS:
        if stale_id in reg_by_id:
            failures.append(f"Disallowed stale ID found in registry: {stale_id}")

    # 2. Check canonical ground truth invariants
    for source_id, expected_fields in CANONICAL_GROUND_TRUTH.items():
        actual = reg_by_id.get(source_id)
        if not actual:
            failures.append(f"Missing mandatory canonical source in registry: {source_id}")
            continue

        for field_name, expected_value in expected_fields.items():
            actual_value = actual.get(field_name)
            if actual_value != expected_value:
                failures.append(
                    f"Canonical drift in {source_id}.{field_name}: "
                    f"registry has '{actual_value}', ground truth expects '{expected_value}'"
                )

    # 3. Check student variants are never Tier A
    for sid in ["UIT-QBANK-CH06-2024-VARIANT-STUDENT-23520237", "UIT-REF-CH06-STUDENT-23521551-PDF"]:
        row = reg_by_id.get(sid)
        if row and row.get("tier") == "A":
            failures.append(f"Student submission variant {sid} must not be Tier A")

    return failures


def check_source_ledger_consistency(registry_rows: list[dict]) -> list[str]:
    """Verify that research/SOURCE_LEDGER.md canonical rows agree with registry."""
    failures: list[str] = []
    if not SOURCE_LEDGER_PATH.exists():
        return ["research/SOURCE_LEDGER.md missing"]

    ledger_text = SOURCE_LEDGER_PATH.read_text(encoding="utf-8")
    reg_by_id = {r.get("id"): r for r in registry_rows}

    # Expected canonical pairings: (Source Ledger Row ID, Registry ID)
    canonical_checks = [
        ("A-01", "UIT-OUTLINE-2024"),
        ("A-05", "UIT-SLIDE-CH04-1-2024"),
        ("A-06", "UIT-SLIDE-CH04-2-2024"),
        ("A-08", "UIT-SLIDE-CH05-1-2024"),
        ("A-10", "UIT-SLIDE-CH05-2-2024"),
        ("A-12", "UIT-SLIDE-CH06-2024"),
        ("A-13", "UIT-SLIDE-CH07-2024"),
        ("A-22", "UIT-QBANK-CH07-2024"),
    ]

    for ledger_id, reg_id in canonical_checks:
        reg_entry = reg_by_id.get(reg_id)
        if not reg_entry:
            failures.append(f"Registry missing expected canonical ID '{reg_id}'")
            continue
        expected_filename = reg_entry.get("exact_filename")
        pattern = rf"\|\s*\*\*{re.escape(ledger_id)}\*\*\s*\|\s*`{re.escape(expected_filename)}`"
        if not re.search(pattern, ledger_text):
            failures.append(
                f"SOURCE_LEDGER.md canonical row '{ledger_id}' does not match registry canonical filename '{expected_filename}'"
            )

    # Disallow known local variants in canonical authority rows
    disallowed_in_canonical = [
        ("A-01", "De cuong.pdf"),
        ("A-13", "Week12-Chapter7 2024.pdf"),
        ("A-05", "Week04-Chapter4-1 2024.pdf"),
        ("A-06", "Week05-Chapter4-2 2024.pdf"),
        ("A-08", "Week07-Chapter5-1 2024.pdf"),
        ("A-10", "Week09-Chapter5-2 2024.pdf"),
        ("A-11", "Week10-Chapter5-3 2024.pdf"),
        ("A-12", "Week11-Chapter6 2024.pdf"),
    ]

    for ledger_id, variant_filename in disallowed_in_canonical:
        pattern = rf"\|\s*\*\*{re.escape(ledger_id)}\*\*\s*\|\s*`{re.escape(variant_filename)}`"
        if re.search(pattern, ledger_text):
            failures.append(
                f"SOURCE_LEDGER.md canonical row '{ledger_id}' contains variant '{variant_filename}' (must be variant row only)"
            )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Global Source Registry SSOT Canonical Drift Checker (Check-only)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="Perform dry-run verification against SSOT ground truth (default; no writes)",
    )
    args = parser.parse_args()

    print(">>> Checking Global Source Registry for Canonical SSOT Drift...")

    if not REGISTRY_PATH.exists():
        print(f"FAIL: Registry file missing at {REGISTRY_PATH}")
        return 1

    rows = parse_registry(REGISTRY_PATH)
    drift_errors = check_registry_drift(rows)
    ledger_errors = check_source_ledger_consistency(rows)
    all_errors = drift_errors + ledger_errors

    if all_errors:
        print("REGISTRY / SOURCE LEDGER SSOT DRIFT DETECTED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print(f"REGISTRY SSOT CHECK PASS: Verified {len(rows)} registered sources.")
    print("  [OK] UIT-OUTLINE-2024 -> IT007_HeDieuHanh_14.2024.pdf (418,490 bytes)")
    print("  [OK] UIT-OUTLINE-2024-VARIANT-LOCAL-DECUONG -> De cuong.pdf (variant)")
    print("  [OK] UIT-SLIDE-CH04-1-2024 -> #Week04-Chapter4-1 2024.pdf (74 pages)")
    print("  [OK] UIT-SLIDE-CH04-2-2024 -> #Week05-Chapter4-2 2024.pdf (59 pages)")
    print("  [OK] UIT-SLIDE-CH05-1-2024 -> #Week06-Chapter5-1 2024.pdf (67 pages)")
    print("  [OK] UIT-SLIDE-CH05-2-2024 -> #Week07-Chapter5-2 2024.pdf (72 pages)")
    print("  [OK] UIT-SLIDE-CH06-2024 -> #Week08-Chapter6 2024.pdf (6,008,743 bytes)")
    print("  [OK] UIT-SLIDE-CH06-2024-VARIANT-WEEK11-5MB -> Week11-Chapter6 2024.pdf (variant)")
    print("  [OK] Zero stale legacy IDs detected (CH05 CANONICAL-USER correctly absent)")
    print("  [OK] SOURCE_LEDGER.md Tier-A canonical rows match registry SSOT")
    print("  [OK] Zero mutations performed (check/dry-run mode)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

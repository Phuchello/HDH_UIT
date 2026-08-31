"""Small dependency-free readers for the repository's deliberately simple YAML data.

The CI environment only guarantees Python's standard library plus pypdf.  These
helpers therefore parse the flat record lists used by the research manifests
without silently treating summary numbers as evidence.
"""

from __future__ import annotations

import re
from pathlib import Path


def scalar(value: str):
    value = value.split(" #", 1)[0].strip().strip('"\'')
    if value in {"", "null", "None"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _records(path: Path, start_pattern: str):
    """Parse flat YAML records beginning with a matching list-item line."""
    if not path.exists():
        return []
    records = []
    current = None
    block_key = None
    block_indent = None
    block_lines = []

    def finish_block():
        nonlocal block_key, block_indent, block_lines
        if block_key is not None and current is not None:
            # Literal YAML block scalars preserve line boundaries.  Remove only
            # the structural indentation and the implicit final newline; the
            # source wording itself remains unchanged.
            current[block_key] = "\n".join(block_lines).rstrip("\n")
        block_key = None
        block_indent = None
        block_lines = []

    start_re = re.compile(start_pattern)
    for raw in path.read_text(encoding="utf-8").splitlines():
        if block_key is not None:
            indent = len(raw) - len(raw.lstrip())
            if not raw.strip() or indent > block_indent:
                block_lines.append(raw[(block_indent + 2):] if raw.strip() else "")
                continue
            finish_block()
        if start_re.match(raw):
            if current is not None:
                records.append(current)
            current = {}
            key, value = raw.strip()[2:].split(":", 1)
            current[key.strip()] = scalar(value)
            continue
        if current is None:
            continue
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        value = value.strip()
        if value in {"|", "|-", "|+"}:
            block_key = key.strip()
            block_indent = len(raw) - len(raw.lstrip())
            block_lines = []
            continue
        current[key.strip()] = scalar(value)
    finish_block()
    if current is not None:
        records.append(current)
    return records


def parse_registry(path: Path):
    return _records(path, r"^  - id:")


def parse_questions(path: Path):
    return _records(path, r"^  - source_id:")


def parse_exams(path: Path):
    return _records(path, r"^  - exam_id:")


def parse_page_range(value: str):
    match = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", str(value or "").strip())
    if not match:
        return []
    first = int(match.group(1))
    last = int(match.group(2) or first)
    return list(range(first, last + 1))


def parse_slide_coverage(path: Path):
    """Read slide decks and sections, retaining every declared section field."""
    decks = []
    deck = None
    section = None
    if not path.exists():
        return decks
    for raw in path.read_text(encoding="utf-8").splitlines():
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()
        if indent == 2 and stripped.startswith("- source_id:"):
            if deck is not None:
                decks.append(deck)
            deck = {"sections": []}
            key, value = stripped[2:].split(":", 1)
            deck[key.strip()] = scalar(value)
            section = None
            continue
        if deck is None:
            continue
        if indent >= 6 and stripped.startswith("- page_range:"):
            key, value = stripped[2:].split(":", 1)
            section = {key.strip(): scalar(value)}
            deck["sections"].append(section)
            continue
        if section is not None and indent >= 8 and ":" in stripped and not stripped.startswith("-"):
            key, value = stripped.split(":", 1)
            section[key.strip()] = scalar(value)
        elif section is None and indent >= 4 and ":" in stripped and not stripped.startswith("-"):
            key, value = stripped.split(":", 1)
            if key.strip() != "sections":
                deck[key.strip()] = scalar(value)
    if deck is not None:
        decks.append(deck)
    return decks


def expand_coverage(decks):
    """Expand ranges to one deterministic record per physical page."""
    expanded = []
    for deck in decks:
        for section in deck.get("sections", []):
            for page in parse_page_range(section.get("page_range")):
                expanded.append({
                    "source_id": deck.get("source_id"),
                    "page": page,
                    "heading": section.get("heading") or section.get("topic"),
                    "subheading": section.get("subheading") or "",
                    "bullet_clusters": section.get("bullet_clusters") or [section.get("topic", "")],
                    "terms": section.get("terms") or [],
                    "questionable_or_exam_relevant_properties": section.get("questionable_or_exam_relevant_properties") or [],
                    "classification": section.get("classification"),
                    "mapping_status": section.get("mapping_status"),
                    "v2_destination": section.get("v2_destination"),
                    "content_status": section.get("content_status"),
                    "range": section.get("page_range"),
                })
    return expanded

#!/usr/bin/env python3
"""Regression gates for production-only web assets and reader features."""

from __future__ import annotations

import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "public" / "site"
BUILD = ROOT / "scripts" / "build_web.py"
PRODUCTION = ROOT / "src" / "web" / "assets"
REPORT = ROOT / "research" / "data" / "web_feature_validation.json"
REQUIRED = {
    "theory/ch01-overview.html", "theory/ch02-structure.html", "theory/ch03-process.html", "theory/ch04-scheduling.html",
    "questions/subjective/ch01.html", "questions/subjective/ch02.html", "questions/subjective/ch03.html", "questions/subjective/ch04.html",
    "reviews/midterm.html", "labs/lab01-linux-basics.html", "exams/midterm/2023-2024-hk1.html", "glossary/terms.html", "flashcards/ch01-cards.html",
}
SEARCH_CASES = {
    "convoy effect": "theory/ch04-scheduling.html",
    "exponential averaging": "theory/ch04-scheduling.html",
    "dispatch latency": "theory/ch04-scheduling.html",
    "zombie": "theory/ch03-process.html",
    "processor affinity": "theory/ch04-scheduling.html",
}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def reachable() -> set[str]:
    queue, seen = ["index.html"], set()
    while queue:
        current = queue.pop(0)
        if current in seen or not (SITE / current).is_file():
            continue
        seen.add(current)
        parser = Links(); parser.feed((SITE / current).read_text(encoding="utf-8"))
        for href in parser.links:
            if urlparse(href).scheme or href.startswith("//"):
                continue
            path, _ = urldefrag(href)
            if not path:
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(current), path))
            if target.endswith(".html"):
                queue.append(target)
    return seen


def main() -> int:
    failures: list[str] = []
    def expect(condition: bool, message: str) -> None:
        if not condition: failures.append(message)
    source = BUILD.read_text(encoding="utf-8")
    # The build script names ``archive`` only in its destructive-cleanup
    # safety deny-list.  Reject actual archive asset/source references while
    # allowing that guard to remain explicit and testable.
    expect("ARCHIVE_ASSETS" not in source and "archive/" not in source.lower(), "production build references archive")
    expect((PRODUCTION / "css/style.css").is_file() and (PRODUCTION / "js/app.js").is_file(), "production asset tree incomplete")
    index = json.loads((SITE / "search_index.json").read_text(encoding="utf-8"))
    for item in index:
        expect(all(key in item for key in ("title", "summary", "headings", "searchable_text")), f"search record missing body fields: {item.get('id')}")
    for query, route in SEARCH_CASES.items():
        matches = [item.get("url") for item in index if query in " ".join([str(item.get("title", "")), str(item.get("summary", "")), " ".join(item.get("headings", [])), str(item.get("searchable_text", ""))]).lower()]
        expect(route in matches, f"full-text search regression failed: {query} -> {route}")
    home = (SITE / "index.html").read_text(encoding="utf-8")
    expect("reviews/midterm.html" in home and "ÔN TẬP" in home, "Midterm review absent from homepage navigation")
    expect("CUSTOM_STATIC_GENERATOR" not in home, "reader-facing internal build label remains")
    reader_text = "\n".join(path.read_text(encoding="utf-8") for path in SITE.rglob("*.html"))
    expect("Barem chính thức" not in reader_text and "Barem Điểm" not in reader_text and "Barem Chấm" not in reader_text, "forbidden official-score language in reader UI")
    expect("LIÊN KẾT TỪ CÁC TRANG KHÁC" in reader_text, "generated backlinks not rendered")
    reached = reachable(); unreachable = sorted(REQUIRED - reached)
    expect(not unreachable, f"unreachable reader pages: {', '.join(unreachable)}")
    REPORT.write_text(json.dumps({"passed": not failures, "unreachable_reader_pages": unreachable, "search_cases": SEARCH_CASES, "failures": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WEB FEATURE VALIDATION: {'PASS' if not failures else 'FAIL'} (UNREACHABLE_READER_PAGES={len(unreachable)})")
    for failure in failures: print(f"  - {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

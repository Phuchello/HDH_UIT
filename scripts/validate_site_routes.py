#!/usr/bin/env python3
"""Crawl generated HTML and local assets, rejecting broken internal routes."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SITE = ROOT / "public" / "site"
OUTPUT = ROOT / "research" / "data" / "route_validation.json"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if "name" in attrs:
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key) is not None:
                self.links.append((key, attrs[key]))


def _is_external(url: str):
    parsed = urlparse(url)
    return bool(parsed.scheme or parsed.netloc) or url.startswith("//")


def crawl(site: Path):
    broken = []
    internal_count = 0
    pages = sorted(site.rglob("*.html")) if site.exists() else []
    for page in pages:
        parser = LinkParser()
        try:
            parser.feed(page.read_text(encoding="utf-8"))
        except Exception as exc:
            broken.append({"page": page.relative_to(site).as_posix(), "target": "<parse>", "reason": str(exc)})
            continue
        for attr, raw_url in parser.links:
            if not raw_url or _is_external(raw_url) or raw_url.startswith(("mailto:", "javascript:", "data:")):
                continue
            internal_count += 1
            path_part, fragment = urldefrag(raw_url)
            if not path_part:
                if fragment and fragment not in parser.ids:
                    broken.append({"page": page.relative_to(site).as_posix(), "target": raw_url, "reason": "missing same-page anchor"})
                elif not fragment:
                    broken.append({"page": page.relative_to(site).as_posix(), "target": raw_url, "reason": "empty internal URL"})
                continue
            target_rel = posixpath.normpath(posixpath.join(page.relative_to(site).parent.as_posix(), path_part))
            target = site / Path(target_rel)
            if not target.is_file():
                broken.append({"page": page.relative_to(site).as_posix(), "target": raw_url, "reason": "target does not exist"})
                continue
            if fragment and target.suffix.lower() in {".html", ".htm"}:
                target_parser = LinkParser()
                target_parser.feed(target.read_text(encoding="utf-8"))
                if fragment not in target_parser.ids:
                    broken.append({"page": page.relative_to(site).as_posix(), "target": raw_url, "reason": "missing target anchor"})
    result = {
        "site_root": site.name,
        "pages": len(pages),
        "internal_links": internal_count,
        "broken": broken,
        "passed": not broken and bool(pages),
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SITE ROUTE VALIDATION: {'PASS' if result['passed'] else 'FAIL'} ({len(pages)} pages, {len(broken)} broken routes)")
    if broken:
        for item in broken[:25]:
            print(f"  - {item['page']} -> {item['target']}: {item['reason']}")
    return result["passed"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", default=str(DEFAULT_SITE))
    args = parser.parse_args()
    sys.exit(0 if crawl(Path(args.site_root).resolve()) else 1)

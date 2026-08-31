#!/usr/bin/env python3
"""Deterministic custom static generator for the V2 canonical content tree.

The renderer intentionally has no network dependency.  It expands each
Markdown source into one HTML route and emits search/graph data from the same
document manifest, so the web companion remains safe to scale.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTENT = ROOT / "content"
DEFAULT_OUTPUT = ROOT / "public" / "site"
PRODUCTION_ASSETS = ROOT / "src" / "web" / "assets"
SHARED_VENDOR = ROOT / "src" / "shared" / "vendor"


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) != 3:
        return {}, text
    meta, active = {}, None
    for raw in parts[1].strip().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-") and active:
            meta[active].append(line[1:].strip().strip('"\''))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip().strip('"\'')
        if not value:
            meta[key], active = [], key
        else:
            active = None
            if value == "null":
                value = None
            elif value == "true":
                value = True
            elif value == "false":
                value = False
            meta[key] = value
    return meta, parts[2]


def slugify(value):
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", ascii_value.lower()).strip("-") or "section"


def split_table_row(line):
    text = line.strip().strip("|")
    cells, current, code, escaped = [], [], False, False
    for char in text:
        if char == "`" and not escaped:
            code = not code
        if char == "|" and not code and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    cells.append("".join(current).strip())
    return cells


def inline(text, routes, current_rel):
    placeholders = {}
    def protect_code(match):
        key = f"@@CODE{len(placeholders)}@@"
        placeholders[key] = f"<code>{html.escape(match.group(1))}</code>"
        return key
    text = re.sub(r"`([^`]+)`", protect_code, text)
    text = html.escape(text, quote=False)
    def wikilink(match):
        target = match.group(1).strip()
        label = target
        if "|" in target:
            target, label = [part.strip() for part in target.split("|", 1)]
        if target in routes:
            base = Path(current_rel).parent.as_posix() or "."
            href = os.path.relpath(routes[target], base).replace("\\", "/")
            return f'<a class="wikilink" href="{href}">{html.escape(label)}</a>'
        return f'<a class="wikilink" href="#{html.escape(target)}">{html.escape(label)}</a>'
    text = re.sub(r"\[\[([^\]]+)\]\]", wikilink, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def render_table(lines, routes, current_rel):
    if len(lines) < 2:
        return ""
    header = split_table_row(lines[0])
    separator = split_table_row(lines[1])
    has_separator = separator and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in separator)
    body = lines[2:] if has_separator else lines[1:]
    cells = [f"<th>{inline(item, routes, current_rel)}</th>" for item in header]
    rows = []
    for line in body:
        row = split_table_row(line)
        rows.append("<tr>" + "".join(f"<td>{inline(item, routes, current_rel)}</td>" for item in row) + "</tr>")
    return "<table><thead><tr>" + "".join(cells) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def render_callout(kind, body, doc_id, routes, current_rel):
    lower = kind.lower()
    if lower in {"studycard", "subjectivepractice"}:
        identifier = re.search(r'id=["\']([^"\']+)', body)
        item_id = identifier.group(1) if identifier else f"{lower}-{doc_id}"
        body = re.sub(r'^\s*id=["\'][^"\']+["\']\s*\n?', "", body, count=1)
        if lower == "studycard":
            question, hint, keypoints, answer = body, "", "", ""
            for marker, field in (("<!-- hint -->", "hint"), ("<!-- keypoints -->", "keypoints"), ("<!-- answer -->", "answer")):
                if marker in question:
                    before, question = question.split(marker, 1)
                    if field == "hint":
                        hint = question
                    elif field == "keypoints":
                        keypoints = question
                    else:
                        answer = question
                    question = before
            parts = [f'<div class="study-card" data-card-id="{html.escape(item_id)}"><div class="card-header"><span class="card-tag">Active Recall</span><span class="card-stats">Tự học tương tác</span></div>', f'<div class="card-question">{inline(question.strip(), routes, current_rel)}</div>']
            if hint:
                parts.append(f'<div class="card-section card-hint"><strong>💡 Gợi ý:</strong> {inline(hint.strip(), routes, current_rel)}</div>')
            if keypoints:
                items = [f"<li>{inline(line.lstrip('- ').strip(), routes, current_rel)}</li>" for line in keypoints.splitlines() if line.strip().startswith("-")]
                parts.append('<div class="card-section card-keypoints"><strong>🔑 Từ khóa bắt buộc:</strong><ul>' + "".join(items) + "</ul></div>")
            if answer:
                parts.append(f'<div class="card-section card-answer"><strong>📖 Lời giải hoàn chỉnh:</strong><p>{inline(answer.strip(), routes, current_rel)}</p></div>')
            parts.append('<div class="card-actions"><button class="btn-card success btn-remember">✅ Đã Thuộc</button><button class="btn-card danger btn-forgot">❌ Chưa Nhớ</button></div></div>')
            return "".join(parts)
        score = re.search(r'max_score=([0-9.]+)', body)
        prompt, rubric = body.split("<!-- rubric", 1) if "<!-- rubric" in body else (body, "")
        rubric = rubric.split("-->", 1)[-1]
        rows = []
        for line in rubric.splitlines():
            if line.strip().startswith("-"):
                weight = re.search(r"\[([0-9.]+)\s*điểm\]", line)
                rows.append(f'<div class="rubric-item"><input type="checkbox" class="rubric-check" data-weight="{weight.group(1) if weight else "0.5"}"><div>{inline(line.lstrip("- ").strip(), routes, current_rel)}</div></div>')
        return f'<div class="subjective-practice" data-practice-id="{html.escape(item_id)}" data-max-score="{score.group(1) if score else "1.0"}"><div class="practice-header"><h3>Luyện Tập Viết Tự Luận</h3><span class="card-tag">Tự đánh giá</span></div><div>{inline(prompt.strip(), routes, current_rel)}</div><textarea class="practice-textarea" aria-label="Bài làm tự luận"></textarea><button class="btn-card primary btn-compare">So sánh với Rubric tự kiểm tra</button><div class="rubric-container" aria-label="Rubric tự kiểm tra">{''.join(rows)}<p class="self-check-score">Tự kiểm tra: <output class="current-score">0.00</output> / {score.group(1) if score else "1.0"}</p></div></div>'
    title = {"characteristics": "ĐẶC TÍNH KỸ THUẬT", "note": "LƯU Ý QUAN TRỌNG", "important": "YÊU CẦU QUAN TRỌNG", "warning": "CẢNH BÁO KỸ THUẬT", "tip": "KHUYẾN NGHỊ THỰC HÀNH"}.get(lower, lower.upper())
    body_html = inline(body, routes, current_rel).replace("\n", "<br>")
    return f'<div class="callout {html.escape(lower)}"><div class="callout-title">{title}</div><p>{body_html}</p></div>'


def render_fenced_code(language, code):
    """Render a fenced block while preserving code bytes and indentation."""
    code_text = "\n".join(code)
    return f'<pre><code class="language-{html.escape(language)}">{html.escape(code_text)}</code></pre>'


def parse_indented_fence(lines, start, parent_indent):
    """Parse a fenced block indented as a list-item continuation.

    CommonMark permits a fenced block to be indented beneath a list item.  The
    handbook uses two-space continuation indentation, so the fence indentation
    is removed from each code line while indentation inside the code remains
    untouched.  Return ``(html, next_index)`` or ``(None, start)`` when the
    current line is not such a fence.
    """
    opening = re.match(r"^(?P<indent> +)```(?P<language>.*)$", lines[start])
    if not opening or len(opening.group("indent")) <= parent_indent:
        return None, start
    fence_indent = len(opening.group("indent"))
    language = opening.group("language").strip()
    index = start + 1
    code = []
    while index < len(lines):
        current = lines[index]
        if current.strip().startswith("```") and len(current) - len(current.lstrip(" ")) <= fence_indent:
            return render_fenced_code(language, code), index + 1
        if current.strip():
            code.append(current[fence_indent:] if current.startswith(" " * fence_indent) else current)
        else:
            code.append("")
        index += 1
    # Keep an unterminated fence visible as a code block, matching root-level
    # fence handling while allowing the rest of the list to continue safely.
    return render_fenced_code(language, code), index


def render_blockquote_body(lines, routes, current_rel):
    """Render blockquote text while preserving fenced code blocks."""
    parts, paragraph, index = [], [], 0

    def flush_paragraph():
        if paragraph:
            parts.append(inline("\n".join(paragraph), routes, current_rel).replace("\n", "<br>"))
            paragraph.clear()

    while index < len(lines):
        opening = re.match(r"^\s*```(?P<language>.*)$", lines[index])
        if not opening:
            paragraph.append(lines[index])
            index += 1
            continue
        flush_paragraph()
        language, code = opening.group("language").strip(), []
        index += 1
        while index < len(lines) and not re.match(r"^\s*```", lines[index]):
            code.append(lines[index])
            index += 1
        if index < len(lines):
            index += 1
        parts.append(render_fenced_code(language, code))
    flush_paragraph()
    return "<br>".join(parts)


def parse_indented_blockquote(lines, start, parent_indent, routes, current_rel):
    """Parse a blockquote indented as a list-item continuation."""
    opening = re.match(r"^(?P<indent> +)>\s?(?P<body>.*)$", lines[start])
    if not opening or len(opening.group("indent")) <= parent_indent:
        return None, start
    quote_indent = len(opening.group("indent"))
    body, index = [], start
    while index < len(lines):
        match = re.match(r"^(?P<indent> +)>\s?(?P<body>.*)$", lines[index])
        if match and len(match.group("indent")) >= quote_indent:
            body.append(match.group("body"))
            index += 1
            continue
        if not lines[index].strip() and index + 1 < len(lines):
            next_quote = re.match(r"^(?P<indent> +)>\s?(?P<body>.*)$", lines[index + 1])
            if next_quote and len(next_quote.group("indent")) >= quote_indent:
                body.append("")
                index += 1
                continue
        break
    return f"<blockquote>{render_blockquote_body(body, routes, current_rel)}</blockquote>", index


HORIZONTAL_RULE_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")


def markdown_to_html(text, doc_id, routes, current_rel):
    lines = text.replace("\r\n", "\n").split("\n")
    output, index = [], 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            language, code = line[3:].strip(), []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            output.append(render_fenced_code(language, code))
            continue
        if HORIZONTAL_RULE_RE.fullmatch(line):
            output.append("<hr>")
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*$", line)
        if heading:
            title, level = heading.group(2).strip(), len(heading.group(1))
            output.append(f'<h{level} id="{slugify(title)}">{inline(title, routes, current_rel)}</h{level}>')
            index += 1
            continue
        callout = re.match(r"^>\s*\[!([A-Za-z0-9_-]+)\].*$", line)
        if callout:
            kind, body = callout.group(1), []
            index += 1
            while index < len(lines) and lines[index].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[index]))
                index += 1
            # Keep attributes from the marker line (for StudyCard IDs/max_score)
            marker_attrs = line.split("]", 1)[1].strip() if "]" in line else ""
            output.append(render_callout(kind, marker_attrs + "\n" + "\n".join(body).strip(), doc_id, routes, current_rel))
            continue
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table = []
            while index < len(lines) and lines[index].strip().startswith("|") and lines[index].strip().endswith("|"):
                table.append(lines[index])
                index += 1
            output.append(render_table(table, routes, current_rel))
            continue
        list_match = LIST_ITEM_RE.match(line)
        if list_match:
            rendered_list, index = render_list(lines, index, routes, current_rel)
            output.append(rendered_list)
            continue
        if line.startswith(">"):
            body = []
            while index < len(lines) and lines[index].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[index]))
                index += 1
            output.append(f'<blockquote>{render_blockquote_body(body, routes, current_rel)}</blockquote>')
            continue
        if not line.strip():
            index += 1
            continue
        paragraph = [line]
        index += 1
        while index < len(lines) and lines[index].strip() and not re.match(r"^(#{1,6})\s+|^```|^>|^\s*[-*+] |^\s*\d+[.] |^\s*\|", lines[index]):
            paragraph.append(lines[index])
            index += 1
        para_text = inline("\n".join(paragraph), routes, current_rel).replace(chr(10), "<br>")
        output.append(f"<p>{para_text}</p>")
    return "\n\n".join(output)


def relative_link(from_route, to_route):
    base = Path(from_route).parent.as_posix() or "."
    return os.path.relpath(to_route, base).replace("\\", "/")


def search_text(markdown: str) -> str:
    """Canonical-document text for offline full-text search; never derive it from HTML."""
    clean = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    clean = re.sub(r"<!--.*?-->", " ", clean, flags=re.DOTALL)
    clean = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", clean)
    clean = re.sub(r"[`*_>#|]", " ", clean)
    return re.sub(r"\s+", " ", clean).strip()


LIST_ITEM_RE = re.compile(r"^(?P<indent> *)(?P<marker>[-*+] |\d+[.] )(?P<text>.*)$")


def render_list(lines, start, routes, current_rel):
    """Render the handbook's indentation-aware list subset.

    Child lists are attached to the preceding ``<li>``.  This supports the
    mixed ordered/unordered nesting used by the handbook without attempting
    the full CommonMark grammar.
    """
    first = LIST_ITEM_RE.match(lines[start])
    if not first:
        return "", start
    root_indent = len(first.group("indent"))
    tag = "ol" if first.group("marker")[0].isdigit() else "ul"
    output = [f"<{tag}>"]
    index = start
    while index < len(lines):
        match = LIST_ITEM_RE.match(lines[index])
        if not match or len(match.group("indent")) != root_indent:
            break
        item_text = inline(match.group("text"), routes, current_rel)
        index += 1
        nested = []
        while index < len(lines):
            child = LIST_ITEM_RE.match(lines[index])
            if child and len(child.group("indent")) > root_indent:
                child_html, index = render_list(lines, index, routes, current_rel)
                nested.append(child_html)
                continue
            if HORIZONTAL_RULE_RE.fullmatch(lines[index]) and len(lines[index]) - len(lines[index].lstrip(" ")) > root_indent:
                nested.append("<hr>")
                index += 1
                continue
            fenced_html, fenced_index = parse_indented_fence(lines, index, root_indent)
            if fenced_html is not None:
                nested.append(fenced_html)
                index = fenced_index
                continue
            quote_html, quote_index = parse_indented_blockquote(lines, index, root_indent, routes, current_rel)
            if quote_html is not None:
                nested.append(quote_html)
                index = quote_index
                continue
            break
        output.append(f"<li>{item_text}{''.join(nested)}</li>")
    output.append(f"</{tag}>")
    return "".join(output), index


def assert_safe_output_dir(output_dir):
    """Validate an output path without mutating the filesystem.

    Destructive cleanup is allowlisted to the canonical generated site and to
    descendants of the operating system's real temporary directory.  Every
    path is resolved first so ``..`` and symlinked components cannot bypass
    the policy.
    """
    candidate = Path(output_dir).expanduser()
    if candidate.is_symlink():
        raise RuntimeError(f"Refusing to clean symlink output directory: {candidate}")
    resolved = candidate.resolve()
    production_root = (ROOT / "public" / "site").resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    allowed = (
        resolved == production_root
        or production_root in resolved.parents
        or temp_root in resolved.parents
    )
    if not allowed:
        raise RuntimeError(f"Refusing unsafe generated output directory: {resolved}")
    if candidate.exists() and not candidate.is_dir():
        raise RuntimeError(f"Generated output path is not a directory: {resolved}")
    return resolved


def clean_output_dir(output_dir):
    """Safely make a generated output directory represent one clean build."""
    output_dir = assert_safe_output_dir(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for child in list(output_dir.iterdir()):
        child_resolved = child.resolve()
        if output_dir not in child_resolved.parents:
            raise RuntimeError(f"Refusing cleanup outside output directory: {child}")
        if child.is_symlink() or child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)
    return output_dir


def build_site(content_root=DEFAULT_CONTENT, output_dir=DEFAULT_OUTPUT):
    content_root = Path(content_root)
    output_dir = clean_output_dir(output_dir)
    assets = output_dir / "assets"
    if not PRODUCTION_ASSETS.is_dir():
        raise RuntimeError(f"Missing production web assets: {PRODUCTION_ASSETS}")
    shutil.copytree(PRODUCTION_ASSETS, assets, dirs_exist_ok=True)
    vendor = assets / "vendor"
    vendor.mkdir(parents=True, exist_ok=True)
    if SHARED_VENDOR.exists():
        shutil.copytree(SHARED_VENDOR, vendor, dirs_exist_ok=True)

    docs = []
    for source in sorted(content_root.glob("**/*.md")):
        rel = source.relative_to(content_root)
        meta, body = parse_frontmatter(source.read_text(encoding="utf-8"))
        doc_id = meta.get("id") or rel.with_suffix("").as_posix()
        docs.append({"path": source, "rel": rel.as_posix(), "id": doc_id, "title": meta.get("title", doc_id), "summary": meta.get("summary", ""), "meta": meta, "body": body, "route": rel.with_suffix(".html").as_posix()})
    routes = {doc["id"]: doc["route"] for doc in docs}
    routes.update({Path(doc["route"]).stem: doc["route"] for doc in docs})

    for doc in docs:
        doc["headings"] = re.findall(r"^#{1,6}\s+(.+?)\s*$", doc["body"], flags=re.MULTILINE)
        doc["searchable_text"] = search_text(doc["body"])
    search = [{"id": doc["id"], "title": doc["title"], "summary": doc["summary"], "headings": doc["headings"], "searchable_text": doc["searchable_text"], "url": doc["route"], "snippet": doc["summary"] or doc["title"]} for doc in docs]
    (output_dir / "search_index.json").write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    graph_nodes = [{"id": doc["id"], "label": doc["title"][:32], "link": doc["route"], "x": 40 + (i * 67) % 270, "y": 35 + (i * 43) % 125, "r": 7, "color": "#0969da"} for i, doc in enumerate(docs)]
    graph_edges = [{"from": doc["id"], "to": rel} for doc in docs for rel in (doc["meta"].get("related", []) if isinstance(doc["meta"].get("related", []), list) else []) if rel in routes]
    (output_dir / "graph_data.json").write_text(json.dumps({"nodes": graph_nodes, "edges": graph_edges}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def nav(current):
        groups = [("LÝ THUYẾT", "theory"), ("NGÂN HÀNG CÂU HỎI", "questions"), ("ÔN TẬP", "reviews"), ("THỰC HÀNH", "labs"), ("ĐỀ THI & TRA CỨU", ("exams", "glossary", "flashcards"))]
        out = []
        for label, kinds in groups:
            out.append(f'<div class="nav-section-title">{label}</div><ul class="nav-tree">')
            for doc in docs:
                if (any(kind in doc["rel"] for kind in kinds) if isinstance(kinds, tuple) else kinds in doc["rel"]):
                    active = " active" if doc["route"] == current else ""
                    out.append(f'<li class="nav-tree-item"><a class="nav-link{active}" href="{relative_link(current, doc["route"])}">{html.escape(doc["title"])}</a></li>')
            out.append("</ul>")
        return "\n".join(out)

    def page(doc):
        route, depth = doc["route"], len(Path(doc["route"]).parts) - 1
        prefix = "../" * depth
        rendered = markdown_to_html(doc["body"], doc["id"], routes, route)
        references = set(doc["meta"].get("related", []) if isinstance(doc["meta"].get("related", []), list) else [])
        references.update(match.group(1).split("|", 1)[0].strip() for match in re.finditer(r"\[\[([^\]]+)\]\]", doc["body"]))
        backlink_docs = [source for source in docs if doc["id"] in set(source["meta"].get("related", []) if isinstance(source["meta"].get("related", []), list) else []) or doc["id"] in {match.group(1).split("|", 1)[0].strip() for match in re.finditer(r"\[\[([^\]]+)\]\]", source["body"])}]
        backlinks = ""
        if backlink_docs:
            links = "".join(f'<li><a href="{relative_link(route, source["route"])}">{html.escape(str(source["title"]))}</a></li>' for source in backlink_docs)
            backlinks = f'<section class="backlinks" aria-label="Liên kết từ các trang khác"><h2>LIÊN KẾT TỪ CÁC TRANG KHÁC</h2><ul>{links}</ul></section>'
        toc = "".join(f'<li class="toc-item"><a class="toc-link" href="#{m.group(1)}">{html.escape(m.group(2))}</a></li>' for m in re.finditer(r'<h[23] id="([^"]+)">(.+?)</h[23]>', rendered))
        title = html.escape(str(doc["title"]))
        return f'''<!DOCTYPE html>
<html lang="vi" data-theme="light"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} — IT007 UIT</title><link rel="stylesheet" href="{prefix}assets/css/style.css"><script src="{prefix}assets/vendor/mathjax/es5/tex-mml-chtml.js"></script></head>
<body><header class="app-header"><a class="brand-container" href="{prefix}index.html"><span class="brand-badge">IT007</span><span class="brand-title">Hệ Điều Hành · IT007 UIT</span></a><div class="header-actions"><button class="search-trigger-btn" id="search-trigger-btn">🔍 Tìm kiếm nhanh... <kbd class="kbd-shortcut">Ctrl+K</kbd></button><button class="theme-toggle-btn" id="theme-toggle-btn"><span id="theme-icon">🌙</span></button></div></header>
<div class="workspace-layout"><aside class="sidebar-left">{nav(route)}</aside><main class="content-center"><div class="breadcrumbs"><a href="{prefix}index.html">Trang chủ</a> <span>/</span> <span>{title}</span></div><article class="article-body">{rendered}{backlinks}<div class="article-footer">Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.</div></article></main><aside class="sidebar-right"><div class="graph-container"><div class="graph-header">Đồ Thị Tri Thức</div><canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas></div><div class="toc-container"><div class="toc-title">MỤC LỤC TRANG</div><ul class="toc-list">{toc or '<li class="toc-item">Trang không có tiểu mục</li>'}</ul></div></aside></div>
<div class="search-modal-overlay" id="search-modal-overlay"><div class="search-modal"><div class="search-input-wrapper">🔍<input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm..."><kbd class="kbd-shortcut">ESC</kbd></div><ul class="search-results-list" id="search-results-list"></ul></div></div><script src="{prefix}assets/js/app.js"></script></body></html>'''

    for doc in docs:
        target = output_dir / doc["route"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(doc), encoding="utf-8")

    cards = []
    for doc in docs:
        if "theory" in doc["rel"]:
            cards.append(f'<a href="{doc["route"]}"><h3>{html.escape(doc["title"])}</h3><p>{html.escape(str(doc["summary"]))}</p></a>')
    index = f'''<!DOCTYPE html><html lang="vi" data-theme="light"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>IT007 · Hệ Điều Hành UIT</title><link rel="stylesheet" href="assets/css/style.css"><script src="assets/vendor/mathjax/es5/tex-mml-chtml.js"></script></head><body><header class="app-header"><a class="brand-container" href="index.html"><span class="brand-badge">IT007</span><span class="brand-title">Hệ Điều Hành · IT007 UIT</span></a><div class="header-actions"><button class="search-trigger-btn" id="search-trigger-btn">Tìm kiếm <kbd class="kbd-shortcut">Ctrl+K</kbd></button><button class="theme-toggle-btn" id="theme-toggle-btn"><span id="theme-icon">🌙</span></button></div></header><div class="workspace-layout"><aside class="sidebar-left">{nav("index.html")}</aside><main class="content-center"><article class="article-body"><h1>Hệ Điều Hành</h1><p>IT007 · Lý thuyết · Tự luận · Bài tập · Thực hành · Ôn tập · Đề thi</p><div class="article-meta-bar">Biên soạn: <strong>Võ Trọng Phúc</strong></div><h2>Các Chuyên Đề Cốt Lõi</h2><div class="document-grid">{"".join(cards)}</div><div class="article-footer">Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.</div></article></main><aside class="sidebar-right"><div class="graph-container"><div class="graph-header">Đồ Thị Tri Thức</div><canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas></div></aside></div><div class="search-modal-overlay" id="search-modal-overlay"><div class="search-modal"><div class="search-input-wrapper"><input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm..."><kbd class="kbd-shortcut">ESC</kbd></div><ul class="search-results-list" id="search-results-list"></ul></div></div><script src="assets/js/app.js"></script></body></html>'''
    (output_dir / "index.html").write_text(index, encoding="utf-8")
    print(f"Successfully compiled {len(docs) + 1} static pages into {output_dir}.")
    return docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-root", default=str(DEFAULT_CONTENT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    build_site(args.content_root, args.output_dir)

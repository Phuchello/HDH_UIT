#!/usr/bin/env python3
"""
scripts/build_web.py
Deterministic Quartz-Architecture SSOT Static Web Compiler for HDH_UIT V2.
Compiles all canonical Markdown from content/ into public/site/.
Generates dynamic full-text search, semantic knowledge graph, breadcrumbs, TOC, and backlinks.
"""

import os
import sys
import re
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_DIR = ROOT / "public" / "site"
ARCHIVE_ASSETS = ROOT / "archive" / "web-prototype-v2" / "assets"
SHARED_VENDOR = ROOT / "src" / "shared" / "vendor"

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
            if v == "null":
                v = None
            elif v == "true":
                v = True
            elif v == "false":
                v = False
            meta[k] = v
    return meta, body

def markdown_to_html(md_text, doc_id=""):
    # Convert headings with IDs
    def heading_repl(m):
        level = len(m.group(1))
        title = m.group(2).strip()
        slug = re.sub(r'[^a-zA-Z0-9\-_]', '', title.lower().replace(' ', '-'))
        return f'<h{level} id="{slug}">{title}</h{level}>'
    
    html = re.sub(r'^(#{1,6})\s+(.+)$', heading_repl, md_text, flags=re.MULTILINE)
    
    # Convert Callouts
    def callout_repl(m):
        ctype = m.group(1).lower()
        content = m.group(2).strip()
        
        # Check for studycard
        if ctype == "studycard":
            cid_match = re.search(r'id=["\']([^"\']+)["\']', m.group(0))
            cid = cid_match.group(1) if cid_match else f"card-{doc_id}"
            
            # Split sections
            hint = ""
            keypoints = ""
            answer = ""
            
            if "<!-- hint -->" in content:
                parts = content.split("<!-- hint -->", 1)
                q_text = parts[0].strip()
                rest = parts[1]
                if "<!-- keypoints -->" in rest:
                    h_parts = rest.split("<!-- keypoints -->", 1)
                    hint = h_parts[0].strip()
                    rest2 = h_parts[1]
                    if "<!-- answer -->" in rest2:
                        k_parts = rest2.split("<!-- answer -->", 1)
                        keypoints = k_parts[0].strip()
                        answer = k_parts[1].strip()
                    else:
                        keypoints = rest2.strip()
                elif "<!-- answer -->" in rest:
                    h_parts = rest.split("<!-- answer -->", 1)
                    hint = h_parts[0].strip()
                    answer = h_parts[1].strip()
                else:
                    hint = rest.strip()
            elif "<!-- keypoints -->" in content:
                parts = content.split("<!-- keypoints -->", 1)
                q_text = parts[0].strip()
                rest = parts[1]
                if "<!-- answer -->" in rest:
                    k_parts = rest.split("<!-- answer -->", 1)
                    keypoints = k_parts[0].strip()
                    answer = k_parts[1].strip()
                else:
                    keypoints = rest.strip()
            elif "<!-- answer -->" in content:
                parts = content.split("<!-- answer -->", 1)
                q_text = parts[0].strip()
                answer = parts[1].strip()
            else:
                q_text = content
                
            q_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', q_text)
            hint_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', hint) if hint else ""
            ans_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', answer) if answer else ""
            
            card_html = f'''
<div class="study-card" data-card-id="{cid}">
  <div class="card-header">
    <span class="card-tag">Active Recall</span>
    <span class="card-stats">Tự học tương tác</span>
  </div>
  <div class="card-question">{q_html}</div>
'''
            if hint:
                card_html += f'<div class="card-section card-hint"><strong>💡 Gợi ý:</strong> {hint_html}</div>\n'
            if keypoints:
                kp_items = ""
                for line in keypoints.splitlines():
                    if line.strip().startswith("- [ ]") or line.strip().startswith("-"):
                        item_txt = line.replace("- [ ]", "").replace("-", "").strip()
                        kp_items += f'<li>{item_txt}</li>'
                card_html += f'<div class="card-section card-keypoints"><strong>🔑 Từ khóa bắt buộc:</strong><ul>{kp_items}</ul></div>\n'
            if answer:
                card_html += f'<div class="card-section card-answer"><strong>📖 Lời giải hoàn chỉnh:</strong><p>{ans_html}</p></div>\n'
                
            card_html += '''
  <div class="card-actions">
'''
            if hint:
                card_html += '    <button class="btn-card btn-hint">💡 Gợi ý</button>\n'
            if keypoints:
                card_html += '    <button class="btn-card btn-keypoints">🔑 Xem Từ Khóa</button>\n'
            if answer:
                card_html += '    <button class="btn-card primary btn-answer">📖 Hiện Lời Giải</button>\n'
            card_html += '''    <button class="btn-card success btn-remember">✅ Đã Thuộc</button>
    <button class="btn-card danger btn-forgot">❌ Chưa Nhớ</button>
  </div>
</div>
'''
            return card_html

        # Check for SubjectivePractice
        if ctype == "subjectivepractice":
            pid_match = re.search(r'id=["\']([^"\']+)["\']', m.group(0))
            pid = pid_match.group(1) if pid_match else f"prac-{doc_id}"
            max_score_match = re.search(r'max_score=([0-9\.]+)', m.group(0))
            max_score = max_score_match.group(1) if max_score_match else "1.0"
            
            prompt_text = content
            rubric_text = ""
            if "<!-- rubric" in content:
                parts = content.split("<!-- rubric", 1)
                prompt_text = parts[0].strip()
                r_rest = parts[1]
                if "-->" in r_rest:
                    rubric_text = r_rest.split("-->", 1)[1].strip()
                    
            prompt_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', prompt_text)
            
            rubric_items = ""
            for line in rubric_text.splitlines():
                if line.strip().startswith("-"):
                    line_clean = line.strip().lstrip("-").strip()
                    weight_match = re.search(r'\[([0-9\.]+)\s*điểm\]', line_clean)
                    weight = weight_match.group(1) if weight_match else "0.5"
                    item_desc = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line_clean)
                    rubric_items += f'''
<div class="rubric-item">
  <input type="checkbox" class="rubric-check" data-weight="{weight}">
  <div>{item_desc}</div>
</div>'''
            
            prac_html = f'''
<div class="subjective-practice" data-practice-id="{pid}" data-max-score="{max_score}">
  <div class="practice-header">
    <h3>Luyện Tập Viết Tự Luận</h3>
    <span class="card-tag">Tự đánh giá</span>
  </div>
  <div style="font-size: 0.92rem; margin-bottom: 0.75rem;">{prompt_html}</div>
  <textarea class="practice-textarea" placeholder="Nhập câu trả lời tự luận của bạn vào đây trước khi nhấn xem barem điểm..."></textarea>
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
    <button class="btn-card primary btn-compare">So Sánh Với Barem Điểm</button>
    <span style="font-size: 0.82rem; color: var(--text-muted);">Gợi ý tự chấm hỗ trợ tự học</span>
  </div>
  <div class="rubric-container">
    <h4 style="margin-bottom: 0.75rem;">📋 Rubric Tự Kiểm Tra Gợi Ý (Self-Check Rubric):</h4>
    {rubric_items}
    <div class="rubric-score-box">
      <span>Điểm số tự đánh giá:</span>
      <span style="font-size: 1.1rem; color: var(--accent-text);"><span class="current-score">0.00</span> / {max_score} điểm</span>
    </div>
  </div>
</div>
'''
            return prac_html

        c_class = "callout " + ctype
        c_title = ctype.upper()
        if ctype == "characteristics":
            c_title = "ĐẶC TÍNH KỸ THUẬT"
        elif ctype == "note":
            c_title = "LƯU Ý QUAN TRỌNG"
        elif ctype == "important":
            c_title = "YÊU CẦU QUAN TRỌNG"
        elif ctype == "warning":
            c_title = "CẢNH BÁO KỸ THUẬT"
        elif ctype == "tip":
            c_title = "KHUYẾN NGHỊ THỰC HÀNH"
            
        c_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        c_body = c_body.replace('\n', '<br>')
        return f'<div class="{c_class}"><div class="callout-title">{c_title}</div><p>{c_body}</p></div>'

    html = re.sub(r'^>\s+\[!([A-Z_]+)\](?:[^\n]*)\n((?:>\s+[^\n]*\n?)+)', 
                  lambda m: callout_repl(re.match(r'>\s+\[!([A-Za-z0-9_]+)\](?:[^\n]*)\n([\s\S]+)', m.group(0))), 
                  html, flags=re.MULTILINE)
    
    # Process simple blockquotes
    def bq_repl(m):
        body = m.group(1).replace('> ', '').replace('>', '')
        return f'<blockquote>{body}</blockquote>'
    html = re.sub(r'((?:^>[^\n]*\n?)+)', bq_repl, html, flags=re.MULTILINE)

    # Process Code Blocks
    def code_repl(m):
        lang = m.group(1) or ""
        code = m.group(2).replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="language-{lang}">{code}</code></pre>'
    html = re.sub(r'```([a-zA-Z0-9_]*)\n([\s\S]*?)```', code_repl, html)

    # Inline Code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Tables
    lines = html.splitlines()
    in_table = False
    table_lines = []
    out_lines = []
    
    for l in lines:
        if l.strip().startswith('|') and l.strip().endswith('|'):
            in_table = True
            table_lines.append(l.strip())
        else:
            if in_table:
                # Render table
                out_lines.append(render_markdown_table(table_lines))
                table_lines = []
                in_table = False
            out_lines.append(l)
    if in_table:
        out_lines.append(render_markdown_table(table_lines))
        
    html = '\n'.join(out_lines)

    # Wikilinks [[slug]]
    def wikilink_repl(m):
        target = m.group(1).strip()
        label = target
        if "|" in target:
            target, label = target.split("|", 1)
        return f'<a class="wikilink" href="#{target}">{label}</a>'
    html = re.sub(r'\[\[([^\]]+)\]\]', wikilink_repl, html)

    # Paragraphs
    paragraphs = html.split('\n\n')
    rendered_p = []
    for p in paragraphs:
        p_str = p.strip()
        if not p_str:
            continue
        if any(p_str.startswith(tag) for tag in ['<h', '<div', '<pre', '<table', '<blockquote', '<ul', '<ol']):
            rendered_p.append(p_str)
        else:
            p_formatted = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p_str)
            p_formatted = re.sub(r'\*(.+?)\*', r'<em>\1</em>', p_formatted)
            rendered_p.append(f'<p>{p_formatted}</p>')
            
    return '\n\n'.join(rendered_p)

def render_markdown_table(lines):
    if len(lines) < 2:
        return '\n'.join(lines)
    header_cols = [c.strip() for c in lines[0].strip('|').split('|')]
    th_html = ''.join(f'<th>{c}</th>' for c in header_cols)
    
    rows_html = []
    for row in lines[2:]:
        cols = [c.strip() for c in row.strip('|').split('|')]
        td_html = ''.join(f'<td>{c}</td>' for c in cols)
        rows_html.append(f'<tr>{td_html}</tr>')
        
    return f'''<table>
  <thead><tr>{th_html}</tr></thead>
  <tbody>{''.join(rows_html)}</tbody>
</table>'''

def build_site():
    print(">>> Starting Deterministic Quartz SSOT Web Build...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Copy Assets & Vendor math
    assets_dest = OUTPUT_DIR / "assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    if ARCHIVE_ASSETS.exists():
        for item in ARCHIVE_ASSETS.iterdir():
            target = assets_dest / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)
                
    # Copy shared vendor mathjax into assets/vendor
    vendor_dest = assets_dest / "vendor"
    vendor_dest.mkdir(parents=True, exist_ok=True)
    if SHARED_VENDOR.exists():
        shutil.copytree(SHARED_VENDOR, vendor_dest, dirs_exist_ok=True)
        
    # 2. Discover all published canonical markdown files
    docs = []
    for md_path in CONTENT_DIR.glob("**/*.md"):
        rel_path = md_path.relative_to(CONTENT_DIR)
        txt = md_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(txt)
        
        doc_id = meta.get("id", str(rel_path.with_suffix("")).replace("\\", "/"))
        title = meta.get("title", doc_id)
        slug = meta.get("slug", rel_path.stem)
        summary = meta.get("summary", "")
        
        docs.append({
            "path": md_path,
            "rel_path": rel_path,
            "id": doc_id,
            "title": title,
            "slug": slug,
            "summary": summary,
            "meta": meta,
            "body": body,
            "out_html_rel": str(rel_path.with_suffix(".html")).replace("\\", "/")
        })
        
    print(f"Discovered {len(docs)} canonical content documents.")
    
    # 3. Build Dynamic Search Index
    search_index = []
    for d in docs:
        search_index.append({
            "id": d["id"],
            "title": d["title"],
            "url": d["out_html_rel"],
            "snippet": d["summary"] or d["title"]
        })
    (OUTPUT_DIR / "search_index.json").write_text(json.dumps(search_index, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # 4. Build Dynamic Semantic Knowledge Graph
    nodes = []
    edges = []
    node_coords = [
        (140, 90), (80, 40), (60, 140), (200, 50), (220, 130), (140, 160), (280, 90)
    ]
    for idx, d in enumerate(docs):
        coord = node_coords[idx % len(node_coords)]
        nodes.append({
            "id": d["id"],
            "label": d["title"].split(":")[0] if ":" in d["title"] else d["title"][:20],
            "x": coord[0] + (idx * 15) % 80,
            "y": coord[1] + (idx * 20) % 60,
            "r": 7,
            "color": "#0969da" if "theory" in d["id"] else ("#0e7490" if "lab" in d["id"] else "#9a6700"),
            "link": d["out_html_rel"]
        })
        
        # Connect related
        for rel in d["meta"].get("related", []):
            edges.append({"from": d["id"], "to": rel})
            
    graph_data = {"nodes": nodes, "edges": edges}
    (OUTPUT_DIR / "graph_data.json").write_text(json.dumps(graph_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # 5. Build Dynamic Navigation Tree
    def build_nav_html(current_rel):
        nav_html = '<div class="nav-section-title">LÝ THUYẾT (THEORY)</div>\n<ul class="nav-tree">\n'
        for d in docs:
            if "theory" in str(d["rel_path"]):
                active_cls = ' active' if d["out_html_rel"] == current_rel else ''
                # calculate relative link
                rel_link = get_relative_link(current_rel, d["out_html_rel"])
                nav_html += f'  <li class="nav-tree-item"><a class="nav-link{active_cls}" href="{rel_link}">{d["title"]}</a></li>\n'
        nav_html += '</ul>\n'
        
        nav_html += '<div class="nav-section-title">NGÂN HÀNG CÂU HỎI</div>\n<ul class="nav-tree">\n'
        for d in docs:
            if "questions" in str(d["rel_path"]):
                active_cls = ' active' if d["out_html_rel"] == current_rel else ''
                rel_link = get_relative_link(current_rel, d["out_html_rel"])
                nav_html += f'  <li class="nav-tree-item"><a class="nav-link{active_cls}" href="{rel_link}">{d["title"]}</a></li>\n'
        nav_html += '</ul>\n'
        
        nav_html += '<div class="nav-section-title">THỰC HÀNH (LAB)</div>\n<ul class="nav-tree">\n'
        for d in docs:
            if "labs" in str(d["rel_path"]):
                active_cls = ' active' if d["out_html_rel"] == current_rel else ''
                rel_link = get_relative_link(current_rel, d["out_html_rel"])
                nav_html += f'  <li class="nav-tree-item"><a class="nav-link{active_cls}" href="{rel_link}">{d["title"]}</a></li>\n'
        nav_html += '</ul>\n'
        
        nav_html += '<div class="nav-section-title">ĐỀ THI & TRA CỨU</div>\n<ul class="nav-tree">\n'
        for d in docs:
            if "exams" in str(d["rel_path"]) or "glossary" in str(d["rel_path"]) or "flashcards" in str(d["rel_path"]):
                active_cls = ' active' if d["out_html_rel"] == current_rel else ''
                rel_link = get_relative_link(current_rel, d["out_html_rel"])
                nav_html += f'  <li class="nav-tree-item"><a class="nav-link{active_cls}" href="{rel_link}">{d["title"]}</a></li>\n'
        nav_html += '</ul>\n'
        return nav_html

    # Helper for relative paths
    def get_relative_link(from_path, to_path):
        from_dir = os.path.dirname(from_path)
        if not from_dir:
            return to_path
        depth = len(from_dir.split("/"))
        prefix = "../" * depth
        return prefix + to_path

    # 6. Render every page from canonical markdown
    for d in docs:
        out_file = OUTPUT_DIR / d["out_html_rel"]
        out_file.parent.mkdir(parents=True, exist_ok=True)
        
        rendered_body = markdown_to_html(d["body"], d["id"])
        nav_html = build_nav_html(d["out_html_rel"])
        
        # Calculate root relative prefix
        depth = len(d["out_html_rel"].split("/")) - 1
        root_prefix = "../" * depth if depth > 0 else ""
        
        # Extract headings for TOC
        toc_items = ""
        for h in re.finditer(r'<h([23]) id="([^"]+)">([^<]+)</h[23]>', rendered_body):
            h_id = h.group(2)
            h_title = h.group(3)
            toc_items += f'<li class="toc-item"><a class="toc-link" href="#{h_id}">{h_title}</a></li>\n'
            
        page_html = f'''<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{d["title"]} — IT007 UIT</title>
  <link rel="stylesheet" href="{root_prefix}assets/css/style.css">
  <script src="{root_prefix}assets/vendor/mathjax/es5/tex-mml-chtml.js"></script>
</head>
<body>

  <!-- Top App Header -->
  <header class="app-header">
    <a class="brand-container" href="{root_prefix}index.html">
      <span class="brand-badge">IT007</span>
      <span class="brand-title">Hệ Điều Hành · IT007 UIT</span>
    </a>
    <div class="header-actions">
      <button class="search-trigger-btn" id="search-trigger-btn">
        <span>🔍 Tìm kiếm nhanh...</span>
        <kbd class="kbd-shortcut">Ctrl+K</kbd>
      </button>
      <button class="theme-toggle-btn" id="theme-toggle-btn" title="Chuyển đổi giao diện Sáng / Tối">
        <span id="theme-icon">🌙</span>
      </button>
    </div>
  </header>

  <!-- 3-Column Workspace Layout -->
  <div class="workspace-layout">

    <!-- Left Sidebar (Explorer) -->
    <aside class="sidebar-left">
      {nav_html}
    </aside>

    <!-- Center Column (Reading Canvas) -->
    <main class="content-center">
      <div class="breadcrumbs">
        <a href="{root_prefix}index.html">Trang chủ</a> <span>/</span> <span>{d["title"]}</span>
      </div>

      <article class="article-body">
        {rendered_body}
        
        <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); font-size: 0.82rem; color: var(--text-muted); text-align: center;">
          Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.
        </div>
      </article>
    </main>

    <!-- Right Sidebar (Local Graph & TOC) -->
    <aside class="sidebar-right">
      <div class="graph-container">
        <div class="graph-header">🌐 Đồ Thị Tri Thức Cục Bộ</div>
        <canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas>
      </div>

      <div class="toc-container">
        <div class="toc-title">MỤC LỤC TRANG</div>
        <ul class="toc-list">
          {toc_items or '<li class="toc-item"><span style="color: var(--text-muted);">Trang không có tiểu mục</span></li>'}
        </ul>
      </div>
    </aside>

  </div>

  <!-- Full-Text Search Modal -->
  <div class="search-modal-overlay" id="search-modal-overlay">
    <div class="search-modal">
      <div class="search-input-wrapper">
        <span>🔍</span>
        <input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm khái niệm, câu hỏi, bài lab...">
        <kbd class="kbd-shortcut">ESC</kbd>
      </div>
      <ul class="search-results-list" id="search-results-list"></ul>
    </div>
  </div>

  <script src="{root_prefix}assets/js/app.js"></script>
</body>
</html>
'''
        out_file.write_text(page_html, encoding="utf-8")

    # 7. Generate index.html at root of site
    index_html = f'''<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IT007 · Hệ Điều Hành UIT</title>
  <link rel="stylesheet" href="assets/css/style.css">
  <script src="assets/vendor/mathjax/es5/tex-mml-chtml.js"></script>
</head>
<body>

  <header class="app-header">
    <a class="brand-container" href="index.html">
      <span class="brand-badge">IT007</span>
      <span class="brand-title">Hệ Điều Hành · IT007 UIT</span>
    </a>
    <div class="header-actions">
      <button class="search-trigger-btn" id="search-trigger-btn">
        <span>🔍 Tìm kiếm nhanh...</span>
        <kbd class="kbd-shortcut">Ctrl+K</kbd>
      </button>
      <button class="theme-toggle-btn" id="theme-toggle-btn" title="Chuyển đổi giao diện Sáng / Tối">
        <span id="theme-icon">🌙</span>
      </button>
    </div>
  </header>

  <div class="workspace-layout">
    <aside class="sidebar-left">
      {build_nav_html("index.html")}
    </aside>

    <main class="content-center">
      <article class="article-body">
        <h1>Hệ Điều Hành (IT007)</h1>
        <p style="font-size: 1.1rem; color: var(--text-secondary);">Lý thuyết · Tự luận · Bài tập · Thực hành · Đề thi</p>
        
        <div class="article-meta-bar">
          <span class="meta-item">Biên soạn: <strong>Võ Trọng Phúc</strong></span>
          <span class="meta-item">Đối chuẩn: <strong>Khoa Kỹ thuật Máy tính · UIT</strong></span>
        </div>

        <p>
          Chào mừng bạn đến với tài liệu học tập và tra cứu môn <strong>Hệ điều hành (IT007)</strong>. Mọi nội dung được biên soạn từ các nguồn tài liệu giảng dạy chính thức, tiêu chuẩn quốc tế POSIX/Linux và ngân hàng đề thi lưu trữ.
        </p>

        <h2>Các Chuyên Đề Cốt Lõi</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
          <a href="theory/ch01-overview.html" style="display: block; padding: 1.2rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 8px; text-decoration: none; color: inherit;">
            <h3 style="margin-top: 0; color: var(--accent-text);">📖 Lý Thuyết Chương 1</h3>
            <p style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 0;">Tổng quan HDH, cơ chế ngắt, phân cấp lưu trữ và Dual-Mode.</p>
          </a>
          <a href="questions/subjective/ch01.html" style="display: block; padding: 1.2rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 8px; text-decoration: none; color: inherit;">
            <h3 style="margin-top: 0; color: var(--accent-text);">✍️ Ngân Hàng Tự Luận</h3>
            <p style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 0;">Luyện viết tự luận có rubric tự kiểm tra gợi ý.</p>
          </a>
        </div>

        <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); font-size: 0.82rem; color: var(--text-muted); text-align: center;">
          Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.
        </div>
      </article>
    </main>

    <aside class="sidebar-right">
      <div class="graph-container">
        <div class="graph-header">🌐 Đồ Thị Tri Thức Cục Bộ</div>
        <canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas>
      </div>
    </aside>
  </div>

  <div class="search-modal-overlay" id="search-modal-overlay">
    <div class="search-modal">
      <div class="search-input-wrapper">
        <span>🔍</span>
        <input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm...">
        <kbd class="kbd-shortcut">ESC</kbd>
      </div>
      <ul class="search-results-list" id="search-results-list"></ul>
    </div>
  </div>

  <script src="assets/js/app.js"></script>
</body>
</html>
'''
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Successfully compiled {len(docs) + 1} static pages into public/site/.")

if __name__ == "__main__":
    build_site()

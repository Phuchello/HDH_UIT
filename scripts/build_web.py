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

    def mdlink(match):
        label = match.group(1)
        target = match.group(2).strip()
        href = target
        fragment = ""
        clean_target = target
        if "#" in target:
            clean_target, fragment = target.split("#", 1)
            fragment = "#" + fragment

        if not target.startswith(("http://", "https://", "mailto:", "#")):
            base_dir = Path(current_rel).parent.as_posix() or "."
            stem_or_id = clean_target
            if stem_or_id.endswith(".md") or stem_or_id.endswith(".html"):
                stem_or_id = os.path.splitext(stem_or_id)[0]

            norm_path = os.path.normpath(os.path.join(base_dir, stem_or_id)).replace("\\", "/")
            while norm_path.startswith("../"):
                norm_path = norm_path[3:]

            candidate_id = None
            if stem_or_id in routes:
                candidate_id = stem_or_id
            elif norm_path in routes:
                candidate_id = norm_path
            elif Path(stem_or_id).stem in routes:
                candidate_id = Path(stem_or_id).stem

            if candidate_id and candidate_id in routes:
                dest_route = routes[candidate_id]
                href = os.path.relpath(dest_route, base_dir).replace("\\", "/") + fragment
            elif clean_target.endswith(".md"):
                href = clean_target[:-3] + ".html" + fragment
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", mdlink, text)
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


def _parse_studycard_sections(body: str, card_id: str = "", source_path: str = "") -> tuple[str, str, str, str]:
    """Deterministic single-pass StudyCard section parser with marker validation.

    ENG-LEARN-003 FIX: The old loop mutated ``question`` after each split,
    causing later markers that appeared after <!-- hint --> to be lost.
    This parser validates marker counts and ordering, splits in a single pass,
    and ensures no markers leak into the parsed fields.
    """
    MARKERS = ("<!-- hint -->", "<!-- keypoints -->", "<!-- answer -->")

    # Marker validation: at most 1 occurrence per marker
    for m in MARKERS:
        count = body.count(m)
        if count > 1:
            raise RuntimeError(
                f"StudyCard marker validation failure in {source_path} [id={card_id}]: "
                f"Marker '{m}' appeared {count} times (maximum 1 allowed)."
            )

    # Marker validation: ordering question -> hint? -> keypoints? -> answer?
    hint_pos = body.find("<!-- hint -->")
    kp_pos = body.find("<!-- keypoints -->")
    ans_pos = body.find("<!-- answer -->")

    if hint_pos != -1 and kp_pos != -1 and hint_pos > kp_pos:
        raise RuntimeError(
            f"StudyCard marker validation failure in {source_path} [id={card_id}]: "
            f"'<!-- hint -->' appeared after '<!-- keypoints -->'."
        )
    if hint_pos != -1 and ans_pos != -1 and hint_pos > ans_pos:
        raise RuntimeError(
            f"StudyCard marker validation failure in {source_path} [id={card_id}]: "
            f"'<!-- hint -->' appeared after '<!-- answer -->'."
        )
    if kp_pos != -1 and ans_pos != -1 and kp_pos > ans_pos:
        raise RuntimeError(
            f"StudyCard marker validation failure in {source_path} [id={card_id}]: "
            f"'<!-- keypoints -->' appeared after '<!-- answer -->'."
        )

    pattern = "(" + "|".join(re.escape(m) for m in MARKERS) + ")"
    parts = re.split(pattern, body)
    question = parts[0]
    hint = keypoints = answer = ""
    i = 1
    while i < len(parts) - 1:
        marker = parts[i]
        chunk = parts[i + 1]
        if marker == "<!-- hint -->":
            hint = chunk
        elif marker == "<!-- keypoints -->":
            keypoints = chunk
        elif marker == "<!-- answer -->":
            answer = chunk
        i += 2

    # Validation: no markers leak into rendered chunks
    for field_name, val in (("question", question), ("hint", hint), ("keypoints", keypoints), ("answer", answer)):
        for m in MARKERS:
            if m in val:
                raise RuntimeError(
                    f"StudyCard marker leak in {source_path} [id={card_id}]: "
                    f"Marker '{m}' leaked into field '{field_name}'."
                )

    return question, hint, keypoints, answer


ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def render_callout(kind, body, doc_id, routes, current_rel):
    lower = kind.lower()
    if lower in {"studycard", "subjectivepractice", "recallcheckpoint", "transferproblem"}:
        id_match = re.search(r'\bid=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', body)
        if not id_match:
            snippet = body.strip().splitlines()[0][:80] if body.strip() else "(empty block)"
            raise RuntimeError(
                f"ID-LEARN-001 BUILD ERROR: Missing explicit 'id=' in {kind} callout in {current_rel} (doc_id={doc_id}). "
                f"Context: {snippet!r}. Persistent interactive primitives must have an explicit persistent id."
            )
        raw_id = (id_match.group(1) if id_match.group(1) is not None else (id_match.group(2) if id_match.group(2) is not None else id_match.group(3))).strip()
        if not raw_id:
            snippet = body.strip().splitlines()[0][:80] if body.strip() else "(empty block)"
            raise RuntimeError(
                f"ID-LEARN-001 BUILD ERROR: Missing explicit 'id=' in {kind} callout in {current_rel} (doc_id={doc_id}). "
                f"Context: {snippet!r}. Persistent interactive primitives must have an explicit persistent id."
            )
        if not ID_PATTERN.match(raw_id):
            raise RuntimeError(
                f"ID-LEARN-001 BUILD ERROR: Invalid 'id=' format {raw_id!r} in {kind} callout in {current_rel} (doc_id={doc_id}). "
                f"IDs must match ^[A-Za-z0-9][A-Za-z0-9_-]*$."
            )

        item_id = raw_id
        concept_match = re.search(r'concept(?:_id)?=["\']([^"\']+)', body)
        concept_id = concept_match.group(1) if concept_match else item_id
        body = re.sub(r'^\s*id=(?:"[^"]*"|\'[^\']*\'|[^\s>]+)[ \t]*\n?', "", body, count=1)
        body = re.sub(r'^\s*concept(?:_id)?=["\'][^"\']+["\'][ \t]*\n?', "", body, count=1)

        eid = html.escape(item_id)
        cid = html.escape(concept_id)

        # ------------------------------------------------------------------
        # StudyCard V2 (A11Y-LEARN-001, STATE-LEARN-001, PED-LEARN-004)
        # ------------------------------------------------------------------
        if lower == "studycard":
            question, hint, keypoints, answer = _parse_studycard_sections(body, eid, current_rel)
            hint_id = f"{eid}__hint"
            kp_id = f"{eid}__keypoints"
            ans_id = f"{eid}__answer"
            scratchpad_id = f"{eid}__scratchpad"
            feedback_id = f"{eid}__feedback"
            rating_actions_id = f"{eid}__rating_actions"

            parts = [
                f'<div class="study-card" id="{eid}" data-card-id="{eid}" data-concept-id="{cid}"'
                f' data-mastery="M0" role="region" aria-label="Thẻ học tập: {eid}">',
                f'<div class="card-header">',
                f'<span class="card-tag">Active Recall</span>',
                f'<span class="card-mastery-badge" aria-label="Cấp độ thành thạo">M0</span>',
                f'</div>',
                f'<div class="card-question">{inline(question.strip(), routes, current_rel)}</div>',
                f'<textarea id="{scratchpad_id}" class="card-scratchpad"'
                f' aria-label="Nháp câu trả lời của bạn"'
                f' placeholder="Viết câu trả lời của bạn vào đây trước khi xem gợi ý…"></textarea>',
            ]

            # Section elements with stable IDs matching button aria-controls
            reveal_btns = []
            if hint:
                parts.append(
                    f'<div id="{hint_id}" class="card-section card-hint" aria-hidden="true">'
                    f'<strong>💡 Gợi ý:</strong> {inline(hint.strip(), routes, current_rel)}'
                    f'</div>'
                )
                reveal_btns.append(
                    f'<button type="button" class="btn-card btn-hint" aria-expanded="false"'
                    f' aria-controls="{hint_id}">💡 Xem Gợi ý</button>'
                )
            if keypoints:
                kp_items = [
                    f"<li>{inline(line.lstrip('- ').strip(), routes, current_rel)}</li>"
                    for line in keypoints.splitlines()
                    if line.strip().startswith("-")
                ]
                parts.append(
                    f'<div id="{kp_id}" class="card-section card-keypoints" aria-hidden="true">'
                    f'<strong>🔑 Từ khóa bắt buộc:</strong><ul>'
                    + "".join(kp_items)
                    + '</ul></div>'
                )
                reveal_btns.append(
                    f'<button type="button" class="btn-card btn-keypoints" aria-expanded="false"'
                    f' aria-controls="{kp_id}">🔑 Xem Từ khóa</button>'
                )
            if answer:
                parts.append(
                    f'<div id="{ans_id}" class="card-section card-answer" aria-hidden="true">'
                    f'<strong>📖 Lời giải hoàn chỉnh:</strong>'
                    f'<div class="card-answer-body">{inline(answer.strip(), routes, current_rel)}</div>'
                    f'</div>'
                )
                reveal_btns.append(
                    f'<button type="button" class="btn-card btn-answer" aria-expanded="false"'
                    f' aria-controls="{ans_id}">📖 Xem Lời giải</button>'
                )

            if reveal_btns:
                parts.append(
                    '<div class="card-reveal-actions">'
                    + "".join(reveal_btns)
                    + '</div>'
                )

            # PED-LEARN-004: Rating controls hidden until feedback is revealed
            parts.append(
                f'<div class="card-feedback-status" id="{feedback_id}" aria-live="polite"></div>'
                f'<div class="card-actions card-rating-actions" id="{rating_actions_id}" style="display: none;" aria-hidden="true">'
                f'<span class="card-actions-label">Đánh giá lượt ôn:</span>'
                f'<button type="button" class="btn-card btn-rating btn-again" data-rating="AGAIN"'
                f' aria-label="Đánh giá: Quên hoàn toàn">🔴 Quên</button>'
                f'<button type="button" class="btn-card btn-rating btn-hard" data-rating="HARD"'
                f' aria-label="Đánh giá: Nhớ nhưng khó">🟠 Khó</button>'
                f'<button type="button" class="btn-card btn-rating btn-good" data-rating="GOOD"'
                f' aria-label="Đánh giá: Nhớ chuẩn mực">🟢 Ổn</button>'
                f'<button type="button" class="btn-card btn-rating btn-easy" data-rating="EASY"'
                f' aria-label="Đánh giá: Nhớ xuất sắc">⭐ Dễ</button>'
                f'</div>'
                f'</div>'
            )
            return "".join(parts)

        # ------------------------------------------------------------------
        # RecallCheckpoint (MASTERY-LEARN-001)
        # ------------------------------------------------------------------
        if lower == "recallcheckpoint":
            prompt, rubric = body.split("<!-- rubric", 1) if "<!-- rubric" in body else (body, "")
            rubric = rubric.split("-->", 1)[-1]
            rows = []
            for line in rubric.splitlines():
                if line.strip().startswith("-"):
                    weight = re.search(r"\[([0-9.]+)\s*điểm\]", line)
                    w = weight.group(1) if weight else "0.5"
                    clean_line = re.sub(r"^-\s*", "", line.strip())
                    clean_line = re.sub(r"\[[0-9.]+\s*điểm\]", "", clean_line).strip()
                    rows.append(
                        f'<div class="rubric-item">'
                        f'<label><input type="checkbox" class="rubric-check" data-weight="{w}"> '
                        f'{inline(clean_line, routes, current_rel)} ({w}đ)</label>'
                        f'</div>'
                    )
            rubric_id = f"{eid}__rubric"
            scratchpad_id = f"{eid}__scratchpad"
            feedback_id = f"{eid}__feedback"
            rows_html = "".join(rows) if rows else (
                '<div class="rubric-item">'
                '<label><input type="checkbox" class="rubric-check" data-weight="1.0"> '
                'Nắm vững định nghĩa và cơ chế vận hành cốt lõi (1.0đ)</label></div>'
            )
            return (
                f'<div class="recall-checkpoint" id="{eid}" data-item-id="{eid}" data-concept-id="{cid}"'
                f' role="region" aria-label="Trạm thu hồi: {cid}">'
                f'<div class="checkpoint-header">'
                f'<span class="card-tag">Recall Checkpoint</span>'
                f'<span class="card-mastery-badge" aria-label="Cấp độ thành thạo">M0</span>'
                f'<span class="checkpoint-status" aria-live="polite">Chưa tự kiểm tra</span>'
                f'</div>'
                f'<div class="checkpoint-prompt">{inline(prompt.strip(), routes, current_rel)}</div>'
                f'<textarea id="{scratchpad_id}" class="checkpoint-scratchpad"'
                f' aria-label="Nháp câu trả lời kín sách" placeholder="Tự thu hồi câu trả lời kín sách trước khi xem rubric..."></textarea>'
                f'<div class="checkpoint-actions">'
                f'<button type="button" class="btn-card primary btn-reveal-rubric" aria-expanded="false"'
                f' aria-controls="{rubric_id}">🔍 Mở Rubric Đối soát</button>'
                f'</div>'
                f'<div id="{rubric_id}" class="rubric-container card-section" aria-hidden="true" style="display: none;">'
                f'<div class="rubric-title"><strong>Tiêu chí đối soát tự đánh giá:</strong></div>'
                f'<div class="rubric-items">{rows_html}</div>'
                f'<div class="rubric-evaluation">'
                f'<button type="button" class="btn-card success btn-submit-recall">Xác nhận Tự đánh giá (Đạt M2 nếu ≥80%)</button>'
                f'<span class="recall-feedback" id="{feedback_id}" aria-live="polite"></span>'
                f'</div>'
                f'</div></div>'
            )

        # ------------------------------------------------------------------
        # TransferProblem (MASTERY-LEARN-001)
        # ------------------------------------------------------------------
        if lower == "transferproblem":
            prompt, solution = body.split("<!-- solution", 1) if "<!-- solution" in body else (body, "")
            if not solution and "<!-- rubric" in body:
                prompt, solution = body.split("<!-- rubric", 1)
            solution = solution.split("-->", 1)[-1]
            sol_id = f"{eid}__solution"
            scratchpad_id = f"{eid}__scratchpad"
            feedback_id = f"{eid}__feedback"
            sol_body = inline(solution.strip(), routes, current_rel) if solution.strip() else "Xem đáp án và tự kiểm tra mức độ độc lập chuyển giao."
            return (
                f'<div class="transfer-problem" id="{eid}" data-item-id="{eid}" data-concept-id="{cid}"'
                f' role="region" aria-label="Bài toán chuyển giao: {cid}">'
                f'<div class="problem-header">'
                f'<span class="card-tag">Transfer Problem (Level C)</span>'
                f'<span class="card-mastery-badge" aria-label="Cấp độ thành thạo">M0</span>'
                f'<span class="transfer-gate-status" aria-live="polite">Cần hoàn thành M2 trước</span>'
                f'</div>'
                f'<div class="problem-prompt">{inline(prompt.strip(), routes, current_rel)}</div>'
                f'<textarea id="{scratchpad_id}" class="transfer-scratchpad"'
                f' aria-label="Bài làm chuyển giao độc lập" placeholder="Độc lập giải quyết bài toán với tham số mới không dùng gợi ý..."></textarea>'
                f'<div class="problem-actions">'
                f'<button type="button" class="btn-card primary btn-reveal-transfer-solution" aria-expanded="false"'
                f' aria-controls="{sol_id}">📖 Xem Lời giải & Đối soát</button>'
                f'</div>'
                f'<div id="{sol_id}" class="transfer-solution-container card-section" aria-hidden="true" style="display: none;">'
                f'<div class="solution-content">{sol_body}</div>'
                f'<div class="transfer-evaluation">'
                f'<span class="eval-label">Đánh giá kết quả chuyển giao độc lập:</span>'
                f'<button type="button" class="btn-card success btn-transfer-pass" aria-label="Đạt yêu cầu chuyển giao">✅ Đạt (Độc lập giải đúng)</button>'
                f'<button type="button" class="btn-card danger btn-transfer-fail" aria-label="Chưa đạt yêu cầu chuyển giao">❌ Chưa đạt</button>'
                f'<span class="transfer-feedback" id="{feedback_id}" aria-live="polite"></span>'
                f'</div>'
                f'</div></div>'
            )

        # ------------------------------------------------------------------
        # SubjectivePractice
        # ------------------------------------------------------------------
        score = re.search(r'max_score=([0-9.]+)', body)
        prompt, rubric = body.split("<!-- rubric", 1) if "<!-- rubric" in body else (body, "")
        rubric = rubric.split("-->", 1)[-1]
        rows = []
        for line in rubric.splitlines():
            if line.strip().startswith("-"):
                weight = re.search(r"\[([0-9.]+)\s*điểm\]", line)
                w = weight.group(1) if weight else "0.5"
                rows.append(
                    f'<div class="rubric-item">'
                    f'<input type="checkbox" class="rubric-check" data-weight="{w}">'
                    f'<div>{inline(line.lstrip("- ").strip(), routes, current_rel)}</div>'
                    f'</div>'
                )
        max_score_val = score.group(1) if score else "1.0"
        rows_html = "".join(rows)
        rubric_id = f"{eid}__rubric"
        scratchpad_id = f"{eid}__scratchpad"
        feedback_id = f"{eid}__feedback"
        return (
            f'<div class="subjective-practice" id="{eid}" data-practice-id="{eid}" data-concept-id="{cid}"'
            f' data-max-score="{max_score_val}">'
            f'<div class="practice-header"><h3>Luyện Tập Viết Tự Luận</h3>'
            f'<span class="card-tag">Tự đánh giá</span>'
            f'<span class="card-mastery-badge" aria-label="Cấp độ thành thạo">M0</span></div>'
            f'<div>{inline(prompt.strip(), routes, current_rel)}</div>'
            f'<textarea id="{scratchpad_id}" class="practice-textarea" aria-label="Bài làm tự luận"></textarea>'
            f'<button type="button" class="btn-card primary btn-compare" aria-expanded="false"'
            f' aria-controls="{rubric_id}">So sánh với Rubric tự kiểm tra</button>'
            f'<div id="{rubric_id}" class="rubric-container" aria-label="Rubric tự kiểm tra" aria-hidden="true">{rows_html}'
            f'<p class="self-check-score">Tự kiểm tra: '
            f'<output class="current-score">0.00</output> / {max_score_val}</p>'
            f'<div class="practice-mastery-action">'
            f'<button type="button" class="btn-card success btn-practice-claim-m2" style="display: none;">Ghi nhận M2 (Đạt ≥80% Rubric)</button>'
            f'<span class="practice-feedback" id="{feedback_id}" aria-live="polite"></span>'
            f'</div>'
            f'</div></div>'
        )

    title = {
        "characteristics": "ĐẶC TÍNH KỸ THUẬT",
        "note": "LƯU Ý QUAN TRỌNG",
        "important": "YÊU CẦU QUAN TRỌNG",
        "warning": "CẢNH BÁO KỸ THUẬT",
        "tip": "KHUYẾN NGHỊ THỰC HÀNH",
        # 12 Pedagogical Primitives contracts
        "conceptmap": "🗺️ BẢN ĐỒ KHÁI NIỆM",
        "problemhook": "❓ VẤN ĐỀ DẪN NHẬP",
        "mentalmodel": "🧠 MÔ HÌNH TƯ DUY",
        "predictioncheckpoint": "🔮 DỰ ĐOÁN HIỆN TƯỢNG (PREDICT)",
        "executiontrace": "🔍 VẾT THỰC THI HỆ THỐNG",
        "recallcheckpoint": "🎯 TRẠM THU HỒI CHỦ ĐỘNG",
        "workedexample": "📝 BÀI TOÁN MẪU CHI TIẾT (LEVEL A)",
        "fadedexample": "🧩 BÀI TẬP KHUYẾT BƯỚC (LEVEL B)",
        "transferproblem": "🚀 BÀI TOÁN CHUYỂN GIAO (LEVEL C)",
        "errordiagnosis": "⚠️ CHẨN ĐOÁN & SỬA SAI",
        "reviewhook": "🔄 ĐIỂM ÔN TẬP GẮN KẾT",
        "masterycheck": "🏆 ĐÁNH GIÁ NĂNG LỰC TOÀN DIỆN",
    }.get(lower, lower.upper())
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


def line_indent(line):
    """Return the number of leading spaces in a Markdown source line."""
    return len(line) - len(line.lstrip(" "))


def next_nonblank(lines, start):
    """Return the first non-blank line at or after ``start``."""
    index = start
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def parse_indented_paragraph(lines, start, parent_indent, routes, current_rel):
    """Parse a generic indented list-item continuation paragraph.

    Markdown commonly puts explanatory prose below a list item with a blank
    line before the next item.  Treat any non-structural line indented beyond
    the current list as content of that ``<li>``; nested lists, fences,
    blockquotes, and horizontal rules remain handled by their dedicated
    parsers before this fallback.
    """
    if start >= len(lines) or not lines[start].strip() or line_indent(lines[start]) <= parent_indent:
        return None, start
    paragraph, index = [], start
    while index < len(lines):
        current = lines[index]
        if not current.strip() or line_indent(current) <= parent_indent:
            break
        if LIST_ITEM_RE.match(current) or current.lstrip().startswith(">") or current.lstrip().startswith("```") or HORIZONTAL_RULE_RE.fullmatch(current):
            break
        paragraph.append(current.lstrip())
        index += 1
    if not paragraph:
        return None, start
    rendered = inline("\n".join(paragraph), routes, current_rel).replace("\n", "<br>")
    return f"<p>{rendered}</p>", index


def markdown_to_html(text, doc_id, routes, current_rel):
    lines = text.replace("\r\n", "\n").split("\n")
    output, index = [], 0
    seen_slugs = {}
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
            base_slug = slugify(title)
            count = seen_slugs.get(base_slug, 0)
            if count == 0:
                heading_id = base_slug
                seen_slugs[base_slug] = 1
            else:
                count += 1
                heading_id = f"{base_slug}-{count}"
                while heading_id in seen_slugs:
                    count += 1
                    heading_id = f"{base_slug}-{count}"
                seen_slugs[base_slug] = count
                seen_slugs[heading_id] = 1
            output.append(f'<h{level} id="{heading_id}">{inline(title, routes, current_rel)}</h{level}>')
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
            if not lines[index].strip():
                following = next_nonblank(lines, index)
                if following >= len(lines):
                    index = following
                    break
                following_match = LIST_ITEM_RE.match(lines[following])
                if following_match and len(following_match.group("indent")) == root_indent:
                    expected_tag = "ol" if following_match.group("marker")[0].isdigit() else "ul"
                    if expected_tag == tag:
                        index = following
                    break
                if line_indent(lines[following]) > root_indent:
                    index = following
                    continue
                break
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
            paragraph_html, paragraph_index = parse_indented_paragraph(lines, index, root_indent, routes, current_rel)
            if paragraph_html is not None:
                nested.append(paragraph_html)
                index = paragraph_index
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

    # ------------------------------------------------------------------
    # Stable-ID duplicate detection: fail fast at build time.
    # ------------------------------------------------------------------
    CARD_ID_RE = re.compile(r'data-(?:card|item|practice)-id="([^"]+)"')
    all_card_ids: list[str] = []
    for doc in docs:
        temp_html = markdown_to_html(doc["body"], doc["id"], routes, doc["route"])
        for cid in CARD_ID_RE.findall(temp_html):
            all_card_ids.append(cid)
    seen_ids: dict[str, int] = {}
    duplicate_ids: list[str] = []
    for cid in all_card_ids:
        seen_ids[cid] = seen_ids.get(cid, 0) + 1
    for cid, count in seen_ids.items():
        if count > 1:
            duplicate_ids.append(cid)
    if duplicate_ids:
        raise RuntimeError(
            f"BUILD FAIL — Duplicate interactive item IDs detected: {duplicate_ids}\n"
            "Each StudyCard, Checkpoint, or Practice must have a globally unique id='' attribute."
        )

    for doc in docs:
        doc["headings"] = re.findall(r"^#{1,6}\s+(.+?)\s*$", doc["body"], flags=re.MULTILINE)
        doc["searchable_text"] = search_text(doc["body"])
    search = [{"id": doc["id"], "title": doc["title"], "summary": doc["summary"], "headings": doc["headings"], "searchable_text": doc["searchable_text"], "url": doc["route"], "snippet": doc["summary"] or doc["title"]} for doc in docs]
    (output_dir / "search_index.json").write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    graph_nodes = [{"id": doc["id"], "label": doc["title"][:32], "link": doc["route"], "x": 40 + (i * 67) % 270, "y": 35 + (i * 43) % 125, "r": 7, "color": "#0969da"} for i, doc in enumerate(docs)]
    graph_edges = [{"from": doc["id"], "to": rel} for doc in docs for rel in (doc["meta"].get("related", []) if isinstance(doc["meta"].get("related", []), list) else []) if rel in routes]
    (output_dir / "graph_data.json").write_text(json.dumps({"nodes": graph_nodes, "edges": graph_edges}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------
    # study_index.json (REVIEW-LEARN-001)
    # Derived artifact for the client-side learning runtime.
    # Generated from canonical Markdown; never manually maintained.
    # ------------------------------------------------------------------
    STUDY_CARD_META_RE = re.compile(
        r'<div class="study-card"[^>]*data-card-id="(?P<cid>[^"]+)"[^>]*data-concept-id="(?P<concept>[^"]+)"[^>]*>.*?<div class="card-question">(?P<q>.*?)</div>',
        re.DOTALL,
    )
    RECALL_META_RE = re.compile(
        r'<div class="recall-checkpoint"[^>]*data-item-id="(?P<cid>[^"]+)"[^>]*data-concept-id="(?P<concept>[^"]+)"[^>]*>.*?<div class="checkpoint-prompt">(?P<q>.*?)</div>',
        re.DOTALL,
    )
    TRANSFER_META_RE = re.compile(
        r'<div class="transfer-problem"[^>]*data-item-id="(?P<cid>[^"]+)"[^>]*data-concept-id="(?P<concept>[^"]+)"[^>]*>.*?<div class="problem-prompt">(?P<q>.*?)</div>',
        re.DOTALL,
    )
    SUBJECTIVE_META_RE = re.compile(
        r'<div class="subjective-practice"[^>]*data-practice-id="(?P<cid>[^"]+)"[^>]*data-concept-id="(?P<concept>[^"]+)"[^>]*>.*?<div>(?P<q>.*?)</div>',
        re.DOTALL,
    )

    study_items = []
    for doc in docs:
        temp_html = markdown_to_html(doc["body"], doc["id"], routes, doc["route"])
        ch = doc["meta"].get("chapter", 0)

        # 1. StudyCards
        for m in STUDY_CARD_META_RE.finditer(temp_html):
            raw_q = re.sub(r"<[^>]+>", "", m.group("q")).strip()
            study_items.append({
                "id": m.group("cid"),
                "concept_id": m.group("concept"),
                "type": "studycard",
                "chapter": ch,
                "doc_id": doc["id"],
                "doc_title": doc["title"],
                "question": raw_q[:160],
                "url": doc["route"],
                "anchor": m.group("cid"),
            })

        # 2. RecallCheckpoints
        for m in RECALL_META_RE.finditer(temp_html):
            raw_q = re.sub(r"<[^>]+>", "", m.group("q")).strip()
            study_items.append({
                "id": m.group("cid"),
                "concept_id": m.group("concept"),
                "type": "recallcheckpoint",
                "chapter": ch,
                "doc_id": doc["id"],
                "doc_title": doc["title"],
                "question": raw_q[:160],
                "url": doc["route"],
                "anchor": m.group("cid"),
            })

        # 3. TransferProblems
        for m in TRANSFER_META_RE.finditer(temp_html):
            raw_q = re.sub(r"<[^>]+>", "", m.group("q")).strip()
            study_items.append({
                "id": m.group("cid"),
                "concept_id": m.group("concept"),
                "type": "transferproblem",
                "chapter": ch,
                "doc_id": doc["id"],
                "doc_title": doc["title"],
                "question": raw_q[:160],
                "url": doc["route"],
                "anchor": m.group("cid"),
            })

        # 4. SubjectivePractices
        for m in SUBJECTIVE_META_RE.finditer(temp_html):
            raw_q = re.sub(r"<[^>]+>", "", m.group("q")).strip()
            study_items.append({
                "id": m.group("cid"),
                "concept_id": m.group("concept"),
                "type": "subjectivepractice",
                "chapter": ch,
                "doc_id": doc["id"],
                "doc_title": doc["title"],
                "question": raw_q[:160],
                "url": doc["route"],
                "anchor": m.group("cid"),
            })

    (output_dir / "study_index.json").write_text(
        json.dumps(study_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def nav(current):
        groups = [
            ("LÝ THUYẾT", "theory"),
            ("NGÂN HÀNG CÂU HỎI", "questions"),
            ("ÔN TẬP", ("reviews", "review")),
            ("THỰC HÀNH", "labs"),
            ("ĐỀ THI & TRA CỨU", ("exams", "glossary", "flashcards")),
        ]
        out = []
        for label, kinds in groups:
            out.append(f'<div class="nav-section-title">{label}</div><ul class="nav-tree">')
            if label == "ÔN TẬP":
                hub_active = " active" if current == "review/index.html" else ""
                out.append(
                    f'<li class="nav-tree-item"><a class="nav-link{hub_active}"'
                    f' href="{relative_link(current, "review/index.html")}">Hàng đợi ôn tập (Review Hub)</a></li>'
                )
            for doc in docs:
                if (any(kind in doc["rel"] for kind in kinds) if isinstance(kinds, tuple) else kinds in doc["rel"]):
                    active = " active" if doc["route"] == current else ""
                    out.append(f'<li class="nav-tree-item"><a class="nav-link{active}" href="{relative_link(current, doc["route"])}">{html.escape(doc["title"])}</a></li>')
            out.append("</ul>")
        return "\n".join(out)

    def render_mode_switcher(prefix):
        return (
            '<div class="mode-switcher" role="group" aria-label="Chế độ học tập">'
            '<button type="button" class="mode-btn" data-mode="learn" aria-pressed="false">📚 Học</button>'
            '<button type="button" class="mode-btn" data-mode="review" aria-pressed="false">🔄 Ôn</button>'
            '<button type="button" class="mode-btn" data-mode="reference" aria-pressed="false">🔎 Tra</button>'
            f'<a class="review-hub-shortcut" id="review-hub-shortcut" href="{prefix}review/index.html" style="display: none;">Hàng đợi toàn môn ↗</a>'
            '</div>'
        )

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

        def format_toc_label(raw_html):
            clean_text = html.unescape(re.sub(r"<[^>]+>", "", raw_html))
            return html.escape(clean_text)

        toc = "".join(f'<li class="toc-item"><a class="toc-link" href="#{m.group(1)}">{format_toc_label(m.group(2))}</a></li>' for m in re.finditer(r'<h[23] id="([^"]+)">(.+?)</h[23]>', rendered))
        title = html.escape(str(doc["title"]))
        return f'''<!DOCTYPE html>
<html lang="vi" data-theme="light" data-ui-mode="learn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} — IT007 UIT</title><link rel="stylesheet" href="{prefix}assets/css/style.css"><script src="{prefix}assets/vendor/mathjax/es5/tex-mml-chtml.js"></script></head>
<body><header class="app-header"><a class="brand-container" href="{prefix}index.html"><span class="brand-badge">IT007</span><span class="brand-title">Hệ Điều Hành · IT007 UIT</span></a><div class="header-actions">{render_mode_switcher(prefix)}<button type="button" class="search-trigger-btn" id="search-trigger-btn">🔍 Tìm kiếm nhanh... <kbd class="kbd-shortcut">Ctrl+K</kbd></button><button type="button" class="theme-toggle-btn" id="theme-toggle-btn"><span id="theme-icon">🌙</span></button></div></header>
<div class="workspace-layout"><aside class="sidebar-left">{nav(route)}</aside><main class="content-center"><div class="breadcrumbs"><a href="{prefix}index.html">Trang chủ</a> <span>/</span> <span>{title}</span></div><article class="article-body">{rendered}{backlinks}<div class="article-footer">Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.</div></article></main><aside class="sidebar-right"><div class="graph-container"><div class="graph-header">Đồ Thị Tri Thức</div><canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas></div><div class="toc-container"><div class="toc-title">MỤC LỤC TRANG</div><ul class="toc-list">{toc or '<li class="toc-item">Trang không có tiểu mục</li>'}</ul></div></aside></div>
<div class="search-modal-overlay" id="search-modal-overlay"><div class="search-modal"><div class="search-input-wrapper">🔍<input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm..."><kbd class="kbd-shortcut">ESC</kbd></div><ul class="search-results-list" id="search-results-list"></ul></div></div><script src="{prefix}assets/js/app.js"></script></body></html>'''

    for doc in docs:
        target = output_dir / doc["route"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(doc), encoding="utf-8")

    # ------------------------------------------------------------------
    # Review Hub: review/index.html (REVIEW-LEARN-001)
    # ------------------------------------------------------------------
    review_hub_html = f'''<!DOCTYPE html>
<html lang="vi" data-theme="light" data-ui-mode="review"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Hàng Đợi Ôn Tập (Review Hub) — IT007 UIT</title><link rel="stylesheet" href="../assets/css/style.css"><script src="../assets/vendor/mathjax/es5/tex-mml-chtml.js"></script></head>
<body><header class="app-header"><a class="brand-container" href="../index.html"><span class="brand-badge">IT007</span><span class="brand-title">Hệ Điều Hành · IT007 UIT</span></a><div class="header-actions">{render_mode_switcher("../")}<button type="button" class="search-trigger-btn" id="search-trigger-btn">🔍 Tìm kiếm nhanh... <kbd class="kbd-shortcut">Ctrl+K</kbd></button><button type="button" class="theme-toggle-btn" id="theme-toggle-btn"><span id="theme-icon">🌙</span></button></div></header>
<div class="workspace-layout"><aside class="sidebar-left">{nav("review/index.html")}</aside><main class="content-center"><div class="breadcrumbs"><a href="../index.html">Trang chủ</a> <span>/</span> <a href="../reviews/midterm.html">Ôn tập</a> <span>/</span> <span>Review Hub</span></div><article class="article-body">
<h1>Hàng Đợi Ôn Tập Toàn Trang (Review Hub)</h1>
<p>Tổng hợp tất cả các mục Active Recall, Recall Checkpoint và Transfer Problem đến hạn ôn tập trên toàn bộ Cẩm nang Hệ Điều Hành IT007.</p>
<div class="review-hub-controls">
  <div class="review-stats-bar">
    <span class="stat-badge stat-due">Đến hạn: <strong id="hub-due-count">0</strong></span>
    <span class="stat-badge stat-weak">Cần củng cố: <strong id="hub-weak-count">0</strong></span>
    <span class="stat-badge stat-pending">Chờ chuyển giao: <strong id="hub-pending-count">0</strong></span>
    <span class="stat-badge stat-mistake">Có lỗi sai: <strong id="hub-mistake-count">0</strong></span>
    <span class="stat-badge stat-total">Tổng số thẻ: <strong id="hub-total-count">0</strong></span>
  </div>
  <div class="review-hub-actions">
    <button type="button" class="btn-card primary" id="btn-refresh-hub">🔄 Làm mới danh sách</button>
  </div>
</div>
<div id="review-hub-queue" class="review-hub-queue" aria-live="polite">
  <div class="queue-loading">Đang tải hàng đợi ôn tập từ bộ nhớ trình duyệt...</div>
</div>
<div class="article-footer">Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.</div></article></main><aside class="sidebar-right"><div class="graph-container"><div class="graph-header">Đồ Thị Tri Thức</div><canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas></div></aside></div>
<div class="search-modal-overlay" id="search-modal-overlay"><div class="search-modal"><div class="search-input-wrapper">🔍<input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm..."><kbd class="kbd-shortcut">ESC</kbd></div><ul class="search-results-list" id="search-results-list"></ul></div></div><script src="../assets/js/app.js"></script></body></html>'''
    (output_dir / "review" / "index.html").parent.mkdir(parents=True, exist_ok=True)
    (output_dir / "review" / "index.html").write_text(review_hub_html, encoding="utf-8")

    cards = []
    for doc in docs:
        if "theory" in doc["rel"]:
            cards.append(f'<a href="{doc["route"]}"><h3>{html.escape(doc["title"])}</h3><p>{html.escape(str(doc["summary"]))}</p></a>')
    index = f'''<!DOCTYPE html><html lang="vi" data-theme="light" data-ui-mode="learn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>IT007 · Hệ Điều Hành UIT</title><link rel="stylesheet" href="assets/css/style.css"><script src="assets/vendor/mathjax/es5/tex-mml-chtml.js"></script></head><body><header class="app-header"><a class="brand-container" href="index.html"><span class="brand-badge">IT007</span><span class="brand-title">Hệ Điều Hành · IT007 UIT</span></a><div class="header-actions">{render_mode_switcher("")}<button type="button" class="search-trigger-btn" id="search-trigger-btn">Tìm kiếm <kbd class="kbd-shortcut">Ctrl+K</kbd></button><button type="button" class="theme-toggle-btn" id="theme-toggle-btn"><span id="theme-icon">🌙</span></button></div></header><div class="workspace-layout"><aside class="sidebar-left">{nav("index.html")}</aside><main class="content-center"><article class="article-body"><h1>Hệ Điều Hành</h1><p>IT007 · Lý thuyết · Tự luận · Bài tập · Thực hành · Ôn tập · Đề thi</p><div class="article-meta-bar">Biên soạn: <strong>Võ Trọng Phúc</strong></div><h2>Các Chuyên Đề Cốt Lõi</h2><div class="document-grid">{"".join(cards)}</div><div class="article-footer">Tài liệu học tập độc lập dành cho môn IT007. Không phải ấn phẩm chính thức của UIT.</div></article></main><aside class="sidebar-right"><div class="graph-container"><div class="graph-header">Đồ Thị Tri Thức</div><canvas class="graph-canvas" id="knowledge-graph-canvas"></canvas></div></aside></div><div class="search-modal-overlay" id="search-modal-overlay"><div class="search-modal"><div class="search-input-wrapper"><input type="text" class="search-input" id="search-input" placeholder="Tìm kiếm..."><kbd class="kbd-shortcut">ESC</kbd></div><ul class="search-results-list" id="search-results-list"></ul></div></div><script src="assets/js/app.js"></script></body></html>'''
    (output_dir / "index.html").write_text(index, encoding="utf-8")
    print(f"Successfully compiled {len(docs) + 2} static pages into {output_dir}.")
    return docs




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-root", default=str(DEFAULT_CONTENT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    build_site(args.content_root, args.output_dir)

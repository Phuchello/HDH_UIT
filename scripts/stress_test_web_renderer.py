#!/usr/bin/env python3
"""Build realistic temporary fixtures and prove the custom renderer is parse-safe."""

from __future__ import annotations

import html.parser
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "research" / "WEB_RENDERER_STRESS_TEST.md"
sys.path.insert(0, str(ROOT / "scripts"))
from build_web import assert_safe_output_dir


class StructureParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = {"tag": "#root", "attrs": {}, "text": "", "children": [], "parent": None}
        self.stack = [self.root]
        self.errors = []

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "text": "", "children": [], "parent": self.stack[-1]}
        self.stack[-1]["children"].append(node)
        if tag not in {"meta", "link", "img", "input", "br", "hr"}:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack[-1]["tag"] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if len(self.stack) == 1 or self.stack[-1]["tag"] != tag:
            self.errors.append(f"unexpected closing tag: {tag}")
            return
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1]["text"] += data

    @property
    def open_tags(self):
        return [node["tag"] for node in self.stack[1:]]


def walk(node):
    for child in node["children"]:
        yield child
        yield from walk(child)


def has_descendant(node, tag):
    return any(child["tag"] == tag or has_descendant(child, tag) for child in node["children"])


def text_content(node):
    return node.get("text", "") + "".join(text_content(child) for child in node["children"])


def node_with_id(root, tag, node_id):
    return next((node for node in walk(root) if node["tag"] == tag and node["attrs"].get("id") == node_id), None)


def section_lists(root, heading_id):
    heading = node_with_id(root, "h3", heading_id)
    if heading is None:
        return []
    siblings = heading["parent"]["children"]
    start = siblings.index(heading) + 1
    end = next((index for index in range(start, len(siblings)) if siblings[index]["tag"] in {"h2", "h3"}), len(siblings))
    return [node for node in siblings[start:end] if node["tag"] == "ol"]


def section_list_shape(html_text, heading_id, expected_tokens, expected_count):
    parser = StructureParser()
    parser.feed(html_text)
    lists = section_lists(parser.root, heading_id)
    if len(lists) != 1:
        return parser, False
    ordered = lists[0]
    direct_items = [child for child in ordered["children"] if child["tag"] == "li"]
    if len(direct_items) != expected_count or len(ordered["children"]) != expected_count:
        return parser, False
    return parser, all(token in text_content(item) for token, item in zip(expected_tokens, direct_items))


def ordered_lists_well_formed(html_text):
    parser = StructureParser()
    parser.feed(html_text)
    ordered = [node for node in walk(parser.root) if node["tag"] == "ol"]
    return parser, all(any(child["tag"] == "li" for child in node["children"]) and all(child["tag"] == "li" for child in node["children"]) for node in ordered)


def list_item_has_nested_blockquote(theory):
    parser = StructureParser()
    parser.feed(theory)
    for ordered in (node for node in walk(parser.root) if node["tag"] == "ol"):
        direct_items = [child for child in ordered["children"] if child["tag"] == "li"]
        for first, second in zip(direct_items, direct_items[1:]):
            if "x.wait()" in text_content(first) and has_descendant(first, "blockquote") and "x.signal()" in text_content(second):
                return parser, True
    return parser, False


def structure_quality(html_text):
    parser = StructureParser()
    parser.feed(html_text)
    lists = [node for node in walk(parser.root) if node["tag"] in {"ul", "ol"}]
    items = [node for node in walk(parser.root) if node["tag"] == "li"]
    no_orphan_items = all(item["parent"]["tag"] in {"ul", "ol"} for item in items)
    nested_lists = [node for node in lists if any(ancestor["tag"] in {"ul", "ol"} for ancestor in ancestors(node))]
    valid_nested_lists = all(node["parent"]["tag"] == "li" for node in nested_lists)
    return parser, {
        "balanced HTML": not parser.open_tags and not parser.errors,
        "no orphan li": no_orphan_items,
        "valid nested-list relationships": valid_nested_lists,
    }


def list_structure_checks(theory):
    parser = StructureParser()
    parser.feed(theory)
    lists = [node for node in walk(parser.root) if node["tag"] in {"ul", "ol"}]
    items = [node for node in walk(parser.root) if node["tag"] == "li"]
    no_orphan_items = all(item["parent"]["tag"] in {"ul", "ol"} for item in items)
    nested_lists = [node for node in lists if any(ancestor["tag"] in {"ul", "ol"} for ancestor in ancestors(node))]
    no_fake_siblings = all(node["parent"]["tag"] == "li" for node in nested_lists)
    unordered_nested = any(node["tag"] == "ul" and any(child["tag"] == "li" and has_descendant(child, "ul") for child in node["children"]) for node in lists)
    ordered_nested = any(node["tag"] == "ol" and any(child["tag"] == "li" and has_descendant(child, "ol") for child in node["children"]) for node in lists)
    mixed_nested = any(node["tag"] == "ul" and any(child["tag"] == "li" and has_descendant(child, "ol") for child in node["children"]) for node in lists) and any(node["tag"] == "ul" and any(child["tag"] == "li" and has_descendant(child, "ul") for child in node["children"]) for node in lists)
    depth_three = max((1 + sum(1 for ancestor in ancestors(node) if ancestor["tag"] in {"ul", "ol"}) for node in lists), default=0) >= 3
    return parser, {
        "no orphan li": no_orphan_items,
        "no fake list siblings": no_fake_siblings,
        "nested unordered list": unordered_nested,
        "nested ordered list": ordered_nested,
        "mixed ordered/unordered list": mixed_nested,
        "depth-3 list": depth_three,
    }


def ancestors(node):
    parent = node.get("parent")
    while parent is not None:
        yield parent
        parent = parent.get("parent")


FIXTURES = {
    "theory/fixture.md": """---
id: \"fixture-theory\"
title: \"Định hướng Unicode & Công thức\"
summary: \"fixture\"
related:
  - \"fixture-questions\"
---

# Tiêu đề Tiếng Việt

## Dữ liệu lồng nhau

- Mục ngoài [[fixture-questions|có liên kết]]
  - Mục trong có `inline | pipe`
    - Mục sâu cấp ba
- Mục ngoài thứ hai
  1. x.wait()
     > **Cơ chế bắt buộc:** dùng `code` và [[fixture-questions|liên kết]].
     1. Cháu ordered
     2. Cháu ordered hai
  2. x.signal()
- Process
  1. New
  2. Ready
- Thread
  - PC
  - Registers
- Producer:
  ```c
  while (true) {
      produce();
  }
  ```
- Consumer:
  ```c
  while (true) {
      consume();
  }
  ```

- Continuation paragraph one
  This explanatory paragraph stays inside the first item with **inline** formatting.

- Continuation paragraph two

1. Ordered continuity one
   Its indented description remains inside the first ordered item.

2. Ordered continuity two

---
***
___

abc --- xyz

> Note with code:
> ```c
> signal(empty);
> ```

| Cột | Ví dụ |
| --- | --- |
| code | `a | b` |

```c
int main(void) {
  const char *s = \"a | b\";
  return s[0] == 'a' ? 0 : 1;
}
```

Công thức inline $E = mc^2$ và công thức khối:

$$\\sum_{i=1}^{n} i = n(n+1)/2$$

> [!NOTE]
> Callout có tiếng Việt và [[fixture-questions|liên kết bí danh]].

## Nghiên cứu & Phát triển

👉 **[Ngân hàng liên kết đậm](../questions/fixture-questions.md)**

### Đề bài gốc
Nội dung đề bài phân nhánh thứ nhất.

#### Bước giải chi tiết
Bước tính toán mẫu một.

### Đề bài gốc
Nội dung đề bài phân nhánh thứ hai.

#### Bước giải chi tiết
Bước tính toán mẫu hai.

```c
int adjacent_fence = 1;
```
> [!NOTE]
> Ghi chú kỹ thuật nằm sát cạnh fenced code block không bị nuốt.
""",
    "questions/fixture-questions.md": """---
id: \"fixture-questions\"
title: \"Câu hỏi fixture\"
related:
  - \"fixture-theory\"
---

# Câu hỏi

> [!STUDYCARD] id=\"fixture-card\"
> Câu hỏi có **định dạng**.
> <!-- answer -->
> Đáp án có `code`.
""",
    "theory/delete-me.md": """---
id: "fixture-delete-me"
title: "Xóa sau lượt build đầu"
summary: "stale route fixture"
---

# Trang sẽ bị xóa

Nội dung tạm thời.
""",
}


def main():
    with tempfile.TemporaryDirectory(prefix="hdh-renderer-") as tmp:
        root = Path(tmp)
        content = root / "content"
        output = root / "site"
        for relative, body in FIXTURES.items():
            target = content / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        checks = []

        def run_build(target_output=output):
            return subprocess.run([sys.executable, "scripts/build_web.py", "--content-root", str(content), "--output-dir", str(target_output)], cwd=ROOT, capture_output=True, text=True)

        def manifest(target_output):
            return {
                path.relative_to(target_output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in target_output.rglob("*") if path.is_file()
            }

        first_result = run_build()
        checks.append(("initial build exits zero", first_result.returncode == 0))
        files = [output / "index.html", output / "theory/fixture.html", output / "questions/fixture-questions.html", output / "theory/delete-me.html"]
        checks.append(("all initial fixture routes exist", all(path.is_file() for path in files)))
        for path in files:
            if path.is_file():
                parser = StructureParser()
                parser.feed(path.read_text(encoding="utf-8"))
                checks.append((f"{path.name} has balanced HTML", not parser.open_tags and not parser.errors))
        theory = (output / "theory/fixture.html").read_text(encoding="utf-8") if (output / "theory/fixture.html").is_file() else ""
        _, list_checks = list_structure_checks(theory)
        for label, ok in list_checks.items():
            checks.append((label, ok))
        checks.append(("table pipe, fenced code, Unicode, math and wikilink survive", all(token in theory for token in ("a | b", "language-c", "Định hướng", "mc", 'class="wikilink"'))))
        checks.append(("indented fenced code remains inside list items", theory.count('class="language-c"') >= 3 and "```" not in theory and "<li>Producer:<pre>" in theory and "<li>Consumer:<pre>" in theory))
        checks.append(("blockquote fenced code remains a code block", '<blockquote>' in theory and 'signal(empty);</code></pre></blockquote>' in theory))
        checks.append(("standalone horizontal rules render as hr", theory.count("<hr>") == 3 and "<p>---</p>" not in theory and "<p>***</p>" not in theory and "<p>___</p>" not in theory))
        checks.append(("inline hyphens remain paragraph text", "abc --- xyz" in theory and "<p>abc --- xyz</p>" in theory))
        condition_parser, condition_ok = list_item_has_nested_blockquote(theory)
        checks.append(("list continuation blockquote stays inside the correct ordered list item", condition_ok))
        checks.append(("list continuation has no escaped quote marker", "&gt; Cơ chế bắt buộc" not in theory))
        checks.append(("indented continuation paragraph stays inside its list item", "<li>Continuation paragraph one<p>This explanatory paragraph stays inside the first item with <strong>inline</strong> formatting.</p></li>" in theory))
        checks.append(("blank lines do not split one ordered list", theory.count("<ol>") >= 2 and "<ol><li>Ordered continuity one<p>Its indented description remains inside the first ordered item.</p></li><li>Ordered continuity two</li></ol>" in theory))
        _, fixture_structure = structure_quality(theory)
        checks.extend((f"fixture {label}", ok) for label, ok in fixture_structure.items())
        checks.append(("callout survives", '<div class="callout note">' in theory))
        # ENG-CH6-004..006 regression checks on fixture
        theory_parser = StructureParser()
        theory_parser.feed(theory)
        fixture_ids = [node["attrs"]["id"] for node in walk(theory_parser.root) if node["attrs"].get("id")]
        checks.append(("fixture HTML IDs are strictly unique", len(fixture_ids) == len(set(fixture_ids))))
        checks.append(("fixture repeated subsection slug disambiguation", "e-bai-goc" in fixture_ids and "e-bai-goc-2" in fixture_ids and "buoc-giai-chi-tiet" in fixture_ids and "buoc-giai-chi-tiet-2" in fixture_ids))
        checks.append(("fixture nested bold link renders anchor", '<strong><a href="../questions/fixture-questions.html">Ngân hàng liên kết đậm</a></strong>' in theory))
        checks.append(("fixture TOC ampersand single escaping", "Nghiên cứu &amp; Phát triển" in theory and "&amp;amp;" not in theory))
        checks.append(("fixture callout adjacent to fence renders as callout", '<div class="callout note">' in theory and "adjacent_fence" in theory))

        real_outputs = {
            "real Chapter 5 theory": ROOT / "public/site/theory/ch05-synchronization.html",
            "real Chapter 5 QBank": ROOT / "public/site/questions/subjective/ch05.html",
            "real Chapter 6 theory": ROOT / "public/site/theory/ch06-deadlock.html",
            "real Chapter 6 QBank": ROOT / "public/site/questions/subjective/ch06.html",
        }
        real_text = {}
        for label, path in real_outputs.items():
            exists = path.is_file()
            checks.append((f"{label} exists", exists))
            if not exists:
                continue
            content_html = path.read_text(encoding="utf-8")
            real_text[label] = content_html
            _, quality = structure_quality(content_html)
            checks.extend((f"{label} {name}", ok) for name, ok in quality.items())
            checks.append((f"{label} has no raw fence leak", "```" not in content_html))
            checks.append((f"{label} has no escaped quote marker leak", "&gt; Cơ chế bắt buộc" not in content_html))
            checks.append((f"{label} has no paragraph horizontal-rule leak", "<p>---</p>" not in content_html))
        real_theory = real_text.get("real Chapter 5 theory", "")
        real_qbank = real_text.get("real Chapter 5 QBank", "")
        if real_theory:
            _, real_condition = list_item_has_nested_blockquote(real_theory)
            checks.append(("real Chapter 5 condition-variable list relationship", real_condition))
            checks.append(("real Chapter 5 Producer/Consumer and exercise code render", all(token in real_theory for token in ("Tiến trình Producer", "Tiến trình Consumer", 'class="language-c"'))))
            checks.append(("real Chapter 5 standalone rules render as hr", real_theory.count("<hr>") >= 10))
            for label, heading_id, tokens, count in (
                ("Chapter 5 section 5.2 list continuity", "5-2-spinlock-vs-mutex-khong-busy-waiting", ("Spinlock", "Mutex Lock không Busy Waiting"), 2),
                ("Chapter 5 section 6.2 list continuity", "6-2-phan-loai-semaphore", ("Counting Semaphore", "Binary Semaphore"), 2),
                ("Chapter 5 section 8.2 list continuity", "8-2-cac-dang-that-bai-liveness-ien-hinh", ("Deadlock", "Starvation", "Priority Inversion", "Priority Inheritance Protocol"), 4),
            ):
                _, section_ok = section_list_shape(real_theory, heading_id, tokens, count)
                checks.append((label, section_ok))
        if real_qbank:
            _, qbank_lists = ordered_lists_well_formed(real_qbank)
            checks.append(("real Chapter 5 QBank ordered-list semantics", qbank_lists))
        if real_qbank:
            checks.append(("real Chapter 5 QBank exercise code renders", 'class="language-c"' in real_qbank))
            checks.append(("real Chapter 5 QBank standalone rules render as hr", real_qbank.count("<hr>") >= 10))

        real_ch6_theory = real_text.get("real Chapter 6 theory", "")
        real_ch6_qbank = real_text.get("real Chapter 6 QBank", "")
        if real_ch6_theory:
            checks.append(("real Chapter 6 theory nested bold link renders anchor", '<strong><a href="../questions/subjective/ch06.html">Ngân hàng Câu hỏi Tự luận &amp; Bài tập Chương 6</a></strong>' in real_ch6_theory))
            checks.append(("real Chapter 6 theory TOC single escaping", "&amp;amp;" not in real_ch6_theory))
            checks.append(("real Chapter 6 theory callout note adjacent to fence renders", '<div class="callout note">' in real_ch6_theory))
        if real_ch6_qbank:
            q6_parser = StructureParser()
            q6_parser.feed(real_ch6_qbank)
            q6_ids = [node["attrs"]["id"] for node in walk(q6_parser.root) if node["attrs"].get("id")]
            checks.append(("real Chapter 6 QBank HTML IDs are strictly unique", len(q6_ids) == len(set(q6_ids))))
            checks.append(("real Chapter 6 QBank repeated subsection slug disambiguation", "1-e-bai-goc-source-question" in q6_ids and "1-e-bai-goc-source-question-2" in q6_ids))
            checks.append(("real Chapter 6 QBank TOC single escaping", "&amp;amp;" not in real_ch6_qbank))

        deterministic_output = root / "site-deterministic"
        deterministic_result = run_build(deterministic_output)
        checks.append(("consecutive clean builds are deterministic", deterministic_result.returncode == 0 and manifest(output) == manifest(deterministic_output)))

        (content / "theory/delete-me.md").unlink()
        second_result = run_build()
        checks.append(("rebuild after source deletion exits zero", second_result.returncode == 0))
        checks.append(("stale deleted route is removed", not (output / "theory/delete-me.html").exists()))
        checks.append(("kept route remains", (output / "theory/fixture.html").is_file()))
        try:
            search = json.loads((output / "search_index.json").read_text(encoding="utf-8"))
            graph = json.loads((output / "graph_data.json").read_text(encoding="utf-8"))
            checks.append(("search index has no deleted document", not any(item.get("id") == "fixture-delete-me" for item in search)))
            checks.append(("graph has no deleted document", not any(node.get("id") == "fixture-delete-me" for node in graph.get("nodes", []))))
            checks.append(("navigation has no deleted route", "delete-me.html" not in (output / "index.html").read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            checks.extend([("search index has no deleted document", False), ("graph has no deleted document", False), ("navigation has no deleted route", False)])

        unsafe_paths = {
            "repository root": ROOT,
            "repository parent": ROOT.parent,
            "home": Path.home(),
            "public parent": ROOT / "public",
            "content": ROOT / "content",
            "src": ROOT / "src",
            "scripts": ROOT / "scripts",
            "research": ROOT / "research",
            "external sibling": ROOT.parent / "_hdh-uit-unsafe-sibling-do-not-touch",
        }
        for label, unsafe_path in unsafe_paths.items():
            existed_before = unsafe_path.exists()
            try:
                assert_safe_output_dir(unsafe_path)
            except RuntimeError as error:
                rejected = "Refusing unsafe generated output directory" in str(error)
            else:
                rejected = False
            checks.append((f"unsafe {label} validation is rejected without mutation", rejected and unsafe_path.exists() == existed_before))
        checks.append(("canonical production site validation is allowed", assert_safe_output_dir(ROOT / "public" / "site") == (ROOT / "public" / "site").resolve()))
        checks.append(("temporary output validation is allowed", assert_safe_output_dir(root / "allowed-temp-output") == (root / "allowed-temp-output").resolve()))
        passed = all(ok for _, ok in checks)
        rows = "\n".join(f"- {'PASS' if ok else 'FAIL'} — {label}" for label, ok in checks)
        REPORT.write_text(f"# Web Renderer Stress Test\n\n**Result:** **{'PASS' if passed else 'FAIL'}**\n\n{rows}\n\nFixtures are temporary and are deleted after this run.\n", encoding="utf-8")
        print(f"WEB RENDERER STRESS TEST: {'PASS' if passed else 'FAIL'}")
        for build_result in (first_result, deterministic_result, second_result):
            if build_result.stdout:
                print(build_result.stdout.strip())
            if build_result.stderr:
                print(build_result.stderr.strip(), file=sys.stderr)
        return passed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

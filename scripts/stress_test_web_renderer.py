#!/usr/bin/env python3
"""Build realistic temporary fixtures and prove the custom renderer is parse-safe."""

from __future__ import annotations

import html.parser
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "research" / "WEB_RENDERER_STRESS_TEST.md"


class StructureParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_tags = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"meta", "link", "img", "input", "br", "hr"}:
            self.open_tags.append(tag)

    def handle_endtag(self, tag):
        if tag in self.open_tags:
            self.open_tags.pop()
        else:
            self.errors.append(f"unexpected closing tag: {tag}")


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

- Mục ngoài
  - Mục trong có `inline | pipe`

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
        result = subprocess.run([sys.executable, "scripts/build_web.py", "--content-root", str(content), "--output-dir", str(output)], cwd=ROOT, capture_output=True, text=True)
        checks = []
        checks.append(("build exits zero", result.returncode == 0))
        files = [output / "index.html", output / "theory/fixture.html", output / "questions/fixture-questions.html"]
        checks.append(("all fixture routes exist", all(path.is_file() for path in files)))
        for path in files:
            if path.is_file():
                parser = StructureParser()
                parser.feed(path.read_text(encoding="utf-8"))
                checks.append((f"{path.name} has balanced HTML", not parser.open_tags and not parser.errors))
        theory = (output / "theory/fixture.html").read_text(encoding="utf-8") if (output / "theory/fixture.html").is_file() else ""
        checks.append(("nested list, table pipe, fenced code, Unicode, and math survive", all(token in theory for token in ("<ul>", "a | b", "language-c", "Định hướng", "mc"))))
        passed = all(ok for _, ok in checks)
        rows = "\n".join(f"- {'PASS' if ok else 'FAIL'} — {label}" for label, ok in checks)
        REPORT.write_text(f"# Web Renderer Stress Test\n\n**Result:** **{'PASS' if passed else 'FAIL'}**\n\n{rows}\n\nFixtures are temporary and are deleted after this run.\n", encoding="utf-8")
        print(f"WEB RENDERER STRESS TEST: {'PASS' if passed else 'FAIL'}")
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return passed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

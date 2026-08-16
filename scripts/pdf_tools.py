import argparse
import json
import logging
import math
import os
import re
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

logging.getLogger("pypdf").setLevel(logging.ERROR)

CHAPTERS = [
    ("00-intro", "Phần 0 - Cách học và nền tảng"),
    ("01-overview", "Chương 1 - Tổng quan Hệ điều hành"),
    ("02-structure", "Chương 2 - Cấu trúc Hệ điều hành"),
    ("03-process", "Chương 3 - Quản lý tiến trình"),
    ("04-cpu-scheduling", "Chương 4 - Định thời CPU"),
    ("midterm-review", "Ôn tập giữa kỳ"),
    ("05-synchronization", "Chương 5 - Đồng bộ tiến trình"),
    ("06-deadlock", "Chương 6 - Deadlock"),
    ("07-memory-management", "Chương 7 - Quản lý bộ nhớ"),
    ("08-virtual-memory", "Chương 8 - Bộ nhớ ảo"),
    ("final-review", "Ôn tập cuối kỳ"),
    ("appendix-linux", "Phụ lục - Linux Survival Kit"),
]


def marker(slug: str) -> str:
    return "PAGE_MARKER_" + slug.replace("-", "_").upper()


def page_map(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    found = {}
    marker_pages = {marker(slug): slug for slug, _ in CHAPTERS}
    marker_pages["PAGE_MARKER_TOC"] = "toc"
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        compact = re.sub(r"\s+", "", text)
        for token, slug in marker_pages.items():
            if token in text or token.replace("_", "") in compact:
                found.setdefault(slug, number)
    missing = [slug for slug, _ in CHAPTERS if slug not in found]
    if missing:
        raise RuntimeError(f"Missing PDF chapter markers: {missing}")
    return found


def cmd_map(args):
    mapping = page_map(Path(args.pdf))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(mapping, ensure_ascii=False, indent=2))


def register_fonts():
    candidates = [
        ("Arial", r"C:\Windows\Fonts\arial.ttf"),
        ("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"),
        ("DejaVu", r"C:\Windows\Fonts\DejaVuSans.ttf"),
        ("DejaVu-Bold", r"C:\Windows\Fonts\DejaVuSans-Bold.ttf"),
    ]
    registered = set()
    for name, filename in candidates:
        if os.path.exists(filename):
            pdfmetrics.registerFont(TTFont(name, filename))
            registered.add(name)
    regular = "Arial" if "Arial" in registered else ("DejaVu" if "DejaVu" in registered else "Helvetica")
    bold = "Arial-Bold" if "Arial-Bold" in registered else ("DejaVu-Bold" if "DejaVu-Bold" in registered else "Helvetica-Bold")
    return regular, bold


def current_header(page_number, mapping):
    if page_number < mapping.get("00-intro", 10**9):
        return "Mục lục"
    label = "Cẩm nang Hệ điều hành IT007"
    for slug, chapter_label in CHAPTERS:
        if page_number >= mapping[slug]:
            label = chapter_label
    return label


def make_overlay(path, reader, mapping):
    regular, bold = register_fonts()
    c = canvas.Canvas(str(path), pagesize=(595.2756, 841.8898), pageCompression=1)
    for page_number, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        c.setPageSize((width, height))
        if page_number > 1:
            c.setStrokeColorRGB(0.78, 0.82, 0.87)
            c.setLineWidth(0.45)
            c.line(42, height - 34, width - 42, height - 34)
            c.setFillColorRGB(0.28, 0.34, 0.43)
            c.setFont(regular, 7.6)
            header = current_header(page_number, mapping)
            c.drawString(42, height - 27, header[:92])
            c.setFont(bold, 7.6)
            c.drawRightString(width - 42, height - 27, "IT007 - UIT")
            c.setStrokeColorRGB(0.82, 0.85, 0.89)
            c.line(42, 31, width - 42, 31)
            c.setFont(regular, 8)
            c.drawCentredString(width / 2, 19, str(page_number))
        c.showPage()
    c.save()


def analyze(pdf_path: Path):
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(x_tolerance=1.5, y_tolerance=2)
            text = page.extract_text() or ""
            widths_ok = abs(page.width - 595.276) < 1.5
            heights_ok = abs(page.height - 841.89) < 1.5
            if words:
                top = min(w["top"] for w in words)
                bottom = max(w["bottom"] for w in words)
                used_vertical = max(0.0, min(1.0, (bottom - top) / page.height))
            else:
                used_vertical = 0.0
            row = {
                "page": i,
                "widthPt": round(page.width, 3),
                "heightPt": round(page.height, 3),
                "a4": widths_ok and heights_ok,
                "words": len(words),
                "chars": len(text),
                "images": len(page.images),
                "rects": len(page.rects),
                "curves": len(page.curves),
                "usedVerticalRatio": round(used_vertical, 3),
            }
            flags = []
            if not row["a4"]:
                flags.append("unexpected_page_size")
            if i != 1 and len(words) < 35:
                flags.append("near_blank")
            elif i != 1 and (len(words) < 95 or used_vertical < 0.38):
                flags.append("sparse")
            if len(words) > 720 or len(text) > 5000:
                flags.append("dense")
            row["flags"] = flags
            pages.append(row)
    return pages


def cmd_finalize(args):
    raw = Path(args.raw)
    output = Path(args.out)
    toc_expected = json.loads(Path(args.toc).read_text(encoding="utf-8"))
    toc_actual = page_map(raw)
    mismatches = {slug: {"toc": toc_expected.get(slug), "actual": toc_actual.get(slug)} for slug, _ in CHAPTERS if toc_expected.get(slug) != toc_actual.get(slug)}
    if mismatches:
        raise RuntimeError(f"TOC changed between passes: {mismatches}")
    reader = PdfReader(str(raw))
    overlay = output.with_suffix(".overlay.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    make_overlay(overlay, reader, toc_actual)
    overlay_reader = PdfReader(str(overlay))
    writer = PdfWriter()
    for index, page in enumerate(reader.pages):
        page.merge_page(overlay_reader.pages[index])
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Cẩm nang Hệ điều hành IT007 - UIT",
        "/Author": "Võ Trọng Phúc",
        "/Subject": "Tài liệu học tập môn Hệ điều hành IT007",
        "/Creator": "Deterministic offline publication build",
        "/Producer": "pypdf",
        "/CreationDate": "D:20260813000000+07'00'",
        "/ModDate": "D:20260813000000+07'00'",
    })
    with output.open("wb") as stream:
        writer.write(stream)
    overlay.unlink(missing_ok=True)
    reopened = PdfReader(str(output))
    if len(reopened.pages) != len(reader.pages):
        raise RuntimeError("Page count changed during finalization")
    pages = analyze(output)
    report = {
        "pdf": str(output),
        "pageCount": len(pages),
        "tocExpected": toc_expected,
        "tocActual": toc_actual,
        "tocVerified": not mismatches,
        "unexpectedPageSizes": [p["page"] for p in pages if "unexpected_page_size" in p["flags"]],
        "suspectPages": [p["page"] for p in pages if p["flags"]],
        "pages": pages,
    }
    Path(args.analysis).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "pages"}, ensure_ascii=False, indent=2))


def find_pdftoppm():
    candidates = [
        str(Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "poppler" / "Library" / "bin" / "pdftoppm.exe"),
        "pdftoppm",
        "pdftoppm.cmd",
    ]
    for name in candidates:
        if os.path.isabs(name) and not os.path.exists(name):
            continue
        try:
            subprocess.run([name, "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            return name
        except FileNotFoundError:
            pass
    raise RuntimeError("pdftoppm not found")


def cmd_render_pages(args):
    pdf = Path(args.pdf).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    for old in list(outdir.glob("page-*.png")) + list(outdir.glob("contact-*.png")):
        old.unlink()
    tool = find_pdftoppm()
    prefix = outdir / "page"
    subprocess.run([tool, "-png", "-r", str(args.dpi), str(pdf), str(prefix)], check=True)
    files = sorted(outdir.glob("page-*.png"), key=lambda p: int(re.search(r"(\d+)$", p.stem).group(1)))
    if not files:
        raise RuntimeError("No pages rendered")
    thumb_w = 220
    thumb_h = int(thumb_w * math.sqrt(2))
    cols, rows = 4, 5
    per_sheet = cols * rows
    font = ImageFont.load_default()
    sheets = []
    for sheet_index in range(math.ceil(len(files) / per_sheet)):
        batch = files[sheet_index*per_sheet:(sheet_index+1)*per_sheet]
        sheet = Image.new("RGB", (cols*(thumb_w+16)+16, rows*(thumb_h+30)+16), "#d8dde5")
        draw = ImageDraw.Draw(sheet)
        for slot, file in enumerate(batch):
            with Image.open(file) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb_w, thumb_h))
                x = 16 + (slot % cols)*(thumb_w+16)
                y = 16 + (slot // cols)*(thumb_h+30)
                sheet.paste(im, (x, y))
                page_no = int(re.search(r"(\d+)$", file.stem).group(1))
                draw.text((x, y+thumb_h+5), f"Page {page_no}", fill="#172033", font=font)
        sheet_path = outdir / f"contact-{sheet_index+1:02d}.png"
        sheet.save(sheet_path, optimize=True)
        sheets.append(str(sheet_path))
    print(json.dumps({"pageImages":len(files), "contactSheets":sheets}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("map")
    p.add_argument("--pdf", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_map)
    p = sub.add_parser("finalize")
    p.add_argument("--raw", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--toc", required=True)
    p.add_argument("--analysis", required=True)
    p.set_defaults(func=cmd_finalize)
    p = sub.add_parser("render-pages")
    p.add_argument("--pdf", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--dpi", type=int, default=90)
    p.set_defaults(func=cmd_render_pages)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

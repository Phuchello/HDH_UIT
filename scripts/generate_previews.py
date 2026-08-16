#!/usr/bin/env python3
"""
Generate optimized preview PNG images from the canonical IT007 handbook PDF for GitHub documentation and README.
"""

from pathlib import Path
import sys
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "dist" / "IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf"
PREVIEW_DIR = ROOT / "docs" / "preview"

PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

if not PDF_PATH.exists():
    print(f"Error: Canonical PDF not found at {PDF_PATH}", file=sys.stderr)
    sys.exit(1)

pdf = pdfium.PdfDocument(PDF_PATH)
total_pages = len(pdf)
print(f"Loaded canonical PDF with {total_pages} pages.")

# 1. Cover (Page 1)
cover_img = pdf[0].render(scale=2.0).to_pil().convert("RGB")
cover_img.save(PREVIEW_DIR / "cover.png", optimize=True)
print("Saved docs/preview/cover.png")

# 2. Table of Contents (Page 2)
toc_img = pdf[1].render(scale=2.0).to_pil().convert("RGB")
toc_img.save(PREVIEW_DIR / "toc.png", optimize=True)
print("Saved docs/preview/toc.png")

# 3. Sample Process & Fork (Page 15)
process_img = pdf[14].render(scale=2.0).to_pil().convert("RGB")
process_img.save(PREVIEW_DIR / "sample-process.png", optimize=True)
print("Saved docs/preview/sample-process.png")

# 4. Sample Scheduling & Gantt (Page 23)
sched_img = pdf[22].render(scale=2.0).to_pil().convert("RGB")
sched_img.save(PREVIEW_DIR / "sample-scheduling.png", optimize=True)
print("Saved docs/preview/sample-scheduling.png")

# 5. Sample Virtual Memory & Page Replacement (Page 44)
mem_img = pdf[43].render(scale=2.0).to_pil().convert("RGB")
mem_img.save(PREVIEW_DIR / "sample-memory.png", optimize=True)
print("Saved docs/preview/sample-memory.png")

# 6. Showcase Montage (Cover, Scheduling, Synchronization, Memory)
montage_pages = [1, 23, 31, 44]  # Cover, CPU Scheduling, Semaphore, LRU Paging
card_w = 340
card_h = 480
spacing = 20
margin_x = 30
margin_y = 40

total_w = len(montage_pages) * card_w + (len(montage_pages) - 1) * spacing + margin_x * 2
total_h = card_h + margin_y * 2 + 40

canvas = Image.new("RGB", (total_w, total_h), "#0b132b")
draw = ImageDraw.Draw(canvas)

for idx, p_num in enumerate(montage_pages):
    p_img = pdf[p_num - 1].render(scale=2.0).to_pil().convert("RGB")
    thumb = p_img.resize((card_w, card_h), Image.Resampling.LANCZOS)
    
    pos_x = margin_x + idx * (card_w + spacing)
    pos_y = margin_y + 30
    
    # Shadow
    shadow_box = Image.new("RGBA", (card_w + 12, card_h + 12), (0, 0, 0, 150))
    canvas.paste(shadow_box, (pos_x + 5, pos_y + 5), shadow_box)
    canvas.paste(thumb, (pos_x, pos_y))

draw.text((margin_x, 15), "IT007 — CẨM NANG HỆ ĐIỀU HÀNH UIT (VÕ TRỌNG PHÚC)", fill="#48cae4")
draw.text((margin_x, 35), "Bản xem trước các chuyên đề: Bìa sách • Định thời CPU (Tr. 23) • Đồng bộ Semaphore (Tr. 31) • Bộ nhớ ảo LRU (Tr. 44)", fill="#90e0ef")

canvas.save(PREVIEW_DIR / "handbook-showcase.png", optimize=True)
print("Saved docs/preview/handbook-showcase.png")

print("All preview assets generated successfully!")

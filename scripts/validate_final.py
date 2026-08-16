import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "dist" / "IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html"
PDF = ROOT / "dist" / "IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf"


def main():
    source = HTML.read_text(encoding="utf-8")
    ids = re.findall(r'\bid\s*=\s*["\']([^"\']+)["\']', source, flags=re.I)
    hrefs = re.findall(r'\bhref\s*=\s*["\']([^"\']+)["\']', source, flags=re.I)
    srcs = re.findall(r'\bsrc\s*=\s*["\']([^"\']+)["\']', source, flags=re.I)
    local_refs = [x for x in srcs + hrefs if not x.startswith(("#", "http://", "https://", "data:", "mailto:"))]
    missing = []
    for ref in local_refs:
        candidate = (HTML.parent / ref.split("?", 1)[0].split("#", 1)[0]).resolve()
        if not candidate.exists():
            missing.append({"reference":ref,"resolved":str(candidate)})
    anchors = [x[1:] for x in hrefs if x.startswith("#")]
    broken_anchors = [x for x in anchors if x not in ids]
    placeholders = []
    placeholder_re = re.compile(r"\b(TODO|FIXME|TBD|PLACEHOLDER|LOREM|INSERT)\b|\?\?\?", re.I)
    for number, line in enumerate(source.splitlines(), start=1):
        if placeholder_re.search(line):
            placeholders.append({"line":number,"text":line.strip()[:240]})

    reader = PdfReader(str(PDF))
    page_sizes = []
    searchable_pages = 0
    link_annotations = 0
    for index, page in enumerate(reader.pages, start=1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        page_sizes.append({"page":index,"widthPt":round(width,3),"heightPt":round(height,3),"a4":abs(width-595.276)<1.5 and abs(height-841.89)<1.5})
        if (page.extract_text() or "").strip():
            searchable_pages += 1
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            if annotation.get("/Subtype") == "/Link":
                link_annotations += 1

    result = {
        "finalHtml": str(HTML),
        "finalPdf": str(PDF),
        "iframeCount": len(re.findall(r"<iframe\b", source, flags=re.I)),
        "remoteDependencyCount": len(re.findall(r'(?:src|href)\s*=\s*["\']https?://', source, flags=re.I)),
        "localReferences": local_refs,
        "missingAssets": missing,
        "idCount": len(ids),
        "uniqueIdCount": len(set(ids)),
        "duplicateIds": sorted({x for x in ids if ids.count(x) > 1}),
        "anchorLinkCount": len(anchors),
        "brokenAnchors": broken_anchors,
        "placeholderMatches": placeholders,
        "pageCount": len(reader.pages),
        "a4Pages": sum(x["a4"] for x in page_sizes),
        "searchablePages": searchable_pages,
        "pdfLinkAnnotations": link_annotations,
        "metadata": {str(k):str(v) for k,v in (reader.metadata or {}).items()},
    }
    failures = []
    for key in ("iframeCount", "remoteDependencyCount"):
        if result[key] != 0: failures.append(key)
    for key in ("missingAssets", "duplicateIds", "brokenAnchors", "placeholderMatches"):
        if result[key]: failures.append(key)
    if result["a4Pages"] != result["pageCount"]: failures.append("pageSize")
    if result["searchablePages"] != result["pageCount"]: failures.append("searchableText")
    result["result"] = "PASS" if not failures else "FAIL"
    result["failures"] = failures
    out = ROOT / "build" / "final-validation.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

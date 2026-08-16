const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const ROOT = path.resolve(__dirname, '..');
const CHAPTERS = [
  ['00-intro', 'Phần 0', 'Cách học IT007 và nền tảng C/Linux', 'chapter'],
  ['01-overview', 'Chương 1', 'Tổng quan về Hệ điều hành', 'chapter'],
  ['02-structure', 'Chương 2', 'Cấu trúc Hệ điều hành', 'chapter'],
  ['03-process', 'Chương 3', 'Quản lý tiến trình', 'chapter'],
  ['04-cpu-scheduling', 'Chương 4', 'Định thời CPU', 'chapter'],
  ['midterm-review', 'Giữa kỳ', 'Master Review và đề thi thử', 'review'],
  ['05-synchronization', 'Chương 5', 'Đồng bộ tiến trình', 'chapter'],
  ['06-deadlock', 'Chương 6', 'Deadlock (Bế tắc)', 'chapter'],
  ['07-memory-management', 'Chương 7', 'Quản lý bộ nhớ', 'chapter'],
  ['08-virtual-memory', 'Chương 8', 'Bộ nhớ ảo', 'chapter'],
  ['final-review', 'Cuối kỳ', 'Master Review và 02 đề thi mô phỏng', 'review'],
  ['appendix-linux', 'Phụ lục', 'Linux Survival Kit và mẫu mã thực hành chọn lọc', 'appendix'],
];

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

function readUtf8(file) {
  return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
}

function bodyOf(html, file) {
  const match = html.match(/<body\b[^>]*>([\s\S]*?)<\/body>/i);
  if (!match) throw new Error(`No body found in ${file}`);
  return match[1].trim();
}

function normalizeIds(fragment, prefix) {
  const ids = new Map();
  fragment.replace(/\bid\s*=\s*(["'])([^"']+)\1/gi, (_, q, id) => {
    if (!ids.has(id)) ids.set(id, `${prefix}-${id}`);
    return _;
  });
  for (const [oldId, newId] of ids) {
    const escaped = oldId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    fragment = fragment
      .replace(new RegExp(`(\\bid\\s*=\\s*["'])${escaped}(["'])`, 'gi'), `$1${newId}$2`)
      .replace(new RegExp(`(href\\s*=\\s*["']#)${escaped}(["'])`, 'gi'), `$1${newId}$2`)
      .replace(new RegExp(`(\\bfor\\s*=\\s*["'])${escaped}(["'])`, 'gi'), `$1${newId}$2`);
  }
  return fragment;
}

function stats(html) {
  const count = re => (html.match(re) || []).length;
  const ids = [...html.matchAll(/\bid\s*=\s*["']([^"']+)["']/gi)].map(m => m[1]);
  return {
    chars: html.length,
    headings: count(/<h[1-6]\b/gi),
    paragraphs: count(/<p\b/gi),
    tables: count(/<table\b/gi),
    pre: count(/<pre\b/gi),
    code: count(/<code\b/gi),
    svg: count(/<svg\b/gi),
    images: count(/<img\b/gi),
    links: count(/<a\b/gi),
    ids: ids.length,
    uniqueIds: new Set(ids).size,
    classes: count(/\bclass\s*=/gi),
  };
}

function sumStats(rows) {
  const total = {};
  for (const row of rows) for (const [key, value] of Object.entries(row.stats)) {
    if (key !== 'chars') total[key] = (total[key] || 0) + value;
  }
  return total;
}

function htmlEscape(text) {
  return String(text).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}

function merge() {
  const out = path.resolve(arg('out', path.join(ROOT, 'dist', 'master-final.html')));
  const tocFile = arg('toc');
  const tocPages = tocFile && fs.existsSync(tocFile) ? JSON.parse(readUtf8(tocFile)) : {};
  const css = ['components.css', 'publication.css']
    .map(name => {
      const cssPath = fs.existsSync(path.join(ROOT, 'src', 'styles', name))
        ? path.join(ROOT, 'src', 'styles', name)
        : path.join(ROOT, 'styles', name);
      const localCss = readUtf8(cssPath)
        .replace(/@import\s+url\([^)]*\)\s*;?/gi, '');
      return `/* ${name} */\n${localCss}`;
    })
    .join('\n\n');

  const sourceRows = [];
  const sections = CHAPTERS.map(([slug, kind, title, type]) => {
    const file = fs.existsSync(path.join(ROOT, 'src', 'chapters', `${slug}.html`))
      ? path.join(ROOT, 'src', 'chapters', `${slug}.html`)
      : path.join(ROOT, 'chapters', `${slug}.html`);
    let body = bodyOf(readUtf8(file), file);
    sourceRows.push({slug, file: path.relative(ROOT, file), stats: stats(body)});
    body = normalizeIds(body, slug);
    return `<article class="chapter chapter-${type}" id="chapter-${slug}" data-chapter="${slug}">
<span class="page-marker" aria-hidden="true">PAGE_MARKER_${slug.replace(/-/g, '_').toUpperCase()}</span>
${body}
</article>`;
  }).join('\n\n');

  const toc = CHAPTERS.map(([slug, kind, title, type]) => {
    const page = tocPages[slug] || '—';
    return `<li class="toc-item toc-${type}"><a href="#chapter-${slug}"><span class="toc-kind">${htmlEscape(kind)}:</span> ${htmlEscape(title)}</a><span class="toc-leader"></span><span class="toc-page" data-toc-for="${slug}">${htmlEscape(page)}</span></li>`;
  }).join('\n');

  const document = `<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cẩm nang Hệ điều hành IT007 - Võ Trọng Phúc</title>
<meta name="author" content="Võ Trọng Phúc">
<style>${css}</style>
<script>window.MathJax={loader:{load:['input/tex','output/chtml']},tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']],displayMath:[['$$','$$'],['\\\\[','\\\\]']],processEscapes:true},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']},startup:{typeset:true}};</script>
<script defer src="../src/vendor/mathjax/es5/tex-mml-chtml.js"></script>
</head>
<body>
<section class="book-cover" id="cover">
  <div>
    <div class="cover-kicker">Trường Đại học Công nghệ Thông tin - ĐHQG-HCM</div>
    <div class="cover-course">KHOA KỸ THUẬT MÁY TÍNH - MÔN IT007</div>
  </div>
  <div class="cover-main">
    <h1 class="cover-title">CẨM NANG HỆ ĐIỀU HÀNH</h1>
    <div class="cover-it007">IT007 - UIT</div>
    <div class="cover-subtitle">Từ trực giác → bản chất → thuật toán → bài tập → Lab Linux → luyện thi</div>
  </div>
  <div class="cover-meta">
    <div class="cover-author">Biên soạn: Võ Trọng Phúc</div>
    <div class="cover-edition">Bản biên soạn 2026</div>
  </div>
</section>
<nav class="toc-container" id="table-of-contents" aria-label="Mục lục">
  <span class="page-marker" aria-hidden="true">PAGE_MARKER_TOC</span>
  <h1 class="toc-title">MỤC LỤC</h1>
  <p class="toc-note">Số trang được tạo tự động từ bản PDF hai lượt. Nhấn vào mục để chuyển đến chương tương ứng trong HTML.</p>
  <ol class="toc-list">${toc}</ol>
</nav>
<main>${sections}</main>
</body>
</html>`;

  fs.mkdirSync(path.dirname(out), {recursive: true});
  fs.writeFileSync(out, document, 'utf8');
  const mergedStats = stats(sections);
  const audit = {
    generatedAt: '2026-08-13',
    chapterOrder: CHAPTERS.map(x => x[0]),
    source: sourceRows,
    sourceTotals: sumStats(sourceRows),
    merged: mergedStats,
    iframeCount: (document.match(/<iframe\b/gi) || []).length,
    remoteDependencyCount: (document.match(/(?:src|href)\s*=\s*["']https?:\/\//gi) || []).length,
  };
  const auditPath = path.join(ROOT, 'build', 'merge-audit.json');
  fs.mkdirSync(path.dirname(auditPath), {recursive: true});
  fs.writeFileSync(auditPath, JSON.stringify(audit, null, 2), 'utf8');
  console.log(JSON.stringify({out, auditPath, iframeCount:audit.iframeCount, remoteDependencyCount:audit.remoteDependencyCount, merged: mergedStats}, null, 2));
}

async function render() {
  const input = path.resolve(arg('input'));
  const out = path.resolve(arg('out'));
  const diagnostics = path.resolve(arg('diagnostics', `${out}.json`));
  const executablePath = arg('chrome');
  if (!input || !out || !executablePath) throw new Error('render requires --input, --out and --chrome');
  const { chromium } = require('playwright');
  const browser = await chromium.launch({headless:true, executablePath, args:['--allow-file-access-from-files','--disable-gpu']});
  try {
    const context = await browser.newContext();
    let remoteRequests = [];
    await context.route(/^https?:\/\//, route => { remoteRequests.push(route.request().url()); return route.abort('blockedbyclient'); });
    const page = await context.newPage();
    await page.goto(pathToFileURL(input).href, {waitUntil:'load', timeout:120000});
    await page.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, {timeout:120000});
    await page.evaluate(() => MathJax.startup.promise);
    await page.evaluate(() => document.fonts && document.fonts.ready);
    const diag = await page.evaluate(() => {
      const unresolved = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        const parent = node.parentElement;
        if (!parent || parent.closest('script,style,pre,code,mjx-container')) continue;
        const t = node.nodeValue || '';
        if (/\$\$|(^|[^\\])\$[^$]+\$|\\\(|\\\)|\\\[|\\\]/.test(t)) unresolved.push(t.trim().slice(0,180));
      }
      // Ignore sub-pixel/scrollbar variance and MathJax's intentionally wide internal
      // measurement nodes; report only material layout overflow in printable content.
      const overflow = [...document.querySelectorAll('body *')].filter(el => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && (el.scrollWidth - el.clientWidth > 12) && !el.closest('pre,mjx-container');
      }).slice(0,50).map(el => ({tag:el.tagName, cls:el.className, id:el.id, client:el.clientWidth, scroll:el.scrollWidth}));
      return {
        title: document.title,
        mathContainers: document.querySelectorAll('mjx-container').length,
        mathErrors: document.querySelectorAll('mjx-merror').length,
        unresolvedVisibleMath: unresolved,
        iframeCount: document.querySelectorAll('iframe').length,
        chapters: document.querySelectorAll('article.chapter').length,
        overflow,
      };
    });
    diag.remoteRequests = remoteRequests;
    await page.emulateMedia({media:'print'});
    fs.mkdirSync(path.dirname(out), {recursive:true});
    await page.pdf({path:out, format:'A4', printBackground:true, preferCSSPageSize:true, displayHeaderFooter:false, margin:{top:'0',right:'0',bottom:'0',left:'0'}});
    fs.writeFileSync(diagnostics, JSON.stringify(diag, null, 2), 'utf8');
    if (diag.mathErrors || diag.unresolvedVisibleMath.length || remoteRequests.length || diag.iframeCount) {
      throw new Error(`Render validation failed: ${JSON.stringify(diag)}`);
    }
    console.log(JSON.stringify({out, diagnostics, ...diag}, null, 2));
  } finally {
    await browser.close();
  }
}

(async () => {
  const cmd = process.argv[2];
  if (cmd === 'merge') merge();
  else if (cmd === 'render') await render();
  else throw new Error('Usage: node build.js <merge|render> [options]');
})().catch(error => { console.error(error.stack || error); process.exit(1); });

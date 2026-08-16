param(
    [string]$ChromePath,
    [string]$NodePath,
    [string]$PythonPath
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot

function Find-Tool($name, $candidates) {
    if (Get-Command $name -ErrorAction SilentlyContinue) {
        return (Get-Command $name).Source
    }
    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }
    throw "Required tool '$name' was not found on PATH or in the supplied candidates."
}

$NodeExe = if ($NodePath) { $NodePath } else { Find-Tool "node" @() }
$PythonExe = if ($PythonPath) { $PythonPath } elseif (Get-Command python -ErrorAction SilentlyContinue) { (Get-Command python).Source } elseif (Get-Command py -ErrorAction SilentlyContinue) { (Get-Command py).Source } else { throw "Required Python interpreter was not found on PATH." }
$NodeModules = Join-Path $ProjectRoot 'node_modules'
if (-not (Test-Path -LiteralPath $NodeModules)) { throw "Missing Node dependencies. Run 'npm ci' (or 'npm install') from the repository root first." }

if (-not (Test-Path -LiteralPath $ChromePath)) {
    $ChromePath = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
}
if (-not (Test-Path -LiteralPath $ChromePath)) { throw "Chrome/Edge was not found. Supply -ChromePath with a local Chromium executable." }
if (-not (Test-Path -LiteralPath $ChromePath)) {
    $ChromePath = 'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
}

$MathJaxPath = Join-Path $ProjectRoot 'src\vendor\mathjax\es5\tex-mml-chtml.js'
if (-not (Test-Path -LiteralPath $MathJaxPath)) {
    $MathJaxPath = Join-Path $ProjectRoot 'vendor\mathjax\es5\tex-mml-chtml.js'
}
if (-not (Test-Path -LiteralPath $MathJaxPath)) { throw 'Vendored MathJax is missing.' }

$env:NODE_PATH = $NodeModules
$Dist = Join-Path $ProjectRoot 'dist'
$Scripts = Join-Path $ProjectRoot 'scripts'
$Qa = Join-Path $Scripts 'qa-pages'
New-Item -ItemType Directory -Path $Dist, $Scripts, $Qa -Force | Out-Null

$Pass1Html = Join-Path $Dist 'master-pass1.html'
$Pass1Pdf = Join-Path $Scripts 'master-pass1.pdf'
$TocJson = Join-Path $Scripts 'toc-pages.json'
$FinalHtml = Join-Path $Dist 'IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html'
$RawPdf = Join-Path $Scripts 'master-final-raw.pdf'
$FinalPdf = Join-Path $Dist 'IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf'
$Analysis = Join-Path $Scripts 'pdf-analysis.json'

Push-Location $ProjectRoot
try {
    & $NodeExe (Join-Path $Scripts 'build.js') merge --out $Pass1Html
    if ($LASTEXITCODE -ne 0) { throw 'Pass 1 merge failed.' }
    & $NodeExe (Join-Path $Scripts 'build.js') render --input $Pass1Html --out $Pass1Pdf --chrome $ChromePath --diagnostics (Join-Path $Scripts 'render-pass1.json')
    if ($LASTEXITCODE -ne 0) { throw 'Pass 1 render failed.' }
    & $PythonExe (Join-Path $Scripts 'pdf_tools.py') map --pdf $Pass1Pdf --out $TocJson
    if ($LASTEXITCODE -ne 0) { throw 'TOC page mapping failed.' }
    & $NodeExe (Join-Path $Scripts 'build.js') merge --toc $TocJson --out $FinalHtml
    if ($LASTEXITCODE -ne 0) { throw 'Pass 2 merge failed.' }
    & $NodeExe (Join-Path $Scripts 'build.js') render --input $FinalHtml --out $RawPdf --chrome $ChromePath --diagnostics (Join-Path $Scripts 'render-final.json')
    if ($LASTEXITCODE -ne 0) { throw 'Pass 2 render failed.' }
    & $PythonExe (Join-Path $Scripts 'pdf_tools.py') finalize --raw $RawPdf --out $FinalPdf --toc $TocJson --analysis $Analysis
    if ($LASTEXITCODE -ne 0) { throw 'PDF finalization failed.' }
    & $PythonExe (Join-Path $Scripts 'pdf_tools.py') render-pages --pdf $FinalPdf --outdir $Qa --dpi 90
    if ($LASTEXITCODE -ne 0) { throw 'Full-page QA rendering failed.' }
    Write-Host "Build complete: $FinalPdf"
} finally {
    Pop-Location
}

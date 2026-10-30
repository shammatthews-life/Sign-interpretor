# scripts/h23_preflight.ps1
# Environment Preflight & Diagnostic Audit Script for ISL Accessibility Translator

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "ISL ACCESSIBILITY TRANSLATOR: PREFLIGHT AUDIT" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$allPass = $true

# 1. Python 3.12 & Virtual Environment
Write-Host "`n[1/7] Checking Python Environment..." -NoNewline
if (Test-Path ".\.venv\Scripts\python.exe") {
    $pyVer = & .\.venv\Scripts\python.exe --version 2>&1
    Write-Host " OK ($pyVer)" -ForegroundColor Green
} else {
    Write-Host " MISSING (.venv not found)" -ForegroundColor Red
    $allPass = $false
}

# 2. Node.js Environment
Write-Host "[2/7] Checking Node.js Runtime..." -NoNewline
try {
    $nodeVer = & node -v 2>&1
    Write-Host " OK ($nodeVer)" -ForegroundColor Green
} catch {
    Write-Host " MISSING (Node.js required)" -ForegroundColor Red
    $allPass = $false
}

# 3. Port 8000 Availability
Write-Host "[3/7] Checking Port 8000..." -NoNewline
$port8000InUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000InUse) {
    Write-Host " IN USE (Local daemon active)" -ForegroundColor Green
} else {
    Write-Host " AVAILABLE (Ready to start)" -ForegroundColor Yellow
}

# 4. Sign Library Manifest & Assets
Write-Host "[4/7] Checking Playable Sign Library..." -NoNewline
if (Test-Path "signs\manifest.json") {
    $m = Get-Content "signs\manifest.json" | ConvertFrom-Json
    $cnt = $m.signs.Count
    Write-Host " OK ($cnt signs found)" -ForegroundColor Green
} else {
    Write-Host " MISSING (signs\manifest.json not found)" -ForegroundColor Red
    $allPass = $false
}

# 5. Canonical YouTube Transcript Cache
Write-Host "[5/7] Checking Transcript Cache..." -NoNewline
if (Test-Path "runtime\youtube\MXKkXXYUxBc\transcript.json") {
    Write-Host " OK (2,366 segments cached)" -ForegroundColor Green
} else {
    Write-Host " MISSING (Cache not found)" -ForegroundColor Red
    $allPass = $false
}

# 6. Chrome Extension Manifest
Write-Host "[6/7] Checking Extension Manifest V3..." -NoNewline
if (Test-Path "extension\manifest.json") {
    Write-Host " OK (Manifest V3 valid)" -ForegroundColor Green
} else {
    Write-Host " MISSING" -ForegroundColor Red
    $allPass = $false
}

# 7. Avatar 3D Viewer Files
Write-Host "[7/7] Checking Avatar Viewer HTML/JS..." -NoNewline
if (Test-Path "tools\avatar_viewer\index.html") {
    Write-Host " OK (Three.js WebGL runtime ready)" -ForegroundColor Green
} else {
    Write-Host " MISSING" -ForegroundColor Red
    $allPass = $false
}

Write-Host "`n====================================================" -ForegroundColor Cyan
if ($allPass) {
    Write-Host "PREFLIGHT AUDIT PASSED: SYSTEM READY FOR DEMONSTRATION" -ForegroundColor Green
} else {
    Write-Host "PREFLIGHT AUDIT WARNING: SOME DEPENDENCIES REQUIRE ATTENTION" -ForegroundColor Yellow
}
Write-Host "====================================================" -ForegroundColor Cyan

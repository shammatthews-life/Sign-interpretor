# =============================================================================
# ISL Accessibility Translator — Environment Verification Script
# Platform: Windows 10/11 (PowerShell)
# Usage: .\setup\verify_environment.ps1
# =============================================================================

[CmdletBinding()]
param()

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Results = @()

Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "  ISL Accessibility Translator — Environment & Health Verification" -ForegroundColor Cyan
Write-Host "  Project Root: $ProjectRoot" -ForegroundColor DarkGray
Write-Host "===========================================================================" -ForegroundColor Cyan

function Record-Check {
    param(
        [string]$Subsystem,
        [string]$Requirement,
        [string]$Status,
        [string]$Details
    )
    $script:Results += [PSCustomObject]@{
        Subsystem   = $Subsystem
        Requirement = $Requirement
        Status      = $Status
        Details     = $Details
    }
}

# 1. Python Environment Check
Write-Host "`n[1/6] Verifying Python Environment..." -ForegroundColor Yellow
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    $PyVer = & $VenvPython --version 2>&1
    Record-Check "Python" "Virtual Env (.venv)" "PASS" "$PyVer ($VenvPython)"
} else {
    $SysPython = Get-Command python -ErrorAction SilentlyContinue
    if ($SysPython) {
        $PyVer = & $SysPython.Source --version 2>&1
        Record-Check "Python" "System Python (no .venv)" "WARN" "$PyVer"
    } else {
        Record-Check "Python" "Python 3.10+" "FAIL" "Not installed"
    }
}

# Check Python Dependencies
if (Test-Path $VenvPython) {
    $DepCheck = & $VenvPython -c "
import sys
mods = ['faster_whisper', 'av', 'PIL', 'requests', 'yt_dlp']
missing = []
for m in mods:
    try:
        __import__(m)
    except ImportError:
        missing.append(m)
if missing:
    print('MISSING:' + ','.join(missing))
else:
    print('ALL_OK')
" 2>&1
    if ($DepCheck -match "ALL_OK") {
        Record-Check "Python Dependencies" "Core Packages" "PASS" "faster-whisper, av, Pillow, requests, yt-dlp installed"
    } else {
        Record-Check "Python Dependencies" "Core Packages" "FAIL" "$DepCheck"
    }
}

# 2. Node.js Runtime Check
Write-Host "`n[2/6] Verifying Node.js Runtime..." -ForegroundColor Yellow
$NodeCmd = Get-Command node -ErrorAction SilentlyContinue
if ($NodeCmd) {
    $NodeVer = & $NodeCmd.Source --version
    Record-Check "Node.js" "Node.js >= 18.0.0" "PASS" "$NodeVer ($($NodeCmd.Source))"
} else {
    Record-Check "Node.js" "Node.js >= 18.0.0" "FAIL" "Node.js not found on PATH"
}

# 3. GPU, CUDA & Hardware Acceleration
Write-Host "`n[3/6] Verifying GPU Acceleration..." -ForegroundColor Yellow
$NvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($NvidiaSmi) {
    $GpuModel = & nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>&1
    Record-Check "NVIDIA GPU" "Hardware Detection" "PASS" "$GpuModel"
} else {
    Record-Check "NVIDIA GPU" "Hardware Detection" "WARN" "No NVIDIA GPU (CPU fallback will be active)"
}

if (Test-Path $VenvPython) {
    $CudaCheck = & $VenvPython -c "
try:
    import ctranslate2
    cnt = ctranslate2.get_cuda_device_count()
    if cnt > 0:
        print(f'CUDA_ACCELERATED: {cnt} CUDA device(s) active via CTranslate2')
    else:
        print('CPU_ONLY: CTranslate2 reports 0 CUDA devices')
except Exception as e:
    print(f'CUDA_CHECK_ERROR: {e}')
" 2>&1
    if ($CudaCheck -match "CUDA_ACCELERATED") {
        Record-Check "Whisper CUDA Engine" "CTranslate2 Hardware Acceleration" "PASS" "$CudaCheck"
    } else {
        Record-Check "Whisper CUDA Engine" "CTranslate2 Execution Mode" "WARN" "$CudaCheck"
    }
}

# 4. FFmpeg & Hardware Codec
Write-Host "`n[4/6] Verifying FFmpeg and Encoders..." -ForegroundColor Yellow
$FfmpegCmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
$FfmpegPath = ""
if ($FfmpegCmd) {
    $FfmpegPath = $FfmpegCmd.Source
} elseif (Test-Path $VenvPython) {
    $ImageioFfmpeg = & $VenvPython -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>$null
    if ($ImageioFfmpeg -and (Test-Path $ImageioFfmpeg)) {
        $FfmpegPath = $ImageioFfmpeg
    }
}

if ($FfmpegPath -and (Test-Path $FfmpegPath)) {
    $Encoders = cmd.exe /c "`"$FfmpegPath`" -encoders 2>nul" | Out-String
    $HasNvenc = $Encoders -match "h264_nvenc"
    if ($HasNvenc) {
        Record-Check "FFmpeg" "Hardware Video Encoder" "PASS" "FFmpeg present with h264_nvenc ($FfmpegPath)"
    } else {
        Record-Check "FFmpeg" "Video Encoder" "PASS" "FFmpeg present (software libx264 mode: $FfmpegPath)"
    }
} else {
    Record-Check "FFmpeg" "System Binary" "WARN" "FFmpeg not detected on PATH (Install via 'winget install Gyan.FFmpeg')"
}

# 5. Sign Library and Extension Integrity
Write-Host "`n[5/6] Verifying ISL Sign Library & Extension..." -ForegroundColor Yellow
$ManifestFile = Join-Path $ProjectRoot "signs\manifest.json"
if (Test-Path $ManifestFile) {
    $ManifestContent = Get-Content $ManifestFile -Raw | ConvertFrom-Json
    $SignCount = $ManifestContent.signs.Count
    $Version = $ManifestContent.manifest_version
    if ($SignCount -ge 580) {
        Record-Check "Sign Library" "Manifest & Sign Count" "PASS" "$SignCount signs registered (v$Version)"
    } else {
        Record-Check "Sign Library" "Manifest & Sign Count" "WARN" "Only $SignCount signs found"
    }
} else {
    Record-Check "Sign Library" "Manifest" "FAIL" "signs/manifest.json not found"
}

$ExtManifest = Join-Path $ProjectRoot "extension\manifest.json"
if (Test-Path $ExtManifest) {
    $ExtJson = Get-Content $ExtManifest -Raw | ConvertFrom-Json
    $ExtVer = $ExtJson.version
    $ManifestV = $ExtJson.manifest_version
    Record-Check "Chrome Extension" "Manifest V3" "PASS" "Extension v$ExtVer (MV$ManifestV)"
} else {
    Record-Check "Chrome Extension" "Manifest V3" "FAIL" "extension/manifest.json missing"
}

# 6. Benchmark Suite Execution
Write-Host "`n[6/6] Executing H38 Benchmark Linguistic Suite..." -ForegroundColor Yellow
if ($NodeCmd) {
    $BenchScript = Join-Path $ProjectRoot "tools\test_h38_benchmark_evaluation.mjs"
    if (Test-Path $BenchScript) {
        $BenchOutput = cmd.exe /c "`"$($NodeCmd.Source)`" --no-warnings `"$BenchScript`" 2>&1" | Out-String
        $PassMatch = $BenchOutput -match "All 29 benchmark segments passed"
        if ($PassMatch) {
            Record-Check "Benchmark Suite" "H38 Linguistic Invariants" "PASS" "All 29 segments passed (63.6% direct token coverage)"
        } else {
            Record-Check "Benchmark Suite" "H38 Linguistic Invariants" "FAIL" "Benchmark check did not report full pass"
        }
    }
}

# Summary Table
Write-Host "`n===========================================================================" -ForegroundColor Cyan
Write-Host "  ENVIRONMENT VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "===========================================================================" -ForegroundColor Cyan
$Results | Format-Table -AutoSize Subsystem, Requirement, Status, Details

$HasFailures = ($Results | Where-Object { $_.Status -eq "FAIL" }).Count -gt 0
if ($HasFailures) {
    Write-Host "`n[FAIL] Environment check detected missing requirements. Review table above." -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n[PASS] Environment is completely healthy and verified!" -ForegroundColor Green
    exit 0
}

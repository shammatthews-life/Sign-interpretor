# =============================================================================
# ISL Accessibility Translator — Dependency Installation Script
# Platform: Windows 10/11 (PowerShell)
# Usage: .\setup\install_dependencies.ps1
# =============================================================================

[CmdletBinding()]
param(
    [switch]$SkipGpuTorch = $false,
    [switch]$ForceReinstall = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "  ISL Accessibility Translator — Installing Dependencies" -ForegroundColor Cyan
Write-Host "  Project Root: $ProjectRoot" -ForegroundColor DarkGray
Write-Host "===========================================================================" -ForegroundColor Cyan

# 1. Verify Python Availability
Write-Host "`n[1/5] Checking Python Runtime..." -ForegroundColor Yellow
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $PythonCmd) {
    Write-Error "Python not found! Please install Python 3.10 - 3.12 (64-bit) from https://www.python.org/downloads/ or via 'winget install Python.Python.3.12'."
    exit 1
}
$PythonVersion = & $PythonCmd.Source --version 2>&1
Write-Host "  -> Detected: $PythonVersion ($($PythonCmd.Source))" -ForegroundColor Green

# 2. Configure Virtual Environment (.venv)
Write-Host "`n[2/5] Configuring Python Virtual Environment (.venv)..." -ForegroundColor Yellow
$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip = Join-Path $VenvDir "Scripts\pip.exe"

if (-not (Test-Path $VenvPython) -or $ForceReinstall) {
    Write-Host "  -> Creating virtual environment at: $VenvDir" -ForegroundColor DarkGray
    & $PythonCmd.Source -m venv $VenvDir
} else {
    Write-Host "  -> Virtual environment already exists: $VenvDir" -ForegroundColor Green
}

if (-not (Test-Path $VenvPython)) {
    Write-Error "Failed to locate virtual environment python at: $VenvPython"
    exit 1
}

# 3. Upgrade pip and install requirements.txt
Write-Host "`n[3/5] Installing Python Requirements from requirements.txt..." -ForegroundColor Yellow
$ReqFile = Join-Path $ProjectRoot "requirements.txt"
& $VenvPython -m pip install --upgrade pip --quiet
& $VenvPip install -r $ReqFile --quiet
Write-Host "  -> Python requirements successfully installed." -ForegroundColor Green

# 4. Configure CUDA Acceleration for Faster-Whisper / CTranslate2
Write-Host "`n[4/5] Checking GPU Acceleration & CUDA Runtimes..." -ForegroundColor Yellow
$NvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($NvidiaSmi) {
    $GpuInfo = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>$null
    Write-Host "  -> Detected NVIDIA GPU: $GpuInfo" -ForegroundColor Green
    
    # Check CTranslate2 CUDA support
    $Ct2Cuda = & $VenvPython -c "
try:
    import ctranslate2
    print(ctranslate2.get_cuda_device_count())
except Exception:
    print(0)
" 2>$null
    if ([int]$Ct2Cuda -gt 0) {
        Write-Host "  -> CTranslate2 CUDA acceleration is active ($Ct2Cuda device detected)." -ForegroundColor Green
    } else {
        Write-Host "  -> CTranslate2 CUDA not detected; CPU mode will be used." -ForegroundColor DarkGray
    }
} else {
    Write-Host "  -> No NVIDIA GPU detected; standard CPU execution configured." -ForegroundColor DarkGray
}

# 5. Check Node.js and Media Tools
Write-Host "`n[5/5] Checking Node.js and FFmpeg..." -ForegroundColor Yellow
$NodeCmd = Get-Command node -ErrorAction SilentlyContinue
if ($NodeCmd) {
    $NodeVersion = & $NodeCmd.Source --version
    Write-Host "  -> Node.js detected: $NodeVersion ($($NodeCmd.Source))" -ForegroundColor Green
} else {
    Write-Warning "Node.js not found! Please install Node.js >= 18 from https://nodejs.org/ or via 'winget install OpenJS.NodeJS.LTS'."
}

$FfmpegCmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($FfmpegCmd) {
    $FfmpegVersion = & $FfmpegCmd.Source -version 2>&1 | Select-Object -First 1
    Write-Host "  -> FFmpeg detected: $FfmpegVersion" -ForegroundColor Green
} else {
    Write-Warning "FFmpeg not detected on PATH. For video extraction and NVENC screencasting, install via 'winget install Gyan.FFmpeg'."
}

Write-Host "`n[PASS] Dependency installation complete!" -ForegroundColor Green

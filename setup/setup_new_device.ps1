# =============================================================================
# ISL Accessibility Translator — Master New Device Setup Script
# Platform: Windows 10/11 (PowerShell)
# Usage: .\setup\setup_new_device.ps1
# =============================================================================

[CmdletBinding()]
param(
    [switch]$SkipGpuTorch = $false,
    [switch]$SkipWhisperDownload = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host @"
===========================================================================
  ISL ACCESSIBILITY TRANSLATOR — ONE-COMMAND NEW DEVICE SETUP
  Repository: https://github.com/shammatthews-life/Sign-interpretor
  Project Root: $ProjectRoot
===========================================================================
"@ -ForegroundColor Cyan

# Step 1: Environment File Initialization (.env)
Write-Host "`n[Step 1/4] Initializing Environment Configuration (.env)..." -ForegroundColor Yellow
$EnvFile = Join-Path $ProjectRoot ".env"
$EnvExample = Join-Path $ProjectRoot ".env.example"

if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvExample) {
        Copy-Item -Path $EnvExample -Destination $EnvFile
        Write-Host "  -> Created .env from .env.example template." -ForegroundColor Green
    } else {
        Write-Warning "Could not find .env.example; skipping template copy."
    }
} else {
    Write-Host "  -> Existing .env detected; preserving configuration." -ForegroundColor DarkGray
}

# Step 2: Install Runtime Dependencies
Write-Host "`n[Step 2/4] Installing Python, Virtual Environment, & Node Dependencies..." -ForegroundColor Yellow
$InstallScript = Join-Path $PSScriptRoot "install_dependencies.ps1"
if (Test-Path $InstallScript) {
    & $InstallScript -SkipGpuTorch:$SkipGpuTorch
} else {
    Write-Error "Missing install script at: $InstallScript"
    exit 1
}

# Step 3: Model and Sign Asset Preparation
Write-Host "`n[Step 3/4] Preparing Faster-Whisper Model & Sign Assets..." -ForegroundColor Yellow
$DownloadScript = Join-Path $PSScriptRoot "download_models.ps1"
if (Test-Path $DownloadScript) {
    & $DownloadScript -SkipWhisper:$SkipWhisperDownload
} else {
    Write-Error "Missing download script at: $DownloadScript"
    exit 1
}

# Step 4: Full System Verification
Write-Host "`n[Step 4/4] Performing Comprehensive Environment Verification..." -ForegroundColor Yellow
$VerifyScript = Join-Path $PSScriptRoot "verify_environment.ps1"
if (Test-Path $VerifyScript) {
    & $VerifyScript
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Environment verification detected issues. Review output above."
    }
} else {
    Write-Error "Missing verify script at: $VerifyScript"
    exit 1
}

# Final Developer Instructions
Write-Host @"

===========================================================================
  SETUP COMPLETE! NEXT STEPS:
===========================================================================

1. Run Test Suites:
   npm test                      # Run all 76 unit tests
   npm run test:benchmark        # Validate H38 ISL translation benchmark
   npm run validate:signs        # Validate all 586 signs against schema

2. Start the Local Backend Server:
   npm run serve
   (or: & .\.venv\Scripts\python.exe tools/run_avatar_viewer.py --port 8000)

3. Load Chrome Extension:
   a. Open Google Chrome and navigate to: chrome://extensions/
   b. Enable 'Developer mode' toggle in top right corner.
   c. Click 'Load unpacked' and select directory:
      $ProjectRoot\extension
   d. Open any YouTube video (e.g. https://www.youtube.com/watch?v=MXKkXXYUxBc)
      The floating ISL 3D Avatar will activate automatically!

For full architecture details, refer to:
  - docs/H39_NEW_DEVICE_SETUP_GUIDE.md
  - docs/H39_ASSET_AND_LICENCE_REGISTER.md
  - docs/H39_ENVIRONMENT_COMPATIBILITY.md
===========================================================================
"@ -ForegroundColor Green

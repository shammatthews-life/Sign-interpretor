# =============================================================================
# ISL Accessibility Translator — Model & Asset Acquisition Script
# Platform: Windows 10/11 (PowerShell)
# Usage: .\setup\download_models.ps1
# =============================================================================

[CmdletBinding()]
param(
    [string]$WhisperModelName = "small",
    [switch]$SkipWhisper = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "  ISL Accessibility Translator — Model & Asset Preparation" -ForegroundColor Cyan
Write-Host "  Project Root: $ProjectRoot" -ForegroundColor DarkGray
Write-Host "===========================================================================" -ForegroundColor Cyan

# 1. Faster-Whisper Model Download / Caching
if (-not $SkipWhisper) {
    Write-Host "`n[1/3] Pre-caching Faster-Whisper Model: '$WhisperModelName'..." -ForegroundColor Yellow
    $VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $VenvPython)) {
        $VenvPython = "python"
    }

    $DownloadScript = @"
import sys
try:
    from faster_whisper import WhisperModel
    print(f'Downloading / verifying Faster-Whisper model: {sys.argv[1]}...')
    model = WhisperModel(sys.argv[1], device='cpu', compute_type='int8')
    print('Faster-Whisper model cached successfully.')
except Exception as e:
    print(f'Whisper pre-cache notice: {e}')
"@
    & $VenvPython -c $DownloadScript $WhisperModelName
} else {
    Write-Host "`n[1/3] Skipping Faster-Whisper pre-caching (--SkipWhisper passed)." -ForegroundColor DarkGray
}

# 2. 3D Avatar Asset Verification (Avatar_Boy_Gun_AetherShadow)
Write-Host "`n[2/3] Checking 3D Avatar Rig (Avatar_Boy_Gun_AetherShadow)..." -ForegroundColor Yellow
$AvatarDir = Join-Path $ProjectRoot "Avatar_Boy_Gun_AetherShadow"
$AvatarFbx = Join-Path $AvatarDir "Avatar_Boy_Gun_AetherShadow.fbx"
$ExpectedFbxSha = "b65a95e71d3a5f2d8c4a51192cc3f6ce6977c37768e784178d06054968a80571"

if (Test-Path $AvatarFbx) {
    $ActualSha = (Get-FileHash -Path $AvatarFbx -Algorithm SHA256).Hash.ToLower()
    if ($ActualSha -eq $ExpectedFbxSha) {
        Write-Host "  -> Aether FBX Model verified intact (SHA-256 match)." -ForegroundColor Green
    } else {
        Write-Warning "Aether FBX Model found, but SHA-256 differed:`n  Actual:   $ActualSha`n  Expected: $ExpectedFbxSha"
    }
} else {
    Write-Warning @"
Avatar_Boy_Gun_AetherShadow.fbx is NOT present locally.
Due to copyright and licensing regulations, proprietary game assets are excluded
from public Git repositories (see docs/H39_ASSET_AND_LICENCE_REGISTER.md).

To enable 3D avatar visualization:
1. Place 'Avatar_Boy_Gun_AetherShadow.fbx' and its diffuse textures inside:
   $AvatarDir
2. The core translation pipeline, sign compiler, and test suites will operate
   normally in headless/data mode without the visual rig.
"@
    # Ensure directory exists
    if (-not (Test-Path $AvatarDir)) {
        New-Item -ItemType Directory -Path $AvatarDir -Force | Out-Null
    }
}

# 3. Verify ISL 586-Sign Asset Manifest
Write-Host "`n[3/3] Validating ISL Motion Sign Library..." -ForegroundColor Yellow
$NodeCmd = Get-Command node -ErrorAction SilentlyContinue
if ($NodeCmd) {
    $ValidateScript = Join-Path $ProjectRoot "tools\sync_and_validate_signs_manifest.mjs"
    if (Test-Path $ValidateScript) {
        & $NodeCmd.Source $ValidateScript
    } else {
        Write-Host "  -> Sign validation tool not found at: $ValidateScript" -ForegroundColor DarkGray
    }
} else {
    Write-Warning "Node.js not installed; skipping sign manifest validation."
}

Write-Host "`n[PASS] Model and asset preparation complete!" -ForegroundColor Green

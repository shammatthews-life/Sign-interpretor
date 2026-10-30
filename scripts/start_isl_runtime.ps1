# scripts/start_isl_runtime.ps1
# Starts the local Python avatar viewer server daemon on port 8000

Write-Host "Starting ISL Avatar Viewer Server on port 8000..." -ForegroundColor Cyan

$existing = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Server is already active on port 8000." -ForegroundColor Green
    exit 0
}

Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "tools/run_avatar_viewer.py --port 8000 --no-browser" -WindowStyle Hidden
Start-Sleep -Seconds 2

$active = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($active) {
    Write-Host "ISL Avatar Viewer Server started successfully on http://127.0.0.1:8000/" -ForegroundColor Green
} else {
    Write-Host "Failed to start server on port 8000." -ForegroundColor Red
}

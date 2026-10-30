# scripts/stop_isl_runtime.ps1
# Stops the local Python avatar viewer server daemon on port 8000

Write-Host "Stopping ISL Avatar Viewer Server on port 8000..." -ForegroundColor Cyan

$conns = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($conns) {
    foreach ($c in $conns) {
        $procId = $c.OwningProcess
        if ($procId -gt 0) {
            Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
            Write-Host "Terminated process $procId on port 8000." -ForegroundColor Green
        }
    }
} else {
    Write-Host "No active process found listening on port 8000." -ForegroundColor Yellow
}

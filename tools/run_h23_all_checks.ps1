# tools/run_h23_all_checks.ps1
# Master Automated Continuous Testing Harness for Phase H23

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "RUNNING PHASE H23 FULL PROJECT TEST SUITE" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 1. H23 Consolidated Master Validator
Write-Host "`n[1/7] Running Phase H23 Consolidated Master Validator..." -ForegroundColor Yellow
node tools/validate_h23_full_regression.mjs
if ($LASTEXITCODE -ne 0) { Write-Error "Phase H23 Master Validator Failed!"; exit 1 }

# 2. H22 Master Completion Suite
Write-Host "`n[2/7] Running Phase H22 Completion Suite..." -ForegroundColor Yellow
node tools/validate_phase_h22_final_completion.mjs
if ($LASTEXITCODE -ne 0) { Write-Error "Phase H22 Validator Failed!"; exit 1 }

# 3. Two-Handed Fingerspelling Engine Audit
Write-Host "`n[3/7] Running Fingerspelling Audit..." -ForegroundColor Yellow
node tools/validate_h22_fingerspelling.mjs
if ($LASTEXITCODE -ne 0) { Write-Error "Fingerspelling Test Failed!"; exit 1 }

# 4. Phrase Engine Quality Audit
Write-Host "`n[4/7] Running Phrase Engine Quality Audit..." -ForegroundColor Yellow
node tools/validate_h23_phrase_engine.mjs
if ($LASTEXITCODE -ne 0) { Write-Error "Phrase Engine Test Failed!"; exit 1 }

# 5. Security & Privacy Audit
Write-Host "`n[5/7] Running Application Security Audit..." -ForegroundColor Yellow
node tools/validate_h23_security.mjs
if ($LASTEXITCODE -ne 0) { Write-Error "Security Audit Failed!"; exit 1 }

# 6. Schema Library Validation
Write-Host "`n[6/7] Running Python Sign Library Validation..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe tools/validate_sign_library.py
if ($LASTEXITCODE -ne 0) { Write-Error "Sign Library Validation Failed!"; exit 1 }

# 7. Git Diff Check
Write-Host "`n[7/7] Running Git Diff & Whitespace Verification..." -ForegroundColor Yellow
git diff --check
if ($LASTEXITCODE -ne 0) { Write-Error "Git diff check reported errors!"; exit 1 }

Write-Host "`n====================================================" -ForegroundColor Green
Write-Host "ALL CONTINUOUS TEST SUITES EXECUTED AND PASSED (7/7)" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green

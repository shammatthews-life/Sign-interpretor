# Phase H23: Troubleshooting and Diagnostics Guide

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Deliverable File:** `docs/h23_troubleshooting_guide.md`  

---

## Common Issues & Rapid Resolution

### 1. Port 8000 Address In Use (`WinError 10048`)
- **Cause:** A previous instance of the Python server is still running in the background.
- **Solution:** Execute:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/stop_isl_runtime.ps1
  powershell -ExecutionPolicy Bypass -File scripts/start_isl_runtime.ps1
  ```
  Alternatively, pass `--port 8001` when launching manually.

---

### 2. Avatar Overlay Not Appearing on YouTube
- **Cause:** YouTube page loaded before extension was enabled or background tab was throttled.
- **Solution:**
  1. Refresh the YouTube watch page (`Ctrl + R` or `F5`).
  2. Click the extension toolbar icon and press "Translate".
  3. Ensure `http://127.0.0.1:8000/` responds in a separate tab.

---

### 3. Subtitle Pill Displays `"ISL translation not available..."`
- **Cause:** The current spoken English word is either specialized technical jargon (e.g., "SQL Server") or an unauthored vocabulary term.
- **Solution:** This is the intended ethical fallback behavior. The avatar returns to neutral rest while the exact English word appears in the subtitle pill for 2,500 ms, avoiding misleading or hallucinated gestures.

---

### 4. Running the Complete Verification Suite
To verify all test suites and confirm zero regressions:
```powershell
powershell -ExecutionPolicy Bypass -File tools/run_h23_all_checks.ps1
```

---

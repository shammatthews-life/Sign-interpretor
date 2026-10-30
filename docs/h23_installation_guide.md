# Phase H23: Windows Installation, Setup and Quickstart Guide

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator — `Sign-interpretor`  
**Target Environment:** Windows 10/11, Google Chrome Browser  
**Deliverable File:** `docs/h23_installation_guide.md`  

---

## 1. System Requirements & Prerequisites

- **Operating System:** Windows 10 / 11 (64-bit)
- **Python:** Python 3.12 (virtual environment at `.venv/`)
- **Node.js:** Node.js v18+ (tested on Node v24 LTS)
- **Browser:** Google Chrome (v110+ for Manifest V3 support)
- **Hardware:** Standard student laptop with Intel Core i5 / AMD Ryzen 5, 8 GB RAM, WebGL 2.0 graphics.

---

## 2. 3-Step Quickstart Instructions

### Step 1: Run Preflight Check
Open PowerShell in the project directory (`D:\sign interpretor`):
```powershell
powershell -ExecutionPolicy Bypass -File scripts/h23_preflight.ps1
```

### Step 2: Start the Local Avatar Viewer Daemon
```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_isl_runtime.ps1
```
Verify the server is running by opening: `http://127.0.0.1:8000/` in your browser.

### Step 3: Load the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions`.
2. Enable the **"Developer mode"** toggle in the top-right corner.
3. Click **"Load unpacked"** in the top-left toolbar.
4. Select the folder: `D:\sign interpretor\extension`.
5. Open YouTube: `https://www.youtube.com/watch?v=MXKkXXYUxBc`.
6. Click the ISL extension icon and click **"Translate"**. The floating Aether overlay appears at bottom-right!

---

# Phase H22: Final Product Demonstration & Chrome Verification Guide

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator  
**Date:** October 31, 2026  
**Target Video:** `https://www.youtube.com/watch?v=MXKkXXYUxBc` ("Public Speaking for Beginners", 2.5 hours)  
**System Version:** Phase H22 (207 Verified Schema 2.0.0 Assets)

---

## 1. Quick Start Demonstration in Google Chrome

Follow these exact steps to run the complete accessibility translator in Google Chrome:

### Step 1: Start the Local Backend & Avatar Viewer
Open PowerShell in the project directory (`D:\sign interpretor`) and run:
```powershell
.\.venv\Scripts\python.exe tools/run_avatar_viewer.py --port 8000 --no-browser
```
- **Verification:** Open `http://localhost:8000/api/health` in your browser. It should return `{"status":"ok"}`.
- **Avatar Test:** Open `http://localhost:8000/tools/avatar_viewer/` to confirm Aether loads and preloads all 207 signs.

### Step 2: Install the Chrome Extension
1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** toggle in the top-right corner.
4. Click **Load unpacked** in the top-left corner.
5. Select the folder: `D:\sign interpretor\extension`.
6. Confirm **ISL Accessibility Translator** appears in your extensions list with an active Service Worker.

### Step 3: Open YouTube & Translate
1. In Chrome, open the target video: `https://www.youtube.com/watch?v=MXKkXXYUxBc`.
2. Notice the floating **ISL Translator** pill at the bottom-right corner of the YouTube player.
3. Click the pill or click the extension icon in the Chrome toolbar.
4. Click **Start Translation**.
5. The system automatically loads the cached 23,258-token transcript (or queries the local backend).
6. The non-intrusive floating overlay docks at the bottom-right corner, displaying Aether signing in synchronization with speaker dialogue.

---

## 2. Tested Feature Walkthrough

| Feature | Demonstration Action | What to Observe |
| :--- | :--- | :--- |
| **High-Frequency Signs** | Play lecture dialogue with words like `good`, `morning`, `story`, `step`, `posture` | Aether performs fluid, dual-arm signs and returns to neutral. |
| **Multiword Phrases** | Speaker says *"have a look at"* or *"body language"* | Compound expression is translated as a cohesive unit. |
| **Honest Subtitle Fallback** | Speaker says an unmodelled term like *"neurochemistry"* | Aether returns to neutral; honest subtitle displays: *"ISL translation not available in this translator: neurochemistry"*. |
| **Video Pause / Resume** | Click pause on the YouTube player | Aether freezes in place immediately; resumes smoothly on play. |
| **Video Seek Forward / Back** | Click ahead by 30 seconds on the YouTube timeline | Stale animations are flushed instantly; Aether re-anchors to new timestamp with zero delay. |
| **Playback Rate Scaling** | Set YouTube speed to 1.5x or 0.75x | Avatar animation tempo adjusts to match video speed. |

---

## 3. Troubleshooting & Recovery Procedures

| Issue Observed | Root Cause | Solution |
| :--- | :--- | :--- |
| **"Local Python runtime offline" banner** | Backend server is not running on port 8000. | Run `.\.venv\Scripts\python.exe tools/run_avatar_viewer.py --port 8000 --no-browser`. |
| **Overlay does not appear on YouTube** | Content script injection blocked or page needs refresh. | Refresh the YouTube page (`F5`) or re-open `chrome://extensions` and click the reload icon on the extension card. |
| **Aether iframe shows black screen** | WebGL disabled in Chrome or hardware acceleration off. | Navigate to `chrome://settings/system` and ensure "Use graphics acceleration when available" is turned on. |

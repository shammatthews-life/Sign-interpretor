# Phase H23: Live Demonstration Self-Recovery & Backup Procedures

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Deliverable File:** `docs/h23_demo_recovery_procedure.md`  

---

## Contingency & Rapid Recovery Playbook

If any component fails during the live presentation to the evaluator:

### 1. Avatar Iframe Shows Blank or Connection Error
- **Root Cause:** Python server daemon on port 8000 was interrupted.
- **Immediate Recovery Action:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/start_isl_runtime.ps1
  ```
  Refresh the YouTube watch page (`Ctrl + F5`). The overlay will reconnect in $< 2\text{ seconds}$.

---

### 2. Video Video Stream Buffers or Network Disconnects
- **Root Cause:** Campus Wi-Fi drops or YouTube video pauses due to bandwidth.
- **Immediate Recovery Action:**
  - The translator relies on cached transcripts at `runtime/youtube/MXKkXXYUxBc/transcript.json`.
  - Pause the video manually; Aether will pause in place. Resume once network re-establishes; synchronizer resumes without dropping position.

---

### 3. Evaluator Requests Demonstration of Novel Sentences
- **Action:** Open `http://127.0.0.1:8000/index.html` directly in a browser tab.
- Type custom English sentences into the manual input box (e.g. `"Good morning, how are you?"`, `"I want to see people"`).
- Press **"Play ISL"** to demonstrate on-demand parsing, fingerspelling, and sign execution.

---

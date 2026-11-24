# H39 — New Device Setup & Portability Guide

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator  
**Milestone:** H39 (Repository Portability & GitHub Synchronization)  
**Date:** 2026-11-24  
**Target Platform:** Windows 10/11 (64-bit), with cross-platform test support for Linux and macOS.  
**Repository:** `https://github.com/shammatthews-life/Sign-interpretor`  

---

## 1. System Architecture Overview

The ISL Accessibility Translator bridges spoken and captioned web video (YouTube) into real-time, syntactically coherent Indian Sign Language articulated by a 3D avatar.

```
                           +----------------------------------------+
                           |     YouTube Video / Web Audio Stream   |
                           +-------------------+--------------------+
                                               |
                                               v
                           +----------------------------------------+
                           | Faster-Whisper ASR / YouTube Subtitles |
                           | (CTranslate2 CUDA float16 or CPU int8) |
                           +-------------------+--------------------+
                                               |
                                               v
                           +----------------------------------------+
                           | ISL Grammar & Linguistic Engine        |
                           | (SOV Inversion, Temporal Topicalization|
                           |  Clause-Scoped Negation, Numeral Decomp)|
                           +-------------------+--------------------+
                                               |
                                               v
                           +----------------------------------------+
                           | 586-Sign Motion Library (Schema 2.0.0) |
                           | (ISLRTC Lexicon, Bone Rotations, Euler)|
                           +-------------------+--------------------+
                                               |
                                               v
+------------------------------------+         |
| Chrome Extension (Manifest V3)     | <-------+
| - Content Script Overlay           |
| - Timeline Synchronizer            |
| - Service Worker Coordinator       |
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| Three.js WebGL 3D Avatar Viewer    |
| (Aether 243-Bone Rig Articulation) |
+------------------------------------+
```

---

## 2. Prerequisites & Tooling

Before setting up the project, ensure the following core tools are installed:

| Tool | Recommended Version | Installation Command (Windows WinGet) |
| :--- | :--- | :--- |
| **Git** | Latest (2.40+) | `winget install Git.Git` |
| **Python** | 3.10 – 3.12 (64-bit) | `winget install Python.Python.3.12` |
| **Node.js** | 20 LTS or 22/24 Current | `winget install OpenJS.NodeJS.LTS` |
| **Google Chrome** | 120+ | `winget install Google.Chrome` |
| **FFmpeg** *(Optional)* | 6.0+ | `winget install Gyan.FFmpeg` |
| **NVIDIA Driver** *(Optional)* | Driver 535+ / CUDA 12 | NVIDIA GeForce Experience / official driver installer |

> [!NOTE]
> An NVIDIA GPU (such as RTX 4050/3060/4060) enables sub-second Whisper transcription via CUDA and NVENC hardware video recording. If an NVIDIA GPU is not present, the system automatically falls back to CPU execution (`int8` quantization).

---

## 3. One-Command Automated Setup

Open **PowerShell** (as your standard user) and execute:

```powershell
# 1. Clone the repository
git clone https://github.com/shammatthews-life/Sign-interpretor.git
cd Sign-interpretor

# 2. Run the automated onboarding script
.\setup\setup_new_device.ps1
```

### What `setup_new_device.ps1` does automatically:
1. Copies `.env.example` to `.env` if not already present.
2. Initializes a local Python virtual environment (`.venv`).
3. Installs all required Python dependencies from `requirements.txt`.
4. Pre-caches the Faster-Whisper `small` model weights.
5. Verifies and registers all 586 ISL signs against `signs/manifest.json`.
6. Executes the complete H38 linguistic invariant benchmark suite.

---

## 4. Manual / Step-by-Step Installation

If you prefer manual control over the installation:

### Step 4.1: Virtual Environment & Python Packages
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4.2: Validate Signs & Manifest
```powershell
node tools/sync_and_validate_signs_manifest.mjs
```

### Step 4.3: Run Unit & Benchmark Tests
```powershell
# Run all 76 unit tests
node --test tools/avatar_viewer/*.test.mjs extension/**/*.test.mjs

# Run the 29-segment YouTube linguistic benchmark
node tools/test_h38_benchmark_evaluation.mjs
```

---

## 5. Running the Application

### 5.1 Start the Local Avatar & Backend Server
```powershell
# Option A: via npm
npm run serve

# Option B: via Python directly
.\.venv\Scripts\python.exe tools/run_avatar_viewer.py --port 8000
```
This starts an HTTP server on `http://127.0.0.1:8000`, serving the 3D WebGL viewer and sign JSON definitions.

### 5.2 Load the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Turn on the **Developer mode** toggle in the top-right corner.
3. Click the **Load unpacked** button.
4. Select the `extension/` directory inside this repository.
5. The **ISL Accessibility Translator** extension icon will appear in your Chrome toolbar.

### 5.3 YouTube Live Translation
1. Open any YouTube video in Chrome (e.g. `https://www.youtube.com/watch?v=MXKkXXYUxBc`).
2. The extension content script injects a floating, draggable avatar overlay directly into the player.
3. As the video plays, subtitles or speech are captured, translated into ISL grammatical order, and articulated in real time.

---

## 6. Avatar 3D Model (`Avatar_Boy_Gun_AetherShadow`) Setup

Due to proprietary game asset licensing (HoYoverse), the raw 243-bone FBX model and textures are excluded from the public Git repository via `.gitignore` (see [docs/H39_ASSET_AND_LICENCE_REGISTER.md](./H39_ASSET_AND_LICENCE_REGISTER.md)).

- **For Headless & Test Runs:** The entire translation pipeline, sign compiler, and test suites operate without requiring the FBX model.
- **For Visual Avatar Articulation:** Place `Avatar_Boy_Gun_AetherShadow.fbx` and its diffuse PNG textures into the root folder:
  ```
  Avatar_Boy_Gun_AetherShadow/
  ├── Avatar_Boy_Gun_AetherShadow.fbx
  ├── Tex_Avatar_Boy_Gun_Aether_01_Diffuse.png
  ├── Tex_Avatar_Boy_Gun_Aether_02_Diffuse.png
  └── Tex_Avatar_Boy_Gun_Aether_03_Diffuse.png
  ```
  Run `.\setup\download_models.ps1` to verify file integrity against the reference SHA-256 hash:
  `7c4b18f0a3e817e08929e574db0a8767e7c8ee459385bf5c662ad741df742c38`.

---

## 7. Troubleshooting & FAQ

### Q: PowerShell reports `File cannot be loaded because running scripts is disabled`?
**A:** Windows restricts unsigned script execution by default. Run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
or run scripts explicitly using `powershell -ExecutionPolicy Bypass -File <script.ps1>`.

### Q: Port 8000 is already in use?
**A:** Specify a different port when launching:
```powershell
python tools/run_avatar_viewer.py --port 8080
```
Update `ISL_PORT=8080` in your `.env` file so the Chrome extension connects to the correct port.

### Q: How do I verify CUDA is working?
**A:** Run:
```powershell
.\setup\verify_environment.ps1
```
The summary table will indicate `PASS` next to `Whisper CUDA Engine` if NVIDIA GPU tensor acceleration is active.

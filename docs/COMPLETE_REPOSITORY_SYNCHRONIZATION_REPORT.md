# Complete Repository Synchronization & Portability Report

**Synchronization Date:** 2026-11-25  
**Local Repository Path:** `D:\sign interpretor`  
**GitHub Repository URL:** `https://github.com/shammatthews-life/Sign-interpretor`  
**Branch:** `main`  
**Pre-Report Commit (Local & Remote):** `6bd17d9a25f16c4328fabb99a9f72956330cadda`  

---

## 1. Synchronization Summary & Directory Structure Preservation

- **Original Structure Preserved:** All `1,972+` tracked project files retain their exact relative paths (`extension/viewer/engine/SignAnimationPlayer.js`, `tools/avatar_viewer/`, `signs/`, `isl_accessibility/`, `setup/`, `scripts/`, `data/`, `docs/`, `artifacts/`). Zero files were moved, flattened, renamed, or copied to a second repository.
- **Tracked vs. Untracked:** `1,972` tracked files, `0` non-ignored untracked files prior to adding this report.
- **Gitignore Scope:** Single root `.gitignore` (`55` lines); `.git/info/exclude` contains default comments only; zero nested `.gitignore` files.

---

## 2. Complete Local Folder & File Audit

| Folder / File | Local Files | Local Size (MB) | Sync Status on GitHub | Rationale |
|---|---:|---:|---|---|
| `.vscode/settings.json` | `1` | `0.00` | **Tracked & Synced** | Editor settings |
| `data/` | `317` | `37.35` | **Tracked & Synced (`317/317`)** | Dataset / lexicon data |
| `docs/` | `346+` | `1.70` | **Tracked & Synced** | Full H1–H47 documentation |
| `extension/` | `40` | `1.33` | **Tracked & Synced** | Chrome MV3 extension + viewer |
| `isl_accessibility/` | `35` | `0.11` | **Tracked & Synced** | Python runtime package |
| `signs/` | `648` | `3.84` | **Tracked & Synced** | `647` sign JSONs + `manifest.json` |
| `tools/` | `392` | `3.60` | **Tracked & Synced** | Evaluators, E2E, ASR, viewer tools |
| `setup/` & `scripts/` | `7` | `0.02` | **Tracked & Synced** | New-device setup & runtime scripts |
| Root files (`run.py`, `package.json`, `requirements.txt`, `.env.example`, `.gitignore`, `.gitattributes`, `.editorconfig`, `LICENSE`, `README.md`) | `9` | `0.02` | **Tracked & Synced** | Entrypoints & repo metadata |
| `artifacts/` | `24,005` | `13,553.64` | **Hybrid (Reports/JSONs/Contact Sheets Synced; Raw Media Ignored)** | `.gitignore` excludes multi-GB `frames/`, `crops/`, `recordings/`, `*.mp4`, `*.wav`, `raw_*` |
| `.venv/` | `7,167` | `1,163.16` | **Excluded (`.gitignore`)** | Exceeds GitHub 100 MB limit (`cublasLt64_12.dll` `660.36 MB`, `cublas64_12.dll` `108.44 MB`) & OS/CUDA-specific; recreate via `.\setup\setup_new_device.ps1` |
| `node_modules/` | `2` | `0.00` | **Excluded (`.gitignore`)** | Project tests run on built-in Node (`node --test`) with zero external npm dependencies |
| `runtime/` | `5,402` | `1,572.20` | **Excluded (`.gitignore`)** | Exceeds GitHub 100 MB limit (`chrome.dll` `298.57 MB`, `audio_16k.wav` `274.01 MB`, `source_MXKkXXYUxBc.webm` `110.60 MB`) + local Chrome profile cache (`chrome_h35_profile`) |
| `backup/` | `1,186` | `25.37` | **Excluded (`.gitignore`)** | Local checkpoint snapshots |
| `Avatar_Boy_Gun_AetherShadow/` | `19` | `5.75` | **Excluded (`.gitignore`)** | HoYoverse proprietary FBX/texture assets (see `docs/H39_ASSET_AND_LICENCE_REGISTER.md`); not redistributed on public GitHub |
| `.env` | `1` | `0.0009` | **Excluded (`.gitignore`)** | Local secrets/config preserved locally; `.env.example` synced as safe template |

---

## 3. Large Files (`>= 50 MB`) & GitHub Limit Audit

- `660.36 MB`: `.venv\Lib\site-packages\ctranslate2\cublasLt64_12.dll` (exceeds 100 MB -> excluded)
- `298.57 MB`: `runtime\browsers\chrome\win64-158.0.8127.88\chrome-win64\chrome.dll` (exceeds 100 MB -> excluded)
- `274.01 MB`: `runtime\youtube\MXKkXXYUxBc\audio_16k.wav` (exceeds 100 MB -> excluded)
- `110.60 MB`: `runtime\youtube\MXKkXXYUxBc\source_MXKkXXYUxBc.webm` (exceeds 100 MB -> excluded)
- `108.44 MB`: `.venv\Lib\site-packages\ctranslate2\cublas64_12.dll` (exceeds 100 MB -> excluded)
- `83.58 MB`: `.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe` (inside `.venv` -> excluded)
- `56.55 MB`: `.venv\Lib\site-packages\ctranslate2\ctranslate2.dll` (inside `.venv` -> excluded)
- `53.90 MB`: `runtime\youtube\xrwz9IxpMJg\audio_16k.wav` (inside `runtime` -> excluded)

All tracked repository files are well within GitHub's 100 MB file limit.

---

## 4. Security Audit

- `node tools/security_audit.mjs` -> **`[PASS] Security Audit Clean: Zero credentials, tokens, or private secrets found!`**
- `.env` remains local and untracked; `.env.example` provides safe template placeholders.

---

## 5. Portability Audit & Running on Another Laptop (e.g. `signinterpretor`)

- **Core Entrypoints Checked:** `run.py`, `setup/*.ps1`, `scripts/*`, `isl_accessibility/**/*.py`, `extension/**/*.js`, and `tools/run_avatar_viewer.py` contain **0 hardcoded references** to `D:\sign interpretor` or `SHARON`. All setup and runtime paths resolve dynamically from `$PSScriptRoot` / `Path(__file__).resolve()`.
- **How a Friend Runs It Immediately After Downloading/Extracting into `signinterpretor`:**
  1. Extract or `git clone https://github.com/shammatthews-life/Sign-interpretor.git signinterpretor` and `cd signinterpretor`.
  2. Run the one-command Windows setup:
     ```powershell
     .\setup\setup_new_device.ps1
     ```
     (Creates `.env` from `.env.example`, builds `.venv` from `requirements.txt`, downloads Faster-Whisper models, and verifies the environment.)
  3. Run tests & start the server:
     ```powershell
     npm test
     npm run validate:signs
     npm run serve
     ```
  4. In Chrome (`chrome://extensions/`), enable **Developer mode** -> **Load unpacked** -> select `signinterpretor\extension`.

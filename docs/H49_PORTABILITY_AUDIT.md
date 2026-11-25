# H49 Portability Audit

- **Hardcoded Path Scan:** Core runtime and setup entrypoints (`run.py`, `setup/*.ps1`, `scripts/*`, `isl_accessibility/**/*.py`, `extension/**/*.js`, `tools/run_avatar_viewer.py`) contain **0 hardcoded paths** to `D:\sign interpretor` or `SHARON`.
- **Node Test Shim Fixed in H48/H49:** `node_modules/three/{index.js,package.json}` is now tracked on GitHub, so `npm test` (`88/88`) runs immediately on a fresh clone with zero `npm install` needed.
- **New-Device Setup (`signinterpretor` folder):**
  1. `git clone https://github.com/shammatthews-life/Sign-interpretor.git signinterpretor && cd signinterpretor` (with `git lfs pull` if LFS objects are needed).
  2. Run `.\setup\setup_new_device.ps1` (creates `.env` from `.env.example`, creates `.venv` from `requirements.txt`, caches Faster-Whisper models, verifies environment).
  3. Run `npm test`, `npm run validate:signs`, `npm run serve`, and load `signinterpretor\extension` unpacked in `chrome://extensions/`.

# H48 Complete Local Tree & GitHub Synchronization Audit

**Audit Date:** 2026-11-25  
**Local Repository:** `D:\sign interpretor`  
**GitHub Repository:** `https://github.com/shammatthews-life/Sign-interpretor`  
**Branch:** `main`  
**Git LFS Installed:** `git-lfs/3.7.1 (GitHub; windows amd64)`  

---

## 1. Exhaustive Path-by-Path Inventory (All 26+ Root Entries Audited)

| Local Path | Exists Locally | Tracked in Git | On GitHub (`main`) | Ignored | GitHub Limit / Legal / Security / Portability | Total Files | Total Size (MB) | Status | Exact Reason |
|---|---|---|---|---|---|---:|---:|---|---|
| `.editorconfig` | Yes | Yes | Yes | No | None | `1` | `0.0003` | `SYNCED` | Tracked project config |
| `.env` | Yes | No | No | Yes (`.gitignore`) | **Security** | `1` | `0.0009` | `SECURITY_EXCLUDED` | Holds local runtime env vars (`ISL_HOST`, `WHISPER_*`); `.env.example` synced instead |
| `.env.example` | Yes | Yes | Yes | No | None | `1` | `0.0009` | `SYNCED` | Safe template for new-device setup |
| `.gitattributes` | Yes | Yes | Yes | No | None | `1` | `0.0005` | `SYNCED` | Tracked Git attributes |
| `.gitignore` | Yes | Yes | Yes | No | None | `1` | `0.0009` | `SYNCED` | Updated in H48 to track `backup/` and `node_modules/three/` |
| `LICENSE` | Yes | Yes | Yes | No | None | `1` | `0.0110` | `SYNCED` | MIT License |
| `package.json` | Yes | Yes | Yes | No | None | `1` | `0.0009` | `SYNCED` | Node scripts & metadata |
| `README.md` | Yes | Yes | Yes | No | None | `1` | `0.0125` | `SYNCED` | Project documentation |
| `requirements.txt` | Yes | Yes | Yes | No | None | `1` | `0.0001` | `SYNCED` | Python dependency manifest |
| `run.py` | Yes | Yes | Yes | No | None | `1` | `0.0002` | `SYNCED` | Root launcher |
| `.vscode/` | Yes | Yes | Yes | Partial (`.vscode/*`, `!.vscode/settings.json`) | None | `1` | `0.0000` | `SYNCED` | `settings.json` tracked; only 1 file exists locally |
| `__pycache__/` | Yes | Yes | Yes | Yes (`__pycache__/`) | Portability (OS/Python bytecode) | `2` | `0.0000` | `SYNCED` (root) / `IGNORED` (subdirs) | Root `run.cpython-312.pyc` & `run.cpython-314.pyc` tracked; subdirs regenerated at runtime |
| `data/` | Yes | Yes | Yes | No | None | `317` | `37.35` | `SYNCED` | All 317 corpus/lexicon files tracked |
| `docs/` | Yes | Yes | Yes | No | None | `347+` | `1.70+` | `SYNCED` | All milestone & audit reports tracked |
| `extension/` | Yes | Yes | Yes | No | None | `40` | `1.33` | `SYNCED` | Chrome MV3 extension + viewer engine |
| `isl_accessibility/` | Yes | Yes | Yes | No | None | `35` | `0.11` | `SYNCED` | Core Python package |
| `scripts/` | Yes | Yes | Yes | No | None | `3` | `0.00` | `SYNCED` | Runtime launch scripts |
| `setup/` | Yes | Yes | Yes | No | None | `4` | `0.02` | `SYNCED` | New-device setup PowerShell suite |
| `signs/` | Yes | Yes | Yes | No | None | `648` | `3.84` | `SYNCED` | `647` sign JSONs + `manifest.json` |
| `tools/` | Yes | Yes | Yes | No | None | `392` | `3.60` | `SYNCED` | Evaluators, E2E, ASR & viewer tools |
| `node_modules/` | Yes | **Now Yes (H48)** | **Now Yes (H48)** | `!node_modules/three/` | None (`1.14 KB`) | `2` | `0.0011` | `SYNCED` | H48 discovered `node_modules/three/{index.js,package.json}` is required by `npm test` and synced both files |
| `backup/` | Yes | **Now Yes (H48)** | **Now Yes (H48)** | Unignored in H48 | None (`25.37 MB`, max `1.74 MB`, `0` secrets) | `1,186` | `25.37` | `SYNCED` | H48 audited `h16–h21` checkpoints (`0` secrets, < 2 MB/file) and synchronized all 1,186 files |
| `artifacts/` | Yes | Partial (`223` files) | Partial (`223` files) | Partial (`frames/`, `crops/`, `recordings/`, `*.mp4`, `*.wav`, `raw_*`) | **GitHub Limit** (`13.55 GB` > 1 GB Free LFS quota) | `24,005` | `13,553.64` | `SYNCED` (reports/JSONs/sheets) + `GITHUB_LIMIT` (raw media) | Reports, JSON ledgers, contact sheets & crops sheets synced; `23,782` raw frames/MP4s/WAVs (`~13.5 GB`) exceed GitHub Free LFS quota (1 GB) |
| `Avatar_Boy_Gun_AetherShadow/` | Yes | No | No | Yes (`.gitignore`) | **Legal / License** | `19` | `5.75` | `LICENSE_EXCLUDED` | Copyrighted miHoYo / HoYoverse (*Genshin Impact*) FBX & textures (`docs/H39_ASSET_AND_LICENCE_REGISTER.md`); public redistribution prohibited |
| `runtime/` | Yes | No | No | Yes (`.gitignore`) | **GitHub Limit + Security + Portability** | `5,402` | `1,572.20` | `GITHUB_LIMIT` / `SECURITY_EXCLUDED` | Contains `chrome.dll` (`298.57 MB`), `audio_16k.wav` (`274.01 MB`), `source_MXKkXXYUxBc.webm` (`110.60 MB`), and 12 local Chrome/Edge profiles (cookies/cache) |
| `.venv/` | Yes | No | No | Yes (`.gitignore`) | **GitHub Limit + Portability** | `7,167` | `1,163.16` | `GITHUB_LIMIT` / `LOCAL_ONLY` | Contains `cublasLt64_12.dll` (`660.36 MB`), `cublas64_12.dll` (`108.44 MB`), and Windows/CUDA-12 binaries; recreated via `.\setup\setup_new_device.ps1` |

---

## 2. Git LFS Investigation Conclusion

- `git-lfs/3.7.1` is installed locally, but **GitHub Free provides 1 GB LFS storage and 1 GB/month LFS bandwidth**.
- Attempting to push `artifacts/` (`13.55 GB`) + `runtime/` (`1.57 GB`) + `.venv/` (`1.16 GB`) = **`16.28 GB`** via Git LFS would immediately fail GitHub's quota (and `runtime/` + `.venv/` also contain private browser cookies and OS/CUDA-specific binaries).
- Therefore, **all safe, legal, non-secret, within-limit folders—including `backup/` (`1,186` files, `25.37 MB`) and `node_modules/three/` (`2` files, `1.14 KB`)—are now 100% synchronized to `origin/main` at their exact original relative paths**, while only `artifacts/` raw multi-GB media (`GITHUB_LIMIT`), `runtime/` (`GITHUB_LIMIT` + `SECURITY_EXCLUDED`), `.venv/` (`GITHUB_LIMIT` + `LOCAL_ONLY`), `Avatar_Boy_Gun_AetherShadow/` (`LICENSE_EXCLUDED`), and `.env` (`SECURITY_EXCLUDED`) remain local.

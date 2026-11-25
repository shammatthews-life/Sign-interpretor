# H49 Local-vs-Remote File Comparison

Verified via `git ls-tree -r --name-only origin/main` vs recursive filesystem walk in [h49_verify_local_vs_remote.mjs](file:///d:/sign%20interpretor/tools/h49_verify_local_vs_remote.mjs):

| Category | Files | Size (MB) | Synced on `origin/main`? |
|---|---:|---:|---|
| Core Source, Docs, Signs, Data, Extension, Setup, Backup (`1,186`), `node_modules/three` (`2`), `artifacts` Reports/Sheets/Crops/MP4/WAV, `runtime` Transcripts/WAV/Wheel | `3,290` | `496.68` | **YES (`SYNCED` / `SYNCED_VIA_LFS`)** |
| `artifacts/` raw frame dumps (`frames/`, `raw_video_*`) | `23,723` | `13,242.97` | No (`GITHUB_LIMIT`) |
| `.venv/` (Windows/CUDA-12 Python env) | `7,167` | `1,163.16` | No (`GITHUB_LIMIT` / `LOCAL_ONLY`) |
| `runtime/` (`browsers/`, `youtube/*.wav/*.webm`) | `322` | `1,066.24` | No (`GITHUB_LIMIT` / Reproducible) |
| `runtime/` (12 Chrome/Edge profiles) | `5,011` | `392.87` | No (`SECURITY_EXCLUDED`) |
| `Avatar_Boy_Gun_AetherShadow/` | `19` | `5.75` | No (`LICENSE_EXCLUDED`) |
| `__pycache__/` nested `.pyc` | `48` | `0.43` | No (`IGNORED` bytecode) |
| `.env` | `1` | `0.0009` | No (`SECURITY_EXCLUDED`) |

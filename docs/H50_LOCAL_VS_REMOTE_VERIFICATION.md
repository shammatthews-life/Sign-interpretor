# H50 Local-vs-Remote Verification

Verified via [h49_verify_local_vs_remote.mjs](file:///d:/sign%20interpretor/tools/h49_verify_local_vs_remote.mjs) (`git ls-tree -r --name-only origin/main` vs `D:\sign interpretor`):

| Bucket | Files | Size (MB) | Status |
|---|---:|---:|---|
| Matched on `origin/main` | `3,452` (+7 H50 docs) | `824.12` | `SYNCED` / `SYNCED_VIA_LFS` (`69` LFS files) |
| `artifacts/` raw `h35–h42/frames/` & `raw_video_*` | `23,580` | `13,148.45` | `GITHUB_LIMIT` (exceeds `1 GB` Free LFS quota) |
| `.venv/` (Windows/CUDA-12 Python env) | `7,167` | `1,163.16` | `GITHUB_LIMIT` / `LOCAL_ONLY` (`C:\Users\SHARON` paths) |
| `runtime/` (`browsers/`, `MXKkXXYUxBc/*.wav/*.webm`) | `312` | `833.34` | `GITHUB_LIMIT` (`>100 MB` & LFS quota) |
| `runtime/` (12 Chrome/Edge profiles) | `5,011` | `392.87` | `SECURITY_EXCLUDED` (cookies/sessions) |
| `Avatar_Boy_Gun_AetherShadow/` | `19` | `5.75` | `LICENSE_EXCLUDED` (HoYoverse proprietary) |
| `__pycache__/` nested `.pyc` | `48` | `0.43` | `IGNORED` (regenerated Python bytecode) |
| `.env` | `1` | `0.0009` | `SECURITY_EXCLUDED` (`.env.example` synced) |
| Unaccounted | **`0`** | `0.00` | `100%` accounted |

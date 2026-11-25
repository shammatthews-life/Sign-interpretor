# H50 Final Report — Mandatory Full Local Project Upload to GitHub

- **Local Project:** `D:\sign interpretor` (`39,590` files pre-report)
- **Remote Repository:** `https://github.com/shammatthews-life/Sign-interpretor` (`main`)
- **Pre-Report Verified SHA:** `ce9cac5127c0cc622bb549b7a90acaa82ab21820`
- **Total Synchronized on `origin/main`:** `3,452` files (`824.12 MB`, including `69` Git LFS files = `~597 MB` LFS storage within GitHub Free's `1 GB` quota) + `7` H50 final reports.
- **Uploaded in H50:**
  - `143` H43–H47 Chrome phase frame captures (`94.52 MB` in `22a1372`)
  - `10` `runtime/youtube/` `.wav` & `.webm` media files `< 100 MB` (`232.91 MB` via Git LFS in `ce9cac5`)
- **Remaining Exclusions (Zero Silent / Arbitrary Exclusions):**
  - `Avatar_Boy_Gun_AetherShadow/` (`19` files, `5.75 MB`): `LICENSE_EXCLUDED` (HoYoverse proprietary copyright).
  - `.env` (`1` file) & `runtime/*_profile/` (`5,011` files, `392.87 MB`): `SECURITY_EXCLUDED`.
  - `.venv/` (`7,167` files, `1,163.16 MB`), `runtime/browsers/` + `MXKkXXYUxBc/*.wav/*.webm` (`312` files, `833.34 MB`), `artifacts/` `h35–h42` raw frames (`23,580` files, `13,148.45 MB`): `GITHUB_LIMIT` (exceeds `100 MB` file limit / `1 GB` Free LFS quota; reproducible via `.\setup\setup_new_device.ps1`).
- **Verification:** `node tools/security_audit.mjs` (`[PASS]`), `npm.cmd test` (`88 / 88 PASS`), `npm.cmd run validate:signs` (`647 / 647` valid).

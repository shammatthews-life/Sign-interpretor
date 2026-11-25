# H50 Virtual Environment Upload Report (`.venv/`)

- **Local Path:** `D:\sign interpretor\.venv` (`7,167` files, `1,163.16 MB`)
- **Synchronization Status:** `GITHUB_LIMIT` / `LOCAL_ONLY`
- **Size & Content Breakdown:**
  - `>= 100 MB` (`2` files, `768.81 MB`): `cublasLt64_12.dll` (`660.36 MB`), `cublas64_12.dll` (`108.44 MB`) — strictly exceeds GitHub's `100 MB` file limit and remaining GitHub Free `1 GB` LFS quota (`~403 MB` remaining after `597 MB` already pushed).
  - `50–100 MB` (`2` files, `140.13 MB`): `ffmpeg-win-x86_64-v7.1.exe` (`83.58 MB`), `ctranslate2.dll` (`56.55 MB`).
  - `< 50 MB` (`7,163` files, `254.22 MB`).
- **Hardcoded Machine Paths Verified in `.venv/pyvenv.cfg`:**
  - `home = C:\Users\SHARON\AppData\Local\Programs\Python\Python312`
  - `command = ... -m venv D:\sign interpretor\.venv`
- **Conclusion:** Uploading a partial `.venv` without its CUDA DLLs breaks `ctranslate2` on clone while embedding `C:\Users\SHARON` paths; `.\setup\setup_new_device.ps1` + `requirements.txt` cleanly recreates `.venv` on any target laptop.

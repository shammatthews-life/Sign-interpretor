# H50 Runtime Synchronization Report (`runtime/`)

- **Synced on `origin/main`:**
  - `35` `runtime/youtube/` JSON/VTT/TXT transcript & job result files (`80.72 MB`)
  - **`10` `runtime/youtube/` `.wav` & `.webm` media files (`232.91 MB` via Git LFS in `ce9cac5`)**: `y8tFSuOMAqQ`, `EvbhKINYrPg`, `D9Ihs241zeg`, `aircAruvnKk`, `xrwz9IxpMJg`
  - `30` `runtime/*.wav` benchmark chunks (`~5.5 MB` via Git LFS), `runtime/viewer_test.png` (`0.07 MB`), and `runtime/wheels/av-18.0.0-cp311-abi3-win_amd64.whl` (`26.28 MB` via Git LFS)
- **Remaining Local-Only in `runtime/`:**
  - `5,011` files (`392.87 MB`) across 12 local Chrome/Edge profiles (`chrome_*_profile`, `edge_test_profile`, `test_ext_profile`): **`SECURITY_EXCLUDED`** (browser cookies, sessions, Local Storage, cache).
  - `312` files (`833.34 MB`): `runtime/browsers/` (`306` files, `448.73 MB`, contains `chrome.dll` `298.57 MB`) and `runtime/youtube/MXKkXXYUxBc/` (`audio_16k.wav` `274.01 MB` + `source_MXKkXXYUxBc.webm` `110.60 MB`) — **`GITHUB_LIMIT`** (`> 100 MB` & exceeds remaining `~403 MB` Free LFS quota; reproducible via Puppeteer / `yt-dlp`).

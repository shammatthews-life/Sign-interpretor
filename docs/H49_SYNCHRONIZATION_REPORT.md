# H49 Synchronization Report

- **Synchronized During H49 (`d3c349b` + final report commit):**
  - `129` files (`334 MB` across `46` LFS objects + JSON/VTT/crop files) added cleanly at their exact original relative paths:
    - `19` MP4 E2E recordings (`artifacts/**/recording/*.mp4`, `artifacts/**/recordings/*.mp4`)
    - `65` avatar crop PNGs/manifests (`artifacts/**/crops/**`)
    - `7` preprocessed ASR WAVs (`artifacts/**/preprocessed_audio/*.wav`)
    - `1` subtitle VTT (`artifacts/h43/tmp_subs_y8tFSuOMAqQ.en.vtt`)
    - `35` YouTube transcript/metadata JSON/VTT/TXT files (`runtime/youtube/**`)
    - `30` benchmark WAV chunks + `viewer_test.png` (`runtime/`)
    - `1` Python wheel (`runtime/wheels/av-18.0.0-cp311-abi3-win_amd64.whl`)
- **Security Audit:** `node tools/security_audit.mjs` -> `[PASS] Security Audit Clean`.
- **Unit & Sign Tests:** `npm.cmd test` -> `88 / 88 PASS`; `npm.cmd run validate:signs` -> `647 / 647` valid.

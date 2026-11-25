# H49 GitHub Storage & Git LFS Report

- **Git LFS Version:** `git-lfs/3.7.1 (GitHub; windows amd64)`
- **Configured LFS Patterns (`.gitattributes`):**
  - `artifacts/**/*.mp4` (`19` MP4 recordings = `243.35 MB`)
  - `artifacts/**/*.wav` (`7` preprocessed audio WAVs = `26.64 MB`)
  - `runtime/*.wav` (`30` benchmark chunks = `~5.5 MB`)
  - `runtime/wheels/*.whl` (`av-18.0.0-cp311-abi3-win_amd64.whl` = `26.28 MB`)
- **Uploaded LFS Batch (`d3c349b`):** `46 / 46` objects (`334 MB` at `1.3 MB/s`, 100% verified).
- **GitHub Free Quota Boundary:** GitHub Free provides `1 GB` LFS storage and `1 GB/month` LFS bandwidth. The remaining `~13.24 GB` of raw frame PNG/JPEGs (`artifacts/**/frames/`, `artifacts/**/recordings/raw_video_*`), `1.16 GB` `.venv/`, and `1.07 GB` `runtime/browsers` + `runtime/youtube/*.wav/*.webm` exceed the `1 GB` Free LFS quota by `>15x` and are therefore classified as `GITHUB_LIMIT`.

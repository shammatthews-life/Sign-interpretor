# H43 — Architecture & System Reliability Report (WS7)

**Status:** COMPLETE  
**Addresses Defects:** `DEF-H43-001`, `DEF-H43-002`, `DEF-H43-003`, `DEF-H43-004`

---

## 1. Local Network Access / PNA Iframe Deadlock Fix (`DEF-H43-001`)
Chrome 158 blocked `<iframe id="isl-aether-iframe" src="http://localhost:8000/tools/avatar_viewer/index.html?embed=1">` inside `https://www.youtube.com` pages via Private Network Access (PNA) restrictions, stalling the iframe at `about:blank` while `overlay.js` prematurely hid `#isl-aether-fallback`.

**Architectural Resolution:**
1. **`extension/viewer/embed.html` & `extension/viewer/embed.js`:** Packaged a self-contained Three.js 3D WebGL avatar viewer (`extension/vendor/three/` + synced `extension/viewer/engine/`) directly as MV3 `web_accessible_resources` (`chrome-extension://<id>/viewer/embed.html`) without inline scripts or CDN fetches.
2. **PNA Headers & Bundle Endpoint (`tools/run_avatar_viewer.py`):** Added `Access-Control-Allow-Private-Network: true`, `Access-Control-Allow-Origin: *`, `OPTIONS` preflight support, and `GET /signs/bundle.json` returning all validated sign definitions in a single gzippable HTTP payload.
3. **Honest Fallback State Gating (`extension/content/overlay.js`, `extension/content/content-script.js`):** Updated `overlay.js` to load `chrome.runtime.getURL('viewer/embed.html?...')` when running inside Chrome Extension context and keep `#isl-aether-fallback` visible until `ISL_AETHER_READY` or `ISL_AETHER_STATE` confirms actual WebGL & sign initialization.

---

## 2. Startup Latency & Preload Cutoff Elimination (`DEF-H43-002`, `DEF-H43-003`)
- Added `SignLibrary.preloadBundle()` fetching `/signs/bundle.json` in a single request (falling back safely to array or object `manifest.signs`), eliminating the `550`-sign hardcoded array cutoff and reducing preload latency across `627` signs to a single request.
- Integrated dynamic `fs_<word>` fingerspelling resolution inside `SignLibrary.loadSign()` and `SignLibrary.getPlayable()`, preventing HTTP 404 failures for proper nouns and domain acronyms.

---

## 3. Pipeline Cache Hashing & Confidence Propagation (`WS7` / `WS1`)
- Extended `_translation_implementation_hash()` in `tools/youtube_pipeline/youtube_ingest.py` to hash `SemanticUnderstandingEngine.js` and `ISLFingerspelling.js` alongside `EnglishToISLTranslator.js`, `translate_segments.mjs`, and `signs/*.json`.
- Extended `transcribe_audio_file()` to capture `avg_logprob`, `no_speech_prob`, and calibrated `asr_confidence`, forwarded by `translate_segments.mjs` into `EnglishToISLTranslator.translate(..., { asrContext })`.

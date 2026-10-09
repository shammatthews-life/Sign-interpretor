# Phase H6 — Browser Extension Architecture & Integration Specification

> **CRITICAL ARCHITECTURAL DISCLAIMER:**
> **"The extension shell does not imply broad ISL motion coverage."**
> The Phase H6 browser extension shell provides an isolated host UI and integration bridge for web and streaming video environments (such as YouTube). It does **NOT** claim complete YouTube translation, nor does it fabricate or expand Indian Sign Language (ISL) gestures beyond verified repository assets.

---

## 1. Architectural Overview

Phase H6 introduces a Chromium/Chrome Manifest V3 accessibility extension shell structured around decoupled message passing, strict styling encapsulation, and fail-safe local runtime connectivity.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Web Page Context (e.g. YouTube)                 │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ #isl-accessibility-overlay-root (Shadow DOM boundary)          │   │
│   │                                                                │   │
│   │   [Header: Status Pills (CONN | AUDIO | ASR | TRANS | SIGN)]   │   │
│   │   [Aether 3D Avatar Frame (Iframe / postMessage bridge)]       │   │
│   │   [Speech & Transcript Telemetry (Partial & Final)]            │   │
│   │   [ISL Representation (Gloss, Status, Trace)]                  │   │
│   │   [Sign Queue & Unavailable Concepts Indicator]                │   │
│   │   [Deterministic Demo Controls & Scenario Selector]            │   │
│   └────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────▲──────────────────────────────────────┘
                                  │ chrome.runtime (postMessage/events)
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│               Extension Background (Service Worker MV3)                │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │   ISLMessageContract      │◄────►│      ISLRuntimeBridge       │   │
│   │      (Schema 1.0.0)       │      │   - Localhost Health Check  │   │
│   └───────────────────────────┘      │   - Deterministic Demo Hub  │   │
│                                      └──────────────┬──────────────┘   │
└─────────────────────────────────────────────────────┼──────────────────┘
                                                      │ HTTP / Fetch
                                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 Local Development Runtime (localhost:8000)             │
│                                                                        │
│   - Python Streaming ASR Service (`/asr/*` endpoints)                  │
│   - Aether FBX Model & Textures (`/Avatar_Boy_Gun_AetherShadow/*`)      │
│   - Three.js Interactive Viewer (`/tools/avatar_viewer/index.html`)     │
│   - Verified Sign Library (`/signs/*.json`)                            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Structure

The extension is organized cleanly under `extension/` without duplicating core repository translation or sign logic into content scripts:

| Path | Role | Description |
|---|---|---|
| `manifest.json` | Manifest V3 Config | Defines permissions (`storage`, `activeTab`), host permissions (`localhost`, `youtube.com`), service worker, and content scripts. |
| `shared/message-contract.js` | Universal Schema (1.0.0) | Enforces structured envelopes, action constants, and 5 mandatory lifecycle matrices. |
| `shared/demo-data.js` | Deterministic Demo Engine | Supplies strictly verified demonstration sequences (`greeting` and `missing_concept`). |
| `background/runtime-bridge.js` | Backend Coordinator | Non-blocking localhost health monitoring, error boundary, and demo step sequencer. |
| `background/service-worker.js` | Service Worker | MV3 event hub routing messages across tabs, popups, and the runtime bridge. |
| `content/overlay.css` | Encapsulated Stylesheet | Glassmorphism, dark-theme layout, high-contrast badges; isolated inside Shadow DOM. |
| `content/overlay.js` | Shadow DOM Component | Draggable, minimizable accessibility panel presenting real-time pipeline telemetry. |
| `content/content-script.js` | Host Page Adapter | Injects overlay root, handles YouTube SPA page transitions (`yt-navigate-finish`), and dispatches events. |
| `popup/` | Toolbar Action UI | Quick toggle, localhost probe, standalone viewer launcher, and demo triggers. |
| `icons/` | Visual Identity | Valid 16px, 48px, 128px extension icons. |

---

## 3. Message Contract Schema (v1.0.0)

All inter-component communication uses versioned message envelopes:

```typescript
interface ISLMessageEnvelope<T = any> {
  version: '1.0.0';
  type: string;
  payload: T;
  correlationId: string;
  timestamp: number;
}
```

### Mandatory UI Matrices (Task H6-C)
1. **Connection:** `DISCONNECTED` | `CONNECTING` | `CONNECTED` | `ERROR`
2. **Audio:** `IDLE` | `LISTENING` | `PAUSED` | `STOPPED`
3. **ASR:** `WAITING` | `PARTIAL` | `FINAL` | `ERROR`
4. **Translation:** `IDLE` | `TRANSLATING` | `READY` | `PARTIAL` | `HEURISTIC` | `UNCERTAIN`
5. **Signing:** `IDLE` | `PLAYING` | `QUEUED` | `UNAVAILABLE`

---

## 4. YouTube Page Compatibility (Task H6-F)

The extension safely integrates into YouTube (`*://*.youtube.com/*`):
- **Encapsulated Shadow DOM:** The overlay attaches to `#isl-accessibility-overlay-root` using `attachShadow({ mode: 'open' })`. Neither YouTube's extensive CSS nor the overlay's styles leak across this boundary.
- **SPA Resilience:** Listens for YouTube navigation events (`yt-navigate-finish` and `popstate`) so the overlay remains stable across page navigations without duplicate DOM elements.
- **Zero Privacy Scraping:** The overlay does not touch private user metadata, session cookies, search queries, or internal video data.
- **Non-Interference:** The panel is freely draggable and minimizable to a compact floating badge (`#isl-launcher-badge`), preventing obstruction of native YouTube player controls, captions, or progress bars.

---

## 5. Localhost Development & Aether Integration (Task H6-E)

### Why Localhost Integration is Development-Only:
- **Redistribution & Model Licensing:** The Aether 3D model binary (`Avatar_Boy_Gun_AetherShadow.fbx`, ~18.5 MB) and associated textures are proprietary development assets. Packaging them directly into a distributed Chrome extension bundle would violate size limits, performance targets, and redistribution constraints.
- **Local Native ASR Acceleration:** Phase F2.5 utilizes Python `ctranslate2` / CUDA hardware acceleration (`LocalASRService`), which requires a local Python host.
- **Integration Bridge:**
  - When localhost is active (`http://localhost:8000`), the overlay embeds an iframe with `?embed=1` and communicates via `postMessage({ type: 'ISL_AETHER_COMMAND', command, signId })`.
  - When localhost is offline, the overlay displays a non-crashing fallback card instructing the developer to run `python tools/run_avatar_viewer.py`.

---

## 6. Relationship to the Sign Evidence Gate

The browser extension shell does **NOT** authorize or generate sign motion.
- Playable signs remain strictly: `HELLO`, `GOOD`, `MORNING` (10/110 occurrences = 9.09% in H1 corpus).
- Top missing concepts (`YOU`, `WATER`, `I`, `HELP`, `ME`, `NEED`, `DRINK`) are flagged transparently as `UNAVAILABLE` with their visual evidence status (`MOTION_INCOMPLETE` or `MOTION_NOT_AUTHORED`).
- The H5 human-evidence capture protocol remains the sole gating path for candidate motions to enter the playable library.

---

## 7. Future Production Architecture (Task H6-L)

The decoupled interface enables future upgrades without modifying the overlay or extension shell:
1. **ASR Replacement:** Replace localhost Python server with WebAssembly Whisper (e.g. Transformers.js / ONNX) or a cloud WebSockets endpoint by updating `RuntimeBridge`.
2. **Translation Replacement:** Swap the transparent G2/G3 rule engine for a neural ISL sequence model by keeping the `translate()` contract.
3. **Avatar Renderer Replacement:** Replace the Three.js Aether viewer with a WebGPU or glTF/VRM avatar engine through the standard `PLAY_SIGN` / `QUEUE_SIGN` / `RESET_AVATAR` interface.

# Phase H23: Chrome Manifest V3 Service Worker Lifecycle Audit

**Project:** Indian Sign Language (ISL) Accessibility Translator — `Sign-interpretor`  
**Date:** October 31, 2026  
**Standards:** Google Chrome Extensions Manifest V3 Specifications  
**Deliverable File:** `docs/h23_mv3_lifecycle_audit.md`  

---

## 1. Architectural Constraints of Manifest V3 Service Workers

In Google Chrome's Manifest V3 architecture, background execution is handled by event-driven **Service Workers** rather than persistent background pages:
- **Ephemeral Idle Suspension:** Chrome aggressively suspends service workers after **30 seconds of inactivity** to conserve battery and memory.
- **Popup Ephemerality:** When a user clicks outside the extension popup window, the popup DOM and JavaScript execution context are completely destroyed.
- **Long-Running ASR Threat:** Processing a 2.5-hour lecture through speech-to-text takes multiple seconds. If long-running tasks rely on in-memory variables inside the service worker or popup, state is lost upon worker termination.

---

## 2. Hardened Architecture for Asynchronous Job Longevity

Our extension design circumvents MV3 worker ephemerality through three coordinated mechanisms:
1. **Delegated Local Daemon Execution:** All heavy compute (audio extraction, Whisper ASR inference, corpus transcription caching) is offloaded to the local Python daemon (`http://127.0.0.1:8000/api/youtube/job`). The extension service worker only initiates jobs and polls for status.
2. **`chrome.storage.local` Persistence:** Job IDs and transcript metadata are written directly to `chrome.storage.local`. If the service worker is terminated or the popup closes, the state remains intact on disk.
3. **Content Script Autonomy:** Once the floating overlay is injected on YouTube, `overlay-controller.js` and `timeline-synchronizer.js` run directly in the persistent YouTube tab context, unaffected by background service worker lifecycle resets.

---
*Task 14 certified and verified.*

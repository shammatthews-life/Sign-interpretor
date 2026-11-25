# Phase 1B: ISL Visual Asset Acquisition & Source Report

**Project:** ISL Accessibility Translator  
**Phase:** 1B — First Five Real ISL Visual Assets  
**Date:** September 30, 2026  
**Scope:** Controlled verification of initial 5 lexical concepts (`hello`, `good`, `morning`, `thank you`, `water`).

---

## 1. Executive Summary & Policy Compliance

In strict adherence to the project's **ISL Sign Asset Policy**:
- **No scraping or unverified image harvesting:** We do NOT scrape Google Images, Pinterest, or commercial stock sites.
- **No ASL / foreign sign substitution:** All concepts must be verified against Indian Sign Language (ISL), which uses distinct handshapes, orientations, and two-handed conventions.
- **No synthetic / AI-generated hand imagery:** Synthetic hand renderings are prohibited.
- **Separation of lexical signs and fingerspelling:** Fingerspelling (e.g., spelling out `H-E-L-L-O`) is prohibited for lexical words.
- **No premature verification claims:** The `"verified": false` flag is strictly preserved until candidate visual assets are manually inspected, validated, and placed by the researcher.

Official investigative research into the **Indian Sign Language Research and Training Centre (ISLRTC)** repositories reveals that ISLRTC's dictionary is primarily **video-based** (available via the official *Sign Learn* mobile application, DIKSHA portal, and the official [ISLRTC YouTube Channel](https://www.youtube.com/@islrtc)). Standalone open-access static JPEG image downloads are not distributed by ISLRTC.

Therefore, automatic frame harvesting has **not** been performed. All 5 target assets are formally designated as **MANUAL ACQUISITION REQUIRED** with direct reference guidance for human inspection below.

---

## 2. Asset Acquisition Status Table

| Concept | ISL source found | Visual asset obtained | Licence/use status | Verified | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **hello** | Yes (ISLRTC Official Portal / Sign Learn / YouTube) | No (Static image not distributed; video only) | Government of India / ISLRTC copyright (Standard YouTube / Educational viewing) | `false` | MANUAL ACQUISITION REQUIRED |
| **good** | Yes (ISLRTC Official Dictionary / Sign Learn) | No (Static image not distributed; video only) | Government of India / ISLRTC copyright (Educational viewing) | `false` | MANUAL ACQUISITION REQUIRED |
| **morning** | Yes (ISLRTC Official Dictionary / Sign Learn) | No (Static image not distributed; video only) | Government of India / ISLRTC copyright (Educational viewing) | `false` | MANUAL ACQUISITION REQUIRED |
| **thank you** | Yes (ISLRTC Official Dictionary / Sign Learn) | No (Static image not distributed; video only) | Government of India / ISLRTC copyright (Educational viewing) | `false` | MANUAL ACQUISITION REQUIRED |
| **water** | Yes (ISLRTC Official Dictionary / Sign Learn) | No (Static image not distributed; video only) | Government of India / ISLRTC copyright (Educational viewing) | `false` | MANUAL ACQUISITION REQUIRED |

---

## 3. Detailed Source Breakdown & Manual Acquisition Guide

### 1. `hello`
- **Concept:** Greeting lexical sign (informal/formal greeting).
- **Target Filename:** `isl_accessibility/signs/hello.jpg`
- **Official Source:** ISLRTC Official Portal (`http://www.islrtc.nic.in/`) & ISLRTC YouTube Channel (`https://www.youtube.com/@islrtc`).
- **Linguistic Form:** In ISL, "Hello" is signed as a distinct lexical movement (open hand near temple/forehead, moving slightly outward in a salute-like or polite waving motion), differing distinctly from ASL. It must **not** be fingerspelled as `H → E → L → L → O`.
- **Licensing & Fair Use:** Videos are copyrighted by ISLRTC. For academic, non-commercial accessibility research, manually capturing a single representative still frame showing the peak hand configuration falls under fair dealing / educational research.
- **Manual Action Required:**
  1. Open the Sign Learn app or ISLRTC channel video demonstrating greeting signs.
  2. Pause at the peak inflection point (where the signer's handshape, orientation, and facial expression are clear).
  3. Capture/crop a clear square frame (300×300 to 500×500 px).
  4. Save as `isl_accessibility/signs/hello.jpg`.
  5. Update `data/sign_dictionary.json` with the exact source timestamp/URL and mark `"verified": true`.

---

### 2. `good`
- **Concept:** Positive evaluation lexical sign.
- **Target Filename:** `isl_accessibility/signs/good.jpg`
- **Official Source:** ISLRTC Official Dictionary (*Sign Learn* app / DIKSHA portal).
- **Linguistic Form:** Open flat hand moving outward from the chin/chest forward.
- **Licensing & Fair Use:** ISLRTC educational copyright. Single representative still keyframe allowable for non-commercial educational prototype under fair dealing with proper attribution.
- **Manual Action Required:**
  1. Locate "Good" in the ISLRTC Sign Learn dictionary or DIKSHA vocabulary series.
  2. Capture the focal hand pose showing hand position relative to the chin.
  3. Save as `isl_accessibility/signs/good.jpg`.
  4. Update `data/sign_dictionary.json` and mark `"verified": true`.

---

### 3. `morning`
- **Concept:** Time-of-day lexical sign.
- **Target Filename:** `isl_accessibility/signs/morning.jpg`
- **Official Source:** ISLRTC Official Dictionary (*Sign Learn* app / DIKSHA portal).
- **Linguistic Form:** Rising sun / upward motion representing dawn. Distinct from Western sign languages.
- **Licensing & Fair Use:** ISLRTC educational copyright.
- **Manual Action Required:**
  1. Locate "Morning" in ISLRTC dictionary resources.
  2. Capture keyframe showing the terminal or peak gesture height.
  3. Save as `isl_accessibility/signs/morning.jpg`.
  4. Update `data/sign_dictionary.json` and mark `"verified": true`.

---

### 4. `thank you`
- **Concept:** Courtesy lexical sign (Dhanyavaad).
- **Target Filename:** `isl_accessibility/signs/thank_you.jpg`
- **Official Source:** ISLRTC Official Dictionary (*Sign Learn* app / introductory lessons).
- **Linguistic Form:** Flat hand touching or near the chin and moving forward toward the addressee with a polite nod. Must **not** be fingerspelled.
- **Licensing & Fair Use:** ISLRTC educational copyright.
- **Manual Action Required:**
  1. Locate "Thank You" / "Dhanyavaad" in ISLRTC official video demonstrations.
  2. Capture keyframe showing outward hand motion and posture.
  3. Save as `isl_accessibility/signs/thank_you.jpg`.
  4. Update `data/sign_dictionary.json` and mark `"verified": true`.

---

### 5. `water`
- **Concept:** Natural resource / beverage noun sign (Paani).
- **Target Filename:** `isl_accessibility/signs/water.jpg`
- **Official Source:** ISLRTC Official Dictionary (*Sign Learn* app / NCERT accessible curriculum lessons).
- **Linguistic Form:** Three extended fingers (resembling 'W' or index-middle-ring) tapping or gesturing near the side of the mouth/chin.
- **Licensing & Fair Use:** ISLRTC educational copyright.
- **Manual Action Required:**
  1. Locate "Water" in ISLRTC vocabulary video.
  2. Capture keyframe clearly showing the three-finger handshape positioned beside the mouth.
  3. Save as `isl_accessibility/signs/water.jpg`.
  4. Update `data/sign_dictionary.json` and mark `"verified": true`.

---

## 4. Current Application Behavior

Because no unverified images were scraped or fabricated:
1. All 5 images remain **missing on disk** (`MISSING` reported by `tools/validate_sign_library.py`).
2. The Tkinter GUI continues to operate smoothly without crashing, rendering clean, dynamic fallback placeholder cards (`SIGN IMAGE NOT ADDED YET`) for all entries.
3. The moment any valid `.jpg` file is placed in `isl_accessibility/signs/` matching the required filename, the GUI will immediately load and display the real sign on next translation.

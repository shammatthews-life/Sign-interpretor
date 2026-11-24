# Indian Sign Language (ISL) Accessibility Translator

[![Tests: Passing](https://img.shields.io/badge/Tests-76%2F76%20Passing-brightgreen.svg)](./package.json)
[![Sign Library: 586 Playable](https://img.shields.io/badge/ISL%20Signs-586%2F586%20(100%25)-blue.svg)](./signs/manifest.json)
[![Manifest V3](https://img.shields.io/badge/Chrome%20Extension-Manifest%20V3-orange.svg)](./extension/manifest.json)
[![Whisper CUDA](https://img.shields.io/badge/ASR-Faster--Whisper%20CUDA%2012-76b900.svg)](./requirements.txt)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

> **Real-Time 3D Avatar Assistive Technology for Web & YouTube Video**  
> Translates spoken English dialogue into grammatically structured Indian Sign Language (ISL) and articulates signs in real time via an interactive, WebGL 3D avatar (**Aether**).

---

## 1. Executive Summary & Problem Statement

Over 18 million Deaf and Hard-of-Hearing individuals across India communicate primarily in Indian Sign Language (ISL). Standard automated closed captions do not provide true accessibility because English and ISL operate on fundamentally different linguistic structures:

- **Grammar & Syntax:** English is Subject-Verb-Object (SVO). Natural ISL is strictly **Subject-Object-Verb (SOV)**, placing verbs, interrogatives, and negations at clause and propositional boundaries.
- **Topicalization & Discourse:** ISL topicalizes time, location, and condition markers at the beginning of propositions before presenting the core predicate.
- **Strict Prohibition on Silent Substitution:** ASL or BSL signs cannot be silently substituted for established ISL lexical concepts. All signs in this project are verified against official Indian Sign Language authorities, primarily the **Indian Sign Language Research and Training Centre (ISLRTC)**.

---

## 2. System Architecture

The project is structured into four decoupled, high-performance subsystems:

```
                            +----------------------------------------+
                            |     YouTube Video / Web Audio Stream   |
                            +-------------------+--------------------+
                                                |
                                                v
                            +----------------------------------------+
                            | Faster-Whisper ASR / Audio Pipeline    |
                            | (CTranslate2 CUDA float16 or CPU int8) |
                            +-------------------+--------------------+
                                                |
                                                v
                            +----------------------------------------+
                            | ISL Grammar & Linguistic Engine        |
                            | (SOV Inversion, Temporal Topicalization|
                            |  Clause-Scoped Negation, Numeral Decomp)|
                            +-------------------+--------------------+
                                                |
                                                v
                            +----------------------------------------+
                            | 586-Sign Motion Library (Schema 2.0.0) |
                            | (ISLRTC Lexicon, Bone Rotations, Euler)|
                            +-------------------+--------------------+
                                                |
                                                v
+------------------------------------+          |
| Chrome Extension (Manifest V3)     | <--------+
| - Floating Shadow DOM Overlay      |
| - HTML5 Timeline Synchronizer      |
| - Service Worker State Bridge      |
+------------------+-----------------+
                   |
                   v
+------------------------------------+
| Three.js WebGL 3D Avatar Viewer    |
| - Aether 243-Bone Humanoid Rig     |
| - Full-Body & Adaptive Framing     |
| - Cubic Easing & Multi-Bone Blend  |
+------------------------------------+
```

---

## 3. Quick Start (One-Command Setup)

On a Windows 10/11 machine with PowerShell:

```powershell
# 1. Clone the repository
git clone https://github.com/shammatthews-life/Sign-interpretor.git
cd Sign-interpretor

# 2. Run the automated onboarding script
.\setup\setup_new_device.ps1
```

### What `setup_new_device.ps1` accomplishes:
- Creates `.env` from template.
- Initializes a local Python virtual environment (`.venv`).
- Installs Python dependencies (`faster-whisper`, `av`, `Pillow`, `requests`, `yt-dlp`).
- Validates the 586-sign motion library and synchronizes `signs/manifest.json`.
- Runs full environment diagnostics and executes the 29-segment linguistic test suite.

For step-by-step manual setup, refer to [docs/H39_NEW_DEVICE_SETUP_GUIDE.md](./docs/H39_NEW_DEVICE_SETUP_GUIDE.md).

---

## 4. Running the Translator

### Step 1: Start the Local Avatar Server
```powershell
npm run serve
# (or: & .\.venv\Scripts\python.exe tools/run_avatar_viewer.py --port 8000)
```
The server will start at `http://127.0.0.1:8000`, serving the WebGL viewer and sign definitions.

### Step 2: Load the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Toggle **Developer mode** ON (top right).
3. Click **Load unpacked** and select the `extension/` folder in this repository.

### Step 3: Watch YouTube with ISL Interpretation
Navigate to any supported YouTube video (e.g. [Public Speaking for Beginners](https://www.youtube.com/watch?v=MXKkXXYUxBc)). The floating, draggable 3D Aether avatar appears directly on the video player and articulates signs synchronized with the speech timeline.

---

## 5. Verification & Test Suites

The repository contains automated unit, benchmark, and manifest validation suites:

```powershell
# Run all 76 unit tests across extension and viewer
npm test

# Run the 29-segment YouTube benchmark linguistic evaluation
npm run test:benchmark

# Validate and compile all 586 Schema 2.0.0 signs
npm run validate:signs

# Run full hardware & environment diagnostics
powershell -ExecutionPolicy Bypass -File setup/verify_environment.ps1
```

All 76 unit tests and 29 benchmark invariant checks pass with zero failures.

---

## 6. Implementation Status Matrix

| Subsystem | Status | Key Features & Metrics |
| :--- | :---: | :--- |
| **Sign Library (`signs/`)** | **100% Playable** | **586/586 signs** valid Schema 2.0.0, zero corrupted files, Manifest v2.5.0. |
| **ISL Grammar Engine** | **Production Ready** | SOV transformation, clause-scoped negation, relative clause preservation, multi-digit numeral decomposition. |
| **Benchmark Coverage** | **63.6% Direct / 100% Concept** | 272 spoken words $\to$ 173 playable signs, 0 unknown concepts, 7 fingerspelled names. |
| **ASR & Audio Pipeline** | **CUDA Accelerated** | Faster-Whisper on NVIDIA RTX 4050 (`float16`, RTF 0.0298) with automatic CPU fallback. |
| **3D Avatar Viewer** | **Full Body & Half Body** | Three.js WebGL, 243-bone Aether rig, portrait viewport dynamic distance scaling. |
| **Chrome Extension (MV3)** | **Tested & Verified** | Shadow DOM overlay, drift-free timeline synchronizer, service-worker probe coalescing. |

---

## 7. ISL Grammar & Linguistic Rules

The translator implements core Indian Sign Language grammatical rules:

1. **Subject-Object-Verb (SOV) Reordering:**
   - English: `"You win fear"` $\to$ ISL: `YOU FEAR WIN`
2. **Clause-Scoped Negation:**
   - English: `"If you haven't seen it, my name is Alex"` $\to$ ISL: `BEFORE SEE NOT MY NAME ALEX` (Negation scoped strictly to subordinate clause).
3. **Relative Clause Preservation:**
   - English: `"Watch what happens"` $\to$ ISL: `WATCH WHAT HAPPEN` (Declarative relative pronoun retained without interrogative inversion).
4. **Multi-Digit Numeral Decomposition:**
   - Multi-digit numbers decompose into standard ISL bases (e.g. `110` $\to$ `HUNDRED TEN`, `30` $\to$ `THIRTY`, `25` $\to$ `TWENTY FIVE`).
5. **Temporal Topicalization:**
   - Time words (`TODAY`, `BEFORE`, `NOW`) fronted to the beginning of the proposition.

---

## 8. Asset Licensing & Governance

To maintain strict compliance with open-source licensing and intellectual property laws:
- **Project Code & Sign Library:** Released under open-source terms.
- **Avatar 3D Model (`Avatar_Boy_Gun_AetherShadow`):** Proprietary game character rig (HoYoverse). Excluded from Git via `.gitignore` to prevent copyright takedowns. Complete local acquisition and integrity instructions are documented in [docs/H39_ASSET_AND_LICENCE_REGISTER.md](./docs/H39_ASSET_AND_LICENCE_REGISTER.md).
- **Headless Portability:** The compiler, translation engine, and test suites operate with 100% functionality even in headless mode without the proprietary FBX mesh.

---

## 9. Repository Structure

```
├── .editorconfig                          # Cross-platform editor formatting
├── .env.example                           # Configuration environment template
├── .gitattributes                         # LF/CRLF line-ending normalization
├── .gitignore                             # Git ignore rules (excludes models & frame dumps)
├── package.json                           # Node.js project scripts and test triggers
├── requirements.txt                       # Core Python packages
├── README.md                              # Main project documentation
├── extension/                             # Chrome Extension (Manifest V3)
│   ├── manifest.json                      # Extension manifest
│   ├── background/                        # Service worker & message routing
│   ├── content/                           # Shadow DOM overlay & timeline sync
│   └── shared/                            # Cue manifests & message contracts
├── isl_accessibility/                     # Core Python translation package
├── signs/                                 # 586 Schema 2.0.0 ISL Sign Definitions
│   ├── manifest.json                      # Synchronized sign index (v2.5.0)
│   └── *.json                             # Individual bone rotation motion files
├── tools/                                 # Verification, pipeline, & avatar tools
│   ├── avatar_viewer/                     # Three.js WebGL avatar player & translator
│   ├── youtube_pipeline/                  # YouTube audio & subtitle extraction
│   └── *.mjs                              # Automated test suites & audit scripts
├── setup/                                 # Modular new-device setup scripts
│   ├── install_dependencies.ps1           # Python, venv, and package installation
│   ├── download_models.ps1                # Model pre-caching & asset verification
│   ├── verify_environment.ps1             # System diagnostics & health check
│   └── setup_new_device.ps1               # Master one-command onboarding script
└── docs/                                  # Engineering diaries & milestone reports
    ├── H38_SINGLE_VIDEO_PERFECTION_FINAL_REPORT.md
    ├── H39_ASSET_AND_LICENCE_REGISTER.md
    ├── H39_ENVIRONMENT_COMPATIBILITY.md
    ├── H39_NEW_DEVICE_SETUP_GUIDE.md
    └── H39_REPOSITORY_COMPLETENESS_AUDIT.md
```

---

## 10. Documentation Index

- [docs/H39_NEW_DEVICE_SETUP_GUIDE.md](./docs/H39_NEW_DEVICE_SETUP_GUIDE.md) — Comprehensive new-machine setup guide.
- [docs/H39_ASSET_AND_LICENCE_REGISTER.md](./docs/H39_ASSET_AND_LICENCE_REGISTER.md) — Asset provenance, licences, and SHA-256 hashes.
- [docs/H39_ENVIRONMENT_COMPATIBILITY.md](./docs/H39_ENVIRONMENT_COMPATIBILITY.md) — Platform support, GPU requirements, and CUDA specifications.
- [docs/H39_REPOSITORY_COMPLETENESS_AUDIT.md](./docs/H39_REPOSITORY_COMPLETENESS_AUDIT.md) — Forensic repository inventory and delta analysis.
- [docs/H38_SINGLE_VIDEO_PERFECTION_FINAL_REPORT.md](./docs/H38_SINGLE_VIDEO_PERFECTION_FINAL_REPORT.md) — H38 milestone results and benchmark verification.

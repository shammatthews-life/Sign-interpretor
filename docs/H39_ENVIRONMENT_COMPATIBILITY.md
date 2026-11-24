# H39 — Environment and Platform Compatibility Specification

**Project:** Indian Sign Language (ISL) Real-Time Accessibility Translator  
**Milestone:** H39 (Repository Portability & GitHub Synchronization)  
**Date:** 2026-11-24  
**Author:** Antigravity Autonomous Engineering Agent  
**Repository:** `https://github.com/shammatthews-life/Sign-interpretor`  

---

## 1. Overview & Portability Target

The ISL Accessibility Translator is engineered for reproducible deployment across standard Windows development environments, with cross-platform support for headless translation, unit testing, and sign validation on Linux and macOS.

This specification documents exact system requirements, hardware accelerators, runtime dependencies, and fallback strategies to guarantee out-of-the-box operation on a newly cloned workstation.

---

## 2. Hardware and Acceleration Matrix

| Component | Minimum Specification | Recommended / Benchmark Configuration | Fallback Mode (No GPU) |
| :--- | :--- | :--- | :--- |
| **CPU** | 4 cores / 8 threads (x86_64 or ARM64) | Intel Core i7 / AMD Ryzen 7 (8+ cores) | Standard execution |
| **RAM** | 8 GB DDR4 | 16 GB – 32 GB DDR5 | Supported (Whisper `base` or `small`) |
| **GPU** | Integrated Graphics (Intel Iris Xe / AMD Radeon) | **NVIDIA GeForce RTX 4050 Laptop GPU** (6 GB GDDR6) or higher | Software WebGL / CPU Whisper inference |
| **CUDA** | CUDA 11.8+ (optional) | **CUDA 12.1 / 12.4** with cuDNN 8.9+ | Automatic CPU mode (`compute_type="int8"`) |
| **Display** | 1080p (1920x1080) 60 Hz | 1080p or 1440p high-DPI display | Headless Playwright / Offscreen canvas |
| **Storage** | 5 GB free disk space | 20 GB SSD NVMe | Required |

---

## 3. Operating System Support Matrix

| Platform | Support Tier | Primary Use Case | Validation Status |
| :--- | :---: | :--- | :--- |
| **Windows 11 (64-bit)** | **Tier 1 (Primary)** | Full End-to-End: Chrome Extension, WebGL, CUDA, NVENC recording | **100% Tested & Verified** |
| **Windows 10 (64-bit)** | **Tier 1** | Full End-to-End: Chrome Extension, WebGL, CUDA, NVENC recording | Supported |
| **Ubuntu 22.04 / 24.04 LTS** | **Tier 2** | Headless CLI, Faster-Whisper ASR, Node.js test suites, sign validation | Supported via Bash scripts |
| **macOS 13+ (Ventura / Sonoma / Sequoia)** | **Tier 2** | Development, Node.js test suites, sign authoring, Chrome extension loading | Supported (CPU/MPS Whisper) |

---

## 4. Runtime & Language Dependencies

### 4.1 Node.js
- **Required Version:** Node.js $\ge 18.0.0$ (Recommended: Node.js 20 LTS or Node.js 24 Current).
- **Verified Local Version:** `v24.2.0` (x64).
- **Key Modules Used:** Built-in `node:test`, `node:assert`, `node:fs`, `node:path`, `node:crypto`, `node:http`.
- **Zero-Dependency Core:** The sign compiler, manifest validator, translation engine, and test suites run on pure vanilla Node.js without requiring third-party npm packages.

### 4.2 Python
- **Required Version:** Python 3.10 – 3.12 (64-bit).
- **Verified Local Version:** `Python 3.12.3` (x64).
- **Virtual Environment:** Dedicated `.venv` created via `python -m venv .venv`.
- **Core Python Packages (`requirements.txt`):**
  - `faster-whisper==1.1.1`: High-performance Whisper model runner based on CTranslate2.
  - `av==18.0.0`: PyAV audio/video demuxing and decoding bindings.
  - `Pillow>=10.0.0`: Image processing and inspection utilities.
  - `requests==2.32.3`: HTTP request handling.
  - `yt-dlp==2024.8.19` (or newer): High-speed YouTube audio and metadata extraction.

### 4.3 FFmpeg
- **Required Version:** FFmpeg $\ge 6.0$ (Recommended: FFmpeg 7.x essentials or full build).
- **Hardware Encoders Supported:**
  - `h264_nvenc` (NVIDIA hardware acceleration — sub-second screencast encoding).
  - `h264_qsv` (Intel QuickSync).
  - `h264_amf` (AMD AMF).
  - `libx264` (Universal CPU software fallback).

---

## 5. Browser & Extension Runtime

### 5.1 Google Chrome / Chromium
- **Required Version:** Google Chrome $\ge 120.0$ (64-bit).
- **Extension Architecture:** Chrome Manifest V3 (`extension/manifest.json`).
- **Required Capabilities:**
  - `activeTab`, `storage`, `tabs`, `scripting` permissions.
  - Content script injection into `*://*.youtube.com/*`.
  - WebGL 2.0 context support with hardware canvas rendering.
  - ES6 Module loading via `<script type="module">` and `<script type="importmap">`.

---

## 6. Verification and Compatibility Self-Test

The repository provides an automated environment verification script:
```powershell
# Windows PowerShell
.\setup\verify_environment.ps1
```
The script checks and outputs:
1. Python version and virtual environment activation.
2. Node.js version and test runner readiness.
3. NVIDIA CUDA availability and GPU model detection.
4. FFmpeg binary availability and `h264_nvenc` support.
5. All 586 sign JSON files and manifest synchronization.
6. Extension manifest syntax and file integrity.

# ISL Accessibility Translator

An assistive technology initiative designed to convert spoken English into Indian Sign Language (ISL), eventually presenting translations via a continuous visual signer as an accessibility overlay for live broadcasts, videos, and educational platforms.

---

## Project Goal

The long-term goal of this project is an end-to-end accessibility pipeline:

```
English Speech
      ↓
English Text (Speech-to-Text)
      ↓
ISL Linguistic Translation (SOV Grammar & Non-Manual Features)
      ↓
Visual Signing (3D Animated Avatar)
      ↓
Real-Time Accessibility Overlay (Web, YouTube, Television, Public Broadcasts)
```

---

## Current Status

The original **Phase 1 English text → ISL sign images** desktop prototype
remains available through `python run.py`. The repository also contains the
later local development runtime described below. Neither path is a
linguistically complete English-to-ISL translator.

Phase 1 capabilities include:
- **English Text Input:** Desktop GUI text entry supporting the Enter key and translate button.
- **Text Preprocessing:** Tokenization, lowercasing, punctuation stripping, and whitespace normalization.
- **Controlled ISL Mapping:** Direct dictionary lookup for tokens and 2-word phrases (`data/sign_dictionary.json`).
- **ISL Gloss Output:** Formatted sign gloss sequence (e.g., `GOOD → MORNING`).
- **Sign Image Display:** Horizontal, scrollable visual card presentation.
- **Placeholder Handling:** Dynamic, in-memory Pillow placeholder rendering for missing sign images.
- **Sign Asset Validation:** Automated test suite verifying schema integrity, Pillow decoding, and missing visual assets (`tools/validate_sign_library.py`).

### Local runtime implementation

The later G1–H8 development runtime is implemented under `tools/` and
`extension/`:

- `tools/avatar_viewer/` contains the avatar viewer, schema 2.0.0 sign
  library, scheduler, authoring controls, and existing translation pipeline.
- `tools/audio_pipeline/`, `tools/asr/`, and `tools/youtube_pipeline/`
  implement speech/audio handling and the H7 YouTube-to-transcript pipeline.
- `extension/` contains the Manifest V3 popup, content overlay, service
  worker, and runtime bridge. The H8 YouTube flow uses the local runtime API.
- `signs/` contains the authored sign JSON files. A sign is schedulable only
  when the existing library marks its motion playable.
- `tools/validate_phase_*.mjs` and `tools/validate_phase_*.py` contain the
  phase validation scripts that are present in this checkout.

Use Python 3.12 for the runtime. Start the local viewer and development API
from the repository root:

```powershell
.\.venv\Scripts\python.exe tools\run_avatar_viewer.py --port 8000
```

Load the unpacked extension by selecting the `extension/` directory in the
browser's extension developer mode. The extension talks to the local viewer
API; it is not a hosted service. See
[`docs/h8_youtube_extension_integration.md`](docs/h8_youtube_extension_integration.md)
and the H7/H8 test reports for the API contract and tested limitations.

The viewer expects the separately supplied Aether model and textures at
`Avatar_Boy_Gun_AetherShadow/` in the repository root. Those third-party
assets are excluded from Git; obtain and place them locally only when their
license permits. YouTube downloads, generated transcripts, benchmark/runtime
output, and optional local wheel files belong under the ignored `runtime/`
directory and are not source files. ASR benchmark WAV fixtures are also
excluded because they are derived from an upstream recording; benchmark
scripts can create local fixtures with
`tools/asr/generate_benchmark_audio.py` after reviewing the upstream source
terms.

---

## IMPORTANT LIMITATION

> **Notice:**  
> **This Phase 1 implementation is a controlled prototype and is NOT a complete linguistically validated English-to-ISL translation model.**
>
> Natural Indian Sign Language (ISL) has its own distinct grammar, Subject-Object-Verb (SOV) sentence order, spatial signing space, and critical facial expressions. Word-for-word token mapping is strictly used as an engineering scaffold for this phase and will be replaced by a formal translation engine in subsequent phases.

---

## Project Structure

```
Sign-interpretor/
│
├── .gitignore                         # Git exclusion rules (.venv, cache, etc.)
├── LICENSE                            # Apache 2.0 License
├── README.md                          # Repository overview & setup guide
├── requirements.txt                   # Minimal dependencies (Pillow)
├── run.py                             # Root application launcher
│
├── .vscode/
│   └── settings.json                  # VS Code interpreter configuration
│
├── isl_accessibility/                 # Core Python package
│   ├── __init__.py
│   ├── app.py                         # Application entry point
│   ├── config.py                      # Paths, UI constants, styling
│   │
│   ├── nlp/                           # Natural Language Processing
│   │   ├── __init__.py
│   │   └── text_processor.py          # Tokenization and text cleaning
│   │
│   ├── isl/                           # ISL Representation
│   │   ├── __init__.py
│   │   └── sign_mapper.py             # Dictionary lookup & gloss sequencing
│   │
│   ├── data/                          # Data assets
│   │   └── sign_dictionary.json       # 13 controlled vocabulary concepts
│   │
│   ├── signs/                         # Visual sign library
│   │   ├── README.txt                 # Asset storage guidelines
│   │   └── alphabet/                  # Fingerspelling references (A-Z)
│   │       └── README.txt             # Fingerspelling vs lexical sign guidelines
│   │
│   ├── ui/                            # Desktop Interface
│   │   ├── __init__.py
│   │   └── interface.py               # Tkinter GUI implementation
│   │
│   ├── tools/                         # Package validation tools
│   │   ├── __init__.py
│   │   └── validate_sign_library.py
│   │
│   └── README.md                      # Detailed Phase 1 architecture documentation
│
├── tools/                             # Repository utilities
│   ├── __init__.py
│   └── validate_sign_library.py       # Standalone dataset & asset validator
│
└── docs/                              # Project documentation
    ├── phase1_plan.md                 # Architecture plan
    ├── phase1b_asset_report.md        # Asset research & acquisition report
    └── PROJECT_STATUS.md              # Detailed implementation checklist
```

---

## Installation

The project uses **Python 3.12.10**.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shammatthews-life/Sign-interpretor.git
   cd Sign-interpretor
   ```

2. **Create a local virtual environment:**
   ```bash
   py -3.12 -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
     *(If script execution is disabled, enable it for your user: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
   - On Command Prompt:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Run

Launch the application using Python:

```bash
python run.py
```
*(Or `.\.venv\Scripts\python.exe run.py`)*

To validate the sign library and inspect missing assets:
```bash
python tools/validate_sign_library.py
```

---

## Sign Assets

Visual sign assets belong in:
`isl_accessibility/signs/`

Expected filenames for the initial controlled concepts:
- `hello.jpg`
- `good.jpg`
- `morning.jpg`
- `thank_you.jpg`
- `water.jpg`
- `evening.jpg`, `how.jpg`, `you.jpg`, `help.jpg`, `me.jpg`, `tomorrow.jpg`, `rain.jpg`, `please.jpg`

When an image is absent, the GUI safely displays an informative placeholder card without crashing.

---

## Asset Policy

To protect linguistic authenticity and ethical standards:
1. **Authoritative ISL Sources:** Reference official resources, primarily the **Indian Sign Language Research and Training Centre (ISLRTC)**.
2. **No ASL Substitution:** American Sign Language (ASL) or British Sign Language (BSL) must **not** be silently substituted.
3. **No Fingerspelling for Lexical Signs:** Fingerspelling (`signs/alphabet/`) is reserved for proper nouns and fallback purposes. Words like `HELLO` must not be replaced by `H-E-L-L-O`.
4. **No Unverified Web Scraping:** Do not scrape random Google Images or Pinterest pictures.
5. **No Synthetic AI Hands:** Do not generate synthetic AI hand imagery as substitutes for real signs.
6. **Transparent Metadata:** Every entry in `data/sign_dictionary.json` must record source, source URL, access date, and licensing terms.
7. **Strict Verification State:** All entries remain `"verified": false` until manually inspected and validated against official ISL linguistic materials.

---

## Roadmap

The repository preserves the Phase 1 prototype and includes later development
work through H8. Current work includes fine-grained avatar articulation
testing (R1). This remains a limited prototype: sign coverage, linguistic
validation, and a browser-installed YouTube extension session are not implied
by the presence of the runtime code. See the phase-specific reports under
[`docs/`](docs/).

---

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

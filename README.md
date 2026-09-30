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

**PHASE 1 — English Text → ISL Sign Images**

The project is currently a local, standalone prototype. Current capabilities include:
- **English Text Input:** Desktop GUI text entry supporting the Enter key and translate button.
- **Text Preprocessing:** Tokenization, lowercasing, punctuation stripping, and whitespace normalization.
- **Controlled ISL Mapping:** Direct dictionary lookup for tokens and 2-word phrases (`data/sign_dictionary.json`).
- **ISL Gloss Output:** Formatted sign gloss sequence (e.g., `GOOD → MORNING`).
- **Sign Image Display:** Horizontal, scrollable visual card presentation.
- **Placeholder Handling:** Dynamic, in-memory Pillow placeholder rendering for missing sign images.
- **Sign Asset Validation:** Automated test suite verifying schema integrity, Pillow decoding, and missing visual assets (`tools/validate_sign_library.py`).

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

Development proceeds strictly phase-by-phase:

- **Phase 1 (Current):** English Text → ISL Sign Images prototype.
- **Phase 2 (Future):** Validated ISL sign library expansion and organization.
- **Phase 3 (Future):** English → ISL linguistic representation (syntax parsing, SOV restructuring).
- **Phase 4 (Future):** English speech → text integration.
- **Phase 5 (Future):** Speech → ISL signs pipeline.
- **Phase 6 (Future):** Continuous sign sequencing and timing.
- **Phase 7 (Future):** 3D human/avatar signer.
- **Phase 8 (Future):** Real-time optimization.
- **Phase 9 (Future):** Browser extension for web video accessibility.
- **Phase 10 (Future):** Live video / TV accessibility overlay integration.

---

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

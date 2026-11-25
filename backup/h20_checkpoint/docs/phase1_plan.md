# Phase 1: English Text → ISL Sign Images

## Architecture & Implementation Plan

### 1. Scope & Objective
Phase 1 implements a lightweight, standalone desktop prototype in Python using Tkinter and Pillow. It establishes the initial pipeline:
1. Accept English sentence from user input.
2. Clean and tokenize text (case normalization, punctuation removal, whitespace cleanup).
3. Map tokens/phrases to ISL glosses and associated image filenames via a controlled demonstration dictionary (`data/sign_dictionary.json`).
4. Display the resulting ISL gloss sequence and corresponding sign images (or informative placeholders if images are not yet added).
5. Highlight unknown words without crashing.

> **Controlled Vocabulary Prototype Notice:**  
> Phase 1 is a demonstration prototype mapping words/phrases to sign representations. It does **not** perform grammatically correct English-to-ISL translation (which requires grammatical restructuring, SOV word order, non-manual features, and spatial syntax—slated for Phase 3+).

---

### 2. Directory Structure

```
Sign-interpretor/
│
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
│
├── .vscode/
│   └── settings.json
│
├── isl_accessibility/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   │
│   ├── nlp/
│   │   ├── __init__.py
│   │   └── text_processor.py
│   │
│   ├── isl/
│   │   ├── __init__.py
│   │   └── sign_mapper.py
│   │
│   ├── data/
│   │   └── sign_dictionary.json
│   │
│   ├── signs/
│   │   ├── README.txt
│   │   └── alphabet/
│   │       └── README.txt
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── interface.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   └── validate_sign_library.py
│   │
│   └── README.md
│
├── tools/
│   └── validate_sign_library.py
│
└── docs/
    ├── phase1b_asset_report.md
    ├── phase1_plan.md
    └── PROJECT_STATUS.md
```

---

### 3. Component Design

#### A. NLP (`nlp/text_processor.py`)
- Independent, testable text processing.
- Converts to lowercase, strips punctuation, normalizes whitespace.
- Returns clean list of string tokens.

#### B. ISL Mapper (`isl/sign_mapper.py`)
- Reads `data/sign_dictionary.json`.
- Uses a greedy lookup mechanism to support both multi-word phrases (e.g. `"thank you"`) and single words.
- Returns a structured dictionary:
  ```json
  {
    "glosses": ["GOOD", "MORNING"],
    "images": ["good.jpg", "morning.jpg"],
    "unknown": []
  }
  ```
- Handles unknown words cleanly without raising uncaught exceptions.

#### C. Data (`data/sign_dictionary.json`)
Controlled demonstration vocabulary (13 concepts):
`hello`, `thank you`, `good`, `morning`, `evening`, `how`, `you`, `help`, `me`, `water`, `tomorrow`, `rain`, `please`.

#### D. Image & Placeholder Strategy (`ui/interface.py` & `signs/`)
- No scraped or unvalidated images are bundled.
- If an image file exists in `signs/`, Pillow loads and displays it.
- If an image file does not exist, a Pillow-rendered card is generated displaying:
  ```
  ┌────────────────────────┐
  │      [NO IMAGE]        │
  │   SIGN IMAGE NOT YET   │
  │         ADDED          │
  │     Gloss: HELLO       │
  └────────────────────────┘
  ```
- Zero crashes on missing/invalid files.

#### E. GUI (`ui/interface.py` & `app.py`)
- Standard Tkinter desktop GUI.
- Text input box with `<Return>` binding and a prominent "Translate" button.
- Clean summary section showing:
  - English input echo
  - ISL Gloss Sequence (`GOOD → MORNING`)
  - Horizontally scrollable card gallery for sign images / placeholders
  - Unknown words list
- Error banners for empty input.

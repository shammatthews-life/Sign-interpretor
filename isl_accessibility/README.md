# ISL Accessibility Translator

A modular, phased assistive technology system designed to translate English into Indian Sign Language (ISL) representations.

> **Important Prototype Disclaimer:**  
> **Phase 1 is a prototype English-text-to-ISL-sign-image mapping system. It is not a complete linguistically validated English-to-ISL translation model.**

---

## 1. Project Purpose
The ultimate goal of the ISL Accessibility Translator is to build a real-time system that listens to spoken English and translates it into Indian Sign Language (ISL), eventually presenting the signs through an expressive human-like animated 3D avatar. In the future, this system is intended to function as an accessibility overlay for YouTube, streaming platforms, educational lectures, television broadcasts, and public informational screens.

To ensure stability, correctness, and pedagogical clarity, development is structured sequentially across distinct phases.

---

## 2. Current Scope: Phase 1 & Phase 1A
- **Phase 1 Focus:** *English Text → ISL Sign Representation Pipeline*
- **Phase 1A Focus:** *ISL Sign Asset Infrastructure & Validation*

In Phase 1 and 1A, we build the core architectural pipeline on a local machine:
- Accepts raw English text from a desktop interface.
- Normalizes and tokenizes text (lowercasing, punctuation stripping, whitespace handling).
- Looks up tokens and 2-word phrases against a controlled demonstration dictionary (`data/sign_dictionary.json`).
- Formats the mapped ISL sequence (e.g. `GOOD → MORNING`).
- Displays sign images horizontally inside a scrollable card interface.
- Displays dynamic, non-crashing placeholders if an image file is not yet present on disk.
- Reports unknown words that are not in the dictionary.
- Enforces an official asset management policy with source tracking and validation tools.

---

## 3. ISL Sign Asset Policy

To ensure linguistic integrity and ethical data handling, the project strictly adheres to the following policies:

1. **Linguistic Distinction: Lexical Signs vs. Fingerspelling**
   - **Lexical Signs:** Standard words in ISL (e.g. `HELLO`, `WATER`, `GOOD`) are distinct, self-contained gestures with designated handshapes, positions, and movements.
   - **Fingerspelling:** Used exclusively for proper nouns (names of people, places) or words lacking an established sign.
   - **Fingerspelling is NOT a substitute for lexical translation:** `HELLO` must not be spelled out as `H → E → L → L → O`. Fingerspelling assets reside in a separate directory (`signs/alphabet/`) and are reserved for a future fallback mechanism.

2. **Official ISL-Specific Reference Resources**
   - Reference source: The **Indian Sign Language Research and Training Centre (ISLRTC)**.
   - We do **NOT** scrape random Google Images or generic stock photo websites.
   - We do **NOT** silently substitute American Sign Language (ASL) or British Sign Language (BSL) signs, as ISL possesses its own distinct vocabulary and two-handed manual alphabet.

3. **No Synthetic / AI-Generated Hand Substitutes**
   - We do **NOT** use AI-generated hands or speculative graphics as substitutes for verified sign language data.

4. **Transparent Source Tracking**
   - Every sign in `data/sign_dictionary.json` records metadata:
     - `source`: e.g. `"ISLRTC"`
     - `source_url`: URL reference where available
     - `accessed_date`: Date asset was reviewed
     - `license_notes`: Usage terms
     - `verified`: Boolean flag (`true` or `false`)

5. **Strict Verification State**
   - All entries default to `"verified": false`.
   - A sign is only marked `"verified": true` after it has been formally cross-checked against official ISL materials or validated by a certified ISL consultant.

6. **No Premature Linguistic Claims**
   - The current dictionary and display represent a controlled vocabulary demonstration. The project does not claim to generate grammatically fluent ISL sentences at this phase.

---

## 4. Technologies Used
- **Python 3.11+** (Tested on Python 3.14)
- **Tkinter / ttk**: Desktop Graphical User Interface (Python standard library)
- **Pillow (PIL)**: High-quality image loading, aspect-ratio scaling, and dynamic in-memory placeholder generation
- **JSON**: Storage format for the sign dictionary (`sign_dictionary.json`)

*Note: No machine learning models, external cloud APIs, or web servers are used in Phase 1 / 1A.*

---

## 5. Installation

1. **Clone or Navigate to the Project Root:**
   ```bash
   cd "d:/sign interpretor"
   ```

2. **(Optional but recommended) Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Command Prompt:
   .\venv\Scripts\activate.bat
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r isl_accessibility/requirements.txt
   ```

---

## 6. How to Run

### Run the Desktop Translator
From the workspace root directory:
```bash
python run.py
```
*(Or `python isl_accessibility/app.py`)*

Type an English sentence in the text box and press **Enter** or click **TRANSLATE**.

### Run the Sign Library Validator
To verify dictionary integrity and check which visual assets are present:
```bash
python tools/validate_sign_library.py
```

---

## 7. Folder Structure

```
isl_accessibility/
│
├── app.py                     # Application entry point
├── config.py                  # Paths, constants, and UI styling
├── requirements.txt           # Minimal external dependencies (Pillow)
├── README.md                  # Project documentation & Phase 1/1A overview
│
├── nlp/                       # Natural Language Processing
│   ├── __init__.py
│   └── text_processor.py      # Text cleaning, normalization, tokenization
│
├── isl/                       # ISL Representation & Lookup
│   ├── __init__.py
│   └── sign_mapper.py         # Dictionary lookup & gloss sequencing
│
├── data/                      # Data assets
│   └── sign_dictionary.json   # Controlled vocabulary (13 concepts with source metadata)
│
├── signs/                     # Lexical sign image repository
│   ├── README.txt             # Guidelines for adding validated images
│   └── alphabet/              # Dedicated fingerspelling alphabet folder (A-Z)
│       └── README.txt         # Linguistic guidelines on fingerspelling
│
├── tools/                     # Validation utilities
│   ├── __init__.py
│   └── validate_sign_library.py
│
└── ui/                        # Desktop Interface
    ├── __init__.py
    └── interface.py           # Tkinter GUI implementation
```

---

## 8. How to Add a Validated Sign Image

1. Obtain a legitimate ISL reference image from an official source (e.g. ISLRTC).
2. Check `data/sign_dictionary.json` for the expected filename:
   - `hello.jpg`, `thank_you.jpg`, `good.jpg`, `morning.jpg`, `evening.jpg`, `how.jpg`, `you.jpg`, `help.jpg`, `me.jpg`, `water.jpg`, `tomorrow.jpg`, `rain.jpg`, `please.jpg`.
3. Place the file directly in `isl_accessibility/signs/`.
4. Update the dictionary entry's `source_url`, `accessed_date`, and set `"verified": true` once verified.
5. Run `python tools/validate_sign_library.py` to confirm the asset is recognized.

---

## 9. Example Inputs & Expected Outputs

| Input Sentence | ISL Sequence | Output Cards | Unknown Words |
| :--- | :--- | :--- | :--- |
| `"Hello"` | `HELLO` | 1 Card (`hello.jpg` or placeholder) | `None` |
| `"Good morning"` | `GOOD → MORNING` | 2 Cards (`good.jpg`, `morning.jpg`) | `None` |
| `"Thank you"` | `THANK YOU` | 1 Card (`thank_you.jpg`) | `None` |
| `"The boy drinks water"` | `WATER` | 1 Card (`water.jpg`) | `the, boy, drinks` |
| `"How are you?"` | `HOW → YOU` | 2 Cards (`how.jpg`, `you.jpg`) | `are` |

---

## 10. Current Limitations (Phase 1 / 1A)
- **Controlled Vocabulary Only:** Only words and phrases present in `data/sign_dictionary.json` (13 concepts) are recognized.
- **Pending Visual Assets:** Legitimate visual assets are tracked but currently missing from disk, displaying safe placeholder cards.
- **Word-for-Word Ordering:** Signs are displayed sequentially based on English input; grammar restructuring (English SVO to ISL SOV) is not yet applied.
- **Static Display:** Signs are presented as static images/cards rather than continuous motions.
- **No Non-Manual Signals:** Does not capture facial expressions, head movements, or spatial signing space.

---

## 11. Future Phases (Roadmap)

- **Phase 2 (Future):** Expand and organize a validated ISL sign library.
- **Phase 3 (Future):** English sentence processing → ISL linguistic representation (syntax parsing, SOV restructuring, lemmatization).
- **Phase 4 (Future):** English Speech → Text integration.
- **Phase 5 (Future):** Speech → ISL Sign Images pipeline.
- **Phase 6 (Future):** Continuous sentence/sign sequencing and improved timing.
- **Phase 7 (Future):** 3D human/avatar signer.
- **Phase 8 (Future):** Real-time optimization.
- **Phase 9 (Future):** Chrome/browser accessibility extension.
- **Phase 10 (Future):** Live video / YouTube / TV accessibility overlay integration.

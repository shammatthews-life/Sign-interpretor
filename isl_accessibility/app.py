"""Application Entry Point for ISL Accessibility Translator (Phase 1).

Starts the Tkinter desktop GUI application.
Ensures directories and dependencies are initialized properly before launch.
"""

import sys
from pathlib import Path
import tkinter as tk

# Ensure current package directory and workspace are on sys.path
CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent

for path in (CURRENT_DIR, PARENT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from isl_accessibility.config import (
        APP_TITLE,
        DATA_DIR,
        SIGNS_DIR,
        ALPHABET_DIR,
        DICTIONARY_PATH,
    )
    from isl_accessibility.ui.interface import ISLTranslatorUI
except ImportError:
    # Direct execution fallback when run inside isl_accessibility directory
    from config import (
        APP_TITLE,
        DATA_DIR,
        SIGNS_DIR,
        ALPHABET_DIR,
        DICTIONARY_PATH,
    )
    from ui.interface import ISLTranslatorUI


def main() -> None:
    """Bootstrap and start the Tkinter application."""
    # Ensure required runtime directories exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SIGNS_DIR.mkdir(parents=True, exist_ok=True)
    ALPHABET_DIR.mkdir(parents=True, exist_ok=True)

    if not DICTIONARY_PATH.exists():
        print(f"[Warning] Sign dictionary not found at {DICTIONARY_PATH}.")

    root = tk.Tk()
    root.title(APP_TITLE)

    # Initialize UI
    app = ISLTranslatorUI(root)

    # Start main event loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")


if __name__ == "__main__":
    main()

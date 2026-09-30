"""Configuration module for ISL Accessibility Translator (Phase 1).

Centralizes file paths, UI configuration parameters, and constants.
Uses pathlib for cross-platform filesystem compatibility.
"""

from pathlib import Path

# Base project directory (isl_accessibility/)
BASE_DIR = Path(__file__).resolve().parent

# Data paths
DATA_DIR = BASE_DIR / "data"
SIGNS_DIR = BASE_DIR / "signs"
ALPHABET_DIR = SIGNS_DIR / "alphabet"
DICTIONARY_PATH = DATA_DIR / "sign_dictionary.json"

# UI Settings
APP_TITLE = "ISL Accessibility Translator — Phase 1"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# Sign Card Display Dimensions (pixels)
SIGN_IMAGE_WIDTH = 180
SIGN_IMAGE_HEIGHT = 180

# Visual Styling Colors (Clean modern light theme)
COLOR_BG = "#F8FAFC"             # Slate-50 background
COLOR_PANEL_BG = "#FFFFFF"       # White card background
COLOR_PRIMARY = "#2563EB"        # Blue-600 primary action
COLOR_PRIMARY_HOVER = "#1D4ED8"  # Blue-700
COLOR_TEXT_MAIN = "#0F172A"      # Slate-900 high contrast text
COLOR_TEXT_MUTED = "#64748B"     # Slate-500 secondary text
COLOR_CARD_BORDER = "#CBD5E1"    # Slate-300 border
COLOR_CARD_BG = "#F1F5F9"        # Slate-100 placeholder background
COLOR_ALERT_WARN = "#D97706"     # Amber-600 for unknown words
COLOR_ACCENT = "#059669"         # Emerald-600 for sequence glosses

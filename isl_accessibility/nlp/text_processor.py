"""Text Preprocessor Module for ISL Accessibility Translator (Phase 1).

Responsible for:
1. Converting text to lowercase.
2. Stripping punctuation while preserving words.
3. Normalizing whitespace (removing redundant spaces, tabs, newlines).
4. Tokenizing the sentence into clean word tokens.

This module is completely decoupled from UI and ISL dictionary logic.
"""

import re
import string


def clean_text(text: str) -> str:
    """Normalize and clean raw input text.

    Steps performed:
    1. Handle edge cases (None or non-string input).
    2. Convert characters to lowercase.
    3. Remove punctuation characters (e.g. !?,.:;'"-).
    4. Collapse multiple spaces/tabs/newlines into a single space.

    Args:
        text: Raw input string from user.

    Returns:
        Cleaned, normalized string.
    """
    if not text or not isinstance(text, str):
        return ""

    # 1. Lowercase
    normalized = text.lower()

    # 2. Remove punctuation
    # We replace punctuation with spaces so "hello,world" becomes "hello world"
    translator = str.maketrans({char: " " for char in string.punctuation})
    no_punctuation = normalized.translate(translator)

    # 3. Normalize whitespace (strips leading/trailing spaces and collapses internal spaces)
    cleaned = re.sub(r"\s+", " ", no_punctuation).strip()

    return cleaned


def tokenize_text(text: str) -> list[str]:
    """Preprocess and tokenize input text into a list of words.

    Example:
        >>> tokenize_text("Good morning!")
        ['good', 'morning']
        >>> tokenize_text("  Hello,  how are you?  ")
        ['hello', 'how', 'are', 'you']

    Args:
        text: Raw input string.

    Returns:
        List of cleaned token strings. Returns empty list for empty/whitespace input.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    # Split on whitespace
    return cleaned.split()

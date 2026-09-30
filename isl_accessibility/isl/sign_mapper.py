"""Sign Mapper Module for ISL Accessibility Translator (Phase 1).

Maps preprocessed English tokens/phrases to their corresponding
Indian Sign Language (ISL) glosses and sign image metadata.

==============================================================================
PHASE 1 PROTOTYPE NOTICE:
This is a controlled vocabulary demonstration mapper.
It performs simple direct dictionary lookups for tokens/phrases.
This is NOT a complete or grammatically validated English-to-ISL translation system.
ISL has its own distinct syntax, grammar (e.g., Subject-Object-Verb),
facial expressions, and spatial relations.
In future phases (Phase 3+), this component will be replaced by a formal
linguistic translation module.
==============================================================================
"""

import json
from pathlib import Path
from typing import Any, Optional


class SignMapper:
    """Loads sign metadata from JSON and maps English word tokens to ISL glosses."""

    def __init__(self, dictionary_path: Optional[Path | str] = None) -> None:
        """Initialize the mapper by loading the sign dictionary.

        Args:
            dictionary_path: Path to the JSON dictionary file.
        """
        self.dictionary: dict[str, dict[str, str]] = {}
        if dictionary_path:
            self.load_dictionary(dictionary_path)

    def load_dictionary(self, dictionary_path: Path | str) -> None:
        """Safely load sign metadata from a JSON file.

        Handles missing file or JSON formatting errors gracefully.

        Args:
            dictionary_path: Path to the sign dictionary JSON.
        """
        path = Path(dictionary_path)
        if not path.exists():
            print(f"[Warning] Sign dictionary not found at {path}. Operating with empty dictionary.")
            self.dictionary = {}
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.dictionary = data
                else:
                    print(f"[Warning] Dictionary at {path} is not a valid JSON object. Found: {type(data)}")
                    self.dictionary = {}
        except json.JSONDecodeError as err:
            print(f"[Error] Failed to parse dictionary JSON at {path}: {err}")
            self.dictionary = {}
        except Exception as err:
            print(f"[Error] Unexpected error loading dictionary: {err}")
            self.dictionary = {}

    def map_tokens(self, tokens: list[str]) -> dict[str, list[str]]:
        """Map clean tokens to ISL glosses, image filenames, and unknown tokens.

        Supports multi-word phrase matching (greedy 2-word lookahead, e.g. "thank you")
        as well as single-word matching. Unmatched tokens are gathered in 'unknown'.

        Args:
            tokens: Cleaned lowercase word tokens from the text processor.

        Returns:
            Dictionary with keys:
                - 'glosses': List of matched ISL gloss strings (e.g., ['GOOD', 'MORNING'])
                - 'images': List of image filenames (e.g., ['good.jpg', 'morning.jpg'])
                - 'unknown': List of tokens not found in the dictionary
        """
        glosses: list[str] = []
        images: list[str] = []
        unknown: list[str] = []

        if not tokens:
            return {"glosses": glosses, "images": images, "unknown": unknown}

        i = 0
        total_tokens = len(tokens)

        while i < total_tokens:
            # 1. Greedy 2-word phrase check (e.g., "thank you")
            if i + 1 < total_tokens:
                two_word_phrase = f"{tokens[i]} {tokens[i + 1]}"
                if two_word_phrase in self.dictionary:
                    entry = self.dictionary[two_word_phrase]
                    glosses.append(entry.get("gloss", two_word_phrase.upper()))
                    images.append(entry.get("image", ""))
                    i += 2
                    continue

            # 2. Single-word check
            word = tokens[i]
            if word in self.dictionary:
                entry = self.dictionary[word]
                glosses.append(entry.get("gloss", word.upper()))
                images.append(entry.get("image", ""))
            else:
                unknown.append(word)

            i += 1

        return {
            "glosses": glosses,
            "images": images,
            "unknown": unknown,
        }

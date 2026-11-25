"""ISL Sign Library Validation Tool.

Validates the integrity of data/sign_dictionary.json and the presence/validity
of local visual assets in signs/.

Checks:
1. Every dictionary entry contains: gloss, image, source, verified.
2. The referenced image exists and can be opened with Pillow (or reports MISSING).
3. No dictionary entries contain empty gloss values.
4. No duplicate image filenames exist across entries.
5. Prints a clean, readable report.
"""

import json
import sys
from pathlib import Path

# Resolve base directories
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "tools" else SCRIPT_DIR

if (PROJECT_ROOT / "isl_accessibility" / "data").exists():
    DATA_DIR = PROJECT_ROOT / "isl_accessibility" / "data"
    SIGNS_DIR = PROJECT_ROOT / "isl_accessibility" / "signs"
elif (PROJECT_ROOT / "data").exists():
    DATA_DIR = PROJECT_ROOT / "data"
    SIGNS_DIR = PROJECT_ROOT / "signs"
else:
    DATA_DIR = PROJECT_ROOT / "isl_accessibility" / "data"
    SIGNS_DIR = PROJECT_ROOT / "isl_accessibility" / "signs"

DICTIONARY_PATH = DATA_DIR / "sign_dictionary.json"

REQUIRED_FIELDS = ("gloss", "image", "source", "verified")


def validate_sign_library() -> bool:
    """Run all validation checks against the sign dictionary and asset folder.

    Returns:
        True if all schema rules pass, False otherwise.
    """
    print("=" * 50)
    print("ISL SIGN LIBRARY VALIDATION")
    print("=" * 50)

    if not DICTIONARY_PATH.exists():
        print(f"ERROR: Dictionary file not found at {DICTIONARY_PATH}")
        return False

    try:
        with open(DICTIONARY_PATH, "r", encoding="utf-8") as f:
            dictionary = json.load(f)
    except json.JSONDecodeError as err:
        print(f"ERROR: Invalid JSON in dictionary: {err}")
        return False

    if not isinstance(dictionary, dict) or not dictionary:
        print("ERROR: Dictionary must be a non-empty JSON object.")
        return False

    images_found = 0
    images_missing = 0
    seen_images: dict[str, str] = {}
    schema_errors: list[str] = []

    # Optional Pillow check for image decoding integrity
    try:
        from PIL import Image
        pillow_available = True
    except ImportError:
        pillow_available = False

    for word, meta in dictionary.items():
        # Check entry is a dictionary
        if not isinstance(meta, dict):
            schema_errors.append(f"'{word}': Entry must be a JSON object.")
            continue

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in meta:
                schema_errors.append(f"'{word}': Missing required field '{field}'.")

        # Check non-empty gloss
        gloss = meta.get("gloss")
        if not gloss or not isinstance(gloss, str) or not gloss.strip():
            schema_errors.append(f"'{word}': 'gloss' must be a non-empty string.")

        # Check image filename format and duplicate detection
        image_name = meta.get("image")
        if not image_name or not isinstance(image_name, str) or not image_name.strip():
            schema_errors.append(f"'{word}': 'image' must be a non-empty string.")
        else:
            if image_name in seen_images:
                schema_errors.append(
                    f"'{word}': Duplicate image filename '{image_name}' already used by '{seen_images[image_name]}'."
                )
            else:
                seen_images[image_name] = word

        # Check verified type
        if "verified" in meta and not isinstance(meta["verified"], bool):
            schema_errors.append(f"'{word}': 'verified' must be a boolean (true/false).")

        # Check asset existence on disk and format validity
        if image_name:
            image_path = SIGNS_DIR / image_name
            if image_path.is_file():
                if pillow_available:
                    try:
                        with Image.open(image_path) as img:
                            img.verify()
                        status = "FOUND"
                        images_found += 1
                    except Exception as img_err:
                        status = f"FOUND (CORRUPT: {img_err})"
                        schema_errors.append(f"'{word}': Image '{image_name}' is corrupt or unreadable.")
                else:
                    status = "FOUND"
                    images_found += 1
            else:
                status = "MISSING"
                images_missing += 1
        else:
            status = "NO IMAGE SPECIFIED"
            images_missing += 1

        # Print line item
        print(f"{word:<12} -> {status}")

    print("=" * 50)
    print(f"Total signs:    {len(dictionary)}")
    print(f"Images found:   {images_found}")
    print(f"Images missing: {images_missing}")

    if schema_errors:
        print("\nSCHEMA ERRORS:")
        for err in schema_errors:
            print(f"  - {err}")
        print("\nResult: FAILED (Schema violations detected)")
        return False

    print("\nSchema check:   PASSED")
    if images_missing > 0:
        print("Asset status:   Pending legitimate ISL image collection (expected at this stage).")
    else:
        print("Asset status:   All images present.")
    print("=" * 50)
    return True


if __name__ == "__main__":
    success = validate_sign_library()
    sys.exit(0 if success else 1)

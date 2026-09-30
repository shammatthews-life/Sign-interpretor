"""ISL Sign Library Validation Tool (shim/package entry point).

Executes the sign library validator from tools/validate_sign_library.py.
"""

from tools.validate_sign_library import validate_sign_library

if __name__ == "__main__":
    import sys
    success = validate_sign_library()
    sys.exit(0 if success else 1)

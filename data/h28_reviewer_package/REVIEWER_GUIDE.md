# Indian Sign Language (ISL) Expert Reviewer Protocol

## Purpose
This review package is prepared for **certified ISL interpreters, Deaf educators, and native Deaf signers** to evaluate the 3D avatar animations produced by the Aether engine for the ISL Accessibility Translator project.

## Review Instructions
For each sign asset in `reviewer_package_manifest.json`:
1. **Lexical Authenticity:** Does this sign reflect authentic Indian Sign Language as recognized by the Indian Sign Language Research and Training Centre (ISLRTC)?
2. **Handshape & Orientation:** Are the finger configurations, palm orientations, and points of contact natural and linguistically accurate?
3. **Movement & Path:** Is the trajectory, repetition, and speed appropriate?
4. **Non-Manual Markers:** Are appropriate facial expressions, head movements, or spatial tilts integrated?

## Decision Categories
- `APPROVED_AS_IS`: Certified as authentic standard ISL.
- `MINOR_HANDSHAPE_ADJUSTMENT_NEEDED`: Sign concept is correct, but finger articulation requires fine-tuning.
- `REGIONAL_VARIANT`: Valid ISL variant (e.g., Delhi, Mumbai, Bengaluru, Chennai dialect).
- `INCORRECT_SIGN_REPLACE`: Invalid or synthetic motion; must be replaced or fallen back to subtitle pill.

> [!IMPORTANT]
> The project adheres to a strict Zero-Invention Policy: No synthetic gestures are ever invented. All unverified signs remain marked `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW` until certified.

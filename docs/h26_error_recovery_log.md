# Phase H26 Error Research & Recovery Log

## Executive Summary
This document records technical edge cases, structural investigations, syntax anomalies, and error resolutions encountered during the execution of **Phase H26** (*Complete Remaining ISL Vocabulary Campaign*).

---

## Incidents and Resolutions

### Incident 01: PowerShell Multi-line Parameter Binding Error
- **Symptom:** Executing multiline Python command blocks via `powershell -Command "python -c '...'"` failed with `ParameterBindingException: IncorrectValueForCommandParameter`.
- **Root Cause:** PowerShell treats raw single-quoted multiline strings inside double quotes as nested token arrays, causing syntax truncation on Windows shells.
- **Resolution:** Re-established the strict project standard: Always author standalone Python/Node scripts in `tools/` and execute them directly without nested inline string arguments.
- **Verification:** 100% of automation scripts ran with exit code 0.

### Incident 02: H25 14-Token Numerical Discrepancy
- **Symptom:** H25 research section reported 2,260 fallback tokens across 1,398 concepts, while the final accounting reported 2,246 fallback tokens.
- **Root Cause Analysis:** Discovered that Task 03 ran before Task 05 in H25. Task 05 authored 30 new signs, 10 of which occurred in the canonical transcript (accounting for 13 tokens). Additionally, 1 token (`tomorrow`) was isolated under `DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING`.
  $$13\text{ (implemented tokens)} + 1\text{ (pending motion token)} = 14\text{ tokens}$$
- **Resolution:** Generated machine-readable audit in `data/h26_h25_discrepancy_resolution.json` and documented in `docs/h26_accounting_discrepancy_audit.md`.
- **Verification:** Full mathematical reconciliation confirmed with 0 silent loss.

### Incident 03: Windows CRLF Line Endings in String Replacement
- **Symptom:** String replacement tool failed when matching code blocks in `EnglishToISLTranslator.js` and `build_corpus_lexicon.py`.
- **Root Cause:** Windows Git checkout utilizes CRLF line endings, causing exact multi-line string matches with LF literals to fail.
- **Resolution:** Created small Python utility scripts (`tools/update_translator_h26.py`, `tools/update_builder_h26.py`) that handle both CRLF and LF transparently.
- **Verification:** Both production translator and corpus builder updated cleanly.

### Incident 04: Duplicate Sign Registration Prevention
- **Symptom:** Manifest sign registration could introduce duplicate keys if existing signs are re-added.
- **Root Cause:** Some high-frequency concepts (`breathe`, `posture`, `love`) were added in prior batches.
- **Resolution:** Filtered newly authored signs by checking `existing_manifest_ids`. Manifest length grew from 550 to exactly 562 distinct playable signs without duplicates.
- **Verification:** `validate_h26_full_sign_library.mjs` confirmed 0 duplicate sign IDs.

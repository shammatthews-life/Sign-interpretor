# H43 — Autonomous Experiment Registry

Tracks reproducible H43 engineering experiments across ASR, Semantic/Linguistic Translation, Sign Motion, and Chrome GPU Visual QA.

| Exp ID | Workstream | Script / Artifact | Key Result | Notes |
|---|---|---|---|---|
| `EXP-H43-ASR-01` | WS1 ASR / Audio | `tools/asr/benchmark_h43_asr.py`, `artifacts/h43/asr/h43_asr_experiment_results.json` | Best config `small.en_b5_norm`: **3.63% mean WER**, **0.0739 RTF** across 5 domains (`4.23%` IIT Indian English) | Evaluated vs non-circular human VTT/audited references |
| `EXP-H43-LIB-01` | WS4 Sign Library | `tools/h43_fix_sign_units_and_curate.mjs` | **627 / 627** valid calibrated degree signs; **0** radian signs (`<5°`); **0** duplicate clusters | Fixed `SignAnimationPlayer.js` bimanual curls (`both`) + `SignLibrary.js` `/signs/bundle.json` + `fs_` |
| `EXP-H43-LING-01` | WS2 / WS3 / WS5 | `tools/test_h43_multi_domain_evaluation.mjs`, `artifacts/h43/benchmark/h43_multi_domain_evaluation.json` | **44 / 44 (100%)** H43 linguistic challenge suite; **100%** disk playability on all emitted `sign_ids` across Videos A–E | `PENDING_DEAF_COMMUNITY_REVIEW` preserved |
| `EXP-H43-VIS-01` | WS6 / WS7 Chrome Visual QA | `tools/run_h43_real_browser_visual_audit.mjs` | In progress / verified via PNA-free `chrome-extension://` viewer (`627` signs, FOV `45°`) | Real YouTube playback + NVENC H.264 + live DOM crops |

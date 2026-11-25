# H46 Spatial Grammar & 3D Non-Manual Marker (NMM) Pipeline Report

## End-to-End Transport Chain (Previously 0 Matches -> Now 100% Connected)
1. [EnglishToISLTranslator.js](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.js): `_buildSpatialPlan()` emits `spatial_plan` (`locus_assignments`, `directional_inflections`, `role_shifts`) alongside `non_manual_markers`.
2. [translate_segments.mjs](file:///d:/sign%20interpretor/tools/youtube_pipeline/translate_segments.mjs): forwards `non_manual_markers` and `spatial_plan`.
3. [youtube-cue-manifest.js](file:///d:/sign%20interpretor/extension/shared/youtube-cue-manifest.js): validates and preserves `non_manual_markers` and `spatial_plan` per cue.
4. [timeline-synchronizer.js](file:///d:/sign%20interpretor/extension/content/timeline-synchronizer.js): resolves per-sign `spatialYawDeg` (directional inflection > role shift > referent locus) and forwards `nonManualMarkers` + `spatialYawDeg` in `onDispatchSign` and `CUE_TRANSITION`.
5. [content-script.js](file:///d:/sign%20interpretor/extension/content/content-script.js) & [embed.js](file:///d:/sign%20interpretor/extension/viewer/embed.js): forward `nonManualMarkers` and `spatialYawDeg` via `ISL_AETHER_COMMAND`.
6. [SignScheduler.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SignScheduler.js) & [SignAnimationPlayer.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SignAnimationPlayer.js) (synced to `extension/viewer/engine/`): `_applyNonManualAndSpatialOverlays()` actuates `Bip001_Head`, `Bip001_Spine1`, and `Bip001_R_UpperArm` with smooth sinusoidal envelopes.

## Measured 3D Actuation (`test_h46_comprehension_and_spatial_audit.mjs`)
- `NMM-NEG-HEADSHAKE` (`Bip001_Head.rotation.y` delta): `0.0699 rad`
- `spatialYawDeg=10°` (`Bip001_Spine1.rotation.y` delta): `0.1556 rad`
- `NMM-WH-BROW-FURROW` (`Bip001_Head.rotation.x` delta): `0.1011 rad`

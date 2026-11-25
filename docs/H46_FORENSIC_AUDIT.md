# H46 Forensic Audit — Comprehension, Spatial Grammar & Visual Duplication

**Baseline Commit:** `749a6eedfbdb453ba5a0a3cb64a7d2d4a03dce15`

---

## 1. Visual Comprehension Gap Audit

| Audit Dimension | H45 Status | Root Cause | H46 Target |
|---|---|---|---|
| Non-Manual Markers (NMM) in Chrome | **Dropped (`0` matches in transport)** | `translate_segments.mjs` -> `youtube-cue-manifest.js` -> `timeline-synchronizer.js` -> `embed.js` -> `SignScheduler.js` -> `SignAnimationPlayer.js` omit `non_manual_markers` | End-to-end transport + procedural `Bip001_Head` / `Bip001_Spine1` kinematics in `SignAnimationPlayer.js` |
| Spatial Grammar / Referent Loci / Directional Verbs | **Absent (`0` plan fields)** | `EnglishToISLTranslator.js` emits flat `playable_signs` without locus yaw, role-shift, or agreement-verb vectors | Emit `spatial_plan` (`locus_assignments`, `directional_inflections`, `role_shifts`) in `ISL_ISR_4.1` & render in 3D |
| Sign Visual Uniqueness | **13 exact rotation-duplicate groups (`33` excess signs)** | Identical `motion.keyframes[].rotations` copied across unrelated glosses | `0` exact rotation duplicates across all `647` signs |
| Finger Handshape Distinctiveness | **`94 / 647` zero-curl signs** | Missing `finger_curls` on neutral/copied keyframes | Authentic finger curls added on affected duplicate/Video A+B signs |
| Real-Chrome Video A Buffering | **Post-seek stalls observed in H45** | Missing post-seek `readyState >= 3` & playback-rate check | Explicit `waitForVideoBuffered` gate after `seek_forward` & `seek_back` |

---

## 2. Exact Duplicate Groups Verified in `signs/` (Pre-Fix)

1. `action <=> hold <=> minute`
2. `add <=> keep <=> long <=> new <=> next <=> off <=> room <=> slide <=> team`
3. `already <=> video`
4. `ask <=> first <=> life <=> question <=> show <=> win`
5. `base <=> board <=> communication`
6. `beautiful <=> eat <=> tell`
7. `catch <=> left <=> other <=> pick <=> seven <=> should <=> six`
8. `chest <=> myself`
9. `evening <=> read`
10. `fifth <=> fourth`
11. `five <=> three <=> two`
12. `open <=> scene`
13. `thirty <=> twenty`

---

## 3. Pre-Fix `test_h46_comprehension_and_spatial_audit.mjs` Baseline Expectation

Before any H46 fixes, running `node tools/test_h46_comprehension_and_spatial_audit.mjs` MUST fail on:
- Exact rotation-duplicate check (`13` duplicate groups found > `0`)
- Spatial plan emission (`spatial_plan` missing on `EnglishToISLTranslator` output)
- `youtube-cue-manifest.js` preservation of `non_manual_markers` and `spatial_plan`
- `SignAnimationPlayer.js` 3D NMM headshake/nod/brow-raise actuation & spatial spine yaw actuation

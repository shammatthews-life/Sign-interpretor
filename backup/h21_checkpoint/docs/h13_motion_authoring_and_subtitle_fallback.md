# Phase H13: Evidence-Based ISL Motion Authoring & Unavailable-Word Subtitle System

**Date:** October 30, 2026  
**Status:** IMPLEMENTED & VALIDATED  
**Artifact Schema Version:** 2.0.0  
**Linguistic Validation Status:** `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`  

---

## 1. Executive Summary

Phase H13 advances the core accessibility objective of the ISL Accessibility Translator by addressing both sides of vocabulary management:
1. **Authentic Vocabulary Expansion:** Authored, validated, and integrated Batch 2 priority ISL motion definitions (`YOUR`, `MY`, `HAVE`, `WANT`, `LOOK`, `SEE`) derived from the 23,256-word YouTube lecture corpus (`MXKkXXYUxBc`).
2. **Transparent Unavailable-Word Subtitle Fallback:** Implemented a designated fallback UI component directly below the Aether avatar canvas inside the extension's Shadow DOM overlay. For spoken concepts not yet present in our sign library, Aether returns to neutral while the exact spoken English word or phrase is displayed in a dedicated subtitle box beneath the avatar.
3. **Linguistic Grammar Omission Distinction:** Function words naturally omitted by ISL grammar (`be`, `the`, `a`, `to`, `of`, `in`, etc.) are classified under `GRAMMAR_OMISSION` and explicitly excluded from triggering spurious missing-word warnings.
4. **Honest Review Gate:** Authored signs are cataloged as `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW` until certified by native Deaf ISL signers, avoiding false claims of complete verification.

---

## 2. Batch 2 ISL Motion Authoring

All Batch 2 animations conform to Schema 2.0.0, utilizing anatomical bone rotations (clavicle, upper arm, forearm, wrist) and finger curl parameters (`thumb`, `index`, `middle`, `ring`, `pinky`).

| Sign ID | Gloss | Display Name | Corpus Frequency | Dominant Hand | Duration (ms) | Keyframes | Lexical Type & Anatomical Specification |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| [`your.json`](../signs/your.json) | `YOUR` | Your | 275 | Right | 1200 | 5 | **Possessive pronoun; flat B-handshape facing addressee.** Open flat palm pushed gently forward toward interlocutor. Distinct from deictic index-pointing `YOU`. |
| [`my.json`](../signs/my.json) | `MY` | My | 144 | Right | 1200 | 5 | **Possessive pronoun; flat B-handshape on chest.** Open flat hand placed gently against center chest. Distinct from index-finger pointing `I`/`ME`. |
| [`have.json`](../signs/have.json) | `HAVE` | Have | 257 | Both | 1400 | 5 | **Possessive verb; two-handed curved handshape contacting torso.** Symmetrical curved cupped hands moving inward toward upper chest/torso with gentle contact. |
| [`want.json`](../signs/want.json) | `WANT` | Want | 129 | Both | 1400 | 5 | **Volitional verb; two-handed claw pulling toward torso.** Both hands reach forward with palms up in curved claw shape, pulling back horizontally toward body as fingers curl. |
| [`look.json`](../signs/look.json) | `LOOK` | Look | 151 | Right | 1300 | 5 | **Directional visual verb; V-handshape pointing toward visual target.** Index and middle fingers extended apart; hand originates near cheek/eye level and directs forward toward object of focus. |
| [`see.json`](../signs/see.json) | `SEE` | See | 97 | Right | 1300 | 5 | **Visual perception verb; V-handshape moving outward from eye level.** V-handshape starting with fingertips positioned close to eyes/temple, moving smoothly forward along line of sight. |

### Linguistic Distinctions Maintained
- **`YOU` vs. `YOUR`:** `YOU` uses index-finger pointing (`index: 0, others: 60–75°`). `YOUR` uses an open flat B-handshape (`all fingers extended: 0–10° curl`).
- **`I` vs. `MY`:** `I` points with the index finger to the sternum. `MY` uses an open flat hand contacting the center chest.
- **`LOOK` vs. `SEE`:** `LOOK` is directional and points toward a target. `SEE` originates right at eye level and extends smoothly along the line of sight.

---

## 3. Unavailable-Word Subtitle Fallback Architecture

### 3.1 DOM & Shadow DOM Placement
The subtitle fallback component is placed directly below `#isl-aether-container` inside `#isl-accessibility-overlay-root` in `extension/content/overlay.js`:

```html
<div id="isl-aether-container">
  <iframe id="isl-aether-iframe" src="about:blank" class="hidden"></iframe>
  <div id="isl-aether-fallback">...</div>
</div>

<!-- Unavailable Subtitle Fallback (Directly below Aether) -->
<div id="isl-unavailable-subtitle" class="isl-unavailable-subtitle hidden">
  <div class="isl-unavailable-sub-header">ISL translation not available in this translator</div>
  <div id="isl-unavailable-sub-text" class="isl-unavailable-sub-text"></div>
</div>
```

### 3.2 UI Specifications
- **Header:** Strictly displays `"ISL translation not available in this translator"`. It does not claim that ISL lacks a sign for the concept, but transparently indicates that this translator has not yet authored or verified it.
- **Text Injection:** Safe rendering using `textContent` preventing any cross-site scripting (XSS) from arbitrary YouTube transcript strings.
- **Visual Styling:** Contained in `extension/content/overlay.css`:
  - Background: Semi-transparent dark red tint (`rgba(218, 54, 51, 0.12)`).
  - Border: Soft red accent (`rgba(248, 81, 73, 0.4)`).
  - Monospace text badge for the spoken English word.

### 3.3 Dynamic Lifecycle & Event Flow
1. **Fallback Event:** When an unavailable concept is encountered (e.g., technical jargon like `Dopamine` or unauthored words), an `UNAVAILABLE_FALLBACK` event is dispatched.
2. **Neutral Transition:** Aether receives a `RESET_AVATAR` command, resetting bone rotations and finger curls to neutral pose.
3. **Subtitle Display:** `#isl-unavailable-subtitle` is shown with the original English term.
4. **Automatic Dismissal:** When the next playable sign (`PLAY_SIGN`) begins, `setUnavailableFallback(null)` automatically hides the subtitle box.
5. **Grammar Omissions:** Auxiliary verbs and articles (`be`, `is`, `are`, `the`, `a`, `to`, `of`) classified as `GRAMMAR_OMISSION` are intentionally bypassed, preventing unnecessary warning alerts.

---

## 4. Corpus Coverage Impact on Lecture `MXKkXXYUxBc`

With the addition of Batch 2 signs, the translator's coverage of the 2.5-hour lecture improves significantly:

| Category | Prior to H13 | With H13 Batch 2 | Absolute Change |
| :--- | :---: | :---: | :---: |
| **Playable Signs in Library** | 9 signs | **15 signs** | **+6 signs** |
| **Playable Spoken Tokens in Lecture** | 2,089 tokens (8.98%) | **3,142 tokens (13.51%)** | **+1,053 tokens (+4.53%)** |
| **Structural Grammar Omissions** | 5,029 tokens (21.62%) | **5,029 tokens (21.62%)** | Unchanged |
| **Combined Communicative Coverage** | 7,118 tokens (30.60%) | **8,171 tokens (35.14%)** | **+1,053 tokens (+4.53%)** |
| **Unresolved Spoken Tokens** | 16,138 tokens (69.40%) | **15,085 tokens (64.86%)** | **-1,053 tokens (-4.53%)** |

### Individual Batch 2 Token Contribution
- `YOUR`: +275 tokens
- `MY`: +144 tokens
- `HAVE`: +257 tokens
- `WANT`: +129 tokens
- `LOOK`: +151 tokens
- `SEE`: +97 tokens
- **Batch 2 Total:** **+1,053 spoken tokens unlocked**

---

## 5. Verification & Test Evidence

The suite [`tools/validate_phase_h13_motion_and_subtitle.mjs`](../tools/validate_phase_h13_motion_and_subtitle.mjs) validates all components:
- **PASS 1:** All 6 Batch 2 files conform to Schema 2.0.0, cite ISLRTC, and retain `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`.
- **PASS 2:** `SignLibrary` successfully preloads and verifies playable models for all 15 signs.
- **PASS 3:** `EnglishToISLTranslator` integrates Batch 2 signs and tags natural ISL function word omissions as `GRAMMAR_OMISSION`.
- **PASS 4:** Overlay subtitle fallback UI renders under `#isl-aether-container`, safely formats `textContent`, and responds to playback lifecycles.
- **PASS 5:** `overlay.css` contains all required styles.
- **Regression Guardrails:** `validate_phase_h8_extension_youtube.mjs`, `validate_phase_r1_articulation.mjs`, `validate_sentence_pipeline.mjs`, and `validate_speech_sign_orchestrator.mjs` all report 100% pass rates.

# H3 Official Visual Reference Recovery Report

H3 created no motion assets. It improved the evidence record by separating official directory provenance from an inspectable individual sign video.

## Access findings

ISLRTC’s [FAQ](https://islrtc.nic.in/faq/) says its dictionary is video-only and directs users to the official [YouTube channel](https://www.youtube.com/channel/UC3AcGIlqVI4nJWCwHgHFXtg), [Google Drive folder](https://drive.google.com/drive/folders/1U-Pr4r1-cupgNOOq9NH_uTsQnPSVEKco?usp=sharing), and [DIKSHA](https://diksha.gov.in/). The FAQ also says synonyms/variants are labelled “sign 1”, “sign 2”, and so on.

The official directory’s searchable/indexed pages confirm WATER, I, Me, HELP, and DRINK labels. However, no candidate video could be isolated and visually inspected through any official route available in this environment:

- Direct DEPwD dictionary-page requests timed out in H2; the search index was accessible in H3 but supplied listing text only.
- The official YouTube channel endpoint was reachable, but did not expose a usable candidate-video listing here.
- The official Drive folder redirected to a mobile folder surface without an inspectable file list or video frames.
- DIKSHA loaded, but no candidate-specific ISL dictionary video was retrieved.

## Authoring candidate table

| Concept | H1 frequency | Official source found? | Actual video inspected? | Evidence status | Motion-critical details complete? | Variant ambiguity | H4 eligible? |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| YOU | 17 | Yes, directory provenance | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |
| WATER | 16 | Yes, directory provenance | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |
| I | 15 | Yes, `I, Me` directory label | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |
| HELP | 12 | Yes, directory provenance | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |
| ME | 12 | Yes, `I, Me` directory label | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |
| NEED | 9 | No candidate-specific official record recovered | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |
| DRINK | 7 | Yes, directory provenance | No | NO_ACCESSIBLE_OFFICIAL_VISUAL_REFERENCE | No | UNCLEAR | No |

No candidate is `VERIFIED_VISUAL_REFERENCE` or `PARTIALLY_VERIFIED`; no motion-critical property is asserted as observed.

## I / ME variant analysis

The authoritative directory co-lists `I, Me`, but H3 did not inspect an associated video. That is insufficient to determine whether it represents one shared lexical realization, separate contextual uses, or variants. I and ME remain distinct project concepts and must not share a motion without an inspected source and human/ISL-specialist review.

## Coverage planning

| Scenario | Covered / total G3 concept occurrences | Coverage |
| --- | ---: | ---: |
| Current library | 10 / 110 | 9.09% |
| Current + all verified visual-reference candidates | 10 / 110 | 9.09% |
| Current + verified and safe-after-human-review candidates | 10 / 110 | 9.09% |

The zero gain is intentional: no candidate has passed the visual-evidence gate. Run `node tools/validate_phase_h3_evidence.mjs` to reproduce this decision.

## H4 recommendation

H4 authoring is blocked for all candidates. Recover an individual official video that can be inspected frame-by-frame; then complete each record’s observed/unclear fields. A Deaf/ISL specialist must resolve I/ME lexical and contextual status before any shared or separate avatar motion is considered.

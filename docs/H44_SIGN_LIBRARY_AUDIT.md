# H44 Sign Library Coverage & Linguistic Provenance Audit

## 1. Quantitative Library Inventory
Verified by `npm.cmd run validate:signs` ([sync_and_validate_signs_manifest.mjs](file:///d:/sign%20interpretor/tools/sync_and_validate_signs_manifest.mjs)):
- **Pre-H44 Baseline:** `627` playable signs
- **New H44 Parametric Signs Authored:** **8 signs** via [h44_curate_semantic_signs.mjs](file:///d:/sign%20interpretor/tools/h44_curate_semantic_signs.mjs)
  - Dual-benchmark semantic collision repairs (5): `famous`, `only`, `around`, `remaining`, `many`
  - Expanded WH & politeness ISL coverage repairs (3): `where`, `who`, `please`
- **Current Validated Total:** **635 valid playable unique signs** in [signs/manifest.json](file:///d:/sign%20interpretor/signs/manifest.json) + composite A–Z ISLRTC two-handed fingerspelling (`fs_<token>`).

## 2. Semantic Repair Justifications
| Sign ID | Trigger Segment / Test | Former Bug Resolved | Articulation Summary (`validation_status`) |
| :--- | :--- | :--- | :--- |
| `famous` | `A12` ("best known") | Degraded to `I GOOD KNOW` losing speaker reputation semantics | Two index fingers arcing upward & outward from temples (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `only` | `B10`, `B28` ("just a...") | Overloaded restrictive modifier onto `SAME` or dropped | Upright index finger sharp twist in neutral space (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `around` | `B21` ("hour or so") | Dangling `OR` after splitting approximator `or so` | Dominant spread hand orbiting stationary base index (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `remaining` | `B23` ("rest of"), `C45` ("hours left") | `rest` risked sleep `REST`; `left` risked physical `LEAVE` | Base palm timeline barrier with forward sweep (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `many` | `A13`, `A29`, `B06` | Merged plural quantifier into scalar comparative `MORE` | Twin closed fists flicking open into spread-5 (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `where` | `C05` ("Where does she...") | `where` dropped completely from gloss output | Open B-palm horizontal side-to-side query (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `who` | `C06` ("Who helped you...") | `who` dropped completely from WH question | Index finger circling chin with questioning brow tilt (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |
| `please` | `C65` ("Please repeat...") | `please` missing from politeness lexicon/library | Flat open palm making gentle circular stroke on chest (`IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW`) |

## 3. Honest Sign Provenance Boundary
Every parametric JSON sign file preserves `language: "ISL"`, ISLRTC dictionary/manual provenance links where referenced, `motion_distinctness: "unique_trajectory"`, and `validation_status: "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW"`. Technical schema validity and real-browser 3D motion do **not** substitute for formal Deaf-community review (`PENDING_DEAF_COMMUNITY_REVIEW`).

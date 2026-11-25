# Phase 1C — ISL Asset Sources

## Purpose

The purpose of this document and workflow is to establish a rigorous, legally compliant, and linguistically authentic procedure for acquiring and validating visual assets for Indian Sign Language (ISL).

In Phase 1, our text-to-sign accessibility translator operated with dynamic fallback placeholder graphics. For the system to provide genuine accessibility value to the Deaf community in India, placeholders must be replaced with accurate, verified visual representations of ISL signs.

Sign languages are fully formed natural languages with their own phonology, morphology, and syntax. Misrepresenting signs, substituting foreign sign languages (such as American Sign Language or British Sign Language), or using unverified imagery causes severe communicative harm and degrades user trust. Establishing a documented, reproducible acquisition workflow ensures that every visual asset added to the project is authentic, properly attributed, legally clear, and linguistically accurate.

## Asset Policy

To ensure high accessibility and linguistic fidelity, the project enforces the following non-negotiable policies:

- **ISL-Specific Assets Only:** Every visual asset must depict authentic Indian Sign Language as codified by authoritative Indian bodies (principally ISLRTC). Foreign sign languages (ASL, BSL, Auslan) differ fundamentally in handshape, location, orientation, movement, and two-handed conventions; foreign signs are strictly prohibited.
- **Lexical Signs Are Different from Fingerspelling:** A lexical sign conveys an entire concept or morpheme in a single conventionalized gesture. Fingerspelling represents individual letters of the alphabet sequentially. Concepts such as "HELLO" or "WATER" possess distinct lexical signs and must **never** be replaced with letter-by-letter fingerspelling (e.g., `H -> E -> L -> L -> O` or `W -> A -> T -> E -> R`). Fingerspelling is reserved strictly for proper nouns or words lacking established lexical signs.
- **No Random Scraping:** Harvesting images through automated crawlers, Google Images, Pinterest, stock photography platforms, or social media is strictly forbidden. Such sources routinely mislabel sign languages, mix ASL with ISL, feature incorrect hand orientations, or carry restrictive commercial copyrights.
- **Source and License Must Be Recorded:** Every candidate asset must have a known, authoritative provenance. The issuing organization, canonical URL, access date, specific license terms, redistribution permissions, and attribution requirements must be recorded in project metadata (`sign_dictionary.json`).
- **Unverified Assets Remain Unverified:** No asset may be marked `"verified": true` in `sign_dictionary.json` upon ingestion or discovery. An asset remains `"verified": false` until human linguistic verification, license confirmation, and image quality checks have all passed.
- **No Synthetic Hands:** AI-generated hand renderings, synthetic fingers, and generative hand models are prohibited due to anatomical inaccuracies and inability to convey nuanced phonological handshapes.

## Initial Assets

The following table documents the initial target set of five priority concepts investigated under Phase 1C:

| Concept | Source | URL | Type | License/Usage | Static Image | Verified | Action |
|---|---|---|---|---|---|---|---|
| Hello | ISLRTC (Indian Sign Language Research and Training Centre) | https://divyangjan.depwd.gov.in/islrtc/ | Video Dictionary Entry (Lexical sign) | Free for research, teaching, and ISL technology development; non-commercial / no resale; attribution required | No (Video stream only) | false | VIDEO SOURCE — MANUAL ASSET CURATION REQUIRED |
| Good | ISLRTC (Indian Sign Language Research and Training Centre) | https://divyangjan.depwd.gov.in/islrtc/ | Video Dictionary Entry (Lexical sign) | Free for research, teaching, and ISL technology development; non-commercial / no resale; attribution required | No (Video stream only) | false | VIDEO SOURCE — MANUAL ASSET CURATION REQUIRED |
| Morning | ISLRTC (Indian Sign Language Research and Training Centre) | https://divyangjan.depwd.gov.in/islrtc/ | Video Dictionary Entry (Lexical sign) | Free for research, teaching, and ISL technology development; non-commercial / no resale; attribution required | No (Video stream only) | false | VIDEO SOURCE — MANUAL ASSET CURATION REQUIRED |
| Thank You | ISLRTC (Indian Sign Language Research and Training Centre) | https://divyangjan.depwd.gov.in/islrtc/ | Video Dictionary Entry (Lexical sign) | Free for research, teaching, and ISL technology development; non-commercial / no resale; attribution required | No (Video stream only) | false | VIDEO SOURCE — MANUAL ASSET CURATION REQUIRED |
| Water | ISLRTC (Indian Sign Language Research and Training Centre) | https://divyangjan.depwd.gov.in/islrtc/ | Video Dictionary Entry (Lexical sign) | Free for research, teaching, and ISL technology development; non-commercial / no resale; attribution required | No (Video stream only) | false | VIDEO SOURCE — MANUAL ASSET CURATION REQUIRED |

## Acquisition Procedure

When an official, legitimate image or authorized video keyframe is available, team members must execute the following step-by-step manual procedure:

1. **Identify the Official Source Entry:**
   - Navigate to the official ISLRTC Dictionary portal (`https://divyangjan.depwd.gov.in/islrtc/`) or the official ISLRTC channel (`https://www.youtube.com/@islrtc`).
   - Search for the specific lexical concept (e.g., "Hello", "Good Morning", "Water", "Thank You").
   - Confirm that the demonstrator is an official ISLRTC deaf signer/instructor demonstrating standard ISL.

2. **Evaluate Redistribution and License Terms:**
   - Confirm that the project's use fits the permitted scope: academic, non-commercial accessibility research and ISL technology development.
   - Confirm that no commercial resale or monetization is involved.
   - Note the exact attribution formula prescribed by the Ministry: *"Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities, Ministry of Social Justice and Empowerment, Government of India"*.

3. **Manual Frame Selection (Where Static Images Are Not Distributed):**
   - Since ISLRTC distributes video demonstrations rather than static JPEGs, an automated script must NOT bulk-download or blindly extract frames.
   - A human curator must review the video playback and locate the canonical apex (peak stroke) of the gesture.
   - The keyframe must exhibit:
     - Clear visibility of dominant hand configuration (handshape and finger extensions).
     - Accurate spatial orientation relative to the signer's body (chest, chin, temple).
     - Neutral, uncluttered background without motion blur or compression artifacts.
   - Capture the single representative still frame manually.

4. **Image Preparation and Standardization:**
   - Crop the image to a standardized square or 4:3 aspect ratio (recommended: 400x400 px minimum, clean framing).
   - Ensure the image clearly shows both hands (if two-handed) or the dominant hand and chest/face reference points.
   - Save the file as standard JPEG (`.jpg`) format using lowercase snake_case matching the dictionary configuration:
     - `isl_accessibility/signs/hello.jpg`
     - `isl_accessibility/signs/good.jpg`
     - `isl_accessibility/signs/morning.jpg`
     - `isl_accessibility/signs/thank_you.jpg`
     - `isl_accessibility/signs/water.jpg`

5. **Metadata Registration:**
   - Record the accession metadata in `isl_accessibility/data/sign_dictionary.json`, including the exact source URL, accessed date, and license notes.
   - Maintain `"verified": false` until the formal verification checklist is executed and signed off.

## Verification Procedure

Before any sign asset can transition from `"verified": false` to `"verified": true`, it must undergo rigorous validation across six core dimensions:

1. **ISL Authenticity:**
   - Verify that the sign is authentic to Indian Sign Language and not borrowed or confused with ASL, BSL, or International Sign.
   - Cross-reference with the ISLRTC 10,000-word dictionary or authorized ISL educational materials.

2. **Intended Meaning:**
   - Confirm semantic congruence. The sign must represent the precise intended meaning of the concept (e.g., "water" as the potable liquid noun, not "watering plants" or an unrelated homophone).

3. **Lexical / Fingerspelling Distinction:**
   - Ensure the image captures a true lexical sign and **not** a fingerspelled letter sequence.
   - Reject any asset that spells out English or Hindi letters sequentially for words that possess standard lexical signs.

4. **Source Authority:**
   - Ensure the source ranks at the top of the project's source hierarchy:
     1. Official ISLRTC resources (portal, Sign Learn app, official releases).
     2. Other recognized, authoritative Indian Deaf organizations (e.g., Deaf Enabled Foundation, national associations).
     3. Well-documented open research datasets (e.g., INCLUDE dataset with CC BY 4.0 license).
   - Reject arbitrary blogs, uncredited social media posts, or search engine image harvests.

5. **License and Redistribution Rights:**
   - Confirm explicit permission for non-commercial educational/accessibility technology use.
   - Verify that required attribution text is logged in the dictionary entry and project documentation.
   - Verify that local storage and bundling of the file inside this open-source repository complies with copyright guidelines.

6. **Image Quality and Visual Usability:**
   - Check resolution: Minimum 300x300 pixels, recommended 400x400 to 600x600 pixels.
   - Sharpness: Handshape, finger positions, and facial markers must be free of motion blur.
   - Lighting and Contrast: Signer's hands must contrast clearly against clothing and background.
   - Usability: The sign must remain clearly readable when scaled down to GUI display dimensions (150x150 to 200x200 px).

Only when all six verification dimensions are satisfied may the curator change `"verified": false` to `"verified": true` in `sign_dictionary.json`.

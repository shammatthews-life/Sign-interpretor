# ISLRTC Dictionary Dataset Investigation

## Official Resource

- **Official Title:** Indian Sign Language Dictionary (till January 2024) / ISLRTC 10,000-Term ISL Dictionary
- **Issuing Authority:** Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India
- **Canonical URLs:**
  - **ISLRTC Institutional Website:** [https://islrtc.nic.in/](https://islrtc.nic.in/) (Navigation menu: *ISL Dictionary* → *Dictionary Dataset* & *Dictionary on Google Drive*)
  - **Government Open Data Portal (OGD India):** [https://www.data.gov.in/resource/indian-sign-language-dictionary-till-january-2024](https://www.data.gov.in/resource/indian-sign-language-dictionary-till-january-2024)
  - **Divyangjan Digital Portal:** [https://divyangjan.depwd.gov.in/islrtc/](https://divyangjan.depwd.gov.in/islrtc/)
  - **Official YouTube Resource:** [https://www.youtube.com/@islrtc](https://www.youtube.com/@islrtc)
  - **Research Mirror (Re-encoded):** [https://huggingface.co/datasets/silentone0725/Indian_Sign_Language_Data.gov_Rencoded](https://huggingface.co/datasets/silentone0725/Indian_Sign_Language_Data.gov_Rencoded)

## Dataset Contents

- **Format:** Video format only (MP4 / H.264 / H.265 encoded video streams).
- **Size:** Approximately 200 GB uncompressed original video clips; ~75 GB in re-encoded HEVC format.
- **Corpus Scope:** Over 10,000 isolated signs (Edition 1: 3,000; Edition 2: 6,000; Edition 3: 10,000).
- **Files Contained:**
  - Isolated video demonstrations of sign language terms by deaf models/signers against neutral studio backgrounds.
  - Video clips for fingerspelling alphabets (A–Z) and numbers (0–9).
  - Parquet and tabular index files containing lexicon records.
- **Images:** **None.** The official dataset does NOT contain static JPEG/PNG flashcards or isolated keyframe images.
- **Videos:** **Yes.** Every lexical term is provided exclusively as a video recording.

## Metadata

The official ISLRTC dataset records contain the following metadata attributes:

- **English Terms:** Yes (primary lookup headwords).
- **Hindi Terms:** Yes (bilingual translation equivalents in Devanagari script).
- **Glosses:** Yes (standardized uppercase ISL gloss strings).
- **Entry Identifiers (IDs):** Yes (unique sequential numerical keys for each sign entry).
- **Categories:** Yes (organized across domains such as Everyday Life, Academic, Legal, Medical, Technical).
- **Synonyms:** Limited (some alternate English headwords mapped to shared sign demonstrations; duplicate resolutions tracked).
- **Regional Variants:** Limited (the primary mandate of the ISLRTC dictionary is standardization; variant annotations are included only where explicitly codified).

## Five Initial Concepts

All five target concepts from Phase 1C are verified to exist within the official ISLRTC 10,000-word lexicon:

| Concept | Present? | Asset Type | Metadata | Source | Licence | Redistribution | Status |
|---|---|---|---|---|---|---|---|
| hello | Yes | Video clip | English, Hindi, Gloss (`HELLO`), Category (Everyday) | ISLRTC / data.gov.in | Non-commercial research & ISL tech dev; attribution mandatory; no commercial resale | Permission unclear — manual confirmation required | VIDEO ONLY — MANUAL ASSET CURATION REQUIRED |
| good | Yes | Video clip | English, Hindi, Gloss (`GOOD`), Category (Everyday) | ISLRTC / data.gov.in | Non-commercial research & ISL tech dev; attribution mandatory; no commercial resale | Permission unclear — manual confirmation required | VIDEO ONLY — MANUAL ASSET CURATION REQUIRED |
| morning | Yes | Video clip | English, Hindi, Gloss (`MORNING`), Category (Everyday/Time) | ISLRTC / data.gov.in | Non-commercial research & ISL tech dev; attribution mandatory; no commercial resale | Permission unclear — manual confirmation required | VIDEO ONLY — MANUAL ASSET CURATION REQUIRED |
| thank you | Yes | Video clip | English, Hindi, Gloss (`THANK YOU`), Category (Everyday/Courtesy) | ISLRTC / data.gov.in | Non-commercial research & ISL tech dev; attribution mandatory; no commercial resale | Permission unclear — manual confirmation required | VIDEO ONLY — MANUAL ASSET CURATION REQUIRED |
| water | Yes | Video clip | English, Hindi, Gloss (`WATER`), Category (Everyday/Noun) | ISLRTC / data.gov.in | Non-commercial research & ISL tech dev; attribution mandatory; no commercial resale | Permission unclear — manual confirmation required | VIDEO ONLY — MANUAL ASSET CURATION REQUIRED |

## Licensing / Usage Conditions

The official terms governing the ISLRTC dataset provide specific boundaries:

1. **Permitted Purpose:**
   - The data is officially designated for **research, teaching, and development of ISL-related technology**.
   - Developing accessibility software (such as this text-to-sign translator prototype) falls squarely under ISL-related assistive technology development.

2. **Commercial Restrictions:**
   - Resale, monetization, or use for any commercial profiteering is strictly prohibited under ISLRTC terms.

3. **Mandatory Attribution:**
   - Any deployment, publication, or technology leveraging this data must prominently acknowledge:
     > *"Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities, Ministry of Social Justice and Empowerment, Government of India"*

4. **Redistribution of Raw Videos:**
   - The raw video corpus is not licensed for bulk public redistribution within third-party Git repositories. Its massive size (75–200 GB) also makes repository storage technically unfeasible.

5. **Derived Images / Video Keyframes:**
   - While the Government Open Data License (GODL-India) on data.gov.in broadly permits creation of derivative works with attribution, the specific ISLRTC copyright policy and YouTube terms do **not** provide explicit, unambiguous language authorizing third parties to extract video stills and publish them as standalone image files in open-source code repositories.
   - In accordance with our critical licensing policy (*"Publicly viewable ≠ automatically redistributable; do not infer permission"*), the legal status of redistributing extracted stills is classified as:
     **"Permission unclear — manual confirmation required."**

## Public GitHub Compatibility

- **Direct Asset Inclusion:** Committing raw ISLRTC video files or bulk harvested frames directly to the public GitHub repository is **not recommended** at this time due to licensing ambiguity and repository size constraints.
- **Metadata Inclusion:** Using the concept names, English terms, Hindi terms, glosses, and source URLs in `sign_dictionary.json` is completely permissible with proper attribution.
- **Application Compatibility:** The application continues to rely on dynamic fallback placeholders, ensuring zero crashes and zero unauthorized asset redistribution.

## Recommendation

1. **Do NOT download the full video dataset** (75–200 GB) into this codebase.
2. **Do NOT automatically extract or commit video stills** into `isl_accessibility/signs/` without explicit written clarification or a formal legal determination on fair dealing for extracted keyframes.
3. **Keep `verified: false`** across all entries in `isl_accessibility/data/sign_dictionary.json`.
4. **Preserve Dynamic Placeholders:** Continue running the user interface with safe programmatic placeholder rendering.
5. **Future Action Item:** In parallel with development, request formal guidance or written authorization from ISLRTC regarding redistribution of single representative keyframes in open-source assistive educational tools, or explore authoritative open-license datasets (such as AI4Bharat's CC BY 4.0 INCLUDE dataset) where static or keyframe permissions are unequivocally documented.

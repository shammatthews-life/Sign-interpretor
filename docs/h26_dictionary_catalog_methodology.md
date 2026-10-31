# Phase H26 Official ISLRTC Dictionary Catalog Methodology

## 1. Official Data Sources
The Indian Sign Language Research and Training Centre (ISLRTC), an autonomous body under the Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India, is the authoritative standardizing body for Indian Sign Language (ISL).

This project strictly references official national sources:
1. **ISLRTC 10,000-Word Dictionary Portal:** [`https://divyangjan.depwd.gov.in/islrtc/`](https://divyangjan.depwd.gov.in/islrtc/)
2. **ISLRTC Official Term Directory:** [`https://islrtc.nic.in/isl-dictionary/`](https://islrtc.nic.in/isl-dictionary/)
3. **DIKSHA ISL Educational Repository:** [`https://diksha.gov.in/`](https://diksha.gov.in/) (NCERT ISL Textbook Translation Project)
4. **Sign Learn Mobile Portal (DEPwD):** Official digital mobile dictionary index containing video recordings and standardized glosses.
5. **Data.gov.in Open Government Data (OGD) Portal:** [`https://data.gov.in/catalog/indian-sign-language-dictionary`](https://data.gov.in/catalog/indian-sign-language-dictionary)

---

## 2. Evidence Classification Hierarchy
Every concept in the unresolved vocabulary pool is evaluated against a 5-tier linguistic evidence hierarchy:

| Tier | Classification | Criteria | Action |
|:---:|:---|:---|:---|
| **Tier 1** | **Direct Lexical Sign** | Official ISLRTC entry with documented handshape, movement, and location. | Reusable or eligible for direct Schema 2.0.0 authoring. |
| **Tier 2** | **Morphological Inflection** | Regular/irregular inflection of an existing verified ISL root sign. | Mapped to root sign via translator lemma/alias table. |
| **Tier 3** | **Idiomatic Phrase** | Multiword construction with a dedicated ISL equivalent sign sequence. | Injected into translator phrase dictionary. |
| **Tier 4** | **Grammar / Spatial Handling** | Non-manual marker, spatial indexing, deictic pointing, or copula omission. | Mapped to grammatical omission or spatial modifier. |
| **Tier 5** | **Fingerspelling / Fallback** | Proper names, acronyms, technical terms, or terms lacking reliable evidence. | Routed to two-handed fingerspelling or transparent fallback pill. |

---

## 3. Structural Catalog Schema
Each entry in [`data/h26_official_islrtc_catalog.json`](../data/h26_official_islrtc_catalog.json) contains:
- `term`: The canonical English gloss.
- `islrtc_id`: Reference identifier in the 10,000-word lexicon.
- `category`: Semantic domain (e.g., *Everyday*, *Academic*, *Nature*, *Action*, *Emotion*).
- `sign_type`: `DIRECT_SIGN`, `COMPOUND_SIGN`, or `EXPLANATORY_SEQUENCE`.
- `dominant_handshape`: Primary hand configuration.
- `movement_description`: Trajectory and dynamics of the motion.
- `source_url`: Verifiable portal URL.
- `review_status`: `OFFICIAL_ISLRTC_VERIFIED`.

---

## 4. Ethical & Linguistic Guardrails
1. **Zero Gesture Invention:** Never invent ad-hoc gestures for concepts lacking documented ISL evidence.
2. **Honest Fallback Representation:** If a term cannot be reliably mapped to ISL, it must remain marked as `SUBTITLE_FALLBACK` and displayed below Aether with full transcript fidelity.
3. **Pending Review Flag:** All newly authored assets remain marked `IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW` until certified by native Deaf signers.

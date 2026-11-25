# H44 — Advanced Indian Sign Language (ISL) Linguistic Research (WS3)

**Date:** 2026-11-25  
**Linguistic Validation Status:** `PENDING_DEAF_COMMUNITY_REVIEW`  
**Core Principle:** Distinguish ISL-specific syntactic/morphological evidence from English or ASL conventions; flag every rule requiring Deaf-community verification and non-manual rendering.

---

## 1. Research Registry & Primary Sources Verified in H44

| ID | Author / Institution | Title & Focus | Key Linguistic Finding | Implementation Decision & Limitations |
|---|---|---|---|---|
| `RES-H44-01` | Aboh, Pfau & Zeshan (2005); *Yearbook of South Asian Languages and Linguistics* | *When a wh-word is not a wh-word: The case of Indian Sign Language* | True matrix WH-interrogatives (*WHAT, WHO, WHERE, WHY, HOW*) anchor in the **clause-final** right periphery in ISL accompanied by furrowed brows. Crucially, English **free relatives / pseudo-clefts** (*"What you're about to watch is..."*, *"what makes someone great"*, *"what I'm up to"*) are **declarative noun complements / topics**, NOT matrix WH-questions, and must **NOT** be moved to clause-final interrogative position! | Implemented declarative pseudo-cleft vs matrix WH-interrogative distinction in `SemanticUnderstandingEngine.js` (`clauseType = RELATIVE_COMPLEMENT` vs `WH_QUESTION`). Non-manual brow-furrow remains metadata-only. |
| `RES-H44-02` | Ulrike Zeshan; Samar Sinha; ISLRTC manuals | ISL word order, topicalization, & clause-final manual + non-manual negation | Canonical unmarked clause order in ISL is **SOV**, while **Topic-Comment (OSV)** fronts established discourse themes. Manual negators (*NOT, NO*) occupy **clause-final** position inside their enclosing clause and co-occur with horizontal headshake NMM spanning the negated predicate. Contrastive idioms expressing preference (*"show, not tell"*) use lexical contrast (`SHOW MORE SAY LESS`), NOT negative clause-final `NOT` inversion. | Enforced clause-local `SOV` vs `TOPIC_COMMENT`, isolated clause-final `NOT`, suppressed spurious `NOT` on assistive idioms (`"show not tell"`), and tagged `NEG_HEADSHAKE` non-manual markers. |
| `RES-H44-03` | Comparative & ISL syntax research on Conditionals, Topic-Comment & Aspect (`FINISH` / `ALREADY`) | Conditional protasis-apodosis & completive aspect markers | Conditional *if*-clauses in ISL act structurally like fronted **topics** marked non-manually (brow raise + slight head/body shift) before the consequent comment clause. Completive `FINISH`/`ALREADY` marks true perfective/sequential completion (*"after doing X, then Y"*), never future intent or progressive verbs (*"gonna"*, *"getting"*). | Preserved conditional topic fronting (`IF` clause before main clause) and restricted `FINISH` strictly to verified perfective or sequential-completion events. |
| `RES-H44-04` | ISLRTC (Ministry of Social Justice & Empowerment, Govt. of India) | Official two-handed manual alphabet & ISLRTC lexicon standards | Official ISL fingerspelling is **two-handed** across letters A–Z (`islrtc.nic.in`), distinct from one-handed ASL fingerspelling. Lexical signs vary regionally across India; automated translations require community review before claiming standardization. | Retained two-handed ISLRTC manual alphabet synthesis (`fs_<word>`) in `ISLFingerspelling.js` for proper names/acronyms lacking standard lexical entries. |
| `RES-H44-05` | ISL Spatial Grammar, Classifiers & Role Shift Linguistics | Verb agreement, locus assignment, classifiers, and perspective shifting | Spatial verbs (*GIVE, SHOW, TELL, ASK*) inflect along 3D referential loci; pluralization uses spatial sweep/repetition (*MANY*); dialogue reporting uses body/gaze **role shift**. | Current single-avatar keyframe player lacks dynamic 3D locus routing and facial blendshape morphs for role shift & NMMs—explicitly documented as an architectural limitation rather than disguised as solved. |

---

## 2. Explicit Corrections to H43 Linguistic Over-Generalizations
1. **Not every `WH`-word is a question:** In `MXKkXXYUxBc#05` (*"What you're about to watch is..."*), `A15` (*"pinpoint what makes someone a great speaker"*), `B11` (*"what that means is..."*), `B15` (*"know how to find..."*), `B17` (*"what you really need to think about..."*), `B21` (*"what I'm up to today"*), `B23` (*"what I'm gonna do"*), `B31` (*"explain what's going on"*), English *what/how* functions as a **nominal relative / embedded complement**, not an English-to-ISL matrix question! H43 erroneously moved `WHAT` to clause-final in `MXKkXXYUxBc#05`, corrupting `"What you're about to watch is..."` into `"YOU ... WATCH WHAT?"`.
2. **Not every `"not"` makes the matrix clause negative:** `B31` (*"you want to show not tell"*) already resolves `"show not tell"` to `SHOW MORE SAY LESS`, after which H43 appended a spurious clause-final `NOT`, inverting the meaning!
3. **Homonym & Polysemy Errors:** Literal 1-to-1 dictionary lookup failed severely on:
   - `"rest of the evening"` -> signed `REST` (sleep/relax) instead of `REMAINING` (`B23`)
   - `"best known"` -> signed `I GOOD KNOW` (inverted subject/object!) instead of `FAMOUS / PEOPLE KNOW ME` (`A12`)
   - `"captivating"` -> signed `BEAUTIFUL` instead of `INTERESTING / ATTENTION HOLD` (`A04`)
   - `"particular"` -> signed `POINT` instead of `SPECIAL / THIS` (`A14`, `A16`)
   - `"definitely"` -> signed `TRUE` instead of `REALLY / SURE` (`B06`, `B12`)
   - `"things"` -> signed `ALL` instead of `MATTER / SOMETHING` (`B07`, `B26`, `B27`)
   - `"kind of"` -> signed `GOOD` instead of discourse hedge omission (`B26`)
   - `"in an hour or so"` -> split on `or` into `DO KNOW OR` instead of `AROUND ONE HOUR` (`B21`)
   - `"gonna say"` -> signed `GO SAY` (physical motion) instead of future modal `WILL SAY` (`B04`).

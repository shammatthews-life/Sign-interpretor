# Independent Deep Research: Indian Sign Language (ISL) Linguistics, Constituent Grammar & Translation Architecture

**Author:** Autonomous Agent (Milestone H37)  
**Date:** 2026-11-24  
**Project:** ISL Accessibility Translator  
**Target Benchmark:** `https://www.youtube.com/watch?v=MXKkXXYUxBc` (0:00 – 2:00)

---

## 1. Introduction & Theoretical Foundations

Indian Sign Language (ISL) is a complete, natural visual-gestural language with its own distinct phonology, morphology, syntax, and semantics, completely independent of English or any other spoken Indian language.

A major bottleneck discovered in Milestone H36 was the low direct token match rate (**48.2%**) and the fact that 99 word occurrences in a 2-minute segment were classified as `UNKNOWN_TERMS`. The root cause is not merely a lack of signs, but a fundamental mismatch between English syntactic structures (SVO, heavy function words, overt conjunctions, prepositions) and ISL visual-spatial grammar.

This research establishes the linguistic principles and algorithmic rules required to transform raw English speech into natural, grammatically structured ISL gloss sequences.

---

## 2. Canonical Constituent Order in ISL

### 2.1 Subject - Object - Verb (SOV)
Unlike English, which is canonically Subject - Verb - Object (SVO), Indian Sign Language is predominantly **Subject - Object - Verb (SOV)** (Zeshan 2000, 2003; Vasishta et al. 1985; Sinha 2008):
- *English:* "I studied speakers" (S - V - O)
- *ISL Gloss:* `I SPEAKER STUDY` (S - O - V)
- *English:* "You will walk away with practical tools"
- *ISL Gloss:* `YOU PRACTICAL TOOL GET`

### 2.2 Time - Topic - Comment
In ISL discourse, temporal reference frames must be established before the event is narrated. Temporal adverbs and time indicators always precede the core proposition:
$$\text{Sentence} \to [\text{TIME}] \quad [\text{TOPIC}] \quad [\text{COMMENT (SOV)}]$$
- *English:* "You can apply tomorrow"
- *ISL Gloss:* `TOMORROW YOU APPLY CAN` (Time first, modal auxiliary last)
- *English:* "Over the next two hours, you'll discover essential tools"
- *ISL Gloss:* `NEXT TWO HOUR YOU IMPORTANT TOOL FIND`

### 2.3 Clause-Final Negation
In ISL, negation is syntactically positioned at the **end of the clause**, directly following the verb or predicate (Zeshan 2003):
$$\text{Clause}_{\text{neg}} \to [\text{SUBJECT}] \quad [\text{OBJECT}] \quad [\text{VERB}] \quad [\text{NOT}]$$
The manual sign `NOT` is co-articulated with a continuous non-manual **headshake**:
- *English:* "If we haven't met before"
- *Raw English Translation:* `WE HAVE NOT MEET` (Incorrect English word order)
- *Natural ISL:* `BEFORE WE MEET NOT` (Temporal adverb fronted, verb followed by final negation)

### 2.4 Interrogative Syntax (WH-Questions)
WH-question words (`WHAT`, `HOW`, `WHERE`, `WHO`, `WHY`, `WHEN`) in ISL canonically occupy the **clause-final position** (Zeshan 2000):
- *English:* "What you are about to watch"
- *Natural ISL:* `YOU WATCH WHAT`
- *English:* "...to pinpoint exactly what makes someone a great speaker"
- *Natural ISL:* `SOMEONE GREAT SPEAKER MAKE WHAT`

Non-manual markers for WH-questions require furrowed brows and head tilt, while polar (yes/no) questions use raised eyebrows.

---

## 3. Handling English Function Words & Conjunctions

### 3.1 Coordinating Conjunctions ("AND", "OR")
Spoken English relies heavily on lexical conjunctions: in our locked 2-minute benchmark, the word **"and" occurs 16 times**!
In natural ISL:
- There is no direct lexical sign equivalent to the English spoken conjunction "and".
- Coordination is achieved through:
  1. **Prosodic Pauses:** A slight hold or transition pause between coordinate clauses.
  2. **Spatial Shifting:** Articulating the first concept in the left signing space and the second concept in the right signing space.
  3. **Sequential Listing:** Listing items using hand fingers (index finger for item 1, middle finger for item 2).
- **Engineering Implementation:** Conjunction "and" must not be emitted as an unknown error. It should be classified as a `SYNTACTIC_PAUSE` or prosodic phrase boundary, allowing smooth transition between coordinated concepts.

### 3.2 Prepositions & Spatial Relations
English prepositions ("with", "into", "from", "on", "over", "around", "about", "for") are not signed as independent manual prepositions in ISL. They are expressed through:
- Directional movement of the verb (e.g., `GIVE`, `BRING`, `MOVE`).
- Relational nouns and spatial positioning.
- Where an English preposition acts adverbially or idiomatically ("walk away with" -> `GET` / `HAVE`), it should be mapped to the semantic verb rather than treated as an isolated missing preposition.

---

## 4. Semantic Disambiguation & Synonym Mapping

A critical insight from auditing the 69 "unknown terms" is that many concepts have direct semantic equivalents already available in our 570-sign library:

| English Spoken Token | Contextual Meaning | Available ISL Sign Asset | Justification |
| :--- | :--- | :--- | :--- |
| `essential` | Crucial / necessary | `important` (`signs/important.json`) | Direct synonym; ISL uses `IMPORTANT` for essential |
| `global` | Worldwide / international | `world` (`signs/world.json`) | Direct semantic concept |
| `endeavour` | Work / project | `work` (`signs/work.json`) | ISL uses `WORK` for project/endeavour |
| `view` / `viewed` | Look at / see | `see` / `look` (`signs/see.json`) | Visual perception verb |
| `captivating` | Attractive / beautiful | `beautiful` (`signs/beautiful.json`) | Expressive positive attribute |
| `giants` | Big organizations | `big` (`signs/big.json`) | Modifying adjective |
| `overcome` | Defeat / succeed | `win` (`signs/win.json`) | Metaphorical victory over fear |
| `discover` | Find out / learn | `find` / `learn` (`signs/find.json`) | Acquisition of knowledge |
| `apply` | Practice / use | `practice` (`signs/practice.json`) | Real-world application |
| `gathered` | Collected / have | `have` (`signs/have.json`) | Possession over career |
| `uncertain` | Doubt / not sure | `not` + `sure` (`signs/not.json` + `sure.json`)| Morphological negation of confidence |
| `anxious` | Nervous / afraid | `fear` (`signs/fear.json`) | Core emotional state |
| `capturing` | Grabbing / holding | `hold` (`signs/hold.json`) | "capturing attention" -> `ATTENTION HOLD` |
| `delivering` | Speaking / presenting | `presentation` (`signs/presentation.json`)| Formal speech delivery |

---

## 5. Proper Noun & Acronym Handling (Fingerspelling)

In ISL, personal names and non-lexicalized English acronyms are produced using the **two-handed ISL fingerspelling manual alphabet**.
In the locked benchmark:
- `David JP Phillips` -> Personal name of the speaker.
- `TEDx` -> International talk organization.
- `Oracle`, `Google`, `Disney` -> Corporate client names.
- `Sweden` -> Country name (note: `signs/sweden.json` is already a playable sign!).

**Architecture Requirement:**
When the translator encounters a verified proper noun, it should:
1. Check if a dedicated cultural sign exists (e.g. `sweden` exists in `signs/sweden.json`).
2. If it is a personal name or brand without a dedicated sign, map it to a structured fingerspelling descriptor `[FS: DAVID]`, `[FS: GOOGLE]`, rather than dropping it as an unhandled failure.

---

## 6. Compound Numbers & Digit Sequences

The locked benchmark contains several numeric expressions:
- `3-day` -> `THREE` `DAY`
- `110-step` -> `1-1-0` `STEP`
- `5,000` -> `FIVE` `THOUSAND` or `5-0-0-0`
- `two hours and 30 minutes` -> `TWO` `HOUR` `30` `MINUTE`
- `25 year career` -> `25` `YEAR` `CAREER`

In ISL, numbers 1 through 10 have distinct single-handed or two-handed handshapes. Numbers 1 (`one`) and 2 (`two`) exist in `signs/`. Signs for `three` (`three.json`) and `day` (`day.json`) are fundamental high-frequency lexical items that must be integrated to support numeric temporal phrases.

---

## 7. Conclusions for Engineering Implementation

To advance from 48.2% to $>85\%$ meaningful concept coverage and authentic ISL grammar, the translation engine must be upgraded with:
1. **Clause-Level ISL Reordering Engine:**
   - Time-fronting (move `TODAY`, `TOMORROW`, `BEFORE`, `NOW` to clause start).
   - SOV transformation for transitive clauses.
   - Clause-final negation (`[VERB] [NOT]`).
   - Clause-final WH-questions (`[TOPIC] [WH-WORD]`).
2. **Syntactic Conjunction & Prosodic Boundary Resolver:**
   - Absorb coordinating `and` into prosodic pauses.
3. **Semantic Synonym Expander:**
   - Map formal English vocabulary to the rich 570-sign library.
4. **Fingerspelling & Proper Noun Pipeline:**
   - Identify names and brand terms and route to fingerspelled representations.
5. **High-Frequency Vocabulary Additions:**
   - Provide Schema 2.0.0 motion definitions for `three`, `day`, `all`, `make`, `before`.

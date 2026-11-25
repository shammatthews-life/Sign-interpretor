# H44 Word, Phrasal Verb, Idiom, Homonym & Disfluency Research (Videos A & B)

This report catalogs every non-compositional phrase, phrasal verb, homonym/polysemous token, quantifier/numeral, proper noun, and speech disfluency identified across all 60 segments (`A01–A29`, `B01–B31`), together with research justification and verified ISL mappings implemented in [EnglishToISLTranslator.js](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.js) and [SemanticUnderstandingEngine.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SemanticUnderstandingEngine.js).

## 1. Idioms & Non-Compositional Expressions
A literal word-for-word sign mapping destroys meaning for spoken English idioms. H44 enforces **multiword phrase matching prior to contextual single-word overrides** (`_compiledPhrases` sorted longest-first):

| Source Expression | Segments | Literal Bug If Split | Research-Grounded ISL Gloss Resolution | Underlying Playable Signs |
| :--- | :--- | :--- | :--- | :--- |
| `best known for` | `A12` | `GOOD KNOW` | `FAMOUS BECAUSE` | `famous`, `because` |
| `pinpoint` + `exactly` | `A15` | `FIND CLEAR CLEAR` | `FIND TRUE` | `find`, `true` |
| `lean in` | `A23` | `LEAN IN` (physical tilt) | `FOCUS` | `focus` |
| `walk away with` | `A23` | `WALK AWAY` (ambulation) | `GET` | `get` |
| `in my opinion` | `B03` | `I THINK` / omitted | `I THINK` | `i`, `think` |
| `in the back of your mind` | `B03` | `YOUR MIND INSIDE` (`inside` unplayable) | `YOUR MIND DEEP` | `your`, `mind`, `deep` |
| `story is king` | `B12` | `STORY KING` | `STORY MOST IMPORTANT` | `story`, `most`, `important` |
| `have to have a story` | `B11`, `B13` | `HAVE HAVE STORY` | `STORY HAVE NEED` | `story`, `have`, `need` |
| `stitched together` | `B18` | `SEW TOGETHER` | `COMBINATION JOIN` | `combination`, `join` |
| `greater and broader` | `B18` | dropped synonyms | `MORE BIG` | `more`, `big` |
| `in an hour or so` | `B21` | split at `so` -> dangling `OR` | `HOUR AROUND` | `hour`, `around` |
| `rest of the evening` | `B23` | `REST` (sleep/relax) | `REMAINING EVENING` | `remaining`, `evening` |
| `trial and error` | `B07` | `TEST FAIL` / UNK | `PRACTICE FAIL LEARN` | `practice`, `fail`, `learn` |
| `show not tell` | `B31` | false clause `NOT` inversion | `SHOW MORE SAY LESS` | `show`, `more`, `say`, `less` |
| `cold start` | Video B intro | temperature `COLD` | `START HARD` | `start`, `hard` |
| `overthinking` / `overcomplicating` | `B05`, `B08` | UNK | `THINK MORE` | `think`, `more` |

## 2. Phrasal Verbs & Domain-Specific Verb Senses
- `begin with` -> `START` (`A07`)
- `move into` -> `MOVE` (`A08`)
- `finish off` -> `FINISH` (`A09`)
- `sat down` -> `SIT` (`B02`, previously corrupted in lexicon duplicate keys)
- `scripted out` -> `PLAN WRITE` (`B02`)
- `up to` (`what I'm up to`) -> `DO` (`B21`)
- `break it down` -> `BREAK` / `EXPLAIN` (`B16`)
- `capturing attention` -> `ATTENTION HOLD` (`A08`/`A18`) vs. `capture some dialogue` (`B30`) -> `COMMUNICATION RECORD` (domain sense disambiguation!)
- `shooting of` / `filming` -> `RECORD` (`B25`, `B19`)
- `make sure` -> `NEED` / obligation modal (`NECESSITY_OBLIGATION`)

## 3. Homonyms & Contextual Disambiguation
1. **`rest` (`B23`):** Nominative `rest of` disambiguated to `REMAINING` (`remaining.json`) rather than `SLEEP`/`REST`.
2. **`just` (`A17`, `B10`, `B28`):** `"just like"` preserves simile `LIKE` (`_compiledPhrases` runs before context override); `"just a"` resolves to `ONLY` (`only.json`).
3. **`right` (`A06`, `B04`):** `"feel right"` -> `GOOD` (`B04`); `"right here"` -> locative focus `HERE` (`A06`).
4. **`left`:** Disambiguated by syntactic frame between `REMAINING` (`hours left`) vs directional `LEFT`.
5. **`too` (`B13`):** Resolved to `ALSO` rather than degree adverb colliding keys.
6. **`gonna` (`B04`):** Corrected from `go` (physical locomotion) to future auxiliary `will` (`FUTURE_INTENT`), preventing spurious `GO` before `SAY`.

## 4. Numbers, Quantifiers & Time Expressions
- `110-step` (`A10`) -> `HUNDRED TEN STEP`
- `5,000` (`A15`) -> `FIVE THOUSAND`
- `two hours and 30 minutes` (`A19`) -> `TWO HOUR THIRTY MINUTE`
- `25 years` (`A20`) -> `TWENTY FIVE YEAR`
- `a lot of` / `most viewed` / `over the years` -> unified under curated quantifier `MANY` (`many.json`).
- Generic noun `time` (`B01` `"best time to go out"`) excluded from deictic time-fronting so `SUMMER HERE` remains clause topic.

## 5. Proper Nouns & ISLRTC Two-Handed Fingerspelling
All verified proper nouns synthesize playable **two-handed ISLRTC manual alphabet** fingerspelling (`fs_<token>`) without English fallback suppression:
- `David` -> `fs_david`, `JP` -> `fs_jp`, `Phillips` -> `fs_phillips` (`A11`)
- `TEDx` -> `fs_tedx` (`A12`)
- `Oracle` -> `fs_oracle`, `Google` -> `fs_google` (`A17`)
- `Disney` -> `fs_disney` (`A18`)

## 6. Speech Disfluencies, Inflections & Spoken Repairs
- **Immediate Stutters:** `_dedupeAdjacent()` collapses 1-token (`I I`) and 2-token (`I've I've`, `A20`) boundary repetitions cleanly.
- **Possessive `'s` (`A18`):** `"audience's"` strips trailing `'s` prior to lexicon lookup so `AUDIENCE` resolves cleanly.
- **Auxiliaries Under Perfective Aspect:** When `FINISH` marks clause completion (`have + V-en`), redundant English auxiliary `HAVE` is dropped so clauses remain grammatical ISL (`I STUDY FINISH`, not `I HAVE STUDY FINISH`).

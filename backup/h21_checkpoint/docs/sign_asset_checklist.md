# ISL Sign Asset Verification Checklist

This checklist must be executed manually for each visual sign asset before it can be committed to the repository and marked `"verified": true` in `isl_accessibility/data/sign_dictionary.json`.

---

## Verification Rules

1. **All 10 checks must pass** before toggling `"verified": false` to `"verified": true`.
2. If any check fails or is uncertain, the asset remains **unverified** (`"verified": false`), or is rejected.
3. Automated bulk harvesting, web scraping, or AI-generated hand renderings are strictly prohibited.
4. Lexical signs must never be substituted with fingerspelled sequences.

---

## Sign Checklists

### 1. `hello` (`hello.jpg`)

- [ ] Source located
- [ ] Source is ISL
- [ ] Correct lexical meaning
- [ ] Not fingerspelling
- [ ] Usage permission understood
- [ ] Attribution recorded
- [ ] Image manually obtained
- [ ] Image visually checked
- [ ] Filename correct (`isl_accessibility/signs/hello.jpg`)
- [ ] verified=true only after ALL checks pass

**Current Status:** UNVERIFIED (`verified`: false). Static image not yet placed. Awaiting manual curation from ISLRTC video source.

---

### 2. `good` (`good.jpg`)

- [ ] Source located
- [ ] Source is ISL
- [ ] Correct lexical meaning
- [ ] Not fingerspelling
- [ ] Usage permission understood
- [ ] Attribution recorded
- [ ] Image manually obtained
- [ ] Image visually checked
- [ ] Filename correct (`isl_accessibility/signs/good.jpg`)
- [ ] verified=true only after ALL checks pass

**Current Status:** UNVERIFIED (`verified`: false). Static image not yet placed. Awaiting manual curation from ISLRTC video source.

---

### 3. `morning` (`morning.jpg`)

- [ ] Source located
- [ ] Source is ISL
- [ ] Correct lexical meaning
- [ ] Not fingerspelling
- [ ] Usage permission understood
- [ ] Attribution recorded
- [ ] Image manually obtained
- [ ] Image visually checked
- [ ] Filename correct (`isl_accessibility/signs/morning.jpg`)
- [ ] verified=true only after ALL checks pass

**Current Status:** UNVERIFIED (`verified`: false). Static image not yet placed. Awaiting manual curation from ISLRTC video source.

---

### 4. `thank you` (`thank_you.jpg`)

- [ ] Source located
- [ ] Source is ISL
- [ ] Correct lexical meaning
- [ ] Not fingerspelling
- [ ] Usage permission understood
- [ ] Attribution recorded
- [ ] Image manually obtained
- [ ] Image visually checked
- [ ] Filename correct (`isl_accessibility/signs/thank_you.jpg`)
- [ ] verified=true only after ALL checks pass

**Current Status:** UNVERIFIED (`verified`: false). Static image not yet placed. Awaiting manual curation from ISLRTC video source.

---

### 5. `water` (`water.jpg`)

- [ ] Source located
- [ ] Source is ISL
- [ ] Correct lexical meaning
- [ ] Not fingerspelling
- [ ] Usage permission understood
- [ ] Attribution recorded
- [ ] Image manually obtained
- [ ] Image visually checked
- [ ] Filename correct (`isl_accessibility/signs/water.jpg`)
- [ ] verified=true only after ALL checks pass

**Current Status:** UNVERIFIED (`verified`: false). Static image not yet placed. Awaiting manual curation from ISLRTC video source.

---

## Post-Verification Action Item

When all 10 checks have been checked and passed for a sign:
1. Place the verified `.jpg` file in `isl_accessibility/signs/`.
2. Update the corresponding entry in `isl_accessibility/data/sign_dictionary.json`:
   - Set `"verified": true`.
   - Update `"accessed_date"` to the verification date.
   - Record the specific source video URL / timestamp in `"notes"`.
3. Run `python tools/validate_sign_library.py` to confirm schema integrity and asset detection.

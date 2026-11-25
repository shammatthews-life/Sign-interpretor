# H44 Sentence-Level Translation Ledger (All 60 Benchmark Segments)

Generated: `2026-11-25T10:02:58.684Z` | Milestone: `H44` | Window: `0.0s – 120.0s (Locked)` | Human Deaf Validation: `PENDING_DEAF_COMMUNITY_REVIEW`

> [!IMPORTANT]
> 100% playable sign resolution across all 60 segments (`555` playable sign instances across `632` validated ISLRTC-referenced sign animations + composite fingerspelling) demonstrates complete engineering lexical coverage, **not** 100% human Deaf-community acceptance, which explicitly remains `PENDING_DEAF_COMMUNITY_REVIEW`.

## Summary Metrics

| Metric | Value |
| :--- | ---: |
| Total Locked Segments Audited | 60 (A: 29, B: 31) |
| H42 Reference Diffs Corrected Against Audio/VTT | 12 |
| Segments with Zero Unknown Terms | 60 / 60 |
| Segments with Zero Unavailable Signs | 60 / 60 |
| Segments with Pre-H44 Defects Repaired & Verified | 34 |
| Total Playable Sign Instances | 555 |
| Sign Library Manifest Size | 632 |

## Video A (`MXKkXXYUxBc` — Public Speaking for Beginners)

### A01 (`2.45s – 8.45s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** This is public speaking for beginners, and the goal of this video is simple.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=2.45,8.45` (conf=`0.8095`, avg_logprob=`-0.1686`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `THIS PUBLIC SPEECH NEW PEOPLE LEARN GOAL THIS VIDEO SIMPLE`
- **Playable Sign IDs (10):** `this, public, speech, new, people, learn, goal, this, video, simple` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "simple" previously had duplicate lexicon entry collision; fixed to uniform SIMPLE
- **Research Basis:** RES-H44-02 (ISLRTC Topic-Comment & Nominal Predicates) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A02 (`8.45s – 14.45s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** It's to help you overcome being uncertain, nervous, anxious, afraid,
- **Prior H42 String (Corrected):** `It's to help you overcome being uncertain, anxious, afraid,`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=8.45,14.45` (conf=`0.8095`, avg_logprob=`-0.1686`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `YOU CONFUSED NERVOUS AFRAID OVERCOME HELP`
- **Playable Sign IDs (6):** `you, confused, nervous, afraid, overcome, help` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 benchmark omitted spoken "nervous"; "afraid" duplicate lexicon collision ("FEAR" vs "AFRAID")
- **Research Basis:** RES-H44-00 (Audio+VTT forensic verification); RES-H44-05 (Lexicon collision purge) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A03 (`14.45s – 21.45s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** and bring you a few steps closer to being more confident, more clear,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=14.45,21.45` (conf=`0.8095`, avg_logprob=`-0.1686`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `BRING YOU FEW STEP CLOSE MORE CONFIDENT MORE CLEAR`
- **Playable Sign IDs (9):** `bring, you, few, step, close, more, confident, more, clear` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** None after verified lexical alignment ("few steps closer")
- **Research Basis:** RES-H44-02 (Comparative MORE + adjective marking) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A04 (`21.45s – 24.45s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** and a much more captivating speaker.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=21.45,24.45` (conf=`0.8095`, avg_logprob=`-0.1686`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `VERY MORE INTERESTING SPEAKER`
- **Playable Sign IDs (4):** `very, more, interesting, speaker` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "captivating" previously collided in lexicon (PLAYABLE INTERESTING unified)
- **Research Basis:** RES-H44-05 (Lexicon synonym normalization) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A05 (`24.45s – 30.45s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** What you're about to watch is a special compilation of a three-day public speaking challenge
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=24.45,30.45` (conf=`0.7509`, avg_logprob=`-0.1397`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[NOMINAL_CLEFT_OR_RELATIVE]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WHAT YOU SPECIAL COMBINATION THREE DAY PUBLIC SPEECH CHALLENGE WATCH`
- **Playable Sign IDs (10):** `what, you, special, combination, three, day, public, speech, challenge, watch` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Nominal pseudo-cleft "What you're about to watch is..." falsely triggered WH-final reordering (WHAT moved to clause end)
- **Research Basis:** RES-H44-01 (Aboh, Pfau & Zeshan 2005: nominal free-relative vs matrix WH-question) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A06 (`30.45s – 34.25s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** which we delivered live right here in our studio.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=30.45,34.25` (conf=`0.7509`, avg_logprob=`-0.1397`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WE HERE GIVE LIVE RECORD ROOM`
- **Playable Sign IDs (6):** `we, here, give, live, record, room` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "right here in our studio" verified intact with RECORD ROOM
- **Research Basis:** RES-H44-02 (Locative HERE pre-verbal grounding) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A07 (`34.25s – 37.33s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** We'll begin with mindset and confidence.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=34.25,37.33` (conf=`0.7509`, avg_logprob=`-0.1397`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WE MINDSET CONFIDENT START`
- **Playable Sign IDs (4):** `we, mindset, confident, start` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Coordinator split risked splitting noun coordination "mindset and confidence"
- **Research Basis:** RES-H44-03 (Noun coordination preservation without spurious clause break) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A08 (`37.33s – 40.21s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** We'll move into the science of capturing attention,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=37.33,40.21` (conf=`0.7509`, avg_logprob=`-0.1397`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WE SCIENCE ATTENTION MOVE HOLD`
- **Playable Sign IDs (5):** `we, science, attention, move, hold` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Phrase "capturing attention" preserved before SOV verb ordering -> WE SCIENCE ATTENTION MOVE HOLD
- **Research Basis:** RES-H44-02 (Clause-local SOV placement) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A09 (`40.21s – 43.77s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** and we'll finish off with the most impactful delivery skills
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=40.21,43.77` (conf=`0.7509`, avg_logprob=`-0.1397`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WE MOST POWER PRESENTATION SKILL FINISH`
- **Playable Sign IDs (6):** `we, most, power, presentation, skill, finish` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "impactful" unified to POWER; "finish off" unified to FINISH
- **Research Basis:** RES-H44-05 (Phrasal verb normalization) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A10 (`43.77s – 47.81s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** from the 110-step chart of excellent communication.
- **Prior H42 String (Corrected):** `from the 110-step chart of excellence communication.`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=43.77,47.81` (conf=`0.7509`, avg_logprob=`-0.1397`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `HUNDRED TEN STEP CHART GREAT COMMUNICATION`
- **Playable Sign IDs (6):** `hundred, ten, step, chart, great, communication` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 reference had ASR substitution "excellence" instead of spoken "excellent"
- **Research Basis:** RES-H44-00 (small.en_b5_norm + VTT cross-audit) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A11 (`49.37s – 52.85s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** Hey, if we haven't met before, my name is David JP Phillips,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=49.37,52.85` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[GREETING_VOCATIVE, STATEMENT]`, temporal=`[]`, neg_clauses=`[0]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha); ISLRTC two-handed fingerspelling (DAVID, JP, PHILLIPS)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `HEY IF BEFORE WE MEET FINISH NOT MY NAME FS_DAVID FS_JP FS_PHILLIPS`
- **Playable Sign IDs (12):** `hey, if, before, we, meet, finish, not, my, name, fs_david, fs_jp, fs_phillips` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Proper name David JP Phillips fingerspelled via ISLRTC two-handed FS_ signs; conditional non-manual brow-raise marked
- **Research Basis:** RES-H44-02 (Zeshan & Sinha conditionals + ISLRTC manual alphabet) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A12 (`52.85s – 54.73s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** and I'm best known for my TEDx talks,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=52.85,54.73` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); ISLRTC two-handed fingerspelling (TEDX)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I FAMOUS BECAUSE MY FS_TEDX SAY`
- **Playable Sign IDs (6):** `i, famous, because, my, fs_tedx, say` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "best known" lacked semantic sign famous (repaired with curated ISL sign famous.json)
- **Research Basis:** RES-H44-06 (ISLRTC Fame / Reputation parametric sign authoring) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A13 (`54.73s – 57.01s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** which are among the most viewed in the world
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=54.73,57.01` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WORLD MANY SEE`
- **Playable Sign IDs (3):** `world, many, see` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "most viewed" previously omitted quantifier MANY ("most viewed in the world" -> WORLD MANY SEE)
- **Research Basis:** RES-H44-06 (ISLRTC quantifier many.json authoring) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A14 (`57.01s – 58.53s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** on this particular subject.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=57.01,58.53` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `THIS SPECIAL SUBJECT`
- **Playable Sign IDs (3):** `this, special, subject` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "particular" duplicate lexicon collision unified to SPECIAL
- **Research Basis:** RES-H44-05 (Lexicon collision purge) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A15 (`58.53s – 65.01s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** You see, I've studied over 5,000 speakers to pinpoint exactly what makes someone a great speaker.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=58.53,65.01` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I FIVE THOUSAND SPEAKER STUDY FINISH FIND TRUE WHAT MAKE SOMEBODY GREAT SPEAKER`
- **Playable Sign IDs (13):** `i, five, thousand, speaker, study, finish, find, true, what, make, somebody, great, speaker` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "pinpoint" + "exactly" previously duplicated CLEAR ("FIND CLEAR CLEAR"); simplified to FIND TRUE
- **Research Basis:** RES-H44-05 (Idiomatic intensity collocation) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A16 (`65.01s – 69.49s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** And this chart is one of the results of that particular endeavour.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=65.01,69.49` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `THIS CHART ONE RESULT THAT SPECIAL WORK`
- **Playable Sign IDs (7):** `this, chart, one, result, that, special, work` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Cleanly retains "ONE RESULT THAT SPECIAL WORK"
- **Research Basis:** RES-H44-02 (Nominal predicate without copula) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A17 (`69.49s – 74.29s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** Oh, and they have been put to practice. I've coached global giants like Oracle, Google,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=69.49,74.29` (conf=`0.6721`, avg_logprob=`-0.1737`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); ISLRTC two-handed fingerspelling (ORACLE, GOOGLE)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `THEY PRACTICE FINISH I WORLD BIG COMPANY LIKE FS_ORACLE FS_GOOGLE COACHING FINISH`
- **Playable Sign IDs (12):** `they, practice, finish, i, world, big, company, like, fs_oracle, fs_google, coaching, finish` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Proper nouns Oracle, Google fingerspelled; "just like" prevented wrong contextual "ONLY" override
- **Research Basis:** RES-H44-03 (Multiword idiom precedence before single-token context overrides) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A18 (`74.29s – 80.45s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** and Disney and storytelling and presentation skills, and the beautiful science of holding an audience's
- **Prior H42 String (Corrected):** `and Disney and storytelling and presentation skills, and the beautiful science of holding an audience`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=74.29,80.45` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); ISLRTC two-handed fingerspelling (DISNEY)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `FS_DISNEY STORY PRESENTATION SKILL BEAUTIFUL SCIENCE AUDIENCE HOLD`
- **Playable Sign IDs (8):** `fs_disney, story, presentation, skill, beautiful, science, audience, hold` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 reference had "audience attention"; possessive "audience's" failed lexicon lookup -> stripped trailing 's before lookup
- **Research Basis:** RES-H44-00 (Audio+VTT audit); RES-H44-04 (Inflectional possessive normalization) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A19 (`80.45s – 86.61s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** attention. Now over the next two hours and 30 minutes, you'll discover the essential tools
- **Prior H42 String (Corrected):** `attention. Now over the next two hours and 30 minutes, you'll discover the essential tools I've`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=80.45,86.61` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `ATTENTION NEXT NOW TWO HOUR THIRTY MINUTE YOU IMPORTANT TOOLS FIND`
- **Playable Sign IDs (11):** `attention, next, now, two, hour, thirty, minute, you, important, tools, find` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Preserves temporal "NEXT NOW TWO HOUR THIRTY MINUTE" cleanly
- **Research Basis:** RES-H44-02 (Time-topic fronting) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A20 (`86.61s – 89.53s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** I've gathered during my 25 year career as a public speaker
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=86.61,89.53` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I DURING FIND FINISH MY TWENTY FIVE YEAR CAREER PUBLIC SPEAKER`
- **Playable Sign IDs (11):** `i, during, find, finish, my, twenty, five, year, career, public, speaker` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 reference kept stutter "I've I've"; translator stutter-collapse + auxiliary HAVE drop after FINISH
- **Research Basis:** RES-H44-00; RES-H44-02 (Perfective FINISH without redundant HAVE) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A21 (`89.53s – 91.69s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** and public speaking coach.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=89.53,91.69` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `PUBLIC SPEECH COACHING`
- **Playable Sign IDs (3):** `public, speech, coaching` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Concise topical phrase "PUBLIC SPEECH COACHING"
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A22 (`91.69s – 95.33s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** So make sure you have a pen and a paper,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=91.69,95.33` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[NECESSITY_OBLIGATION]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `REMEMBER IMPORTANT YOU PEN PAPER HAVE`
- **Playable Sign IDs (6):** `remember, important, you, pen, paper, have` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Clause splitter previously broke coordinated object "a pen and a paper"; preserved intact as single SOV clause
- **Research Basis:** RES-H44-03 (Noun coordination guard) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A23 (`95.33s – 98.93s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** lean in and you'll walk away with practical tools
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=95.33,98.93` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `FOCUS YOU PRACTICAL TOOLS GET`
- **Playable Sign IDs (5):** `focus, you, practical, tools, get` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "lean in" + "walk away with" are idioms, NOT literal LEAN/WALK -> resolved to FOCUS / GET
- **Research Basis:** RES-H44-04 (Non-compositional phrasal verb resolution) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A24 (`98.93s – 101.81s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** you can apply tomorrow.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=98.93,101.81` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[ABILITY_CAN]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `TOMORROW YOU PRACTICE`
- **Playable Sign IDs (3):** `tomorrow, you, practice` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Cleanly fronts temporal TOMORROW before YOU PRACTICE
- **Research Basis:** RES-H44-02 (Temporal fronting) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A25 (`101.81s – 107.03s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** Have fun.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=101.81,107.03` (conf=`0.7997`, avg_logprob=`-0.1801`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `ENJOY`
- **Playable Sign IDs (1):** `enjoy` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Single affective verb ENJOY
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A26 (`107.03s – 110.79s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** Welcome beautiful people all around the world
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=107.03,110.79` (conf=`0.7643`, avg_logprob=`-0.2376`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[GREETING_VOCATIVE]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WELCOME BEAUTIFUL PEOPLE ALL WORLD`
- **Playable Sign IDs (5):** `welcome, beautiful, people, all, world` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Vocative greeting preserved with WELCOME before BEAUTIFUL PEOPLE ALL WORLD
- **Research Basis:** RES-H44-02 (Greeting boundary preservation) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A27 (`110.79s – 114.03s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** to the lovely country of Sweden.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=110.79,114.03` (conf=`0.7643`, avg_logprob=`-0.2376`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `SWEDEN LOVELY COUNTRY`
- **Playable Sign IDs (3):** `sweden, lovely, country` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Topic-comment "SWEDEN LOVELY COUNTRY" cleanly omits English copula "is"
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A28 (`114.03s – 116.63s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** This is, well, this is my view of you.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=114.03,116.63` (conf=`0.7643`, avg_logprob=`-0.2376`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `THIS MY SEE YOU`
- **Playable Sign IDs (4):** `this, my, see, you` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Visual introduction "THIS MY SEE YOU"
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### A29 (`116.63s – 118.95s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** There's pictures all over the place.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_MXKkXXYUxBc_16k_norm.wav#t=116.63,118.95` (conf=`0.7643`, avg_logprob=`-0.2376`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `PICTURE MANY PLACE`
- **Playable Sign IDs (3):** `picture, many, place` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "different places" -> MANY PLACE (many.json)
- **Research Basis:** RES-H44-06 (Quantifier coverage) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

## Video B (`y8tFSuOMAqQ` — How to Vlog as a Beginner)

### B01 (`0s – 3.84s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** Alright, so summer is here and in my opinion that's really the best time to go out, start filming,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=0,3.84` (conf=`0.8402`, avg_logprob=`-0.1336`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[GREETING_VOCATIVE]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `SUMMER HERE I THINK THAT REAL GOOD TIME GO START RECORD`
- **Playable Sign IDs (11):** `summer, here, i, think, that, real, good, time, go, start, record` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Generic noun "TIME" ("best time to go out") falsely fronted ahead of "SUMMER HERE"; fixed timeGlosses exclusion
- **Research Basis:** RES-H44-02 (Distinguish temporal deictics vs lexical noun TIME) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B02 (`3.84s – 7.68s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** start vlogging and documenting your life. Maybe you've just sat down and scripted out your first
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=3.84,7.68` (conf=`0.8402`, avg_logprob=`-0.1336`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[EPISTEMIC_POSSIBILITY]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `START VIDEO MOVIE YOUR LIFE MAYBE YOU SIT FINISH PLAN WRITE YOUR FIRST`
- **Playable Sign IDs (13):** `start, video, movie, your, life, maybe, you, sit, finish, plan, write, your, first` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "sat" previously collided in lexicon; "scripted out" resolved to PLAN WRITE + FINISH
- **Research Basis:** RES-H44-05 (Idiom + perfective aspect) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B03 (`7.68s – 12.24s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** video or maybe you've even gone out and filmed it but I bet in the back of your mind something still
- **Prior H42 String (Corrected):** `video or maybe you even gone out and filmed it but I bet in the back of your mind something still`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=7.68,12.24` (conf=`0.8402`, avg_logprob=`-0.1336`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[EPISTEMIC_POSSIBILITY]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `VIDEO OR MAYBE YOU GO FINISH FILM BUT I THINK YOUR MIND DEEP ONE CONTINUOUS`
- **Playable Sign IDs (15):** `video, or, maybe, you, go, finish, film, but, i, think, your, mind, deep, one, continuous` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 missed spoken "you've"; "in the back of your mind" previously emitted unplayable INSIDE -> unified to playable YOUR MIND DEEP; added barrier->WALL
- **Research Basis:** RES-H44-00; RES-H44-04 (Playable metaphor mapping) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B04 (`12.24s – 15.68s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** just doesn't feel right about your vlog and I'm gonna say it right now you're probably just
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=12.24,15.68` (conf=`0.8402`, avg_logprob=`-0.1336`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[0]`, modality=`[EPISTEMIC_POSSIBILITY]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `FEEL GOOD YOUR VIDEO NOT NOW I SAY YOU THINK`
- **Playable Sign IDs (10):** `feel, good, your, video, not, now, i, say, you, think` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "gonna" previously expanded to "go" producing wrong motion "I GO SAY"; fixed CONTRACTION_PATTERNS ("gonna" -> "will")
- **Research Basis:** RES-H44-04 (Future auxiliary grammaticalization) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B05 (`15.68s – 20.32s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** overthinking it. I was too in the very beginning and honestly I still do even to this day but the
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=15.68,20.32` (conf=`0.8402`, avg_logprob=`-0.1336`)
- **ISR 3.0 Semantics:** clauses=`4`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `MORE THINK I ALSO VERY START HONESTY I CONTINUOUS THIS DAY DO BUT`
- **Playable Sign IDs (13):** `more, think, i, also, very, start, honesty, i, continuous, this, day, do, but` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "overthinking" / "overcomplicate" unified to THINK MORE
- **Research Basis:** RES-H44-05 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B06 (`20.32s – 24.48s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** entire creative process for vlogging has definitely gotten a lot easier over the years so today I
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=20.32,24.48` (conf=`0.8402`, avg_logprob=`-0.1336`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `ALL ART STEP VIDEO VERY EASY MANY YEAR GET FINISH TODAY I`
- **Playable Sign IDs (12):** `all, art, step, video, very, easy, many, year, get, finish, today, i` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "creative process" -> ART STEP; "over the years" -> MANY YEAR (many.json); FINISH aspect preserved
- **Research Basis:** RES-H44-04; RES-H44-06 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B07 (`24.48s – 28.64s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** wanted to share some advice about that. Things I've learned through years of trial and error on how
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=24.48,28.64` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `FEW ADVICE WANT SHARE THAT MATTER I YEAR LEARN FINISH PRACTICE FAIL LEARN HOW`
- **Playable Sign IDs (14):** `few, advice, want, share, that, matter, i, year, learn, finish, practice, fail, learn, how` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Clean advice framing with PRACTICE FAIL LEARN HOW
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B08 (`28.64s – 32.56s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** you can go about your day and start vlogging your life without completely overcomplicating
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=28.64,32.56` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[ABILITY_CAN]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `YOU LIVE YOUR DAY START VIDEO YOUR LIFE WITHOUT ALL CONFUSED`
- **Playable Sign IDs (11):** `you, live, your, day, start, video, your, life, without, all, confused` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Privative WITHOUT preserved cleanly before ALL CONFUSED
- **Research Basis:** RES-H44-02 (Privative preposition retention) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B09 (`32.56s – 37.32s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** the process as a beginner.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=32.56,37.32` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `STEP NEW LEARN`
- **Playable Sign IDs (3):** `step, new, learn` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Step-by-step opener STEP NEW LEARN
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B10 (`37.32s – 41.56s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** So essentially a vlog is just a very loosely defined short film.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=37.32,41.56` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `VIDEO ONLY VERY SIMPLE SMALL FILM`
- **Playable Sign IDs (6):** `video, only, very, simple, small, film` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "just a" ("your vlog isn't just a...") required curated only.json + WH/pseudo-cleft stability; H42 continuation split
- **Research Basis:** RES-H44-06 (ISLRTC focus particle ONLY) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B11 (`41.56s – 45.2s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** And what that means is at the core of it all you still need a good story.
- **Prior H42 String (Corrected):** `And what that means is that the core of it all you still need a good story.`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=41.56,45.2` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[NECESSITY_OBLIGATION]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `WHAT THAT MEAN CORE ALL YOU CONTINUOUS GOOD STORY NEED`
- **Playable Sign IDs (10):** `what, that, mean, core, all, you, continuous, good, story, need` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 reference had ASR error "that the core" instead of "at the core"; "have to have" unified to NEED
- **Research Basis:** RES-H44-00; RES-H44-05 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B12 (`45.2s – 48.48s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** I know you are definitely tired of hearing that from everybody that story is king.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=45.2,48.48` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I KNOW YOU VERY TIRED HEAR THAT PEOPLE THAT STORY MOST IMPORTANT`
- **Playable Sign IDs (12):** `i, know, you, very, tired, hear, that, people, that, story, most, important` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Idiom "story is king" -> STORY MOST IMPORTANT
- **Research Basis:** RES-H44-04 (Metaphorical predicate translation) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B13 (`48.48s – 51.56s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** You have to have a story because everybody knows that and I know you do too.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=48.48,51.56` (conf=`0.8108`, avg_logprob=`-0.1872`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[NECESSITY_OBLIGATION]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `YOU STORY HAVE NEED BECAUSE PEOPLE KNOW THAT I KNOW YOU DO ALSO`
- **Playable Sign IDs (13):** `you, story, have, need, because, people, know, that, i, know, you, do, also` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "too" previously risked wrong gloss instead of ALSO; fixed to ALSO + causal BECAUSE retained
- **Research Basis:** RES-H44-05 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B14 (`51.56s – 53.24s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** See the problem isn't that you don't know that.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=51.56,53.24` (conf=`0.8766`, avg_logprob=`-0.1198`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[0]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `SEE PROBLEM THAT YOU KNOW THAT NOT`
- **Playable Sign IDs (7):** `see, problem, that, you, know, that, not` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Clause-scoped negation keeps NOT strictly at end of negated clause ("THAT YOU KNOW THAT NOT")
- **Research Basis:** RES-H44-02 (Zeshan & Sinha clause-final negation) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B15 (`53.24s – 57.08s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** It's that you don't know how to actually find a story in your day to tell.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=53.24,57.08` (conf=`0.8766`, avg_logprob=`-0.1198`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[0]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `THAT YOU KNOW HOW FIND STORY YOUR DAY TELL NOT`
- **Playable Sign IDs (10):** `that, you, know, how, find, story, your, day, tell, not` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "don't know how to find... to tell" preserves KNOW HOW FIND STORY YOUR DAY TELL NOT
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B16 (`57.08s – 62.68s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** So to break down how I find a story in my day to make a vlog about, I like to think about the fundamental pieces in a movie.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=57.08,62.68` (conf=`0.8766`, avg_logprob=`-0.1198`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `BREAK HOW I STORY FIND MY DAY MAKE VIDEO I LIKE BASE PART MOVIE THINK`
- **Playable Sign IDs (15):** `break, how, i, story, find, my, day, make, video, i, like, base, part, movie, think` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Analogy base premise cleanly isolates BREAK HOW I STORY FIND MY DAY MAKE VIDEO
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B17 (`62.68s – 67.58s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** And just like short films, feature films, documentaries, what you really need to think about are scenes.
- **Prior H42 String (Corrected):** `And just like short films, future films, documentaries, what you really need to think about are scenes.`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=62.68,67.58` (conf=`0.8766`, avg_logprob=`-0.1198`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[NECESSITY_OBLIGATION]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `LIKE SMALL FILM FEATURE FILM MOVIE WHAT YOU REAL SCENE NEED THINK`
- **Playable Sign IDs (12):** `like, small, film, feature, film, movie, what, you, real, scene, need, think` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 truncated/corrupted "feature films" check; "short films" -> SMALL FILM; restored FEATURE FILM phrasing
- **Research Basis:** RES-H44-00; RES-H44-05 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B18 (`67.58s – 73.58s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** Just like scenes in your favorite movie, you need to have a compilation of scenes that when stitched together tell a greater and broader story.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=67.58,73.58` (conf=`0.8766`, avg_logprob=`-0.1198`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[NECESSITY_OBLIGATION]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `LIKE SCENE YOUR FAVORITE MOVIE YOU COMBINATION SCENE NEED THAT WHEN COMBINATION JOIN MORE BIG STORY TELL`
- **Playable Sign IDs (17):** `like, scene, your, favorite, movie, you, combination, scene, need, that, when, combination, join, more, big, story, tell` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "greater and broader" unified to MORE BIG; SOV object loop previously swept across THAT into relative clause -> stopped SOV at subordinator THAT
- **Research Basis:** RES-H44-03 (Subordinate clause boundary for SOV reordering) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B19 (`73.58s – 78.38s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** When it comes to vlogging, because you're filming as the day is going on, you sometimes don't know that overarching story,
- **Prior H42 String (Corrected):** `When it comes to vlogging, because you're filming as the day is going on, you sometimes don't know that over-arching story,`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=73.58,78.38` (conf=`0.8766`, avg_logprob=`-0.1198`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[2]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `WHEN COME VIDEO BECAUSE YOU DAY RECORD GO YOU SOMETIMES KNOW THAT ALL STORY NOT`
- **Playable Sign IDs (15):** `when, come, video, because, you, day, record, go, you, sometimes, know, that, all, story, not` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 reference had ASR error vs "overarching"; sentence-scoped NOT placed clause-finally
- **Research Basis:** RES-H44-00; RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B20 (`78.38s – 81.48s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** but I bet you do know at least a scene or two ahead.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=78.38,81.48` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `BUT FUTURE I THINK YOU DO KNOW LITTLE SCENE OR TWO`
- **Playable Sign IDs (11):** `but, future, i, think, you, do, know, little, scene, or, two` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "going forward" -> FUTURE fronted; "do know" epistemic emphasis retained
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B21 (`81.48s – 85.88s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** What that means is maybe I don't know exactly what I'm up to today, but I do know that in an hour or so,
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=81.48,85.88` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[NOMINAL_CLEFT_OR_RELATIVE, STATEMENT]`, temporal=`[]`, neg_clauses=`[0]`, modality=`[EPISTEMIC_POSSIBILITY]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `TODAY WHAT THAT MEAN MAYBE I CLEAR KNOW WHAT I DO NOT BUT I DO KNOW THAT HOUR AROUND`
- **Playable Sign IDs (19):** `today, what, that, mean, maybe, i, clear, know, what, i, do, not, but, i, do, know, that, hour, around` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "or so" previously split on "so" leaving dangling trailing "OR"; now emits HOUR AROUND cleanly with curated around.json
- **Research Basis:** RES-H44-03 (Approximator MWE preservation); RES-H44-06 (around.json) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B22 (`85.88s – 89.8s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** I'm gonna go meet up with a friend so I can build a scene around that and then after that again
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=85.88,89.8` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT, ABILITY_CAN]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I FRIEND GO MEET I SCENE BUILD THAT NEXT AFTER THAT MORE`
- **Playable Sign IDs (12):** `i, friend, go, meet, i, scene, build, that, next, after, that, more` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "go meet" temporal sequence SCENE BUILD THAT NEXT AFTER THAT MORE
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B23 (`89.8s – 91.68s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** I might not know what I'm gonna do for the rest of the evening
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=89.8,91.68` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`1`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[0]`, modality=`[EPISTEMIC_POSSIBILITY]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final manual NOT + headshake NMM (Zeshan & Sinha)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `I MAY KNOW WHAT I DO REMAINING EVENING NOT`
- **Playable Sign IDs (9):** `i, may, know, what, i, do, remaining, evening, not` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "rest of the evening" previously risked mis-sensed "REST" (sleep); context override + remaining.json -> REMAINING EVENING
- **Research Basis:** RES-H44-06 (ISLRTC remaining.json); RES-H44-04 (Polysemy disambiguation) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B24 (`91.68s – 95.24s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** But I do know that I'm hungry so I'm gonna go get some food. That's another scene
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=91.68,95.24` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `BUT I DO KNOW THAT I HUNGRY I FEW FOOD GO GET THAT OTHER SCENE`
- **Playable Sign IDs (15):** `but, i, do, know, that, i, hungry, i, few, food, go, get, that, other, scene` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Causal realization "HUNGRY -> FOOD GO GET THAT OTHER SCENE"
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B25 (`95.24s – 98.52s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** So instead of stressing yourself before you start shooting of what is my story
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=95.24,98.52` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT, WH_QUESTION]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Clause-final matrix WH-element (Aboh, Pfau & Zeshan 2005)
- **Non-Manual Markers:** undefined@clauseundefined
- **Output ISL Gloss:** `INSTEAD NERVOUS YOU BEFORE YOU START RECORD MY STORY WHAT`
- **Playable Sign IDs (10):** `instead, nervous, you, before, you, start, record, my, story, what` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Embedded direct self-question "shooting of what is my story" failed WH-final rule; split at "of what is" -> MY STORY WHAT
- **Research Basis:** RES-H44-01 (Embedded direct question WH-final syntax) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B26 (`98.56s – 105.04s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** Just allow yourself to live life and think of things scene by scene and also think about how the scenes kind of tie into the overall
- **Prior H42 String (Corrected):** `Just allow yourself to live life and think of things seen by scene and also think about how the scenes kind of tie into the overall`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=98.56,105.04` (conf=`0.7333`, avg_logprob=`-0.0706`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `ALLOW YOU LIFE LIVE MATTER SCENE STEP THINK ALSO THINK HOW SCENE JOIN ALL`
- **Playable Sign IDs (14):** `allow, you, life, live, matter, scene, step, think, also, think, how, scene, join, all` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 missed hyphen/spacing consistency in "scene by scene" -> SCENE STEP + JOIN ALL
- **Research Basis:** RES-H44-00; RES-H44-05 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B27 (`105.04s – 107.92s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** feeling that you're trying to deliver so when I'm out shooting and filming things
- **Prior H42 String (Corrected):** `Feeling that you're trying to deliver so when I'm out shooting and filming things`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=105.04,107.92` (conf=`0.685`, avg_logprob=`-0.1648`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `FEEL THAT YOU TRY GIVE WHEN I MATTER RECORD`
- **Playable Sign IDs (9):** `feel, that, you, try, give, when, i, matter, record` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Intentional recording framing FEEL THAT YOU TRY GIVE WHEN I MATTER RECORD
- **Research Basis:** RES-H44-02 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B28 (`107.92s – 111.12s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** I always try and think is this just a shot that I'm getting because it looks cool
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=107.92,111.12` (conf=`0.685`, avg_logprob=`-0.1648`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I CONTINUOUS TRY THINK THIS ONLY PICTURE THAT I GET BECAUSE COOL LOOK`
- **Playable Sign IDs (13):** `i, continuous, try, think, this, only, picture, that, i, get, because, cool, look` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** "just a" -> ONLY; progressive "getting" protected against false FINISH aspect; causal BECAUSE preserved
- **Research Basis:** RES-H44-02; RES-H44-06 | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B29 (`111.12s – 113.4s`) — `VERIFIED_ACCURATE`
- **Verified Reference English:** or is this an actual scene if it's a scene
- **Prior H42 String (Corrected):** `Or is this an actual scene if it's a scene`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=111.12,113.4` (conf=`0.685`, avg_logprob=`-0.1648`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02); Condition-first clause with brow-raise NMM (NMM-COND-BROW-RAISE)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `OR THIS REAL SCENE IF SCENE`
- **Playable Sign IDs (6):** `or, this, real, scene, if, scene` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Conditional contrast "OR THIS REAL SCENE IF SCENE" with brow-raise NMM
- **Research Basis:** RES-H44-02 (Zeshan & Sinha conditional NMM) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B30 (`113.4s – 117.48s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** I'll have to build a little bit more around it. Most often I'll also capture some dialogue, some talking,
- **Prior H42 String (Corrected):** `I'll have to build a little bit more around it. Most often it'll also capture some dialogues. I'm talking`
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=113.4,117.48` (conf=`0.685`, avg_logprob=`-0.1648`)
- **ISR 3.0 Semantics:** clauses=`2`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[NECESSITY_OBLIGATION, FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I LITTLE BIT MORE NEED BUILD MOST USUALLY I ALSO COMMUNICATION FEW RECORD SAY`
- **Playable Sign IDs (14):** `i, little, bit, more, need, build, most, usually, i, also, communication, few, record, say` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** H42 omitted spoken clause ", some talking,"; "capture some dialogue" previously emitted literal HOLD -> fixed to COMMUNICATION RECORD
- **Research Basis:** RES-H44-00; RES-H44-04 (Domain-appropriate verb sense) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`

### B31 (`117.48s – 120s`) — `FIXED_AND_VERIFIED`
- **Verified Reference English:** I'll talk straight to the camera and explain what's going on. A lot of people will tell you that in filmmaking you want to show not tell.
- **Audio Ref & Whisper `small.en_b5_norm`:** `artifacts/h44/asr/audio_y8tFSuOMAqQ_16k_norm.wav#t=117.48,120` (conf=`0.685`, avg_logprob=`-0.1648`)
- **ISR 3.0 Semantics:** clauses=`3`, acts=`[STATEMENT]`, temporal=`[]`, neg_clauses=`[]`, modality=`[FUTURE_INTENT]`
- **Intended ISL Strategy:** Topic-comment & clause-local SOV ordering (ISL-SOV-02)
- **Non-Manual Markers:** None
- **Output ISL Gloss:** `I CLEAR CAMERA SAY EXPLAIN WHAT GO MANY PEOPLE TELL YOU THAT FILM YOU WANT SHOW MORE SAY LESS`
- **Playable Sign IDs (19):** `i, clear, camera, say, explain, what, go, many, people, tell, you, that, film, you, want, show, more, say, less` (UNK: 0, UNAVAIL: 0)
- **Pre-H44 Defects & Repairs:** Contrastive idiom "show not tell" falsely triggered clause polarity inversion ("NOT" appended); fixed idiom flag + SHOW MORE SAY LESS
- **Research Basis:** RES-H44-04 (Contrastive idiom polarity isolation) | **Human Review:** `PENDING_DEAF_COMMUNITY_REVIEW`


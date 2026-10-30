"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 15 (520 Signs & 90%+ Coverage Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**500 Schema 2.0.0 Assets (+293 Signs) — LANDMARK 500 MILESTONE**', '**520 Schema 2.0.0 Assets (+313 Signs) — 90%+ COVERAGE MILESTONE**')
text = text.replace('**20,896 / 23,258 tokens (89.84%)**', '**20,998 / 23,258 tokens (90.28%)**')
text = text.replace('Reduced by 1,199 tokens from 3,560 down to **2,361 tokens (10.15%)**', 'Reduced by 1,301 tokens from 3,560 down to **2,259 tokens (9.71%)**')

# Update Executive summary
text = text.replace('**Fourteen-Batch Lexical Expansion (293 New Schema 2.0.0 Signs - 500 Landmark Milestone):**', '**Fifteen-Batch Lexical Expansion (313 New Schema 2.0.0 Signs - 520 Milestone, 90%+ Coverage):**')
text = text.replace('expanding the playable library to 500 signs:', 'expanding the playable library to 520 signs:')

batch14_sub = '`result`.'
batch15_sub = '`result`.\n   - **Batch 15 (20 signs):** `may`, `hey`, `boom`, `sweden`, `everything`, `somebody`, `anyone`, `anything`, `nothing`, `until`, `weird`, `along`, `quarter`, `tumble`, `fill`, `danger`, `conductor`, `lie`, `luxury`, `turbo`.'
text = text.replace(batch14_sub, batch15_sub)

text = text.replace('articulates all 293 new motions', 'articulates all 313 new motions')
text = text.replace('1324+ new vocabulary dispatches', '1429+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 1324 occurrences', '**New Vocabulary Dispatches:** 1429 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 961', '**Active Sign Real-Time Updates:** 1014')
text = text.replace('68.98 ms', '55.00 ms')

# Update Accounting Invariant
text = text.replace('10,185 + 9,064 + 2,361 + 1,444 + 203 + 1', '10,287 + 9,064 + 2,259 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 10,185 | 43.79% | Authored, playable Schema 2.0.0 signs (+1,240 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 10,287 | 44.23% | Authored, playable Schema 2.0.0 signs (+1,342 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,361 | 10.15% | Transparent text subtitles for specialized terminology (-1,199 tokens from H23) |', '| **Subtitle Fallback** | 2,259 | 9.71% | Transparent text subtitles for specialized terminology (-1,301 tokens from H23) |')

# Update test table
b14_test_line = '| `tools/author_h24_batch14_signs.py` | **PASS** | Batch 14 (20 signs) generated in Schema 2.0.0 |'
b15_test_line = b14_test_line + '\n| `tools/author_h24_batch15_signs.py` | **PASS** | Batch 15 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b14_test_line, b15_test_line)

text = text.replace('All 293 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 313 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 500 signs conform to Schema 2.0.0; 2,488 keyframes checked', 'All 520 signs conform to Schema 2.0.0; 2,588 keyframes checked')
text = text.replace('2,366 segments processed in 69.0 ms; 1324+ vocab dispatches; right sidebar verified', '2,366 segments processed in 55.0 ms; 1429+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')

print("Successfully updated docs/h24_ui_modernization_and_vocabulary_report.md for Batch 15.")

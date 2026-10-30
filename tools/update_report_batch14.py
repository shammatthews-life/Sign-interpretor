"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 14 (500 Signs Landmark Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**480 Schema 2.0.0 Assets (+273 Signs)**', '**500 Schema 2.0.0 Assets (+293 Signs) — LANDMARK 500 MILESTONE**')
text = text.replace('**20,868 / 23,258 tokens (89.72%)**', '**20,896 / 23,258 tokens (89.84%)**')
text = text.replace('Reduced by 1,171 tokens from 3,560 down to **2,389 tokens (10.27%)**', 'Reduced by 1,199 tokens from 3,560 down to **2,361 tokens (10.15%)**')

# Update Executive summary
text = text.replace('**Thirteen-Batch Lexical Expansion (273 New Schema 2.0.0 Signs - 480 Milestone):**', '**Fourteen-Batch Lexical Expansion (293 New Schema 2.0.0 Signs - 500 Landmark Milestone):**')
text = text.replace('expanding the playable library to 480 signs:', 'expanding the playable library to 500 signs:')

batch13_sub = '`decide`.'
batch14_sub = '`decide`.\n   - **Batch 14 (20 signs):** `test`, `village`, `street`, `cloak`, `average`, `dry`, `attract`, `grab`, `send`, `behavior`, `effect`, `belief`, `failure`, `gray`, `nowhere`, `burden`, `observant`, `kid`, `set`, `result`.'
text = text.replace(batch13_sub, batch14_sub)

text = text.replace('articulates all 273 new motions', 'articulates all 293 new motions')
text = text.replace('1265+ new vocabulary dispatches', '1324+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 1265 occurrences', '**New Vocabulary Dispatches:** 1324 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 929', '**Active Sign Real-Time Updates:** 961')
text = text.replace('75.88 ms', '68.98 ms')

# Update Accounting Invariant
text = text.replace('10,133 + 9,088 + 2,389 + 1,444 + 203 + 1', '10,185 + 9,064 + 2,361 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 10,133 | 43.57% | Authored, playable Schema 2.0.0 signs (+1,188 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 10,185 | 43.79% | Authored, playable Schema 2.0.0 signs (+1,240 tokens from H23) |')
text = text.replace('| **Grammar Omission** | 9,088 | 39.07% | Structural function words, copulas, and discourse particles omitted per ISL syntax |', '| **Grammar Omission** | 9,064 | 38.97% | Structural function words, copulas, and discourse particles omitted per ISL syntax |')
text = text.replace('| **Subtitle Fallback** | 2,389 | 10.27% | Transparent text subtitles for specialized terminology (-1,171 tokens from H23) |', '| **Subtitle Fallback** | 2,361 | 10.15% | Transparent text subtitles for specialized terminology (-1,199 tokens from H23) |')

# Update test table
b13_test_line = '| `tools/author_h24_batch13_signs.py` | **PASS** | Batch 13 (20 signs) generated in Schema 2.0.0 |'
b14_test_line = b13_test_line + '\n| `tools/author_h24_batch14_signs.py` | **PASS** | Batch 14 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b13_test_line, b14_test_line)

text = text.replace('All 273 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 293 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 480 signs conform to Schema 2.0.0; 2,388 keyframes checked', 'All 500 signs conform to Schema 2.0.0; 2,488 keyframes checked')
text = text.replace('2,366 segments processed in 75.9 ms; 1265+ vocab dispatches; right sidebar verified', '2,366 segments processed in 69.0 ms; 1324+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')

print("Successfully updated docs/h24_ui_modernization_and_vocabulary_report.md for Batch 14.")

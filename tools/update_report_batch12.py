"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 12 (460 Signs Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**440 Schema 2.0.0 Assets (+233 Signs)**', '**460 Schema 2.0.0 Assets (+253 Signs)**')
text = text.replace('**20,770 / 23,258 tokens (89.30%)**', '**20,822 / 23,258 tokens (89.53%)**')
text = text.replace('Reduced by 1,073 tokens from 3,560 down to **2,487 tokens (10.69%)**', 'Reduced by 1,125 tokens from 3,560 down to **2,435 tokens (10.47%)**')

# Update Executive summary
text = text.replace('**Eleven-Batch Lexical Expansion (233 New Schema 2.0.0 Signs - 440 Milestone):**', '**Twelve-Batch Lexical Expansion (253 New Schema 2.0.0 Signs - 460 Milestone):**')
text = text.replace('expanding the playable library to 440 signs:', 'expanding the playable library to 460 signs:')

batch11_sub = '`united`.'
batch12_sub = '`united`.\n   - **Batch 12 (20 signs):** `conference`, `door`, `break`, `road`, `full`, `past`, `worth`, `ten`, `setting`, `expectation`, `server`, `simply`, `cannot`, `dollar`, `deep`, `phenomenal`, `record`, `buy`, `breathe`, `billion`.'
text = text.replace(batch11_sub, batch12_sub)

text = text.replace('articulates all 233 new motions', 'articulates all 253 new motions')
text = text.replace('1167+ new vocabulary dispatches', '1219+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 1167 occurrences', '**New Vocabulary Dispatches:** 1219 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 880', '**Active Sign Real-Time Updates:** 905')
text = text.replace('39.57 ms', '68.64 ms')

# Update Accounting Invariant
text = text.replace('10,035 + 9,088 + 2,487 + 1,444 + 203 + 1', '10,087 + 9,088 + 2,435 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 10,035 | 43.15% | Authored, playable Schema 2.0.0 signs (+1,090 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 10,087 | 43.37% | Authored, playable Schema 2.0.0 signs (+1,142 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,487 | 10.69% | Transparent text subtitles for specialized terminology (-1,073 tokens from H23) |', '| **Subtitle Fallback** | 2,435 | 10.47% | Transparent text subtitles for specialized terminology (-1,125 tokens from H23) |')

# Update test table
b11_test_line = '| `tools/author_h24_batch11_signs.py` | **PASS** | Batch 11 (20 signs) generated in Schema 2.0.0 |'
b12_test_line = b11_test_line + '\n| `tools/author_h24_batch12_signs.py` | **PASS** | Batch 12 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b11_test_line, b12_test_line)

text = text.replace('All 233 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 253 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 440 signs conform to Schema 2.0.0; 2,188 keyframes checked', 'All 460 signs conform to Schema 2.0.0; 2,288 keyframes checked')
text = text.replace('2,366 segments processed in 39.6 ms; 1167+ vocab dispatches; right sidebar verified', '2,366 segments processed in 68.6 ms; 1219+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')

print("Successfully updated docs/h24_ui_modernization_and_vocabulary_report.md for Batch 12.")

"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 9 (400 Signs Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**380 Schema 2.0.0 Assets (+173 Signs)**', '**400 Schema 2.0.0 Assets (+193 Signs)**')
text = text.replace('**20,583 / 23,258 tokens (88.50%)**', '**20,640 / 23,258 tokens (88.74%)**')
text = text.replace('Reduced by 886 tokens from 3,560 down to **2,674 tokens (11.50%)**', 'Reduced by 943 tokens from 3,560 down to **2,617 tokens (11.25%)**')

# Update Executive summary
text = text.replace('**Eight-Batch Lexical Expansion (173 New Schema 2.0.0 Signs):**', '**Nine-Batch Lexical Expansion (193 New Schema 2.0.0 Signs - 400 Milestone):**')
text = text.replace('expanding the playable library to 380 signs:', 'expanding the playable library to 400 signs:')

batch8_sub = '`guy`.'
batch9_sub = '`guy`.\n   - **Batch 9 (20 signs):** `smile`, `dream`, `exercise`, `accomplish`, `close`, `old`, `hungry`, `intention`, `motivated`, `few`, `lovely`, `focus`, `sometimes`, `list`, `connected`, `course`, `analyze`, `fourth`, `fifth`, `meeting`.'
text = text.replace(batch8_sub, batch9_sub)

text = text.replace('articulates all 173 new motions', 'articulates all 193 new motions')
text = text.replace('967+ new vocabulary dispatches', '1037+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 967 occurrences', '**New Vocabulary Dispatches:** 1037 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 761', '**Active Sign Real-Time Updates:** 809')
text = text.replace('53.86 ms', '57.72 ms')

# Update Accounting Invariant
text = text.replace('9,848 + 9,088 + 2,674 + 1,444 + 203 + 1', '9,905 + 9,088 + 2,617 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 9,848 | 42.34% | Authored, playable Schema 2.0.0 signs (+903 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 9,905 | 42.59% | Authored, playable Schema 2.0.0 signs (+960 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,674 | 11.50% | Transparent text subtitles for specialized terminology (-886 tokens from H23) |', '| **Subtitle Fallback** | 2,617 | 11.25% | Transparent text subtitles for specialized terminology (-943 tokens from H23) |')

# Update test table
b8_test_line = '| `tools/author_h24_batch8_signs.py` | **PASS** | Batch 8 (24 signs) generated in Schema 2.0.0 |'
b9_test_line = b8_test_line + '\n| `tools/author_h24_batch9_signs.py` | **PASS** | Batch 9 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b8_test_line, b9_test_line)

text = text.replace('All 173 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 193 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 380 signs conform to Schema 2.0.0; 1,888 keyframes checked', 'All 400 signs conform to Schema 2.0.0; 1,988 keyframes checked')
text = text.replace('2,366 segments processed in 53.9 ms; 967+ vocab dispatches; right sidebar verified', '2,366 segments processed in 57.7 ms; 1037+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')
print('Updated docs/h24_ui_modernization_and_vocabulary_report.md successfully for Batch 9 (400 signs).')

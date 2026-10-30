"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 10 (420 Signs Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**400 Schema 2.0.0 Assets (+193 Signs)**', '**420 Schema 2.0.0 Assets (+213 Signs)**')
text = text.replace('**20,640 / 23,258 tokens (88.74%)**', '**20,707 / 23,258 tokens (89.03%)**')
text = text.replace('Reduced by 943 tokens from 3,560 down to **2,617 tokens (11.25%)**', 'Reduced by 1,010 tokens from 3,560 down to **2,550 tokens (10.96%)**')

# Update Executive summary
text = text.replace('**Nine-Batch Lexical Expansion (193 New Schema 2.0.0 Signs - 400 Milestone):**', '**Ten-Batch Lexical Expansion (213 New Schema 2.0.0 Signs - 420 Milestone):**')
text = text.replace('expanding the playable library to 400 signs:', 'expanding the playable library to 420 signs:')

batch9_sub = '`meeting`.'
batch10_sub = '`meeting`.\n   - **Batch 10 (20 signs):** `human`, `relate`, `cool`, `wow`, `corner`, `chest`, `extension`, `loop`, `similar`, `metaphor`, `scientific`, `skilled`, `proven`, `absolute`, `dominant`, `arena`, `myself`, `uncomfortable`, `filled`, `empowering`.'
text = text.replace(batch9_sub, batch10_sub)

text = text.replace('articulates all 193 new motions', 'articulates all 213 new motions')
text = text.replace('1037+ new vocabulary dispatches', '1104+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 1037 occurrences', '**New Vocabulary Dispatches:** 1104 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 809', '**Active Sign Real-Time Updates:** 848')
text = text.replace('57.72 ms', '44.82 ms')

# Update Accounting Invariant
text = text.replace('9,905 + 9,088 + 2,617 + 1,444 + 203 + 1', '9,972 + 9,088 + 2,550 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 9,905 | 42.59% | Authored, playable Schema 2.0.0 signs (+960 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 9,972 | 42.88% | Authored, playable Schema 2.0.0 signs (+1,027 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,617 | 11.25% | Transparent text subtitles for specialized terminology (-943 tokens from H23) |', '| **Subtitle Fallback** | 2,550 | 10.96% | Transparent text subtitles for specialized terminology (-1,010 tokens from H23) |')

# Update test table
b9_test_line = '| `tools/author_h24_batch9_signs.py` | **PASS** | Batch 9 (20 signs) generated in Schema 2.0.0 |'
b10_test_line = b9_test_line + '\n| `tools/author_h24_batch10_signs.py` | **PASS** | Batch 10 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b9_test_line, b10_test_line)

text = text.replace('All 193 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 213 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 400 signs conform to Schema 2.0.0; 1,988 keyframes checked', 'All 420 signs conform to Schema 2.0.0; 2,088 keyframes checked')
text = text.replace('2,366 segments processed in 57.7 ms; 1037+ vocab dispatches; right sidebar verified', '2,366 segments processed in 44.8 ms; 1104+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')

print("Successfully updated docs/h24_ui_modernization_and_vocabulary_report.md for Batch 10.")

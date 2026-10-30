"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 13 (480 Signs Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**460 Schema 2.0.0 Assets (+253 Signs)**', '**480 Schema 2.0.0 Assets (+273 Signs)**')
text = text.replace('**20,822 / 23,258 tokens (89.53%)**', '**20,868 / 23,258 tokens (89.72%)**')
text = text.replace('Reduced by 1,125 tokens from 3,560 down to **2,435 tokens (10.47%)**', 'Reduced by 1,171 tokens from 3,560 down to **2,389 tokens (10.27%)**')

# Update Executive summary
text = text.replace('**Twelve-Batch Lexical Expansion (253 New Schema 2.0.0 Signs - 460 Milestone):**', '**Thirteen-Batch Lexical Expansion (273 New Schema 2.0.0 Signs - 480 Milestone):**')
text = text.replace('expanding the playable library to 460 signs:', 'expanding the playable library to 480 signs:')

batch12_sub = '`billion`.'
batch13_sub = '`billion`.\n   - **Batch 13 (20 signs):** `laugh`, `soul`, `meal`, `follow`, `fair`, `statistics`, `nose`, `self`, `angel`, `math`, `insane`, `goosebumps`, `pointless`, `misunderstand`, `tilt`, `spend`, `perceive`, `upon`, `fan`, `decide`.'
text = text.replace(batch12_sub, batch13_sub)

text = text.replace('articulates all 253 new motions', 'articulates all 273 new motions')
text = text.replace('1219+ new vocabulary dispatches', '1265+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 1219 occurrences', '**New Vocabulary Dispatches:** 1265 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 905', '**Active Sign Real-Time Updates:** 929')
text = text.replace('68.64 ms', '75.88 ms')

# Update Accounting Invariant
text = text.replace('10,087 + 9,088 + 2,435 + 1,444 + 203 + 1', '10,133 + 9,088 + 2,389 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 10,087 | 43.37% | Authored, playable Schema 2.0.0 signs (+1,142 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 10,133 | 43.57% | Authored, playable Schema 2.0.0 signs (+1,188 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,435 | 10.47% | Transparent text subtitles for specialized terminology (-1,125 tokens from H23) |', '| **Subtitle Fallback** | 2,389 | 10.27% | Transparent text subtitles for specialized terminology (-1,171 tokens from H23) |')

# Update test table
b12_test_line = '| `tools/author_h24_batch12_signs.py` | **PASS** | Batch 12 (20 signs) generated in Schema 2.0.0 |'
b13_test_line = b12_test_line + '\n| `tools/author_h24_batch13_signs.py` | **PASS** | Batch 13 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b12_test_line, b13_test_line)

text = text.replace('All 253 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 273 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 460 signs conform to Schema 2.0.0; 2,288 keyframes checked', 'All 480 signs conform to Schema 2.0.0; 2,388 keyframes checked')
text = text.replace('2,366 segments processed in 68.6 ms; 1219+ vocab dispatches; right sidebar verified', '2,366 segments processed in 75.9 ms; 1265+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')

print("Successfully updated docs/h24_ui_modernization_and_vocabulary_report.md for Batch 13.")

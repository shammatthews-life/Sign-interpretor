"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 7.
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**332 Schema 2.0.0 Assets (+125 Signs)**', '**356 Schema 2.0.0 Assets (+149 Signs)**')
text = text.replace('**20,394 / 23,258 tokens (87.69%)**', '**20,493 / 23,258 tokens (88.11%)**')
text = text.replace('Reduced by 697 tokens from 3,560 down to **2,863 tokens (12.31%)**', 'Reduced by 796 tokens from 3,560 down to **2,764 tokens (11.88%)**')

# Update Executive summary
text = text.replace('**Six-Batch Lexical Expansion (125 New Schema 2.0.0 Signs):**', '**Seven-Batch Lexical Expansion (149 New Schema 2.0.0 Signs):**')
text = text.replace('expanding the playable library to 332 signs:', 'expanding the playable library to 356 signs:')

batch6_sub = '`allow`.'
batch7_sub = '`allow`.\n   - **Batch 7 (24 signs):** `job`, `business`, `message`, `care`, `promise`, `flow`, `store`, `center`, `middle`, `sister`, `post`, `package`, `favorite`, `silent`, `comfortable`, `football`, `low`, `amount`, `crazy`, `between`, `each`, `chat`, `bit`, `super`.'
text = text.replace(batch6_sub, batch7_sub)

text = text.replace('articulates all 125 new motions', 'articulates all 149 new motions')
text = text.replace('401+ new vocabulary dispatches', '868+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 401 occurrences', '**New Vocabulary Dispatches:** 868 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 357', '**Active Sign Real-Time Updates:** 707')
text = text.replace('56.17 ms', '56.49 ms')

# Update Accounting Invariant
text = text.replace('9,642 + 9,088 + 2,863 + 1,444 + 220 + 1', '9,749 + 9,088 + 2,764 + 1,444 + 212 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 9,642 | 41.46% | Authored, playable Schema 2.0.0 signs (+697 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 9,749 | 41.92% | Authored, playable Schema 2.0.0 signs (+804 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,863 | 12.31% | Transparent text subtitles for specialized terminology (-697 tokens from H23) |', '| **Subtitle Fallback** | 2,764 | 11.88% | Transparent text subtitles for specialized terminology (-796 tokens from H23) |')
text = text.replace('| **Fingerspelled** | 220 | 0.95% |', '| **Fingerspelled** | 212 | 0.91% |')

# Update test table
b6_test_line = '| `tools/author_h24_batch6_signs.py` | **PASS** | Batch 6 (24 signs) generated in Schema 2.0.0 |'
b7_test_line = b6_test_line + '\n| `tools/author_h24_batch7_signs.py` | **PASS** | Batch 7 (24 signs) generated in Schema 2.0.0 |'
text = text.replace(b6_test_line, b7_test_line)

text = text.replace('All 125 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 149 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 332 signs conform to Schema 2.0.0; 1,648 keyframes checked', 'All 356 signs conform to Schema 2.0.0; 1,768 keyframes checked')
text = text.replace('2,366 segments processed in 56.2 ms; 401+ vocab dispatches; right sidebar verified', '2,366 segments processed in 56.5 ms; 868+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')
print('Updated docs/h24_ui_modernization_and_vocabulary_report.md successfully.')

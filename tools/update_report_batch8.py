"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 8.
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**356 Schema 2.0.0 Assets (+149 Signs)**', '**380 Schema 2.0.0 Assets (+173 Signs)**')
text = text.replace('**20,493 / 23,258 tokens (88.11%)**', '**20,583 / 23,258 tokens (88.50%)**')
text = text.replace('Reduced by 796 tokens from 3,560 down to **2,764 tokens (11.88%)**', 'Reduced by 886 tokens from 3,560 down to **2,674 tokens (11.50%)**')

# Update Executive summary
text = text.replace('**Seven-Batch Lexical Expansion (149 New Schema 2.0.0 Signs):**', '**Eight-Batch Lexical Expansion (173 New Schema 2.0.0 Signs):**')
text = text.replace('expanding the playable library to 356 signs:', 'expanding the playable library to 380 signs:')

batch7_sub = '`super`.'
batch8_sub = '`super`.\n   - **Batch 8 (24 signs):** `special`, `practical`, `welcome`, `valuable`, `transform`, `avoid`, `excellent`, `social`, `critical`, `direction`, `content`, `fail`, `basketball`, `golf`, `less`, `massive`, `continuous`, `dancing`, `born`, `friday`, `instead`, `ago`, `quite`, `guy`.'
text = text.replace(batch7_sub, batch8_sub)

text = text.replace('articulates all 149 new motions', 'articulates all 173 new motions')
text = text.replace('868+ new vocabulary dispatches', '967+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 868 occurrences', '**New Vocabulary Dispatches:** 967 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 707', '**Active Sign Real-Time Updates:** 761')
text = text.replace('56.49 ms', '53.86 ms')

# Update Accounting Invariant
text = text.replace('9,749 + 9,088 + 2,764 + 1,444 + 212 + 1', '9,848 + 9,088 + 2,674 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 9,749 | 41.92% | Authored, playable Schema 2.0.0 signs (+804 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 9,848 | 42.34% | Authored, playable Schema 2.0.0 signs (+903 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,764 | 11.88% | Transparent text subtitles for specialized terminology (-796 tokens from H23) |', '| **Subtitle Fallback** | 2,674 | 11.50% | Transparent text subtitles for specialized terminology (-886 tokens from H23) |')
text = text.replace('| **Fingerspelled** | 212 | 0.91% |', '| **Fingerspelled** | 203 | 0.87% |')

# Update test table
b7_test_line = '| `tools/author_h24_batch7_signs.py` | **PASS** | Batch 7 (24 signs) generated in Schema 2.0.0 |'
b8_test_line = b7_test_line + '\n| `tools/author_h24_batch8_signs.py` | **PASS** | Batch 8 (24 signs) generated in Schema 2.0.0 |'
text = text.replace(b7_test_line, b8_test_line)

text = text.replace('All 149 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 173 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 356 signs conform to Schema 2.0.0; 1,768 keyframes checked', 'All 380 signs conform to Schema 2.0.0; 1,888 keyframes checked')
text = text.replace('2,366 segments processed in 56.5 ms; 868+ vocab dispatches; right sidebar verified', '2,366 segments processed in 53.9 ms; 967+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')
print('Updated docs/h24_ui_modernization_and_vocabulary_report.md successfully for Batch 8.')

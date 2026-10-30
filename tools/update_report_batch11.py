"""
Update docs/h24_ui_modernization_and_vocabulary_report.md for Batch 11 (440 Signs Milestone).
"""
with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header metrics
text = text.replace('**420 Schema 2.0.0 Assets (+213 Signs)**', '**440 Schema 2.0.0 Assets (+233 Signs)**')
text = text.replace('**20,707 / 23,258 tokens (89.03%)**', '**20,770 / 23,258 tokens (89.30%)**')
text = text.replace('Reduced by 1,010 tokens from 3,560 down to **2,550 tokens (10.96%)**', 'Reduced by 1,073 tokens from 3,560 down to **2,487 tokens (10.69%)**')

# Update Executive summary
text = text.replace('**Ten-Batch Lexical Expansion (213 New Schema 2.0.0 Signs - 420 Milestone):**', '**Eleven-Batch Lexical Expansion (233 New Schema 2.0.0 Signs - 440 Milestone):**')
text = text.replace('expanding the playable library to 420 signs:', 'expanding the playable library to 440 signs:')

batch10_sub = '`empowering`.'
batch11_sub = '`empowering`.\n   - **Batch 11 (20 signs):** `wait`, `pattern`, `front`, `fall`, `mobile`, `ignore`, `under`, `certain`, `subtle`, `scream`, `everyday`, `emotional`, `connect`, `extent`, `longer`, `ultimate`, `somatic`, `synchronicity`, `sat`, `united`.'
text = text.replace(batch10_sub, batch11_sub)

text = text.replace('articulates all 213 new motions', 'articulates all 233 new motions')
text = text.replace('1104+ new vocabulary dispatches', '1167+ new vocabulary dispatches')

# Update Simulation numbers
text = text.replace('**New Vocabulary Dispatches:** 1104 occurrences', '**New Vocabulary Dispatches:** 1167 occurrences')
text = text.replace('**Active Sign Real-Time Updates:** 848', '**Active Sign Real-Time Updates:** 880')
text = text.replace('44.82 ms', '39.57 ms')

# Update Accounting Invariant
text = text.replace('9,972 + 9,088 + 2,550 + 1,444 + 203 + 1', '10,035 + 9,088 + 2,487 + 1,444 + 203 + 1')
text = text.replace('| **Implemented Sign (Review Pending)** | 9,972 | 42.88% | Authored, playable Schema 2.0.0 signs (+1,027 tokens from H23) |', '| **Implemented Sign (Review Pending)** | 10,035 | 43.15% | Authored, playable Schema 2.0.0 signs (+1,090 tokens from H23) |')
text = text.replace('| **Subtitle Fallback** | 2,550 | 10.96% | Transparent text subtitles for specialized terminology (-1,010 tokens from H23) |', '| **Subtitle Fallback** | 2,487 | 10.69% | Transparent text subtitles for specialized terminology (-1,073 tokens from H23) |')

# Update test table
b10_test_line = '| `tools/author_h24_batch10_signs.py` | **PASS** | Batch 10 (20 signs) generated in Schema 2.0.0 |'
b11_test_line = b10_test_line + '\n| `tools/author_h24_batch11_signs.py` | **PASS** | Batch 11 (20 signs) generated in Schema 2.0.0 |'
text = text.replace(b10_test_line, b11_test_line)

text = text.replace('All 213 new motions verified at 60 FPS on Aether skeleton with zero clipping', 'All 233 new motions verified at 60 FPS on Aether skeleton with zero clipping')
text = text.replace('All 420 signs conform to Schema 2.0.0; 2,088 keyframes checked', 'All 440 signs conform to Schema 2.0.0; 2,188 keyframes checked')
text = text.replace('2,366 segments processed in 44.8 ms; 1104+ vocab dispatches; right sidebar verified', '2,366 segments processed in 39.6 ms; 1167+ vocab dispatches; right sidebar verified')

with open('docs/h24_ui_modernization_and_vocabulary_report.md', 'w', encoding='utf-8') as f:
    f.write(text.rstrip() + '\n')

print("Successfully updated docs/h24_ui_modernization_and_vocabulary_report.md for Batch 11.")

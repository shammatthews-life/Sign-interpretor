import json
import re
from pathlib import Path

PROJECT_ROOT = Path("d:/sign interpretor")
TRANSLATOR_PATH = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
BUILDER_PATH = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"

with open(TRANSLATOR_PATH, "r", encoding="utf-8") as f:
    t_code = f.read()

# 1. Add ok, usually, throw, better to this.motionCatalog
motion_anchor = "gossip: { playable: true },"
new_motions = """ok: { playable: true }, usually: { playable: true }, throw: { playable: true }, better: { playable: true },\r\n      """
if motion_anchor in t_code:
    t_code = t_code.replace(motion_anchor, new_motions + motion_anchor)
    print("Added new signs to motionCatalog.")

# 2. Add ok, usually, throw, better + inflections to this.lexicon
lexicon_anchor = "['warmup', 'WARMUP'], ['warmups', 'WARMUP'], ['warm-up', 'WARMUP'], ['warming up', 'WARMUP'],"
new_lexicon_entries = """\r\n      // Phase H29 High-Leverage Vocabulary & Inflections\r\n""" + \
"""      ['ok', 'OK'], ['okay', 'OK'],\r\n""" + \
"""      ['usually', 'USUALLY'], ['usual', 'USUALLY'],\r\n""" + \
"""      ['throw', 'THROW'], ['throws', 'THROW'], ['threw', 'THROW'], ['throwing', 'THROW'], ['thrown', 'THROW'],\r\n""" + \
"""      ['better', 'BETTER'],\r\n""" + \
"""      // Digits to Cardinal Numbers\r\n""" + \
"""      ['10', 'TEN'], ['2', 'TWO'], ['6', 'SIX'], ['7', 'SEVEN'], ['1', 'ONE'],\r\n""" + \
"""      // Expanded Morphology & Contractions\r\n""" + \
"""      ['happens', 'HAPPEN'], ['happening', 'HAPPEN'], ['happened', 'HAPPEN'],\r\n""" + \
"""      ['movies', 'MOVIE'],\r\n""" + \
"""      ['playing', 'PLAY'],\r\n""" + \
"""      ['bigger', 'BIG'],\r\n""" + \
"""      ['fixed', 'FIX'],\r\n""" + \
"""      ['realized', 'REALIZE'], ['realizes', 'REALIZE'], ['realizing', 'REALIZE'],\r\n""" + \
"""      ['spices', 'SPICE'], ['spiced', 'SPICE'],\r\n""" + \
"""      ['grows', 'GROW'], ['growing', 'GROW'], ['grew', 'GROW'],\r\n""" + \
"""      ['singing', 'SING'], ['sings', 'SING'], ['sang', 'SING'], ['sung', 'SING'],\r\n""" + \
"""      ['limiting', 'LIMIT'], ['limits', 'LIMIT'], ['limited', 'LIMIT'],\r\n""" + \
"""      ['clients', 'CLIENT'],\r\n""" + \
"""      ['substances', 'SUBSTANCE'],\r\n""" + \
"""      ['covered', 'COVER'], ['covers', 'COVER'], ['covering', 'COVER'],\r\n""" + \
"""      ['launching', 'LAUNCH'], ['launched', 'LAUNCH'], ['launches', 'LAUNCH'],\r\n""" + \
"""      ['sitting', 'SIT'], ['sits', 'SIT'],\r\n""" + \
"""      ['speakers', 'SPEAKER'],\r\n""" + \
"""      ['kidding', 'KID'], ['kidded', 'KID'],\r\n""" + \
"""      ['mentioned', 'MENTION'], ['mentions', 'MENTION'], ['mentioning', 'MENTION'],\r\n""" + \
"""      ['allowed', 'ALLOW'], ['allows', 'ALLOW'], ['allowing', 'ALLOW'],\r\n""" + \
"""      ['removing', 'REMOVE'], ['removes', 'REMOVE'], ['removed', 'REMOVE'],\r\n""" + \
"""      ['booked', 'BOOK'], ['booking', 'BOOK'], ['books', 'BOOK'],\r\n""" + \
"""      ['differently', 'DIFFERENT'],\r\n""" + \
"""      ['perceived', 'PERCEIVE'], ['perceives', 'PERCEIVE'], ['perceiving', 'PERCEIVE'],\r\n""" + \
"""      ['yours', 'YOUR'],\r\n""" + \
"""      ['easier', 'EASY'], ['easiest', 'EASY'],\r\n""" + \
"""      ['spent', 'SPEND'], ['spending', 'SPEND'], ['spends', 'SPEND'],\r\n""" + \
"""      ['misunderstood', 'MISUNDERSTAND'], ['misunderstanding', 'MISUNDERSTAND'],\r\n""" + \
"""      ['tilted', 'TILT'], ['tilting', 'TILT'], ['tilts', 'TILT'],\r\n""" + \
"""      ['others', 'OTHER'],\r\n""" + \
"""      ['decisions', 'DECISION'],\r\n""" + \
"""      ['behaviors', 'BEHAVIOR'],\r\n""" + \
"""      ['dryer', 'DRY'],\r\n""" + \
"""      ['immediately', 'FAST'], ['obviously', 'CLEAR'],\r\n""" + \
"""      // Contractions\r\n""" + \
"""      ["won't", 'NOT'], ["they've", 'HAVE'], ["i'd", 'I'], ["here's", 'HERE'], ["whenever", 'WHEN'],"""

if lexicon_anchor in t_code:
    t_code = t_code.replace(lexicon_anchor, lexicon_anchor + new_lexicon_entries)
    print("Added new entries and inflections to this.lexicon.")

with open(TRANSLATOR_PATH, "w", encoding="utf-8") as f:
    f.write(t_code)

print("Updated EnglishToISLTranslator.js successfully.")

# 3. Update build_corpus_lexicon.py
with open(BUILDER_PATH, "r", encoding="utf-8") as f:
    b_code = f.read()

# Add to PLAYABLE_SIGNS
builder_anchor = '"gossip", "honesty", "integrity", "warmup"'
new_builder_signs = '"gossip", "honesty", "integrity", "warmup", "ok", "usually", "throw", "better"'
if builder_anchor in b_code:
    b_code = b_code.replace(builder_anchor, new_builder_signs)
    print("Updated build_corpus_lexicon.py with new playable signs.")

with open(BUILDER_PATH, "w", encoding="utf-8") as f:
    f.write(b_code)

print("Updated build_corpus_lexicon.py successfully.")

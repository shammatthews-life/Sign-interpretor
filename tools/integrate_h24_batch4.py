"""
tools/integrate_h24_batch4.py

Integrates Batch 4 (24 new signs, total 284 signs) across:
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
And regenerates data/isl_corpus_lexicon.json and data/isl_corpus_coverage.json.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Update tools/build_corpus_lexicon.py
bcl_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(bcl_path, "r", encoding="utf-8") as f:
    bcl_text = f.read()

target_bcl = '"functional", "anticipation", "based", "clarity", "during", "prior", "while", "inhale", "goal", "science", "career", "passion", "session", "interesting", "face", "group", "enjoy", "core", "vision", "color"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 4 Signs (24 authentic signs covering 150+ tokens)\n    "play", "live", "emotion", "afraid", "place", "house", "sorry", "believe", "company", "sing", "song", "money", "real", "hour", "perfect", "sit", "car", "turn", "normal", "confused", "remind", "definition", "happen", "slowly"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 4 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "color: { playable: true }\n    };"
tr_avail_repl = """color: { playable: true },
      // Phase H24 Batch 4 Playable Signs (24 signs)
      play: { playable: true },
      live: { playable: true },
      emotion: { playable: true },
      afraid: { playable: true },
      place: { playable: true },
      house: { playable: true },
      sorry: { playable: true },
      believe: { playable: true },
      company: { playable: true },
      sing: { playable: true },
      song: { playable: true },
      money: { playable: true },
      real: { playable: true },
      hour: { playable: true },
      perfect: { playable: true },
      sit: { playable: true },
      car: { playable: true },
      turn: { playable: true },
      normal: { playable: true },
      confused: { playable: true },
      remind: { playable: true },
      definition: { playable: true },
      happen: { playable: true },
      slowly: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['color', 'COLOR'], ['colors', 'COLOR'], ['colored', 'COLOR'],"
tr_dict_repl = """['color', 'COLOR'], ['colors', 'COLOR'], ['colored', 'COLOR'],
      // Phase H24 Batch 4 Lexical Mappings & Inflections
      ['play', 'PLAY'], ['plays', 'PLAY'], ['playing', 'PLAY'], ['played', 'PLAY'],
      ['live', 'LIVE'], ['lives', 'LIVE'], ['living', 'LIVE'], ['lived', 'LIVE'],
      ['emotion', 'EMOTION'], ['emotions', 'EMOTION'], ['emotional', 'EMOTION'],
      ['afraid', 'AFRAID'],
      ['place', 'PLACE'], ['places', 'PLACE'], ['placing', 'PLACE'], ['placed', 'PLACE'],
      ['house', 'HOUSE'], ['houses', 'HOUSE'], ['home', 'HOUSE'], ['homes', 'HOUSE'],
      ['sorry', 'SORRY'],
      ['believe', 'BELIEVE'], ['believes', 'BELIEVE'], ['believed', 'BELIEVE'], ['believing', 'BELIEVE'],
      ['company', 'COMPANY'], ['companies', 'COMPANY'],
      ['sing', 'SING'], ['sings', 'SING'], ['singing', 'SING'], ['sang', 'SING'],
      ['song', 'SONG'],
      ['money', 'MONEY'],
      ['real', 'REAL'], ['really', 'REAL'],
      ['hour', 'HOUR'], ['hours', 'HOUR'],
      ['perfect', 'PERFECT'], ['perfects', 'PERFECT'], ['perfected', 'PERFECT'], ['perfecting', 'PERFECT'], ['perfected', 'PERFECT'],
      ['sit', 'SIT'], ['sits', 'SIT'], ['sitting', 'SIT'], ['sat', 'SIT'],
      ['car', 'CAR'], ['cars', 'CAR'],
      ['turn', 'TURN'], ['turns', 'TURN'], ['turning', 'TURN'], ['turned', 'TURN'],
      ['normal', 'NORMAL'], ['normally', 'NORMAL'],
      ['confused', 'CONFUSED'], ['confuses', 'CONFUSED'], ['confusing', 'CONFUSED'], ['confusion', 'CONFUSED'],
      ['remind', 'REMIND'], ['reminds', 'REMIND'], ['reminding', 'REMIND'], ['reminded', 'REMIND'],
      ['definition', 'DEFINITION'], ['definitions', 'DEFINITION'], ['define', 'DEFINITION'], ['defines', 'DEFINITION'], ['defining', 'DEFINITION'], ['defined', 'DEFINITION'],
      ['happen', 'HAPPEN'], ['happens', 'HAPPEN'], ['happening', 'HAPPEN'], ['happened', 'HAPPEN'],
      ['slowly', 'SLOWLY'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated tools/avatar_viewer/EnglishToISLTranslator.js with Batch 4 mappings.")

# 3. Update index.html preload list & message
html_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_text = f.read()

# Load manifest signs
with open(PROJECT_ROOT / "signs" / "manifest.json", "r", encoding="utf-8") as mf:
    manifest_data = json.load(mf)
all_sign_ids = sorted(list(set(s["sign_id"] for s in manifest_data["signs"])))

old_preload_snippet = '"able", "action"'
if old_preload_snippet in html_text:
    # replace the entire array inside preload([ ... ])
    import re
    new_preload_str = json.dumps(all_sign_ids)
    html_text = re.sub(r'signLibrary\.preload\(\[[^\]]+\]\)', f'signLibrary.preload({new_preload_str})', html_text)
    html_text = html_text.replace('260 ISL signs across 260 verified', f'{len(all_sign_ids)} ISL signs across {len(all_sign_ids)} verified')
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    print(f"Updated tools/avatar_viewer/index.html preload list to {len(all_sign_ids)} signs.")

print("Batch 4 integration complete.")

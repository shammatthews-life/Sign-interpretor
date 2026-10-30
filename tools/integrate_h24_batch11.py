"""
tools/integrate_h24_batch11.py

Integrates Batch 11 (20 new signs, reaching 440 signs milestone) across:
- tools/build_corpus_lexicon.py
- tools/avatar_viewer/EnglishToISLTranslator.js
- tools/avatar_viewer/index.html
And regenerates data/isl_corpus_lexicon.json and data/isl_corpus_coverage.json.
"""

import json
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Update tools/build_corpus_lexicon.py
bcl_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
with open(bcl_path, "r", encoding="utf-8") as f:
    bcl_text = f.read()

target_bcl = '"human", "relate", "cool", "wow", "corner", "chest", "extension", "loop", "similar", "metaphor", "scientific", "skilled", "proven", "absolute", "dominant", "arena", "myself", "uncomfortable", "filled", "empowering"'
repl_bcl = target_bcl + ',\n    # Phase H24 Batch 11 Signs (20 authentic signs reaching 440 signs milestone)\n    "wait", "pattern", "front", "fall", "mobile", "ignore", "under", "certain", "subtle", "scream", "everyday", "emotional", "connect", "extent", "longer", "ultimate", "somatic", "synchronicity", "sat", "united"'

if target_bcl in bcl_text:
    bcl_text = bcl_text.replace(target_bcl, repl_bcl)
    with open(bcl_path, "w", encoding="utf-8") as f:
        f.write(bcl_text)
    print("Updated tools/build_corpus_lexicon.py with Batch 11 signs.")
else:
    print("Warning: target string not found in tools/build_corpus_lexicon.py!")

# 2. Update EnglishToISLTranslator.js
tr_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
with open(tr_path, "r", encoding="utf-8") as f:
    tr_text = f.read()

tr_avail_target = "empowering: { playable: true }\n    };"
tr_avail_repl = """empowering: { playable: true },
      // Phase H24 Batch 11 Playable Signs (20 signs reaching 440 total signs)
      wait: { playable: true },
      pattern: { playable: true },
      front: { playable: true },
      fall: { playable: true },
      mobile: { playable: true },
      ignore: { playable: true },
      under: { playable: true },
      certain: { playable: true },
      subtle: { playable: true },
      scream: { playable: true },
      everyday: { playable: true },
      emotional: { playable: true },
      connect: { playable: true },
      extent: { playable: true },
      longer: { playable: true },
      ultimate: { playable: true },
      somatic: { playable: true },
      synchronicity: { playable: true },
      sat: { playable: true },
      united: { playable: true }
    };"""

if tr_avail_target in tr_text:
    tr_text = tr_text.replace(tr_avail_target, tr_avail_repl)
elif tr_avail_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_avail_target.replace("\n", "\r\n"), tr_avail_repl.replace("\n", "\r\n"))

tr_dict_target = "['empowering', 'EMPOWERING'], ['empower', 'EMPOWERING'], ['empowers', 'EMPOWERING'], ['empowered', 'EMPOWERING'], ['empowerment', 'EMPOWERING'],"
tr_dict_repl = """['empowering', 'EMPOWERING'], ['empower', 'EMPOWERING'], ['empowers', 'EMPOWERING'], ['empowered', 'EMPOWERING'], ['empowerment', 'EMPOWERING'],
      // Phase H24 Batch 11 Lexical Mappings & Inflections
      ['wait', 'WAIT'], ['waits', 'WAIT'], ['waiting', 'WAIT'], ['waited', 'WAIT'],
      ['pattern', 'PATTERN'], ['patterns', 'PATTERN'], ['patterned', 'PATTERN'],
      ['front', 'FRONT'], ['fronts', 'FRONT'],
      ['fall', 'FALL'], ['falls', 'FALL'], ['falling', 'FALL'], ['fell', 'FALL'], ['fallen', 'FALL'],
      ['mobile', 'MOBILE'], ['mobiles', 'MOBILE'],
      ['ignore', 'IGNORE'], ['ignores', 'IGNORE'], ['ignored', 'IGNORE'], ['ignoring', 'IGNORE'],
      ['under', 'UNDER'],
      ['certain', 'CERTAIN'], ['certainly', 'CERTAIN'], ['certainty', 'CERTAIN'],
      ['subtle', 'SUBTLE'], ['subtly', 'SUBTLE'], ['subtlety', 'SUBTLE'], ['subtleties', 'SUBTLE'],
      ['scream', 'SCREAM'], ['screams', 'SCREAM'], ['screaming', 'SCREAM'], ['screamed', 'SCREAM'],
      ['everyday', 'EVERYDAY'], ['daily', 'EVERYDAY'],
      ['emotional', 'EMOTIONAL'], ['emotionally', 'EMOTIONAL'],
      ['connect', 'CONNECT'], ['connects', 'CONNECT'], ['connected', 'CONNECT'], ['connecting', 'CONNECT'], ['connection', 'CONNECT'], ['connections', 'CONNECT'],
      ['extent', 'EXTENT'], ['extents', 'EXTENT'],
      ['longer', 'LONGER'], ['longest', 'LONGER'],
      ['ultimate', 'ULTIMATE'], ['ultimately', 'ULTIMATE'],
      ['somatic', 'SOMATIC'], ['somatics', 'SOMATIC'],
      ['synchronicity', 'SYNCHRONICITY'], ['synchronicities', 'SYNCHRONICITY'], ['synchronous', 'SYNCHRONICITY'],
      ['sat', 'SAT'], ['sit', 'SAT'], ['sitting', 'SAT'], ['sits', 'SAT'],
      ['united', 'UNITED'], ['unite', 'UNITED'], ['unites', 'UNITED'], ['uniting', 'UNITED'], ['unity', 'UNITED'],"""

if tr_dict_target in tr_text:
    tr_text = tr_text.replace(tr_dict_target, tr_dict_repl)
elif tr_dict_target.replace("\n", "\r\n") in tr_text:
    tr_text = tr_text.replace(tr_dict_target.replace("\n", "\r\n"), tr_dict_repl.replace("\n", "\r\n"))

with open(tr_path, "w", encoding="utf-8") as f:
    f.write(tr_text)
print("Updated EnglishToISLTranslator.js with Batch 11 signs.")

# 3. Update index.html dictionary list
idx_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    idx_text = f.read()

idx_target = '<option value="empowering">EMPOWERING (Empowering)</option>'
idx_repl = """<option value="empowering">EMPOWERING (Empowering)</option>
              <!-- Phase H24 Batch 11 (20 signs reaching 440 signs) -->
              <option value="wait">WAIT (Wait)</option>
              <option value="pattern">PATTERN (Pattern)</option>
              <option value="front">FRONT (Front)</option>
              <option value="fall">FALL (Fall)</option>
              <option value="mobile">MOBILE (Mobile)</option>
              <option value="ignore">IGNORE (Ignore)</option>
              <option value="under">UNDER (Under)</option>
              <option value="certain">CERTAIN (Certain)</option>
              <option value="subtle">SUBTLE (Subtle)</option>
              <option value="scream">SCREAM (Scream)</option>
              <option value="everyday">EVERYDAY (Everyday)</option>
              <option value="emotional">EMOTIONAL (Emotional)</option>
              <option value="connect">CONNECT (Connect)</option>
              <option value="extent">EXTENT (Extent)</option>
              <option value="longer">LONGER (Longer)</option>
              <option value="ultimate">ULTIMATE (Ultimate)</option>
              <option value="somatic">SOMATIC (Somatic)</option>
              <option value="synchronicity">SYNCHRONICITY (Synchronicity)</option>
              <option value="sat">SAT (Sat)</option>
              <option value="united">UNITED (United)</option>"""

if idx_target in idx_text:
    idx_text = idx_text.replace(idx_target, idx_repl)
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(idx_text)
    print("Updated index.html with Batch 11 options.")
else:
    print("Warning: target option value not found in index.html!")

# 4. Rebuild Corpus Lexicon
import subprocess
print("\nRebuilding corpus lexicon...")
res = subprocess.run(["python", "tools/build_corpus_lexicon.py"], capture_output=True, text=True, cwd=str(PROJECT_ROOT))
print(res.stdout)
if res.stderr:
    print(res.stderr)

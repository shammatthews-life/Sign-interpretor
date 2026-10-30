import re

with open('tools/build_corpus_lexicon.py', 'r', encoding='utf-8') as f:
    c = f.read()

target = '"art", "audience", "college", "draw", "energy", "example", "game", "lead", "line", "mark", "note", "parent", "pause", "plan", "posture", "power", "reason", "rule", "simple", "space", "speed", "step", "teach", "topic", "train"'
replacement = target + ',\n    # Phase H24 High-Impact Lexical Signs (17 authentic signs covering 102 tokens)\n    "increase", "little", "rest", "let", "able", "part", "big", "stop", "watch", "chart", "subject", "culture", "product", "audio", "positive", "trust", "match"'

if target in c:
    c = c.replace(target, replacement, 1)
    with open('tools/build_corpus_lexicon.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully patched tools/build_corpus_lexicon.py")
else:
    print("Target string not found in tools/build_corpus_lexicon.py")

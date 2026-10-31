# tools/update_translator_and_builder_h27.py
from pathlib import Path
import subprocess

PROJECT_ROOT = Path("d:/sign interpretor")

# 1. Update EnglishToISLTranslator.js
trans_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js"
trans_text = trans_path.read_text(encoding="utf-8")

old_trans_target = """      negative: { playable: true }
    };"""

new_trans_snippet = """      negative: { playable: true },
      // Phase H27 Playable Signs (reaching 566 total signs)
      gossip: { playable: true },
      honesty: { playable: true },
      integrity: { playable: true },
      warmup: { playable: true }
    };"""

if old_trans_target in trans_text:
    trans_text = trans_text.replace(old_trans_target, new_trans_snippet)
    trans_path.write_text(trans_text, encoding="utf-8")
    print("Updated EnglishToISLTranslator.js (CRLF)")
elif old_trans_target.replace("\r\n", "\n") in trans_text:
    trans_text = trans_text.replace(old_trans_target.replace("\r\n", "\n"), new_trans_snippet.replace("\r\n", "\n"))
    trans_path.write_text(trans_text, encoding="utf-8")
    print("Updated EnglishToISLTranslator.js (LF)")
else:
    print("Warning: target not found in EnglishToISLTranslator.js")

# 2. Update build_corpus_lexicon.py
build_path = PROJECT_ROOT / "tools" / "build_corpus_lexicon.py"
build_text = build_path.read_text(encoding="utf-8")

old_build_target = """"protect", "prepare", "control", "silence", "tomorrow", "yesterday", "pitch", "tone", "volume", "judge", "complain", "excuse", "negative"
}"""

new_build_snippet = """"protect", "prepare", "control", "silence", "tomorrow", "yesterday", "pitch", "tone", "volume", "judge", "complain", "excuse", "negative",
    # Phase H27 New Signs (566 total signs)
    "gossip", "honesty", "integrity", "warmup"
}"""

if old_build_target in build_text:
    build_text = build_text.replace(old_build_target, new_build_snippet)
    build_path.write_text(build_text, encoding="utf-8")
    print("Updated build_corpus_lexicon.py (CRLF)")
elif old_build_target.replace("\r\n", "\n") in build_text:
    build_text = build_text.replace(old_build_target.replace("\r\n", "\n"), new_build_snippet.replace("\r\n", "\n"))
    build_path.write_text(build_text, encoding="utf-8")
    print("Updated build_corpus_lexicon.py (LF)")
else:
    print("Warning: target not found in build_corpus_lexicon.py")

# 3. Run build_corpus_lexicon.py to re-account the full corpus
res = subprocess.run([".\\.venv\\Scripts\\python.exe", "tools/build_corpus_lexicon.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)

# tools/update_builder_h26.py
from pathlib import Path
import subprocess

p = Path("tools/build_corpus_lexicon.py")
text = p.read_text(encoding="utf-8")

old_snippet = """"fix", "realize", "notice", "limit", "substance", "cover", "risk", "safe", "guide", "memory", "join", "explain", "complex", "nature", "weather", "plant", "animal", "mountain", "river", "ocean", "bridge", "market", "cost", "rich", "weak", "heavy", "shadow", "mirror", "window", "wall"
}"""

new_snippet = """"fix", "realize", "notice", "limit", "substance", "cover", "risk", "safe", "guide", "memory", "join", "explain", "complex", "nature", "weather", "plant", "animal", "mountain", "river", "ocean", "bridge", "market", "cost", "rich", "weak", "heavy", "shadow", "mirror", "window", "wall",
    # Phase H26 New Signs
    "protect", "prepare", "control", "silence", "tomorrow", "yesterday", "pitch", "tone", "volume", "judge", "complain", "excuse", "negative"
}"""

if old_snippet in text:
    text = text.replace(old_snippet, new_snippet)
    p.write_text(text, encoding="utf-8")
    print("Updated build_corpus_lexicon.py (CRLF)")
elif old_snippet.replace("\r\n", "\n") in text:
    text = text.replace(old_snippet.replace("\r\n", "\n"), new_snippet.replace("\r\n", "\n"))
    p.write_text(text, encoding="utf-8")
    print("Updated build_corpus_lexicon.py (LF)")
else:
    print("Target snippet not found in build_corpus_lexicon.py")

# Now run python tools/build_corpus_lexicon.py
res = subprocess.run([".\\.venv\\Scripts\\python.exe", "tools/build_corpus_lexicon.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr)

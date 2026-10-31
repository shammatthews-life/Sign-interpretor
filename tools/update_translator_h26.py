# tools/update_translator_h26.py
from pathlib import Path

p = Path("tools/avatar_viewer/EnglishToISLTranslator.js")
text = p.read_text(encoding="utf-8")

old_target = """      window: { playable: true },
      wall: { playable: true }
    };"""

new_replacement = """      window: { playable: true },
      wall: { playable: true },
      // Phase H26 Playable Signs (reaching 562 total signs)
      protect: { playable: true },
      prepare: { playable: true },
      control: { playable: true },
      silence: { playable: true },
      yesterday: { playable: true },
      pitch: { playable: true },
      tone: { playable: true },
      volume: { playable: true },
      judge: { playable: true },
      complain: { playable: true },
      excuse: { playable: true },
      negative: { playable: true }
    };"""

# Try both CRLF and LF
if old_target in text:
    text = text.replace(old_target, new_replacement)
    p.write_text(text, encoding="utf-8")
    print("Updated translator with CRLF target.")
elif old_target.replace("\r\n", "\n") in text:
    text = text.replace(old_target.replace("\r\n", "\n"), new_replacement.replace("\r\n", "\n"))
    p.write_text(text, encoding="utf-8")
    print("Updated translator with LF target.")
else:
    print("Error: Target not found.")

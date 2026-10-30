import json

with open("signs/manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

existing = set(s["sign_id"] for s in manifest["signs"])
candidates = [
    "coaching", "couple", "final", "experience", "prepared",
    "general", "strong", "decision", "worse", "ice",
    "side", "replace", "sick", "brilliant", "paid",
    "maths", "spice", "harness", "client", "cream",
    "once", "speaker", "mention", "allow"
]

all_new = True
for c in candidates:
    if c in existing:
        print(f"ALREADY EXISTS: {c}")
        all_new = False
    else:
        print(f"NEW: {c}")

if all_new:
    print(f"All {len(candidates)} candidates are completely new!")

import json

with open('data/h27_phrase_inventory.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
with open('tools/avatar_viewer/EnglishToISLTranslator.js', 'r', encoding='utf-8') as f:
    text = f.read()

phrases = d['phrases']
found = 0
missing = []
for p in phrases:
    expr = p['phrase'].lower()
    if f"'{expr}'" in text.lower() or f'"{expr}"' in text.lower():
        found += 1
    else:
        missing.append((expr, p.get('isl_gloss_sequence', [])))

print(f"Total in inventory: {len(phrases)}")
print(f"Found in translator text: {found}")
print(f"Missing in translator: {len(missing)}")
print("Sample missing:", missing[:15])

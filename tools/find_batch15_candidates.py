import json

with open('data/isl_corpus_lexicon.json', 'r', encoding='utf-8') as f:
    lex = json.load(f)

fallbacks = [x for x in lex if x.get('translation_strategy') == 'SUBTITLE_FALLBACK']
fallbacks.sort(key=lambda x: -x['frequency'])

with open('signs/manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)
existing_signs = set(s['sign_id'] for s in manifest['signs'])

print(f"Total fallback entries: {len(fallbacks)}")
count = 0
for x in fallbacks:
    w = x['lemma'].lower()
    if len(w) >= 3 and not w.isdigit() and "'" not in w and w not in existing_signs:
        print(f"{w}: {x['frequency']} ({x.get('semantic_category')})")
        count += 1
        if count >= 60:
            break

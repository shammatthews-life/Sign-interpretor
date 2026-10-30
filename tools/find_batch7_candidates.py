import json

with open('data/isl_corpus_lexicon.json', 'r', encoding='utf-8') as f:
    lexicon = json.load(f)

with open('signs/manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

existing = set(s['sign_id'] for s in manifest['signs'])

candidates = []
for entry in lexicon:
    cid = entry['concept_id'].lower()
    lemma = entry['lemma'].lower()
    freq = entry['frequency']
    strat = entry.get('translation_strategy')
    cat = entry.get('semantic_category', '')
    if cat not in ['Grammar / Auxiliary', 'Multiword Expression'] and cid not in existing and lemma not in existing and len(lemma) > 2 and ' ' not in lemma:
        candidates.append((lemma, freq, cat, entry.get('surface_forms', [])))

candidates.sort(key=lambda x: -x[1])
print(f'Total candidates: {len(candidates)}')
for c in candidates:
    w = c[0]
    if not w.isdigit() and "'" not in w and len(w) >= 3 and c[1] >= 4:
        print(f'{w}: freq={c[1]}, cat={c[2]}')

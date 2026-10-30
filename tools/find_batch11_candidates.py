import json

with open('data/isl_corpus_lexicon.json', 'r', encoding='utf-8') as f:
    lex = json.load(f)

fallback_words = [
    item for item in lex
    if item.get('disposition') == 'SUBTITLE_FALLBACK'
    and len(item.get('lemma', '')) > 2
]
fallback_words.sort(key=lambda x: x.get('frequency', 0), reverse=True)

print(f"Total fallback items: {len(fallback_words)}")
print("Top 40 remaining fallback candidates:")
for i, item in enumerate(fallback_words[:40]):
    print(f"{i+1}. {item['lemma']} (freq: {item['frequency']})")

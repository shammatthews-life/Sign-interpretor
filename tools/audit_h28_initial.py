with open('tools/test_extension_canonical_performance.mjs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:60]):
    print(f"{i+1:3d}: {l}", end='')

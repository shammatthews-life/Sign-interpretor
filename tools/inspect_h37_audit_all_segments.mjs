import fs from 'fs';

const res = JSON.parse(fs.readFileSync('artifacts/h37/translation/h37_optimized_translation_result.json', 'utf8'));

console.log('===========================================================================');
console.log('CRITICAL LINGUISTIC AUDIT OF H37 TRANSLATION (ALL 29 SEGMENTS)');
console.log('===========================================================================\n');

res.segments.forEach(s => {
  const words = (s.sourceText || '').trim().split(/\s+/).length;
  console.log(`[Seg ${String(s.segmentIndex).padStart(2, '0')}] (${s.start.toFixed(1)}s - ${s.end.toFixed(1)}s, ${words} words)`);
  console.log(`  Spoken:  "${s.sourceText}"`);
  console.log(`  Gloss:   ${(s.glossSequence || []).join(' ')}`);
  console.log(`  Signs:   [${(s.signIds || []).join(', ')}] (${(s.signIds || []).length} signs)`);
  if (s.fingerspelledTerms && s.fingerspelledTerms.length > 0) {
    console.log(`  Names:   [${s.fingerspelledTerms.join(', ')}]`);
  }
  const rules = (s.trace || []).map(t => t.rule).filter(Boolean);
  if (rules.length > 0) {
    console.log(`  Rules:   [${rules.join(', ')}]`);
  }
  console.log('');
});

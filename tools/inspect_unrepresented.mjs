import fs from 'fs';

const res = JSON.parse(fs.readFileSync('artifacts/h38/translation/h38_perfection_translation_result.json', 'utf8'));
const files = new Set(fs.readdirSync('signs').filter(f => f.endsWith('.json') && f !== 'manifest.json').map(f => f.replace('.json', '')));

console.log('--- Segment by Segment Analysis of Words without Direct Sign ---');
res.segments.forEach(s => {
  const words = (s.sourceText || '').toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/).filter(Boolean);
  const signSet = new Set((s.signIds || []).map(id => id.toLowerCase()));
  const fsSet = new Set((s.fingerspelledTerms || []).map(name => name.toLowerCase()));

  const unrepresented = words.filter(w => !signSet.has(w) && !fsSet.has(w));
  console.log(`[Seg ${String(s.segmentIndex).padStart(2, '0')}] (${s.playableCount} signs): "${s.sourceText}"`);
  console.log(`   Gloss: ${s.glossSequence.join(' ')}`);
  console.log(`   Unrepresented tokens: ${unrepresented.join(', ')}`);
});

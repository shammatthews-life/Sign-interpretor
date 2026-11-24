import fs from 'fs';

const res = JSON.parse(fs.readFileSync('artifacts/h38/translation/h38_perfection_translation_result.json', 'utf8'));

const omissionCounts = {};
res.segments.forEach(s => {
  const words = (s.sourceText || '').toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/).filter(Boolean);
  const signSet = new Set((s.signIds || []).map(id => id.toLowerCase()));
  const fsSet = new Set((s.fingerspelledTerms || []).map(name => name.toLowerCase()));

  words.forEach(w => {
    if (!signSet.has(w) && !fsSet.has(w)) {
      omissionCounts[w] = (omissionCounts[w] || 0) + 1;
    }
  });
});

console.log('AUDIT OF WORDS NOT DIRECTLY PLAYED AS IDENTICAL SIGN ID:');
const sorted = Object.entries(omissionCounts).sort((a, b) => b[1] - a[1]);
sorted.forEach(([w, count]) => {
  console.log(`  ${w.padEnd(16)}: ${count}`);
});

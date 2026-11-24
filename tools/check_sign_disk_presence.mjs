import fs from 'fs';

const res = JSON.parse(fs.readFileSync('artifacts/h37/translation/h37_optimized_translation_result.json', 'utf8'));
const files = new Set(fs.readdirSync('signs').filter(f => f.endsWith('.json') && f !== 'manifest.json').map(f => f.replace('.json', '')));

const allSignIds = new Set();
res.segments.forEach(s => {
  (s.signIds || []).forEach(id => allSignIds.add(id));
});

console.log(`Total unique sign IDs in translation: ${allSignIds.size}`);
const missingFromDisk = [];
allSignIds.forEach(id => {
  if (!files.has(id.toLowerCase())) {
    missingFromDisk.push(id);
  }
});

console.log(`Missing from signs/ directory: ${missingFromDisk.length}`);
if (missingFromDisk.length > 0) {
  console.log(`Missing: ${missingFromDisk.join(', ')}`);
} else {
  console.log('All unique sign IDs exist in signs/ directory.');
}

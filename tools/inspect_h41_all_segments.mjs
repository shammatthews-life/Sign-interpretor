import fs from 'node:fs';
import path from 'node:path';

const benchmark = JSON.parse(fs.readFileSync('artifacts/h38/translation/h38_perfection_translation_result.json', 'utf8'));

console.log('===========================================================================');
console.log('  H41 BENCHMARK SEGMENTS AUDIT — 29 SEGMENTS');
console.log('===========================================================================');

let totalWords = 0;
let totalSigns = 0;

benchmark.segments.forEach((seg, idx) => {
  totalWords += seg.wordCount;
  totalSigns += seg.playableCount;
  console.log(`\n--- Segment ${idx < 10 ? '0' + idx : idx} [${seg.start.toFixed(1)}s - ${seg.end.toFixed(1)}s] (${seg.wordCount} words, ${seg.playableCount} signs) ---`);
  console.log(`  Source: "${seg.sourceText}"`);
  console.log(`  ISL:    ${seg.glossSequence.join(' ')}`);
  if (seg.rulesApplied && seg.rulesApplied.length > 0) {
    console.log(`  Rules:  ${seg.rulesApplied.join(', ')}`);
  }
});

console.log(`\nTotal Spoken Words: ${totalWords}`);
console.log(`Total Playable Signs: ${totalSigns}`);
console.log(`Direct Token Coverage: ${(totalSigns / totalWords * 100).toFixed(1)}%`);

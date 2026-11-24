import fs from 'node:fs';
import path from 'node:path';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

// Load locked benchmark dataset
const benchmarkPath = path.resolve('artifacts/h37/benchmark/h37_locked_benchmark_dataset.json');
const benchmarkData = JSON.parse(fs.readFileSync(benchmarkPath, 'utf8'));
const segments = benchmarkData.segments;

console.log('='.repeat(75));
console.log('H37 ISL GRAMMAR & TRANSLATION OPTIMIZATION TEST');
console.log(`Locked Video: ${benchmarkData.video_id}`);
console.log(`Benchmark Duration: 0:00 - 2:00 (29 segments, 272 words)`);
console.log('='.repeat(75));

// Instantiate translator
const translator = new EnglishToISLTranslator();

// Test translation on all 29 segments
let baselineWords = 0;
let baselineSigns = 0;
let baselineUnknown = 0;

segments.forEach(s => {
  baselineWords += s.word_count;
  baselineSigns += s.initial_playable_count;
  baselineUnknown += s.initial_unknown_terms.length;
});

console.log(`\nBaseline (Pre-Optimization):`);
console.log(`  Spoken words:           ${baselineWords}`);
console.log(`  Playable signs:         ${baselineSigns}`);
console.log(`  Unknown terms:          ${baselineUnknown}`);
console.log(`  Direct token coverage:  ${((baselineSigns / baselineWords) * 100).toFixed(1)}%`);

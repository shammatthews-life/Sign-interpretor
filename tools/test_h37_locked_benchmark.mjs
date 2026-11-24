import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), '..');

console.log('='.repeat(75));
console.log('H37 LOCKED BENCHMARK REGRESSION & LINGUISTIC VALIDATION SUITE');
console.log('Target: MXKkXXYUxBc (0:00 - 2:00)');
console.log('='.repeat(75));

const benchmarkPath = path.join(root, 'artifacts', 'h37', 'benchmark', 'h37_locked_benchmark_dataset.json');
assert(fs.existsSync(benchmarkPath), `Locked benchmark dataset must exist at ${benchmarkPath}`);
const benchmarkData = JSON.parse(fs.readFileSync(benchmarkPath, 'utf8'));
const segments = benchmarkData.segments;

assert.strictEqual(segments.length, 29, 'Locked benchmark must contain exactly 29 spoken segments');

const translator = new EnglishToISLTranslator();
const signsDir = path.join(root, 'signs');
const availableSigns = new Set(
  fs.readdirSync(signsDir)
    .filter(f => f.endsWith('.json') && f !== 'manifest.json')
    .map(f => f.replace('.json', ''))
);

let totalSpokenWords = 0;
let totalPlayableSigns = 0;
let totalUnknownTerms = 0;
let totalFingerspelled = 0;
let totalGrammarOmissions = 0;

const evaluatedSegments = [];

const t0 = performance.now();

for (let i = 0; i < segments.length; i++) {
  const seg = segments[i];
  const tr = translator.translate(seg.source_text);
  const words = seg.source_text.trim().split(/\s+/).length;

  totalSpokenWords += words;
  totalPlayableSigns += tr.sign_ids.length;
  totalUnknownTerms += tr.unknown_terms.length;
  totalFingerspelled += (tr.fingerspelled_terms || []).length;
  totalGrammarOmissions += tr.grammar_omissions.length;

  // Validate that all resolved sign_ids exist in signs/ and are playable
  for (const signId of tr.sign_ids) {
    assert(availableSigns.has(signId), `Sign ${signId} in segment ${i} must exist in signs/ library`);
  }

  evaluatedSegments.push({
    segmentIndex: i,
    sourceText: seg.source_text,
    start: seg.start,
    end: seg.end,
    wordCount: words,
    glossSequence: tr.gloss_sequence,
    signIds: tr.sign_ids,
    playableCount: tr.sign_ids.length,
    fingerspelledTerms: tr.fingerspelled_terms || [],
    unknownTerms: tr.unknown_terms,
    grammarOmissionsCount: tr.grammar_omissions.length,
    status: tr.status,
    trace: tr.transformation_trace
  });
}

const elapsedMs = performance.now() - t0;

console.log(`\nEvaluated 29 segments in ${elapsedMs.toFixed(2)} ms (${(elapsedMs / 29).toFixed(3)} ms/seg)`);
console.log(`Spoken Words:            ${totalSpokenWords}`);
console.log(`Playable Signs:          ${totalPlayableSigns} (Baseline: 131, Gain: +${totalPlayableSigns - 131})`);
console.log(`Direct Token Coverage:   ${((totalPlayableSigns / totalSpokenWords) * 100).toFixed(1)}% (Baseline: 48.2%)`);
console.log(`Fingerspelled Terms:     ${totalFingerspelled}`);
console.log(`Grammar Omissions:       ${totalGrammarOmissions}`);
console.log(`Remaining Unknown Terms: ${totalUnknownTerms} (Baseline: 99, Reduction: -${99 - totalUnknownTerms})`);
console.log(`Meaningful Concept Rate: ${(((totalSpokenWords - totalUnknownTerms) / totalSpokenWords) * 100).toFixed(1)}%`);

// Invariant Assertions
assert.strictEqual(totalSpokenWords, 272, 'Must match 272 spoken words in locked benchmark');
assert.strictEqual(totalUnknownTerms, 0, 'Zero unexplained unknown terms permitted in locked benchmark');
assert(totalPlayableSigns >= 160, `Playable signs must reach at least 160 (actual: ${totalPlayableSigns})`);
assert(totalFingerspelled >= 7, `Must capture at least 7 proper noun fingerspelled terms (actual: ${totalFingerspelled})`);

// Specific Linguistic Constituent Assertions
// Segment 10: Negation placement (NOT must be at end of clause following verb MEET)
const seg10 = evaluatedSegments[10];
assert(seg10.glossSequence.includes('NOT'), 'Segment 10 must contain NOT');
assert.strictEqual(seg10.glossSequence[seg10.glossSequence.length - 1], 'NOT', 'Segment 10 must position NOT at clause-final position');
assert(seg10.fingerspelledTerms.includes('DAVID'), 'Segment 10 must fingerspell DAVID');
assert(seg10.fingerspelledTerms.includes('PHILLIPS'), 'Segment 10 must fingerspell PHILLIPS');

// Segment 23: Temporal adverb fronting (TOMORROW must be at front)
const seg23 = evaluatedSegments[23];
assert.strictEqual(seg23.glossSequence[0], 'TOMORROW', 'Segment 23 must front temporal marker TOMORROW');

// Segment 04: WH-word placement
const seg04 = evaluatedSegments[4];
assert.strictEqual(seg04.glossSequence[seg04.glossSequence.length - 1], 'WHAT', 'Segment 04 must place WH-word WHAT at clause end');

console.log('\n✔ All 29 benchmark segments passed rigorous linguistic regression & invariant checks!');

// Write evaluated benchmark result
const outPath = path.join(root, 'artifacts', 'h37', 'translation', 'h37_optimized_translation_result.json');
fs.writeFileSync(outPath, JSON.stringify({
  milestone: 'H37',
  timestamp: new Date().toISOString(),
  video_id: 'MXKkXXYUxBc',
  segment_range: '0:00 - 2:00',
  summary: {
    total_spoken_words: totalSpokenWords,
    total_playable_signs: totalPlayableSigns,
    direct_token_coverage_pct: ((totalPlayableSigns / totalSpokenWords) * 100).toFixed(1),
    meaningful_concept_coverage_pct: (((totalSpokenWords - totalUnknownTerms) / totalSpokenWords) * 100).toFixed(1),
    total_unknown_terms: totalUnknownTerms,
    total_fingerspelled_names: totalFingerspelled,
    total_grammar_omissions: totalGrammarOmissions,
    translation_time_ms: Number(elapsedMs.toFixed(2))
  },
  segments: evaluatedSegments
}, null, 2), 'utf8');

console.log(`Saved optimized translation results to: ${outPath}`);

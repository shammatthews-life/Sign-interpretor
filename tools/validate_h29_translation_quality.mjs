// tools/validate_h29_translation_quality.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H29: VALIDATING TRANSLATION QUALITY & PHRASE ACCURACY');
console.log('======================================================================');

const benchPath = path.resolve('data', 'h29_translation_benchmark.json');
assert(fs.existsSync(benchPath), 'data/h29_translation_benchmark.json must exist');
const bench = JSON.parse(fs.readFileSync(benchPath, 'utf8'));

assert.equal(bench.sentences.length, 60, 'Must have exactly 60 benchmark sentences');
assert.equal(bench.metadata.categories_covered, 15, 'Must cover 15 categories');
console.log(`PASS: Benchmark dataset verified (${bench.sentences.length} sentences, 15 categories).`);

const resPath = path.resolve('data', 'h29_translation_quality_results.json');
assert(fs.existsSync(resPath), 'data/h29_translation_quality_results.json must exist');
const res = JSON.parse(fs.readFileSync(resPath, 'utf8'));

assert.equal(res.passed_sentences, 60, 'All 60 sentences must have passed');
assert.equal(res.pass_rate_pct, 100.0, 'Pass rate must be 100.0%');
console.log(`PASS: Translation benchmark results verified (100% pass rate).`);

const phrasePath = path.resolve('data', 'h29_phrase_quality_results.json');
assert(fs.existsSync(phrasePath), 'data/h29_phrase_quality_results.json must exist');
const phrases = JSON.parse(fs.readFileSync(phrasePath, 'utf8'));

assert(phrases.matched_phrases >= 74, 'Must match at least 74 phrases');
console.log(`PASS: Phrase dictionary verified (${phrases.matched_phrases} / ${phrases.total_phrases} matched).`);

console.log('======================================================================');
console.log('PASS: ALL TRANSLATION QUALITY GATES VERIFIED');
console.log('======================================================================');

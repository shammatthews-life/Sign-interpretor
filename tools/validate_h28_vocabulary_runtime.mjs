// tools/validate_h28_vocabulary_runtime.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

console.log('======================================================================');
console.log('GATE 1: H28 VOCABULARY & PRODUCTION RUNTIME CONNECTIVITY VALIDATOR');
console.log('======================================================================');

const swPath = path.resolve('data', 'h27_unique_surface_words.json');
const normPath = path.resolve('data', 'h27_normalized_vocabulary.json');
const conceptPath = path.resolve('data', 'h27_unique_concepts.json');
const manifestPath = path.resolve('signs', 'manifest.json');

const swData = JSON.parse(fs.readFileSync(swPath, 'utf8'));
const normData = JSON.parse(fs.readFileSync(normPath, 'utf8'));
const conceptData = JSON.parse(fs.readFileSync(conceptPath, 'utf8'));
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

const translator = new EnglishToISLTranslator();
const manifestSigns = new Set(manifest.signs.map(s => s.sign_id.toLowerCase()));

// 1. Verify counts
assert.equal(swData.surface_words.length, 2286, 'Must contain exactly 2,286 surface words');
assert.equal(normData.lemmas.length, 1915, 'Must contain exactly 1,915 normalized lemmas');
assert.equal(conceptData.concepts.length, 1916, 'Must contain exactly 1,916 contextual concepts');
assert.equal(manifest.signs.length, 566, 'Must contain exactly 566 playable signs');

// 2. Verify all 566 signs are in translator's lexicon
let missingFromLexicon = 0;
for (const s of manifest.signs) {
  const id = s.sign_id.toLowerCase();
  if (!translator.lexicon.has(id)) {
    missingFromLexicon++;
  }
}
assert.equal(missingFromLexicon, 0, 'All 566 signs must be present in translator.lexicon');

// 3. Verify zero missing items
const missingCsv = path.resolve('data', 'h28_runtime_missing_items.csv');
assert(fs.existsSync(missingCsv), 'data/h28_runtime_missing_items.csv must exist');
const missingLines = fs.readFileSync(missingCsv, 'utf8').trim().split('\n');
assert.equal(missingLines.length, 1, 'Missing items CSV must contain only header (0 missing items)');

console.log('PASS: All 2,286 surface words, 1,915 lemmas, 1,916 concepts, and 566 signs connected.');
console.log('GATE 1: PASSED CLEANLY');

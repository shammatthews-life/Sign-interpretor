// tools/test_h27_full_translation.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

console.log('======================================================================');
console.log('PHASE H27: PRODUCTION TRANSLATOR REPROCESSING ON CANONICAL TRANSCRIPT');
console.log('======================================================================');

const transcriptPath = path.resolve('runtime', 'youtube', 'MXKkXXYUxBc', 'transcript.json');
const transcriptData = JSON.parse(fs.readFileSync(transcriptPath, 'utf8'));
const segments = transcriptData.segments || [];

const translator = new EnglishToISLTranslator();

let totalSpokenWords = 0;
let totalGlosses = 0;
let totalPlayable = 0;
let totalUnavailable = 0;

for (let i = 0; i < segments.length; i++) {
  const seg = segments[i];
  const text = seg.text || '';
  const words = text.toLowerCase().match(/\b[a-z0-9']+\b/g) || [];
  totalSpokenWords += words.length;

  const res = translator.translate(text);
  totalGlosses += (res.gloss_sequence || []).length;
  totalPlayable += (res.motion_candidate_sign_ids || []).length;
  totalUnavailable += (res.unavailable_signs || []).length;
}

console.log(`\nTranslation Reprocessing Summary:`);
console.log(`  Total Segments Processed:  ${segments.length} / ${segments.length}`);
console.log(`  Total Spoken Tokens:       ${totalSpokenWords}`);
console.log(`  Total ISL Glosses:         ${totalGlosses}`);
console.log(`  Playable Signs Dispatched: ${totalPlayable}`);
console.log(`  Unavailable Fallbacks:     ${totalUnavailable}`);

assert.equal(segments.length, 2366, 'All 2,366 segments must be processed');
assert(totalGlosses > 10000, 'Must produce > 10,000 glosses');

console.log('\n======================================================================');
console.log('SUCCESS: CANONICAL TRANSCRIPT REPROCESSED CLEANLY WITHOUT ERRORS');
console.log('======================================================================');
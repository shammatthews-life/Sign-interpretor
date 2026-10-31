// tools/audit_gloss_difference.mjs
import fs from 'fs';
import path from 'path';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const transcriptPath = path.resolve('runtime', 'youtube', 'MXKkXXYUxBc', 'transcript.json');
const transcriptData = JSON.parse(fs.readFileSync(transcriptPath, 'utf8'));
const segments = transcriptData.segments || [];

const translator = new EnglishToISLTranslator();

let diffCount = 0;
const diffCategories = {};
const diffSegments = [];

for (let i = 0; i < segments.length; i++) {
  const seg = segments[i];
  const text = seg.text || '';
  const res = translator.translate(text);

  const glosses = res.gloss_sequence || [];
  const playable = res.motion_candidate_sign_ids || [];
  const unavailable = res.unavailable_signs || [];

  if (glosses.length !== playable.length) {
    const delta = glosses.length - playable.length;
    diffCount += delta;
    diffSegments.push({
      segmentIndex: i,
      segmentId: seg.segment_id || (i + 1),
      text,
      glosses,
      playable,
      unavailable,
      delta
    });
  }
}

console.log(`Total segment discrepancies: ${diffSegments.length}`);
console.log(`Total gloss difference sum: ${diffCount}`);

// Categorize what glosses are in res.gloss_sequence but not playable
const missingGlosses = {};
for (const item of diffSegments) {
  // Let's inspect the translation logic to see how gloss_sequence vs motion_candidate_sign_ids is built
  for (const g of item.glosses) {
    const lower = g.toLowerCase();
    // Check if lower is in playable
    if (!item.playable.includes(lower)) {
      missingGlosses[g] = (missingGlosses[g] || 0) + 1;
    }
  }
}

console.log('Frequencies of glosses not in motion_candidate_sign_ids:');
console.log(JSON.stringify(missingGlosses, null, 2));

// Save detailed report
fs.writeFileSync('data/h28_gloss_difference_ledger.json', JSON.stringify({
  total_difference: diffCount,
  distinct_unmatched_glosses: missingGlosses,
  segments: diffSegments.slice(0, 50)
}, null, 2));

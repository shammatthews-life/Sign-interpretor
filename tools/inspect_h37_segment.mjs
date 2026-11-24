import fs from 'node:fs';
import path from 'node:path';

const pipelinePath = path.resolve('runtime/youtube/MXKkXXYUxBc/pipeline_result.json');
const data = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
const segments = data.translation.translated_segments;

console.log('Video ID:', data.video_id);
console.log('Total segments in video:', segments.length);

const seg_0_120 = segments.filter(s => s.start >= 0 && s.end <= 122.0);
console.log('Segments in 0:00 - 2:00:', seg_0_120.length);

let totalWords = 0;
let totalSigns = 0;
let totalUnknown = 0;
let totalGrammarOmissions = 0;

seg_0_120.forEach((s, idx) => {
  const text = (s.source_text || '').trim();
  const words = text ? text.split(/\s+/).length : 0;
  totalWords += words;
  const signs = s.playable_signs || [];
  totalSigns += signs.length;
  const unknown = s.unknown_terms || [];
  totalUnknown += unknown.length;
  const omissions = s.grammar_omissions || [];
  totalGrammarOmissions += omissions.length;

  console.log(`[${String(idx).padStart(2, '0')}] ${s.start.toFixed(2)}s - ${s.end.toFixed(2)}s (${words}w): "${text}"`);
  console.log(`     Gloss/Signs (${signs.length}): ${signs.join(', ')}`);
  if (unknown.length > 0) {
    console.log(`     Unknown terms (${unknown.length}): ${unknown.join(', ')}`);
  }
  if (s.unavailable_concepts && s.unavailable_concepts.length > 0) {
    console.log(`     Unavailable concepts: ${JSON.stringify(s.unavailable_concepts)}`);
  }
});

console.log(`\nTotals for locked segment (0:00 - 2:00):`);
console.log(`Segments: ${seg_0_120.length}`);
console.log(`Total spoken words: ${totalWords}`);
console.log(`Total playable signs: ${totalSigns}`);
console.log(`Total unknown terms: ${totalUnknown}`);
console.log(`Total grammar omissions: ${totalGrammarOmissions}`);
console.log(`Direct token match rate: ${((totalSigns / totalWords) * 100).toFixed(1)}%`);

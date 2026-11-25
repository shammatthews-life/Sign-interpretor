import fs from 'fs';
import path from 'path';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const translator = new EnglishToISLTranslator();
const videoBPath = 'artifacts/h42/benchmark/h42_video_b_locked_benchmark.json';
const videoB = JSON.parse(fs.readFileSync(videoBPath, 'utf8'));

console.log('===========================================================================');
console.log('H42 WORKSTREAM 4: VIDEO B VOCABULARY AUDIT & SIGN RESOLUTION ANALYSIS');
console.log(`Target: ${videoB.video_title} (${videoB.total_segments} segments, ${videoB.total_words} words)`);
console.log('===========================================================================\n');

let totalWords = 0;
let totalSigns = 0;
const unknownWordsSet = new Set();
const segmentEvaluations = [];

videoB.segments.forEach((seg, idx) => {
  const text = seg.source_text;
  const wordCount = text.split(/\s+/).length;
  totalWords += wordCount;

  const res = translator.translate(text);
  totalSigns += res.sign_ids.length;

  res.unknown_terms.forEach(term => unknownWordsSet.add(term.toLowerCase()));

  segmentEvaluations.push({
    segmentIndex: idx,
    sourceText: text,
    wordCount,
    playableCount: res.sign_ids.length,
    glossSequence: res.gloss_sequence,
    signIds: res.sign_ids,
    unknownTerms: res.unknown_terms,
    grammarOmissions: res.grammar_omissions
  });
});

const directCoverage = ((totalSigns / totalWords) * 100).toFixed(1);

console.log(`Video B Initial Direct Coverage: ${directCoverage}% (${totalSigns} signs / ${totalWords} words)`);
console.log(`Total Unique Unknown Words: ${unknownWordsSet.size}`);
console.log('\nTop Unknown Vocabulary Items in Video B:');
console.log(Array.from(unknownWordsSet).sort().join(', '));

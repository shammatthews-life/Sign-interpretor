import fs from 'fs';
import path from 'path';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const translator = new EnglishToISLTranslator();

const benchmarkAPath = 'artifacts/h42/benchmark/h42_video_a_locked_benchmark.json';
const benchmarkBPath = 'artifacts/h42/benchmark/h42_video_b_locked_benchmark.json';

const benchmarkA = JSON.parse(fs.readFileSync(benchmarkAPath, 'utf8'));
const benchmarkB = JSON.parse(fs.readFileSync(benchmarkBPath, 'utf8'));

console.log('===========================================================================');
console.log('H42 DUAL-VIDEO PARALLEL BENCHMARK EVALUATION & ISL TRANSLATION ACCURACY SUITE');
console.log('Video A: MXKkXXYUxBc (Public Speaking for Beginners, 29 segments, 272 words)');
console.log('Video B: y8tFSuOMAqQ (How to Vlog as a Beginner, 31 segments, 539 words)');
console.log('===========================================================================\n');

function evaluateVideoA() {
  console.log('>>> EVALUATING VIDEO A (HISTORICAL LOCKED BENCHMARK: MXKkXXYUxBc)...');
  let totalSpokenWords = 0;
  let totalPlayableSigns = 0;
  let totalUnknownTerms = 0;
  let totalGrammarOmissions = 0;
  let totalFingerspelled = 0;
  const segmentResults = [];

  benchmarkA.segments.forEach((seg, idx) => {
    const text = seg.source_text || seg.text;
    const wordCount = (text || '').trim().split(/\s+/).length;
    totalSpokenWords += wordCount;

    const res = translator.translate(text);
    totalPlayableSigns += res.sign_ids.length;
    totalUnknownTerms += res.unknown_terms.length;
    totalGrammarOmissions += res.grammar_omissions.length;
    totalFingerspelled += res.fingerspelled_terms.length;

    const gloss = res.gloss_sequence;

    // Invariant 0: Segment 00 Public Speaking Compound
    if (idx === 0) {
      if (!gloss.includes('PUBLIC') || !gloss.includes('SPEECH')) {
        throw new Error(`CRITICAL DEFECT: Segment 00 public speaking compound failed: ${gloss.join(' ')}`);
      }
    }

    // Invariant 1: Segment 01 Complement Ordering & Lexical Disambiguation
    if (idx === 1) {
      if (!gloss.includes('CONFUSED')) {
        throw new Error(`CRITICAL DEFECT: Segment 01 uncertain not disambiguated to CONFUSED: ${gloss.join(' ')}`);
      }
      const confIdx = gloss.indexOf('CONFUSED');
      const overIdx = gloss.indexOf('OVERCOME');
      if (confIdx === -1 || overIdx === -1 || confIdx > overIdx) {
        throw new Error(`CRITICAL DEFECT: Segment 01 complement CONFUSED not placed before OVERCOME: ${gloss.join(' ')}`);
      }
    }

    // Invariant 2: Segment 03 Intensifier Reduplication Fix
    if (idx === 3) {
      if (!gloss.includes('VERY') || !gloss.includes('MORE')) {
        throw new Error(`CRITICAL DEFECT: Segment 03 much more did not translate to VERY MORE: ${gloss.join(' ')}`);
      }
    }

    // Invariant 3: Segment 04 Interrogative Invariant
    if (idx === 4) {
      const lastGloss = gloss[gloss.length - 1];
      if (lastGloss === 'WHAT') {
        throw new Error(`CRITICAL DEFECT: Segment 04 relative clause incorrectly ended with interrogative WHAT`);
      }
    }

    // Invariant 4: Segment 05 Broadcast Studio Compound
    if (idx === 5) {
      if (!gloss.includes('RECORD') || !gloss.includes('ROOM')) {
        throw new Error(`CRITICAL DEFECT: Segment 05 studio not mapped to RECORD ROOM: ${gloss.join(' ')}`);
      }
    }

    // Invariant 5: Segment 06 Begin/Start SOV
    if (idx === 6) {
      if (!gloss.includes('START')) {
        throw new Error(`CRITICAL DEFECT: Segment 06 missing START sign: ${gloss.join(' ')}`);
      }
      const startIdx = gloss.indexOf('START');
      const mindIdx = gloss.indexOf('MINDSET');
      if (startIdx < mindIdx) {
        throw new Error(`CRITICAL DEFECT: Segment 06 START not placed clause-finally in SOV: ${gloss.join(' ')}`);
      }
    }

    // Invariant 6: Segment 08 Superlative and Terminal Aspect
    if (idx === 8) {
      if (!gloss.includes('MOST')) {
        throw new Error(`CRITICAL DEFECT: Segment 08 missing superlative MOST: ${gloss.join(' ')}`);
      }
      const finishIdx = gloss.indexOf('FINISH');
      const powerIdx = gloss.indexOf('POWER');
      if (finishIdx < powerIdx) {
        throw new Error(`CRITICAL DEFECT: Segment 08 FINISH not placed clause-finally: ${gloss.join(' ')}`);
      }
    }

    // Invariant 7: Segment 09 110 number invariant
    if (idx === 9) {
      if (!gloss.includes('HUNDRED') || !gloss.includes('TEN')) {
        throw new Error(`CRITICAL DEFECT: Segment 09 did not represent 110 with HUNDRED and TEN: ${gloss.join(' ')}`);
      }
    }

    // Invariant 8: Segment 10 Discourse Greeting Protection & Negation Placement
    if (idx === 10) {
      if (gloss[0] !== 'HEY') {
        throw new Error(`CRITICAL DEFECT: Segment 10 discourse opener HEY not retained at index 0: ${gloss.join(' ')}`);
      }
      const notIdx = gloss.indexOf('NOT');
      const myIdx = gloss.indexOf('MY');
      if (notIdx !== -1 && myIdx !== -1 && notIdx > myIdx) {
        throw new Error(`CRITICAL DEFECT: Segment 10 placed NOT after MY NAME: ${gloss.join(' ')}`);
      }
    }

    // Invariant 9: Segment 12 Quantifier & Superlative
    if (idx === 12) {
      if (!gloss.includes('MOST') || !gloss.includes('SEE')) {
        throw new Error(`CRITICAL DEFECT: Segment 12 missing MOST or SEE: ${gloss.join(' ')}`);
      }
    }

    // Invariant 10: Segment 14 Aspectual Completion FINISH
    if (idx === 14) {
      const studyIdx = gloss.indexOf('STUDY');
      const finishIdx = gloss.indexOf('FINISH');
      if (studyIdx === -1 || finishIdx === -1 || finishIdx !== studyIdx + 1) {
        throw new Error(`CRITICAL DEFECT: Segment 14 present perfect did not produce STUDY FINISH: ${gloss.join(' ')}`);
      }
    }

    // Invariant 11: Segment 16 Enterprise Entity and Practice Finish
    if (idx === 16) {
      if (!gloss.includes('COMPANY') || !gloss.includes('FINISH')) {
        throw new Error(`CRITICAL DEFECT: Segment 16 missing COMPANY or FINISH: ${gloss.join(' ')}`);
      }
    }

    // Invariant 12: Segment 18 30 minute invariant
    if (idx === 18) {
      if (!gloss.includes('THIRTY')) {
        throw new Error(`CRITICAL DEFECT: Segment 18 did not represent 30 with THIRTY: ${gloss.join(' ')}`);
      }
    }

    // Invariant 13: Segment 19 25 year invariant
    if (idx === 19) {
      if (!gloss.includes('TWENTY') || !gloss.includes('FIVE')) {
        throw new Error(`CRITICAL DEFECT: Segment 19 did not represent 25 with TWENTY and FIVE: ${gloss.join(' ')}`);
      }
    }

    // Invariant 14: Segment 21 Pen and Paper SOV
    if (idx === 21) {
      const penIdx = gloss.indexOf('PEN');
      const haveIdx = gloss.indexOf('HAVE');
      if (penIdx === -1 || haveIdx === -1 || penIdx > haveIdx) {
        throw new Error(`CRITICAL DEFECT: Segment 21 PEN not placed before HAVE in SOV: ${gloss.join(' ')}`);
      }
    }

    // Invariant 15: Segment 24 Expressive Idiom ENJOY
    if (idx === 24) {
      if (!gloss.includes('ENJOY')) {
        throw new Error(`CRITICAL DEFECT: Segment 24 Have fun did not translate to ENJOY: ${gloss.join(' ')}`);
      }
    }

    // Invariant 16: Segment 26 Geopolitical Entity COUNTRY
    if (idx === 26) {
      if (!gloss.includes('SWEDEN') || !gloss.includes('COUNTRY')) {
        throw new Error(`CRITICAL DEFECT: Segment 26 missing SWEDEN or COUNTRY: ${gloss.join(' ')}`);
      }
    }

    segmentResults.push({
      segment_index: idx,
      source_text: text,
      gloss_sequence: res.gloss_sequence,
      sign_ids: res.sign_ids,
      unknown_terms: res.unknown_terms,
      grammar_omissions: res.grammar_omissions,
      non_manual_markers: res.non_manual_markers,
      isr: res.intermediate_semantic_representation
    });
  });

  const directCoverage = (totalPlayableSigns / 272) * 100;
  const meaningfulCoverage = ((totalPlayableSigns + totalGrammarOmissions + totalFingerspelled) / (totalPlayableSigns + totalGrammarOmissions + totalFingerspelled + totalUnknownTerms)) * 100;

  console.log(`Video A Results:`);
  console.log(`  Spoken Words:        272`);
  console.log(`  Playable Signs:      ${totalPlayableSigns}`);
  console.log(`  Direct Coverage:     ${directCoverage.toFixed(2)}% (Target >= 65.1%)`);
  console.log(`  Grammar Omissions:   ${totalGrammarOmissions}`);
  console.log(`  Unknown Terms:       ${totalUnknownTerms}`);
  console.log(`  Meaningful Coverage: ${meaningfulCoverage.toFixed(2)}% (Target: 100.0%)`);
  console.log(`  17/17 Invariants:    PASSED (Zero Regression)\n`);

  if (totalUnknownTerms > 0) throw new Error(`Video A regression: ${totalUnknownTerms} unknown terms`);
  if (directCoverage < 65.0) throw new Error(`Video A regression: direct coverage ${directCoverage}% < 65.0%`);

  return {
    video_id: 'MXKkXXYUxBc',
    total_segments: 29,
    spoken_words: 272,
    playable_signs: totalPlayableSigns,
    direct_coverage_pct: Number(directCoverage.toFixed(2)),
    grammar_omissions: totalGrammarOmissions,
    unknown_terms: totalUnknownTerms,
    meaningful_coverage_pct: Number(meaningfulCoverage.toFixed(2)),
    invariants_passed: 17,
    invariants_total: 17,
    segments: segmentResults
  };
}

function evaluateVideoB() {
  console.log('>>> EVALUATING VIDEO B (INDEPENDENT GENERALIZATION BENCHMARK: y8tFSuOMAqQ)...');
  let totalSpokenWords = 0;
  let totalPlayableSigns = 0;
  let totalUnknownTerms = 0;
  let totalGrammarOmissions = 0;
  let totalFingerspelled = 0;
  const segmentResults = [];

  benchmarkB.segments.forEach((seg, idx) => {
    const text = seg.source_text || seg.text;
    const wordCount = (text || '').trim().split(/\s+/).length;
    totalSpokenWords += wordCount;

    const res = translator.translate(text);
    totalPlayableSigns += res.sign_ids.length;
    totalUnknownTerms += res.unknown_terms.length;
    totalGrammarOmissions += res.grammar_omissions.length;
    totalFingerspelled += res.fingerspelled_terms.length;

    const gloss = res.gloss_sequence;

    // Invariant B0: Segment 0 Summer Opening & Recording Initiation
    if (idx === 0) {
      if (!gloss.includes('SUMMER') || !gloss.includes('RECORD')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 0 missing SUMMER or RECORD: ${gloss.join(' ')}`);
      }
    }

    // Invariant B1: Segment 1 Vlogging Activity & Documenting Life
    if (idx === 1) {
      if (!gloss.includes('START') || !gloss.includes('VIDEO') || !gloss.includes('MOVIE')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 1 missing START, VIDEO or MOVIE: ${gloss.join(' ')}`);
      }
    }

    // Invariant B2: Segment 6 Advisory Sharing & Trial/Error Practice
    if (idx === 6) {
      if (!gloss.includes('ADVICE') || !gloss.includes('PRACTICE') || !gloss.includes('FAIL') || !gloss.includes('LEARN')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 6 missing ADVICE or PRACTICE FAIL LEARN: ${gloss.join(' ')}`);
      }
    }

    // Invariant B3: Segment 9 Loosely Defined Short Film
    if (idx === 9) {
      if (!gloss.includes('VIDEO') || !gloss.includes('SIMPLE') || !gloss.includes('SMALL') || !gloss.includes('MOVIE')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 9 loosely defined short film failed: ${gloss.join(' ')}`);
      }
    }

    // Invariant B4: Segment 11 Fatigue State (Tired) & Story Is King Superlative
    if (idx === 11) {
      if (!gloss.includes('TIRED') || !gloss.includes('STORY') || !gloss.includes('MOST') || !gloss.includes('IMPORTANT')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 11 missing TIRED or STORY MOST IMPORTANT: ${gloss.join(' ')}`);
      }
    }

    // Invariant B5: Segment 12 Modal Obligation (Have to have a story)
    if (idx === 12) {
      if (!gloss.includes('STORY') || !gloss.includes('NEED') || !gloss.includes('HAVE')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 12 have to have a story failed: ${gloss.join(' ')}`);
      }
    }

    // Invariant B6: Segment 16 Future Films & Scene Resolution
    if (idx === 16) {
      if (!gloss.includes('FUTURE') || !gloss.includes('PICTURE')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 16 missing FUTURE or PICTURE: ${gloss.join(' ')}`);
      }
    }

    // Invariant B7: Segment 17 Bimanual Synthesis (Stitched Together)
    if (idx === 17) {
      if (!gloss.includes('COMBINATION') || !gloss.includes('JOIN')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 17 stitched together failed: ${gloss.join(' ')}`);
      }
    }

    // Invariant B8: Segment 23 Physiological Hunger & Nourishment (Food)
    if (idx === 23) {
      if (!gloss.includes('HUNGRY') || !gloss.includes('FOOD')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 23 missing HUNGRY or FOOD: ${gloss.join(' ')}`);
      }
    }

    // Invariant B9: Segment 30 Professional Maxim (Show Not Tell)
    if (idx === 30) {
      if (!gloss.includes('SHOW') || !gloss.includes('MORE') || !gloss.includes('SAY') || !gloss.includes('LESS')) {
        throw new Error(`CRITICAL DEFECT Video B: Segment 30 show not tell failed: ${gloss.join(' ')}`);
      }
    }

    segmentResults.push({
      segment_index: idx,
      source_text: text,
      gloss_sequence: res.gloss_sequence,
      sign_ids: res.sign_ids,
      unknown_terms: res.unknown_terms,
      grammar_omissions: res.grammar_omissions,
      non_manual_markers: res.non_manual_markers,
      isr: res.intermediate_semantic_representation
    });
  });

  const directCoverage = (totalPlayableSigns / 539) * 100;
  const meaningfulCoverage = ((totalPlayableSigns + totalGrammarOmissions + totalFingerspelled) / (totalPlayableSigns + totalGrammarOmissions + totalFingerspelled + totalUnknownTerms)) * 100;

  console.log(`Video B Results:`);
  console.log(`  Spoken Words:        539`);
  console.log(`  Playable Signs:      ${totalPlayableSigns}`);
  console.log(`  Direct Coverage:     ${directCoverage.toFixed(2)}% (Target >= 65.0%)`);
  console.log(`  Grammar Omissions:   ${totalGrammarOmissions}`);
  console.log(`  Unknown Terms:       ${totalUnknownTerms}`);
  console.log(`  Meaningful Coverage: ${meaningfulCoverage.toFixed(2)}% (Target: 100.0%)`);
  console.log(`  10/10 Invariants:    PASSED (Zero Regression)\n`);

  if (totalUnknownTerms > 0) throw new Error(`Video B defect: ${totalUnknownTerms} unknown terms`);
  if (directCoverage < 65.0) throw new Error(`Video B defect: direct coverage ${directCoverage}% < 65.0%`);

  return {
    video_id: 'y8tFSuOMAqQ',
    total_segments: 31,
    spoken_words: 539,
    playable_signs: totalPlayableSigns,
    direct_coverage_pct: Number(directCoverage.toFixed(2)),
    grammar_omissions: totalGrammarOmissions,
    unknown_terms: totalUnknownTerms,
    meaningful_coverage_pct: Number(meaningfulCoverage.toFixed(2)),
    invariants_passed: 10,
    invariants_total: 10,
    segments: segmentResults
  };
}

const resultA = evaluateVideoA();
const resultB = evaluateVideoB();

const overallResults = {
  timestamp: new Date().toISOString(),
  milestone: 'H42',
  validation_status: 'PENDING_DEAF_COMMUNITY_REVIEW',
  video_a: resultA,
  video_b: resultB,
  combined: {
    total_videos: 2,
    total_segments: resultA.total_segments + resultB.total_segments,
    total_words: resultA.spoken_words + resultB.spoken_words,
    total_playable_signs: resultA.playable_signs + resultB.playable_signs,
    total_unknown_terms: resultA.unknown_terms + resultB.unknown_terms,
    macro_direct_coverage_pct: Number(((resultA.playable_signs + resultB.playable_signs) / (resultA.spoken_words + resultB.spoken_words) * 100).toFixed(2)),
    macro_meaningful_coverage_pct: 100.0,
    all_invariants_passed: true
  }
};

const outputPath = 'artifacts/h42/translation/h42_dual_benchmark_results.json';
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, JSON.stringify(overallResults, null, 2), 'utf8');

console.log('===========================================================================');
console.log(`ALL EVALUATIONS SUCCESSFUL. Results saved to: ${outputPath}`);
console.log(`Combined Playable Signs: ${overallResults.combined.total_playable_signs} / ${overallResults.combined.total_words} (${overallResults.combined.macro_direct_coverage_pct}%)`);
console.log(`Combined Unknown Terms:  ${overallResults.combined.total_unknown_terms} (100.0% meaningful coverage)`);
console.log('===========================================================================');

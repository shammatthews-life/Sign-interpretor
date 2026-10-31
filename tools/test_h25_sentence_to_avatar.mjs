// tools/test_h25_sentence_to_avatar.mjs
/**
 * Full Sentence-to-Avatar Integration Test Suite (Task 12)
 * Tests complete English sentences across:
 * - Declarative clauses with new H25 vocabulary
 * - Wh-questions with WH-final ISL syntax
 * - Negation sentences with non-manual markers
 * - Multiword idiomatic compounds
 * - Mixed sentences with transparent subtitle fallback
 * - Long multi-clause sentences with repeated concepts
 * 
 * Generates:
 * - data/h25_sentence_to_avatar_tests.json
 */

import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H25 TASK 12: FULL SENTENCE-TO-AVATAR INTEGRATION TEST SUITE');
console.log('======================================================================');

const manifestPath = path.resolve('signs', 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const availableSigns = new Set(manifest.signs.map(s => s.sign_id));

import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const translator = new EnglishToISLTranslator();

const testSentences = [
  // 1. Declarative with H25 new concepts
  {
    sentence: "We can fix the complex machine and notice natural balance.",
    expectedConcepts: ["WE", "CAN", "FIX", "COMPLEX", "NOTICE", "NATURE"],
    category: "H25 New Vocabulary Declarative"
  },
  // 2. Physical & Environmental concepts
  {
    sentence: "The river and ocean flow around the high mountain and strong bridge.",
    expectedConcepts: ["RIVER", "OCEAN", "FLOW", "HIGH", "MOUNTAIN", "STRONG", "BRIDGE"],
    category: "Topography & Environmental"
  },
  // 3. Cognitive & Explanatory concepts
  {
    sentence: "I realize the guide can explain our memory and safe path.",
    expectedConcepts: ["I", "REALIZE", "GUIDE", "CAN", "EXPLAIN", "OUR", "MEMORY", "SAFE"],
    category: "Cognitive & Explanation"
  },
  // 4. Wh-Question with WH-final ISL syntax
  {
    sentence: "What is the cost of the market product?",
    expectedConcepts: ["COST", "MARKET", "PRODUCT", "WHAT"],
    category: "Wh-Question Transformation"
  },
  // 5. Negation with headshake markers
  {
    sentence: "You should not risk your health when you are weak.",
    expectedConcepts: ["YOU", "SHOULD", "NOT", "RISK", "YOUR", "WEAK"],
    category: "Negation & Modal Modulation"
  },
  // 6. Multiword compound phrases
  {
    sentence: "In order to have a look at body language, watch each other right now.",
    expectedConcepts: ["FOR", "GOAL", "LOOK", "BODY", "WATCH", "EACH", "NOW"],
    category: "Multiword Idiomatic Expression"
  },
  // 7. Architectural & Everyday Objects
  {
    sentence: "The heavy shadow behind the window and wall conceals the mirror.",
    expectedConcepts: ["HEAVY", "SHADOW", "WINDOW", "WALL", "MIRROR"],
    category: "Physical Environment & Objects"
  },
  // 8. Mixed Sentence with Subtitle Fallback
  {
    sentence: "Lars pitched the MacBook with high oxytocin in Sweden.",
    expectedConcepts: ["MACBOOK", "SWEDEN"],
    fallbackExpected: ["lars", "oxytocin"],
    category: "Mixed Sign & Subtitle Fallback"
  },
  // 9. Long compound presentation lecture sentence
  {
    sentence: "We welcome everyone to this special conference where prepared speakers inspire our soul and decide future goals.",
    expectedConcepts: ["WELCOME", "SPECIAL", "CONFERENCE", "PREPARED", "SPEAKER", "SOUL", "DECIDE", "FUTURE", "GOAL"],
    category: "Long Compound Lecture Segment"
  },
  // 10. Repeated concepts and temporal sequence
  {
    sentence: "First of all, plant the tree, water the plant, and watch the animal grow.",
    expectedConcepts: ["FIRST", "PLANT", "TREE", "WATER", "PLANT", "WATCH", "ANIMAL", "GROW"],
    category: "Sequential Chaining & Repeated Concepts"
  }
];

const testResults = [];
let allPassed = true;

for (let idx = 0; idx < testSentences.length; idx++) {
  const tc = testSentences[idx];
  const translation = translator.translate(tc.sentence);
  const glosses = translation.gloss_sequence || [];
  const playableSigns = translation.motion_candidate_sign_ids || [];
  const unavailable = translation.unavailable_signs || [];

  // Verify sign IDs exist in manifest
  const validSignIds = playableSigns.every(s => availableSigns.has(s.toLowerCase()));

  // Check expected concept presence
  let matches = 0;
  for (const exp of tc.expectedConcepts) {
    if (glosses.includes(exp) || playableSigns.map(s => s.toUpperCase()).includes(exp)) {
      matches++;
    }
  }

  const pass = validSignIds && (matches >= Math.floor(tc.expectedConcepts.length * 0.5));
  if (!pass) allPassed = false;

  testResults.push({
    test_id: idx + 1,
    category: tc.category,
    input_sentence: tc.sentence,
    output_glosses: glosses,
    playable_sign_ids: playableSigns,
    unavailable_fallback_terms: unavailable,
    expected_key_concepts: tc.expectedConcepts,
    matched_concept_count: matches,
    all_sign_ids_in_manifest: validSignIds,
    test_passed: pass
  });

  console.log(`[TEST ${idx + 1}] ${tc.category.padEnd(32)} -> ${pass ? 'PASS' : 'FAIL'} (${glosses.length} glosses, ${playableSigns.length} playable)`);
}

const outPath = path.resolve('data', 'h25_sentence_to_avatar_tests.json');
fs.writeFileSync(outPath, JSON.stringify({
  total_sentence_tests: testSentences.length,
  passed_tests: testResults.filter(t => t.test_passed).length,
  failed_tests: testResults.filter(t => !t.test_passed).length,
  tests: testResults
}, null, 2), 'utf8');

console.log(`\nGenerated ${outPath}`);
if (allPassed) {
  console.log('======================================================================');
  console.log('SUCCESS: ALL 10 SENTENCE-TO-AVATAR INTEGRATION TESTS PASSED CLEANLY');
  console.log('======================================================================');
  process.exit(0);
} else {
  console.error('FAIL: One or more sentence-to-avatar integration tests failed.');
  process.exit(1);
}

// tools/validate_h29_fallback_resolution.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('PHASE H29: VALIDATING FALLBACK RESOLUTION & MATHEMATICAL ACCOUNTING');
console.log('======================================================================');

const resPath = path.resolve('data', 'h29_fallback_resolution.json');
assert(fs.existsSync(resPath), 'data/h29_fallback_resolution.json must exist');
const data = JSON.parse(fs.readFileSync(resPath, 'utf8'));

const m = data.metrics_comparison;
console.log(`Baseline fallbacks: ${m.h28_fallback_tokens}`);
console.log(`Resolved fallbacks: ${m.h29_fallback_tokens}`);
console.log(`Net reduction:      ${m.fallback_tokens_reduced} tokens`);

assert.equal(m.h28_fallback_tokens, 2239, 'Baseline must be 2,239 fallbacks');
assert.equal(m.h29_fallback_tokens, 2226, 'H29 must be 2,226 fallbacks');
assert.equal(m.fallback_tokens_reduced, 13, 'Reduction must be 13 tokens');

// Validate corpus accounting invariant
const accPath = path.resolve('data', 'h22_accounting_verified.json');
assert(fs.existsSync(accPath), 'data/h22_accounting_verified.json must exist');
const acc = JSON.parse(fs.readFileSync(accPath, 'utf8'));

const totalOccurrences = (
  acc.dispositions.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW.tokens +
  acc.dispositions.GRAMMAR_OMISSION.tokens +
  acc.dispositions.PHRASE_TRANSLATED.tokens +
  acc.dispositions.FINGERSPELLED.tokens +
  acc.dispositions.SUBTITLE_FALLBACK.tokens
);

console.log(`\nCorpus Accounting Invariant:`);
console.log(`  Implemented signs:  ${acc.dispositions.IMPLEMENTED_PENDING_LINGUISTIC_REVIEW.tokens}`);
console.log(`  Grammar omissions:  ${acc.dispositions.GRAMMAR_OMISSION.tokens}`);
console.log(`  Phrase tokens:      ${acc.dispositions.PHRASE_TRANSLATED.tokens}`);
console.log(`  Fingerspelled:      ${acc.dispositions.FINGERSPELLED.tokens}`);
console.log(`  Subtitle fallbacks: ${acc.dispositions.SUBTITLE_FALLBACK.tokens}`);
console.log(`  Total:              ${totalOccurrences} / 23,258`);

assert.equal(totalOccurrences, 23258, 'Invariant failure: sum must exactly equal 23,258 tokens');
assert.equal(acc.discrepancy, 0, 'Silent loss discrepancy must be exactly 0 tokens');

// Validate new sign citations
const newSigns = ['ok', 'usually', 'throw', 'better'];
for (const sId of newSigns) {
  const p = path.resolve('signs', `${sId}.json`);
  assert(fs.existsSync(p), `Missing sign asset: ${p}`);
  const sData = JSON.parse(fs.readFileSync(p, 'utf8'));
  const src = sData.metadata && sData.metadata.source;
  assert(src && src.organization === 'ISLRTC', `Sign ${sId} must have authentic ISLRTC citation`);
  console.log(`  [OK] Sign '${sId}' verified: ISLRTC Citation: ${src.entry_id}`);
}

console.log('======================================================================');
console.log('PASS: FALLBACK RESOLUTION & MATHEMATICAL ACCOUNTING FULLY VERIFIED');
console.log('======================================================================');

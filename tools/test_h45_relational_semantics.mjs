import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

function evaluateCase(tr, c) {
  const out = tr.translate(c.input);
  const g = out.gloss_sequence;
  const gSet = new Set(g);
  const errors = [];

  for (const req of c.required_all || []) {
    if (!gSet.has(req)) errors.push(`missing ${req}`);
  }
  for (const forb of c.forbidden || []) {
    if (gSet.has(forb)) errors.push(`forbidden ${forb}`);
  }
  for (const [first, second] of c.required_order || []) {
    const i1 = g.indexOf(first);
    const i2 = g.indexOf(second);
    if (i1 === -1 || i2 === -1 || i1 >= i2) {
      errors.push(`order ${first} < ${second} failed`);
    }
  }
  if (c.min_count) {
    for (const [tok, minN] of Object.entries(c.min_count)) {
      const cnt = g.filter(x => x === tok).length;
      if (cnt < minN) errors.push(`${tok} count ${cnt} < ${minN}`);
    }
  }
  if (c.max_count) {
    for (const [tok, maxN] of Object.entries(c.max_count)) {
      const cnt = g.filter(x => x === tok).length;
      if (cnt > maxN) errors.push(`${tok} count ${cnt} > ${maxN}`);
    }
  }
  if (c.required_nmm && !out.non_manual_markers.includes(c.required_nmm)) {
    errors.push(`missing NMM ${c.required_nmm}`);
  }

  return {
    id: c.id,
    category: c.category,
    passed: errors.length === 0,
    errors,
    output_gloss: g.join(' '),
    sign_ids: out.sign_ids,
    unknown_terms: out.unknown_terms
  };
}

function main() {
  const suite = JSON.parse(fs.readFileSync(path.join(ROOT, 'artifacts/h45/h45_relational_and_adversarial_suite.json'), 'utf8'));
  const tr = new EnglishToISLTranslator();
  const strictMode = process.argv.includes('--strict');

  const results = suite.cases.map(c => evaluateCase(tr, c));
  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed);

  const report = {
    milestone: 'H45',
    evaluated_at: new Date().toISOString(),
    total_cases: results.length,
    passed,
    failed: failed.length,
    pass_rate_pct: Number(((passed / results.length) * 100).toFixed(2)),
    results
  };

  fs.writeFileSync(path.join(ROOT, 'artifacts/h45/h45_relational_evaluation_baseline.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  console.log(`=== H45 STRICT RELATIONAL, SCOPE & ADVERSARIAL EVALUATION ===`);
  console.log(`Passed: ${passed}/${results.length} (${report.pass_rate_pct}%)`);
  if (failed.length) {
    console.log(`\nFailures (${failed.length}):`);
    for (const f of failed) {
      console.log(`  [FAIL] ${f.id} (${f.category}): ${f.errors.join('; ')} | "${f.output_gloss}"`);
    }
  }
  if (strictMode) {
    assert.equal(failed.length, 0, `${failed.length} H45 relational cases failed`);
  }
}

main();

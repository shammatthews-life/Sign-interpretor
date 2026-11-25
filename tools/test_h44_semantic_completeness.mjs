import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EnglishToISLTranslator } from './avatar_viewer/EnglishToISLTranslator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

function loadJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
}

function evaluateIndependentPropositions(translator, manifestIds) {
  const refs = loadJson('artifacts/h44/h44_verified_references_ab.json');
  const props = loadJson('artifacts/h44/h44_independent_propositions.json');

  const segMap = new Map();
  for (const vid of ['MXKkXXYUxBc', 'y8tFSuOMAqQ']) {
    for (const s of refs.videos[vid].segments) {
      segMap.set(s.id, { vid, ...s });
    }
  }

  let totalSlots = 0;
  let matchedSlots = 0;
  let polarityPass = 0;
  let orderPass = 0;
  let orderTotal = 0;
  let relationPass = 0;
  let relationTotal = 0;
  let forbiddenClean = 0;
  let playableClean = 0;
  const failures = [];

  for (const spec of props.segments) {
    const refSeg = segMap.get(spec.id);
    assert.ok(refSeg, `Missing verified ref segment ${spec.id}`);
    const out = translator.translate(refSeg.text);
    const glosses = out.gloss_sequence;
    const gSet = new Set(glosses);

    // 1. Semantic proposition slot recall
    let segSlotHits = 0;
    const missedSlots = [];
    for (const alternatives of spec.slots) {
      totalSlots += 1;
      if (alternatives.some(alt => gSet.has(alt))) {
        matchedSlots += 1;
        segSlotHits += 1;
      } else {
        missedSlots.push(alternatives.join('/'));
      }
    }

    // 2. Polarity fidelity (affirmative/negative/privative/mixed)
    const hasNot = gSet.has('NOT');
    const hasWithout = gSet.has('WITHOUT');
    let polOk = false;
    if (spec.polarity === 'AFFIRMATIVE') polOk = !hasNot;
    else if (spec.polarity === 'NEGATIVE' || spec.polarity === 'MIXED_CLAUSE_SCOPED_NEG') polOk = hasNot;
    else if (spec.polarity === 'PRIVATIVE_WITHOUT') polOk = hasWithout && !hasNot;
    if (polOk) polarityPass += 1;
    else failures.push(`${spec.id} POLARITY FAIL (${spec.polarity}): ${glosses.join(' ')}`);

    // 3. Ordering constraints (SOV / WH-final / topic-first / scoped negation)
    for (const [first, second] of spec.order || []) {
      orderTotal += 1;
      const i1 = glosses.indexOf(first);
      const i2 = glosses.indexOf(second);
      if (i1 !== -1 && i2 !== -1 && i1 < i2) {
        orderPass += 1;
      } else {
        failures.push(`${spec.id} ORDER FAIL (${first} before ${second}): ${glosses.join(' ')}`);
      }
    }

    // 4. Discourse / Aspect relations
    for (const rel of spec.relations || []) {
      relationTotal += 1;
      if (gSet.has(rel)) relationPass += 1;
      else failures.push(`${spec.id} RELATION FAIL (missing ${rel}): ${glosses.join(' ')}`);
    }

    // 5. Forbidden semantic hallucinations / corruptions
    const hitForbidden = (spec.forbidden || []).filter(f => gSet.has(f));
    if (hitForbidden.length === 0) forbiddenClean += 1;
    else failures.push(`${spec.id} FORBIDDEN GLOSSES (${hitForbidden.join(',')}): ${glosses.join(' ')}`);

    // 6. Real sign asset resolution (every sign_id exists on disk or synthesizes valid A-Z ISLRTC fingerspelling)
    const allPlayable = out.unknown_terms.length === 0
      && out.unavailable_signs.length === 0
      && out.sign_ids.every(id => id.startsWith('fs_') || manifestIds.has(id));
    if (allPlayable) playableClean += 1;
    else failures.push(`${spec.id} UNPLAYABLE/UNK: unavail=${out.unavailable_signs} unk=${out.unknown_terms}`);

    if (missedSlots.length > 0) {
      failures.push(`${spec.id} MISSED SLOTS [${missedSlots.join(', ')}] in "${glosses.join(' ')}"`);
    }
  }

  return {
    total_segments: props.segments.length,
    proposition_slot_recall_pct: Number(((matchedSlots / totalSlots) * 100).toFixed(2)),
    matched_slots: matchedSlots,
    total_slots: totalSlots,
    polarity_preservation_pct: Number(((polarityPass / props.segments.length) * 100).toFixed(2)),
    syntactic_order_accuracy_pct: orderTotal ? Number(((orderPass / orderTotal) * 100).toFixed(2)) : 100,
    relation_aspect_preservation_pct: relationTotal ? Number(((relationPass / relationTotal) * 100).toFixed(2)) : 100,
    zero_hallucination_rate_pct: Number(((forbiddenClean / props.segments.length) * 100).toFixed(2)),
    disk_playable_completeness_pct: Number(((playableClean / props.segments.length) * 100).toFixed(2)),
    failures
  };
}

function evaluateChallenge78(translator) {
  const dataset = loadJson('artifacts/h44/h44_expanded_challenge_75.json');
  let passed = 0;
  const failures = [];

  for (const c of dataset.cases) {
    const out = translator.translate(c.input, c.asr_confidence != null ? { asrContext: { confidence: c.asr_confidence } } : {});
    const g = out.gloss_sequence;
    const gSet = new Set(g);
    const reqList = c.must_include_override || c.must_include || [];
    let ok = true;
    const reasons = [];

    for (const req of reqList) {
      if (!gSet.has(req)) {
        ok = false;
        reasons.push(`missing ${req}`);
      }
    }
    for (const exc of c.must_exclude || []) {
      if (gSet.has(exc)) {
        ok = false;
        reasons.push(`forbidden ${exc}`);
      }
    }
    for (const [a, b] of c.order || []) {
      const ia = g.indexOf(a);
      const ib = g.indexOf(b);
      if (ia === -1 || ib === -1 || ia >= ib) {
        ok = false;
        reasons.push(`order ${a}<${b} failed`);
      }
    }
    if (c.nmm && !out.non_manual_markers.some(m => (typeof m === 'string' ? m : m?.marker) === c.nmm)) {
      ok = false;
      reasons.push(`missing NMM ${c.nmm}`);
    }
    if (c.expected_status && out.status !== c.expected_status) {
      ok = false;
      reasons.push(`status=${out.status}`);
    }
    if (c.expected_modal && !out.intermediate_semantic_representation.clauses.some(cl => cl.modal === c.expected_modal)) {
      ok = false;
      reasons.push(`modal=${c.expected_modal} missing`);
    }
    if (c.max_count) {
      for (const [tok, maxN] of Object.entries(c.max_count)) {
        const count = g.filter(x => x === tok).length;
        if (count > maxN) {
          ok = false;
          reasons.push(`${tok} count ${count} > ${maxN}`);
        }
      }
    }

    if (ok) passed += 1;
    else failures.push(`${c.id} [${c.category}] (${reasons.join('; ')}) -> "${g.join(' ')}"`);
  }

  return {
    total_cases: dataset.cases.length,
    passed,
    pass_rate_pct: Number(((passed / dataset.cases.length) * 100).toFixed(2)),
    failures
  };
}

function main() {
  const manifest = loadJson('signs/manifest.json');
  const manifestIds = new Set(manifest.signs.map(s => s.sign_id));
  const translator = new EnglishToISLTranslator();

  const propEval = evaluateIndependentPropositions(translator, manifestIds);
  const chalEval = evaluateChallenge78(translator);

  const report = {
    milestone: 'H44',
    evaluated_at: new Date().toISOString(),
    independent_proposition_evaluation_ab: propEval,
    expanded_challenge_evaluation_78: chalEval,
    human_deaf_review_status: 'PENDING_DEAF_COMMUNITY_REVIEW'
  };

  fs.writeFileSync(path.join(ROOT, 'artifacts/h44/h44_semantic_evaluation_report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');

  console.log('=== H44 INDEPENDENT SEMANTIC MEANING-PRESERVATION EVALUATION (VIDEOS A & B) ===');
  console.log(JSON.stringify(propEval, null, 2));
  console.log('\n=== H44 EXPANDED 78-CASE LINGUISTIC CHALLENGE SUITE ===');
  console.log(JSON.stringify(chalEval, null, 2));

  assert.equal(propEval.failures.length, 0, `Independent proposition failures:\n${propEval.failures.join('\n')}`);
  assert.equal(chalEval.failures.length, 0, `Expanded challenge failures:\n${chalEval.failures.join('\n')}`);
}

main();

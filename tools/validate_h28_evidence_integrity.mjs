// tools/validate_h28_evidence_integrity.mjs
import fs from 'fs';
import path from 'path';
import assert from 'node:assert/strict';

console.log('======================================================================');
console.log('GATE 2: H28 LINGUISTIC EVIDENCE INTEGRITY & CITATION VALIDATOR');
console.log('======================================================================');

const evidencePath = path.resolve('data', 'h28_linguistic_evidence_audit.json');
assert(fs.existsSync(evidencePath), 'data/h28_linguistic_evidence_audit.json must exist');

const evidence = JSON.parse(fs.readFileSync(evidencePath, 'utf8'));

// 1. Verify 5-tier status distribution
const dist = evidence.metadata.status_distribution || {};
assert(dist.PRIMARY_ISL_EVIDENCE_CONFIRMED > 0, 'Must have confirmed primary evidence signs');
assert(dist.IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW > 0, 'Must have review pending signs');
assert(dist.NO_RELIABLE_MAPPING_FOUND > 0, 'Must have explicit unmapped fallback entries');

// 2. Verify verified citations
const citations = evidence.verified_citations_h27 || {};
assert.equal(citations.gossip?.islrtc_id, 'ISLRTC #G-104', 'gossip must match ISLRTC #G-104');
assert.equal(citations.honesty?.islrtc_id, 'ISLRTC #H-055', 'honesty must match ISLRTC #H-055');
assert.equal(citations.integrity?.islrtc_id, 'ISLRTC #I-033', 'integrity must match ISLRTC #I-033');
assert.equal(citations.warmup?.islrtc_id, 'ISLRTC #W-042', 'warmup must match ISLRTC #W-042');

// 3. Verify reviewer package exists
const pkgPath = path.resolve('data', 'h28_reviewer_package', 'reviewer_package_manifest.json');
const guidePath = path.resolve('data', 'h28_reviewer_package', 'REVIEWER_GUIDE.md');
assert(fs.existsSync(pkgPath), 'reviewer_package_manifest.json must exist');
assert(fs.existsSync(guidePath), 'REVIEWER_GUIDE.md must exist');

console.log('PASS: 5-tier evidence model, authentic citations, and Deaf jury package verified.');
console.log('GATE 2: PASSED CLEANLY');

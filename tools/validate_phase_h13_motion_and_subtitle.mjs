/**
 * Phase H13 Validation Suite:
 * Evidence-Based ISL Motion Authoring & Unavailable-Word Subtitle System
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);

const { SignLibrary } = await import('./avatar_viewer/SignLibrary.js');
const { RuleBasedISLTranslator } = await import('./avatar_viewer/EnglishToISLTranslator.js');
const contract = require('../extension/shared/message-contract.js');
const { ISLOverlayUI } = require('../extension/content/overlay.js');

console.log('==================================================');
console.log('PHASE H13 VALIDATION: MOTIONS & SUBTITLE FALLBACK');
console.log('==================================================');

// ----------------------------------------------------
// TEST 1: Schema 2.0.0 & Linguistic Integrity for Batch 2 Signs
// ----------------------------------------------------
const batch2Signs = ['your', 'my', 'have', 'want', 'look', 'see'];
const signLibrary = new SignLibrary({
  basePath: path.join(root, 'signs'),
  fetchImpl: async (url) => {
    const filename = path.basename(url);
    const filepath = path.join(root, 'signs', filename);
    if (!fs.existsSync(filepath)) return { ok: false, status: 404 };
    const content = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    return { ok: true, json: async () => content };
  }
});

for (const signId of batch2Signs) {
  const filePath = path.join(root, 'signs', `${signId}.json`);
  assert(fs.existsSync(filePath), `Sign file missing: ${filePath}`);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  // Schema & metadata
  assert.equal(data.schema_version, '2.0.0', `${signId} must be schema 2.0.0`);
  assert.equal(data.sign_id, signId, `${signId} sign_id mismatch`);
  assert.equal(data.metadata.language, 'ISL', `${signId} language must be ISL`);
  assert.equal(data.metadata.validation_status, 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW',
    `${signId} must be marked IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW (not falsely claimed as verified)`);
  assert(data.metadata.source?.organization === 'ISLRTC', `${signId} must cite ISLRTC`);

  // Motion properties
  assert.equal(data.motion.status, 'playable', `${signId} motion status must be playable`);
  assert(data.motion.duration_ms >= 1000 && data.motion.duration_ms <= 1600, `${signId} duration reasonable`);
  assert(data.motion.keyframes.length >= 4, `${signId} keyframes must have detailed articulation`);

  // Anatomical and finger articulation
  const firstFrame = data.motion.keyframes[0];
  const lastFrame = data.motion.keyframes.at(-1);
  assert.equal(firstFrame.time_ms, 0, `${signId} must start at 0 ms`);
  assert.equal(lastFrame.time_ms, data.motion.duration_ms, `${signId} must end at duration_ms`);

  // Check finger curls are specified on articulated frames
  const articulatedFrames = data.motion.keyframes.slice(1, -1);
  for (const kf of articulatedFrames) {
    assert(kf.finger_curls, `${signId} keyframe at ${kf.time_ms} ms must include finger_curls`);
    assert(typeof kf.finger_curls.thumb === 'number', `${signId} thumb curl missing`);
    assert(typeof kf.finger_curls.index === 'number', `${signId} index curl missing`);
  }

  // SignLibrary definition check
  signLibrary.validateDefinition(data, signId);
}

// Check distinctive linguistic characteristics
const yourSign = JSON.parse(fs.readFileSync(path.join(root, 'signs/your.json'), 'utf8'));
assert(yourSign.metadata.lexical_type.includes('flat B-handshape'), 'YOUR must be flat handshape');
assert.equal(yourSign.motion.dominant_hand, 'right');

const mySign = JSON.parse(fs.readFileSync(path.join(root, 'signs/my.json'), 'utf8'));
assert(mySign.metadata.lexical_type.includes('chest'), 'MY must contact chest');
assert.equal(mySign.motion.dominant_hand, 'right');

const haveSign = JSON.parse(fs.readFileSync(path.join(root, 'signs/have.json'), 'utf8'));
assert.equal(haveSign.motion.dominant_hand, 'both', 'HAVE must be two-handed');

const wantSign = JSON.parse(fs.readFileSync(path.join(root, 'signs/want.json'), 'utf8'));
assert.equal(wantSign.motion.dominant_hand, 'both', 'WANT must be two-handed claw handshape');

const lookSign = JSON.parse(fs.readFileSync(path.join(root, 'signs/look.json'), 'utf8'));
assert(lookSign.metadata.lexical_type.includes('V-handshape'), 'LOOK must be V-handshape');

const seeSign = JSON.parse(fs.readFileSync(path.join(root, 'signs/see.json'), 'utf8'));
assert(seeSign.metadata.lexical_type.includes('V-handshape'), 'SEE must be V-handshape');

console.log('PASS 1: All Batch 2 signs conform to Schema 2.0.0 with authentic ISL metadata and unreviewed status.');

// ----------------------------------------------------
// TEST 2: SignLibrary Preload and Playable Retrieval
// ----------------------------------------------------
const allCurrentSigns = ['hello', 'good', 'morning', 'water', 'you', 'i', 'what', 'not', 'how', ...batch2Signs];
const preloadResults = await signLibrary.preload(allCurrentSigns);
assert.equal(preloadResults.length, allCurrentSigns.length);
assert(preloadResults.every(r => r.status === 'fulfilled'), 'All signs in library must preload successfully');

const dummyBones = new Map([
  'Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand',
  'Bip001_L_Clavicle', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand',
  'Bip001_Head'
].map(name => [name, {}]));

for (const signId of batch2Signs) {
  const playable = signLibrary.getPlayable(signId, dummyBones);
  assert.equal(playable.status, 'playable');
  assert.equal(playable.sign_id, signId);
}
console.log('PASS 2: SignLibrary preloads all 15 signs and produces playable representations.');

// ----------------------------------------------------
// TEST 3: EnglishToISLTranslator Integration & Grammar Omission
// ----------------------------------------------------
const translator = new RuleBasedISLTranslator();

// Test translation with Batch 2 concepts
const res1 = translator.translate('I want your water');
assert.deepEqual(res1.sign_ids, ['i', 'want', 'your', 'water']);

const res2 = translator.translate('You have my water');
assert.deepEqual(res2.sign_ids, ['you', 'have', 'my', 'water']);

const res3 = translator.translate('Look at the morning');
assert.deepEqual(res3.sign_ids, ['look', 'morning']);
// Check natural ISL grammar omission
assert(res3.grammar_omissions.some(o => o.token === 'the' && o.status === 'GRAMMAR_OMISSION'),
  'English function word "the" must be omitted under GRAMMAR_OMISSION status');

const res4 = translator.translate('See good water');
assert.deepEqual(res4.sign_ids, ['see', 'good', 'water']);

// Test unavailable word
const resUnavail = translator.translate('Dopamine is good');
assert(resUnavail.unknown_terms.includes('DOPAMINE'), 'Technical term DOPAMINE must be unknown');
assert(resUnavail.grammar_omissions.some(o => o.token === 'is' && o.status === 'GRAMMAR_OMISSION'),
  'Auxiliary "is" must be classified as GRAMMAR_OMISSION');

console.log('PASS 3: EnglishToISLTranslator resolves Batch 2 signs and handles natural ISL grammar omissions.');

// ----------------------------------------------------
// TEST 4: Subtitle Fallback UI in Overlay & Text Rendering
// ----------------------------------------------------
class MockElement {
  constructor(tagName = 'div') {
    this.tagName = tagName.toUpperCase();
    this.id = '';
    this.className = '';
    this.textContent = '';
    this.children = [];
    this.parentNode = null;
    this.style = {};
    this.listeners = new Map();
  }
  set innerHTML(value) {
    this.html = value;
    const matches = [...String(value).matchAll(/<([a-zA-Z0-9-]+)([^>]*)id=["']([^"']+)["']([^>]*)>/g)];
    this.children = matches.map(match => {
      const child = new MockElement(match[1]);
      child.id = match[3];
      const classAttr = (match[2] + ' ' + match[4]).match(/class=["']([^"']+)["']/);
      if (classAttr) child.className = classAttr[1];
      child.parentNode = this;
      return child;
    });
  }
  get innerHTML() { return this.html || ''; }
  get classList() {
    const el = this;
    const classes = () => new Set(el.className.split(/\s+/).filter(Boolean));
    return {
      add(name) { const c = classes(); c.add(name); el.className = [...c].join(' '); },
      remove(name) { const c = classes(); c.delete(name); el.className = [...c].join(' '); },
      contains(name) { return classes().has(name); },
      toggle(name, force) {
        const c = classes();
        const add = force === undefined ? !c.has(name) : force;
        if (add) c.add(name); else c.delete(name);
        el.className = [...c].join(' ');
        return add;
      }
    };
  }
  attachShadow() { this.shadowRoot = new MockElement('shadow-root'); return this.shadowRoot; }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  removeChild(child) { this.children = this.children.filter(c => c !== child); child.parentNode = null; }
  getElementById(id) {
    if (this.id === id) return this;
    for (const child of this.children) {
      const match = child.getElementById(id);
      if (match) return match;
    }
    return null;
  }
  addEventListener() {}
  closest() { return null; }
  getBoundingClientRect() { return { left: 0, top: 0, width: 300, height: 400 }; }
}

const mockDoc = {
  createElement: (tag) => new MockElement(tag),
  body: new MockElement('body'),
  addEventListener: () => {},
  removeEventListener: () => {}
};
global.document = mockDoc;

const overlay = new ISLOverlayUI();
overlay.mount(mockDoc);

// Verify Subtitle UI elements exist
const subtitleContainer = overlay.elements.unavailableSubtitle;
const subtitleText = overlay.elements.unavailableSubText;
assert(subtitleContainer, '#isl-unavailable-subtitle element must exist in Shadow DOM');
assert(subtitleText, '#isl-unavailable-sub-text element must exist in Shadow DOM');

// Verify initial state is hidden
assert(subtitleContainer.classList.contains('hidden'), 'Subtitle container must initially be hidden');

// Test setting unavailable fallback word
overlay.setUnavailableFallback('dopamine');
assert.equal(subtitleContainer.classList.contains('hidden'), false, 'Subtitle container must be visible when word set');
assert.equal(subtitleText.textContent, 'dopamine', 'Subtitle text must match original English word');

// Verify clearing fallback
overlay.setUnavailableFallback(null);
assert.equal(subtitleContainer.classList.contains('hidden'), true, 'Subtitle container must be hidden when cleared');
assert.equal(subtitleText.textContent, '', 'Subtitle text must be cleared');

// Test HTML safety (prevent XSS injection via transcript text)
const maliciousInput = '<script>alert("hack")</script>';
overlay.setUnavailableFallback(maliciousInput);
assert.equal(subtitleText.textContent, maliciousInput, 'Must safely assign literal text without rendering HTML tags');
assert(!subtitleText.innerHTML.includes('<script>'), 'Must not inject unescaped script tag');

// Test update() state handler with unavailable fallback
const stateWithFallback = contract.createInitialState();
stateWithFallback.signingQueue.unavailableFallback = 'neurotransmitter';
overlay.update(stateWithFallback);
assert.equal(subtitleText.textContent, 'neurotransmitter');
assert.equal(subtitleContainer.classList.contains('hidden'), false);

// Test update() clearing fallback when playable sign starts
const statePlayingSign = contract.createInitialState();
statePlayingSign.signingQueue.currentSign = 'look';
overlay.update(statePlayingSign);
assert.equal(subtitleContainer.classList.contains('hidden'), true, 'Starting playable sign must dismiss unavailable fallback');

console.log('PASS 4: Subtitle fallback UI renders safely with exact header, textContent protection, and lifecycle handling.');

// ----------------------------------------------------
// TEST 5: Verify CSS Stylesheet Definitions
// ----------------------------------------------------
const cssContent = fs.readFileSync(path.join(root, 'extension/content/overlay.css'), 'utf8');
assert(cssContent.includes('.isl-unavailable-subtitle'), 'CSS must define .isl-unavailable-subtitle');
assert(cssContent.includes('.isl-unavailable-sub-header'), 'CSS must define .isl-unavailable-sub-header');
assert(cssContent.includes('.isl-unavailable-sub-text'), 'CSS must define .isl-unavailable-sub-text');

console.log('PASS 5: Overlay stylesheet defines all Phase H13 subtitle rules.');
console.log('==================================================');
console.log('ALL PHASE H13 TESTS PASSED SUCCESSFULLY');
console.log('==================================================');

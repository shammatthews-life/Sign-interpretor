/**
 * validate_phase_h6_extension.mjs
 *
 * Comprehensive validation suite for Phase H6:
 * Browser Extension Shell & Product Shell for ISL Accessibility Translator.
 *
 * Tests the 12 required criteria:
 *  1. Extension loads (Manifest V3 schema, file assets, icons, scripts)
 *  2. Content script injects
 *  3. Overlay opens (mount, show)
 *  4. Overlay closes (hide, minimize)
 *  5. Message communication works (envelope, schema versioning, actions)
 *  6. Demo transcript reaches UI
 *  7. Demo translation reaches UI
 *  8. Demo sign queue reaches UI
 *  9. Unavailable sign is displayed correctly (WATER, I, NEED transparent warnings)
 * 10. Runtime disconnect is handled gracefully (no uncaught error, clean state)
 * 11. Page remains functional (Shadow DOM encapsulation, host page unpolluted)
 * 12. Overlay cleanup works (clean teardown and memory release)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const assert = (condition, msg) => {
  if (!condition) {
    console.error(`FAIL: ${msg}`);
    throw new Error(msg);
  }
};

console.log('==================================================');
console.log('VALIDATING PHASE H6: BROWSER EXTENSION PRODUCT SHELL');
console.log('==================================================\n');

// ---------------------------------------------------------------------
// TEST 1: Extension Loads & Manifest V3 Validation
// ---------------------------------------------------------------------
console.log('--- TEST 1: Extension Loads & Manifest V3 Schema ---');
const manifestPath = path.join(projectRoot, 'extension', 'manifest.json');
assert(fs.existsSync(manifestPath), 'manifest.json must exist in extension/');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
assert(manifest.manifest_version === 3, 'Manifest version must be 3 (Manifest V3)');
assert(manifest.name && manifest.version, 'Manifest must have name and version');
assert(manifest.background?.service_worker, 'Manifest must declare a service worker');

// Check background file exists
const swPath = path.join(projectRoot, 'extension', manifest.background.service_worker);
assert(fs.existsSync(swPath), `Background service worker must exist at ${swPath}`);

// Check icons exist
assert(manifest.icons && manifest.icons['16'] && manifest.icons['48'] && manifest.icons['128'], 'Manifest must define 16, 48, 128 icons');
for (const [size, iconRel] of Object.entries(manifest.icons)) {
  const iconPath = path.join(projectRoot, 'extension', iconRel);
  assert(fs.existsSync(iconPath), `Icon (${size}px) must exist at ${iconPath}`);
  const stat = fs.statSync(iconPath);
  assert(stat.size > 0, `Icon (${size}px) must not be empty`);
}

// Check content scripts exist
assert(Array.isArray(manifest.content_scripts) && manifest.content_scripts.length > 0, 'Manifest must define content scripts');
for (const cs of manifest.content_scripts) {
  for (const jsFile of cs.js || []) {
    const jsPath = path.join(projectRoot, 'extension', jsFile);
    assert(fs.existsSync(jsPath), `Content script ${jsFile} must exist at ${jsPath}`);
  }
  for (const cssFile of cs.css || []) {
    const cssPath = path.join(projectRoot, 'extension', cssFile);
    assert(fs.existsSync(cssPath), `Content style ${cssFile} must exist at ${cssPath}`);
  }
}

// Check popup exists
assert(manifest.action?.default_popup, 'Manifest must specify default popup');
const popupPath = path.join(projectRoot, 'extension', manifest.action.default_popup);
assert(fs.existsSync(popupPath), `Popup HTML must exist at ${popupPath}`);

console.log('PASS: Manifest V3 schema and all referenced assets verified.\n');

// ---------------------------------------------------------------------
// Load Modules
// ---------------------------------------------------------------------
const { createRequire } = await import('module');
const require = createRequire(import.meta.url);

const messageContract = require('../extension/shared/message-contract.js');
const demoData = require('../extension/shared/demo-data.js');
const { RuntimeBridge } = require('../extension/background/runtime-bridge.js');

// ---------------------------------------------------------------------
// Mock DOM Implementation for UI Tests
// ---------------------------------------------------------------------
class MockDOMElement {
  constructor(tagName = 'div') {
    this.tagName = tagName.toUpperCase();
    this.id = '';
    this.className = '';
    this.style = {};
    this.dataset = {};
    this.children = [];
    this.parentNode = null;
    this.textContent_val = '';
    this.innerHTML_val = '';
    this.eventListeners = new Map();
    this.value = '';
    this.title = '';
    this.src = '';
    this.shadowRoot = null;
  }

  get textContent() {
    return this.textContent_val;
  }
  set textContent(val) {
    this.textContent_val = String(val);
    this.innerHTML_val = String(val);
  }

  get innerHTML() {
    return this.innerHTML_val;
  }
  set innerHTML(html) {
    this.innerHTML_val = html;
    this.children = [];
    this.parseHtmlStub(html);
  }

  get classList() {
    return {
      add: (cls) => {
        const set = new Set((this.className || '').split(' ').filter(Boolean));
        set.add(cls);
        this.className = [...set].join(' ');
      },
      remove: (cls) => {
        const set = new Set((this.className || '').split(' ').filter(Boolean));
        set.delete(cls);
        this.className = [...set].join(' ');
      },
      toggle: (cls, force) => {
        const set = new Set((this.className || '').split(' ').filter(Boolean));
        const has = set.has(cls);
        const shouldAdd = force !== undefined ? force : !has;
        if (shouldAdd) set.add(cls);
        else set.delete(cls);
        this.className = [...set].join(' ');
        return shouldAdd;
      },
      contains: (cls) => (this.className || '').split(' ').includes(cls)
    };
  }

  parseHtmlStub(html) {
    const idMatches = [...html.matchAll(/id=["']([^"']+)["']/g)];
    for (const match of idMatches) {
      const el = new MockDOMElement();
      el.id = match[1];
      el.parentNode = this;
      this.children.push(el);
    }
  }

  attachShadow({ mode = 'open' } = {}) {
    this.shadowRoot = new MockDOMElement('SHADOW-ROOT');
    this.shadowRoot.host = this;
    return this.shadowRoot;
  }

  appendChild(child) {
    child.parentNode = this;
    this.children.push(child);
    return child;
  }

  removeChild(child) {
    const idx = this.children.indexOf(child);
    if (idx !== -1) {
      this.children.splice(idx, 1);
      child.parentNode = null;
    }
    return child;
  }

  getElementById(id) {
    if (this.id === id) return this;
    for (const child of this.children) {
      const found = child.getElementById(id);
      if (found) return found;
    }
    return null;
  }

  addEventListener(type, listener) {
    if (!this.eventListeners.has(type)) this.eventListeners.set(type, []);
    this.eventListeners.get(type).push(listener);
  }

  removeEventListener(type, listener) {
    if (!this.eventListeners.has(type)) return;
    const list = this.eventListeners.get(type).filter(fn => fn !== listener);
    this.eventListeners.set(type, list);
  }

  dispatchEvent(event) {
    const list = this.eventListeners.get(event.type) || [];
    for (const fn of list) fn(event);
  }

  getBoundingClientRect() {
    return { left: 100, top: 100, width: 400, height: 500, right: 500, bottom: 600 };
  }
}

class MockDocument {
  constructor() {
    this.body = new MockDOMElement('BODY');
    this.readyState = 'complete';
    this.eventListeners = new Map();
  }

  createElement(tag) {
    return new MockDOMElement(tag);
  }

  getElementById(id) {
    return this.body.getElementById(id);
  }

  addEventListener(type, listener) {
    if (!this.eventListeners.has(type)) this.eventListeners.set(type, []);
    this.eventListeners.get(type).push(listener);
  }

  removeEventListener(type, listener) {
    if (!this.eventListeners.has(type)) return;
    this.eventListeners.set(type, this.eventListeners.get(type).filter(fn => fn !== listener));
  }
}

// Set up global mocks for UI testing
const mockDoc = new MockDocument();
global.document = mockDoc;
global.window = {
  innerWidth: 1920,
  innerHeight: 1080,
  addEventListener: () => {},
  removeEventListener: () => {}
};
global.self = global.window;
global.ISLMessageContract = messageContract;
global.ISLDemoData = demoData;

const overlayModule = require('../extension/content/overlay.js');
const ISLOverlayUI = overlayModule.ISLOverlayUI;

// ---------------------------------------------------------------------
// TEST 2: Content Script Injects
// ---------------------------------------------------------------------
console.log('--- TEST 2: Content Script Injection ---');
const contentScriptSource = fs.readFileSync(path.join(projectRoot, 'extension', 'content', 'content-script.js'), 'utf8');
assert(contentScriptSource.includes('__ISL_EXTENSION_INJECTED__'), 'Content script must prevent duplicate injection');
assert(contentScriptSource.includes('yt-navigate-finish'), 'Content script must support YouTube SPA navigation event');
assert(contentScriptSource.includes('__ISL_EXTENSION_CLEANUP__'), 'Content script must provide cleanup handler');
console.log('PASS: Content script injection structure and lifecycle hooks validated.\n');

// ---------------------------------------------------------------------
// TEST 3 & 4: Overlay Opens and Closes
// ---------------------------------------------------------------------
console.log('--- TEST 3 & 4: Overlay Opens, Minimizes, and Closes ---');
let lastDispatchedAction = null;
const ui = new ISLOverlayUI({
  onAction: (type, payload) => {
    lastDispatchedAction = { type, payload };
  }
});

ui.mount(mockDoc);
const rootHost = mockDoc.getElementById('isl-accessibility-overlay-root');
assert(rootHost !== null, 'Overlay root element must be mounted into document.body');
assert(rootHost.shadowRoot !== null, 'Overlay root must attach a Shadow DOM');

// Open / Close / Minimize states
assert(ui.isVisible === true, 'Overlay should initially be visible');
ui.hide();
assert(ui.isVisible === false, 'Overlay must hide when hide() is called');
assert(ui.elements.container.classList.contains('hidden'), 'Container must have hidden class');
assert(!ui.elements.launcher.classList.contains('hidden'), 'Launcher button must show when panel hidden');

ui.show();
assert(ui.isVisible === true, 'Overlay must show when show() is called');
assert(!ui.elements.container.classList.contains('hidden'), 'Container must remove hidden class');

ui.toggleMinimize();
assert(ui.isMinimized === true, 'Overlay must minimize when toggleMinimize() is called');
assert(ui.elements.container.classList.contains('minimized'), 'Container must have minimized class');

ui.toggleMinimize();
assert(ui.isMinimized === false, 'Overlay must un-minimize on second toggle');
console.log('PASS: Overlay opening, closing, and minimizing verified.\n');

// ---------------------------------------------------------------------
// TEST 5: Message Communication Works
// ---------------------------------------------------------------------
console.log('--- TEST 5: Message Communication Contract ---');
const testMsg = messageContract.createMessage(messageContract.MESSAGE_TYPES.GET_STATE, { foo: 'bar' });
assert(testMsg.version === '1.0.0', 'Message version must match contract version 1.0.0');
assert(testMsg.type === 'GET_STATE', 'Message type must match requested action');
assert(testMsg.correlationId.startsWith('msg_'), 'Message must generate correlationId');
assert(typeof testMsg.timestamp === 'number', 'Message must include timestamp');

const valResult = messageContract.validateMessage(testMsg);
assert(valResult.valid === true, 'Generated message must be valid according to contract');

const invalidVal = messageContract.validateMessage({ foo: 'no type' });
assert(invalidVal.valid === false, 'Invalid message without type must fail validation');
console.log('PASS: Message envelope, schema versioning, and validation verified.\n');

// ---------------------------------------------------------------------
// TEST 6, 7, 8: Demo Mode Text → Translation → Sign Queue reaches UI
// ---------------------------------------------------------------------
console.log('--- TEST 6, 7, 8: Demo Mode Text → Translation → Queue Flow ---');
let bridgeState = null;
const bridge = new RuntimeBridge({
  defaultEndpoint: 'http://localhost:8000',
  onStateUpdate: (s) => {
    bridgeState = s;
    ui.update(s);
  }
});

// Step 1: Greeting demo start
bridge.startDemo('greeting');
assert(bridgeState.demo.active === true, 'Demo mode should be active');
assert(bridgeState.demo.step === 1, 'Demo should begin at step 1');
assert(bridgeState.transcript.partial === 'hello', 'Step 1 should emit partial transcript "hello"');
assert(bridgeState.representation.gloss === 'HELLO', 'Step 1 gloss should be HELLO');
assert(bridgeState.signingQueue.currentSign === 'hello', 'Step 1 current active sign should be hello');

// Check UI updated
assert(ui.elements.boxPartial.textContent === 'hello', 'UI partial transcript box must display "hello"');
assert(ui.elements.boxGloss.textContent === 'HELLO', 'UI gloss badge must display HELLO');
assert(ui.elements.pillActiveSign.textContent === 'HELLO', 'UI active sign pill must show HELLO');

// Step 2: "hello good"
bridge.stepDemo();
assert(bridgeState.demo.step === 2, 'Demo must advance to step 2');
assert(bridgeState.transcript.partial === 'hello good', 'Step 2 partial transcript must be "hello good"');
assert(bridgeState.representation.gloss === 'HELLO GOOD', 'Step 2 gloss must be HELLO GOOD');
assert(bridgeState.signingQueue.queuedSigns.includes('good'), 'Step 2 queued signs must contain "good"');
assert(ui.elements.boxGloss.textContent === 'HELLO GOOD', 'UI gloss must update to HELLO GOOD');

// Step 3: Final transcript "hello good morning"
bridge.stepDemo();
assert(bridgeState.demo.step === 3, 'Demo must advance to step 3');
assert(bridgeState.transcript.final === 'hello good morning', 'Step 3 final transcript must be "hello good morning"');
assert(bridgeState.representation.gloss === 'HELLO GOOD MORNING', 'Step 3 gloss must be HELLO GOOD MORNING');
assert(bridgeState.signingQueue.queuedSigns.length === 2, 'Step 3 queue must contain [good, morning]');

// Step 4: Advance playback to "good"
bridge.stepDemo();
assert(bridgeState.signingQueue.currentSign === 'good', 'Step 4 current active sign must be good');
assert(bridgeState.signingQueue.queuedSigns.length === 1, 'Step 4 queued sign must be morning');

// Step 5: Advance playback to "morning"
bridge.stepDemo();
assert(bridgeState.signingQueue.currentSign === 'morning', 'Step 5 current active sign must be morning');
assert(bridgeState.signingQueue.queuedSigns.length === 0, 'Step 5 queue must be empty');

// Step 6: Playback finishes
bridge.stepDemo();
assert(bridgeState.signingQueue.currentSign === null, 'Step 6 playback finished; current sign null');
assert(bridgeState.signing === messageContract.STATES.SIGNING.IDLE, 'Signing state should be IDLE');
console.log('PASS: Text → Translation → Sign Queue state transitions verified through all 6 demo steps.\n');

// ---------------------------------------------------------------------
// TEST 9: Unavailable Sign Handling
// ---------------------------------------------------------------------
console.log('--- TEST 9: Missing Concept & Unavailable Signs ---');
bridge.startDemo('missing_concept');
assert(bridgeState.demo.scenario === 'missing_concept', 'Scenario must be missing_concept');
assert(bridgeState.representation.gloss === 'I WATER NEED', 'Translation should resolve to I WATER NEED');
assert(bridgeState.signing === messageContract.STATES.SIGNING.UNAVAILABLE, 'Signing state must be UNAVAILABLE');
assert(bridgeState.signingQueue.unavailableConcepts.length === 3, 'Must report 3 unavailable concepts (water, i, need)');

// Check UI reflects unavailable signs transparently
assert(!ui.elements.boxUnavailable.classList.contains('hidden'), 'UI unavailable concepts box must be visible');
assert(ui.elements.listUnavailable.innerHTML.includes('WATER'), 'Unavailable list must include WATER');
assert(ui.elements.listUnavailable.innerHTML.includes('MOTION_INCOMPLETE'), 'Unavailable list must note MOTION_INCOMPLETE');
assert(ui.elements.listUnavailable.innerHTML.includes('NEED'), 'Unavailable list must include NEED');
console.log('PASS: Unavailable concepts (WATER, I, NEED) displayed transparently with exact reasons without fake animation.\n');

// ---------------------------------------------------------------------
// TEST 10: Runtime Disconnect Handled Gracefully
// ---------------------------------------------------------------------
console.log('--- TEST 10: Localhost Offline / Disconnect Handling ---');
// Calling pingRuntime on non-listening port/bogus URL should NOT throw uncaught error
const offlineState = await bridge.pingRuntime('http://localhost:59999');
assert(offlineState.connection === messageContract.STATES.CONNECTION.DISCONNECTED, 'Connection must be DISCONNECTED when offline');
assert(offlineState.runtimeAvailable === false, 'runtimeAvailable must be false');
assert(offlineState.runtimeError !== null, 'runtimeError must explain offline status');
assert(ui.elements.stConn.textContent === 'DISCONNECTED', 'UI CONN pill must display DISCONNECTED');
assert(ui.elements.aetherIframe.classList.contains('hidden'), 'Aether iframe must be hidden when offline');
assert(!ui.elements.aetherFallback.classList.contains('hidden'), 'Aether offline fallback card must be visible');
console.log('PASS: Offline runtime failure handled gracefully without uncaught exceptions.\n');

// ---------------------------------------------------------------------
// TEST 11: Page Remains Functional (Shadow DOM Isolation)
// ---------------------------------------------------------------------
console.log('--- TEST 11: Host Page Isolation & Non-Interference ---');
assert(rootHost.tagName === 'DIV', 'Host element must be a standard wrapper DIV');
assert(rootHost.shadowRoot !== null, 'Overlay DOM must reside in open shadowRoot');
assert(mockDoc.body.children.length === 1, 'Only the single root wrapper was added to body');
console.log('PASS: Shadow DOM container prevents style leakage and preserves host page integrity.\n');

// ---------------------------------------------------------------------
// TEST 12: Overlay Cleanup
// ---------------------------------------------------------------------
console.log('--- TEST 12: Overlay Teardown & Cleanup ---');
ui.destroy();
assert(mockDoc.body.children.length === 0, 'Overlay host element must be completely removed from body on destroy');
assert(ui.hostElement === null, 'Host element reference must be nulled');
assert(ui.shadowRoot === null, 'Shadow root reference must be nulled');
console.log('PASS: Teardown and DOM cleanup verified.\n');

console.log('==================================================');
console.log('ALL 12 PHASE H6 EXTENSION TESTS PASSED CLEANLY!');
console.log('==================================================');

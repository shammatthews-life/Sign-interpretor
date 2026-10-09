/**
 * H8 YouTube extension integration validation.
 *
 * Default mode is deterministic and offline. Pass --runtime to exercise the
 * local HTTP API against the cached H7 test video without forcing a download.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const nativeFetch = globalThis.fetch.bind(globalThis);
const contract = require('../extension/shared/message-contract.js');
global.ISLMessageContract = contract;
const { RuntimeBridge } = require('../extension/background/runtime-bridge.js');

function validateManifestAndExtension() {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'extension/manifest.json'), 'utf8'));
  assert.equal(manifest.manifest_version, 3);
  assert(manifest.host_permissions.some(permission => permission.startsWith('http://localhost:')));
  for (const file of [
    manifest.background.service_worker,
    manifest.action.default_popup,
    ...manifest.content_scripts.flatMap(script => [...script.js, ...script.css])
  ]) assert(fs.existsSync(path.join(root, 'extension', file)), `Missing extension resource: ${file}`);
  const popup = fs.readFileSync(path.join(root, 'extension', manifest.action.default_popup), 'utf8');
  assert(popup.includes('id="youtube-url"') && popup.includes('id="btn-youtube-process"'));
  console.log('PASS 1: Manifest and extension resource loading.');
}

function validateUrlAndContract() {
  const valid = contract.validateYouTubeUrl('https://youtu.be/y8tFSuOMAqQ');
  assert.equal(valid.valid, true);
  assert.equal(valid.videoId, 'y8tFSuOMAqQ');
  assert.equal(valid.canonicalUrl, 'https://www.youtube.com/watch?v=y8tFSuOMAqQ');
  for (const invalid of ['', 'not a url', 'https://youtube.com.evil.test/watch?v=y8tFSuOMAqQ', 'https://youtube.com/watch?v=short']) {
    assert.equal(contract.validateYouTubeUrl(invalid).valid, false, `Unexpectedly accepted: ${invalid}`);
  }
  for (const type of ['YOUTUBE_PROCESS', 'YOUTUBE_JOB_CREATED', 'YOUTUBE_STATUS', 'YOUTUBE_RESULT', 'YOUTUBE_ERROR']) {
    const message = contract.createMessage(contract.MESSAGE_TYPES[type], {});
    assert.equal(contract.validateMessage(message).valid, true);
    assert.equal(message.version, contract.CONTRACT_VERSION);
  }
  console.log('PASS 2: YouTube URL validation and versioned message contract.');
}

class MockElement {
  constructor(tagName = 'div') {
    this.tagName = tagName.toUpperCase();
    this.id = '';
    this.className = '';
    this.style = {};
    this.dataset = {};
    this.children = [];
    this.parentNode = null;
    this.textContent = '';
    this.value = '';
    this.src = '';
    this.listeners = new Map();
  }
  set innerHTML(value) {
    this.html = value;
    this.children = [...String(value).matchAll(/id=["']([^"']+)["']/g)].map(match => {
      const child = new MockElement();
      child.id = match[1];
      child.parentNode = this;
      return child;
    });
  }
  get innerHTML() { return this.html || ''; }
  get classList() {
    const element = this;
    const classes = () => new Set(element.className.split(/\s+/).filter(Boolean));
    return {
      add(name) { const value = classes(); value.add(name); element.className = [...value].join(' '); },
      remove(name) { const value = classes(); value.delete(name); element.className = [...value].join(' '); },
      contains(name) { return classes().has(name); },
      toggle(name, force) {
        const value = classes();
        const shouldAdd = force === undefined ? !value.has(name) : force;
        if (shouldAdd) value.add(name); else value.delete(name);
        element.className = [...value].join(' ');
        return shouldAdd;
      }
    };
  }
  attachShadow() { this.shadowRoot = new MockElement('shadow-root'); return this.shadowRoot; }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  removeChild(child) { this.children = this.children.filter(item => item !== child); child.parentNode = null; }
  getElementById(id) {
    if (this.id === id) return this;
    for (const child of this.children) {
      const match = child.getElementById(id);
      if (match) return match;
    }
    return null;
  }
  addEventListener(type, listener) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(listener);
  }
}

function validateOverlayLifecycleAndSpaResilience() {
  const document = {
    body: new MockElement('body'),
    createElement: tagName => new MockElement(tagName),
    getElementById(id) { return this.body.getElementById(id); }
  };
  global.document = document;
  global.window = {
    innerWidth: 1280,
    innerHeight: 720,
    addEventListener() {},
    removeEventListener() {}
  };
  global.self = global.window;
  global.chrome = { runtime: { getURL: value => `chrome-extension://test/${value}` } };
  const { ISLOverlayUI } = require('../extension/content/overlay.js');
  const overlay = new ISLOverlayUI();
  overlay.mount(document);
  const host = document.getElementById('isl-accessibility-overlay-root');
  assert(host?.shadowRoot);
  overlay.mount(document);
  assert.equal(document.body.children.length, 1, 'Mount must not create duplicate overlay roots.');
  overlay.hide();
  assert.equal(overlay.isVisible, false);
  overlay.show();
  assert.equal(overlay.isVisible, true);
  overlay.update({
    youtube: { state: 'READY', title: 'Real video', segmentCount: 1, latestSegment: 'Real ASR', glosses: ['GOOD'], playableSigns: ['good'], unavailableConcepts: [{ word: 'water', reason: 'MOTION_INCOMPLETE' }] },
    signingQueue: { currentSign: 'good', queuedSigns: [] }
  });
  assert.equal(overlay.elements.youtubeVideoTitle.textContent, 'Real video');
  assert.match(overlay.elements.youtubeUnavailableConcepts.textContent, /WATER/);
  assert.match(overlay.elements.youtubeUnavailableConcepts.textContent, /MOTION_INCOMPLETE/);
  const contentScript = fs.readFileSync(path.join(root, 'extension/content/content-script.js'), 'utf8');
  assert(contentScript.includes('__ISL_EXTENSION_INJECTED__'));
  assert(contentScript.includes('yt-navigate-finish'));
  assert(contentScript.includes('__ISL_EXTENSION_CLEANUP__'));
  assert(contentScript.includes('AETHER_COMMAND'));
  overlay.destroy();
  assert.equal(document.body.children.length, 0);
  console.log('PASS 13-14: Overlay lifecycle, single mount, YouTube SPA resilience, and Aether command relay.');
}

async function validateBridgeWithDeterministicFetch() {
  const originalFetch = globalThis.fetch;
  const requests = [];
  const states = [];
  let statusPolls = 0;
  global.fetch = async (url, options = {}) => {
    requests.push({ url: String(url), method: options.method || 'GET' });
    if (String(url).endsWith('/youtube/process')) {
      return Response.json({ job_id: 'yt_test_123', state: 'QUEUED' }, { status: 202 });
    }
    if (String(url).endsWith('/youtube/status/yt_test_123')) {
      statusPolls += 1;
      return statusPolls === 1
        ? Response.json({ job_id: 'yt_test_123', stage: 'DOWNLOADING', progress: 0.25 })
        : Response.json({ job_id: 'yt_test_123', stage: 'READY', progress: 1 });
    }
    if (String(url).endsWith('/youtube/result/yt_test_123')) {
      return Response.json({
        job_id: 'yt_test_123',
        state: 'READY',
        result: {
          metadata: { title: 'Video', duration: 20, audio_duration_s: 19.8 },
          transcript: { full_text: 'good morning', segments: [{ start: 0, end: 1, text: 'good morning' }] },
          translation: { translated_segments: [{
            gloss: ['GOOD', 'MORNING'],
            playable_signs: ['good'],
            unavailable_concepts: [{ sign_id: 'morning', reason: 'MOTION_NOT_AUTHORED' }]
          }] }
        }
      });
    }
    throw new Error(`Unexpected deterministic fetch: ${url}`);
  };
  const bridge = new RuntimeBridge({ defaultEndpoint: 'http://localhost:8000', onStateUpdate: state => states.push(state) });
  await assert.rejects(() => bridge.submitYouTube('https://example.com/watch?v=y8tFSuOMAqQ'), /valid YouTube/);
  const job = await bridge.submitYouTube('https://youtu.be/y8tFSuOMAqQ');
  assert.equal(job.job_id, 'yt_test_123');
  assert.equal(job.state, 'QUEUED');
  for (let count = 0; count < 50 && bridge.getState().youtube.state !== 'READY'; count += 1) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  const state = bridge.getState();
  assert.equal(state.youtube.state, 'READY');
  assert.equal(state.youtube.segmentCount, 1);
  assert.deepEqual(state.youtube.playableSigns, ['good']);
  assert.equal(state.youtube.unavailableConcepts[0].word, 'morning');
  assert.equal(state.youtube.transcriptSummary, 'good morning');
  assert(states.some(value => value.youtube.state === 'READY'));
  assert(states.some(value => value.youtube.state === 'DOWNLOADING'));
  assert(requests.some(request => request.method === 'POST' && request.url.endsWith('/youtube/process')));
  assert(requests.some(request => request.url.endsWith('/youtube/status/yt_test_123')));
  assert(requests.some(request => request.url.endsWith('/youtube/result/yt_test_123')));

  const commands = [
    contract.createMessage(contract.MESSAGE_TYPES.AETHER_COMMAND, { command: contract.AETHER_COMMANDS.PLAY_SIGN, signId: 'good' }),
    contract.createMessage(contract.MESSAGE_TYPES.AETHER_COMMAND, { command: contract.AETHER_COMMANDS.QUEUE_SIGN, signId: 'good' })
  ];
  assert(commands.every(message => contract.validateMessage(message).valid));
  const avatar = fs.readFileSync(path.join(root, 'tools/avatar_viewer/index.html'), 'utf8');
  assert(avatar.includes("case 'PLAY_SIGN':") && avatar.includes("case 'QUEUE_SIGN':"));
  globalThis.fetch = async () => { throw new TypeError('Failed to fetch'); };
  const offlineBridge = new RuntimeBridge({ defaultEndpoint: 'http://offline.test' });
  await assert.rejects(() => offlineBridge.submitYouTube('https://youtu.be/y8tFSuOMAqQ'), /Failed to fetch/);

  globalThis.fetch = async () => Response.json({ state: 'READY' }, { status: 202 });
  const malformedBridge = new RuntimeBridge({ defaultEndpoint: 'http://malformed.test' });
  await assert.rejects(() => malformedBridge.submitYouTube('https://youtu.be/y8tFSuOMAqQ'), /malformed YouTube job response/);

  globalThis.fetch = async url => {
    if (String(url).endsWith('/youtube/process')) return Response.json({ job_id: 'yt_error_123', state: 'QUEUED' }, { status: 202 });
    if (String(url).endsWith('/youtube/status/yt_error_123')) return Response.json({ job_id: 'yt_error_123', stage: 'ERROR', error: 'ASR failed' });
    throw new Error(`Unexpected failure test request: ${url}`);
  };
  const failedJobBridge = new RuntimeBridge({ defaultEndpoint: 'http://failure.test' });
  await failedJobBridge.submitYouTube('https://youtu.be/y8tFSuOMAqQ');
  for (let count = 0; count < 50 && failedJobBridge.getState().youtube.state !== 'ERROR'; count += 1) {
    await new Promise(resolve => setTimeout(resolve, 20));
  }
  assert.equal(failedJobBridge.getState().youtube.error, 'ASR failed');

  globalThis.fetch = (_url, options) => new Promise((_resolve, reject) => {
    options.signal.addEventListener('abort', () => reject(Object.assign(new Error('aborted'), { name: 'AbortError' })), { once: true });
  });
  const timeoutBridge = new RuntimeBridge({ defaultEndpoint: 'http://timeout.test' });
  await assert.rejects(() => timeoutBridge.requestJson('http://timeout.test/test', {}, 5), /timed out/);
  globalThis.fetch = originalFetch;
  console.log('PASS 3-12: Deterministic submit, job ID, polling, result schema, transcript, translation, availability, errors, and Aether commands.');
}

async function validateRuntime() {
  const endpoint = process.env.H7_RUNTIME_URL || 'http://localhost:8000';
  const invalidResponse = await nativeFetch(`${endpoint}/youtube/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: 'https://example.com/not-youtube' })
  });
  assert.equal(invalidResponse.status, 400, 'Invalid YouTube URL must fail with HTTP 400.');
  const invalidSubdomainResponse = await nativeFetch(`${endpoint}/youtube/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: 'https://evil.youtube.com/watch?v=y8tFSuOMAqQ' })
  });
  assert.equal(invalidSubdomainResponse.status, 400, 'Unapproved YouTube subdomain must fail with HTTP 400.');
  const unknownJob = await nativeFetch(`${endpoint}/youtube/status/not_a_real_job`);
  assert.equal(unknownJob.status, 404, 'Unknown job ID must fail with HTTP 404.');
  const response = await nativeFetch(`${endpoint}/youtube/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: 'https://youtu.be/y8tFSuOMAqQ' })
  });
  assert.equal(response.status, 202, `Expected job creation HTTP 202; got ${response.status}`);
  const job = await response.json();
  assert.equal(job.state, 'QUEUED');
  assert.equal(typeof job.job_id, 'string');
  console.log(`Runtime job created: ${job.job_id}`);

  const deadline = Date.now() + 20 * 60 * 1000;
  let status;
  do {
    await new Promise(resolve => setTimeout(resolve, 1000));
    const statusResponse = await nativeFetch(`${endpoint}/youtube/status/${encodeURIComponent(job.job_id)}`);
    assert.equal(statusResponse.status, 200);
    status = await statusResponse.json();
    assert.equal(status.job_id, job.job_id);
    console.log(`Runtime state: ${status.stage} (${Math.round((status.progress || 0) * 100)}%)`);
    assert(!['INITIALIZING'].includes(status.stage));
    if (status.stage === 'ERROR') throw new Error(status.error || 'H7 job failed.');
  } while (status.stage !== 'READY' && Date.now() < deadline);
  assert.equal(status.stage, 'READY', 'H7 job exceeded the runtime test timeout.');

  const resultResponse = await nativeFetch(`${endpoint}/youtube/result/${encodeURIComponent(job.job_id)}`);
  assert.equal(resultResponse.status, 200);
  const envelope = await resultResponse.json();
  const result = envelope.result;
  assert.equal(envelope.state, 'READY');
  assert(result.transcript.segments.length > 0);
  assert(result.transcript.segments.every(segment => Number.isFinite(segment.start) && Number.isFinite(segment.end) && typeof segment.text === 'string'));
  const translated = result.translation.translated_segments;
  const playable = translated.flatMap(segment => segment.playable_signs || []);
  const unavailable = translated.flatMap(segment => segment.unavailable_concepts || []);
  assert(playable.length > 0, 'Real H7 transcript has no playable signs.');
  assert(playable.every(sign => sign === 'good'), 'Unexpected playable sign in cached test video.');
  assert(unavailable.length > 0, 'Expected unavailable concepts to remain visible.');

  const aetherCommands = [];
  let workerListener;
  const chrome = {
    runtime: {
      onInstalled: { addListener() {} },
      onMessage: { addListener(listener) { workerListener = listener; } },
      sendMessage(_message, callback) { callback?.({}); },
      lastError: null
    },
    tabs: {
      query(_query, callback) { callback([{ id: 42 }]); },
      sendMessage(tabId, message, callback) {
        if (message.type === contract.MESSAGE_TYPES.AETHER_COMMAND) aetherCommands.push({ tabId, ...message.payload });
        callback?.({});
      }
    }
  };
  const workerSource = fs.readFileSync(path.join(root, 'extension/background/service-worker.js'), 'utf8');
  const workerContext = {
    self: {
      ISLMessageContract: contract,
      ISLRuntimeBridge: { RuntimeBridge },
      ISLDemoData: {}
    },
    chrome,
    importScripts() {},
    fetch: nativeFetch,
    AbortController,
    console,
    setTimeout,
    clearTimeout
  };
  const vm = await import('node:vm');
  vm.runInNewContext(workerSource, workerContext, { filename: 'extension/background/service-worker.js' });
  assert.equal(typeof workerListener, 'function', 'Service worker message listener did not register.');
  const workerResponse = await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Service worker did not return the created job.')), 15000);
    workerListener(
      contract.createMessage(contract.MESSAGE_TYPES.YOUTUBE_PROCESS, { url: 'https://youtu.be/y8tFSuOMAqQ' }),
      {},
      value => { clearTimeout(timeout); resolve(value); }
    );
  });
  assert.equal(workerResponse.success, true);
  const workerJobId = workerResponse.payload.job_id;
  const commandDeadline = Date.now() + 30000;
  while (!aetherCommands.length && Date.now() < commandDeadline) await new Promise(resolve => setTimeout(resolve, 100));
  assert.deepEqual(aetherCommands.map(command => command.command), ['PLAY_SIGN', 'QUEUE_SIGN', 'QUEUE_SIGN']);
  assert(aetherCommands.every(command => command.signId === 'good' && command.tabId === 42));
  console.log(JSON.stringify({
    job_id: job.job_id,
    extension_worker_job_id: workerJobId,
    video_title: result.metadata.title,
    audio_duration_s: result.transcript.audio_duration_s,
    transcript_segments: result.transcript.segment_count,
    resolved_concept_occurrences: result.translation.total_concept_occurrences,
    playable_sign_occurrences: playable.length,
    playable_signs: [...new Set(playable)],
    unavailable_concept_occurrences: unavailable.length,
    unknown_term_occurrences: result.translation.unknown_term_occurrences,
    extension_worker_aether_commands: aetherCommands.map(({ command, signId }) => ({ command, signId }))
  }, null, 2));
}

validateManifestAndExtension();
validateUrlAndContract();
validateOverlayLifecycleAndSpaResilience();
await validateBridgeWithDeterministicFetch();
if (process.argv.includes('--runtime')) await validateRuntime();

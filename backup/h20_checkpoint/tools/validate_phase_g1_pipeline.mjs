/**
 * validate_phase_g1_pipeline.mjs
 *
 * Full integration test for Phase G1 — Speech-to-Sign Pipeline:
 *   Streaming ASR Events
 *     ↓
 *   SpeechSignOrchestrator
 *     ↓
 *   SentenceProcessor
 *     ↓
 *   Real SignLibrary (signs/*.json)
 *     ↓
 *   SignScheduler & SignAnimationPlayer
 */

import fs from 'fs/promises';
import path from 'path';
import { SpeechSignOrchestrator } from './avatar_viewer/SpeechSignOrchestrator.js';
import { SentenceProcessor } from './avatar_viewer/SentenceProcessor.js';
import { SignLibrary } from './avatar_viewer/SignLibrary.js';
import { SignScheduler } from './avatar_viewer/SignScheduler.js';

const assert = (condition, msg) => {
  if (!condition) throw new Error(msg);
};

console.log('==================================================');
console.log('VALIDATING PHASE G1: SPEECH → SIGN → AETHER');
console.log('==================================================');

// 1. Mock Bones Map matching Aether verified rig bones from sign definitions
const allBones = new Set();
for (const signDef of [
  await fs.readFile(path.resolve('signs/hello.json'), 'utf-8').then(JSON.parse),
  await fs.readFile(path.resolve('signs/good.json'), 'utf-8').then(JSON.parse),
  await fs.readFile(path.resolve('signs/morning.json'), 'utf-8').then(JSON.parse),
]) {
  if (signDef.motion?.involved_bones) {
    for (const b of signDef.motion.involved_bones) allBones.add(b);
  }
}
const mockBonesMap = new Map([...allBones].map(name => [name, {}]));

// 2. Mock Three.js Animation Player for Aether
class MockAetherPlayer {
  constructor() {
    this.currentSign = null;
    this.playing = false;
    this.currentTimeMs = 0;
    this.history = [];
    this.onCompleteCallback = null;
  }
  loadSign(motion) {
    this.currentSign = motion.sign_id;
    this.currentTimeMs = 0;
    this.history.push({ signId: motion.sign_id, loadedAt: performance.now() });
  }
  play() { this.playing = true; }
  pause() { this.playing = false; }
  stop() { this.playing = false; this.currentSign = null; this.currentTimeMs = 0; }
  step(ms) {
    if (!this.playing) return;
    this.currentTimeMs += ms;
  }
  complete() {
    this.playing = false;
    const finished = this.currentSign;
    this.currentSign = null;
    if (this.onCompleteCallback) this.onCompleteCallback();
    return finished;
  }
}

// 3. File-backed SignLibrary loader reading disk signs/
const fileFetch = async (url) => {
  const filePath = path.resolve('signs', path.basename(url));
  try {
    const data = await fs.readFile(filePath, 'utf-8');
    return { ok: true, json: async () => JSON.parse(data) };
  } catch (err) {
    return { ok: false, status: 404, statusText: 'Not Found' };
  }
};

const library = new SignLibrary({ fetchImpl: fileFetch });
await library.preload(['hello', 'good', 'morning', 'water']);

// -------------------------------------------------------------
// TEST 1: Task 7 & 8 — "Hello good morning" streaming pipeline
// -------------------------------------------------------------
console.log("\n--- TEST 1: End-to-End 'Hello good morning' Incremental Speech Pipeline ---");
const processor = new SentenceProcessor();
const player1 = new MockAetherPlayer();
const scheduler1 = new SignScheduler(player1, library, mockBonesMap);

let commitCount = 0;
const orchestrator1 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler1,
  signLibrary: library,
  onCommit: (rec) => {
    commitCount += 1;
    console.log(`  [Commit ${commitCount}] Sign '${rec.id.toUpperCase()}' safely committed to scheduler.`);
  },
});

const t0 = performance.now();
orchestrator1.start(t0);

// Step A: Speaker says "Hello..." -> Partial 1 arrives
console.log("-> ASR Partial 1: 'hello'");
orchestrator1.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello',
  audio_start_ms: t0,
  audio_end_ms: t0 + 800,
});
// "hello" is trailing in partial 1, waiting for second observation or subsequent token
assert(orchestrator1.committedSigns.length === 0, 'Trailing single token should not commit on first partial.');

// Step B: Speaker continues "...good..." -> Partial 2 arrives
console.log("-> ASR Partial 2: 'hello good'");
orchestrator1.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello good',
  audio_start_ms: t0,
  audio_end_ms: t0 + 1500,
});
// "hello" is followed by "good" -> Stable prefix confirmed! Commits HELLO!
assert(orchestrator1.committedSigns.length === 1, 'HELLO must be committed.');
assert(orchestrator1.committedSigns[0].id === 'hello', 'First sign must be HELLO.');
assert(scheduler1.getState().current === 'hello', 'Aether must start signing HELLO immediately.');
console.log("  Aether active sign: " + scheduler1.getState().current.toUpperCase());

// Step C: Speaker continues "...morning." -> Partial 3 arrives
console.log("-> ASR Partial 3: 'hello good morning'");
orchestrator1.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello good morning',
  audio_start_ms: t0,
  audio_end_ms: t0 + 2100,
});
// "good" is followed by "morning" -> Stable prefix confirmed! Commits GOOD!
// HELLO must NOT be re-committed or duplicated!
assert(orchestrator1.committedSigns.length === 2, 'GOOD must be committed.');
assert(orchestrator1.committedSigns[1].id === 'good', 'Second sign must be GOOD.');
assert(scheduler1.getState().current === 'hello', 'Aether must still be playing HELLO.');
assert(scheduler1.getState().queued[0] === 'good', 'GOOD must be queued behind active HELLO.');
console.log(`  Aether active sign: ${scheduler1.getState().current.toUpperCase()}, Queued: [${scheduler1.getState().queued.map(s => s.toUpperCase()).join(', ')}]`);

// Step D: ASR flushes final transcript
console.log("-> ASR Final Transcript: 'hello good morning'");
orchestrator1.handleTranscriptEvent({
  kind: 'FINAL_TRANSCRIPT',
  text: 'hello good morning',
  audio_start_ms: t0,
  audio_end_ms: t0 + 2600,
});
// Final confirms remaining MORNING!
assert(orchestrator1.committedSigns.length === 3, 'MORNING must be committed.');
assert(orchestrator1.committedSigns[2].id === 'morning', 'Third sign must be MORNING.');
assert(JSON.stringify(scheduler1.getState().queued) === JSON.stringify(['good', 'morning']), 'Queue must be [GOOD, MORNING].');
console.log(`  Aether active sign: ${scheduler1.getState().current.toUpperCase()}, Queued: [${scheduler1.getState().queued.map(s => s.toUpperCase()).join(', ')}]`);

// Step E: Verify Aether completes signs in sequence
console.log("-> Stepping Aether playback completion...");
player1.complete(); // HELLO completes -> GOOD starts automatically
assert(scheduler1.getState().current === 'good', 'GOOD must transition to active.');
console.log("  Active: " + scheduler1.getState().current.toUpperCase());

player1.complete(); // GOOD completes -> MORNING starts automatically
assert(scheduler1.getState().current === 'morning', 'MORNING must transition to active.');
console.log("  Active: " + scheduler1.getState().current.toUpperCase());

player1.complete(); // MORNING completes -> Queue empty
assert(!scheduler1.getState().current && scheduler1.getState().queued.length === 0, 'Scheduler queue must be cleanly emptied.');
console.log("  Sequence playback finished cleanly.");

const playedSigns = player1.history.map(h => h.signId);
assert(JSON.stringify(playedSigns) === JSON.stringify(['hello', 'good', 'morning']), `Expected ['hello', 'good', 'morning'], got ${JSON.stringify(playedSigns)}`);
console.log("PASS: Speech 'Hello good morning' mapped to HELLO -> GOOD -> MORNING with zero sign duplication.");

// -------------------------------------------------------------
// TEST 2: Task 11 — Safety against duplicate transcript wobble
// -------------------------------------------------------------
console.log("\n--- TEST 2: Task 11 — Duplicate Transcript Evolution Stress Test ---");
const player2 = new MockAetherPlayer();
const scheduler2 = new SignScheduler(player2, library, mockBonesMap);
const orchestrator2 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler2,
  signLibrary: library,
});
orchestrator2.start();

const wobbleSequence = [
  { kind: 'PARTIAL_TRANSCRIPT', text: 'hello' },
  { kind: 'PARTIAL_TRANSCRIPT', text: 'hello good' },
  { kind: 'PARTIAL_TRANSCRIPT', text: 'hello good morning' },
  { kind: 'PARTIAL_TRANSCRIPT', text: 'hello good morning' }, // duplicate text partial
  { kind: 'PARTIAL_TRANSCRIPT', text: 'hello good morning' }, // duplicate text partial
  { kind: 'FINAL_TRANSCRIPT',   text: 'hello good morning' }, // finalization
];

for (const ev of wobbleSequence) {
  orchestrator2.handleTranscriptEvent(ev);
}

const diag2 = orchestrator2.getDiagnostics();
assert(diag2.signsCommitted === 3, `Expected 3 committed signs, got ${diag2.signsCommitted}`);
assert(JSON.stringify(diag2.committedSignIds) === JSON.stringify(['hello', 'good', 'morning']), `Expected ['hello', 'good', 'morning'], got ${JSON.stringify(diag2.committedSignIds)}`);
console.log("PASS: 5 overlapping/repeated partials produced exactly 3 unique sign commitments (zero duplicate enqueuing).");

// -------------------------------------------------------------
// TEST 3: Task 4 — Unknown words & MOTION_INCOMPLETE signs (WATER)
// -------------------------------------------------------------
console.log("\n--- TEST 3: Task 4 — Unknown Words & MOTION_INCOMPLETE Signs ---");
const player3 = new MockAetherPlayer();
const scheduler3 = new SignScheduler(player3, library, mockBonesMap);
const orchestrator3 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler3,
  signLibrary: library,
});
orchestrator3.start();

orchestrator3.handleTranscriptEvent({
  kind: 'FINAL_TRANSCRIPT',
  text: 'hello water smartphone morning',
});

const diag3 = orchestrator3.getDiagnostics();
assert(diag3.unknownWords.includes('SMARTPHONE'), 'SMARTPHONE must be reported as unknown word.');
assert(diag3.unavailableSigns.includes('water'), 'WATER must be reported as unavailable (MOTION_INCOMPLETE).');
assert(!diag3.committedSignIds.includes('water'), 'WATER must NOT be sent to Aether scheduler.');
assert(!diag3.committedSignIds.includes('smartphone'), 'SMARTPHONE must NOT fabricate a sign.');
assert(JSON.stringify(diag3.committedSignIds) === JSON.stringify(['hello', 'morning']), `Expected ['hello', 'morning'], got ${JSON.stringify(diag3.committedSignIds)}`);
console.log("PASS: Unknown words and incomplete signs filtered safely with zero hallucinated signs.");

// -------------------------------------------------------------
// TEST 4: Task 12 — Backpressure & Queue Age Measurement
// -------------------------------------------------------------
console.log("\n--- TEST 4: Task 12 — Backpressure Diagnostics ---");
const player4 = new MockAetherPlayer();
const scheduler4 = new SignScheduler(player4, library, mockBonesMap);
const orchestrator4 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler4,
  signLibrary: library,
});
orchestrator4.start();

// Fast burst: 3 signs arriving in rapid succession
orchestrator4.handleTranscriptEvent({
  kind: 'FINAL_TRANSCRIPT',
  text: 'hello good morning',
});

const bpDiag = orchestrator4.getDiagnostics();
console.log(`  Signs committed:       ${bpDiag.signsCommitted}`);
console.log(`  Current active sign:   ${bpDiag.currentSign}`);
console.log(`  Queued signs:          [${bpDiag.queuedSigns.join(', ')}] (count: ${bpDiag.queueCount})`);
console.log(`  Oldest queued sign:    '${bpDiag.oldestQueuedSign}'`);
console.log(`  Queue age:             ${bpDiag.queueAgeMs} ms`);

assert(bpDiag.currentSign === 'hello', 'HELLO should be active.');
assert(bpDiag.queueCount === 2, 'Two signs should be waiting in queue.');
assert(bpDiag.oldestQueuedSign === 'good', 'GOOD should be the oldest queued sign.');
assert(typeof bpDiag.queueAgeMs === 'number', 'Queue age must be numeric.');
console.log("PASS: Backpressure diagnostics accurately capture queue buildup when speech outpaces signing.");

// -------------------------------------------------------------
// TEST 5: Task 14 — End-to-End Latency Instrumentation
// -------------------------------------------------------------
console.log("\n--- TEST 5: Task 14 — End-to-End Timing Telemetry (T0 -> T1 -> T2 -> T3 -> T4) ---");
const player5 = new MockAetherPlayer();
const scheduler5 = new SignScheduler(player5, library, mockBonesMap);
const orchestrator5 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler5,
  signLibrary: library,
});

const audioT0 = performance.now() - 300.0; // Audio started 300ms ago
orchestrator5.start(audioT0);

orchestrator5.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello good',
  audio_start_ms: audioT0,
});

const tDiag = orchestrator5.getDiagnostics().timings;
console.log(`  T0 (Audio Entered):     ${tDiag.t0?.toFixed(1)} ms`);
console.log(`  T1 (First Partial):     ${tDiag.t1?.toFixed(1)} ms (T1 - T0 = ${tDiag.firstPartialLatencyMs?.toFixed(1)} ms)`);
console.log(`  T2 (First Sign Commit): ${tDiag.t2?.toFixed(1)} ms (T2 - T0 = ${tDiag.firstCommitLatencyMs?.toFixed(1)} ms)`);
console.log(`  T3 (Scheduler Enqueue): ${tDiag.t3?.toFixed(1)} ms (T3 - T2 = ${tDiag.schedulerEnqueueLatencyMs?.toFixed(3)} ms)`);
console.log(`  T4 (Aether Playback):   ${tDiag.t4?.toFixed(1)} ms (T4 - T0 = ${tDiag.speechToAetherLatencyMs?.toFixed(1)} ms)`);

assert(tDiag.t0 === audioT0, 'T0 mismatch.');
assert(tDiag.firstPartialLatencyMs >= 0, 'T1 - T0 must be non-negative.');
assert(tDiag.firstCommitLatencyMs >= 0, 'T2 - T0 must be non-negative.');
assert(tDiag.speechToAetherLatencyMs >= 0, 'T4 - T0 must be non-negative.');
console.log("PASS: Full end-to-end speech-to-Aether latency instrumented accurately.");

// -------------------------------------------------------------
// TEST 6: Task 13 — Lifecycle (Start, Pause, Resume, Reset)
// -------------------------------------------------------------
console.log("\n--- TEST 6: Task 13 — Lifecycle Management ---");
orchestrator5.pause();
assert(orchestrator5.state === 'paused', 'Orchestrator must be paused.');
assert(scheduler5.isPaused, 'Scheduler must be paused.');

orchestrator5.resume();
assert(orchestrator5.state === 'running', 'Orchestrator must resume.');
assert(!scheduler5.isPaused, 'Scheduler must resume.');

orchestrator5.reset();
assert(orchestrator5.state === 'idle', 'Orchestrator must be idle.');
assert(orchestrator5.committedSigns.length === 0, 'Committed signs cleared.');
assert(scheduler5.queue.length === 0, 'Scheduler queue cleared.');
assert(scheduler5.currentId === null, 'Active sign stopped.');
console.log("PASS: Lifecycle transitions verified with clean reset.");

console.log('\n==================================================');
console.log('ALL PHASE G1 INTEGRATION PIPELINE TESTS PASSED!');
console.log('==================================================');

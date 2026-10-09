/**
 * validate_speech_sign_orchestrator.mjs
 *
 * Unit tests for Phase G1 SpeechSignOrchestrator:
 * - Partial transcript evolution and incremental queuing
 * - Strict duplicate suppression
 * - Final transcript flush and commitment
 * - Unknown word detection and reporting (no fabrication)
 * - Incomplete / unavailable sign handling (e.g. WATER)
 * - Backpressure diagnostics and queue age measurement
 * - End-to-end timing instrumentation (T0 -> T1 -> T2 -> T3 -> T4)
 * - Clean lifecycle pause, resume, reset
 */

import { SpeechSignOrchestrator } from './avatar_viewer/SpeechSignOrchestrator.js';
import { SentenceProcessor } from './avatar_viewer/SentenceProcessor.js';
import { SignScheduler } from './avatar_viewer/SignScheduler.js';

const assert = (condition, msg) => {
  if (!condition) throw new Error(msg);
};

console.log('==================================================');
console.log('VALIDATING SPEECH-TO-SIGN ORCHESTRATOR (PHASE G1)');
console.log('==================================================');

class MockPlayer {
  constructor() {
    this.loaded = [];
    this.playing = false;
    this.currentTimeMs = 0;
    this.onCompleteCallback = null;
  }
  loadSign(playable) {
    this.loaded.push(playable.sign_id);
    this.currentTimeMs = 0;
  }
  play() { this.playing = true; }
  pause() { this.playing = false; }
  stop() { this.playing = false; this.currentTimeMs = 0; }
  complete() {
    this.playing = false;
    if (this.onCompleteCallback) this.onCompleteCallback();
  }
}

class MockLibrary {
  constructor(playableSet = new Set(['hello', 'good', 'morning'])) {
    this.playableSet = playableSet;
  }
  getPlayable(id) {
    const norm = String(id).trim().toLowerCase();
    if (norm === 'water') {
      const err = new Error("Sign 'Water' is not playable: MOTION_INCOMPLETE");
      err.code = 'MOTION_INCOMPLETE';
      throw err;
    }
    if (!this.playableSet.has(norm)) {
      const err = new Error(`Sign '${norm}' was not found.`);
      err.code = 'NOT_FOUND';
      throw err;
    }
    return {
      sign_id: norm,
      duration_ms: 1000,
      involved_bones: [],
      keyframes: [],
    };
  }
}

// -------------------------------------------------------------
// TEST 1: Incremental partial evolution without sign duplication
// -------------------------------------------------------------
console.log('--> Test 1: Incremental partial transcript evolution...');
const processor = new SentenceProcessor();
const player1 = new MockPlayer();
const library1 = new MockLibrary();
const scheduler1 = new SignScheduler(player1, library1, new Map());

const orchestrator1 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler1,
  signLibrary: library1,
  minTrailingObservations: 2,
});
orchestrator1.start(1000.0);

// Stream partial 1: "hello"
orchestrator1.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello',
  audio_start_ms: 1000,
  audio_end_ms: 1800,
});
// At partial 1, "hello" is trailing and seen once -> pending confirmation
assert(orchestrator1.committedSigns.length === 0, 'Trailing single partial should wait for stability.');

// Stream partial 2: "hello good"
orchestrator1.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello good',
  audio_start_ms: 1000,
  audio_end_ms: 2500,
});
// "hello" is now followed by "good" (stable prefix) -> commits HELLO!
assert(orchestrator1.committedSigns.length === 1, 'HELLO should commit once followed by GOOD.');
assert(orchestrator1.committedSigns[0].id === 'hello', 'First committed sign must be HELLO.');
assert(scheduler1.getState().current === 'hello', 'HELLO should start playing on Aether.');

// Stream partial 3: "hello good morning"
orchestrator1.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello good morning',
  audio_start_ms: 1000,
  audio_end_ms: 3200,
});
// "good" is now followed by "morning" -> commits GOOD! HELLO must NOT be duplicated.
assert(orchestrator1.committedSigns.length === 2, 'GOOD should commit as stable prefix.');
assert(orchestrator1.committedSigns[1].id === 'good', 'Second committed sign must be GOOD.');
assert(scheduler1.getState().queued.length === 1 && scheduler1.getState().queued[0] === 'good', 'GOOD should enter queue behind active HELLO.');

// Stream final: "hello good morning"
orchestrator1.handleTranscriptEvent({
  kind: 'FINAL_TRANSCRIPT',
  text: 'hello good morning',
  audio_start_ms: 1000,
  audio_end_ms: 3800,
});
// Final confirms MORNING!
assert(orchestrator1.committedSigns.length === 3, 'MORNING should commit upon FINAL_TRANSCRIPT.');
assert(orchestrator1.committedSigns[2].id === 'morning', 'Third committed sign must be MORNING.');

// Verify total signs enqueued
const queuedIds = orchestrator1.committedSigns.map(s => s.id);
assert(JSON.stringify(queuedIds) === JSON.stringify(['hello', 'good', 'morning']), `Expected ['hello', 'good', 'morning'], got ${JSON.stringify(queuedIds)}`);
console.log('PASS: Partial evolution queued HELLO -> GOOD -> MORNING with 0 duplicates.');

// Play through
player1.complete(); // HELLO ends, GOOD starts
assert(scheduler1.getState().current === 'good', 'GOOD should start when HELLO completes.');
player1.complete(); // GOOD ends, MORNING starts
assert(scheduler1.getState().current === 'morning', 'MORNING should start when GOOD completes.');
player1.complete(); // MORNING ends
assert(!scheduler1.getState().current && scheduler1.getState().queued.length === 0, 'Queue should empty cleanly.');

// -------------------------------------------------------------
// TEST 2: Trailing single-word stability
// -------------------------------------------------------------
console.log('--> Test 2: Trailing single-word stability...');
const player2 = new MockPlayer();
const scheduler2 = new SignScheduler(player2, library1, new Map());
const orchestrator2 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler2,
  signLibrary: library1,
  minTrailingObservations: 2,
});
orchestrator2.start();

orchestrator2.handleTranscriptEvent({ kind: 'PARTIAL_TRANSCRIPT', text: 'hello' });
assert(orchestrator2.committedSigns.length === 0, 'First observation of trailing word should not commit prematurely.');
orchestrator2.handleTranscriptEvent({ kind: 'PARTIAL_TRANSCRIPT', text: 'hello' });
assert(orchestrator2.committedSigns.length === 1 && orchestrator2.committedSigns[0].id === 'hello', 'Second consecutive observation must commit trailing word.');
console.log('PASS: Trailing word commits on consecutive observation count.');

// -------------------------------------------------------------
// TEST 3: Unknown words & Incomplete signs (WATER)
// -------------------------------------------------------------
console.log('--> Test 3: Unknown words & MOTION_INCOMPLETE signs...');
const player3 = new MockPlayer();
const scheduler3 = new SignScheduler(player3, library1, new Map());
const orchestrator3 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler3,
  signLibrary: library1,
});
orchestrator3.start();

orchestrator3.handleTranscriptEvent({
  kind: 'FINAL_TRANSCRIPT',
  text: 'hello water mystery good',
});

const diag3 = orchestrator3.getDiagnostics();
assert(diag3.unknownWords.includes('MYSTERY'), 'Unknown word MYSTERY must be reported.');
assert(diag3.unavailableSigns.includes('water'), 'MOTION_INCOMPLETE sign WATER must be reported as unavailable.');
assert(!diag3.committedSignIds.includes('water'), 'WATER must NOT enter playable sign queue.');
assert(!diag3.committedSignIds.includes('mystery'), 'Unknown word must NOT be fabricated as sign.');
assert(JSON.stringify(diag3.committedSignIds) === JSON.stringify(['hello', 'good']), `Expected ['hello', 'good'], got ${JSON.stringify(diag3.committedSignIds)}`);
console.log('PASS: Unknown words and incomplete signs filtered safely without fabrication.');

// -------------------------------------------------------------
// TEST 4: Backpressure diagnostics
// -------------------------------------------------------------
console.log('--> Test 4: Backpressure diagnostics...');
const player4 = new MockPlayer();
const scheduler4 = new SignScheduler(player4, library1, new Map());
const orchestrator4 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler4,
  signLibrary: library1,
});
orchestrator4.start();

orchestrator4.handleTranscriptEvent({
  kind: 'FINAL_TRANSCRIPT',
  text: 'hello good morning',
});
const bpDiag = orchestrator4.getDiagnostics();
assert(bpDiag.currentSign === 'hello', 'HELLO should be active.');
assert(bpDiag.queueCount === 2, 'Queue should have 2 signs waiting.');
assert(bpDiag.oldestQueuedSign === 'good', 'Oldest queued sign should be GOOD.');
assert(typeof bpDiag.queueAgeMs === 'number', 'Queue age must be numeric.');
console.log(`PASS: Backpressure telemetry measured: queue count ${bpDiag.queueCount}, oldest '${bpDiag.oldestQueuedSign}', age ${bpDiag.queueAgeMs} ms.`);

// -------------------------------------------------------------
// TEST 5: Lifecycle (pause, resume, reset)
// -------------------------------------------------------------
console.log('--> Test 5: Lifecycle management...');
orchestrator4.pause();
assert(orchestrator4.state === 'paused', 'Orchestrator should be paused.');
assert(scheduler4.isPaused, 'Scheduler should pause.');
orchestrator4.resume();
assert(orchestrator4.state === 'running', 'Orchestrator should be running.');
orchestrator4.reset();
assert(orchestrator4.state === 'idle', 'Orchestrator should be idle after reset.');
assert(orchestrator4.committedSigns.length === 0, 'Committed signs cleared on reset.');
assert(scheduler4.queue.length === 0 && !scheduler4.currentId, 'Scheduler queue cleared on reset.');
console.log('PASS: Lifecycle pause, resume, reset verified.');

// -------------------------------------------------------------
// TEST 6: End-to-end timing (T0 -> T1 -> T2 -> T3 -> T4)
// -------------------------------------------------------------
console.log('--> Test 6: End-to-end timing instrumentation...');
const player6 = new MockPlayer();
const scheduler6 = new SignScheduler(player6, library1, new Map());
const orchestrator6 = new SpeechSignOrchestrator({
  sentenceProcessor: processor,
  signScheduler: scheduler6,
  signLibrary: library1,
});
const mockT0 = performance.now() - 200.0;
orchestrator6.start(mockT0);

orchestrator6.handleTranscriptEvent({
  kind: 'PARTIAL_TRANSCRIPT',
  text: 'hello good',
  audio_start_ms: mockT0,
});
const timings = orchestrator6.getDiagnostics().timings;
assert(timings.t0 === mockT0, 'T0 audio start mismatch.');
assert(timings.t1 !== null, 'T1 first partial missing.');
assert(timings.t2 !== null, 'T2 first sign commit missing.');
assert(timings.t3 !== null, 'T3 scheduler queue missing.');
assert(timings.t4 !== null, 'T4 playback start missing.');
assert(timings.firstCommitLatencyMs >= 0, 'First commit latency should be positive.');
assert(timings.speechToAetherLatencyMs >= 0, 'Speech-to-Aether latency should be positive.');
console.log(`PASS: Timing recorded: T1-T0=${timings.firstPartialLatencyMs?.toFixed(1)}ms, T2-T0=${timings.firstCommitLatencyMs?.toFixed(1)}ms, T4-T0=${timings.speechToAetherLatencyMs?.toFixed(1)}ms`);

console.log('==================================================');
console.log('ALL SPEECH-TO-SIGN ORCHESTRATOR TESTS PASSED!');
console.log('==================================================');

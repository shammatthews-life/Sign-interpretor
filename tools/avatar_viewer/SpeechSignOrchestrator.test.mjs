import assert from 'node:assert/strict';
import test from 'node:test';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SentenceProcessor } from './SentenceProcessor.js';
import { SignLibrary } from './SignLibrary.js';
import { SignScheduler } from './SignScheduler.js';
import { SpeechSignOrchestrator } from './SpeechSignOrchestrator.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const signIds = ['hello', 'good', 'morning'];

class MockPlayer {
  constructor() {
    this.history = [];
    this.onCompleteCallback = null;
  }
  loadSign(sign) { this.history.push(sign.sign_id); }
  play() {}
  pause() {}
  stop() {}
  complete() { this.onCompleteCallback?.(); }
}

async function createPipeline() {
  const library = new SignLibrary({
    fetchImpl: async url => {
      const definition = JSON.parse(await fs.readFile(path.join(root, 'signs', path.basename(url)), 'utf8'));
      return { ok: true, json: async () => definition };
    }
  });
  const loaded = await library.preload(signIds);
  assert.ok(loaded.every(result => result.status === 'fulfilled'));
  const definitions = await Promise.all(signIds.map(id => fs.readFile(path.join(root, 'signs', `${id}.json`), 'utf8').then(JSON.parse)));
  const bones = new Map(definitions.flatMap(definition => definition.motion.involved_bones).map(name => [name, {}]));
  const player = new MockPlayer();
  const scheduler = new SignScheduler(player, library, bones);
  const orchestrator = new SpeechSignOrchestrator({
    sentenceProcessor: new SentenceProcessor(),
    signScheduler: scheduler,
    signLibrary: library
  });
  orchestrator.start();
  return { library, player, scheduler, orchestrator };
}

test('a single final hello resolves to and starts the playable sign', async () => {
  const { player, scheduler, orchestrator } = await createPipeline();
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello' });

  assert.deepEqual(player.history, ['hello']);
  assert.equal(scheduler.getState().current, 'hello');
  assert.equal(orchestrator.getDiagnostics().committedSignIds[0], 'hello');
});

test('a separate finalized hello can play again after the first completes', async () => {
  const { player, scheduler, orchestrator } = await createPipeline();
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello' });
  player.complete();
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello' });

  assert.deepEqual(player.history, ['hello', 'hello']);
  assert.equal(scheduler.getState().current, 'hello');
});

test('partial transcript followed by its final does not enqueue a duplicate', async () => {
  const { player, scheduler, orchestrator } = await createPipeline();
  orchestrator.handleTranscriptEvent({ kind: 'PARTIAL_TRANSCRIPT', text: 'hello' });
  orchestrator.handleTranscriptEvent({ kind: 'PARTIAL_TRANSCRIPT', text: 'hello' });
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello' });

  assert.deepEqual(player.history, ['hello']);
  assert.deepEqual(scheduler.getState().queued, []);
});

test('good reports its actual technical and linguistic status and remains playable', async () => {
  const { library, player, orchestrator } = await createPipeline();
  const good = await fs.readFile(path.join(root, 'signs', 'good.json'), 'utf8').then(JSON.parse);
  assert.equal(good.motion.status, 'playable');
  assert.equal(good.metadata.technical_animation_status, 'TECHNICALLY_PLAYABLE');
  assert.equal(good.metadata.linguistic_verification_status, 'IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW');
  assert.ok(library.getPlayable('good', new Map(good.motion.involved_bones.map(name => [name, {}]))));

  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'good' });
  assert.deepEqual(player.history, ['good']);
});

test('phrase order is preserved and unsupported words stay visible without fabricated signs', async () => {
  const { player, scheduler, orchestrator } = await createPipeline();
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'hello, good morning' });

  assert.deepEqual(player.history, ['hello']);
  assert.deepEqual(scheduler.getState().queued, ['good', 'morning']);
  assert.deepEqual(orchestrator.getDiagnostics().committedSignIds, ['hello', 'good', 'morning']);
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'mystery' });
  assert.ok(orchestrator.getDiagnostics().unknownWords.includes('MYSTERY'));
  assert.deepEqual(orchestrator.getDiagnostics().committedSignIds, ['hello', 'good', 'morning']);
});

test('empty and unsupported recognition results do not leave scheduler busy', async () => {
  const { scheduler, orchestrator } = await createPipeline();
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: '' });
  orchestrator.handleTranscriptEvent({ kind: 'FINAL_TRANSCRIPT', text: 'unrecognized' });

  assert.equal(scheduler.getState().current, null);
  assert.deepEqual(scheduler.getState().queued, []);
  assert.ok(orchestrator.getDiagnostics().unknownWords.includes('UNRECOGNIZED'));
});

import assert from 'node:assert/strict';
import { test } from 'node:test';
import { SignScheduler } from './SignScheduler.js';
import { SignLibraryError } from './SignLibrary.js';

function harness() {
  const lifecycle = [];
  const player = {
    currentTimeMs: 0,
    onCompleteCallback: null,
    loadSign(sign) { this.loaded = sign; },
    play() { this.playing = true; },
    pause() { this.playing = false; },
    stop() { this.playing = false; }
  };
  const library = {
    getPlayable(id) {
      if (id === 'library-error') throw new SignLibraryError('not playable', 'NOT_FOUND');
      return id === 'missing' ? null : { id };
    }
  };
  const scheduler = new SignScheduler(player, library, new Map(), null, event => lifecycle.push(event));
  return { scheduler, player, lifecycle };
}

test('scheduler validates signs, preserves event identity, and emits accepted/start/end lifecycle', () => {
  const { scheduler, player, lifecycle } = harness();
  assert.deepEqual(scheduler.enqueue('missing', 'bad-event'), {
    accepted: false,
    reason: 'SIGN_NOT_PLAYABLE'
  });
  assert.deepEqual(scheduler.enqueue('library-error', 'missing-event'), {
    accepted: false,
    reason: 'NOT_FOUND'
  });
  assert.deepEqual(scheduler.enqueue('HELLO', 'event-1'), { accepted: true });
  assert.equal(scheduler.currentId, 'hello');
  assert.deepEqual(lifecycle.map(event => [event.type, event.id, event.eventId]), [
    ['accepted', 'hello', 'event-1'],
    ['playback_start', 'hello', 'event-1']
  ]);
  player.onCompleteCallback();
  assert.equal(lifecycle.at(-1).type, 'playback_end');
  assert.equal(lifecycle.at(-1).id, 'hello');
  assert.equal(lifecycle.at(-1).eventId, 'event-1');
  assert.ok(Number.isFinite(lifecycle.at(-1).atMs));
});

test('scheduler bounds queued work and reports cancellation for active and queued occurrences', () => {
  const { scheduler, lifecycle } = harness();
  assert.equal(scheduler.enqueue('hello', 'active').accepted, true);
  for (let index = 0; index < SignScheduler.MAX_QUEUE_SIZE; index += 1) {
    assert.equal(scheduler.enqueue('hello', `queued-${index}`).accepted, true);
  }
  assert.deepEqual(scheduler.enqueue('hello', 'overflow'), {
    accepted: false,
    reason: 'QUEUE_FULL'
  });
  scheduler.cancel();
  const cancelled = lifecycle.filter(event => event.type === 'playback_cancelled');
  assert.equal(cancelled.length, SignScheduler.MAX_QUEUE_SIZE + 1);
  assert.equal(cancelled[0].eventId, 'active');
  assert.equal(cancelled.at(-1).eventId, `queued-${SignScheduler.MAX_QUEUE_SIZE - 1}`);
  assert.equal(scheduler.queue.length, 0);
  assert.equal(scheduler.currentId, null);
});

test('advancing cues preserves active and independent playback but cancels expired cue backlog', () => {
  const { scheduler, player, lifecycle } = harness();
  scheduler.enqueue('hello', 'current', 'cue-one', 'job-a');
  scheduler.enqueue('hello', 'old-queued', 'cue-one', 'job-a');
  scheduler.enqueue('hello', 'other-job', 'cue-one', 'job-b');
  scheduler.enqueue('hello', 'manual', null, null);

  scheduler.advanceCue('job-a', 'cue-two');
  assert.equal(scheduler.currentId, 'hello');
  assert.deepEqual(scheduler.queue.map(item => item.eventId), ['manual']);
  assert.ok(lifecycle.some(event => event.eventId === 'old-queued' && event.type === 'playback_cancelled'));
  assert.ok(lifecycle.some(event => event.eventId === 'other-job' && event.type === 'playback_cancelled'));

  player.onCompleteCallback();
  assert.equal(scheduler.currentEntry.eventId, 'manual');
});

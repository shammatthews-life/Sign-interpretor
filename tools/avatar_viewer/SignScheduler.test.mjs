import assert from 'node:assert/strict';
import { test } from 'node:test';
import { SignScheduler } from './SignScheduler.js';
import { SignLibraryError } from './SignLibrary.js';

function harness() {
  const lifecycle = [];
  const player = {
    currentTimeMs: 0,
    onCompleteCallback: null,
    loadSign(sign) {
      if (sign.id === 'fails_on_load') throw new Error('test load failure');
      this.loaded = sign;
    },
    play() { this.playing = true; },
    pause() { this.playing = false; },
    stop() { this.playing = false; }
  };
  const library = {
    getPlayable(id) {
      if (id === 'library_error') throw new SignLibraryError('not playable', 'NOT_FOUND');
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
  assert.deepEqual(scheduler.enqueue('library_error', 'missing-event'), {
    accepted: false,
    reason: 'NOT_FOUND'
  });
  assert.deepEqual(scheduler.enqueue('HELLO', 'event-1'), { accepted: true });
  assert.equal(scheduler.currentId, 'hello');
  assert.deepEqual(lifecycle.filter(event => event.eventId === 'event-1').map(event => [event.type, event.id, event.eventId]), [
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
  assert.deepEqual(scheduler.queue.map(item => item.eventId), ['other-job', 'manual']);
  assert.ok(lifecycle.some(event => event.eventId === 'old-queued' && event.type === 'playback_cancelled'));
  assert.ok(!lifecycle.some(event => event.eventId === 'other-job' && event.type === 'playback_cancelled'));

  player.onCompleteCallback();
  assert.equal(scheduler.currentEntry.eventId, 'other-job');
  player.onCompleteCallback();
  assert.equal(scheduler.currentEntry.eventId, 'manual');
});

test('duplicate event IDs acknowledge again without enqueueing or replaying a sign', () => {
  const { scheduler, player, lifecycle } = harness();
  assert.equal(scheduler.enqueue('hello', 'same-event', 'cue-1', 'job-1').accepted, true);
  assert.deepEqual(scheduler.enqueue('hello', 'same-event', 'cue-1', 'job-1'), {
    accepted: true,
    duplicate: true
  });
  assert.equal(lifecycle.filter(event => event.type === 'accepted').length, 1);
  assert.equal(lifecycle.filter(event => event.type === 'playback_start').length, 1);
  assert.equal(scheduler.enqueue('water', 'same-event', 'cue-1', 'job-1').reason, 'EVENT_ID_CONFLICT');
  player.onCompleteCallback();
  assert.equal(lifecycle.filter(event => event.type === 'playback_end').length, 1);
});

test('plays the requested five-sign sequence once and only advances after completion', () => {
  const { scheduler, player, lifecycle } = harness();
  const sequence = ['hello', 'good', 'morning', 'water', 'thank_you'];
  sequence.forEach((signId, index) => {
    scheduler.enqueue(signId, `seq-${index}`, 'cue-1', 'job-1');
    if (index < sequence.length - 1) {
      assert.equal(scheduler.currentId, 'hello');
      assert.equal(lifecycle.filter(event => event.type === 'playback_start').length, 1);
    }
  });
  const started = [];
  while (scheduler.currentEntry) {
    started.push(scheduler.currentId);
    player.onCompleteCallback();
  }
  assert.deepEqual(started, sequence);
  assert.deepEqual(
    lifecycle.filter(event => event.type === 'playback_end').map(event => event.id),
    sequence
  );
  assert.equal(new Set(lifecycle.filter(event => event.type === 'playback_start').map(event => event.eventId)).size, 5);
});

test('job cancellation removes only that job and leaves unrelated and manual playback intact', () => {
  const { scheduler, player, lifecycle } = harness();
  scheduler.enqueue('hello', 'job-a-active', 'cue-a', 'job-a');
  scheduler.enqueue('good', 'job-a-queued', 'cue-a', 'job-a');
  scheduler.enqueue('water', 'job-b-queued', 'cue-b', 'job-b');
  scheduler.enqueue('morning', 'manual-queued');

  assert.equal(scheduler.cancelJob('job-a'), 2);
  assert.equal(scheduler.currentId, 'water');
  assert.deepEqual(scheduler.queue.map(item => item.eventId), ['manual-queued']);
  assert.deepEqual(
    lifecycle.filter(event => event.type === 'playback_cancelled').map(event => event.eventId),
    ['job-a-queued', 'job-a-active']
  );
  player.onCompleteCallback();
  assert.equal(scheduler.currentId, 'morning');
});

test('playback setup failure emits failure and advances the queue', () => {
  const { scheduler, lifecycle } = harness();
  scheduler.enqueue('fails_on_load', 'fails', 'cue-1', 'job-1');
  scheduler.enqueue('hello', 'next', 'cue-1', 'job-1');
  assert.equal(scheduler.currentEntry.eventId, 'next');
  assert.ok(lifecycle.some(event => event.eventId === 'fails' && event.type === 'playback_failed'));
  assert.ok(lifecycle.some(event => event.eventId === 'next' && event.type === 'playback_start'));
});

test('an unavailable sign is rejected without blocking a later playable occurrence', () => {
  const { scheduler, lifecycle } = harness();
  assert.deepEqual(scheduler.enqueue('missing', 'missing-word', 'cue-1', 'job-1'), {
    accepted: false,
    reason: 'SIGN_NOT_PLAYABLE'
  });
  scheduler.enqueue('water', 'next-playable', 'cue-1', 'job-1');
  assert.equal(scheduler.currentId, 'water');
  assert.ok(lifecycle.some(event => event.type === 'playback_rejected'
    && event.eventId === 'missing-word' && event.reason === 'SIGN_NOT_PLAYABLE'));
  assert.ok(lifecycle.some(event => event.type === 'playback_start' && event.eventId === 'next-playable'));
});

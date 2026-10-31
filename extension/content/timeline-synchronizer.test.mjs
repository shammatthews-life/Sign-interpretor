import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';

const require = createRequire(import.meta.url);
const { YouTubeTimelineSynchronizer } = require('./timeline-synchronizer.js');

class FakeVideo {
  constructor(currentTime = 0, playbackRate = 1) {
    this.currentTime = currentTime;
    this.playbackRate = playbackRate;
    this.paused = true;
    this.listeners = new Map();
  }
  addEventListener(type, handler) {
    if (!this.listeners.has(type)) this.listeners.set(type, new Set());
    this.listeners.get(type).add(handler);
  }
  removeEventListener(type, handler) { this.listeners.get(type)?.delete(handler); }
  emit(type) { for (const handler of this.listeners.get(type) || []) handler(); }
  listenerCount() { return [...this.listeners.values()].reduce((sum, listeners) => sum + listeners.size, 0); }
}

function harness(video = new FakeVideo()) {
  const events = [];
  const synchronizer = new YouTubeTimelineSynchronizer({
    videoElement: video,
    onDispatchSign: (signId, metadata) => events.push(['sign', signId, metadata]),
    onDispatchCommand: (command, payload) => events.push(['command', command, payload]),
    onFallback: text => events.push(['fallback', text]),
    onClearFallback: () => events.push(['clear'])
  });
  events.length = 0;
  return { video, synchronizer, events };
}

const cue = (id, start, end, extra = {}) => ({
  id, start, end, signIds: [], fallbackWords: [], ...extra
});

test('activates only the current cue once and preserves repeated sign occurrence identities', () => {
  const { video, synchronizer, events } = harness(new FakeVideo(1));
  synchronizer.setSegments([
    cue('first', 0, 2, {
      signIds: ['good', 'good'],
      signOccurrences: [{ occurrence_id: 'first:0' }, { occurrence_id: 'first:1' }]
    }),
    cue('fallback', 2, 4, {
      fallbackWords: ['UNKNOWN'],
      fallbackMessage: 'Sign not available for: UNKNOWN. Original text: unknown.'
    })
  ], 'job-a');
  video.paused = false;
  video.emit('timeupdate');
  video.emit('timeupdate');
  const firstDelivery = events.filter(event => event[0] === 'sign');
  assert.deepEqual(firstDelivery.map(event => [event[1], event[2].command]), [
    ['good', 'QUEUE_SIGN'],
    ['good', 'QUEUE_SIGN']
  ]);
  assert.ok(firstDelivery[0][2].eventId.endsWith('first:0'));
  assert.ok(firstDelivery[1][2].eventId.endsWith('first:1'));
  video.currentTime = 2;
  video.emit('timeupdate');
  assert.ok(events.some(event => event[0] === 'fallback' && event[1].includes('not available')));
  assert.equal(events.filter(event => event[0] === 'sign').length, 2);
  assert.ok(events.some(event => event[0] === 'command' && event[1] === 'CUE_TRANSITION'
    && event[2].cueId === 'fallback'));
  video.currentTime = 4;
  video.emit('timeupdate');
  assert.equal(synchronizer.activeCueId, null);
  assert.ok(events.some(event => event[0] === 'command' && event[1] === 'CUE_TRANSITION'
    && event[2].cueId === null));
});

test('seeking back into a cue creates a fresh delivery identity for replay', () => {
  const { video, synchronizer, events } = harness(new FakeVideo(1));
  synchronizer.setSegments([cue('repeatable', 0, 5, {
    signIds: ['hello'],
    signOccurrences: [{ occurrence_id: 'hello-occurrence' }]
  })], 'job-replay');
  video.paused = false;
  video.emit('timeupdate');
  const firstEventId = events.find(event => event[0] === 'sign')[2].eventId;
  video.emit('seeking');
  video.emit('seeked');
  const deliveries = events.filter(event => event[0] === 'sign');
  assert.equal(deliveries.length, 2);
  assert.notEqual(deliveries[0][2].eventId, deliveries[1][2].eventId);
  assert.ok(deliveries[1][2].eventId.includes('hello-occurrence'));
  assert.ok(firstEventId.includes('hello-occurrence'));
});

test('installing cues evaluates the current video time and queues signs without cancelling prior cues', () => {
  const { video, synchronizer, events } = harness(new FakeVideo(1));
  video.paused = false;
  synchronizer.setSegments([
    cue('first', 0, 2, { signIds: ['hello'] }),
    cue('second', 2, 4, { signIds: ['good'] })
  ], 'job-immediate');
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
  events.length = 0;
  video.currentTime = 2.5;
  video.emit('timeupdate');
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
  assert.equal(events.some(event => event[0] === 'command' && event[1] === 'RESET_AVATAR'), false);
  assert.equal(events.find(event => event[0] === 'sign')[1], 'good');
});

test('rejects overlaps and invalid cue ordering instead of sorting timestamped cues', () => {
  const { synchronizer } = harness();
  assert.throws(() => synchronizer.setSegments([
    cue('later', 2, 4),
    cue('overlap', 3, 5)
  ]), /order or overlap/);
  assert.throws(() => synchronizer.setSegments([
    cue('first', 2, 4),
    cue('earlier', 1, 2)
  ]), /order or overlap/);
  assert.throws(() => synchronizer.setSegments([cue('bad', 1, 1)]), /Invalid timestamped cue/);
});

test('seek cancels stale playback and activates only the destination cue or fallback', () => {
  const { video, synchronizer, events } = harness(new FakeVideo(1));
  synchronizer.setSegments([
    cue('one', 0, 2, { signIds: ['hello'] }),
    cue('two', 2, 4, { signIds: ['good'] }),
    cue('unknown', 5, 7, { fallbackWords: ['UNKNOWN'], source_text: 'unknown word' })
  ], 'job-seek');
  video.paused = false;
  video.emit('seeked');
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
  events.length = 0;
  video.emit('seeking');
  video.currentTime = 5.5;
  assert.ok(events.some(event => event[0] === 'command' && event[1] === 'RESET_AVATAR'));
  video.emit('seeked');
  assert.equal(events.filter(event => event[0] === 'sign').length, 0);
  assert.ok(events.some(event => event[0] === 'fallback' && event[1].includes('UNKNOWN')));
  events.length = 0;
  video.emit('seeking');
  video.currentTime = 4.5;
  video.emit('seeked');
  assert.equal(synchronizer.activeCueId, null);
  assert.ok(events.some(event => event[0] === 'clear'));
});

test('pause, resume and playback-rate payloads are forwarded without replaying an active cue', () => {
  const { video, synchronizer, events } = harness(new FakeVideo(1, 1));
  synchronizer.setSegments([cue('one', 0, 5, { signIds: ['hello'] })], 'job-rate');
  video.paused = false;
  video.emit('play');
  video.emit('play');
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
  video.emit('pause');
  for (const rate of [0.5, 0.75, 1, 1.25, 1.5, 2]) {
    video.playbackRate = rate;
    video.emit('ratechange');
  }
  assert.deepEqual(
    events.filter(event => event[0] === 'command' && event[1] === 'SET_PLAYBACK_RATE').map(event => event[2].rate),
    [0.5, 0.75, 1, 1.25, 1.5, 2]
  );
  assert.ok(events.some(event => event[0] === 'command' && event[1] === 'PAUSE'));
  assert.ok(events.some(event => event[0] === 'command' && event[1] === 'RESUME'));
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
});

test('rebind removes old listeners and follows only the replacement video clock', () => {
  const first = new FakeVideo(1);
  const { synchronizer, events } = harness(first);
  synchronizer.setSegments([cue('one', 0, 2, { signIds: ['hello'] })], 'job-rebind');
  first.paused = false;
  first.emit('timeupdate');
  const second = new FakeVideo(1.5);
  second.paused = false;
  events.length = 0;
  synchronizer.rebind(second);
  assert.equal(first.listenerCount(), 0);
  assert.equal(second.listenerCount(), 9);
  first.currentTime = 3;
  first.emit('timeupdate');
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
  second.emit('timeupdate');
  assert.equal(events.filter(event => event[0] === 'sign').length, 1);
  synchronizer.detach();
  assert.equal(second.listenerCount(), 0);
});

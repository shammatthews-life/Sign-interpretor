import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';

const require = createRequire(import.meta.url);
const { AetherPlaybackLedger, validateLifecycleEvent } = require('./aether-playback.js');

function event(type, overrides = {}) {
  return {
    type,
    id: 'hello',
    eventId: 'job-1:cue-1:hello-0',
    jobId: 'job-1',
    cueId: 'cue-1',
    atMs: 100,
    ...overrides
  };
}

test('validates required occurrence, job, cue, and timestamp fields', () => {
  assert.equal(validateLifecycleEvent(event('accepted')).valid, true);
  assert.equal(validateLifecycleEvent(event('playback_start', { jobId: null })).valid, false);
  assert.equal(validateLifecycleEvent(event('accepted', { cueId: null })).valid, true);
  assert.equal(validateLifecycleEvent(event('unknown')).valid, false);
  assert.equal(validateLifecycleEvent(event('accepted', { eventId: '' })).valid, false);
  assert.equal(validateLifecycleEvent(event('accepted', { atMs: NaN })).valid, false);
});

test('tracks exactly one accepted, started, and completed lifecycle per occurrence', () => {
  const ledger = new AetherPlaybackLedger();
  assert.equal(ledger.record(event('accepted'), 'tab-1').accepted, true);
  assert.equal(ledger.record(event('accepted'), 'tab-1').duplicate, true);
  assert.equal(ledger.record(event('playback_start'), 'tab-1').accepted, true);
  assert.equal(ledger.record(event('playback_end'), 'tab-1').accepted, true);
  assert.equal(ledger.record(event('playback_end'), 'tab-1').duplicate, true);
  assert.equal(ledger.get('job-1:cue-1:hello-0', 'tab-1').status, 'playback_end');
  assert.equal(ledger.record(event('playback_start'), 'tab-1').duplicate, true);
});

test('rejects event ID identity conflicts and isolates separate tabs', () => {
  const ledger = new AetherPlaybackLedger();
  ledger.record(event('accepted'), 'tab-1');
  assert.equal(ledger.record(event('accepted', { id: 'water' }), 'tab-1').valid, false);
  assert.equal(ledger.record(event('accepted'), 'tab-2').accepted, true);
  assert.equal(ledger.get('job-1:cue-1:hello-0', 'tab-1').status, 'accepted');
  assert.equal(ledger.get('job-1:cue-1:hello-0', 'tab-2').status, 'accepted');
});

test('allows cancellation and failure only before terminal completion', () => {
  const ledger = new AetherPlaybackLedger();
  ledger.record(event('accepted'), 'tab-1');
  assert.equal(ledger.record(event('playback_cancelled'), 'tab-1').accepted, true);
  assert.equal(ledger.record(event('playback_failed'), 'tab-1').valid, false);

  const failed = new AetherPlaybackLedger();
  failed.record(event('accepted'), 'tab-1');
  failed.record(event('playback_start'), 'tab-1');
  assert.equal(failed.record(event('playback_failed'), 'tab-1').accepted, true);

  const timedOut = new AetherPlaybackLedger();
  timedOut.record(event('accepted'), 'tab-1');
  assert.equal(timedOut.record(event('playback_timeout'), 'tab-1').accepted, true);
  assert.equal(timedOut.record(event('playback_cancelled'), 'tab-1').accepted, true);
});

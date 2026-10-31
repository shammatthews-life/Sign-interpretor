import assert from 'node:assert/strict';
import { test } from 'node:test';
import { takePendingAetherEvent } from './PendingAetherQueue.js';

test('cancels only the targeted command waiting for viewer startup', () => {
  const expired = { data: { eventId: 'expired', jobId: 'job-1' }, event: {} };
  const current = { data: { eventId: 'current', jobId: 'job-2' }, event: {} };
  const pendingEvents = new Map([
    ['expired', expired],
    ['current', current]
  ]);

  assert.equal(takePendingAetherEvent(pendingEvents, 'expired'), expired);
  assert.equal(pendingEvents.has('expired'), false);
  assert.equal(pendingEvents.get('current'), current);
  assert.equal(takePendingAetherEvent(pendingEvents, 'missing'), null);
});

import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';

const require = createRequire(import.meta.url);
const contract = require('./message-contract.js');

test('creates unique secure event IDs for manually requested sign playback', () => {
  const first = contract.createEventId();
  const second = contract.createEventId();
  assert.match(first, /^isl-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i);
  assert.notEqual(first, second);
});

test('adds event IDs to PLAY_SIGN and QUEUE_SIGN commands without replacing supplied IDs', () => {
  for (const command of [contract.AETHER_COMMANDS.PLAY_SIGN, contract.AETHER_COMMANDS.QUEUE_SIGN]) {
    const result = contract.ensureAetherEventId({ command, signId: 'hello' });
    assert.match(result.eventId, /^isl-[0-9a-f-]{36}$/i);
    assert.equal(result.signId, 'hello');
  }

  const existing = { command: contract.AETHER_COMMANDS.PLAY_SIGN, signId: 'hello', eventId: 'stable-id' };
  assert.equal(contract.ensureAetherEventId(existing), existing);
});

test('does not add sign event IDs to non-sign commands and rejects malformed payloads', () => {
  const pause = { command: 'PAUSE' };
  assert.equal(contract.ensureAetherEventId(pause), pause);
  assert.throws(() => contract.ensureAetherEventId(null), /payload must be an object/);
  assert.throws(() => contract.ensureAetherEventId([]), /payload must be an object/);
});

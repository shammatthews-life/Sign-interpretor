import assert from 'node:assert/strict';
import { test } from 'node:test';
import { SignLibrary } from './SignLibrary.js';

function definition(signId) {
  return {
    schema_version: '2.0.0',
    sign_id: signId,
    metadata: {
      gloss: signId.toUpperCase(),
      display_name: signId
    },
    motion: { status: 'unavailable' }
  };
}

test('preload limits concurrent fetches, preserves order, and reports individual failures', async () => {
  let activeRequests = 0;
  let maximumActiveRequests = 0;
  const library = new SignLibrary({
    fetchImpl: async url => {
      const signId = url.split('/').at(-1).replace(/\.json$/, '');
      activeRequests += 1;
      maximumActiveRequests = Math.max(maximumActiveRequests, activeRequests);
      await new Promise(resolve => setTimeout(resolve, 2));
      activeRequests -= 1;
      if (signId === 'sign_9') throw new Error('temporary fetch failure');
      return {
        ok: true,
        json: async () => definition(signId)
      };
    }
  });
  const ids = Array.from({ length: 20 }, (_, index) => `sign_${index}`);

  const results = await library.preload(ids);

  assert.ok(maximumActiveRequests > 1);
  assert.ok(maximumActiveRequests <= SignLibrary.MAX_PRELOAD_CONCURRENCY);
  assert.deepEqual(results.map(result => result.id), ids);
  assert.equal(results.filter(result => result.status === 'fulfilled').length, 19);
  assert.equal(results[9].status, 'rejected');
  assert.equal(results[9].reason.code, 'LOAD_FAILED');
  assert.equal(library.cache.size, 19);
});

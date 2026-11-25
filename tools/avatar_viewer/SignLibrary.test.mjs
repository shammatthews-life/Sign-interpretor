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


test('SignLibrary preloadBundle caches bundled signs and synthesizes fs_<word> fingerspelling', async () => {
  const sampleDef = {
    schema_version: '2.0.0',
    sign_id: 'hello',
    metadata: { display_name: 'Hello', gloss: 'HELLO', language: 'ISL' },
    motion: {
      status: 'playable',
      duration_ms: 800,
      dominant_hand: 'right',
      return_to_neutral: true,
      involved_bones: ['mixamorigRightArm'],
      keyframes: [
        { time_ms: 0, rotations: {} },
        { time_ms: 800, rotations: {} }
      ]
    }
  };
  let requestedUrls = [];
  const library = new SignLibrary({
    basePath: '/signs',
    fetchImpl: async url => {
      requestedUrls.push(url);
      if (url.endsWith('/bundle.json')) {
        return {
          ok: true,
          async json() {
            return { signs: { hello: sampleDef } };
          }
        };
      }
      return { ok: false, async json() { return {}; } };
    }
  });

  const summary = await library.preloadBundle();
  assert.equal(summary.source, 'bundle');
  assert.equal(summary.loaded, 1);
  assert.equal(requestedUrls.includes('/signs/bundle.json'), true);

  const boneNames = [
    'Bip001_R_Clavicle', 'Bip001_R_UpperArm', 'Bip001_R_Forearm', 'Bip001_R_Hand',
    'Bip001_L_Clavicle', 'Bip001_L_UpperArm', 'Bip001_L_Forearm', 'Bip001_L_Hand',
    'Bip001_Head'
  ];
  const bonesMap = new Map(boneNames.map(name => [name, { name }]));
  const playableFs = library.getPlayable('fs_ai', bonesMap);
  assert.equal(playableFs.sign_id, 'fs_ai');
  assert.ok(playableFs.keyframes.length >= 2);
});

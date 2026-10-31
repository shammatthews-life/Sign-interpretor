import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const require = createRequire(import.meta.url);
const contract = require('../shared/message-contract.js');
const videoId = 'MXKkXXYUxBc';
const tab = { id: 7, url: `https://www.youtube.com/watch?v=${videoId}` };
const manifest = {
  schema_version: '1.0.0',
  job_id: 'job-1',
  video_id: videoId,
  fingerprint: 'sha256:test',
  playback_ready: true,
  cue_count: 0,
  cues: []
};

function createHarness() {
  const stored = {};
  const tabMessages = [];
  let onMessage;
  let onStateUpdate;
  let bridgeInstance;
  class RuntimeBridge {
    constructor(options) {
      bridgeInstance = this;
      this.state = contract.createInitialState();
      onStateUpdate = options.onStateUpdate;
      this.trackedJobs = [];
      this.jobCount = 0;
    }
    getState() { return JSON.parse(JSON.stringify(this.state)); }
    async submitYouTube(url) {
      const validated = contract.validateYouTubeUrl(url);
      this.jobCount += 1;
      const jobId = `job-${this.jobCount}`;
      this.state.youtube = {
        ...this.state.youtube,
        jobId,
        videoId: validated.videoId,
        state: 'QUEUED'
      };
      onStateUpdate(this.getState());
      return { job_id: jobId, state: 'QUEUED' };
    }
    trackYouTubeJob(jobId) {
      if (!this.trackedJobs.includes(jobId)) this.trackedJobs.push(jobId);
    }
    async getYouTubeCueManifest(jobId, expectedVideoId) {
      if (jobId !== manifest.job_id || expectedVideoId !== manifest.video_id) {
        throw new Error('Mismatched test manifest identity.');
      }
      return manifest;
    }
    setYouTubeError() {}
    pingRuntime() {}
    disconnectRuntime() {}
    updateAetherPlayback() {}
    startDemo() {}
    stepDemo() {}
    stopDemo() {}
    toggleOverlay() { return true; }
    setOverlayVisible() {}
  }

  const chrome = {
    runtime: {
      lastError: null,
      onInstalled: { addListener() {} },
      onMessage: { addListener(listener) { onMessage = listener; } },
      sendMessage(_message, callback) { callback?.(); }
    },
    storage: {
      local: {
        get(keys, callback) {
          callback(Object.fromEntries(keys.filter(key => key in stored).map(key => [key, stored[key]])));
        },
        set(value, callback) {
          Object.assign(stored, value);
          callback();
        }
      }
    },
    tabs: {
      query(_query, callback) { callback([]); },
      get(tabId, callback) { callback(tabId === tab.id ? tab : null); },
      sendMessage(tabId, message, callback) {
        tabMessages.push({ tabId, message });
        callback({ received: true });
      }
    }
  };
  const context = {
    chrome,
    console,
    setTimeout,
    URL,
    importScripts() {},
    ISLMessageContract: contract,
    ISLRuntimeBridge: { RuntimeBridge },
    ISLDemoData: {},
    ISLYouTubeCueManifest: {},
    broadcast: null
  };
  context.self = context;
  vm.runInNewContext(
    require('node:fs').readFileSync(new URL('./service-worker.js', import.meta.url), 'utf8'),
    context,
    { filename: 'service-worker.js' }
  );

  function dispatch(type, payload, sender = { tab }) {
    return new Promise(resolve => {
      const keepChannelOpen = onMessage(contract.createMessage(type, payload), sender, resolve);
      if (keepChannelOpen !== true) resolve(undefined);
    });
  }

  return {
    dispatch,
    tabMessages,
    get trackedJobs() {
      return bridgeInstance.trackedJobs;
    },
    setReadyState() {
      bridgeInstance.state.youtube.state = 'READY';
      bridgeInstance.state.youtube.cueManifestFingerprint = manifest.fingerprint;
      onStateUpdate(bridgeInstance.getState());
    }
  };
}

test('service worker delivers fingerprinted cues only to the matching video job and tab', async () => {
  const harness = createHarness();
  const created = await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PROCESS, {
    url: `https://www.youtube.com/watch?v=${videoId}`
  });
  assert.equal(created.success, true);
  assert.equal(created.payload.job_id, manifest.job_id);

  const pageReady = await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PAGE_READY, {
    protocol_version: 1,
    video_id: videoId
  });
  assert.equal(pageReady.success, true);
  assert.equal(pageReady.job_id, manifest.job_id);
  assert.deepEqual(harness.trackedJobs, [manifest.job_id]);

  harness.setReadyState();
  await new Promise(resolve => setTimeout(resolve, 0));
  assert.ok(harness.tabMessages.some(({ tabId, message }) =>
    tabId === tab.id && message.type === contract.MESSAGE_TYPES.YOUTUBE_CUES_READY
  ));

  const wrongPage = await harness.dispatch(contract.MESSAGE_TYPES.GET_YOUTUBE_CUES, {
    job_id: manifest.job_id,
    video_id: 'aaaaaaaaaaa'
  });
  assert.equal(wrongPage.success, false);

  const delivered = await harness.dispatch(contract.MESSAGE_TYPES.GET_YOUTUBE_CUES, {
    job_id: manifest.job_id,
    video_id: videoId
  });
  assert.equal(delivered.success, true);
  assert.equal(delivered.fingerprint, manifest.fingerprint);
  assert.equal(delivered.payload.job_id, manifest.job_id);

  const ack = await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_CUES_ACK, {
    job_id: manifest.job_id,
    video_id: videoId,
    fingerprint: manifest.fingerprint
  });
  assert.equal(ack.success, true);
  assert.equal(ack.acknowledged, true);

  const newer = await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PROCESS, {
    url: `https://www.youtube.com/watch?v=${videoId}`
  });
  assert.equal(newer.payload.job_id, 'job-2');
  const stale = await harness.dispatch(contract.MESSAGE_TYPES.GET_YOUTUBE_CUES, {
    job_id: manifest.job_id,
    video_id: videoId
  });
  assert.equal(stale.success, false);
  assert.match(stale.error, /superseded/);
});

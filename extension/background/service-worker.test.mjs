import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const require = createRequire(import.meta.url);
const contract = require('../shared/message-contract.js');
const playback = require('../shared/aether-playback.js');
const videoId = 'MXKkXXYUxBc';
const tab = { id: 7, url: `https://www.youtube.com/watch?v=${videoId}` };
const otherTab = { id: 8, url: `https://www.youtube.com/watch?v=${videoId}` };
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
  const storedSession = {};
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
      onSuspend: { addListener() {} },
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
      },
      session: {
        get(keys, callback) {
          callback(Object.fromEntries(keys.filter(key => key in storedSession)
            .map(key => [key, structuredClone(storedSession[key])])));
        },
        set(value, callback) {
          for (const [key, item] of Object.entries(value)) storedSession[key] = structuredClone(item);
          callback();
        }
      }
    },
    tabs: {
      onRemoved: { addListener() {} },
      query(_query, callback) { callback([]); },
      get(tabId, callback) { callback(tabId === tab.id ? tab : null); },
      sendMessage(tabId, message, callback) {
        tabMessages.push({ tabId, message });
        callback({ received: true });
      }
    }
  };
  const workerSource = require('node:fs').readFileSync(new URL('./service-worker.js', import.meta.url), 'utf8');
  function startServiceWorker() {
    const context = {
      chrome,
      console,
      setTimeout,
      URL,
      importScripts() {},
      ISLMessageContract: contract,
      ISLAetherPlayback: playback,
      ISLRuntimeBridge: { RuntimeBridge },
      ISLDemoData: {},
      ISLYouTubeCueManifest: {},
      broadcast: null
    };
    context.self = context;
    vm.runInNewContext(workerSource, context, { filename: 'service-worker.js' });
  }
  startServiceWorker();

  function dispatch(type, payload, sender = { tab }) {
    return new Promise(resolve => {
      const keepChannelOpen = onMessage(contract.createMessage(type, payload), sender, resolve);
      if (keepChannelOpen !== true) resolve(undefined);
    });
  }

  return {
    dispatch,
    tabMessages,
    restart: startServiceWorker,
    dispatchFrom(type, payload, sender) {
      return new Promise(resolve => {
        const keepChannelOpen = onMessage(contract.createMessage(type, payload), sender, resolve);
        if (keepChannelOpen !== true) resolve(undefined);
      });
    },
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
  assert.equal(pageReady.associated, true);
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

  test('playback lifecycle is validated, sequenced, and isolated to the owning YouTube tab', async () => {
    const harness = createHarness();
    const created = await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PROCESS, {
      url: `https://www.youtube.com/watch?v=${videoId}`
    });
    assert.equal(created.success, true);

    const otherPageReady = await harness.dispatchFrom(
      contract.MESSAGE_TYPES.YOUTUBE_PAGE_READY,
      { protocol_version: 1, video_id: videoId },
      { tab: otherTab }
    );
    assert.equal(otherPageReady.associated, false);
    const otherTabCueRequest = await harness.dispatchFrom(
      contract.MESSAGE_TYPES.GET_YOUTUBE_CUES,
      {
        job_id: created.payload.job_id,
        video_id: videoId
      },
      { tab: otherTab }
    );
    assert.equal(otherTabCueRequest.success, false);

    const commandWrongTab = await harness.dispatchFrom(
      contract.MESSAGE_TYPES.AETHER_COMMAND,
      {
        command: contract.AETHER_COMMANDS.QUEUE_SIGN,
        signId: 'hello',
        jobId: created.payload.job_id,
        cueId: 'cue-1',
        eventId: 'wrong-tab-command'
      },
      { tab: otherTab }
    );
    assert.equal(commandWrongTab.success, false);

    const base = {
      protocol_version: 1,
      video_id: videoId,
      job_id: created.payload.job_id,
      cue_id: 'cue-1',
      event_id: 'sequence-hello',
      sign_id: 'hello',
      at_ms: 100,
      video_time_seconds: 1.1,
      video_paused: false,
      playback_rate: 1,
      cue_start_seconds: 1,
      cue_end_seconds: 3,
      timing_error_ms: null
    };
    const wrongTab = await harness.dispatchFrom(
      contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE,
      { ...base, event_type: 'accepted' },
      { tab: otherTab }
    );
    assert.equal(wrongTab.success, false);

    await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PAGE_READY, {
      protocol_version: 1,
      video_id: videoId
    });

    test('service worker routes only valid Aether commands back to their YouTube tab', async () => {
      const harness = createHarness();
      const valid = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_COMMAND, {
        command: contract.AETHER_COMMANDS.QUEUE_SIGN,
        signId: 'hello',
        eventId: 'manual-hello'
      });
      assert.equal(valid.success, true);
      assert.equal(valid.tab_id, tab.id);
      const delivered = harness.tabMessages.at(-1);
      assert.equal(delivered.tabId, tab.id);
      assert.equal(delivered.message.type, contract.MESSAGE_TYPES.AETHER_COMMAND);
      assert.equal(delivered.message.payload.eventId, 'manual-hello');

      const missingEvent = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_COMMAND, {
        command: contract.AETHER_COMMANDS.QUEUE_SIGN,
        signId: 'good'
      });
      assert.equal(missingEvent.success, false);
      const invalidCue = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_COMMAND, {
        command: contract.AETHER_COMMANDS.CUE_TRANSITION,
        jobId: 'job-unknown',
        eventId: 'cue-transition-no-cue'
      });
      assert.equal(invalidCue.success, false);
      const unknown = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_COMMAND, {
        command: 'INJECT_SCRIPT'
      });
      assert.equal(unknown.success, false);
    });
    const accepted = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...base,
      event_type: 'accepted'
    });
    const started = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...base,
      at_ms: 200,
      timing_error_ms: 100,
      event_type: 'playback_start'
    });
    const completed = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...base,
      at_ms: 2100,
      video_time_seconds: 2.9,
      timing_error_ms: -100,
      event_type: 'playback_end'
    });
    assert.equal(accepted.accepted, true);
    assert.equal(started.status, 'playback_start');
    assert.equal(completed.status, 'playback_end');
    assert.equal(completed.timing_error_ms, -100);
    assert.equal((await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...base,
      at_ms: 2100,
      video_time_seconds: 2.9,
      timing_error_ms: -100,
      event_type: 'playback_end'
    })).duplicate, true);

    const outOfOrder = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...base,
      event_id: 'sequence-water',
      event_type: 'playback_end'
    });
    assert.equal(outOfOrder.success, false);
    const malformed = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...base,
      event_id: 'sequence-invalid',
      event_type: 'accepted',
      cue_id: 'cue-without-job',
      job_id: null
    });
    assert.equal(malformed.success, false);
  });

  test('playback state snapshots are stored per YouTube tab and reject mismatched video IDs', async () => {
    const harness = createHarness();
    const first = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      kind: 'snapshot',
      video_id: videoId,
      state: { current: 'hello', queued: ['good'], currentTimeMs: 200 }
    });
    const second = await harness.dispatchFrom(
      contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE,
      {
        kind: 'snapshot',
        video_id: videoId,
        state: { current: 'water', queued: [], currentTimeMs: 50 }
      },
      { tab: otherTab }
    );
    assert.equal(first.tab_id, tab.id);
    assert.equal(second.tab_id, otherTab.id);

    const mismatch = await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      kind: 'snapshot',
      video_id: 'aaaaaaaaaaa',
      state: { current: null, queued: [] }
    });
    assert.equal(mismatch.success, false);
  });

  test('playback acknowledgement history survives a service-worker restart', async () => {
    const harness = createHarness();
    const created = await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PROCESS, {
      url: `https://www.youtube.com/watch?v=${videoId}`
    });
    await harness.dispatch(contract.MESSAGE_TYPES.YOUTUBE_PAGE_READY, {
      protocol_version: 1,
      video_id: videoId
    });
    const occurrence = {
      protocol_version: 1,
      video_id: videoId,
      job_id: created.payload.job_id,
      cue_id: 'cue-1',
      event_id: 'restart-sequence',
      sign_id: 'hello',
      at_ms: 10,
      video_time_seconds: 1,
      video_paused: false,
      playback_rate: 1,
      cue_start_seconds: 1,
      cue_end_seconds: 3,
      timing_error_ms: null
    };
    assert.equal((await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...occurrence,
      event_type: 'accepted'
    })).accepted, true);
    assert.equal((await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...occurrence,
      at_ms: 20,
      event_type: 'playback_start',
      timing_error_ms: 0
    })).status, 'playback_start');

    harness.restart();
    assert.equal((await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...occurrence,
      at_ms: 20,
      event_type: 'playback_start',
      timing_error_ms: 0
    })).duplicate, true);
    assert.equal((await harness.dispatch(contract.MESSAGE_TYPES.AETHER_PLAYBACK_STATE, {
      ...occurrence,
      at_ms: 2020,
      video_time_seconds: 2.9,
      timing_error_ms: -100,
      event_type: 'playback_end'
    })).status, 'playback_end');
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

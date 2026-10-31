import assert from 'node:assert/strict';
import test from 'node:test';
import { LiveSpeechSession } from './LiveSpeechSession.mjs';
import { MicrophoneSource } from '../audio_pipeline/AudioPipeline.js';

function createHarness({ sourceStart = async () => {}, requestOverrides = {}, silenceDurationMs = 800 } = {}) {
  const sources = [];
  const pipelines = [];
  const requests = [];
  const states = [];
  const transcripts = [];
  const sourceFactory = () => {
    const source = {
      started: false,
      stopped: 0,
      async start() {
        await sourceStart();
        this.started = true;
      },
      async stop() {
        this.started = false;
        this.stopped += 1;
      }
    };
    sources.push(source);
    return source;
  };
  const pipelineFactory = onResult => {
    const pipeline = {
      onResult,
      state: 'stopped',
      attach(source) { this.source = source; return this; },
      async start() {
        await this.source.start();
        this.state = 'running';
      },
      async stop() {
        this.state = 'stopped';
        const source = this.source;
        this.source = null;
        await source?.stop();
      },
      async reset() {
        this.resetCount = (this.resetCount || 0) + 1;
        await this.stop();
      },
      emit(result) { this.onResult(result); }
    };
    pipelines.push(pipeline);
    return pipeline;
  };
  const request = async (path, body) => {
    requests.push({ path, body });
    if (requestOverrides[path]) return requestOverrides[path](body);
    if (path === '/asr/start') return { state: 'running' };
    if (path === '/asr/chunk') return { status: { state: 'running' }, events: [] };
    if (path === '/asr/flush') return { status: { state: 'running' }, events: [] };
    return { state: path === '/asr/reset' || path === '/asr/stop' ? 'stopped' : 'running' };
  };
  const session = new LiveSpeechSession({
    createSource: sourceFactory,
    createPipeline: pipelineFactory,
    request,
    onState: state => states.push(state),
    onASRStatus: () => {},
    onTranscriptEvents: events => transcripts.push(...events),
    silenceDurationMs
  });
  return { session, sources, pipelines, requests, states, transcripts };
}

test('starts once for concurrent requests and stops and resets the live session cleanly', async () => {
  let resolveSourceStart;
  const harness = createHarness({
    sourceStart: () => new Promise(resolve => { resolveSourceStart = resolve; })
  });
  const firstStart = harness.session.start();
  const secondStart = harness.session.start();

  assert.equal(firstStart, secondStart);
  assert.equal(harness.session.state, 'STARTING');
  assert.equal(harness.sources.length, 1);
  resolveSourceStart();
  await firstStart;
  assert.equal(harness.session.state, 'RUNNING');
  assert.equal(harness.sources[0].started, true);
  assert.equal(harness.requests.filter(item => item.path === '/asr/start').length, 1);
  await harness.session.start();
  assert.equal(harness.sources.length, 1);
  assert.equal(harness.requests.filter(item => item.path === '/asr/start').length, 1);

  await harness.session.stop();
  assert.equal(harness.session.state, 'STOPPED');
  assert.equal(harness.sources[0].started, false);
  assert.equal(harness.sources[0].stopped, 1);
  assert.deepEqual(harness.requests.slice(-3).map(item => item.path), [
    '/asr/flush', '/asr/stop', '/asr/reset'
  ]);
  const requestCount = harness.requests.length;
  await harness.session.stop();
  assert.equal(harness.requests.length, requestCount);
});

test('microphone acquisition failure reports ERROR and releases partial pipeline resources', async () => {
  const permissionError = new Error('Microphone permission denied.');
  const harness = createHarness({ sourceStart: async () => { throw permissionError; } });

  await assert.rejects(harness.session.start(), /Microphone permission denied/);
  assert.equal(harness.session.state, 'ERROR');
  assert.equal(harness.states.some(state => state.state === 'RUNNING'), false);
  assert.equal(harness.sources[0].started, false);
  assert.equal(harness.sources[0].stopped, 1);
  assert.equal(harness.pipelines[0].resetCount, 1);
  assert.deepEqual(harness.requests.map(item => item.path), []);
});

test('ASR startup failure releases microphone and resets a possibly partial ASR session', async () => {
  const harness = createHarness({
    requestOverrides: {
      '/asr/start': async () => { throw new Error('Model unavailable.'); }
    }
  });

  await assert.rejects(harness.session.start(), /Model unavailable/);
  assert.equal(harness.session.state, 'ERROR');
  assert.equal(harness.sources[0].started, false);
  assert.equal(harness.sources[0].stopped, 1);
  assert.deepEqual(harness.requests.map(item => item.path), [
    '/asr/start', '/asr/stop', '/asr/reset'
  ]);
});

test('a stopped session restarts with fresh source, pipeline, and ASR lifecycle', async () => {
  const harness = createHarness();
  await harness.session.start();
  await harness.session.stop();
  await harness.session.start();

  assert.equal(harness.session.state, 'RUNNING');
  assert.equal(harness.sources.length, 2);
  assert.notEqual(harness.sources[0], harness.sources[1]);
  assert.notEqual(harness.pipelines[0], harness.pipelines[1]);
  assert.equal(harness.sources[0].started, false);
  assert.equal(harness.sources[1].started, true);
  assert.equal(harness.requests.filter(item => item.path === '/asr/start').length, 2);

  await harness.session.stop();
});

test('accepted chunks reach ASR and transcript events are forwarded; stopped chunks are ignored', async () => {
  const event = { kind: 'PARTIAL_TRANSCRIPT', text: 'hello' };
  const harness = createHarness({
    requestOverrides: {
      '/asr/chunk': async () => ({ status: { state: 'running' }, events: [event] })
    }
  });
  await harness.session.start();
  harness.pipelines[0].emit({
    accepted: true,
    samplesBase64: 'canonical-float32',
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 20 }
  });
  await Promise.all([...harness.session.pendingChunks]);

  assert.deepEqual(harness.transcripts, [event]);
  const chunkRequest = harness.requests.find(item => item.path === '/asr/chunk');
  assert.equal(chunkRequest.body.samples_base64, 'canonical-float32');
  assert.equal(chunkRequest.body.audio_end_ms, 120);

  await harness.session.stop();
  harness.pipelines[0].emit({
    accepted: true,
    samplesBase64: 'stale',
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 200 }
  });
  assert.equal(harness.requests.filter(item => item.path === '/asr/chunk').length, 1);
});

test('VAD silence flushes short utterances and allows the same word in a new utterance', async () => {
  const finalHello = { kind: 'FINAL_TRANSCRIPT', text: 'hello' };
  const harness = createHarness({
    silenceDurationMs: 200,
    requestOverrides: {
      '/asr/flush': async () => ({ status: { state: 'running' }, events: [finalHello] })
    }
  });
  const accepted = {
    accepted: true,
    samplesBase64: 'short-word',
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 0 }
  };
  const silence = {
    accepted: false,
    diagnostics: { rms: 0 },
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 100 }
  };

  await harness.session.start();
  harness.pipelines[0].emit(accepted);
  await Promise.all([...harness.session.pendingChunks]);
  harness.pipelines[0].emit(silence);
  harness.pipelines[0].emit({ ...silence, chunk: { ...silence.chunk, capturedAt: 200 } });
  await harness.session.finalizingPromise;

  harness.pipelines[0].emit({ ...accepted, chunk: { ...accepted.chunk, capturedAt: 300 } });
  await Promise.all([...harness.session.pendingChunks]);
  harness.pipelines[0].emit({ ...silence, chunk: { ...silence.chunk, capturedAt: 400 } });
  harness.pipelines[0].emit({ ...silence, chunk: { ...silence.chunk, capturedAt: 500 } });
  await harness.session.finalizingPromise;

  assert.deepEqual(harness.transcripts, [finalHello, finalHello]);
  assert.deepEqual(
    harness.requests.filter(item => ['/asr/chunk', '/asr/flush'].includes(item.path)).map(item => item.path),
    ['/asr/chunk', '/asr/flush', '/asr/chunk', '/asr/flush']
  );
  await harness.session.stop();
});

test('a failed final flush retains ASR state so a later stop can retry it', async () => {
  let flushAttempts = 0;
  const harness = createHarness({
    requestOverrides: {
      '/asr/flush': async () => {
        flushAttempts += 1;
        return flushAttempts === 1
          ? { status: { state: 'running' }, flush_status: 'FAILED_RETRYABLE', flush_error: 'Injected finalization failure.' }
          : { status: { state: 'running' }, flush_status: 'COMPLETED', events: [] };
      }
    }
  });
  await harness.session.start();

  await assert.rejects(harness.session.stop(), /Live speech stopped with cleanup errors/);
  assert.equal(harness.session.asrStarted, true);
  assert.equal(harness.requests.some(item => item.path === '/asr/reset'), false);

  await harness.session.stop();
  assert.equal(harness.session.state, 'STOPPED');
  assert.equal(harness.session.asrStarted, false);
  assert.equal(flushAttempts, 2);
  assert.deepEqual(harness.requests.slice(-3).map(item => item.path), [
    '/asr/flush', '/asr/stop', '/asr/reset'
  ]);
});

test('transcript events from a partially failed VAD flush are delivered before retry', async () => {
  const finalized = { kind: 'FINAL_TRANSCRIPT', text: 'completed window' };
  let flushAttempts = 0;
  const harness = createHarness({
    silenceDurationMs: 100,
    requestOverrides: {
      '/asr/flush': async () => {
        flushAttempts += 1;
        return flushAttempts === 1
          ? {
            status: { state: 'running' },
            flush_status: 'FAILED_RETRYABLE',
            flush_error: 'Later window failed.',
            events: [finalized]
          }
          : { status: { state: 'running' }, flush_status: 'COMPLETED', events: [] };
      }
    }
  });
  const accepted = {
    accepted: true,
    samplesBase64: 'short-window',
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 0 }
  };
  const silence = {
    accepted: false,
    diagnostics: { rms: 0 },
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 100 }
  };

  await harness.session.start();
  harness.pipelines[0].emit(accepted);
  await Promise.all([...harness.session.pendingChunks]);
  harness.pipelines[0].emit(silence);
  await harness.session.finalizingPromise;
  assert.deepEqual(harness.transcripts, [finalized]);
  assert.equal(harness.session.asrStarted, true);

  await harness.session.stop();
  assert.deepEqual(harness.transcripts, [finalized]);
  assert.equal(flushAttempts, 2);
});

test('chunk failure reports ERROR, stops capture, and resets ASR', async () => {
  const harness = createHarness({
    requestOverrides: {
      '/asr/chunk': async () => { throw new Error('ASR chunk request failed.'); }
    }
  });
  await harness.session.start();
  harness.pipelines[0].emit({
    accepted: true,
    samplesBase64: 'failed-chunk',
    chunk: { samples: new Float32Array(1600), sampleRate: 16000, capturedAt: 0 }
  });

  await Promise.all([...harness.session.pendingChunks]);
  await harness.session.cleanupPromise;

  assert.equal(harness.session.state, 'ERROR');
  assert.equal(harness.states.some(state => state.state === 'RUNNING'), true);
  assert.equal(harness.states.at(-1).state, 'ERROR');
  assert.equal(harness.sources[0].started, false);
  assert.deepEqual(harness.requests.map(item => item.path), [
    '/asr/start', '/asr/chunk', '/asr/stop', '/asr/reset'
  ]);
});

test('MicrophoneSource releases tracks and AudioContext when graph setup fails', async () => {
  const originalNavigator = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  const originalAudioContext = globalThis.AudioContext;
  const tracks = [{ stopped: 0, stop() { this.stopped += 1; } }];
  let contextClosed = 0;
  const fakeStream = { getTracks: () => tracks };
  class FailingAudioContext {
    constructor() { this.state = 'running'; }
    createMediaStreamSource() { return { connect() {} }; }
    createScriptProcessor() { throw new Error('Audio graph creation failed.'); }
    async close() { contextClosed += 1; this.state = 'closed'; }
  }
  Object.defineProperty(globalThis, 'navigator', {
    configurable: true,
    value: { mediaDevices: { getUserMedia: async () => fakeStream } }
  });
  globalThis.AudioContext = FailingAudioContext;

  try {
    const source = new MicrophoneSource();
    await assert.rejects(source.start(), /Audio graph creation failed/);
    assert.equal(tracks[0].stopped, 1);
    assert.equal(contextClosed, 1);
    assert.equal(source.state, 'stopped');
    assert.equal(source.stream, null);
    assert.equal(source.context, null);
  } finally {
    if (originalNavigator) Object.defineProperty(globalThis, 'navigator', originalNavigator);
    else delete globalThis.navigator;
    if (originalAudioContext === undefined) delete globalThis.AudioContext;
    else globalThis.AudioContext = originalAudioContext;
  }
});

test('MicrophoneSource reports permission failure without leaving a stream active', async () => {
  const originalNavigator = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  const originalAudioContext = globalThis.AudioContext;
  Object.defineProperty(globalThis, 'navigator', {
    configurable: true,
    value: { mediaDevices: { getUserMedia: async () => { throw new Error('Permission denied.'); } } }
  });
  globalThis.AudioContext = class AudioContext {};

  try {
    const source = new MicrophoneSource();
    await assert.rejects(source.start(), /Permission denied/);
    assert.equal(source.state, 'stopped');
    assert.equal(source.stream, null);
  } finally {
    if (originalNavigator) Object.defineProperty(globalThis, 'navigator', originalNavigator);
    else delete globalThis.navigator;
    if (originalAudioContext === undefined) delete globalThis.AudioContext;
    else globalThis.AudioContext = originalAudioContext;
  }
});

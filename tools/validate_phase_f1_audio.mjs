import {
  AudioSource, FileSource, StreamingAudioPipeline, DEFAULT_AUDIO_FORMAT,
  SignalAnalyzer, EnergyVoiceActivityDetector
} from './audio_pipeline/AudioPipeline.js';

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const sine = (length, amplitude = 0.04) => Float32Array.from({ length }, (_, i) => amplitude * Math.sin(i * 0.1));

// Diagnostics are deterministic for simple signals.
const analyzer = new SignalAnalyzer();
const silenceMetrics = analyzer.analyze(new Float32Array(1600));
const speechMetrics = analyzer.analyze(sine(1600));
assert(silenceMetrics.rms === 0 && silenceMetrics.nearSilence, 'Silence RMS/near-silence calculation failed.');
assert(speechMetrics.rms > 0.02 && speechMetrics.peak <= 0.04, 'Speech RMS/peak calculation failed.');
assert(analyzer.analyze(Float32Array.from([1, 0, 0])).clipped, 'Clipping detection failed.');
const vad = new EnergyVoiceActivityDetector();
assert(!vad.detect(silenceMetrics).speech, 'Silence should not be speech.');
assert(vad.detect(speechMetrics).speech, 'Energy VAD should accept an energetic speech-like frame.');

// Input uses 8 kHz frames to prove the pipeline normalizes once to 16 kHz chunks.
const results = [];
const pipeline = new StreamingAudioPipeline({ format: { ...DEFAULT_AUDIO_FORMAT, chunkDurationMs: 100 }, onResult: result => results.push(result) });
pipeline.state = 'running';
const captureAt = performance.now();
for (const samples of [new Float32Array(800), new Float32Array(800), sine(800), sine(800)]) {
  pipeline.ingest({ samples, sampleRate: 8000, channels: 1, capturedAt: captureAt, source: 'test' });
}
assert(results.length === 4, 'Chunker did not preserve incremental chunk order.');
assert(results[0].chunk.samples.length === 1600, 'Canonical chunk must be 100 ms at 16 kHz.');
assert(!results[0].accepted && !results[1].accepted, 'Silence chunks were incorrectly accepted.');
assert(results[2].accepted && results[3].accepted, 'Speech-like chunks were incorrectly rejected.');
assert(pipeline.asrInput.queue.length === 2, 'Only accepted speech chunks should enter ASR input.');
for (const result of results) for (const value of Object.values(result.timings)) assert(Number.isFinite(value), 'Latency instrumentation must be finite.');

// FileSource shares the AudioSource contract and emits incrementally.
const source = new FileSource({ samples: sine(3200), sampleRate: 16000, frameDurationMs: 40 });
let frames = 0; source.onChunk(() => { frames += 1; }); await source.start();
assert(frames === 5 && source.state === 'stopped', 'FileSource did not emit expected progressive frames.');
const generic = new AudioSource(); await generic.start(); generic.pause(); assert(generic.state === 'paused', 'Source pause state failed.'); generic.resume(); generic.stop(); generic.reset(); assert(generic.state === 'stopped', 'Source stop/reset state failed.');

// Long-running input remains incremental and keeps well ahead of 100 ms chunk duration locally.
const stress = new StreamingAudioPipeline(); stress.state = 'running';
const started = performance.now();
for (let i = 0; i < 200; i += 1) stress.ingest({ samples: i % 4 ? sine(1600) : new Float32Array(1600), sampleRate: 16000, channels: 1, capturedAt: performance.now(), source: 'stress' });
const elapsed = performance.now() - started, perChunk = elapsed / 200;
assert(stress.results.length === 200, 'Long-running stream lost chunks.');
assert(perChunk < 100, `Pipeline falls behind real time: ${perChunk.toFixed(3)} ms per 100 ms chunk.`);
pipeline.pause(); assert(pipeline.state === 'paused', 'Pipeline pause failed.'); await pipeline.resume(); assert(pipeline.state === 'running', 'Pipeline resume failed.'); pipeline.reset(); assert(pipeline.asrInput.queue.length === 0 && pipeline.results.length === 0 && pipeline.state === 'stopped', 'Pipeline reset failed.');

console.log('PASS: audio source/file abstraction, chunking, normalization, and lifecycle states');
console.log('PASS: RMS/peak/clipping/silence diagnostics and adaptive energy VAD transitions');
console.log('PASS: accepted chunks enter ASR-ready queue with latency instrumentation');
console.log(`PASS: 200 incremental 100 ms chunks averaged ${perChunk.toFixed(3)} ms processing per chunk`);

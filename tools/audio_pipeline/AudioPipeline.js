/** Dependency-free streaming audio preparation layer for future ASR. */
export const DEFAULT_AUDIO_FORMAT = Object.freeze({ sampleRate: 16000, channels: 1, sampleType: 'Float32Array', chunkDurationMs: 100 });

export class AudioSource {
  constructor() { this.listeners = new Set(); this.state = 'stopped'; }
  onChunk(listener) { this.listeners.add(listener); return () => this.listeners.delete(listener); }
  async emit(chunk) { for (const listener of this.listeners) await listener(chunk); }
  async start() { this.state = 'running'; }
  pause() { if (this.state === 'running') this.state = 'paused'; }
  resume() { if (this.state === 'paused') this.state = 'running'; }
  stop() { this.state = 'stopped'; }
  reset() { this.stop(); }
}

/** Pushes prerecorded PCM progressively, rather than coupling downstream code to files. */
export class FileSource extends AudioSource {
  constructor({ samples, sampleRate, channels = 1, frameDurationMs = 40 }) {
    super(); this.samples = samples; this.sampleRate = sampleRate; this.channels = channels;
    this.frameSamples = Math.max(1, Math.round(sampleRate * channels * frameDurationMs / 1000)); this.offset = 0;
  }
  async start() {
    await super.start();
    while (this.state === 'running' && this.offset < this.samples.length) {
      const end = Math.min(this.samples.length, this.offset + this.frameSamples);
      await this.emit({ samples: this.samples.slice(this.offset, end), sampleRate: this.sampleRate, channels: this.channels, capturedAt: performance.now(), source: 'file' });
      this.offset = end;
    }
    if (this.offset >= this.samples.length) this.stop();
  }
  reset() { super.reset(); this.offset = 0; }
}

/** Browser-only microphone adapter. It only captures PCM; pipeline processing is shared. */
export class MicrophoneSource extends AudioSource {
  constructor({ bufferSize = 2048 } = {}) { super(); this.bufferSize = bufferSize; this.stream = null; this.context = null; this.node = null; }
  async start() {
    if (!globalThis.navigator?.mediaDevices?.getUserMedia || !globalThis.AudioContext) throw new Error('Browser microphone capture is unavailable in this context.');
    this.stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, echoCancellation: false, noiseSuppression: false, autoGainControl: false } });
    this.context = new AudioContext();
    const input = this.context.createMediaStreamSource(this.stream);
    this.node = this.context.createScriptProcessor(this.bufferSize, 1, 1);
    this.node.onaudioprocess = event => {
      if (this.state !== 'running') return;
      const samples = new Float32Array(event.inputBuffer.getChannelData(0));
      this.emit({ samples, sampleRate: this.context.sampleRate, channels: 1, capturedAt: performance.now(), source: 'microphone' });
    };
    input.connect(this.node); this.node.connect(this.context.destination); await super.start();
  }
  pause() { super.pause(); this.context?.suspend(); }
  resume() { super.resume(); this.context?.resume(); }
  stop() { super.stop(); this.node?.disconnect(); this.stream?.getTracks().forEach(track => track.stop()); this.context?.close(); this.node = this.stream = this.context = null; }
}

export function decodeWav(arrayBuffer) {
  const view = new DataView(arrayBuffer);
  const text = (offset, length) => String.fromCharCode(...new Uint8Array(arrayBuffer, offset, length));
  if (text(0, 4) !== 'RIFF' || text(8, 4) !== 'WAVE') throw new Error('Only RIFF/WAVE files are supported by the lightweight file source.');
  let offset = 12, format, data;
  while (offset + 8 <= view.byteLength) {
    const id = text(offset, 4), size = view.getUint32(offset + 4, true); offset += 8;
    if (id === 'fmt ') format = { audioFormat: view.getUint16(offset, true), channels: view.getUint16(offset + 2, true), sampleRate: view.getUint32(offset + 4, true), bits: view.getUint16(offset + 14, true) };
    if (id === 'data') data = { offset, size };
    offset += size + (size % 2);
  }
  if (!format || !data || format.audioFormat !== 1 || ![16, 32].includes(format.bits)) throw new Error('Supported WAV inputs are PCM 16-bit or PCM 32-bit.');
  const count = data.size / (format.bits / 8), samples = new Float32Array(count);
  for (let i = 0; i < count; i++) samples[i] = format.bits === 16 ? view.getInt16(data.offset + i * 2, true) / 32768 : view.getInt32(data.offset + i * 4, true) / 2147483648;
  return { samples, sampleRate: format.sampleRate, channels: format.channels };
}

function toMono(samples, channels) {
  if (channels === 1) return samples;
  const output = new Float32Array(Math.floor(samples.length / channels));
  for (let frame = 0; frame < output.length; frame++) { let sum = 0; for (let c = 0; c < channels; c++) sum += samples[frame * channels + c]; output[frame] = sum / channels; }
  return output;
}
function resample(samples, fromRate, toRate) {
  if (fromRate === toRate) return samples;
  const length = Math.max(1, Math.round(samples.length * toRate / fromRate)), output = new Float32Array(length);
  for (let i = 0; i < length; i++) { const position = i * fromRate / toRate, left = Math.floor(position), right = Math.min(left + 1, samples.length - 1), mix = position - left; output[i] = samples[left] * (1 - mix) + samples[right] * mix; }
  return output;
}

export class PCMChunker {
  constructor(format = DEFAULT_AUDIO_FORMAT) { this.format = format; this.chunkSamples = Math.round(format.sampleRate * format.chunkDurationMs / 1000); this.buffer = new Float32Array(0); }
  push(samples, capturedAt) {
    const joined = new Float32Array(this.buffer.length + samples.length); joined.set(this.buffer); joined.set(samples, this.buffer.length); this.buffer = joined;
    const chunks = [];
    while (this.buffer.length >= this.chunkSamples) { chunks.push({ samples: this.buffer.slice(0, this.chunkSamples), sampleRate: this.format.sampleRate, channels: 1, capturedAt, createdAt: performance.now() }); this.buffer = this.buffer.slice(this.chunkSamples); }
    return chunks;
  }
  reset() { this.buffer = new Float32Array(0); }
}

export class PassthroughNoiseSuppressor { process(chunk) { return chunk; } }
export class SignalAnalyzer {
  analyze(samples) {
    let squared = 0, peak = 0, clipped = 0;
    for (const value of samples) { const absolute = Math.abs(value); squared += value * value; peak = Math.max(peak, absolute); if (absolute >= 0.999) clipped += 1; }
    const rms = Math.sqrt(squared / Math.max(1, samples.length));
    return { rms, peak, clipped: clipped > 0, nearSilence: rms < 0.003 };
  }
}
export class EnergyVoiceActivityDetector {
  constructor({ initialNoiseFloor = 0.003, thresholdMultiplier = 3, minThreshold = 0.008 } = {}) { this.initialNoiseFloor = initialNoiseFloor; this.noiseFloor = initialNoiseFloor; this.thresholdMultiplier = thresholdMultiplier; this.minThreshold = minThreshold; }
  detect(metrics) { const threshold = Math.max(this.minThreshold, this.noiseFloor * this.thresholdMultiplier); const speech = metrics.rms >= threshold; if (!speech) this.noiseFloor = this.noiseFloor * 0.9 + metrics.rms * 0.1; return { speech, threshold, noiseFloor: this.noiseFloor, snrDb: 20 * Math.log10((metrics.rms + 1e-9) / (this.noiseFloor + 1e-9)) }; }
  reset() { this.noiseFloor = this.initialNoiseFloor; }
}
export class StreamingASRInput {
  constructor() { this.queue = []; }
  enqueue(chunk) { this.queue.push(chunk); }
  dequeue() { return this.queue.shift(); }
  reset() { this.queue = []; }
}

export class StreamingAudioPipeline {
  constructor({ format = DEFAULT_AUDIO_FORMAT, suppressor = new PassthroughNoiseSuppressor(), vad = new EnergyVoiceActivityDetector(), asrInput = new StreamingASRInput(), onResult = null } = {}) {
    this.format = { ...DEFAULT_AUDIO_FORMAT, ...format }; this.chunker = new PCMChunker(this.format); this.suppressor = suppressor; this.vad = vad; this.asrInput = asrInput; this.analyzer = new SignalAnalyzer(); this.onResult = onResult; this.state = 'stopped'; this.results = [];
  }
  attach(source) { this.detach?.(); this.detach = source.onChunk(chunk => this.ingest(chunk)); this.source = source; return this; }
  async start() { this.state = 'running'; if (this.source) await this.source.start(); }
  pause() { this.state = 'paused'; this.source?.pause(); }
  async resume() { this.state = 'running'; this.source?.resume(); }
  stop() { this.state = 'stopped'; this.source?.stop(); }
  reset() { this.stop(); this.chunker.reset(); this.vad.reset(); this.asrInput.reset(); this.results = []; }
  ingest(rawChunk) {
    if (this.state !== 'running') return [];
    const mono = toMono(rawChunk.samples, rawChunk.channels || 1), samples = resample(mono, rawChunk.sampleRate, this.format.sampleRate);
    return this.chunker.push(samples, rawChunk.capturedAt).map(chunk => this.process(chunk));
  }
  process(chunk) {
    const preprocessStart = performance.now(), processed = this.suppressor.process(chunk), preprocessEnd = performance.now();
    const vadStart = performance.now(), metrics = this.analyzer.analyze(processed.samples), decision = this.vad.detect(metrics), vadEnd = performance.now();
    const queueStart = performance.now(); if (decision.speech) this.asrInput.enqueue({ ...processed, diagnostics: { ...metrics, ...decision } }); const queueEnd = performance.now();
    const result = { chunk: processed, accepted: decision.speech, diagnostics: { ...metrics, ...decision }, timings: { capturedAt: chunk.capturedAt, createdAt: chunk.createdAt, chunkReadyMs: chunk.createdAt - chunk.capturedAt, preprocessingMs: preprocessEnd - preprocessStart, vadMs: vadEnd - vadStart, queueInsertionMs: queueEnd - queueStart, completedAt: queueEnd } };
    this.results.push(result); this.onResult?.(result); return result;
  }
}

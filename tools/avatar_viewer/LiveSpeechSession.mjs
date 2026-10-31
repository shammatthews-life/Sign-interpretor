export class LiveSpeechSession {
  constructor({
    createSource,
    createPipeline,
    request,
    onState = () => {},
    onASRStatus = () => {},
    onTranscriptEvents = () => {},
    silenceDurationMs = 800
  }) {
    if (![createSource, createPipeline, request].every(value => typeof value === 'function')) {
      throw new TypeError('LiveSpeechSession requires source, pipeline, and request factories.');
    }
    this.createSource = createSource;
    this.createPipeline = createPipeline;
    this.request = request;
    this.onState = onState;
    this.onASRStatus = onASRStatus;
    this.onTranscriptEvents = onTranscriptEvents;
    this.silenceDurationMs = silenceDurationMs;
    this.state = 'IDLE';
    this.error = null;
    this.pipeline = null;
    this.source = null;
    this.acceptingChunks = false;
    this.asrStarted = false;
    this.pendingChunks = new Set();
    this.startPromise = null;
    this.stopPromise = null;
    this.cleanupPromise = null;
    this.sessionId = 0;
    this.speechActive = false;
    this.silenceMs = 0;
    this.finalizingPromise = null;
    this.chunkSendChain = Promise.resolve();
    this.nextChunkId = 0;
    this.flushFailed = false;
  }

  #setState(state, error = null) {
    this.state = state;
    this.error = error;
    this.onState({ state, error: error?.message || null });
  }

  start() {
    if (this.state === 'RUNNING') return Promise.resolve();
    if (this.asrStarted && this.state === 'ERROR') {
      return Promise.reject(this.error || new Error('ASR finalization is pending; stop again to retry the flush.'));
    }
    if (this.state === 'STARTING') return this.startPromise;
    if (this.cleanupPromise) return this.cleanupPromise.then(() => this.start());
    if (this.state === 'STOPPING') {
      return this.stopPromise.then(() => this.start());
    }
    this.#setState('STARTING');
    const sessionId = ++this.sessionId;
    this.startPromise = this.#start(sessionId).finally(() => {
      this.startPromise = null;
    });
    return this.startPromise;
  }

  async #start(sessionId) {
    let asrStartAttempted = false;
    try {
      const source = this.createSource();
      const pipeline = this.createPipeline(result => this.#queueChunk(result, sessionId));
      this.source = source;
      this.pipeline = pipeline;
      pipeline.attach(source);
      await pipeline.start();

      asrStartAttempted = true;
      const response = await this.request('/asr/start');
      if (response?.state !== 'running') {
        throw new Error(`ASR service did not enter running state (received ${response?.state || 'no state'}).`);
      }
      this.asrStarted = true;
      this.acceptingChunks = true;
      this.speechActive = false;
      this.silenceMs = 0;
      this.chunkSendChain = Promise.resolve();
      this.nextChunkId = 0;
      this.flushFailed = false;
      this.onASRStatus(response);
      this.#setState('RUNNING');
      return response;
    } catch (error) {
      this.acceptingChunks = false;
      const cleanupErrors = await this.#releaseResources({ resetASR: asrStartAttempted });
      const reportedError = cleanupErrors.length
        ? new AggregateError([error, ...cleanupErrors], 'Live speech startup failed and cleanup reported errors.')
        : error;
      this.#setState('ERROR', reportedError);
      throw reportedError;
    }
  }

  #queueChunk(result, sessionId) {
    if (!this.acceptingChunks || this.state !== 'RUNNING' || sessionId !== this.sessionId) return;
    const durationMs = result.chunk.samples.length * 1000 / result.chunk.sampleRate;
    if (!result.accepted) {
      if (this.speechActive) {
        this.silenceMs += durationMs;
        if (this.silenceMs >= this.silenceDurationMs && !this.finalizingPromise) {
          this.speechActive = false;
          this.silenceMs = 0;
          this.#trace('vad_speech_end', { silenceDurationMs: this.silenceDurationMs });
          this.finalizingPromise = this.#finalizeUtterance(sessionId)
            .catch(error => {
              this.acceptingChunks = false;
              this.#setState('ERROR', error);
              if (this.flushFailed) {
                return this.#releaseResources({ resetASR: false, preserveASR: true }).then(cleanupErrors => {
                  if (cleanupErrors.length) {
                    this.#setState('ERROR', new AggregateError([error, ...cleanupErrors], 'ASR flush failed and microphone cleanup reported errors.'));
                  }
                });
              }
            })
            .finally(() => { this.finalizingPromise = null; });
        }
      }
      this.#trace('audio_chunk', { accepted: false, durationMs, rms: result.diagnostics?.rms });
      return;
    }
    if (!this.speechActive) this.#trace('vad_speech_start');
    this.speechActive = true;
    this.silenceMs = 0;
    this.#trace('audio_chunk', { accepted: true, durationMs, rms: result.diagnostics?.rms });

    const precedingFinalization = this.finalizingPromise;
    let chunkError = null;
    const task = this.chunkSendChain.then(async () => {
      if (precedingFinalization) await precedingFinalization;
      if (!this.acceptingChunks || this.state !== 'RUNNING') return;
      await this.#sendChunk(result);
    }).catch(error => {
      this.acceptingChunks = false;
      chunkError = error;
      this.#setState('ERROR', error);
    }).finally(() => {
      this.pendingChunks.delete(task);
      if (chunkError && !this.cleanupPromise) {
        const error = chunkError;
        this.asrStarted = false;
        this.cleanupPromise = Promise.all([...this.pendingChunks]).then(() =>
          this.#releaseResources({ resetASR: true })
        ).then(cleanupErrors => {
          if (cleanupErrors.length) {
            this.#setState('ERROR', new AggregateError([error, ...cleanupErrors], 'Live speech failed and cleanup reported errors.'));
          }
        }).catch(cleanupError => {
          this.#setState('ERROR', new AggregateError([error, cleanupError], 'Live speech failed and cleanup reported errors.'));
        }).finally(() => { this.cleanupPromise = null; });
      }
    });
    this.chunkSendChain = task;
    this.pendingChunks.add(task);
  }

  async #finalizeUtterance(sessionId) {
    await Promise.all([...this.pendingChunks]);
    if (!this.asrStarted || sessionId !== this.sessionId) return;
    this.#trace('asr_flush');
    const response = await this.request('/asr/flush');
    this.#consumeFlushResponse(response);
  }

  #consumeFlushResponse(response) {
    this.onASRStatus(response.status);
    if (response.events?.length) {
      for (const event of response.events) {
        this.#trace('asr_transcript', { kind: event.kind, characterCount: event.text?.length || 0 });
      }
      this.onTranscriptEvents(response.events);
    }
    if (response.flush_status && response.flush_status !== 'COMPLETED') {
      this.flushFailed = true;
      throw new Error(response.flush_error || `ASR flush ended with status ${response.flush_status}.`);
    }
    this.flushFailed = false;
  }

  #trace(event, details = {}) {
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) {
      console.debug(`[LiveSpeechSession] ${event}`, details);
    }
  }

  async #sendChunk(result) {
    const durationMs = result.chunk.samples.length * 1000 / result.chunk.sampleRate;
    const response = await this.request('/asr/chunk', {
      samples_base64: result.samplesBase64,
      audio_start_ms: result.chunk.capturedAt,
      audio_end_ms: result.chunk.capturedAt + durationMs,
      chunk_id: this.nextChunkId++
    });
    this.onASRStatus(response.status);
    if (response.events?.length) {
      for (const event of response.events) {
        this.#trace('asr_transcript', { kind: event.kind, characterCount: event.text?.length || 0 });
      }
      this.onTranscriptEvents(response.events);
    }
  }

  async stop() {
    if (this.state === 'STARTING') {
      try {
        await this.startPromise;
      } catch {
        return;
      }
    }
    if (this.state === 'STOPPING') return this.stopPromise;
    if (this.state === 'IDLE' || this.state === 'STOPPED') return;
    if (this.cleanupPromise) {
      await this.cleanupPromise;
      return;
    }
    const resetASR = this.asrStarted || this.state === 'ERROR';
    this.acceptingChunks = false;
    this.#setState('STOPPING');
    this.stopPromise = this.#stop(resetASR).finally(() => {
      this.stopPromise = null;
    });
    return this.stopPromise;
  }

  async #stop(resetASR) {
    const errors = [];
    const flush = this.asrStarted;
    if (this.pipeline) {
      try {
        await this.pipeline.stop();
      } catch (error) {
        errors.push(error);
      }
    }
    await Promise.all([...this.pendingChunks]);
    if (this.finalizingPromise) await this.finalizingPromise;

    if (flush) {
      try {
        const response = await this.request('/asr/flush');
        this.#consumeFlushResponse(response);
      } catch (error) {
        this.flushFailed = true;
        errors.push(error);
      }
    }
    errors.push(...await this.#releaseResources({
      resetASR: resetASR && !this.flushFailed,
      preserveASR: this.flushFailed
    }));
    if (errors.length) {
      const error = new AggregateError(errors, 'Live speech stopped with cleanup errors.');
      this.#setState('ERROR', error);
      throw error;
    }
    this.#setState('STOPPED');
  }

  async #releaseResources({ resetASR, preserveASR = false }) {
    const errors = [];
    const pipeline = this.pipeline;
    this.pipeline = null;
    this.source = null;
    if (!preserveASR) this.asrStarted = false;

    if (pipeline) {
      try {
        await pipeline.reset();
      } catch (error) {
        errors.push(error);
      }
    }
    if (resetASR) {
      try {
        await this.request('/asr/stop');
      } catch (error) {
        errors.push(error);
      }
      try {
        const response = await this.request('/asr/reset');
        this.onASRStatus(response);
      } catch (error) {
        errors.push(error);
      }
    }
    return errors;
  }
}

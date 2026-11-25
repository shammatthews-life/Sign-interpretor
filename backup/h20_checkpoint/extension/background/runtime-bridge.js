/**
 * ISL Accessibility Translator - Runtime Bridge (Phase H6)
 *
 * Manages communication between Chrome Extension and the local Python/JS runtime:
 *   - Localhost health monitoring (http://localhost:8000/asr/status)
 *   - Deterministic demo execution engine
 *   - Error boundary (prevents extension or host page crashes on network failure)
 */

(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLRuntimeBridge = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const contract = typeof ISLMessageContract !== 'undefined'
    ? ISLMessageContract
    : (typeof require !== 'undefined' ? require('../shared/message-contract.js') : null);

  const demoData = typeof ISLDemoData !== 'undefined'
    ? ISLDemoData
    : (typeof require !== 'undefined' ? require('../shared/demo-data.js') : null);

  class RuntimeBridge {
    constructor({ defaultEndpoint = 'http://localhost:8000', onStateUpdate = null } = {}) {
      this.state = contract ? contract.createInitialState() : {};
      this.state.runtimeEndpoint = defaultEndpoint;
      this.onStateUpdate = onStateUpdate;
      this.pingInterval = null;
      this.demoTimer = null;
      this.youtubePollingJobs = new Set();
    }

    getState() {
      return JSON.parse(JSON.stringify(this.state));
    }

    emitUpdate() {
      this.state.updatedAt = Date.now();
      if (typeof this.onStateUpdate === 'function') {
        this.onStateUpdate(this.getState());
      }
    }

    /**
     * Check localhost availability gracefully. Never throws uncaught errors.
     */
    async pingRuntime(endpoint = null) {
      const target = (endpoint || this.state.runtimeEndpoint || 'http://localhost:8000').replace(/\/$/, '');
      this.state.runtimeEndpoint = target;
      this.state.connection = contract.STATES.CONNECTION.CONNECTING;
      this.emitUpdate();

      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);

        const response = await fetch(`${target}/asr/status`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({}),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (response.ok) {
          const data = await response.json().catch(() => ({}));
          this.state.connection = contract.STATES.CONNECTION.CONNECTED;
          this.state.runtimeAvailable = true;
          this.state.runtimeError = null;
          this.state.asr = data.state === 'running' ? contract.STATES.ASR.PARTIAL : contract.STATES.ASR.WAITING;
        } else {
          this.state.connection = contract.STATES.CONNECTION.DISCONNECTED;
          this.state.runtimeAvailable = false;
          this.state.runtimeError = `Localhost runtime HTTP ${response.status}`;
        }
      } catch (err) {
        // Graceful failure: localhost is offline
        this.state.connection = contract.STATES.CONNECTION.DISCONNECTED;
        this.state.runtimeAvailable = false;
        this.state.runtimeError = `Localhost runtime offline (${err.name === 'AbortError' ? 'timeout' : 'unreachable'})`;
      }

      this.emitUpdate();
      return this.getState();
    }

    async requestJson(url, options = {}, timeoutMs = 10000) {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await fetch(url, { ...options, signal: controller.signal });
        const text = await response.text();
        let payload;
        try {
          payload = text ? JSON.parse(text) : {};
        } catch {
          throw new Error(`Local runtime returned malformed JSON (HTTP ${response.status}).`);
        }
        if (!response.ok) {
          throw new Error(payload.error || `Local runtime returned HTTP ${response.status}.`);
        }
        return payload;
      } catch (error) {
        if (error.name === 'AbortError') throw new Error('Local runtime request timed out.');
        throw error;
      } finally {
        clearTimeout(timeoutId);
      }
    }

    async submitYouTube(url) {
      const validation = contract.validateYouTubeUrl(url);
      if (!validation.valid) throw new Error(validation.error);
      if (this.state.youtube.jobId && !['READY', 'ERROR'].includes(this.state.youtube.state)) {
        throw new Error('A YouTube video is already processing.');
      }
      const payload = await this.requestJson(`${this.state.runtimeEndpoint}/youtube/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: validation.canonicalUrl })
      });
      if (!payload || typeof payload.job_id !== 'string' || payload.state !== 'QUEUED') {
        throw new Error('Local runtime returned a malformed YouTube job response.');
      }
      this.state.youtube = {
        ...contract.createInitialState().youtube,
        jobId: payload.job_id,
        state: payload.state,
        progress: 0,
        error: null
      };
      this.state.runtimeAvailable = true;
      this.state.connection = contract.STATES.CONNECTION.CONNECTED;
      this.state.runtimeError = null;
      this.emitUpdate();
      if (!this.youtubePollingJobs.has(payload.job_id)) {
        this.youtubePollingJobs.add(payload.job_id);
        this.pollYouTubeJob(payload.job_id)
          .catch(error => console.warn('[ISL Runtime Bridge] YouTube job failed:', error.message))
          .finally(() => this.youtubePollingJobs.delete(payload.job_id));
      }
      return { job_id: payload.job_id, state: payload.state };
    }

    setYouTubeError(error) {
      this.state.youtube = {
        ...contract.createInitialState().youtube,
        state: 'ERROR',
        error: error?.message || 'YouTube processing could not be started.'
      };
      this.emitUpdate();
    }

    async pollYouTubeJob(jobId) {
      const startedAt = Date.now();
      const allowedStates = new Set([
        'QUEUED', 'DOWNLOADING', 'EXTRACTING_AUDIO', 'TRANSCRIBING',
        'TRANSLATING', 'READY', 'ERROR'
      ]);
      try {
        while (Date.now() - startedAt < 30 * 60 * 1000) {
          const status = await this.requestJson(
            `${this.state.runtimeEndpoint}/youtube/status/${encodeURIComponent(jobId)}`,
            {},
            10000
          );
          if (status.job_id !== jobId || !allowedStates.has(status.stage)) {
            throw new Error('Local runtime returned malformed YouTube job status.');
          }
          this.state.youtube = { ...this.state.youtube, jobId, state: status.stage, progress: Number(status.progress) || 0, error: status.error || null };
          this.emitUpdate();
          if (status.stage === 'ERROR') throw new Error(status.error || 'YouTube processing failed.');
          if (status.stage === 'READY') {
            const envelope = await this.requestJson(
              `${this.state.runtimeEndpoint}/youtube/result/${encodeURIComponent(jobId)}`,
              {},
              30000
            );
            if (envelope.job_id !== jobId || envelope.state !== 'READY' || !envelope.result) {
              throw new Error('Local runtime returned a malformed YouTube result.');
            }
            const transcript = envelope.result.transcript;
            const translation = envelope.result.translation;
            if (!envelope.result.metadata || !Array.isArray(transcript?.segments)
              || typeof transcript.full_text !== 'string'
              || !Array.isArray(translation?.translated_segments)) {
              throw new Error('Local runtime returned an incomplete YouTube result.');
            }
            this.applyYouTubeResult(jobId, envelope.result);
            return envelope.result;
          }
          await new Promise(resolve => setTimeout(resolve, 1200));
        }
        throw new Error('YouTube processing timed out after 30 minutes.');
      } catch (error) {
        this.state.youtube = { ...this.state.youtube, jobId, state: 'ERROR', error: error.message };
        this.emitUpdate();
        throw error;
      }
    }

    applyYouTubeResult(jobId, result) {
      const metadata = result.metadata || {};
      const transcript = result.transcript || {};
      const segments = Array.isArray(transcript.segments) ? transcript.segments : [];
      const translated = result.translation?.translated_segments || [];
      const glosses = [...new Set(translated.flatMap(segment => segment.gloss || []))];
      const translationStatusCounts = translated.reduce((counts, segment) => {
        const status = String(segment.translation_status || 'UNKNOWN').replace(/^TRANSLATION_/, '');
        counts[status] = (counts[status] || 0) + 1;
        return counts;
      }, {});
      const playable = translated.flatMap(segment => segment.playable_signs || []);
      const unavailable = translated.flatMap(segment => segment.unavailable_concepts || []);
      const latest = segments.length ? segments[segments.length - 1] : null;
      this.state.youtube = {
        jobId,
        state: 'READY',
        progress: 1,
        title: String(metadata.title || ''),
        duration: Number(metadata.duration) || null,
        audioDuration: Number(metadata.audio_duration_s) || null,
        segmentCount: segments.length,
        latestSegment: latest ? String(latest.text || '') : '',
        transcriptSummary: String(transcript.full_text || '').slice(0, 1800),
        resultReady: true,
        translationStatus: translated.length ? 'G2/G3 prototype gloss; not full ISL translation' : 'NO_TRANSLATION',
        translationStatusCounts,
        glosses,
        playableSigns: playable,
        currentSign: null,
        queuedSigns: [...new Set(playable)],
        unavailableConcepts: unavailable.map(item => ({
          word: String(item.sign_id || 'unknown'),
          reason: String(item.reason || 'Motion unavailable')
        })),
        error: null
      };
      this.state.transcript.final = String(transcript.full_text || '');
      this.state.transcript.lastUpdated = Date.now();
      this.state.representation = {
        ...this.state.representation,
        gloss: glosses.join(' '),
        glossSequence: glosses,
        status: this.state.youtube.translationStatus,
        playableSignIds: [...new Set(playable)],
        unavailableSignIds: [...new Set(unavailable.map(item => item.sign_id).filter(Boolean))]
      };
      this.state.signingQueue = {
        ...this.state.signingQueue,
        currentSign: null,
        queuedSigns: [...new Set(playable)],
        unavailableConcepts: this.state.youtube.unavailableConcepts
      };
      this.state.signing = playable.length
        ? contract.STATES.SIGNING.QUEUED
        : unavailable.length ? contract.STATES.SIGNING.UNAVAILABLE : contract.STATES.SIGNING.IDLE;
      this.emitUpdate();
    }

    updateAetherPlayback(payload = {}) {
      this.state.signingQueue.currentSign = payload.current || null;
      this.state.signingQueue.queuedSigns = Array.isArray(payload.queued) ? payload.queued : [];
      this.state.youtube.currentSign = this.state.signingQueue.currentSign;
      this.state.youtube.queuedSigns = this.state.signingQueue.queuedSigns;
      this.state.signing = this.state.signingQueue.currentSign
        ? contract.STATES.SIGNING.PLAYING
        : this.state.signingQueue.queuedSigns.length
          ? contract.STATES.SIGNING.QUEUED
          : this.state.youtube.playableSigns.length
            ? contract.STATES.SIGNING.IDLE
            : this.state.signing;
      this.emitUpdate();
    }

    disconnectRuntime() {
      this.state.connection = contract.STATES.CONNECTION.DISCONNECTED;
      this.state.runtimeAvailable = false;
      this.state.runtimeError = null;
      this.emitUpdate();
    }

    /**
     * Start deterministic demo mode (Task H6-D)
     */
    startDemo(scenarioId = 'greeting') {
      const scenarios = demoData ? demoData.DEMO_SCENARIOS : {};
      const scenario = scenarios[scenarioId] || scenarios.greeting;
      if (!scenario) return;

      this.state.demo = {
        active: true,
        scenario: scenario.id,
        step: 0,
        totalSteps: scenario.steps.length
      };

      // Apply initial step
      this.stepDemo();
    }

    /**
     * Advance demo to next deterministic step
     */
    stepDemo() {
      if (!this.state.demo.active) {
        this.startDemo(this.state.demo.scenario || 'greeting');
        return;
      }

      const scenarios = demoData ? demoData.DEMO_SCENARIOS : {};
      const scenario = scenarios[this.state.demo.scenario];
      if (!scenario) return;

      const currentStep = this.state.demo.step;
      const nextStepIndex = currentStep < scenario.steps.length ? currentStep + 1 : 1;
      const stepData = scenario.steps[nextStepIndex - 1];

      if (!stepData) return;

      this.state.demo.step = nextStepIndex;
      this.state.audio = stepData.audio || contract.STATES.AUDIO.IDLE;
      this.state.asr = stepData.asr || contract.STATES.ASR.WAITING;
      this.state.signing = stepData.signing || contract.STATES.SIGNING.IDLE;

      if (stepData.transcript) {
        this.state.transcript.partial = stepData.transcript.partial || '';
        this.state.transcript.final = stepData.transcript.final || '';
        this.state.transcript.lastUpdated = Date.now();
      }

      if (stepData.translation) {
        this.state.translation = stepData.translation.status || contract.STATES.TRANSLATION.READY;
        this.state.representation = {
          gloss: stepData.translation.gloss || '',
          glossSequence: stepData.translation.glossSequence || [],
          status: stepData.translation.status || 'READY',
          trace: stepData.translation.trace || [],
          unknownTerms: stepData.translation.unknownTerms || [],
          candidateSignIds: stepData.translation.candidateSignIds || [],
          playableSignIds: stepData.translation.playableSignIds || [],
          unavailableSignIds: stepData.translation.unavailableSignIds || []
        };
      }

      if (stepData.signingQueue) {
        this.state.signingQueue = {
          currentSign: stepData.signingQueue.currentSign || null,
          queuedSigns: stepData.signingQueue.queuedSigns || [],
          completedSigns: stepData.signingQueue.completedSigns || [],
          unavailableConcepts: stepData.signingQueue.unavailableConcepts || []
        };
      }

      this.emitUpdate();
    }

    /**
     * Stop demo mode and return to idle/clean state
     */
    stopDemo() {
      this.state.demo.active = false;
      this.state.demo.step = 0;
      this.state.audio = contract.STATES.AUDIO.IDLE;
      this.state.asr = contract.STATES.ASR.WAITING;
      this.state.translation = contract.STATES.TRANSLATION.IDLE;
      this.state.signing = contract.STATES.SIGNING.IDLE;
      this.state.transcript = { partial: '', final: '', lastUpdated: null };
      this.state.representation = {
        gloss: '',
        glossSequence: [],
        status: 'IDLE',
        trace: [],
        unknownTerms: [],
        candidateSignIds: [],
        playableSignIds: [],
        unavailableSignIds: []
      };
      this.state.signingQueue = {
        currentSign: null,
        queuedSigns: [],
        completedSigns: [],
        unavailableConcepts: []
      };
      this.emitUpdate();
    }

    toggleOverlay() {
      this.state.overlayVisible = !this.state.overlayVisible;
      this.emitUpdate();
      return this.state.overlayVisible;
    }

    setOverlayVisible(visible) {
      this.state.overlayVisible = Boolean(visible);
      this.emitUpdate();
    }
  }

  return {
    RuntimeBridge
  };
});

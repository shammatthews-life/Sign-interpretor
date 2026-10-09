/**
 * SpeechSignOrchestrator.js
 *
 * Phase G1: First integrated speech-to-avatar prototype orchestrator.
 * Connects:
 *   ASR events (partial / final)
 *     ↓
 *   incremental transcript stabilization & safe prefix commit policy
 *     ↓
 *   SentenceProcessor (controlled English-to-sign ID mapping)
 *     ↓
 *   playability check (filters unknown words & MOTION_INCOMPLETE signs)
 *     ↓
 *   SignScheduler (incremental queuing to Aether player)
 *
 * Key guarantees:
 * 1. Zero duplicate sign enqueuing during streaming partial evolution.
 * 2. Low-latency prefix commitment (committed signs play while trailing speech arrives).
 * 3. Complete decoupled architecture (ASR, SentenceProcessor, and SignScheduler remain independent).
 * 4. Comprehensive end-to-end timing (T0 -> T1 -> T2 -> T3 -> T4) and backpressure telemetry.
 */

export class SpeechSignOrchestrator {
  constructor({
    sentenceProcessor,
    translator = null,
    signScheduler,
    signLibrary = null,
    onCommit = null,
    onStateChange = null,
    onDiagnostics = null,
    minTrailingObservations = 2,
    stabilityDelayMs = 250,
  } = {}) {
    if (!sentenceProcessor) throw new Error('SentenceProcessor is required.');
    if (!signScheduler) throw new Error('SignScheduler is required.');

    this.sentenceProcessor = sentenceProcessor;
    this.translator = translator;
    this.signScheduler = signScheduler;
    this.signLibrary = signLibrary;
    this.onCommit = onCommit;
    this.onStateChange = onStateChange;
    this.onDiagnostics = onDiagnostics;
    this.minTrailingObservations = minTrailingObservations;
    this.stabilityDelayMs = stabilityDelayMs;

    this.state = 'idle'; // 'idle' | 'running' | 'paused' | 'stopped'

    // Incremental transcript & commitment tracking
    this.committedSigns = [];       // [{ id, word, committedAt, enqueuedAt }]
    this.candidateSigns = [];       // currently pending uncommitted sign IDs
    this.trailingCandidates = new Map(); // key -> { count, firstSeenAt }
    this.unknownWordsSet = new Set();
    this.unavailableSignsSet = new Set();
    this.lastProcessedText = '';
    this.lastTranslation = null;

    // End-to-end latency instrumentation
    this.t0 = null;                // Audio entered system (ms)
    this.timings = {
      t0: null,                    // Audio entered system
      t1: null,                    // First partial transcript emitted
      t2: null,                    // First sign committed
      t3: null,                    // First sign entered scheduler
      t4: null,                    // First sign Aether playback start
      firstSignId: null,
      finalTranscriptAt: null,
      finalSignCommittedAt: null,
    };

    // Backpressure & queue tracking
    this.queueEntryTimes = new Map(); // uniqueKey -> performance.now()
    this.completedSignsCount = 0;
    this.totalSignsEnqueued = 0;
    this._queueCounter = 0;

    // Attach lifecycle listener to scheduler to capture T4 (Aether playback start)
    const prevLifecycle = this.signScheduler.onLifecycleEvent;
    this.signScheduler.onLifecycleEvent = (event) => {
      if (prevLifecycle) prevLifecycle(event);
      this._handleSchedulerLifecycle(event);
    };
  }

  start(t0 = null) {
    this.state = 'running';
    if (t0 !== null) {
      this.t0 = t0;
      this.timings.t0 = t0;
    } else if (this.t0 === null) {
      this.t0 = performance.now();
      this.timings.t0 = this.t0;
    }
    this.emitState();
  }

  pause() {
    this.state = 'paused';
    this.signScheduler.pause();
    this.emitState();
  }

  resume() {
    this.state = 'running';
    this.signScheduler.resume();
    this.emitState();
  }

  stop() {
    this.state = 'stopped';
    this.signScheduler.cancel();
    this.emitState();
  }

  reset() {
    this.state = 'idle';
    this.signScheduler.cancel();
    this.committedSigns = [];
    this.candidateSigns = [];
    this.trailingCandidates.clear();
    this.unknownWordsSet.clear();
    this.unavailableSignsSet.clear();
    this.lastProcessedText = '';
    this.lastTranslation = null;
    this.queueEntryTimes.clear();
    this.completedSignsCount = 0;
    this.totalSignsEnqueued = 0;
    this._queueCounter = 0;
    this.t0 = null;
    this.timings = {
      t0: null,
      t1: null,
      t2: null,
      t3: null,
      t4: null,
      firstSignId: null,
      finalTranscriptAt: null,
      finalSignCommittedAt: null,
    };
    this.emitState();
  }

  /**
   * Primary entry point: process incoming transcript events from Streaming ASR.
   * Handles both PARTIAL_TRANSCRIPT and FINAL_TRANSCRIPT.
   */
  handleTranscriptEvent(event) {
    if (this.state !== 'running') return;
    if (!event || !event.text) return;

    const now = performance.now();
    const isFinal = event.kind === 'FINAL_TRANSCRIPT';

    if (this.timings.t0 === null) {
      this.timings.t0 = event.audio_start_ms ?? now;
      this.t0 = this.timings.t0;
    }

    if (this.timings.t1 === null) {
      this.timings.t1 = now;
    }

    if (isFinal) {
      this.timings.finalTranscriptAt = now;
    }

    this._processTranscript(event.text, isFinal, event);
  }

  /**
   * Incremental commitment policy:
   * Maps current transcript tokens to sign candidates and commits safe prefixes.
   */
  _processTranscript(rawText, isFinal, event) {
    const processor = this.translator || this.sentenceProcessor;
    const normalized = processor.normalize(rawText);
    if (!normalized) return;

    const parsed = processor.process(normalized);
    this.lastTranslation = this.translator ? parsed : null;
    const allTokens = normalized.split(' ');

    // Register any unknown words reported by the parser
    for (const unknown of parsed.unknownWords) {
      this.unknownWordsSet.add(unknown);
    }

    const allSignIds = parsed.signIds;
    const committedCount = this.committedSigns.length;

    // Candidate signs that have not yet been committed to SignScheduler
    const candidateSignIds = allSignIds.slice(committedCount);
    this.candidateSigns = candidateSignIds;

    if (candidateSignIds.length === 0) {
      this.emitState();
      return;
    }

    const now = performance.now();
    const toCommit = [];

    if (isFinal) {
      // In a FINAL_TRANSCRIPT event, ALL remaining candidate signs are confirmed
      toCommit.push(...candidateSignIds);
      this.trailingCandidates.clear();
    } else {
      // In a PARTIAL_TRANSCRIPT event:
      // Separate signs into stable prefix signs vs. trailing in-flight signs.
      // A sign is a stable prefix if it does not correspond to the final token of the transcript.
      const lastToken = allTokens.at(-1);

      // Re-map tokens to inspect trailing sign
      for (let i = 0; i < candidateSignIds.length; i++) {
        const signId = candidateSignIds[i];
        const isLastCandidate = (i === candidateSignIds.length - 1);

        if (!isLastCandidate) {
          // Followed by another sign in the candidate list: guaranteed stable prefix!
          toCommit.push(signId);
        } else {
          // Trailing candidate sign:
          // Check if the phrase for this sign is trailing in the token stream
          const candidateKey = `${signId}@${committedCount + i}`;
          const currentTracker = this.trailingCandidates.get(candidateKey) || { count: 0, firstSeenAt: now };
          currentTracker.count += 1;
          this.trailingCandidates.set(candidateKey, currentTracker);

          const isStableByCount = currentTracker.count >= this.minTrailingObservations;
          const isStableByTime = (now - currentTracker.firstSeenAt) >= this.stabilityDelayMs;

          if (isStableByCount || isStableByTime) {
            toCommit.push(signId);
            this.trailingCandidates.delete(candidateKey);
          }
        }
      }
    }

    // Safely commit identified stable signs
    for (const signId of toCommit) {
      this._commitSign(signId, isFinal);
    }

    this.lastProcessedText = normalized;
    this.emitState();
  }

  /**
   * Commit a single sign ID to the SignScheduler, filtering out unplayable signs.
   */
  _commitSign(signId, isFinal) {
    const playability = this._checkPlayability(signId);

    if (!playability.playable) {
      // Report unavailable and skip scheduling; record as processed to prevent infinite loop
      this.unavailableSignsSet.add(signId);
      this.committedSigns.push({
        id: signId,
        status: 'UNAVAILABLE',
        reason: playability.reason,
        committedAt: performance.now(),
        enqueuedAt: null,
      });
      return;
    }

    const now = performance.now();

    if (this.timings.t2 === null) {
      this.timings.t2 = now;
      this.timings.firstSignId = signId;
    }

    // Enqueue to SignScheduler
    const queueKey = `${signId}#${++this._queueCounter}`;
    this.queueEntryTimes.set(queueKey, now);

    this.signScheduler.enqueue(signId);
    const enqueuedAt = performance.now();

    if (this.timings.t3 === null) {
      this.timings.t3 = enqueuedAt;
    }

    if (isFinal) {
      this.timings.finalSignCommittedAt = now;
    }

    this.totalSignsEnqueued += 1;
    const record = {
      id: signId,
      status: 'COMMITTED',
      committedAt: now,
      enqueuedAt,
      queueKey,
    };
    this.committedSigns.push(record);

    if (this.onCommit) {
      this.onCommit(record);
    }
  }

  /**
   * Verify if a sign is playable via SignLibrary.
   */
  _checkPlayability(signId) {
    if (!this.signLibrary) {
      return { playable: true };
    }
    try {
      this.signLibrary.getPlayable(signId, this.signScheduler.bonesMap);
      return { playable: true };
    } catch (err) {
      return { playable: false, reason: err.code || err.message };
    }
  }

  _handleSchedulerLifecycle(event) {
    if (event.type === 'playback_start') {
      if (this.timings.t4 === null) {
        this.timings.t4 = event.atMs;
      }
      // Remove oldest matching entry from queueEntryTimes
      for (const [key] of this.queueEntryTimes.entries()) {
        if (key.startsWith(`${event.id}#`)) {
          this.queueEntryTimes.delete(key);
          break;
        }
      }
    } else if (event.type === 'playback_end') {
      this.completedSignsCount += 1;
    }
    this.emitState();
  }

  /**
   * Diagnostic and backpressure telemetry.
   */
  getDiagnostics() {
    const now = performance.now();
    const schedulerState = this.signScheduler.getState();
    const queuedSigns = schedulerState.queued || [];
    const queueCount = queuedSigns.length;

    let oldestQueuedSign = null;
    let queueAgeMs = 0;

    if (this.queueEntryTimes.size > 0) {
      const oldestEntry = this.queueEntryTimes.entries().next().value;
      if (oldestEntry) {
        const [oldestKey, oldestTime] = oldestEntry;
        oldestQueuedSign = oldestKey.split('#')[0];
        queueAgeMs = Math.max(0, now - oldestTime);
      }
    }

    // End-to-end latencies
    const t0 = this.timings.t0;
    const t1 = this.timings.t1;
    const t2 = this.timings.t2;
    const t3 = this.timings.t3;
    const t4 = this.timings.t4;

    const firstPartialLatencyMs = (t0 !== null && t1 !== null) ? (t1 - t0) : null;
    const firstCommitLatencyMs = (t0 !== null && t2 !== null) ? (t2 - t0) : null;
    const schedulerEnqueueLatencyMs = (t2 !== null && t3 !== null) ? (t3 - t2) : null;
    const speechToAetherLatencyMs = (t0 !== null && t4 !== null) ? (t4 - t0) : null;

    const playableCommitted = this.committedSigns.filter(s => s.status === 'COMMITTED').map(s => s.id);

    return {
      state: this.state,
      signsCommitted: playableCommitted.length,
      committedSignIds: playableCommitted,
      currentSign: schedulerState.current,
      queuedSigns,
      queueCount,
      queueAgeMs: Math.round(queueAgeMs),
      oldestQueuedSign,
      signsCompleted: this.completedSignsCount,
      unknownWords: Array.from(this.unknownWordsSet),
      unavailableSigns: Array.from(this.unavailableSignsSet),
      candidateSigns: this.candidateSigns,
      translation: this.lastTranslation,
      timings: {
        t0,
        t1,
        t2,
        t3,
        t4,
        firstPartialLatencyMs,
        firstCommitLatencyMs,
        schedulerEnqueueLatencyMs,
        speechToAetherLatencyMs,
      },
      fallsBehind: queueCount > 2 || queueAgeMs > 3000,
    };
  }

  emitState() {
    const diag = this.getDiagnostics();
    if (this.onDiagnostics) this.onDiagnostics(diag);
    if (this.onStateChange) this.onStateChange(diag);
  }
}

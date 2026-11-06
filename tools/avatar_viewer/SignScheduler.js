/** Queue-based sign playback using preloaded SignLibrary definitions. */
export class SignScheduler {
  static MAX_QUEUE_SIZE = 512;
  static MAX_PROCESSED_EVENTS = 5000;

  constructor(player, library, bonesMap, onStateChange = null, onLifecycleEvent = null) {
    this.player = player;
    this.library = library;
    this.bonesMap = bonesMap;
    this.queue = [];
    this.currentId = null;
    this.currentEntry = null;
    this.isPaused = false;
    this.onStateChange = onStateChange;
    this.onLifecycleEvent = onLifecycleEvent;
    this.processedEvents = new Map();
    this.player.onCompleteCallback = () => this.completeCurrent();
  }

  enqueue(id, eventId = null, cueId = null, jobId = null, metadata = {}) {
    const normalizedId = typeof id === 'string' ? id.trim().toLowerCase() : '';
    const identity = `${normalizedId}\u0000${jobId ?? ''}\u0000${cueId ?? ''}`
      + `\u0000${metadata.cueStartSeconds ?? ''}\u0000${metadata.cueEndSeconds ?? ''}`;
    if (eventId !== null) {
      if (typeof eventId !== 'string' || !eventId || eventId.length > 256) {
        return { accepted: false, reason: 'INVALID_EVENT_ID' };
      }
      const previous = this.processedEvents.get(eventId);
      if (previous) {
        if (previous.identity !== identity) return { accepted: false, reason: 'EVENT_ID_CONFLICT' };
        return { ...previous.result, duplicate: true };
      }
    }

    let reason = '';
    if (!/^[a-z0-9_]{1,80}$/.test(normalizedId)) reason = 'INVALID_SIGN_ID';
    else if (jobId !== null && (typeof jobId !== 'string' || !jobId || jobId.length > 256)) reason = 'INVALID_JOB_ID';
    else if (cueId !== null && (typeof cueId !== 'string' || !cueId || cueId.length > 256)) reason = 'INVALID_CUE_ID';
    else if (cueId !== null && jobId === null) reason = 'MISSING_JOB_ID';
    else if (this.queue.length >= SignScheduler.MAX_QUEUE_SIZE) reason = 'QUEUE_FULL';

    let playable = null;
    if (!reason) {
      try {
        playable = this.library.getPlayable(normalizedId, this.bonesMap);
      } catch (error) {
        if (error instanceof Error && error.name === 'SignLibraryError') {
          reason = error.code || 'SIGN_NOT_PLAYABLE';
        } else {
          throw error;
        }
      }
      if (!reason && !playable) reason = 'SIGN_NOT_PLAYABLE';
    }

    if (reason) {
      const result = { accepted: false, reason };
      if (eventId) {
        this.rememberEvent(eventId, identity, result);
        this.emitLifecycle('playback_rejected', {
          id: normalizedId || 'unavailable',
          eventId,
          cueId,
          jobId
        }, { reason });
      }
      return result;
    }

    const entry = {
      id: normalizedId,
      playable,
      eventId,
      cueId,
      jobId,
      cueStartSeconds: metadata.cueStartSeconds ?? null,
      cueEndSeconds: metadata.cueEndSeconds ?? null
    };
    const result = { accepted: true };
    if (eventId) this.rememberEvent(eventId, identity, result);
    this.queue.push(entry);
    this.emitLifecycle('accepted', entry);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) {
      console.debug('[SignScheduler] enqueue', {
        queueLength: this.queue.length,
        current: Boolean(this.currentId),
        duplicateSuppressed: false
      });
    }
    if (!this.currentId && !this.isPaused) {
      this.startNext();
    } else if (this.currentEntry && this.currentEntry.cueId === cueId && this.currentEntry.jobId === jobId) {
      if (Number.isFinite(metadata.cueStartSeconds) && Number.isFinite(metadata.cueEndSeconds)) {
        const cueWindowMs = (metadata.cueEndSeconds - metadata.cueStartSeconds) * 1000;
        if (cueWindowMs > 400) {
          const allCueSigns = [this.currentEntry, ...this.queue.filter(q => q.cueId === cueId && q.jobId === jobId)];
          const totalSignDurationMs = allCueSigns.reduce((acc, q) => acc + (q.playable?.duration_ms || 1700), 0);
          if (totalSignDurationMs > cueWindowMs) {
            this.player.playbackSpeed = Math.min(2.2, Math.max(1.0, totalSignDurationMs / cueWindowMs));
          }
        }
      }
    }
    this.emit();
    return result;
  }

  rememberEvent(eventId, identity, result) {
    this.processedEvents.set(eventId, { identity, result });
    while (this.processedEvents.size > SignScheduler.MAX_PROCESSED_EVENTS) {
      this.processedEvents.delete(this.processedEvents.keys().next().value);
    }
  }

  advanceCue(jobId, cueId) {
    if (typeof jobId !== 'string' || !jobId) return;
    const retained = [];
    for (const item of this.queue) {
      if (item.jobId !== jobId || item.cueId === cueId) {
        retained.push(item);
      } else {
        this.emitLifecycle('playback_cancelled', item);
      }
    }
    this.queue = retained;
    this.emit();
  }

  enqueueMany(ids) { ids.forEach(id => this.enqueue(id)); }

  startNext() {
    if (this.isPaused || this.currentEntry) return;
    while (this.queue.length) {
      const next = this.queue.shift();
      this.currentId = next.id;
      this.currentEntry = next;
      try {
        // Dynamic Pacing Engine: Adapt playback tempo to match speech segment window
        if (Number.isFinite(next.cueStartSeconds) && Number.isFinite(next.cueEndSeconds)) {
          const cueWindowMs = (next.cueEndSeconds - next.cueStartSeconds) * 1000;
          if (cueWindowMs > 400) {
            const sameCueRemaining = [next, ...this.queue.filter(q => q.cueId === next.cueId && q.jobId === next.jobId)];
            const totalSignDurationMs = sameCueRemaining.reduce((acc, q) => acc + (q.playable?.duration_ms || 1700), 0);
            if (totalSignDurationMs > cueWindowMs) {
              const tempo = Math.min(2.2, Math.max(1.0, totalSignDurationMs / cueWindowMs));
              this.player.playbackSpeed = tempo;
            } else {
              this.player.playbackSpeed = 1.0;
            }
          } else {
            this.player.playbackSpeed = 1.0;
          }
        } else {
          this.player.playbackSpeed = 1.0;
        }

        this.player.loadSign(next.playable);
        this.player.play();
        this.emitLifecycle('playback_start', next, { durationMs: next.playable.duration_ms });
        if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] playback_start');
        this.emit();
        return;
      } catch (error) {
        this.currentId = null;
        this.currentEntry = null;
        try {
          this.player.stop();
        } catch (cleanupError) {
          console.error('[SignScheduler] Failed to stop a sign after playback setup failed:', cleanupError);
        }
        this.emitLifecycle('playback_failed', next, { reason: error.message || 'PLAYER_START_FAILED' });
        console.error('[SignScheduler] Unable to start sign playback:', error);
      }
    }
    this.currentId = null;
    this.currentEntry = null;
    this.player.stop();
    this.emit();
  }

  completeCurrent() {
    if (!this.currentEntry) return;
    const completed = this.currentEntry;
    this.emitLifecycle('playback_end', completed);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] playback_end');
    this.currentId = null;
    this.currentEntry = null;
    if (!this.isPaused) this.startNext();
    else this.emit();
  }

  cancelEvent(eventId, reason = 'CANCELLED') {
    const queuedIndex = this.queue.findIndex(item => item.eventId === eventId);
    if (queuedIndex >= 0) {
      const [item] = this.queue.splice(queuedIndex, 1);
      this.emitLifecycle('playback_cancelled', item, { reason });
      this.emit();
      return true;
    }
    if (this.currentEntry?.eventId !== eventId) return false;
    const cancelled = this.currentEntry;
    this.currentEntry = null;
    this.currentId = null;
    this.player.stop();
    this.emitLifecycle('playback_cancelled', cancelled, { reason });
    if (!this.isPaused) this.startNext();
    else this.emit();
    return true;
  }

  cancelJob(jobId, reason = 'JOB_CANCELLED') {
    if (typeof jobId !== 'string' || !jobId) return 0;
    let cancelledCount = 0;
    const retained = [];
    for (const item of this.queue) {
      if (item.jobId === jobId) {
        cancelledCount += 1;
        this.emitLifecycle('playback_cancelled', item, { reason });
      } else {
        retained.push(item);
      }
    }
    this.queue = retained;
    if (this.currentEntry?.jobId === jobId) {
      const cancelled = this.currentEntry;
      this.currentEntry = null;
      this.currentId = null;
      cancelledCount += 1;
      this.player.stop();
      this.emitLifecycle('playback_cancelled', cancelled, { reason });
    }
    if (!this.currentEntry && !this.isPaused) this.startNext();
    else this.emit();
    return cancelledCount;
  }

  pause() { this.isPaused = true; this.player.pause(); this.emit(); }
  resume() { this.isPaused = false; if (this.currentId) this.player.play(); else this.startNext(); this.emit(); }

  cancel() {
    if (this.currentEntry) {
      this.emitLifecycle('playback_cancelled', this.currentEntry, { reason: 'RESET' });
    }
    this.queue.forEach(item => this.emitLifecycle('playback_cancelled', item, { reason: 'RESET' }));
    this.queue = [];
    this.currentId = null;
    this.currentEntry = null;
    this.isPaused = false;
    this.player.stop();
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] reset');
    this.emit();
  }

  getState() {
    return {
      current: this.currentId,
      currentEventId: this.currentEntry?.eventId || null,
      currentJobId: this.currentEntry?.jobId || null,
      currentCueId: this.currentEntry?.cueId || null,
      queued: this.queue.map(item => item.id),
      currentTimeMs: this.player.currentTimeMs,
      paused: this.isPaused
    };
  }

  emit() { if (this.onStateChange) this.onStateChange(this.getState()); }

  emitLifecycle(type, entry, extra = {}) {
    if (!this.onLifecycleEvent || !entry?.eventId) return;
    this.onLifecycleEvent({
      type,
      id: entry.id,
      eventId: entry.eventId,
      jobId: entry.jobId ?? null,
      cueId: entry.cueId ?? null,
      cueStartSeconds: entry.cueStartSeconds ?? null,
      cueEndSeconds: entry.cueEndSeconds ?? null,
      atMs: performance.now(),
      ...extra
    });
  }
}

/** Queue-based sign playback using preloaded SignLibrary definitions. */
export class SignScheduler {
  static MAX_QUEUE_SIZE = 512;

  constructor(player, library, bonesMap, onStateChange = null, onLifecycleEvent = null) {
    this.player = player;
    this.library = library;
    this.bonesMap = bonesMap;
    this.queue = [];
    this.currentId = null;
    this.isPaused = false;
    this.onStateChange = onStateChange;
    this.onLifecycleEvent = onLifecycleEvent;
    this.player.onCompleteCallback = () => this.completeCurrent();
  }

  enqueue(id, eventId = null, cueId = null, jobId = null) {
    const normalizedId = String(id).trim().toLowerCase();
    if (!normalizedId) return { accepted: false, reason: 'INVALID_SIGN_ID' };
    if (this.queue.length >= SignScheduler.MAX_QUEUE_SIZE) {
      return { accepted: false, reason: 'QUEUE_FULL' };
    }
    let playable;
    try {
      playable = this.library.getPlayable(normalizedId, this.bonesMap);
    } catch (error) {
      if (error instanceof Error && error.name === 'SignLibraryError') {
        return { accepted: false, reason: error.code || 'SIGN_NOT_PLAYABLE' };
      }
      throw error;
    }
    if (!playable) return { accepted: false, reason: 'SIGN_NOT_PLAYABLE' };
    this.queue.push({ id: normalizedId, playable, eventId, cueId, jobId });
    this.emitLifecycle('accepted', normalizedId, eventId);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) {
      console.debug('[SignScheduler] enqueue', { queueLength: this.queue.length, current: Boolean(this.currentId), duplicateSuppressed: false });
    }
    if (!this.currentId && !this.isPaused) this.startNext();
    this.emit();
    return { accepted: true };
  }

  advanceCue(jobId, cueId) {
    const retained = [];
    for (const item of this.queue) {
      if (item.jobId === null || (item.jobId === jobId && item.cueId === cueId)) {
        retained.push(item);
      } else {
        this.emitLifecycle('playback_cancelled', item.id, item.eventId);
      }
    }
    this.queue = retained;
    this.emit();
  }

  enqueueMany(ids) { ids.forEach(id => this.enqueue(id)); }

  startNext() {
    const next = this.queue.shift();
    if (!next) {
      this.currentId = null;
      this.player.stop();
      this.emit();
      return;
    }
    this.currentId = next.id;
    this.currentEntry = next;
    this.player.loadSign(next.playable); // Safe neutral transition before each sign.
    this.player.play();
    this.emitLifecycle('playback_start', next.id, next.eventId);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] playback_start');
    this.emit();
  }

  completeCurrent() {
    if (this.currentEntry) this.emitLifecycle('playback_end', this.currentEntry.id, this.currentEntry.eventId);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] playback_end');
    this.currentId = null;
    this.currentEntry = null;
    if (!this.isPaused) this.startNext();
    else this.emit();
  }

  pause() { this.isPaused = true; this.player.pause(); this.emit(); }
  resume() { this.isPaused = false; if (this.currentId) this.player.play(); else this.startNext(); this.emit(); }
  cancel() {
    if (this.currentEntry) {
      this.emitLifecycle('playback_cancelled', this.currentEntry.id, this.currentEntry.eventId);
    }
    this.queue.forEach(item => this.emitLifecycle('playback_cancelled', item.id, item.eventId));
    this.queue = [];
    this.currentId = null;
    this.currentEntry = null;
    this.isPaused = false;
    this.player.stop();
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] reset');
    this.emit();
  }

  getState() {
    return { current: this.currentId, queued: this.queue.map(item => item.id), currentTimeMs: this.player.currentTimeMs, paused: this.isPaused };
  }

  emit() { if (this.onStateChange) this.onStateChange(this.getState()); }
  emitLifecycle(type, id, eventId = null) {
    if (this.onLifecycleEvent) this.onLifecycleEvent({ type, id, eventId, atMs: performance.now() });
  }
}

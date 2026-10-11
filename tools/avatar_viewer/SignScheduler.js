/** Queue-based sign playback using preloaded SignLibrary definitions. */
export class SignScheduler {
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

  enqueue(id) {
    const normalizedId = String(id).trim().toLowerCase();
    const playable = this.library.getPlayable(normalizedId, this.bonesMap);
    this.queue.push({ id: normalizedId, playable });
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) {
      console.debug('[SignScheduler] enqueue', { queueLength: this.queue.length, current: Boolean(this.currentId), duplicateSuppressed: false });
    }
    if (!this.currentId && !this.isPaused) this.startNext();
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
    this.player.loadSign(next.playable); // Safe neutral transition before each sign.
    this.player.play();
    this.emitLifecycle('playback_start', next.id);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] playback_start');
    this.emit();
  }

  completeCurrent() {
    if (this.currentId) this.emitLifecycle('playback_end', this.currentId);
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] playback_end');
    this.currentId = null;
    if (!this.isPaused) this.startNext();
    else this.emit();
  }

  pause() { this.isPaused = true; this.player.pause(); this.emit(); }
  resume() { this.isPaused = false; if (this.currentId) this.player.play(); else this.startNext(); this.emit(); }
  cancel() {
    this.queue = [];
    this.currentId = null;
    this.isPaused = false;
    this.player.stop();
    if (globalThis.__SPEECH_DIAGNOSTICS__ === true) console.debug('[SignScheduler] reset');
    this.emit();
  }

  getState() {
    return { current: this.currentId, queued: this.queue.map(item => item.id), currentTimeMs: this.player.currentTimeMs, paused: this.isPaused };
  }

  emit() { if (this.onStateChange) this.onStateChange(this.getState()); }
  emitLifecycle(type, id) { if (this.onLifecycleEvent) this.onLifecycleEvent({ type, id, atMs: performance.now() }); }
}

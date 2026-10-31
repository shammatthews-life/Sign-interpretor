/**
 * Synchronizes timestamped sign cues to the active YouTube video clock.
 */
(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLTimelineSynchronizer = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  class YouTubeTimelineSynchronizer {
    constructor({
      videoElement = null,
      onDispatchSign = null,
      onDispatchCommand = null,
      onFallback = null,
      onClearFallback = null
    } = {}) {
      this.video = null;
      this.onDispatchSign = onDispatchSign;
      this.onDispatchCommand = onDispatchCommand;
      this.onFallback = onFallback;
      this.onClearFallback = onClearFallback;
      this.segments = [];
      this.currentSegmentIndex = -1;
      this.activeCueId = null;
      this.activeCueKey = null;
      this.activationSequence = 0;
      this.activeJobId = null;
      this.isSeeking = false;
      this.boundEvents = [];
      if (videoElement) this.attach(videoElement);
    }

    setCueManifest(manifest, expectedVideoId = null) {
      if (!manifest || manifest.schema_version !== '1.0.0' || !Array.isArray(manifest.cues)) {
        throw new TypeError('Invalid YouTube cue manifest.');
      }
      if (!manifest.playback_ready) throw new TypeError('YouTube cue manifest failed timestamp validation.');
      if (expectedVideoId && manifest.video_id !== expectedVideoId) {
        throw new TypeError('Cue manifest video ID does not match the active YouTube video.');
      }
      if (!manifest.job_id || !manifest.fingerprint) {
        throw new TypeError('Cue manifest is missing its job identity or fingerprint.');
      }
      this.setSegments(manifest.cues.map(cue => ({
        ...cue,
        id: cue.cue_id,
        signIds: Array.isArray(cue.sign_ids) ? cue.sign_ids : [],
        signOccurrences: Array.isArray(cue.sign_occurrences) ? cue.sign_occurrences : [],
        fallbackWords: Array.isArray(cue.fallback_words) ? cue.fallback_words : [],
        fallbackMessage: cue.fallback_message || ''
      })), manifest.job_id);
      this.manifestFingerprint = manifest.fingerprint;
      this.videoId = manifest.video_id;
    }

    setSegments(segments = [], jobId = null) {
      if (!Array.isArray(segments)) throw new TypeError('YouTube cues must be an array.');
      let previousStart = -Infinity;
      let previousEnd = -Infinity;
      const validated = segments.map((segment, index) => {
        const id = segment?.id || segment?.cue_id;
        const start = segment?.start;
        const end = segment?.end;
        if (typeof id !== 'string' || !id || !Number.isFinite(start) || !Number.isFinite(end) || start < 0 || end <= start) {
          throw new TypeError(`Invalid timestamped cue at index ${index}.`);
        }
        if (start < previousStart || start < previousEnd) {
          throw new TypeError(`Cue order or overlap is invalid at index ${index}.`);
        }
        if (segment.signIds !== undefined && (!Array.isArray(segment.signIds)
          || segment.signIds.some(signId => typeof signId !== 'string' || !signId))) {
          throw new TypeError(`Invalid playable sign occurrences in cue ${id}.`);
        }
        if (segment.fallbackWords !== undefined && (!Array.isArray(segment.fallbackWords)
          || segment.fallbackWords.some(word => typeof word !== 'string'))) {
          throw new TypeError(`Invalid fallback words in cue ${id}.`);
        }
        previousStart = start;
        previousEnd = end;
        return {
          ...segment,
          id,
          signIds: segment.signIds || [],
          fallbackWords: segment.fallbackWords || [],
          signOccurrences: segment.signOccurrences || []
        };
      });
      this.clearActiveCue();
      this.segments = validated;
      this.activeJobId = jobId;
      this.manifestFingerprint = null;
      this.videoId = null;
      this.currentSegmentIndex = -1;
    }

    attach(videoElement) {
      if (this.video === videoElement) return;
      this.detach();
      this.video = videoElement;
      if (!this.video) return;
      const handlers = {
        timeupdate: () => this.handleTimeUpdate(),
        play: () => this.handlePlay(),
        pause: () => this.handlePause(),
        seeking: () => this.handleSeeking(),
        seeked: () => this.handleSeeked(),
        ratechange: () => this.handleRateChange()
      };
      for (const [event, handler] of Object.entries(handlers)) {
        this.video.addEventListener(event, handler);
        this.boundEvents.push([event, handler]);
      }
      this.handleRateChange();
    }

    detach() {
      if (this.video) {
        for (const [event, handler] of this.boundEvents) this.video.removeEventListener(event, handler);
      }
      this.boundEvents = [];
      this.clearActiveCue();
      this.video = null;
      this.currentSegmentIndex = -1;
      this.isSeeking = false;
    }

    rebind(newVideoElement) {
      if (this.video === newVideoElement) return;
      this.attach(newVideoElement);
      if (newVideoElement && !newVideoElement.paused) this.evaluateCurrentTime();
    }

    findSegmentIndex(currentTime) {
      return this.segments.findIndex(segment => currentTime >= segment.start && currentTime < segment.end);
    }

    handleTimeUpdate() {
      if (!this.video || this.video.paused || this.isSeeking) return;
      this.evaluateCurrentTime();
    }

    evaluateCurrentTime() {
      if (!this.video || this.isSeeking || !Number.isFinite(this.video.currentTime)) return;
      const index = this.findSegmentIndex(this.video.currentTime);
      this.currentSegmentIndex = index;
      const segment = index < 0 ? null : this.segments[index];
      if (!segment) {
        if (this.activeCueId !== null) this.clearActiveCue();
        return;
      }
      const cueKey = `${this.activeJobId || ''}:${segment.id}`;
      if (cueKey === this.activeCueKey) return;
      this.activateSegment(segment, cueKey);
    }

    activateSegment(segment, cueKey) {
      this.clearActiveCue();
      const activationId = `${cueKey}:${++this.activationSequence}`;
      this.activeCueKey = cueKey;
      this.activeCueId = activationId;
      if (segment.signIds.length) {
        this.onClearFallback?.();
        segment.signIds.forEach((signId, occurrenceIndex) => {
          const occurrence = segment.signOccurrences[occurrenceIndex];
          this.onDispatchSign?.(signId, {
            cueId: segment.id,
            jobId: this.activeJobId,
            occurrenceIndex,
            eventId: `${activationId}:${occurrence?.occurrence_id || `sign:${occurrenceIndex}`}`,
            command: occurrenceIndex === 0 ? 'PLAY_SIGN' : 'QUEUE_SIGN'
          });
        });
      } else {
        this.onDispatchCommand?.('RESET_AVATAR');
      }
      const fallbackMessage = segment.fallbackMessage
        || (segment.fallbackWords.length
          ? `Sign not available for: ${segment.fallbackWords.join(', ')}. Original text: ${segment.source_text || segment.text || ''}`
          : '');
      if (fallbackMessage) this.onFallback?.(fallbackMessage);
      else this.onClearFallback?.();
    }

    clearActiveCue() {
      if (this.activeCueId !== null) this.onDispatchCommand?.('RESET_AVATAR');
      this.activeCueId = null;
      this.activeCueKey = null;
      this.onClearFallback?.();
    }

    handlePlay() {
      this.onDispatchCommand?.('RESUME');
      this.evaluateCurrentTime();
    }

    handlePause() {
      this.onDispatchCommand?.('PAUSE');
    }

    handleSeeking() {
      this.isSeeking = true;
      this.clearActiveCue();
      this.currentSegmentIndex = -1;
    }

    handleSeeked() {
      this.isSeeking = false;
      this.evaluateCurrentTime();
    }

    handleRateChange() {
      if (!this.video) return;
      const rate = Number(this.video.playbackRate);
      if (Number.isFinite(rate) && rate > 0) {
        this.onDispatchCommand?.('SET_PLAYBACK_RATE', { rate });
      }
    }
  }

  return { YouTubeTimelineSynchronizer };
});

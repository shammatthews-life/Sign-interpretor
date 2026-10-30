/**
 * extension/content/timeline-synchronizer.js
 *
 * Phase H21: Hardened YouTube Video Playback Timeline Synchronizer.
 * Coordinates HTML5 <video> playback events with the ISL Avatar Viewer:
 * - video.currentTime synchronization with timestamped transcript segments
 * - Play / Pause event dispatch to Aether
 * - Seek detection: queue cancellation, avatar reset, and transcript repositioning
 * - Playback rate scaling (SET_PLAYBACK_RATE command relay)
 * - Honest subtitle fallback display synchronized to segment boundaries
 * - Bounded queue capacity (max 100 entries) preventing memory accumulation
 * - SPA resilient rebind to handle YouTube dynamic video element replacement
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
      onClearFallback = null,
      maxQueueCapacity = 100
    } = {}) {
      this.video = videoElement;
      this.onDispatchSign = onDispatchSign;
      this.onDispatchCommand = onDispatchCommand;
      this.onFallback = onFallback;
      this.onClearFallback = onClearFallback;
      this.maxQueueCapacity = maxQueueCapacity;

      this.segments = []; // [{ id, start, end, text, signIds, fallbackWords }]
      this.currentSegmentIndex = -1;
      this.lastDispatchedSegmentId = null;
      this.isSeeking = false;
      this.dispatchedQueue = [];
      this.boundEvents = [];

      if (this.video) {
        this.attach(this.video);
      }
    }

    setSegments(segments = []) {
      // Sort segments ascending by start timestamp
      this.segments = [...segments].sort((a, b) => (a.start ?? 0) - (b.start ?? 0));
      this.currentSegmentIndex = -1;
      this.lastDispatchedSegmentId = null;
      this.dispatchedQueue = [];
    }

    attach(videoElement) {
      this.detach();
      this.video = videoElement;
      if (!this.video) return;

      const onTimeUpdate = () => this.handleTimeUpdate();
      const onPlay = () => this.handlePlay();
      const onPause = () => this.handlePause();
      const onSeeking = () => this.handleSeeking();
      const onSeeked = () => this.handleSeeked();
      const onRateChange = () => this.handleRateChange();

      this.video.addEventListener('timeupdate', onTimeUpdate);
      this.video.addEventListener('play', onPlay);
      this.video.addEventListener('pause', onPause);
      this.video.addEventListener('seeking', onSeeking);
      this.video.addEventListener('seeked', onSeeked);
      this.video.addEventListener('ratechange', onRateChange);

      this.boundEvents = [
        ['timeupdate', onTimeUpdate],
        ['play', onPlay],
        ['pause', onPause],
        ['seeking', onSeeking],
        ['seeked', onSeeked],
        ['ratechange', onRateChange]
      ];
    }

    detach() {
      if (this.video && this.boundEvents.length) {
        for (const [event, handler] of this.boundEvents) {
          this.video.removeEventListener(event, handler);
        }
      }
      this.boundEvents = [];
      this.video = null;
      this.currentSegmentIndex = -1;
      this.lastDispatchedSegmentId = null;
      this.dispatchedQueue = [];
    }

    rebind(newVideoElement) {
      if (this.video === newVideoElement) return;
      this.detach();
      if (newVideoElement) {
        this.attach(newVideoElement);
      }
    }

    handleTimeUpdate() {
      if (!this.video || this.isSeeking || !this.segments.length) return;
      const currentTime = this.video.currentTime;

      // Find the segment matching current time
      const index = this.segments.findIndex(seg => currentTime >= seg.start && currentTime <= seg.end);
      if (index === -1) {
        return;
      }

      const activeSegment = this.segments[index];
      if (activeSegment.id !== this.lastDispatchedSegmentId) {
        this.currentSegmentIndex = index;
        this.lastDispatchedSegmentId = activeSegment.id;
        this.dispatchSegment(activeSegment);
      }
    }

    dispatchSegment(segment) {
      if (!segment) return;

      // Track queue length
      if (this.dispatchedQueue.length >= this.maxQueueCapacity) {
        this.dispatchedQueue.shift(); // Drop oldest event if capacity reached
      }
      this.dispatchedQueue.push(segment.id);

      // If segment has playable signs, dispatch them to Aether
      if (Array.isArray(segment.signIds) && segment.signIds.length > 0) {
        if (this.onClearFallback) this.onClearFallback();
        for (const signId of segment.signIds) {
          if (this.onDispatchSign) this.onDispatchSign(signId);
        }
      } else if (Array.isArray(segment.fallbackWords) && segment.fallbackWords.length > 0) {
        // Fallback required: reset avatar to neutral, show honest subtitle
        if (this.onDispatchCommand) this.onDispatchCommand('RESET_AVATAR');
        const fallbackText = segment.fallbackWords.join(', ');
        if (this.onFallback) this.onFallback(fallbackText);
      } else if (segment.text) {
        // Fallback for full text
        if (this.onDispatchCommand) this.onDispatchCommand('RESET_AVATAR');
        if (this.onFallback) this.onFallback(segment.text);
      }
    }

    handlePlay() {
      if (this.onDispatchCommand) {
        this.onDispatchCommand('RESUME');
      }
    }

    handlePause() {
      if (this.onDispatchCommand) {
        this.onDispatchCommand('PAUSE');
      }
    }

    handleSeeking() {
      this.isSeeking = true;
      // Seek initiated: cancel stale queue immediately and reset avatar to neutral
      if (this.onDispatchCommand) {
        this.onDispatchCommand('RESET_AVATAR');
      }
      if (this.onClearFallback) {
        this.onClearFallback();
      }
      this.lastDispatchedSegmentId = null;
      this.dispatchedQueue = [];
    }

    handleSeeked() {
      this.isSeeking = false;
      if (!this.video) return;
      const currentTime = this.video.currentTime;

      // Reposition segment index
      const newIndex = this.segments.findIndex(seg => currentTime >= seg.start && currentTime <= seg.end);
      this.currentSegmentIndex = newIndex;
      if (newIndex !== -1) {
        const seg = this.segments[newIndex];
        this.lastDispatchedSegmentId = seg.id;
        this.dispatchSegment(seg);
      }
    }

    handleRateChange() {
      if (!this.video) return;
      const rate = this.video.playbackRate || 1.0;
      if (this.onDispatchCommand) {
        this.onDispatchCommand('SET_PLAYBACK_RATE', { rate });
      }
    }
  }

  return { YouTubeTimelineSynchronizer };
});

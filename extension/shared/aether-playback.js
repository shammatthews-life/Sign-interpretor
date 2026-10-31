(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLAetherPlayback = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const EVENT_TYPES = Object.freeze([
    'accepted',
    'playback_start',
    'playback_end',
    'playback_cancelled',
    'playback_failed',
    'playback_rejected',
    'playback_timeout'
  ]);
  const TERMINAL_STATES = new Set([
    'playback_end',
    'playback_cancelled',
    'playback_failed',
    'playback_rejected'
  ]);

  function validateLifecycleEvent(event) {
    if (!event || typeof event !== 'object' || Array.isArray(event)) {
      return { valid: false, error: 'Lifecycle event must be an object.' };
    }
    if (!EVENT_TYPES.includes(event.type)) {
      return { valid: false, error: 'Unknown playback lifecycle event.' };
    }
    if (typeof event.eventId !== 'string' || !event.eventId || event.eventId.length > 256) {
      return { valid: false, error: 'Lifecycle event requires a valid event ID.' };
    }
    if (typeof event.id !== 'string' || !/^[a-z0-9_]{1,80}$/.test(event.id)) {
      return { valid: false, error: 'Lifecycle event requires a valid sign ID.' };
    }
    if (event.jobId !== null && (typeof event.jobId !== 'string' || !event.jobId || event.jobId.length > 256)) {
      return { valid: false, error: 'Lifecycle event has an invalid job ID.' };
    }
    if (event.cueId !== null && (typeof event.cueId !== 'string' || !event.cueId || event.cueId.length > 256)) {
      return { valid: false, error: 'Lifecycle event has an invalid cue ID.' };
    }
    if (event.cueId !== null && event.jobId === null) {
      return { valid: false, error: 'Cue lifecycle events require a job ID.' };
    }
    if (!Number.isFinite(event.atMs) || event.atMs < 0) {
      return { valid: false, error: 'Lifecycle event has an invalid timestamp.' };
    }
    if (event.durationMs !== undefined && (!Number.isFinite(event.durationMs) || event.durationMs <= 0)) {
      return { valid: false, error: 'Lifecycle event has an invalid duration.' };
    }
    if (event.reason !== undefined && typeof event.reason !== 'string') {
      return { valid: false, error: 'Lifecycle event has an invalid failure reason.' };
    }
    return { valid: true };
  }

  class AetherPlaybackLedger {
    constructor(maxEntries = 5000) {
      if (!Number.isInteger(maxEntries) || maxEntries < 1) {
        throw new TypeError('Playback ledger size must be a positive integer.');
      }
      this.maxEntries = maxEntries;
      this.entries = new Map();
    }

    record(event, scope = '') {
      const validation = validateLifecycleEvent(event);
      if (!validation.valid) return validation;
      const key = `${scope}:${event.eventId}`;
      const identity = `${event.id}\u0000${event.jobId ?? ''}\u0000${event.cueId ?? ''}`;
      let entry = this.entries.get(key);
      if (entry && entry.identity !== identity) {
        return { valid: false, error: 'Event ID was reused for a different playback occurrence.' };
      }
      if (entry?.events.has(event.type)) {
        return {
          valid: true,
          accepted: false,
          duplicate: true,
          status: entry.status
        };
      }

      const previous = entry?.status || null;
      const validTransition = event.type === 'accepted'
        ? previous === null
        : event.type === 'playback_rejected'
          ? previous === null
          : event.type === 'playback_start'
            ? previous === 'accepted'
            : event.type === 'playback_end'
              ? previous === 'playback_start'
              : event.type === 'playback_cancelled' || event.type === 'playback_failed'
                || event.type === 'playback_timeout'
                ? previous === 'accepted' || previous === 'playback_start'
                  || (event.type !== 'playback_timeout' && previous === 'playback_timeout')
                : false;
      if (!validTransition || (entry && TERMINAL_STATES.has(entry.status))) {
        return {
          valid: false,
          error: `Invalid playback lifecycle transition from ${previous || 'none'} to ${event.type}.`
        };
      }

      if (!entry) {
        entry = {
          identity,
          signId: event.id,
          jobId: event.jobId,
          cueId: event.cueId,
          status: event.type,
          events: new Set(),
          history: []
        };
        this.entries.set(key, entry);
      } else {
        entry.status = event.type;
      }
      entry.events.add(event.type);
      entry.history.push({ ...event });
      while (this.entries.size > this.maxEntries) {
        this.entries.delete(this.entries.keys().next().value);
      }
      return { valid: true, accepted: true, duplicate: false, status: entry.status };
    }

    get(eventId, scope = '') {
      const entry = this.entries.get(`${scope}:${eventId}`);
      if (!entry) return null;
      return {
        signId: entry.signId,
        jobId: entry.jobId,
        cueId: entry.cueId,
        status: entry.status,
        history: entry.history.map(event => ({ ...event }))
      };
    }
  }

  return { EVENT_TYPES, validateLifecycleEvent, AetherPlaybackLedger };
});

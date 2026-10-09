/**
 * ISL Accessibility Translator - Message Contract (Phase H6)
 * Schema Version: 1.0.0
 *
 * Defines standard structured payloads, lifecycle states, and action constants
 * for communication between:
 *   - Content Script (Page Overlay)
 *   - Service Worker (Background coordinator)
 *   - Extension Popup (Toolbar UI)
 *   - Localhost Runtime (Streaming ASR & Aether Viewer)
 */

(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLMessageContract = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const CONTRACT_VERSION = '1.0.0';

  // 1. Core State Enums (Task H6-C)
  const STATES = Object.freeze({
    CONNECTION: Object.freeze({
      DISCONNECTED: 'DISCONNECTED',
      CONNECTING: 'CONNECTING',
      CONNECTED: 'CONNECTED',
      ERROR: 'ERROR'
    }),
    AUDIO: Object.freeze({
      IDLE: 'IDLE',
      LISTENING: 'LISTENING',
      PAUSED: 'PAUSED',
      STOPPED: 'STOPPED'
    }),
    ASR: Object.freeze({
      WAITING: 'WAITING',
      PARTIAL: 'PARTIAL',
      FINAL: 'FINAL',
      ERROR: 'ERROR'
    }),
    TRANSLATION: Object.freeze({
      IDLE: 'IDLE',
      TRANSLATING: 'TRANSLATING',
      READY: 'READY',
      PARTIAL: 'PARTIAL',
      HEURISTIC: 'HEURISTIC',
      UNCERTAIN: 'UNCERTAIN'
    }),
    SIGNING: Object.freeze({
      IDLE: 'IDLE',
      PLAYING: 'PLAYING',
      QUEUED: 'QUEUED',
      UNAVAILABLE: 'UNAVAILABLE'
    })
  });

  // 2. Structured Action / Event Types (Task H6-G)
  const MESSAGE_TYPES = Object.freeze({
    // Lifecycle & Bridge
    GET_STATE: 'GET_STATE',
    STATE_UPDATE: 'STATE_UPDATE',
    CONNECT_RUNTIME: 'CONNECT_RUNTIME',
    DISCONNECT_RUNTIME: 'DISCONNECT_RUNTIME',
    RUNTIME_STATUS: 'RUNTIME_STATUS',
    RUNTIME_ERROR: 'RUNTIME_ERROR',
    PING: 'PING',
    PONG: 'PONG',

    // Audio & ASR
    AUDIO_STATUS: 'AUDIO_STATUS',
    ASR_PARTIAL: 'ASR_PARTIAL',
    ASR_FINAL: 'ASR_FINAL',

    // Translation & Representation
    TRANSLATION_UPDATE: 'TRANSLATION_UPDATE',

    // Signing & Queue
    SIGN_QUEUE_UPDATE: 'SIGN_QUEUE_UPDATE',
    SIGN_STARTED: 'SIGN_STARTED',
    SIGN_FINISHED: 'SIGN_FINISHED',
    SIGN_UNAVAILABLE: 'SIGN_UNAVAILABLE',

    // H7 YouTube job lifecycle
    YOUTUBE_PROCESS: 'YOUTUBE_PROCESS',
    YOUTUBE_JOB_CREATED: 'YOUTUBE_JOB_CREATED',
    YOUTUBE_STATUS: 'YOUTUBE_STATUS',
    YOUTUBE_RESULT: 'YOUTUBE_RESULT',
    YOUTUBE_ERROR: 'YOUTUBE_ERROR',
    AETHER_PLAYBACK_STATE: 'AETHER_PLAYBACK_STATE',

    // Aether Viewer Command Interface (Task H6-E)
    AETHER_COMMAND: 'AETHER_COMMAND',

    // Deterministic Demo Controls (Task H6-D)
    DEMO_START: 'DEMO_START',
    DEMO_STEP: 'DEMO_STEP',
    DEMO_STOP: 'DEMO_STOP',
    DEMO_SET_SCENARIO: 'DEMO_SET_SCENARIO',

    // Overlay Visibility
    TOGGLE_OVERLAY: 'TOGGLE_OVERLAY',
    SET_OVERLAY_VISIBLE: 'SET_OVERLAY_VISIBLE'
  });

  // 3. Aether Avatar Command Actions
  const AETHER_COMMANDS = Object.freeze({
    PLAY_SIGN: 'PLAY_SIGN',
    QUEUE_SIGN: 'QUEUE_SIGN',
    RESET_AVATAR: 'RESET_AVATAR',
    PAUSE: 'PAUSE',
    RESUME: 'RESUME'
  });

  /**
   * Constructs the default initial state schema.
   */
  function createInitialState() {
    return {
      version: CONTRACT_VERSION,
      updatedAt: Date.now(),
      connection: STATES.CONNECTION.DISCONNECTED,
      audio: STATES.AUDIO.IDLE,
      asr: STATES.ASR.WAITING,
      translation: STATES.TRANSLATION.IDLE,
      signing: STATES.SIGNING.IDLE,
      runtimeEndpoint: 'http://localhost:8000',
      runtimeAvailable: false,
      runtimeError: null,
      overlayVisible: true,

      // Transcripts
      transcript: {
        partial: '',
        final: '',
        lastUpdated: null
      },

      // ISL-oriented Translation representation
      representation: {
        gloss: '',
        glossSequence: [],
        status: 'IDLE',
        trace: [],
        unknownTerms: [],
        candidateSignIds: [],
        playableSignIds: [],
        unavailableSignIds: []
      },

      // Sign playback queue
      signingQueue: {
        currentSign: null,
        queuedSigns: [],
        completedSigns: [],
        unavailableConcepts: [] // [{ word, reason }]
      },

      youtube: {
        jobId: null,
        state: 'IDLE',
        progress: 0,
        title: '',
        duration: null,
        audioDuration: null,
        segmentCount: 0,
        latestSegment: '',
        transcriptSummary: '',
        translationStatus: 'IDLE',
        translationStatusCounts: {},
        resultReady: false,
        glosses: [],
        playableSigns: [],
        currentSign: null,
        queuedSigns: [],
        unavailableConcepts: [],
        error: null
      },

      // Demo state machine
      demo: {
        active: false,
        scenario: 'greeting', // 'greeting' | 'missing_concept'
        step: 0,
        totalSteps: 0
      }
    };
  }

  /**
   * Wrap an action and payload in a versioned envelope.
   */
  function createMessage(type, payload = {}, correlationId = null) {
    if (!type || typeof type !== 'string') {
      throw new Error(`[ISLMessageContract] Invalid message type: ${type}`);
    }
    return {
      version: CONTRACT_VERSION,
      type,
      payload,
      correlationId: correlationId || `msg_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
      timestamp: Date.now()
    };
  }

  /**
   * Validates a message structure.
   */
  function validateMessage(msg) {
    if (!msg || typeof msg !== 'object') {
      return { valid: false, error: 'Message must be an object' };
    }
    if (!msg.type || typeof msg.type !== 'string') {
      return { valid: false, error: 'Message missing valid type string' };
    }
    if (!msg.version) {
      return { valid: false, error: 'Message missing version string' };
    }
    return { valid: true };
  }

  function validateYouTubeUrl(value) {
    if (typeof value !== 'string' || !value.trim()) {
      return { valid: false, error: 'Enter a YouTube video URL.' };
    }
    try {
      const url = new URL(value.trim());
      const host = url.hostname.toLowerCase();
      const allowed = host === 'youtu.be' || host === 'youtube.com'
        || host === 'www.youtube.com' || host === 'm.youtube.com';
      if (!allowed || url.protocol !== 'https:' && url.protocol !== 'http:') {
        return { valid: false, error: 'Enter a valid YouTube video URL.' };
      }
      const id = host === 'youtu.be'
        ? url.pathname.split('/').filter(Boolean)[0]
        : url.searchParams.get('v') || url.pathname.match(/^\/(?:shorts|embed)\/([^/]+)/)?.[1];
      if (!id || !/^[A-Za-z0-9_-]{11}$/.test(id)) {
        return { valid: false, error: 'The URL must identify one YouTube video.' };
      }
      return { valid: true, videoId: id, canonicalUrl: `https://www.youtube.com/watch?v=${id}` };
    } catch {
      return { valid: false, error: 'Enter a valid YouTube video URL.' };
    }
  }

  return {
    CONTRACT_VERSION,
    STATES,
    MESSAGE_TYPES,
    AETHER_COMMANDS,
    createInitialState,
    createMessage,
    validateMessage,
    validateYouTubeUrl
  };
});

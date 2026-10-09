/**
 * ISL Accessibility Translator - Deterministic Demo Data (Phase H6)
 *
 * Provides verifiable test sequences strictly adhering to existing repository state:
 * - Playable signs: HELLO, GOOD, MORNING (from signs/hello.json, signs/good.json, signs/morning.json)
 * - Incomplete/unauthored signs: WATER (MOTION_INCOMPLETE), I, NEED, ME, HELP (MOTION_NOT_AUTHORED)
 *
 * NO FAKE SIGN MOTION IS AUTHORED. NO LINGUISTIC FICTION.
 */

(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLDemoData = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const DEMO_SCENARIOS = {
    greeting: {
      id: 'greeting',
      title: 'Playable Greeting: "Hello good morning"',
      description: 'Exercises full incremental speech pipeline using verified signs (HELLO → GOOD → MORNING)',
      steps: [
        {
          stepIndex: 1,
          description: 'Streaming ASR emits partial transcript "hello"',
          audio: 'LISTENING',
          asr: 'PARTIAL',
          transcript: {
            partial: 'hello',
            final: ''
          },
          translation: {
            status: 'SUPPORTED',
            gloss: 'HELLO',
            glossSequence: ['HELLO'],
            candidateSignIds: ['hello'],
            playableSignIds: ['hello'],
            unavailableSignIds: [],
            unknownTerms: [],
            trace: [
              { stage: 'normalize', detail: 'hello' },
              { stage: 'phrase_detection', detail: 'Matched lexical phrase: hello' }
            ]
          },
          signing: 'PLAYING',
          signingQueue: {
            currentSign: 'hello',
            queuedSigns: [],
            completedSigns: [],
            unavailableConcepts: []
          }
        },
        {
          stepIndex: 2,
          description: 'Streaming ASR updates partial to "hello good"',
          audio: 'LISTENING',
          asr: 'PARTIAL',
          transcript: {
            partial: 'hello good',
            final: ''
          },
          translation: {
            status: 'SUPPORTED',
            gloss: 'HELLO GOOD',
            glossSequence: ['HELLO', 'GOOD'],
            candidateSignIds: ['hello', 'good'],
            playableSignIds: ['hello', 'good'],
            unavailableSignIds: [],
            unknownTerms: [],
            trace: [
              { stage: 'normalize', detail: 'hello good' },
              { stage: 'phrase_detection', detail: 'Matched lexical phrase: hello' },
              { stage: 'lexicon_lookup', detail: 'Matched word: good' }
            ]
          },
          signing: 'PLAYING',
          signingQueue: {
            currentSign: 'hello',
            queuedSigns: ['good'],
            completedSigns: [],
            unavailableConcepts: []
          }
        },
        {
          stepIndex: 3,
          description: 'Streaming ASR emits final transcript "hello good morning"',
          audio: 'LISTENING',
          asr: 'FINAL',
          transcript: {
            partial: 'hello good morning',
            final: 'hello good morning'
          },
          translation: {
            status: 'SUPPORTED',
            gloss: 'HELLO GOOD MORNING',
            glossSequence: ['HELLO', 'GOOD', 'MORNING'],
            candidateSignIds: ['hello', 'good', 'morning'],
            playableSignIds: ['hello', 'good', 'morning'],
            unavailableSignIds: [],
            unknownTerms: [],
            trace: [
              { stage: 'normalize', detail: 'hello good morning' },
              { stage: 'phrase_detection', detail: 'Matched phrases: hello, good morning' }
            ]
          },
          signing: 'PLAYING',
          signingQueue: {
            currentSign: 'hello',
            queuedSigns: ['good', 'morning'],
            completedSigns: [],
            unavailableConcepts: []
          }
        },
        {
          stepIndex: 4,
          description: 'Aether player finishes "hello", advances to "good"',
          audio: 'IDLE',
          asr: 'FINAL',
          transcript: {
            partial: 'hello good morning',
            final: 'hello good morning'
          },
          translation: {
            status: 'SUPPORTED',
            gloss: 'HELLO GOOD MORNING',
            glossSequence: ['HELLO', 'GOOD', 'MORNING'],
            candidateSignIds: ['hello', 'good', 'morning'],
            playableSignIds: ['hello', 'good', 'morning'],
            unavailableSignIds: [],
            unknownTerms: [],
            trace: [
              { stage: 'normalize', detail: 'hello good morning' }
            ]
          },
          signing: 'PLAYING',
          signingQueue: {
            currentSign: 'good',
            queuedSigns: ['morning'],
            completedSigns: ['hello'],
            unavailableConcepts: []
          }
        },
        {
          stepIndex: 5,
          description: 'Aether player finishes "good", advances to "morning"',
          audio: 'IDLE',
          asr: 'FINAL',
          transcript: {
            partial: 'hello good morning',
            final: 'hello good morning'
          },
          translation: {
            status: 'SUPPORTED',
            gloss: 'HELLO GOOD MORNING',
            glossSequence: ['HELLO', 'GOOD', 'MORNING'],
            candidateSignIds: ['hello', 'good', 'morning'],
            playableSignIds: ['hello', 'good', 'morning'],
            unavailableSignIds: [],
            unknownTerms: [],
            trace: [
              { stage: 'normalize', detail: 'hello good morning' }
            ]
          },
          signing: 'PLAYING',
          signingQueue: {
            currentSign: 'morning',
            queuedSigns: [],
            completedSigns: ['hello', 'good'],
            unavailableConcepts: []
          }
        },
        {
          stepIndex: 6,
          description: 'Aether playback completed. Player returns to neutral idle pose.',
          audio: 'IDLE',
          asr: 'WAITING',
          transcript: {
            partial: '',
            final: 'hello good morning'
          },
          translation: {
            status: 'READY',
            gloss: 'HELLO GOOD MORNING',
            glossSequence: ['HELLO', 'GOOD', 'MORNING'],
            candidateSignIds: ['hello', 'good', 'morning'],
            playableSignIds: ['hello', 'good', 'morning'],
            unavailableSignIds: [],
            unknownTerms: [],
            trace: []
          },
          signing: 'IDLE',
          signingQueue: {
            currentSign: null,
            queuedSigns: [],
            completedSigns: ['hello', 'good', 'morning'],
            unavailableConcepts: []
          }
        }
      ]
    },

    missing_concept: {
      id: 'missing_concept',
      title: 'Missing Motion Handling: "I need water"',
      description: 'Demonstrates robust error handling and transparent missing-sign feedback without fake animation',
      steps: [
        {
          stepIndex: 1,
          description: 'Speech received: "I need water" → Translation applies G2/G3 SOV heuristic: I WATER NEED',
          audio: 'IDLE',
          asr: 'FINAL',
          transcript: {
            partial: 'i need water',
            final: 'i need water'
          },
          translation: {
            status: 'HEURISTIC',
            gloss: 'I WATER NEED',
            glossSequence: ['I', 'WATER', 'NEED'],
            candidateSignIds: ['i', 'water', 'need'],
            playableSignIds: [],
            unavailableSignIds: ['water', 'i', 'need'],
            unknownTerms: [],
            trace: [
              { stage: 'normalize', detail: 'i need water' },
              { stage: 'lexicon_lookup', detail: 'Tokens matched in controlled lexicon' },
              { stage: 'restructure', detail: 'Controlled semantic-role order: I WATER NEED', basis: 'PROJECT_HEURISTIC' }
            ]
          },
          signing: 'UNAVAILABLE',
          signingQueue: {
            currentSign: null,
            queuedSigns: [],
            completedSigns: [],
            unavailableConcepts: [
              { word: 'water', reason: 'MOTION_INCOMPLETE (Pending H5 visual capture evidence)' },
              { word: 'i', reason: 'MOTION_NOT_AUTHORED (Missing candidate visual evidence)' },
              { word: 'need', reason: 'MOTION_NOT_AUTHORED (Missing candidate visual evidence)' }
            ]
          }
        }
      ]
    }
  };

  return {
    DEMO_SCENARIOS
  };
});

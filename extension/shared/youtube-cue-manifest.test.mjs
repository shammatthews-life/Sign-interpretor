import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { test } from 'node:test';

const require = createRequire(import.meta.url);
const { buildYoutubeCueManifest } = require('./youtube-cue-manifest.js');

function resultWith(transcript, translations) {
  return {
    video_id: 'MXKkXXYUxBc',
    transcript: { segments: transcript },
    translation: { translated_segments: translations }
  };
}

test('manifest preserves timestamped segment and repeated sign occurrences with explicit fallback', async () => {
  const transcript = [
    { start: 4.25, end: 6.5, text: 'Good good, something.' },
    { start: 8, end: 9, text: 'Morning.' }
  ];
  const translations = [
    {
      start: 4.25, end: 6.5, source_text: 'Good good, something.',
      gloss: ['GOOD', 'GOOD'], playable_signs: ['good', 'good'],
      candidate_sign_ids: ['good', 'good'], unavailable_concepts: [],
      unknown_terms: ['SOMETHING'], translation_status: 'TRANSLATION_UNCERTAIN'
    },
    {
      start: 8, end: 9, source_text: 'Morning.',
      gloss: ['MORNING'], playable_signs: ['morning'],
      candidate_sign_ids: ['morning'], unavailable_concepts: [],
      unknown_terms: [], translation_status: 'TRANSLATION_SUPPORTED'
    }
  ];

  const manifest = await buildYoutubeCueManifest('yt_job_1', resultWith(transcript, translations));
  assert.equal(manifest.playback_ready, true);
  assert.equal(manifest.cues.length, 2);
  assert.equal(manifest.cues[0].start, 4.25);
  assert.equal(manifest.cues[0].end, 6.5);
  assert.deepEqual(manifest.cues[0].sign_ids, ['good', 'good']);
  assert.equal(manifest.cues[0].sign_occurrences[0].occurrence_id, 'MXKkXXYUxBc_000001:sign:0');
  assert.equal(manifest.cues[0].sign_occurrences[1].occurrence_id, 'MXKkXXYUxBc_000001:sign:1');
  assert.deepEqual(manifest.cues[0].fallback_words, ['SOMETHING']);
  assert.match(manifest.cues[0].fallback_message, /Sign not available for: SOMETHING/);
  assert.equal(manifest.coverage.playable_sign_occurrences, 3);
  assert.equal(manifest.coverage.unknown_term_occurrences, 1);
  assert.match(manifest.fingerprint, /^sha256:[a-f0-9]{64}$/);
  assert.equal(manifest.fingerprint, (await buildYoutubeCueManifest('yt_job_1', resultWith(transcript, translations))).fingerprint);
});

test('source mismatch is not silently translated and gets an honest fallback cue', async () => {
  const result = resultWith(
    [{ start: 1, end: 2, text: 'Original transcript words.' }],
    [{ start: 1, end: 2, source_text: 'Different words.', gloss: ['HELLO'], playable_signs: ['hello'], unknown_terms: [] }]
  );
  const manifest = await buildYoutubeCueManifest('yt_job_2', result);
  assert.equal(manifest.cues.length, 1);
  assert.equal(manifest.cues[0].translation_aligned, false);
  assert.equal(manifest.cues[0].translation_status, 'UNAVAILABLE_SOURCE_TRANSLATION_MISMATCH');
  assert.deepEqual(manifest.cues[0].sign_ids, []);
  assert.deepEqual(manifest.cues[0].fallback_words, ['Original', 'transcript', 'words']);
  assert.deepEqual(manifest.cues[0].unknown_terms, []);
  assert.deepEqual(manifest.cues[0].fallback_occurrences.map(item => item.category), [
    'source_mismatch', 'source_mismatch', 'source_mismatch'
  ]);
  assert.equal(manifest.coverage.unknown_term_occurrences, 0);
  assert.equal(manifest.coverage.source_mismatch_fallback_occurrences, 3);
  assert.equal(manifest.unmatched_translations[0].reason, 'SOURCE_TEXT_MISMATCH');
});

test('extra translations and malformed overlapping cues are reported, not silently reordered', async () => {
  const result = resultWith(
    [
      { start: 1, end: 3, text: 'First.' },
      { start: 2, end: 4, text: 'Second.' }
    ],
    [
      { start: 1, end: 3, source_text: 'First.', gloss: [], playable_signs: [] },
      { start: 2, end: 4, source_text: 'Second.', gloss: [], playable_signs: [] },
      { start: 4, end: 5, source_text: 'Extra.', gloss: [], playable_signs: [] }
    ]
  );
  const manifest = await buildYoutubeCueManifest('yt_job_3', result);
  assert.equal(manifest.cues.length, 2);
  assert.equal(manifest.unmatched_translations[0].reason, 'NO_TRANSCRIPT_SEGMENT');
  assert.equal(manifest.playback_ready, false);
  assert.equal(manifest.validation_errors[0].code, 'OVERLAPPING_CUE');
});

test('translation timestamps require numeric values and segment identities must remain unique', async () => {
  const result = resultWith(
    [
      { id: 'same', start: 1, end: 2, text: 'First.' },
      { id: 'same', start: 3, end: 4, text: 'Second.' }
    ],
    [
      { id: 'same', start: '1', end: 2, source_text: 'First.', gloss: [], playable_signs: [] },
      { id: 'same', start: 3, end: 4, source_text: 'Second.', gloss: [], playable_signs: [] }
    ]
  );
  const manifest = await buildYoutubeCueManifest('yt_strict_timestamps', result);
  assert.equal(manifest.playback_ready, false);
  assert.ok(manifest.validation_errors.some(error => error.code === 'INVALID_TRANSLATION_TIMESTAMP'));
  assert.ok(manifest.validation_errors.some(error => error.code === 'DUPLICATE_SEGMENT_IDENTITY'));
  assert.ok(manifest.validation_errors.some(error => error.code === 'DUPLICATE_TRANSLATION_IDENTITY'));
  assert.equal(manifest.unmatched_translations[0].reason, 'INVALID_TRANSLATION_TIMESTAMP');
});

test('missing translation segments are represented by per-word fallback occurrences', async () => {
  const manifest = await buildYoutubeCueManifest(
    'yt_missing_translation',
    resultWith([{ start: 0, end: 1, text: 'A new word.' }], [])
  );
  assert.equal(manifest.cues.length, 1);
  assert.equal(manifest.cues[0].translation_status, 'UNAVAILABLE_TRANSLATION_MISSING');
  assert.deepEqual(manifest.cues[0].fallback_occurrences.map(item => item.category), [
    'translation_missing', 'translation_missing', 'translation_missing'
  ]);
  assert.equal(manifest.coverage.missing_translation_fallback_occurrences, 3);
  assert.equal(manifest.unmatched_translations[0].reason, 'TRANSLATION_MISSING');
});

test('malformed playable sign IDs prevent a success-shaped playback manifest', async () => {
  const manifest = await buildYoutubeCueManifest(
    'yt_bad_sign_id',
    resultWith(
      [{ start: 0, end: 1, text: 'Hello.' }],
      [{ start: 0, end: 1, source_text: 'Hello.', gloss: ['HELLO'], playable_signs: ['not a sign id'] }]
    )
  );
  assert.equal(manifest.playback_ready, false);
  assert.ok(manifest.validation_errors.some(error => error.code === 'INVALID_PLAYABLE_SIGN_ID'));
});

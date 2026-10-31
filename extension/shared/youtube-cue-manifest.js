(function (root, factory) {
  if (typeof exports === 'object' && typeof module !== 'undefined') {
    module.exports = factory();
  } else {
    root.ISLYouTubeCueManifest = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const SCHEMA_VERSION = '1.0.0';

  function getSubtleCrypto() {
    if (globalThis.crypto?.subtle) return globalThis.crypto.subtle;
    if (typeof require === 'function') return require('node:crypto').webcrypto.subtle;
    throw new Error('SHA-256 is unavailable; refusing to publish an unfingerprinted cue manifest.');
  }

  async function sha256(value) {
    const bytes = new TextEncoder().encode(value);
    const digest = await getSubtleCrypto().digest('SHA-256', bytes);
    return `sha256:${Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('')}`;
  }

  function normalizeText(value) {
    return String(value ?? '').normalize('NFC').trim();
  }

  function finiteTime(value) {
    return typeof value === 'number' && Number.isFinite(value) && value >= 0;
  }

  function normalizeUnavailable(items) {
    if (!Array.isArray(items)) return [];
    return items.map((item, index) => {
      if (typeof item === 'string') {
        return { order: index, word: item, reason: 'SIGN_NOT_AUTHORED', sign_id: item };
      }
      if (!item || typeof item !== 'object') {
        return { order: index, word: String(item ?? ''), reason: 'INVALID_UNAVAILABLE_CONCEPT', sign_id: '' };
      }
      const signId = String(item.sign_id || item.word || '');
      return {
        order: index,
        word: String(item.word || signId || 'unknown'),
        reason: String(item.reason || 'SIGN_NOT_AUTHORED'),
        sign_id: signId
      };
    });
  }

  function normalizeUnknown(items) {
    if (!Array.isArray(items)) return [];
    return items.map((item, index) => ({
      order: index,
      word: String(item ?? ''),
      reason: 'WORD_NOT_IN_TRANSLATION_CATALOG'
    })).filter(item => item.word.length > 0);
  }

  function tokenizeSource(text) {
    return String(text).match(/[\p{L}\p{N}]+(?:['’\-][\p{L}\p{N}]+)*/gu) || [];
  }

  async function buildYoutubeCueManifest(jobId, result) {
    if (!result || typeof result !== 'object') throw new TypeError('YouTube result must be an object.');
    const videoId = String(result.video_id || result.metadata?.video_id || '');
    if (!/^[A-Za-z0-9_-]{11}$/.test(videoId)) throw new TypeError('YouTube result has an invalid video ID.');
    if (typeof jobId !== 'string' || !jobId.trim()) throw new TypeError('A stable YouTube job ID is required.');

    const transcriptSegments = result.transcript?.segments;
    const translatedSegments = result.translation?.translated_segments;
    if (!Array.isArray(transcriptSegments) || !Array.isArray(translatedSegments)) {
      throw new TypeError('YouTube result must contain transcript and translated segment arrays.');
    }

    const transcriptIdentity = await sha256(JSON.stringify(transcriptSegments.map(segment => ({
      start: segment?.start,
      end: segment?.end,
      text: String(segment?.text ?? '')
    }))));
    const validationErrors = [];
    const unmatchedTranslations = [];
    const cues = [];
    let previousStart = -Infinity;
    let previousEnd = -Infinity;
    let playableOccurrences = 0;
    let fallbackOccurrenceCount = 0;
    let unknownTermOccurrences = 0;
    let sourceMismatchFallbackOccurrences = 0;
    let unavailableConceptOccurrences = 0;

    for (let index = 0; index < transcriptSegments.length; index += 1) {
      const segment = transcriptSegments[index];
      const start = segment?.start;
      const end = segment?.end;
      const sourceText = String(segment?.text ?? '');
      if (!finiteTime(start) || !finiteTime(end) || end <= start) {
        validationErrors.push({ segment_index: index, code: 'INVALID_TIMESTAMP', start, end });
      } else {
        if (start < previousStart) {
          validationErrors.push({ segment_index: index, code: 'OUT_OF_ORDER_TIMESTAMP', start, previous_start: previousStart });
        }
        if (start < previousEnd) {
          validationErrors.push({ segment_index: index, code: 'OVERLAPPING_CUE', start, previous_end: previousEnd });
        }
        previousStart = start;
        previousEnd = Math.max(previousEnd, end);
      }

      const translated = translatedSegments[index];
      const translationText = translated && typeof translated === 'object'
        ? String(translated.source_text ?? '')
        : '';
      const textMatches = Boolean(translated)
        && normalizeText(sourceText) === normalizeText(translationText);
      const timesMatch = Boolean(translated)
        && Number(translated.start) === start
        && Number(translated.end) === end;
      const aligned = textMatches && timesMatch;
      if (translated && !aligned) {
        unmatchedTranslations.push({
          segment_index: index,
          reason: !timesMatch ? 'TIMESTAMP_MISMATCH' : 'SOURCE_TEXT_MISMATCH',
          transcript_text: sourceText,
          translation_text: translationText,
          transcript_start: start,
          transcript_end: end,
          translation_start: translated.start,
          translation_end: translated.end
        });
      }

      const glosses = aligned && Array.isArray(translated.gloss) ? translated.gloss : [];
      const signIds = aligned && Array.isArray(translated.playable_signs)
        ? translated.playable_signs.map(String).filter(Boolean)
        : [];
      const unknownTerms = aligned ? normalizeUnknown(translated.unknown_terms) : [];
      const mismatchFallbackTerms = aligned ? [] : tokenizeSource(sourceText)
        .map((word, order) => ({ order, word, reason: 'SOURCE_TRANSLATION_MISMATCH' }));
      const unavailableConcepts = aligned
        ? normalizeUnavailable(translated.unavailable_concepts)
        : [];
      const cueFallbackOccurrences = [
        ...unknownTerms.map(item => ({ ...item, category: 'unknown_term' })),
        ...mismatchFallbackTerms.map(item => ({ ...item, category: 'source_mismatch' })),
        ...unavailableConcepts.map(item => ({ ...item, category: 'unavailable_sign' }))
      ];
      const signOccurrences = signIds.map((signId, occurrenceIndex) => ({
        occurrence_id: `${videoId}_${String(index + 1).padStart(6, '0')}:sign:${occurrenceIndex}`,
        occurrence_index: occurrenceIndex,
        sign_id: signId,
        candidate_sign_id: aligned && Array.isArray(translated.candidate_sign_ids)
          ? String(translated.candidate_sign_ids[occurrenceIndex] || '')
          : ''
      }));
      const cueId = `${videoId}_${String(index + 1).padStart(6, '0')}`;
      const fallbackWords = cueFallbackOccurrences.map(item => item.word);
      const translationStatus = aligned
        ? String(translated.translation_status || 'TRANSLATION_UNCERTAIN')
        : 'UNAVAILABLE_SOURCE_TRANSLATION_MISMATCH';

      playableOccurrences += signOccurrences.length;
      fallbackOccurrenceCount += cueFallbackOccurrences.length;
      unknownTermOccurrences += unknownTerms.length;
      sourceMismatchFallbackOccurrences += mismatchFallbackTerms.length;
      unavailableConceptOccurrences += unavailableConcepts.length;

      cues.push({
        cue_schema_version: SCHEMA_VERSION,
        cue_id: cueId,
        video_id: videoId,
        job_id: jobId,
        segment_index: index,
        start,
        end,
        source_text: sourceText,
        source_transcript_identity: transcriptIdentity,
        gloss_occurrences: glosses.map((gloss, occurrenceIndex) => ({
          occurrence_id: `${cueId}:gloss:${occurrenceIndex}`,
          occurrence_index: occurrenceIndex,
          gloss: String(gloss)
        })),
        sign_occurrences: signOccurrences,
        sign_ids: signOccurrences.map(item => item.sign_id),
        unavailable_concepts: unavailableConcepts,
        unknown_terms: unknownTerms,
        fallback_occurrences: cueFallbackOccurrences,
        fallback_words: fallbackWords,
        fallback_message: fallbackWords.length
          ? `Sign not available for: ${fallbackWords.join(', ')}. Original text: ${sourceText}`
          : '',
        translation_status: translationStatus,
        translation_aligned: aligned
      });
    }

    for (let index = transcriptSegments.length; index < translatedSegments.length; index += 1) {
      unmatchedTranslations.push({ segment_index: index, reason: 'NO_TRANSCRIPT_SEGMENT' });
    }

    const manifest = {
      schema_version: SCHEMA_VERSION,
      video_id: videoId,
      job_id: jobId,
      source_transcript_identity: transcriptIdentity,
      cue_count: cues.length,
      cues,
      unmatched_translations: unmatchedTranslations,
      validation_errors: validationErrors,
      playback_ready: validationErrors.length === 0,
      coverage: {
        transcript_segments: transcriptSegments.length,
        translation_segments: translatedSegments.length,
        aligned_segments: cues.filter(cue => cue.translation_aligned).length,
        mismatched_segments: unmatchedTranslations.length,
        playable_sign_occurrences: playableOccurrences,
        unavailable_concept_occurrences: unavailableConceptOccurrences,
        unknown_term_occurrences: unknownTermOccurrences,
        source_mismatch_fallback_occurrences: sourceMismatchFallbackOccurrences,
        fallback_occurrences: fallbackOccurrenceCount
      }
    };
    manifest.fingerprint = await sha256(JSON.stringify(manifest));
    return manifest;
  }

  return { SCHEMA_VERSION, buildYoutubeCueManifest };
});

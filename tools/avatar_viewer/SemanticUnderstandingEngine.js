/**
 * tools/avatar_viewer/SemanticUnderstandingEngine.js
 *
 * H43 Workstream 2: Intermediate Semantic Representation (ISR) Engine
 *
 * Segments multi-clause utterances, preserves discourse relations, distinguishes
 * true perfective aspect from obligation/possession, isolates negation per clause,
 * and emits contextual disambiguation hints used directly by EnglishToISLTranslator.
 */

const PAST_PARTICIPLES = new Set([
  'met', 'gone', 'done', 'been', 'seen', 'written', 'read', 'made', 'spoken',
  'known', 'told', 'given', 'taken', 'shown', 'come', 'become', 'found', 'felt',
  'kept', 'left', 'put', 'run', 'sat', 'said', 'lost', 'won', 'built', 'heard',
  'learned', 'studied', 'gathered', 'coached', 'filmed', 'scripted', 'started',
  'finished', 'tried', 'worked', 'helped', 'asked', 'answered', 'created', 'watched',
  'changed', 'moved', 'shared', 'opened', 'closed', 'remembered', 'understood',
  'stitched', 'defined', 'documented', 'explained', 'used', 'picked', 'gotten'
]);

const SUBJECT_START_TOKENS = new Set([
  'i', "i'm", "i've", "i'll", "i'd",
  'you', "you're", "you've", "you'll", "you'd",
  'we', "we're", "we've", "we'll", "we'd",
  'they', "they're", "they've", "they'll", "they'd",
  'he', "he's", "he'll", "he'd",
  'she', "she's", "she'll", "she'd",
  'it', "it's", "it'll",
  'that', "that's", 'there', "there's",
  'people', 'everybody', 'everyone', 'somebody', 'someone', 'nobody', 'my', 'your'
]);

const CLAUSE_CONJUNCTIONS = new Set([
  'and', 'but', 'so', 'because', 'or', 'if', 'when', 'while',
  'although', 'though', 'then', 'since', 'unless', 'after', 'before'
]);

export class SemanticUnderstandingEngine {
  constructor(options = {}) {
    this.options = options;

    this.contextualLexicon = new Map([
      ['vlog', ['VIDEO']],
      ['vlogging', ['VIDEO', 'PRACTICE']],
      ['filming', ['RECORD', 'CAMERA']],
      ['film', ['FILM']],
      ['films', ['FILM']],
      ['shot', ['PICTURE']],
      ['scenes', ['SCENE']],
      ['scene', ['SCENE']],
      ['movie', ['MOVIE']],
      ['movies', ['MOVIE']],
      ['documentaries', ['MOVIE']],
      ['documentary', ['MOVIE']],
      ['stories', ['STORY']],
      ['story', ['STORY']],
      ['feature', ['FEATURE']],
      ['features', ['FEATURE']],
      ['overthinking', ['THINK', 'MORE']],
      ['overcomplicating', ['CONFUSED', 'HARD']],
      ['trial and error', ['PRACTICE', 'TEST', 'FAIL', 'LEARN']],
      ['loosely defined', ['SIMPLE']],
      ['creative process', ['ART', 'STEP']]
    ]);
  }

  /**
   * Split an utterance into semantic clause units while preserving contraction apostrophes
   * and avoiding false splits inside comma-separated noun/adjective lists.
   */
  segmentClauses(text) {
    if (!text || typeof text !== 'string') return [];

    const normalized = text.trim()
      .replace(/([.!?;:,])/g, ' $1 ')
      .replace(/\s+/g, ' ')
      .trim();

    if (!normalized) return [];

    const rawTokens = normalized.split(' ').filter(Boolean);
    const clauses = [];
    let currentClauseTokens = [];
    let currentConjunction = null;

    const terminalPunct = new Set(['.', '!', '?', ';', ':']);

    for (let i = 0; i < rawTokens.length; i++) {
      const raw = rawTokens[i];
      const lower = raw.toLowerCase();

      if (terminalPunct.has(lower)) {
        if (currentClauseTokens.length > 0) {
          clauses.push({
            conjunction: currentConjunction,
            tokens: [...currentClauseTokens],
            punctuation: lower
          });
          currentClauseTokens = [];
          currentConjunction = null;
        }
        continue;
      }

      if (lower === ',') {
        const nextLower = (rawTokens[i + 1] || '').toLowerCase();
        // Split on comma only if the next token starts a new clause/subject/conjunction
        // AND the preceding fragment has at least a minimal clause core (>= 2 words)
        const startsNewClause = CLAUSE_CONJUNCTIONS.has(nextLower) || SUBJECT_START_TOKENS.has(nextLower);
        if (startsNewClause && currentClauseTokens.length >= 2) {
          clauses.push({
            conjunction: currentConjunction,
            tokens: [...currentClauseTokens],
            punctuation: null
          });
          currentClauseTokens = [];
          currentConjunction = null;
        }
        continue;
      }

      if (CLAUSE_CONJUNCTIONS.has(lower) && currentClauseTokens.length >= 2) {
        const nextLower = (rawTokens[i + 1] || '').toLowerCase();
        const prevLower = (currentClauseTokens[currentClauseTokens.length - 1] || '').toLowerCase();
        // Do not split on clause-final adverbs like "met before," or "shortly after."
        const isTrailingAdverb = (lower === 'before' || lower === 'after') && (!nextLower || [',', '.', '!', '?', ';', ':'].includes(nextLower));
        // Keep coordinated noun phrases ("pen and paper", "trial and error", "mindset and confidence") together
        const isCoordinatedPair = (lower === 'and' || lower === 'or')
          && !SUBJECT_START_TOKENS.has(nextLower)
          && !['but', 'so', 'if', 'when', 'because'].includes(nextLower)
          && !['not', 'no'].includes(prevLower)
          && currentClauseTokens.length < 4;

        if (!isTrailingAdverb && !isCoordinatedPair) {
          clauses.push({
            conjunction: currentConjunction,
            tokens: [...currentClauseTokens],
            punctuation: null
          });
          currentClauseTokens = [];
          currentConjunction = lower;
          continue;
        }
      }

      currentClauseTokens.push(raw);
    }

    if (currentClauseTokens.length > 0) {
      clauses.push({
        conjunction: currentConjunction,
        tokens: [...currentClauseTokens],
        punctuation: null
      });
    }

    return clauses;
  }

  _isPastParticiple(token) {
    if (!token) return false;
    const w = token.toLowerCase().replace(/[^a-z']/g, '');
    if (PAST_PARTICIPLES.has(w)) return true;
    return w.length > 4 && (w.endsWith('ed') || w.endsWith('en'));
  }

  /**
   * Parse a single clause unit into structured semantic roles, aspect, polarity, and contextual overrides.
   */
  parseClauseUnit(clause, clauseIndex, fullUtteranceLower = '') {
    const lowerTokens = clause.tokens.map(t => t.toLowerCase());
    const rawText = clause.tokens.join(' ');
    const conj = clause.conjunction || (CLAUSE_CONJUNCTIONS.has(lowerTokens[0]) ? lowerTokens[0] : null);

    // 1. Discourse Act Classification
    let discourseAct = 'STATEMENT';
    if (clause.punctuation === '?' || /^(how|what|where|when|why|who)\b/i.test(rawText)) {
      discourseAct = /^(how|what|where|when|why|who)\b/i.test(rawText) ? 'WH_QUESTION' : 'YES_NO_QUESTION';
    } else if (/^(do|does|did|can|will|are|is)\s+(you|we|they|i|it|this|that)\b/i.test(rawText) && clause.punctuation !== '.') {
      discourseAct = 'YES_NO_QUESTION';
    } else if (clauseIndex === 0 && /^(hey|hello|hi|welcome|alright)\b/i.test(rawText)) {
      discourseAct = 'GREETING_VOCATIVE';
    }

    // 2. Clause Type
    let clauseType = 'MAIN';
    if (conj === 'if' || conj === 'unless') clauseType = 'CONDITIONAL_PROTASIS';
    else if (conj === 'when' || conj === 'while' || conj === 'before' || conj === 'after') clauseType = 'TEMPORAL_ADVERBIAL';
    else if (conj === 'because' || conj === 'since') clauseType = 'REASON_CAUSE';
    else if (conj === 'but' || conj === 'although' || conj === 'though') clauseType = 'CONTRASTIVE';
    else if (conj === 'or') clauseType = 'DISJUNCTIVE';

    // 3. Subject / Agent Identification
    const subjectPronouns = ['i', 'you', 'we', 'they', 'he', 'she', 'it', 'people', 'somebody', 'someone', 'everybody', 'everyone', 'who'];
    let subject = null;
    let sIdx = -1;
    for (let i = 0; i < lowerTokens.length; i++) {
      const root = lowerTokens[i].split("'")[0];
      if (subjectPronouns.includes(root)) {
        subject = root.toUpperCase();
        sIdx = i;
        break;
      }
    }

    // 4. Modal Analysis (Obligation vs Ability vs Intent)
    let modal = null;
    if (/\bhave to\b/i.test(rawText) || /\bneed to\b/i.test(rawText) || lowerTokens.includes('need') || lowerTokens.includes('should')) {
      modal = 'NECESSITY_OBLIGATION';
    } else if (lowerTokens.includes('can') || lowerTokens.includes("can't") || lowerTokens.includes('cannot') || lowerTokens.includes('able')) {
      modal = 'ABILITY_CAN';
    } else if (lowerTokens.includes('might') || lowerTokens.includes('maybe') || lowerTokens.includes('may')) {
      modal = 'EPISTEMIC_POSSIBILITY';
    } else if (lowerTokens.some(t => t === 'will' || t.endsWith("'ll") || t === 'gonna') || /\bgoing to\b/i.test(rawText)) {
      modal = 'FUTURE_INTENT';
    }

    // 5. Clause-Scoped Polarity (count negative contractions cleanly without doubling)
    const negRe = /\b(not|never|no|cannot|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't|won't|wouldn't|can't|couldn't|shouldn't)\b/i;
    const privativeRe = /\bwithout\b/i;
    const hasNegation = negRe.test(rawText);
    const hasPrivative = privativeRe.test(rawText);
    const polarity = hasNegation ? 'NEGATIVE' : (hasPrivative ? 'PRIVATIVE' : 'AFFIRMATIVE');

    // 6. Strict Aspect Analysis: PERFECTIVE_COMPLETED ONLY on have/has/had/'ve + Past Participle
    // Never fire on "have to <verb>" (obligation), possessive "have a story", or "get/getting".
    let aspect = 'NEUTRAL';
    for (let i = 0; i < lowerTokens.length; i++) {
      const t = lowerTokens[i];
      const isHaveAux = t === 'have' || t === 'has' || t === 'had' || t.endsWith("'ve") || t === "haven't" || t === "hasn't" || t === "hadn't";
      if (!isHaveAux) continue;
      let nextIdx = i + 1;
      while (nextIdx < lowerTokens.length && ['not', 'never', 'already', 'just', 'ever', 'definitely', 'also', 'even'].includes(lowerTokens[nextIdx])) {
        nextIdx += 1;
      }
      const nextTok = lowerTokens[nextIdx];
      if (nextTok && nextTok !== 'to' && this._isPastParticiple(nextTok)) {
        aspect = 'PERFECTIVE_COMPLETED';
        break;
      }
    }
    if (aspect === 'NEUTRAL' && (lowerTokens.includes('start') || lowerTokens.includes('begin') || lowerTokens.includes('starting'))) {
      aspect = 'INCEPTIVE_START';
    }

    // 7. Temporal Frame
    const timeKeywords = new Set(['today', 'tomorrow', 'now', 'yesterday', 'summer', 'past', 'future', 'morning', 'evening', 'night', 'before', 'next']);
    const temporalItems = [];
    for (const t of lowerTokens) {
      if (timeKeywords.has(t)) temporalItems.push(t.toUpperCase());
    }

    // 8. Contextual Word Sense Disambiguation Hints (used directly during token->gloss resolution)
    const contextualOverrides = {};
    const inMediaContext = /\b(vlog|vlogs|vlogging|film|films|filming|camera|scene|scenes|movie|shoot|shooting)\b/i.test(fullUtteranceLower || rawText);
    for (let i = 0; i < lowerTokens.length; i++) {
      const tok = lowerTokens[i].replace(/[^a-z]/g, '');
      const prev = (lowerTokens[i - 1] || '').replace(/[^a-z]/g, '');
      const next = (lowerTokens[i + 1] || '').replace(/[^a-z]/g, '');

      if (tok === 'right') {
        if (next === 'here' || next === 'now' || next === 'away') {
          contextualOverrides.right = '__OMIT__';
        } else if (['feel', 'look', 'seem', 'sound'].includes(prev)) {
          contextualOverrides.right = 'GOOD';
        } else {
          contextualOverrides.right = 'TRUE';
        }
      } else if (tok === 'shot' || tok === 'shots') {
        const idiomTry = prev === 'a' && /\b(give|gave|giving|worth)\b/i.test(rawText);
        contextualOverrides[tok] = (inMediaContext || !idiomTry) ? 'PICTURE' : 'TRY';
      } else if (tok === 'just' && next === 'like') {
        contextualOverrides.just = 'SAME';
      }
    }

    return {
      clause_index: clauseIndex,
      raw_text: rawText,
      tokens: clause.tokens,
      conjunction: conj,
      discourse_act: discourseAct,
      clause_type: clauseType,
      subject,
      subject_index: sIdx,
      modal,
      polarity,
      aspect,
      temporal_items: temporalItems,
      contextual_overrides: contextualOverrides,
      confidence: 0.95
    };
  }

  /**
   * Generate complete Intermediate Semantic Representation (ISR) for an utterance.
   */
  parseUtterance(text, asrContext = null) {
    const rawClauses = this.segmentClauses(text);
    const fullLower = String(text ?? '').toLowerCase();
    const parsedClauses = rawClauses.map((c, idx) => this.parseClauseUnit(c, idx, fullLower));

    let overallAct = 'STATEMENT';
    if (parsedClauses.some(c => c.discourse_act === 'WH_QUESTION')) overallAct = 'WH_QUESTION';
    else if (parsedClauses.some(c => c.discourse_act === 'YES_NO_QUESTION')) overallAct = 'YES_NO_QUESTION';
    else if (parsedClauses.some(c => c.discourse_act === 'GREETING_VOCATIVE')) overallAct = 'GREETING_VOCATIVE';

    const negativeClauseIndices = parsedClauses.filter(c => c.polarity === 'NEGATIVE').map(c => c.clause_index);
    const asrConfidence = asrContext && Number.isFinite(asrContext.confidence) ? asrContext.confidence : null;
    const avgLogprob = asrContext && Number.isFinite(asrContext.avg_logprob) ? asrContext.avg_logprob : null;

    return {
      schema: 'ISL_ISR_2.0',
      source_text: text,
      clause_count: parsedClauses.length,
      overall_discourse_act: overallAct,
      conditional_present: parsedClauses.some(c => c.clause_type === 'CONDITIONAL_PROTASIS'),
      negative_clause_indices: negativeClauseIndices,
      multi_clause_negation_isolated: parsedClauses.length > 1 && negativeClauseIndices.length > 0,
      asr_confidence: asrConfidence,
      avg_logprob: avgLogprob,
      clauses: parsedClauses
    };
  }
}

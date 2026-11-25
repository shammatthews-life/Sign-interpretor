/**
 * tools/avatar_viewer/SemanticUnderstandingEngine.js
 *
 * H44 Workstream 5: Intermediate Semantic Representation (ISR 3.0) Engine
 *
 * Segments utterances while preserving coordinated noun objects ("a pen and a paper"),
 * distinguishes matrix WH-questions from free-relative/pseudo-cleft clauses (Aboh, Pfau & Zeshan 2005),
 * separates idiomatic contrast ("show not tell") from negative polarity, resolves polysemous
 * context senses ("rest of" -> REMAINING, "just a" -> ONLY, "feel right" -> GOOD),
 * and emits clause-level proposition & non-manual marker frames.
 */

const PAST_PARTICIPLES = new Set([
  'met', 'gone', 'done', 'been', 'seen', 'written', 'read', 'made', 'spoken',
  'known', 'told', 'given', 'taken', 'shown', 'come', 'become', 'found', 'felt',
  'kept', 'left', 'put', 'run', 'sat', 'said', 'lost', 'won', 'built', 'heard',
  'learned', 'studied', 'gathered', 'coached', 'filmed', 'scripted', 'started',
  'finished', 'tried', 'worked', 'helped', 'asked', 'answered', 'created', 'watched',
  'changed', 'moved', 'shared', 'opened', 'closed', 'remembered', 'understood',
  'stitched', 'defined', 'documented', 'explained', 'used', 'picked', 'gotten', 'delivered'
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

const FINITE_VERB_HINTS = new Set([
  'is', 'are', 'was', 'were', 'am', 'will', 'can', 'could', 'would', 'should',
  'have', 'has', 'had', 'do', 'does', 'did',
  'go', 'goes', 'went', 'know', 'knows', 'think', 'say', 'tell', 'explain',
  'filmed', 'scripted', 'started', 'start', 'begin', 'finish', 'bring', 'meet',
  'make', 'build', 'find', 'show', 'see', 'look', 'feel', 'need', 'want', 'live',
  'walk', 'lean', 'allow', 'overcome', 'delivered', 'coached', 'gathered'
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
      ['filming', ['RECORD']],
      ['film', ['FILM']],
      ['films', ['FILM']],
      ['shot', ['PICTURE']],
      ['scenes', ['SCENE']],
      ['scene', ['SCENE']],
      ['movie', ['MOVIE']],
      ['movies', ['MOVIE']],
      ['stories', ['STORY']],
      ['story', ['STORY']],
      ['feature', ['FEATURE']],
      ['features', ['FEATURE']],
      ['overthinking', ['THINK', 'MORE']],
      ['overcomplicating', ['CONFUSED', 'HARD']],
      ['trial and error', ['PRACTICE', 'FAIL', 'LEARN']],
      ['loosely defined', ['SIMPLE']],
      ['creative process', ['ART', 'STEP']],
      ['story is king', ['STORY', 'MOST', 'IMPORTANT']],
      ['show not tell', ['SHOW', 'MORE', 'SAY', 'LESS']]
    ]);
  }

  _rightSideHasClausePredicate(rawTokens, startIdx) {
    for (let j = startIdx; j < Math.min(rawTokens.length, startIdx + 7); j++) {
      const w = rawTokens[j].toLowerCase().replace(/[^a-z']/g, '');
      if (!w) continue;
      if ([',', '.', '!', '?', ';', ':'].includes(w)) break;
      if (CLAUSE_CONJUNCTIONS.has(w) && j > startIdx) break;
      if (FINITE_VERB_HINTS.has(w)) return true;
    }
    return false;
  }

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
          clauses.push({ conjunction: currentConjunction, tokens: [...currentClauseTokens], punctuation: lower });
          currentClauseTokens = [];
          currentConjunction = null;
        }
        continue;
      }

      if (lower === ',') {
        const nextLower = (rawTokens[i + 1] || '').toLowerCase();
        const startsNewClause = CLAUSE_CONJUNCTIONS.has(nextLower) || SUBJECT_START_TOKENS.has(nextLower);
        if (startsNewClause && currentClauseTokens.length >= 2) {
          clauses.push({ conjunction: currentConjunction, tokens: [...currentClauseTokens], punctuation: null });
          currentClauseTokens = [];
          currentConjunction = null;
        }
        continue;
      }

      if (CLAUSE_CONJUNCTIONS.has(lower) && currentClauseTokens.length >= 2) {
        const nextLower = (rawTokens[i + 1] || '').toLowerCase();
        const prevLower = (currentClauseTokens[currentClauseTokens.length - 1] || '').toLowerCase();

        // Preserve "or so" approximator ("in an hour or so") without splitting on "so"
        if (lower === 'or' && nextLower === 'so') {
          currentClauseTokens.push(raw, rawTokens[i + 1]);
          i += 1;
          continue;
        }

        // Preserve trailing adverbs ("haven't met before,")
        const isTrailingAdverb = (lower === 'before' || lower === 'after')
          && (!nextLower || [',', '.', '!', '?', ';', ':'].includes(nextLower));

        // Do NOT split on 'and'/'or' inside coordinated noun objects ("a pen and a paper", "mindset and confidence")
        // unless the right side begins a subject pronoun OR clearly has a finite verb before next break.
        const isCoordinatedPhrase = (lower === 'and' || lower === 'or')
          && !SUBJECT_START_TOKENS.has(nextLower)
          && !CLAUSE_CONJUNCTIONS.has(nextLower)
          && !this._rightSideHasClausePredicate(rawTokens, i + 1);

        // Wait: preserve short VP pairs like "try and think", "go out and filmed", "sat down and scripted" if needed,
        // while keeping "pen and a paper", "public speaker and public speaking coach" unified!
        if (!isTrailingAdverb && !isCoordinatedPhrase) {
          clauses.push({ conjunction: currentConjunction, tokens: [...currentClauseTokens], punctuation: null });
          currentClauseTokens = [];
          currentConjunction = lower;
          continue;
        }
      }

      // Split embedded quoted direct WH-questions after "of" (e.g., "shooting of what is my story")
      if (lower === 'of' && currentClauseTokens.length >= 2) {
        const nextLower = (rawTokens[i + 1] || '').toLowerCase();
        const next2Lower = (rawTokens[i + 2] || '').toLowerCase();
        if (['what', 'how', 'where', 'who'].includes(nextLower) && ['is', 'are'].includes(next2Lower)) {
          clauses.push({ conjunction: currentConjunction, tokens: [...currentClauseTokens], punctuation: null });
          currentClauseTokens = [];
          currentConjunction = null;
          continue;
        }
      }

      currentClauseTokens.push(raw);
    }

    if (currentClauseTokens.length > 0) {
      clauses.push({ conjunction: currentConjunction, tokens: [...currentClauseTokens], punctuation: null });
    }

    return clauses;
  }

  _isPastParticiple(token) {
    if (!token) return false;
    const w = token.toLowerCase().replace(/[^a-z']/g, '');
    if (PAST_PARTICIPLES.has(w)) return true;
    return w.length > 4 && (w.endsWith('ed') || w.endsWith('en'));
  }

  parseClauseUnit(clause, clauseIndex, fullUtteranceLower = '') {
    const lowerTokens = clause.tokens.map(t => t.toLowerCase());
    const rawText = clause.tokens.join(' ');
    const conj = clause.conjunction || (CLAUSE_CONJUNCTIONS.has(lowerTokens[0]) ? lowerTokens[0] : null);

    // 1. Distinguish True Matrix WH-Questions from Nominal Free Relatives / Pseudo-Clefts (RES-H44-01)
    const whLeadMatch = rawText.match(/^(how|what|where|when|why|who)\b/i);
    const hasExplicitQuestionMark = clause.punctuation === '?';
    const isDirectWhAux = Boolean(whLeadMatch) && /^(how|what|where|when|why|who)\s+(is|are|do|does|did|can|will|would|could|should)\b/i.test(rawText);
    const isPseudoCleftOrRelative = Boolean(whLeadMatch) && (
      /^(what|how|where)\s+(you|i|we|they|he|she|that|everyone|everybody)\b/i.test(rawText)
      || /\b(is|are|was|were)\s+(a|an|the|scenes|at)\b/i.test(rawText.slice(rawText.indexOf(' ') + 1))
    );
    const isMatrixWhQuestion = Boolean(
      (hasExplicitQuestionMark && /\b(how|what|where|when|why|who)\b/i.test(rawText))
      || (isDirectWhAux && !isPseudoCleftOrRelative && !hasExplicitQuestionMark ? true : false)
    );
    const isYesNoQuestion = Boolean(
      (hasExplicitQuestionMark && !isMatrixWhQuestion)
      || (/^(do|does|did|can|will|are|is)\s+(you|we|they|i|it|this|that)\b/i.test(rawText) && clause.punctuation !== '.')
    );

    let discourseAct = 'STATEMENT';
    if (isMatrixWhQuestion) discourseAct = 'WH_QUESTION';
    else if (isYesNoQuestion) discourseAct = 'YES_NO_QUESTION';
    else if (isPseudoCleftOrRelative) discourseAct = 'NOMINAL_CLEFT_OR_RELATIVE';
    else if (clauseIndex === 0 && /^(hey|hello|hi|welcome|alright)\b/i.test(rawText)) discourseAct = 'GREETING_VOCATIVE';

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

    // 4. Modal Analysis
    let modal = null;
    if (/\b(have to|need to|make sure)\b/i.test(rawText) || lowerTokens.includes('need') || lowerTokens.includes('should')) {
      modal = 'NECESSITY_OBLIGATION';
    } else if (lowerTokens.includes('can') || lowerTokens.includes("can't") || lowerTokens.includes('cannot') || lowerTokens.includes('able')) {
      modal = 'ABILITY_CAN';
    } else if (lowerTokens.includes('might') || lowerTokens.includes('maybe') || lowerTokens.includes('may') || lowerTokens.includes('probably')) {
      modal = 'EPISTEMIC_POSSIBILITY';
    } else if (lowerTokens.some(t => t === 'will' || t.endsWith("'ll") || t === 'gonna') || /\bgoing to\b/i.test(rawText)) {
      modal = 'FUTURE_INTENT';
    }

    // 5. Clause-Scoped Polarity: exclude contrastive idioms like "show not tell" and "not only"
    const cleanForNeg = rawText.replace(/\bshow\s*,?\s*not\s+tell\b/gi, '').replace(/\bnot\s+only\b/gi, '');
    const idiomaticNegConsumed = /\bshow\s*,?\s*not\s+tell\b/i.test(rawText);
    const negRe = /\b(not|never|no|cannot|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't|won't|wouldn't|can't|couldn't|shouldn't)\b/i;
    const privativeRe = /\bwithout\b/i;
    const hasNegation = negRe.test(cleanForNeg);
    const hasPrivative = privativeRe.test(rawText);
    const polarity = hasNegation ? 'NEGATIVE' : (hasPrivative ? 'PRIVATIVE' : 'AFFIRMATIVE');

    // 6. Strict Aspect Analysis: PERFECTIVE_COMPLETED on have/has/had/'ve + Past Participle
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

    // 8. Contextual Word-Sense Disambiguation Hints (H44)
    const contextualOverrides = {};
    const inMediaContext = /\b(vlog|vlogs|vlogging|film|films|filming|camera|scene|scenes|movie|shoot|shooting)\b/i.test(fullUtteranceLower || rawText);
    for (let i = 0; i < lowerTokens.length; i++) {
      const tok = lowerTokens[i].replace(/[^a-z]/g, '');
      const prev = (lowerTokens[i - 1] || '').replace(/[^a-z]/g, '');
      const next = (lowerTokens[i + 1] || '').replace(/[^a-z]/g, '');

      if (tok === 'right') {
        if (next === 'here' || next === 'now' || next === 'away') contextualOverrides.right = '__OMIT__';
        else if (['feel', 'look', 'seem', 'sound'].includes(prev)) contextualOverrides.right = 'GOOD';
        else contextualOverrides.right = 'TRUE';
      } else if (tok === 'shot' || tok === 'shots') {
        const idiomTry = prev === 'a' && /\b(give|gave|giving|worth)\b/i.test(rawText);
        contextualOverrides[tok] = (inMediaContext || !idiomTry) ? 'PICTURE' : 'TRY';
      } else if (tok === 'rest') {
        contextualOverrides.rest = next === 'of' ? 'REMAINING' : 'REST';
      } else if (tok === 'just') {
        if (['a', 'an', 'one', 'this', 'that'].includes(next)) contextualOverrides.just = 'ONLY';
        else if (next === 'like') contextualOverrides.just = '__OMIT__';
        else contextualOverrides.just = '__OMIT__';
      } else if (tok === 'exactly') {
        contextualOverrides.exactly = (hasNegation || /\bknow\b/i.test(rawText)) ? 'CLEAR' : 'TRUE';
      } else if (tok === 'left') {
        const spatialCue = ['the', 'to', 'on', 'my', 'your', 'turn'].includes(prev);
        contextualOverrides.left = spatialCue ? 'LEFT' : 'LEAVE';
      } else if (tok === 'too') {
        contextualOverrides.too = 'ALSO';
      }
    }

    // Non-manual markers required for grammatical fidelity
    const clauseNMMs = [];
    if (isMatrixWhQuestion) clauseNMMs.push('BROW_FURROW_WH');
    else if (isYesNoQuestion) clauseNMMs.push('BROW_RAISE_YN');
    if (clauseType === 'CONDITIONAL_PROTASIS') clauseNMMs.push('BROW_RAISE_CONDITIONAL_TOPIC');
    if (hasNegation) clauseNMMs.push('HEADSHAKE_NEGATION');

    return {
      clause_index: clauseIndex,
      raw_text: rawText,
      tokens: clause.tokens,
      conjunction: conj,
      discourse_act: discourseAct,
      is_matrix_wh_question: isMatrixWhQuestion,
      idiomatic_negation_consumed: idiomaticNegConsumed,
      clause_type: clauseType,
      subject,
      subject_index: sIdx,
      modal,
      polarity,
      aspect,
      temporal_items: temporalItems,
      contextual_overrides: contextualOverrides,
      non_manual_markers: clauseNMMs,
      translation_strategy: clauseType === 'CONDITIONAL_PROTASIS'
        ? 'CONDITIONAL_TOPIC_COMMENT'
        : (isMatrixWhQuestion ? 'ISL_CLAUSE_FINAL_WH' : 'CLAUSE_SCOPED_SOV'),
      confidence: 0.95
    };
  }

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

    const propositions = parsedClauses.map(c => ({
      clause_index: c.clause_index,
      agent: c.subject,
      clause_type: c.clause_type,
      polarity: c.polarity,
      aspect: c.aspect,
      modal: c.modal,
      temporal: c.temporal_items,
      is_matrix_wh_question: c.is_matrix_wh_question,
      non_manual_markers: c.non_manual_markers
    }));

    return {
      schema: 'ISL_ISR_3.0',
      source_text: text,
      clause_count: parsedClauses.length,
      overall_discourse_act: overallAct,
      conditional_present: parsedClauses.some(c => c.clause_type === 'CONDITIONAL_PROTASIS'),
      negative_clause_indices: negativeClauseIndices,
      multi_clause_negation_isolated: parsedClauses.length > 1 && negativeClauseIndices.length > 0,
      asr_confidence: asrConfidence,
      avg_logprob: avgLogprob,
      propositions,
      clauses: parsedClauses
    };
  }
}

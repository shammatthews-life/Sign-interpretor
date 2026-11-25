import { TranslationBackend } from './TranslationBackend.js';

/**
 * Phase G2 / H13: English -> ISL-oriented representation layer.
 * Authoring Batch 2 added: YOUR, MY, HAVE, WANT, LOOK, SEE.
 * Includes explicit GRAMMAR_OMISSION classification for natural ISL omission of English function words.
 */
export class EnglishToISLTranslator extends TranslationBackend {
  constructor({ motionCatalog = null, enableG3Improvements = true } = {}) {
    super();
    this.enableG3Improvements = enableG3Improvements;
    // This catalog is motion availability metadata, deliberately separate from glosses.
    this.motionCatalog = motionCatalog || {
      hello: { playable: true }, good: { playable: true }, morning: { playable: true },
      water: { playable: true },
      you: { playable: true }, i: { playable: true }, me: { playable: true },
      your: { playable: true }, my: { playable: true },
      have: { playable: true }, want: { playable: true },
      look: { playable: true }, see: { playable: true },
      what: { playable: true }, not: { playable: true },
      thank_you: { playable: false, reason: 'MOTION_NOT_AUTHORED' },
      drink: { playable: false, reason: 'MOTION_NOT_AUTHORED' },
      help: { playable: false, reason: 'MOTION_NOT_AUTHORED' }, need: { playable: false, reason: 'MOTION_NOT_AUTHORED' },
      how: { playable: true }, tomorrow: { playable: false, reason: 'MOTION_NOT_AUTHORED' },
      go: { playable: true }, do: { playable: true }, people: { playable: true },
      one: { playable: true }, when: { playable: true }, now: { playable: true },
      more: { playable: true },
      like: { playable: true }, can: { playable: true }, know: { playable: true },
      think: { playable: true }, say: { playable: true }, time: { playable: true },
      give: { playable: true }, we: { playable: true }, they: { playable: true },
      will: { playable: true }, two: { playable: true }, yes: { playable: true },
      no: { playable: true }, come: { playable: true }, learn: { playable: true },
    };
    this.phrases = new Map([
      ['good morning', ['GOOD', 'MORNING']], ['thank you', ['THANK_YOU']], ['hello', ['HELLO']],
      ['going to', ['GOING_TO']], ['want to', ['WANT']], ['look at', ['LOOK']],
      ['as well as', ['AND', 'ALSO']], ['in order to', ['FOR']], ['what do you', ['YOU', 'WHAT']],
      ['how to', ['HOW']], ['have to', ['MUST']], ['public speaking', ['SAY', 'PEOPLE']],
    ]);
    this.lexicon = new Map([
      ['i', 'I'], ['you', 'YOU'], ['me', 'ME'],
      ['your', 'YOUR'], ['my', 'MY'],
      ['have', 'HAVE'], ['want', 'WANT'],
      ['look', 'LOOK'], ['see', 'SEE'],
      ['drink', 'DRINK'], ['water', 'WATER'],
      ['help', 'HELP'], ['need', 'NEED'], ['hello', 'HELLO'], ['good', 'GOOD'], ['morning', 'MORNING'],
      ['what', 'WHAT'], ['not', 'NOT'], ['how', 'HOW'],
      ['go', 'GO'], ['going', 'GO'], ['goes', 'GO'], ['went', 'GO'], ['gone', 'GO'],
      ['do', 'DO'], ['doing', 'DO'], ['does', 'DO'], ['did', 'DO'], ['done', 'DO'],
      ['people', 'PEOPLE'], ['person', 'PEOPLE'],
      ['one', 'ONE'], ['ones', 'ONE'],
      ['when', 'WHEN'],
      ['now', 'NOW'],
      ['more', 'MORE'],
      ['like', 'LIKE'], ['likes', 'LIKE'], ['liked', 'LIKE'], ['liking', 'LIKE'],
      ['can', 'CAN'],
      ['know', 'KNOW'], ['knows', 'KNOW'], ['knew', 'KNOW'], ['known', 'KNOW'], ['knowing', 'KNOW'],
      ['think', 'THINK'], ['thinks', 'THINK'], ['thought', 'THINK'], ['thinking', 'THINK'],
      ['say', 'SAY'], ['says', 'SAY'], ['said', 'SAY'], ['saying', 'SAY'],
      ['speak', 'SAY'], ['speaks', 'SAY'], ['spoke', 'SAY'], ['spoken', 'SAY'], ['speaking', 'SAY'],
      ['talk', 'SAY'], ['talks', 'SAY'], ['talked', 'SAY'], ['talking', 'SAY'], ['speaker', 'SAY'],
      ['time', 'TIME'], ['times', 'TIME'], ['second', 'TIME'], ['seconds', 'TIME'], ['minute', 'TIME'], ['minutes', 'TIME'],
      ['give', 'GIVE'], ['gives', 'GIVE'], ['gave', 'GIVE'], ['given', 'GIVE'], ['giving', 'GIVE'],
      ['we', 'WE'], ['us', 'WE'], ['our', 'WE'], ['ours', 'WE'],
      ['they', 'THEY'], ['them', 'THEY'], ['their', 'THEY'], ['theirs', 'THEY'],
      ['will', 'WILL'], ['shall', 'WILL'],
      ['two', 'TWO'],
      ['yes', 'YES'], ['yeah', 'YES'], ['yep', 'YES'],
      ['no', 'NO'], ['nope', 'NO'],
      ['come', 'COME'], ['comes', 'COME'], ['came', 'COME'], ['coming', 'COME'],
      ['learn', 'LEARN'], ['learns', 'LEARN'], ['learned', 'LEARN'], ['learning', 'LEARN'],
      ['has', 'HAVE'], ['had', 'HAVE'], ['having', 'HAVE'],
      ['wants', 'WANT'], ['wanted', 'WANT'], ['wanting', 'WANT'],
      ['looks', 'LOOK'], ['looked', 'LOOK'], ['looking', 'LOOK'],
      ['sees', 'SEE'], ['saw', 'SEE'], ['seen', 'SEE'], ['seeing', 'SEE'],
    ]);
  }

  normalize(text) {
    let s = String(text ?? '').normalize('NFKC').toLowerCase()
      .replace(/[^\p{L}\p{N}?' ]+/gu, ' ').replace(/\s+/g, ' ').trim();
    // Expand frequent spoken contractions according to ISL grammar (copula omitted, modals unpacked)
    s = s.replace(/\bi'm\b/g, 'i')
         .replace(/\byou're\b/g, 'you')
         .replace(/\bwe're\b/g, 'we')
         .replace(/\bthey're\b/g, 'they')
         .replace(/\bhe's\b/g, 'he')
         .replace(/\bshe's\b/g, 'she')
         .replace(/\bthere's\b/g, 'there')
         .replace(/\bthat's\b/g, 'that')
         .replace(/\bwhat's\b/g, 'what')
         .replace(/\bi've\b/g, 'i have')
         .replace(/\byou've\b/g, 'you have')
         .replace(/\bi'll\b/g, 'i will')
         .replace(/\bdon't\b/g, 'not')
         .replace(/\bcan't\b/g, 'can not')
         .replace(/\bgonna\b/g, 'go')
         .replace(/\bwanna\b/g, 'want');
    return s.replace(/\s+/g, ' ').trim();
  }

  // Compatibility surface for the established G1 orchestrator.
  process(text) {
    const representation = this.translate(text);
    return { ...representation, input: representation.source_text, unknownWords: representation.unknown_terms, signIds: representation.motion_candidate_sign_ids };
  }

  textToSignSequence(text) { return this.translate(text).motion_candidate_sign_ids; }
  translate_partial(text) { return this.translate(text); }
  reset() { /* Rule backend is stateless; required by TranslationBackend. */ }

  translate(text) {
    const started = performance.now();
    const source_text = String(text ?? '');
    const normalized_text = this.normalize(source_text);
    const timing = { normalization_ms: 0, analysis_ms: 0, gloss_generation_ms: 0, sign_id_resolution_ms: 0 };
    const normalizedAt = performance.now(); timing.normalization_ms = normalizedAt - started;
    const isQuestion = /\?$/.test(String(text ?? '').trim()) || /^(will|can|do|does|did|are|is|how|what|where|when|why)\b/.test(normalized_text);
    let tokens = normalized_text.replace(/\?/g, '').split(' ').filter(Boolean);
    const trace = [{ stage: 'normalize', detail: normalized_text || '(empty)' }];
    const linguistic_notes = [];
    const removed = [];
    const gloss = [];
    const unknown_terms = [];
    const phraseMatches = [];
    const remainingTokens = [];
    for (let index = 0; index < tokens.length;) {
      const match = [...this.phrases.entries()].find(([phrase]) => {
        const words = phrase.split(' ');
        return words.every((word, offset) => tokens[index + offset] === word);
      });
      if (match) {
        const [phrase, phraseGloss] = match;
        gloss.push(...phraseGloss); phraseMatches.push(phrase); index += phrase.split(' ').length;
      } else { remainingTokens.push(tokens[index]); index += 1; }
    }
    if (phraseMatches.length) {
      trace.push({ stage: 'phrase_detection', detail: `Matched lexical phrase(s): ${phraseMatches.join(', ')}` });
      linguistic_notes.push('Phrase-level concepts were resolved before individual words.');
    }
    const auxiliaries = new Set(['will', 'can', 'do', 'does', 'did', 'are', 'is', 'am', 'was', 'were', 'be', 'been', 'the', 'a', 'an', 'to', 'of', 'in']);
    if (remainingTokens.length) {
      for (const token of remainingTokens) {
        if (auxiliaries.has(token)) {
          const hasOtherVerb = remainingTokens.some(t => t !== 'do' && ['go', 'want', 'see', 'look', 'have', 'need', 'help', 'drink'].includes(t));
          if (token === 'do' && !hasOtherVerb) {
            // Retain lexical DO when no auxiliary function is required
          } else {
            removed.push(token);
            continue;
          }
        }
        const g3Lexicon = this.enableG3Improvements ? { not: 'NOT', how: 'HOW', tomorrow: 'TOMORROW' } : {};
        const entry = this.lexicon.get(token) || g3Lexicon[token];
        if (entry) gloss.push(entry); else unknown_terms.push(token.toUpperCase());
      }
      if (removed.length) trace.push({ stage: 'function_words', detail: `Omitted English function/auxiliary tokens: ${removed.join(', ')}`, basis: 'PROJECT_HEURISTIC', status: 'GRAMMAR_OMISSION' });
      // Small controlled SVO pattern only.  This is intentionally not a general ISL parser.
      const pronounPositions = gloss.map((g, index) => ({ g, index })).filter(x => ['I', 'YOU', 'ME', 'YOUR', 'MY'].includes(x.g));
      const subject = gloss.find(g => ['I', 'YOU', 'YOUR', 'MY', 'PEOPLE', 'ONE'].includes(g));
      const object = gloss.find(g => ['WATER', 'ME', 'MORE'].includes(g)) || (this.enableG3Improvements && pronounPositions.length >= 2 ? pronounPositions[1].g : null);
      const verb = gloss.find(g => ['DRINK', 'HELP', 'NEED', 'HAVE', 'WANT', 'LOOK', 'SEE', 'GO', 'DO'].includes(g));
      if (subject && object && verb && gloss.length === 3) {
        gloss.splice(0, gloss.length, subject, object, verb);
        trace.push({ stage: 'restructure', detail: `Controlled semantic-role order: ${subject} ${object} ${verb}`, basis: 'PROJECT_HEURISTIC', rule_id: 'G3-RULE-PRONOUN-01' });
        linguistic_notes.push('Controlled SOV-style ordering is a project heuristic; it is not asserted as a universal ISL rule.');
      } else if (!phraseMatches.length) {
        trace.push({ stage: 'restructure', detail: 'No general reordering applied; input is outside the controlled declarative pattern.', basis: 'TRANSLATION_UNCERTAIN' });
      }
    }
    // The phrase-first lookup above must still preserve source phrase order when
    // phrases and standalone lexical items occur together (for example HELLO GOOD MORNING).
    if (phraseMatches.length) {
      const orderedGloss = [];
      for (let index = 0; index < tokens.length;) {
        const match = [...this.phrases.entries()].find(([phrase]) => phrase.split(' ').every((word, offset) => tokens[index + offset] === word));
        if (match) { orderedGloss.push(...match[1]); index += match[0].split(' ').length; }
        else {
          const token = tokens[index++];
          if (!auxiliaries.has(token) && this.lexicon.has(token)) orderedGloss.push(this.lexicon.get(token));
        }
      }
      gloss.splice(0, gloss.length, ...orderedGloss);
    }
    if (isQuestion) {
      const isWhQuestion = /^(how|what|where|when|why)\b/.test(normalized_text);
      trace.push({ stage: 'question', detail: `${isWhQuestion ? 'WH' : 'Yes/no'} question retained as a non-manual requirement; no invented manual question sign.`, basis: 'SOURCE_SUPPORTED', rule_id: 'G3-RULE-QUESTION-01' });
      linguistic_notes.push('Requires ISL question non-manual marking; current avatar pipeline does not render it.');
    }
    const hasNegation = gloss.includes('NOT');
    if (hasNegation) {
      trace.push({ stage: 'negation', detail: 'Negation concept retained; exact ISL construction remains unmodeled.', basis: 'SOURCE_SUPPORTED', rule_id: 'G3-RULE-NEGATION-01' });
      linguistic_notes.push('Negation is retained lexically and marked for non-manual review; no claim is made about ISL negation placement.');
    }
    const analysisAt = performance.now(); timing.analysis_ms = analysisAt - normalizedAt;
    const gloss_sequence = gloss;
    trace.push({ stage: 'gloss_generation', detail: gloss_sequence.join(' ') || '(no resolved glosses)' });
    const glossAt = performance.now(); timing.gloss_generation_ms = glossAt - analysisAt;
    const motion_candidate_sign_ids = gloss_sequence.map(g => g.toLowerCase()).filter(id => this.motionCatalog[id]);
    const sign_ids = [];
    const unavailable_signs = [];
    for (const id of motion_candidate_sign_ids) {
      const availability = this.motionCatalog[id];
      if (availability.playable) sign_ids.push(id);
      else unavailable_signs.push({ sign_id: id, reason: availability.reason });
    }
    trace.push({ stage: 'sign_id_resolution', detail: `Playable: ${sign_ids.join(', ') || 'none'}; unavailable: ${unavailable_signs.map(s => s.sign_id).join(', ') || 'none'}` });
    timing.sign_id_resolution_ms = performance.now() - glossAt;
    const hasHeuristic = trace.some(x => x.basis === 'PROJECT_HEURISTIC');
    const status = unknown_terms.length || (!phraseMatches.length && !hasHeuristic) ? 'TRANSLATION_UNCERTAIN' : (hasHeuristic ? 'TRANSLATION_HEURISTIC' : 'TRANSLATION_SUPPORTED');
    const questionMarker = /^(how|what|where|when|why)\b/.test(normalized_text) ? 'WH_QUESTION' : 'YES_NO_QUESTION';
    return {
      source_text,
      normalized_text,
      gloss_sequence,
      sign_ids,
      motion_candidate_sign_ids,
      unknown_terms,
      unavailable_signs,
      grammar_omissions: removed.map(token => ({ token, status: 'GRAMMAR_OMISSION' })),
      non_manual_markers: [...(isQuestion ? [questionMarker] : []), ...(hasNegation ? ['NEGATION'] : [])],
      linguistic_notes,
      transformation_trace: trace,
      status,
      timings_ms: Object.fromEntries(Object.entries(timing).map(([k, v]) => [k, Number(v.toFixed(3))]))
    };
  }
}

/** Current concrete backend name; EnglishToISLTranslator is retained for G2 compatibility. */
export class RuleBasedISLTranslator extends EnglishToISLTranslator {}

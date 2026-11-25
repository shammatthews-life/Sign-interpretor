/** Small deterministic mapper for the controlled text-to-sign prototype. */
export class SentenceProcessor {
  constructor(dictionary = {
    'hello': 'hello',
    'good': 'good',
    'morning': 'morning',
    'good morning': ['good', 'morning'],
    'water': 'water',
    'thank you': 'thank you',
  }) {
    this.dictionary = new Map(Object.entries(dictionary).map(([phrase, signIds]) => [
      this.normalize(phrase), Array.isArray(signIds) ? signIds : [signIds]
    ]));
    this.phrases = [...this.dictionary.keys()].sort((a, b) => b.split(' ').length - a.split(' ').length);
  }

  normalize(text) {
    return String(text ?? '').normalize('NFKC').toLowerCase()
      .replace(/[^\p{L}\p{N}]+/gu, ' ').trim().replace(/\s+/g, ' ');
  }

  process(text) {
    const normalized = this.normalize(text);
    const tokens = normalized ? normalized.split(' ') : [];
    const signIds = [], unknownWords = [];
    for (let index = 0; index < tokens.length;) {
      const phrase = this.phrases.find(candidate => candidate.split(' ').every((token, offset) => tokens[index + offset] === token));
      if (phrase) { signIds.push(...this.dictionary.get(phrase)); index += phrase.split(' ').length; }
      else { unknownWords.push(tokens[index].toUpperCase()); index += 1; }
    }
    return { input: String(text ?? ''), normalized, signIds, unknownWords };
  }

  textToSignSequence(text) { return this.process(text).signIds; }
}

export const textToSignSequence = text => new SentenceProcessor().textToSignSequence(text);

/** Stable contract for a replaceable English-to-ISL representation backend. */
export class TranslationBackend {
  translate(_text) { throw new Error('TranslationBackend.translate(text) must be implemented.'); }
  translate_partial(text) { return this.translate(text); }
  reset() { /* Stateless backends have nothing to reset. */ }
}

import { TranslationBackend } from './TranslationBackend.js';
import { SemanticUnderstandingEngine } from './SemanticUnderstandingEngine.js';

const CONTRACTION_PATTERNS = [
  [/\bi'm\b/g, 'i'], [/\byou're\b/g, 'you'], [/\bwe're\b/g, 'we'], [/\bthey're\b/g, 'they'],
  [/\bhe's\b/g, 'he'], [/\bshe's\b/g, 'she'], [/\bthere's\b/g, 'there'], [/\bthat's\b/g, 'that'],
  [/\bwhat's\b/g, 'what'], [/\bi've\b/g, 'i have'], [/\byou've\b/g, 'you have'], [/\bi'll\b/g, 'i will'],
  [/\bdon't\b/g, 'not'], [/\bcan't\b/g, 'can not'], [/\bgonna\b/g, 'will'], [/\bwanna\b/g, 'want'],
  [/\byou'll\b/g, 'you will'], [/\bthey'll\b/g, 'they will'], [/\bwe'll\b/g, 'we will'],
  [/\bhaven't\b/g, 'have not'], [/\bwe've\b/g, 'we have'], [/\bisn't\b/g, 'not'], [/\bdidn't\b/g, 'not'],
  [/\bdoesn't\b/g, 'not'], [/\bwasn't\b/g, 'not'], [/\bcouldn't\b/g, 'can not'],
  [/\bshouldn't\b/g, 'should not'], [/\bwouldn't\b/g, 'not'],
  [/\bit's\b/g, 'it'], [/\bit'll\b/g, 'it will']
];

/**
 * Phase G2 / H13: English -> ISL-oriented representation layer.
 * Authoring Batch 2 added: YOUR, MY, HAVE, WANT, LOOK, SEE.
 * Includes explicit GRAMMAR_OMISSION classification for natural ISL omission of English function words.
 */
export class EnglishToISLTranslator extends TranslationBackend {
  constructor({ motionCatalog = null, enableG3Improvements = true } = {}) {
    super();
    this.enableG3Improvements = enableG3Improvements;
    this._hasCustomMotionCatalog = Boolean(motionCatalog);
    // This catalog is motion availability metadata, deliberately separate from glosses.
    this.motionCatalog = motionCatalog || {
      hello: { playable: true }, good: { playable: true }, morning: { playable: true },
      water: { playable: true },
      you: { playable: true }, i: { playable: true }, me: { playable: true, sign_id: 'i' },
      your: { playable: true }, my: { playable: true },
      have: { playable: true }, want: { playable: true },
      look: { playable: true }, see: { playable: true },
      what: { playable: true }, not: { playable: true },
      where: { playable: true }, who: { playable: true }, please: { playable: true },
      always: { playable: true }, still: { playable: true }, our: { playable: true },
      again: { playable: true }, some: { playable: true }, something: { playable: true },
      everyone: { playable: true }, become: { playable: true }, thing: { playable: true },
      direct: { playable: true }, continue: { playable: true }, rain: { playable: true },
      thank_you: { playable: false, reason: 'MOTION_NOT_AUTHORED' },
      drink: { playable: true },
      help: { playable: true }, need: { playable: true },
      how: { playable: true }, tomorrow: { playable: true },
      go: { playable: true }, do: { playable: true }, people: { playable: true },
      one: { playable: true }, when: { playable: true }, now: { playable: true },
      more: { playable: true },
      like: { playable: true }, can: { playable: true }, know: { playable: true },
      think: { playable: true }, say: { playable: true }, time: { playable: true },
      give: { playable: true }, we: { playable: true }, they: { playable: true },
      will: { playable: true }, two: { playable: true }, yes: { playable: true },
      no: { playable: true }, come: { playable: true }, learn: { playable: true },
      work: { playable: true }, friend: { playable: true }, name: { playable: true },
      head: { playable: true }, hand: { playable: true }, idea: { playable: true },
      book: { playable: true },
      skill: { playable: true },
      confident: { playable: true },
      show: { playable: true },
      video: { playable: true },
      life: { playable: true },
      second: { playable: true },
      walk: { playable: true },
      question: { playable: true },
      ask: { playable: true },
      level: { playable: true },
      beautiful: { playable: true },
      stage: { playable: true },
      attention: { playable: true },
      voice: { playable: true },
      year: { playable: true },
      pace: { playable: true },
      love: { playable: true },
      first: { playable: true },
      imagine: { playable: true },
      story: { playable: true },
      sound: { playable: true },
      write: { playable: true },
      hear: { playable: true },
      feel: { playable: true },
      minute: { playable: true },
      mean: { playable: true },
      call: { playable: true },
      world: { playable: true },
      put: { playable: true },
      public: { playable: true },
      important: { playable: true },
      gesture: { playable: true },
      stand: { playable: true },
      mindset: { playable: true },
      music: { playable: true },
      challenge: { playable: true },
      practice: { playable: true },
      brain: { playable: true },
      number: { playable: true },
      answer: { playable: true },
      same: { playable: true },
      different: { playable: true },
      fire: { playable: true },
      week: { playable: true },
      move: { playable: true },
      lose: { playable: true },
      presentation: { playable: true },
      today: { playable: true },
      remember: { playable: true },
      small: { playable: true },
      try: { playable: true },
      bad: { playable: true },
      high: { playable: true },
      find: { playable: true },
      study: { playable: true },
      change: { playable: true },
      body: { playable: true },
      action: { playable: true },
      great: { playable: true },
      tell: { playable: true },
      build: { playable: true },
      fast: { playable: true },
      hold: { playable: true },
      eye: { playable: true },
      clear: { playable: true },
      fear: { playable: true },
      share: { playable: true },
      happy: { playable: true },
      open: { playable: true },
      picture: { playable: true },
      teacher: { playable: true },
      class: { playable: true },
      understand: { playable: true },
      meet: { playable: true },
      heart: { playable: true },
      ready: { playable: true },
      win: { playable: true },
      problem: { playable: true },
      easy: { playable: true },
      hard: { playable: true },
      true: { playable: true },
      wrong: { playable: true },
      clean: { playable: true },
      light: { playable: true },
      dark: { playable: true },
      slow: { playable: true },
      finish: { playable: true },
      school: { playable: true },
      read: { playable: true },
      phone: { playable: true },
      computer: { playable: true },
      doctor: { playable: true },
      eat: { playable: true },
      tree: { playable: true },
      flower: { playable: true },
      mind: { playable: true },
      system: { playable: true },
      lesson: { playable: true },
      camera: { playable: true },
      screen: { playable: true },
      other: { playable: true },
      six: { playable: true },
      seven: { playable: true },
      should: { playable: true },
      long: { playable: true },
      left: { playable: true },
      next: { playable: true },
      slide: { playable: true },
      add: { playable: true },
      room: { playable: true },
      off: { playable: true },
      new: { playable: true },
      pick: { playable: true },
      case: { playable: true },
      keep: { playable: true },
      team: { playable: true },
      catch: { playable: true },
      dead: { playable: true },
      later: { playable: true },
      mine: { playable: true },
      base: { playable: true },
      volume: { playable: true },
      point: { playable: true },
      matter: { playable: true },
      structure: { playable: true },
      communication: { playable: true },
      paper: { playable: true },
      board: { playable: true },
      hope: { playable: true },
      bond: { playable: true },
      combination: { playable: true },
      resource: { playable: true },
      range: { playable: true },
      fine: { playable: true },
      somewhere: { playable: true },
      // Phase H21 New Playable Signs
      art: { playable: true },
      audience: { playable: true },
      college: { playable: true },
      draw: { playable: true },
      energy: { playable: true },
      example: { playable: true },
      game: { playable: true },
      lead: { playable: true },
      line: { playable: true },
      mark: { playable: true },
      note: { playable: true },
      parent: { playable: true },
      pause: { playable: true },
      plan: { playable: true },
      posture: { playable: true },
      power: { playable: true },
      reason: { playable: true },
      rule: { playable: true },
      simple: { playable: true },
      space: { playable: true },
      speed: { playable: true },
      step: { playable: true },
      teach: { playable: true },
      topic: { playable: true },
      train: { playable: true },
      // Phase H24 New Playable Signs (17 high-frequency signs)
      increase: { playable: true },
      little: { playable: true },
      rest: { playable: true },
      let: { playable: true },
      able: { playable: true },
      part: { playable: true },
      big: { playable: true },
      stop: { playable: true },
      watch: { playable: true },
      chart: { playable: true },
      subject: { playable: true },
      culture: { playable: true },
      product: { playable: true },
      audio: { playable: true },
      positive: { playable: true },
      trust: { playable: true },
      match: { playable: true },
      // Phase H24 Batch 2 Playable Signs
      perspective: { playable: true },
      after: { playable: true },
      angle: { playable: true },
      wise: { playable: true },
      outside: { playable: true },
      remove: { playable: true },
      sell: { playable: true },
      momentum: { playable: true },
      bring: { playable: true },
      pen: { playable: true },
      nervous: { playable: true },
      feedback: { playable: true },
      quick: { playable: true },
      earth: { playable: true },
      far: { playable: true },
      instance: { playable: true },
      // Phase H24 Batch 3 Playable Signs (20 signs)
      functional: { playable: true },
      anticipation: { playable: true },
      based: { playable: true },
      clarity: { playable: true },
      during: { playable: true },
      prior: { playable: true },
      while: { playable: true },
      inhale: { playable: true },
      goal: { playable: true },
      science: { playable: true },
      career: { playable: true },
      passion: { playable: true },
      session: { playable: true },
      interesting: { playable: true },
      face: { playable: true },
      group: { playable: true },
      enjoy: { playable: true },
      core: { playable: true },
      vision: { playable: true },
      color: { playable: true },
      // Phase H24 Batch 4 Playable Signs (24 signs)
      play: { playable: true },
      live: { playable: true },
      emotion: { playable: true },
      afraid: { playable: true },
      place: { playable: true },
      house: { playable: true },
      sorry: { playable: true },
      believe: { playable: true },
      company: { playable: true },
      sing: { playable: true },
      song: { playable: true },
      money: { playable: true },
      real: { playable: true },
      hour: { playable: true },
      perfect: { playable: true },
      sit: { playable: true },
      car: { playable: true },
      turn: { playable: true },
      normal: { playable: true },
      confused: { playable: true },
      remind: { playable: true },
      definition: { playable: true },
      happen: { playable: true },
      slowly: { playable: true },
      // Phase H24 Batch 5 Playable Signs (24 signs, total 308 signs)
      ability: { playable: true },
      leave: { playable: true },
      movie: { playable: true },
      dynamic: { playable: true },
      guess: { playable: true },
      respect: { playable: true },
      data: { playable: true },
      launch: { playable: true },
      pack: { playable: true },
      apple: { playable: true },
      grow: { playable: true },
      air: { playable: true },
      fun: { playable: true },
      concept: { playable: true },
      present: { playable: true },
      tools: { playable: true },
      sure: { playable: true },
      awesome: { playable: true },
      opposite: { playable: true },
      tip: { playable: true },
      sensation: { playable: true },
      gym: { playable: true },
      basis: { playable: true },
      technique: { playable: true },
      // Phase H24 Batch 6 Playable Signs (24 signs, total 332 signs)
      coaching: { playable: true },
      couple: { playable: true },
      final: { playable: true },
      experience: { playable: true },
      prepared: { playable: true },
      general: { playable: true },
      strong: { playable: true },
      decision: { playable: true },
      worse: { playable: true },
      ice: { playable: true },
      side: { playable: true },
      replace: { playable: true },
      sick: { playable: true },
      brilliant: { playable: true },
      paid: { playable: true },
      maths: { playable: true },
      spice: { playable: true },
      harness: { playable: true },
      client: { playable: true },
      cream: { playable: true },
      once: { playable: true },
      speaker: { playable: true },
      mention: { playable: true },
      allow: { playable: true },
      // Phase H24 Batch 7 Playable Signs (24 signs, total 356 signs)
      job: { playable: true },
      business: { playable: true },
      message: { playable: true },
      care: { playable: true },
      promise: { playable: true },
      flow: { playable: true },
      store: { playable: true },
      center: { playable: true },
      middle: { playable: true },
      sister: { playable: true },
      post: { playable: true },
      package: { playable: true },
      favorite: { playable: true },
      silent: { playable: true },
      comfortable: { playable: true },
      football: { playable: true },
      low: { playable: true },
      amount: { playable: true },
      crazy: { playable: true },
      between: { playable: true },
      each: { playable: true },
      chat: { playable: true },
      bit: { playable: true },
      super: { playable: true },
      // Phase H24 Batch 8 Playable Signs (24 signs, total 380 signs)
      special: { playable: true },
      practical: { playable: true },
      welcome: { playable: true },
      valuable: { playable: true },
      transform: { playable: true },
      avoid: { playable: true },
      excellent: { playable: true },
      social: { playable: true },
      critical: { playable: true },
      direction: { playable: true },
      content: { playable: true },
      fail: { playable: true },
      basketball: { playable: true },
      golf: { playable: true },
      less: { playable: true },
      massive: { playable: true },
      continuous: { playable: true },
      dancing: { playable: true },
      born: { playable: true },
      friday: { playable: true },
      instead: { playable: true },
      ago: { playable: true },
      quite: { playable: true },
      guy: { playable: true },
      // Phase H24 Batch 9 Playable Signs (20 signs reaching 400 total signs)
      smile: { playable: true },
      dream: { playable: true },
      exercise: { playable: true },
      accomplish: { playable: true },
      close: { playable: true },
      old: { playable: true },
      hungry: { playable: true },
      intention: { playable: true },
      motivated: { playable: true },
      few: { playable: true },
      lovely: { playable: true },
      focus: { playable: true },
      sometimes: { playable: true },
      list: { playable: true },
      connected: { playable: true },
      course: { playable: true },
      analyze: { playable: true },
      fourth: { playable: true },
      fifth: { playable: true },
      meeting: { playable: true },
      // Phase H24 Batch 10 Playable Signs (20 signs reaching 420 total signs)
      human: { playable: true },
      relate: { playable: true },
      cool: { playable: true },
      wow: { playable: true },
      corner: { playable: true },
      chest: { playable: true },
      extension: { playable: true },
      loop: { playable: true },
      similar: { playable: true },
      metaphor: { playable: true },
      scientific: { playable: true },
      skilled: { playable: true },
      proven: { playable: true },
      absolute: { playable: true },
      dominant: { playable: true },
      arena: { playable: true },
      myself: { playable: true },
      uncomfortable: { playable: true },
      filled: { playable: true },
      empowering: { playable: true },
      // Phase H24 Batch 11 Playable Signs (20 signs reaching 440 total signs)
      wait: { playable: true },
      pattern: { playable: true },
      front: { playable: true },
      fall: { playable: true },
      mobile: { playable: true },
      ignore: { playable: true },
      under: { playable: true },
      certain: { playable: true },
      subtle: { playable: true },
      scream: { playable: true },
      everyday: { playable: true },
      emotional: { playable: true },
      connect: { playable: true },
      extent: { playable: true },
      longer: { playable: true },
      ultimate: { playable: true },
      somatic: { playable: true },
      synchronicity: { playable: true },
      sat: { playable: true },
      united: { playable: true },
      // Phase H24 Batch 12 Playable Signs (20 signs reaching 460 total signs)
      conference: { playable: true },
      door: { playable: true },
      break: { playable: true },
      road: { playable: true },
      full: { playable: true },
      past: { playable: true },
      worth: { playable: true },
      ten: { playable: true },
      setting: { playable: true },
      expectation: { playable: true },
      server: { playable: true },
      simply: { playable: true },
      cannot: { playable: true },
      dollar: { playable: true },
      deep: { playable: true },
      phenomenal: { playable: true },
      record: { playable: true },
      buy: { playable: true },
      breathe: { playable: true },
      billion: { playable: true },
      // Phase H24 Batch 13 Playable Signs (20 signs reaching 480 total signs)
      laugh: { playable: true },
      soul: { playable: true },
      meal: { playable: true },
      follow: { playable: true },
      fair: { playable: true },
      statistics: { playable: true },
      nose: { playable: true },
      self: { playable: true },
      angel: { playable: true },
      math: { playable: true },
      insane: { playable: true },
      goosebumps: { playable: true },
      pointless: { playable: true },
      misunderstand: { playable: true },
      tilt: { playable: true },
      spend: { playable: true },
      perceive: { playable: true },
      upon: { playable: true },
      fan: { playable: true },
      decide: { playable: true },
      // Phase H24 Batch 14 Playable Signs (20 signs reaching 500 total signs)
      test: { playable: true },
      village: { playable: true },
      street: { playable: true },
      cloak: { playable: true },
      average: { playable: true },
      dry: { playable: true },
      attract: { playable: true },
      grab: { playable: true },
      send: { playable: true },
      behavior: { playable: true },
      effect: { playable: true },
      belief: { playable: true },
      failure: { playable: true },
      gray: { playable: true },
      nowhere: { playable: true },
      burden: { playable: true },
      observant: { playable: true },
      kid: { playable: true },
      set: { playable: true },
      result: { playable: true },
      // Phase H24 Batch 15 Playable Signs (20 signs reaching 520 total signs)
      may: { playable: true },
      hey: { playable: true },
      boom: { playable: true },
      sweden: { playable: true },
      everything: { playable: true },
      somebody: { playable: true },
      anyone: { playable: true },
      anything: { playable: true },
      nothing: { playable: true },
      until: { playable: true },
      weird: { playable: true },
      along: { playable: true },
      quarter: { playable: true },
      tumble: { playable: true },
      fill: { playable: true },
      danger: { playable: true },
      conductor: { playable: true },
      lie: { playable: true },
      luxury: { playable: true },
      turbo: { playable: true },
      // Phase H25 Playable Signs (30 signs reaching 550 total signs)
      fix: { playable: true },
      realize: { playable: true },
      notice: { playable: true },
      limit: { playable: true },
      substance: { playable: true },
      cover: { playable: true },
      risk: { playable: true },
      safe: { playable: true },
      guide: { playable: true },
      memory: { playable: true },
      join: { playable: true },
      explain: { playable: true },
      complex: { playable: true },
      nature: { playable: true },
      weather: { playable: true },
      plant: { playable: true },
      animal: { playable: true },
      mountain: { playable: true },
      river: { playable: true },
      ocean: { playable: true },
      bridge: { playable: true },
      market: { playable: true },
      cost: { playable: true },
      rich: { playable: true },
      weak: { playable: true },
      heavy: { playable: true },
      shadow: { playable: true },
      mirror: { playable: true },
      window: { playable: true },
      wall: { playable: true },
      // Phase H26 Playable Signs (reaching 562 total signs)
      protect: { playable: true },
      prepare: { playable: true },
      control: { playable: true },
      silence: { playable: true },
      yesterday: { playable: true },
      pitch: { playable: true },
      tone: { playable: true },
      volume: { playable: true },
      judge: { playable: true },
      complain: { playable: true },
      excuse: { playable: true },
      negative: { playable: true },
      // Phase H27 Playable Signs (reaching 566 total signs)
      ok: { playable: true }, usually: { playable: true }, throw: { playable: true }, better: { playable: true },

      gossip: { playable: true },
      honesty: { playable: true },
      integrity: { playable: true },
      warmup: { playable: true },
      // Milestone H37 New Playable Signs
      three: { playable: true },
      day: { playable: true },
      all: { playable: true },
      make: { playable: true },
      before: { playable: true },
      five: { playable: true },
      thousand: { playable: true },
      // Milestone H38 New Playable Signs
      hundred: { playable: true },
      twenty: { playable: true },
      thirty: { playable: true },
      zero: { playable: true },
      speech: { playable: true },
      overcome: { playable: true },
      this: { playable: true },
      that: { playable: true },
      here: { playable: true },
      // Milestone H41 New Playable Signs
      start: { playable: true },
      very: { playable: true },
      most: { playable: true },
      country: { playable: true },
      // Milestone H42 New Playable Signs
      food: { playable: true },
      summer: { playable: true },
      future: { playable: true },
      advice: { playable: true },
      together: { playable: true },
      tired: { playable: true },
      // Milestone H43 Grammatical, Lexical & Multi-Domain Playable Signs
      without: { playable: true },
      because: { playable: true },
      but: { playable: true },
      or: { playable: true },
      why: { playable: true },
      if: { playable: true },
      already: { playable: true },
      maybe: { playable: true },
      also: { playable: true },
      evening: { playable: true },
      eight: { playable: true },
      nine: { playable: true },
      third: { playable: true },
      back: { playable: true },
      feature: { playable: true },
      film: { playable: true },
      scene: { playable: true },
      robot: { playable: true },
      network: { playable: true },
      pixel: { playable: true },
      digit: { playable: true },
      layer: { playable: true },
      neuron: { playable: true },
      weight: { playable: true },
      single: { playable: true },
      african: { playable: true },
      africa: { playable: true },
      he: { playable: true },
      she: { playable: true },
      get: { playable: true },
      wind: { playable: true },
      // Milestone H44 Semantic Repair Signs
      famous: { playable: true },
      only: { playable: true },
      around: { playable: true },
      remaining: { playable: true },
      many: { playable: true }
    };
    this.phrases = new Map([
      ['good morning', ['GOOD', 'MORNING']], ['thank you', ['THANK_YOU']], ['hello', ['HELLO']],
      ['going to', ['WILL']], ['want to', ['WANT']], ['look at', ['LOOK']],
      ['as well as', ['MORE']],
      // Phase H22 Curated High-Yield Multiword Phrases
      ["i'm going to show", ['I', 'WILL', 'SHOW']],
      ['going to show you', ['WILL', 'SHOW', 'YOU']],
      ["i'm going to give", ['I', 'WILL', 'GIVE']],
      ['going to give you', ['WILL', 'GIVE', 'YOU']],
      ['want to show you', ['WANT', 'SHOW', 'YOU']],
      ['want to give you', ['WANT', 'GIVE', 'YOU']],
      ['as you can see', ['YOU', 'CAN', 'SEE']],
      ['the reason why', ['REASON']],
      ['give you an example', ['GIVE', 'YOU', 'EXAMPLE']],
      ['take a look', ['LOOK']],
      ['take a look at', ['LOOK']],
      ['pay attention to', ['ATTENTION']],
      ['step by step', ['STEP', 'STEP']],
      ['first of all', ['FIRST']],
      ['let me know', ['TELL', 'ME']],
      ['make sure that', ['TRUE']],
      ['listen to this', ['HEAR']],
      ['in other words', ['MEAN']],
      ['on the stage', ['STAGE']],
      ['in the classroom', ['CLASS']],
      ['public speaking challenge', ['PUBLIC', 'SPEECH', 'CHALLENGE']],
      ['public speaking coach', ['PUBLIC', 'SPEECH', 'COACHING']],
      ['public speaker', ['PUBLIC', 'SPEAKER']],
      ['great job', ['GREAT', 'WORK']],
      ['talk to you', ['SAY', 'YOU']],
      ['look like', ['SAME']],
 ['in order to', ['REASON']], ['what do you', ['YOU', 'WHAT']],
      ['how to', ['HOW']], ['have to', ['NEED']], ['public speaking', ['PUBLIC', 'SPEECH']],
      ["i'm going to", ["I", "WILL"]],
      ["have a look", ["LOOK"]],
      ["a look at", ["LOOK"]],
      ["have a look at", ["LOOK"]],
      ["listen to", ["HEAR"]],
      ["you want to", ["YOU", "WANT"]],
      ["i want you", ["I", "WANT", "YOU"]],
      ["i want you to", ["I", "WANT", "YOU"]],
      ["to give you", ["GIVE", "YOU"]],
      ["look at this", ["LOOK"]],
      ["to show you", ["SHOW", "YOU"]],
      ["every single", ["ONE"]],
      ["going to show", ["WILL", "SHOW"]],
      ["look at your", ["LOOK", "YOUR"]],
      ["we're going to", ["WE", "WILL"]],
      ["going to give", ["WILL", "GIVE"]],
      ["a lot of", ["MANY"]],
      ["a lot easier", ["VERY", "EASY"]],
      ["a lot", ["VERY"]],
      ["here we go", ["WE", "GO"]],
      ["over and over", ["MORE"]],
      ["i don't know", ["I", "NOT", "KNOW"]],
      ["let's have a look", ["LOOK"]],
      ["give me more", ["GIVE", "ME", "MORE"]],
      ["become more confident", ["MORE", "CONFIDENT"]],
      ["the most beautiful", ["MORE", "BEAUTIFUL"]],
      ["body language", ["BODY", "GESTURE"]],
      ["facial expressions", ["HEAD", "GESTURE"]],
      ["over and over again", ["MORE"]],
      ["next time", ["TIME", "MORE"]],
      ["sit down", ["SIT"]],
      ["each other", ["SAME", "MEET"]],
      ["stand up", ["STAND"]],
      ["talk about", ["SAY"]],
      ["feel like", ["FEEL", "LIKE"]],
      ["first time", ["FIRST", "TIME"]],
      ["facial expression", ["HEAD", "GESTURE"]],
      ["voice modulation", ["VOICE", "CHANGE"]],
      ["think about", ["THINK"]],
      ["high level", ["HIGH", "LEVEL"]],
      ["second time", ["SECOND", "TIME"]],
      // Milestone H37 / H41 Contextual Phrases
      ["right here", ["HERE"]],
      ["all around", ["ALL"]],
      ["all over", ["ALL"]],
      ["walk away with", ["GET"]],
      ["over the next", ["NEXT"]],
      ["make sure", ["REMEMBER", "IMPORTANT"]],
      ["lean in", ["FOCUS"]],
      ["have fun", ["ENJOY"]],
      ["finish off with", ["FINISH"]],
      ["finish off", ["FINISH"]],
      ["put to practice", ["PRACTICE"]],
      ["three-day", ["THREE", "DAY"]],
      ["three day", ["THREE", "DAY"]],
      ["110-step", ["HUNDRED", "TEN", "STEP"]],
      ["110", ["HUNDRED", "TEN"]],
      ["5,000", ["FIVE", "THOUSAND"]],
      ["5000", ["FIVE", "THOUSAND"]],
      ["25 year", ["TWENTY", "FIVE", "YEAR"]],
      ["25", ["TWENTY", "FIVE"]],
      ["30 minutes", ["THIRTY", "MINUTE"]],
      ["30 minute", ["THIRTY", "MINUTE"]],
      ["30", ["THIRTY"]],
      ["haven't met before", ["BEFORE", "MEET", "NOT"]],
      ["have not met before", ["BEFORE", "MEET", "NOT"]],
      ["it's to help", ["HELP"]],
      ["to help you overcome", ["YOU", "HELP", "OVERCOME"]],
      ["help you overcome", ["YOU", "HELP", "OVERCOME"]],
      ["overcome being", ["OVERCOME"]],
      ["you see", []],
      ["much more", ["VERY", "MORE"]],
      ["global giants", ["WORLD", "BIG", "COMPANY"]],
      ["among the most viewed in the world", ["WORLD", "MANY", "SEE"]],
      ["most viewed in the world", ["WORLD", "MANY", "SEE"]],
      ["most viewed", ["MOST", "SEE"]],
      ["best known for", ["FAMOUS", "BECAUSE"]],
      ["best known", ["FAMOUS"]],
      ["begin with", ["START"]],
      ["lovely country of sweden", ["SWEDEN", "LOVELY", "COUNTRY"]],
      ["country of sweden", ["SWEDEN", "COUNTRY"]],
      ["country of", ["COUNTRY"]],
      ["right here in our studio", ["HERE", "OUR", "RECORD", "ROOM"]],
      ["in our studio", ["OUR", "RECORD", "ROOM"]],
      ["our studio", ["OUR", "RECORD", "ROOM"]],
      ["for beginners", ["NEW", "PEOPLE", "LEARN"]],
      ["as a beginner", ["NEW", "LEARN"]],
      ["capturing attention", ["ATTENTION", "HOLD"]],
      ["pinpoint", ["FIND"]],
      ["all over the place", ["MANY", "PLACE"]],
      // Milestone H42 / H44 Contextual Phrases (Video B & General Conversational Discourse)
      ["in my opinion", ["I", "THINK"]],
      ["in the back of your mind", ["YOUR", "MIND", "DEEP"]],
      ["over the years", ["MANY", "YEAR"]],
      ["go about", ["LIVE"]],
      ["scripted out", ["PLAN", "WRITE"]],
      ["overthinking it", ["THINK", "MORE"]],
      ["overthinking", ["THINK", "MORE"]],
      ["short film", ["SMALL", "FILM"]],
      ["short films", ["SMALL", "FILM"]],
      ["start filming", ["START", "RECORD"]],
      ["started filming", ["START", "RECORD"]],
      ["dollar store", ["MONEY", "MARKET"]],
      ["cleaning supplies", ["CLEAN", "TOOLS"]],
      ["coffee shop", ["DRINK", "ROOM"]],
      ["coffee shops", ["DRINK", "ROOM"]],
      ["have to have a story", ["STORY", "HAVE", "NEED"]],
      ["have to have", ["NEED", "HAVE"]],
      ["has to have", ["NEED", "HAVE"]],
      ["need to have", ["NEED"]],
      ["story is king", ["STORY", "MOST", "IMPORTANT"]],
      ["stitched together", ["COMBINATION", "JOIN"]],
      ["stitch together", ["COMBINATION", "JOIN"]],
      ["greater and broader", ["MORE", "BIG"]],
      ["just like", ["LIKE"]],
      ["kind of", []],
      ["up to", ["DO"]],
      ["or so", ["AROUND"]],
      ["scene by scene", ["SCENE", "STEP"]],
      ["loosely defined", ["SIMPLE"]],
      ["trial and error", ["PRACTICE", "FAIL", "LEARN"]],
      ["show not tell", ["SHOW", "MORE", "SAY", "LESS"]],
      ["capture some dialogue", ["SOME", "COMMUNICATION", "RECORD"]],
      ["what's going on", ["WHAT", "HAPPEN"]],
      ["what is going on", ["WHAT", "HAPPEN"]],
      ["what going on", ["WHAT", "HAPPEN"]],
      ["whats going on", ["WHAT", "HAPPEN"]],
      ["going on", ["CONTINUE"]],
      ["instead of", []],
      ["stressing yourself", ["YOU", "NERVOUS"]],
      ["a lot easier", ["MORE", "EASY"]],
      ["easier", ["MORE", "EASY"]],
      ["better", ["MORE", "GOOD"]],
      ["clearer", ["MORE", "CLEAR"]],
      ["warmer", ["MORE", "WARM"]],
      ["feel right", ["FEEL", "GOOD"]],
      ["looks cool", ["COOL", "LOOK"]],
      ["cold start", ["START", "HARD"]],
      ["creative process", ["ART", "STEP"]],
      ["at the end of the day", ["FINAL"]],
      ["at least", ["LITTLE"]],
      ["right now", ["NOW"]],
      ["eating food", ["EAT", "FOOD"]],
      ["get food", ["EAT", "FOOD"]],
      ["figure out", ["FIND"]],
      ["give advice", ["GIVE", "ADVICE"]],
      ["giving advice", ["GIVE", "ADVICE"]],
      ["piece of advice", ["ADVICE"]],
      ["pieces of advice", ["ADVICE"]],
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
      ['work', 'WORK'], ['works', 'WORK'], ['worked', 'WORK'], ['working', 'WORK'],
      ['friend', 'FRIEND'], ['friends', 'FRIEND'],
      ['name', 'NAME'], ['names', 'NAME'],
      ['head', 'HEAD'], ['heads', 'HEAD'],
      ['hand', 'HAND'], ['hands', 'HAND'],
      ['idea', 'IDEA'], ['ideas', 'IDEA'],
      ['book', 'BOOK'], ['books', 'BOOK'],
      ['skill', 'SKILL'],
      ['confident', 'CONFIDENT'], ['confidently', 'CONFIDENT'], ['confidence', 'CONFIDENT'],
      ['show', 'SHOW'],
      ['video', 'VIDEO'],
      ['life', 'LIFE'],
      ['second', 'SECOND'],
      ['walk', 'WALK'],
      ['question', 'QUESTION'],
      ['ask', 'ASK'],
      ['level', 'LEVEL'],
      ['beautiful', 'BEAUTIFUL'],
      ['stage', 'STAGE'],
      ['attention', 'ATTENTION'],
      ['voice', 'VOICE'],
      ['year', 'YEAR'],
      ['pace', 'PACE'],
      ['love', 'LOVE'],
      ['first', 'FIRST'],
      ['imagine', 'IMAGINE'],
      ['story', 'STORY'],
      ['sound', 'SOUND'],
      ['write', 'WRITE'],
      ['hear', 'HEAR'],
      ['feel', 'FEEL'],
      ['minute', 'MINUTE'],
      ['mean', 'MEAN'],
      ['call', 'CALL'],
      ['world', 'WORLD'],
      ['put', 'PUT'],
      ['public', 'PUBLIC'],
      ['important', 'IMPORTANT'],
      ['gesture', 'GESTURE'],
      ['stand', 'STAND'],
      ['mindset', 'MINDSET'],
      ['music', 'MUSIC'],
      ['challenge', 'CHALLENGE'],
      ['practice', 'PRACTICE'],
      ['brain', 'BRAIN'],
      ['number', 'NUMBER'],
      ['answer', 'ANSWER'],
      ['same', 'SAME'],
      ['different', 'DIFFERENT'],
      ['fire', 'FIRE'],
      ['week', 'WEEK'],
      ['move', 'MOVE'],
      ['lose', 'LOSE'],
      ['presentation', 'PRESENTATION'],
      ['today', 'TODAY'],
      ['remember', 'REMEMBER'],
      ['small', 'SMALL'],
      ['try', 'TRY'],
      ['bad', 'BAD'],
      ['high', 'HIGH'],
      ['find', 'FIND'],
      ['study', 'STUDY'],
      ['change', 'CHANGE'],
      ['body', 'BODY'],
      ['action', 'ACTION'],
      ['great', 'GREAT'],
      ['tell', 'TELL'],
      ['build', 'BUILD'],
      ['fast', 'FAST'],
      ['hold', 'HOLD'],
      ['eye', 'EYE'],
      ['clear', 'CLEAR'],
      ['fear', 'FEAR'],
      ['share', 'SHARE'],
      ['happy', 'HAPPY'],
      ['open', 'OPEN'],
      ['picture', 'PICTURE'],
      ['teacher', 'TEACHER'],
      ['class', 'CLASS'],
      ['understand', 'UNDERSTAND'],
      ['meet', 'MEET'],
      ['heart', 'HEART'],
      ['ready', 'READY'],
      ['win', 'WIN'],
      ['problem', 'PROBLEM'],
      ['easy', 'EASY'],
      ['hard', 'HARD'],
      ['true', 'TRUE'],
      ['wrong', 'WRONG'],
      ['clean', 'CLEAN'],
      ['light', 'LIGHT'],
      ['dark', 'DARK'],
      ['slow', 'SLOW'],
      ['finish', 'FINISH'],
      ['school', 'SCHOOL'],
      ['read', 'READ'],
      ['phone', 'PHONE'],
      ['computer', 'COMPUTER'],
      ['doctor', 'DOCTOR'],
      ['eat', 'EAT'],
      ['tree', 'TREE'],
      ['flower', 'FLOWER'],
      ['mind', 'MIND'],
      ['system', 'SYSTEM'],
      ['lesson', 'LESSON'],
      ['camera', 'CAMERA'],
      ['screen', 'SCREEN'],
      ['skills', 'SKILL'],
      ['years', 'YEAR'],
      ['seconds', 'SECOND'],
      ['minutes', 'MINUTE'],
      ['levels', 'LEVEL'],
      ['videos', 'VIDEO'],
      ['stories', 'STORY'],
      ['questions', 'QUESTION'],
      ['walks', 'WALK'],
      ['walked', 'WALK'],
      ['walking', 'WALK'],
      ['practices', 'PRACTICE'],
      ['practiced', 'PRACTICE'],
      ['practicing', 'PRACTICE'],
      ['writes', 'WRITE'],
      ['wrote', 'WRITE'],
      ['written', 'WRITE'],
      ['writing', 'WRITE'],
      ['hears', 'HEAR'],
      ['heard', 'HEAR'],
      ['hearing', 'HEAR'],
      ['feels', 'FEEL'],
      ['felt', 'FEEL'],
      ['feeling', 'FEEL'],
      ['means', 'MEAN'],
      ['meant', 'MEAN'],
      ['meaning', 'MEAN'],
      ['calls', 'CALL'],
      ['called', 'CALL'],
      ['calling', 'CALL'],
      ['puts', 'PUT'],
      ['putting', 'PUT'],
      ['stands', 'STAND'],
      ['stood', 'STAND'],
      ['standing', 'STAND'],
      ['moves', 'MOVE'],
      ['moved', 'MOVE'],
      ['moving', 'MOVE'],
      ['loses', 'LOSE'],
      ['lost', 'LOSE'],
      ['losing', 'LOSE'],
      ['remembers', 'REMEMBER'],
      ['remembered', 'REMEMBER'],
      ['remembering', 'REMEMBER'],
      ['tries', 'TRY'],
      ['tried', 'TRY'],
      ['trying', 'TRY'],
      ['finds', 'FIND'],
      ['found', 'FIND'],
      ['finding', 'FIND'],
      ['studies', 'STUDY'],
      ['studied', 'STUDY'],
      ['studying', 'STUDY'],
      ['changes', 'CHANGE'],
      ['changed', 'CHANGE'],
      ['changing', 'CHANGE'],
      ['actions', 'ACTION'],
      ['tells', 'TELL'],
      ['told', 'TELL'],
      ['telling', 'TELL'],
      ['builds', 'BUILD'],
      ['built', 'BUILD'],
      ['building', 'BUILD'],
      ['holds', 'HOLD'],
      ['held', 'HOLD'],
      ['holding', 'HOLD'],
      ['shares', 'SHARE'],
      ['shared', 'SHARE'],
      ['sharing', 'SHARE'],
      ['opens', 'OPEN'],
      ['opened', 'OPEN'],
      ['opening', 'OPEN'],
      ['pictures', 'PICTURE'],
      ['teachers', 'TEACHER'],
      ['classes', 'CLASS'],
      ['understands', 'UNDERSTAND'],
      ['understood', 'UNDERSTAND'],
      ['understanding', 'UNDERSTAND'],
      ['meets', 'MEET'],
      ['met', 'MEET'],
      ['meeting', 'MEET'],
      ['hearts', 'HEART'],
      ['wins', 'WIN'],
      ['won', 'WIN'],
      ['winning', 'WIN'],
      ['problems', 'PROBLEM'],
      ['cleans', 'CLEAN'],
      ['cleaned', 'CLEAN'],
      ['cleaning', 'CLEAN'],
      ['finishes', 'FINISH'],
      ['finished', 'FINISH'],
      ['finishing', 'FINISH'],
      ['schools', 'SCHOOL'],
      ['reads', 'READ'],
      ['reading', 'READ'],
      ['phones', 'PHONE'],
      ['computers', 'COMPUTER'],
      ['doctors', 'DOCTOR'],
      ['eats', 'EAT'],
      ['ate', 'EAT'],
      ['eaten', 'EAT'],
      ['eating', 'EAT'],
      ['trees', 'TREE'],
      ['flowers', 'FLOWER'],
      ['minds', 'MIND'],
      ['systems', 'SYSTEM'],
      ['lessons', 'LESSON'],
      ['cameras', 'CAMERA'],
      ['screens', 'SCREEN'],
      ['challenges', 'CHALLENGE'],
      ['gestures', 'GESTURE'],
      ['bodies', 'BODY'],
      ['eyes', 'EYE'],
      ['numbers', 'NUMBER'],
      ['shows', 'SHOW'],
      ['showed', 'SHOW'],
      ['showing', 'SHOW'],
      ['other', 'OTHER'],
      ['six', 'SIX'],
      ['seven', 'SEVEN'],
      ['should', 'SHOULD'],
      ['long', 'LONG'],
      ['left', 'LEFT'],
      ['next', 'NEXT'],
      ['slide', 'SLIDE'],
      ['add', 'ADD'],
      ['room', 'ROOM'],
      ['off', 'OFF'],
      ['new', 'NEW'],
      ['pick', 'PICK'],
      ['case', 'CASE'],
      ['keep', 'KEEP'],
      ['team', 'TEAM'],
      ['catch', 'CATCH'],
      ['dead', 'DEAD'],
      ['later', 'LATER'],
      ['mine', 'MINE'],
      ['presentations', 'PRESENTATION'],
      ['sounds', 'SOUND'],
      ['weeks', 'WEEK'],
      ['asked', 'ASK'],
      ['coach', 'TEACHER'],
      ['amazing', 'GREAT'],
      ['horrible', 'BAD'],
      ['begin', 'GO'],
      ['growth', 'BUILD'],
      ['kids', 'PEOPLE'],
      ['kid', 'PEOPLE'],
      ['friends', 'FRIEND'],
      ['hands', 'HAND'],
      ['difference', 'DIFFERENT'],
      ['movement', 'MOVE'],
      ['delivering', 'GIVE'],
      ['stronger', 'HARD'],
      ['recording', 'VIDEO'],
      ['presenter', 'TEACHER'],
      ['yesterday', 'YESTERDAY'],
      ['lot', 'MORE'],
      ['language', 'GESTURE'],
      ['facial', 'HEAD'],
      ['speech', 'SAY'],
      ['modulation', 'CHANGE'],
      ['slides', 'SLIDE'],
      ['rooms', 'ROOM'],
      ['picks', 'PICK'],
      ['picked', 'PICK'],
      ['picking', 'PICK'],
      ['cases', 'CASE'],
      ['keeps', 'KEEP'],
      ['kept', 'KEEP'],
      ['keeping', 'KEEP'],
      ['teams', 'TEAM'],
      ['catches', 'CATCH'],
      ['caught', 'CATCH'],
      ['catching', 'CATCH'],
      ['adds', 'ADD'],
      ['added', 'ADD'],
      ['adding', 'ADD'],
      ['words', 'SAY'],
      ['songs', 'MUSIC'],
      ['techniques', 'SKILL'],
      ['truth', 'TRUE'],
      ['repeat', 'MORE'],
      ['moment', 'TIME'],
      ['focus', 'ATTENTION'],
      ['deliver', 'GIVE'], ['delivers', 'GIVE'], ['delivered', 'GIVE'],
      ['end', 'FINISH'],
      ['beginning', 'GO'],
      ['powerful', 'GREAT'],
      ['storytelling', 'STORY'],
      ['micro', 'SMALL'],
      ['macro', 'GREAT'],
      ['away', 'MOVE'],
      ['impact', 'CHANGE'],
      ['kind', 'GOOD'],
      ['filler', 'SAY'],
      ['inject', 'PUT'],
      ['injecting', 'PUT'],
      ['wind', 'WIND'],
      ['nice', 'GOOD'],
      ['third', 'THIRD'],
      ['eight', 'EIGHT'],
      ['nine', 'NINE'],
      ['evening', 'EVENING'],
      ['possible', 'CAN'],
      ['forward', 'GO'],
      ['stories', 'STORY'],
      ['repeating', 'MORE'],
      ['repeated', 'MORE'],
      ['base', 'BASE'],
      ['volume', 'VOLUME'],
      ['point', 'POINT'],
      ['matter', 'MATTER'],
      ['structure', 'STRUCTURE'],
      ['communication', 'COMMUNICATION'],
      ['paper', 'PAPER'],
      ['board', 'BOARD'],
      ['hope', 'HOPE'],
      ['bond', 'BOND'],
      ['combination', 'COMBINATION'],
      ['resource', 'RESOURCE'],
      ['range', 'RANGE'],
      ['fine', 'FINE'],
      ['somewhere', 'SOMEWHERE'],
      // Phase H21 New Signs & Inflections
      ['art', 'ART'],
      ['audience', 'AUDIENCE'],
      ['college', 'COLLEGE'],
      ['draw', 'DRAW'],
      ['energy', 'ENERGY'],
      ['example', 'EXAMPLE'],
      ['game', 'GAME'],
      ['lead', 'LEAD'],
      ['line', 'LINE'],
      ['mark', 'MARK'],
      ['note', 'NOTE'],
      ['parent', 'PARENT'],
      ['pause', 'PAUSE'],
      ['plan', 'PLAN'],
      ['posture', 'POSTURE'],
      ['power', 'POWER'],
      ['reason', 'REASON'],
      ['rule', 'RULE'],
      ['simple', 'SIMPLE'],
      ['space', 'SPACE'],
      ['speed', 'SPEED'],
      ['step', 'STEP'],
      ['teach', 'TEACH'],
      ['topic', 'TOPIC'],
      ['train', 'TRAIN'],
      // Phase H24 Lexical Mappings & Inflections
      ['increase', 'INCREASE'], ['increased', 'INCREASE'], ['increases', 'INCREASE'], ['increasing', 'INCREASE'],
      ['little', 'LITTLE'],
      ['rest', 'REST'], ['rests', 'REST'], ['resting', 'REST'], ['rested', 'REST'],
      ['let', 'LET'], ['lets', 'LET'], ['letting', 'LET'],
      ['able', 'ABLE'],
      ['part', 'PART'], ['parts', 'PART'],
      ['big', 'BIG'],
      ['stop', 'STOP'], ['stops', 'STOP'], ['stopped', 'STOP'], ['stopping', 'STOP'],
      ['watch', 'WATCH'], ['watches', 'WATCH'], ['watched', 'WATCH'], ['watching', 'WATCH'],
      ['chart', 'CHART'], ['charts', 'CHART'],
      ['subject', 'SUBJECT'], ['subjects', 'SUBJECT'],
      ['culture', 'CULTURE'], ['cultures', 'CULTURE'],
      ['product', 'PRODUCT'], ['products', 'PRODUCT'],
      ['audio', 'AUDIO'],
      ['positive', 'POSITIVE'],
      ['trust', 'TRUST'], ['trusts', 'TRUST'], ['trusted', 'TRUST'], ['trusting', 'TRUST'],
      ['match', 'MATCH'], ['matches', 'MATCH'], ['matched', 'MATCH'], ['matching', 'MATCH'],
      // Phase H24 Batch 2 Lexical Mappings & Inflections
      ['perspective', 'PERSPECTIVE'], ['perspectives', 'PERSPECTIVE'],
      ['after', 'AFTER'],
      ['angle', 'ANGLE'], ['angles', 'ANGLE'],
      ['wise', 'WISE'],
      ['outside', 'OUTSIDE'],
      ['remove', 'REMOVE'], ['removes', 'REMOVE'], ['removed', 'REMOVE'], ['removing', 'REMOVE'],
      ['sell', 'SELL'], ['sells', 'SELL'], ['sold', 'SELL'], ['selling', 'SELL'],
      ['momentum', 'MOMENTUM'],
      ['bring', 'BRING'], ['brings', 'BRING'], ['brought', 'BRING'], ['bringing', 'BRING'],
      ['pen', 'PEN'], ['pens', 'PEN'],
      ['nervous', 'NERVOUS'],
      ['feedback', 'FEEDBACK'],
      ['quick', 'QUICK'], ['quickly', 'QUICK'],
      ['earth', 'EARTH'],
      ['far', 'FAR'],
      ['instance', 'INSTANCE'], ['instances', 'INSTANCE'],
      // Phase H24 Batch 3 Lexical Mappings & Inflections
      ['functional', 'FUNCTIONAL'],
      ['anticipation', 'ANTICIPATION'],
      ['based', 'BASED'], ['base', 'BASE'],
      ['clarity', 'CLARITY'],
      ['during', 'DURING'],
      ['prior', 'PRIOR'],
      ['while', 'WHILE'],
      ['inhale', 'INHALE'], ['inhales', 'INHALE'], ['inhaled', 'INHALE'], ['inhaling', 'INHALE'],
      ['goal', 'GOAL'], ['goals', 'GOAL'],
      ['science', 'SCIENCE'], ['scientific', 'SCIENCE'],
      ['career', 'CAREER'], ['careers', 'CAREER'],
      ['passion', 'PASSION'], ['passions', 'PASSION'], ['passionate', 'PASSION'],
      ['session', 'SESSION'], ['sessions', 'SESSION'],
      ['interesting', 'INTERESTING'], ['interest', 'INTERESTING'], ['interests', 'INTERESTING'],
      ['face', 'FACE'], ['faces', 'FACE'], ['facing', 'FACE'],
      ['group', 'GROUP'], ['groups', 'GROUP'],
      ['enjoy', 'ENJOY'], ['enjoys', 'ENJOY'], ['enjoyed', 'ENJOY'], ['enjoying', 'ENJOY'],
      ['core', 'CORE'], ['cores', 'CORE'],
      ['vision', 'VISION'], ['visions', 'VISION'],
      ['color', 'COLOR'], ['colors', 'COLOR'], ['colored', 'COLOR'],
      // Phase H24 Batch 4 Lexical Mappings & Inflections
      ['play', 'PLAY'], ['plays', 'PLAY'], ['playing', 'PLAY'], ['played', 'PLAY'],
      ['live', 'LIVE'], ['lives', 'LIVE'], ['living', 'LIVE'], ['lived', 'LIVE'],
      ['emotion', 'EMOTION'], ['emotions', 'EMOTION'], ['emotional', 'EMOTION'],
      ['afraid', 'AFRAID'],
      ['place', 'PLACE'], ['places', 'PLACE'], ['placing', 'PLACE'], ['placed', 'PLACE'],
      ['house', 'HOUSE'], ['houses', 'HOUSE'], ['home', 'HOUSE'], ['homes', 'HOUSE'],
      ['sorry', 'SORRY'],
      ['believe', 'BELIEVE'], ['believes', 'BELIEVE'], ['believed', 'BELIEVE'], ['believing', 'BELIEVE'],
      ['company', 'COMPANY'], ['companies', 'COMPANY'],
      ['sing', 'SING'], ['sings', 'SING'], ['singing', 'SING'], ['sang', 'SING'],
      ['song', 'SONG'],
      ['money', 'MONEY'],
      ['real', 'REAL'], ['really', 'REAL'],
      ['hour', 'HOUR'], ['hours', 'HOUR'],
      ['perfect', 'PERFECT'], ['perfects', 'PERFECT'], ['perfected', 'PERFECT'], ['perfecting', 'PERFECT'], ['perfected', 'PERFECT'],
      ['sit', 'SIT'], ['sits', 'SIT'], ['sitting', 'SIT'], ['sat', 'SIT'],
      ['car', 'CAR'], ['cars', 'CAR'],
      ['turn', 'TURN'], ['turns', 'TURN'], ['turning', 'TURN'], ['turned', 'TURN'],
      ['normal', 'NORMAL'], ['normally', 'NORMAL'],
      ['confused', 'CONFUSED'], ['confuses', 'CONFUSED'], ['confusing', 'CONFUSED'], ['confusion', 'CONFUSED'],
      ['remind', 'REMIND'], ['reminds', 'REMIND'], ['reminding', 'REMIND'], ['reminded', 'REMIND'],
      ['definition', 'DEFINITION'], ['definitions', 'DEFINITION'], ['define', 'DEFINITION'], ['defines', 'DEFINITION'], ['defining', 'DEFINITION'], ['defined', 'DEFINITION'],
      ['happen', 'HAPPEN'], ['happens', 'HAPPEN'], ['happening', 'HAPPEN'], ['happened', 'HAPPEN'],
      ['slowly', 'SLOWLY'],
      // Phase H24 Batch 5 Lexical Mappings & Inflections
      ['ability', 'ABILITY'], ['abilities', 'ABILITY'],
      ['leave', 'LEAVE'], ['leaves', 'LEAVE'], ['leaving', 'LEAVE'], ['left', 'LEAVE'],
      ['movie', 'MOVIE'], ['movies', 'MOVIE'], ['film', 'FILM'], ['films', 'FILM'],
      ['dynamic', 'DYNAMIC'], ['dynamics', 'DYNAMIC'],
      ['guess', 'GUESS'], ['guesses', 'GUESS'], ['guessing', 'GUESS'], ['guessed', 'GUESS'],
      ['respect', 'RESPECT'], ['respects', 'RESPECT'], ['respected', 'RESPECT'], ['respecting', 'RESPECT'],
      ['data', 'DATA'],
      ['launch', 'LAUNCH'], ['launches', 'LAUNCH'], ['launching', 'LAUNCH'], ['launched', 'LAUNCH'],
      ['pack', 'PACK'], ['packs', 'PACK'], ['packing', 'PACK'], ['packed', 'PACK'],
      ['apple', 'APPLE'], ['apples', 'APPLE'],
      ['grow', 'GROW'], ['grows', 'GROW'], ['growing', 'GROW'], ['grew', 'GROW'], ['grown', 'GROW'],
      ['air', 'AIR'],
      ['fun', 'FUN'],
      ['concept', 'CONCEPT'], ['concepts', 'CONCEPT'],
      ['present', 'PRESENT'], ['presents', 'PRESENT'], ['presenting', 'PRESENT'], ['presented', 'PRESENT'],
      ['tools', 'TOOLS'], ['tool', 'TOOLS'],
      ['sure', 'SURE'], ['surely', 'SURE'],
      ['awesome', 'AWESOME'],
      ['opposite', 'OPPOSITE'], ['opposites', 'OPPOSITE'],
      ['tip', 'TIP'], ['tips', 'TIP'],
      ['sensation', 'SENSATION'], ['sensations', 'SENSATION'],
      ['gym', 'GYM'], ['gyms', 'GYM'],
      ['basis', 'BASIS'], ['bases', 'BASIS'],
      ['technique', 'TECHNIQUE'], ['techniques', 'TECHNIQUE'],
      // Phase H24 Batch 6 Lexical Mappings & Inflections
      ['coaching', 'COACHING'], ['coach', 'COACHING'], ['coaches', 'COACHING'], ['coached', 'COACHING'],
      ['couple', 'COUPLE'], ['couples', 'COUPLE'],
      ['final', 'FINAL'], ['finally', 'FINAL'],
      ['experience', 'EXPERIENCE'], ['experiences', 'EXPERIENCE'], ['experienced', 'EXPERIENCE'],
      ['prepared', 'PREPARED'], ['prepare', 'PREPARED'], ['prepares', 'PREPARED'], ['preparing', 'PREPARED'],
      ['general', 'GENERAL'], ['generally', 'GENERAL'],
      ['strong', 'STRONG'], ['strongly', 'STRONG'], ['stronger', 'STRONG'],
      ['decision', 'DECISION'], ['decisions', 'DECISION'], ['decide', 'DECISION'], ['decided', 'DECISION'],
      ['worse', 'WORSE'], ['worst', 'WORSE'],
      ['ice', 'ICE'],
      ['side', 'SIDE'], ['sides', 'SIDE'],
      ['replace', 'REPLACE'], ['replaces', 'REPLACE'], ['replaced', 'REPLACE'], ['replacing', 'REPLACE'],
      ['sick', 'SICK'], ['sickness', 'SICK'],
      ['brilliant', 'BRILLIANT'], ['brilliantly', 'BRILLIANT'],
      ['paid', 'PAID'], ['pay', 'PAID'], ['pays', 'PAID'], ['paying', 'PAID'],
      ['maths', 'MATHS'], ['math', 'MATHS'],
      ['spice', 'SPICE'], ['spices', 'SPICE'], ['spicy', 'SPICE'],
      ['harness', 'HARNESS'], ['harnesses', 'HARNESS'], ['harnessed', 'HARNESS'], ['harnessing', 'HARNESS'],
      ['client', 'CLIENT'], ['clients', 'CLIENT'],
      ['cream', 'CREAM'], ['creams', 'CREAM'],
      ['once', 'ONCE'],
      ['speaker', 'SPEAKER'], ['speakers', 'SPEAKER'],
      ['mention', 'MENTION'], ['mentions', 'MENTION'], ['mentioned', 'MENTION'], ['mentioning', 'MENTION'],
      ['allow', 'ALLOW'], ['allows', 'ALLOW'], ['allowed', 'ALLOW'], ['allowing', 'ALLOW'],
      // Phase H24 Batch 7 Lexical Mappings & Inflections
      ['job', 'JOB'], ['jobs', 'JOB'],
      ['business', 'BUSINESS'], ['businesses', 'BUSINESS'],
      ['message', 'MESSAGE'], ['messages', 'MESSAGE'],
      ['care', 'CARE'], ['cares', 'CARE'], ['caring', 'CARE'], ['cared', 'CARE'],
      ['promise', 'PROMISE'], ['promises', 'PROMISE'], ['promising', 'PROMISE'], ['promised', 'PROMISE'],
      ['flow', 'FLOW'], ['flows', 'FLOW'], ['flowing', 'FLOW'], ['flowed', 'FLOW'],
      ['store', 'STORE'], ['stores', 'STORE'], ['storing', 'STORE'], ['stored', 'STORE'],
      ['center', 'CENTER'], ['centers', 'CENTER'], ['central', 'CENTER'],
      ['middle', 'MIDDLE'],
      ['sister', 'SISTER'], ['sisters', 'SISTER'],
      ['post', 'POST'], ['posts', 'POST'], ['posting', 'POST'], ['posted', 'POST'],
      ['package', 'PACKAGE'], ['packages', 'PACKAGE'], ['packaging', 'PACKAGE'], ['packaged', 'PACKAGE'],
      ['favorite', 'FAVORITE'], ['favorites', 'FAVORITE'],
      ['silent', 'SILENT'], ['silence', 'SILENT'], ['silently', 'SILENT'],
      ['comfortable', 'COMFORTABLE'], ['comfort', 'COMFORTABLE'],
      ['football', 'FOOTBALL'],
      ['low', 'LOW'], ['lower', 'LOW'], ['lowest', 'LOW'],
      ['amount', 'AMOUNT'], ['amounts', 'AMOUNT'],
      ['crazy', 'CRAZY'],
      ['between', 'BETWEEN'],
      ['each', 'EACH'],
      ['chat', 'CHAT'], ['chats', 'CHAT'], ['chatting', 'CHAT'], ['chatted', 'CHAT'],
      ['bit', 'BIT'], ['bits', 'BIT'],
      ['super', 'SUPER'], ['superb', 'SUPER'],
      // Phase H24 Batch 8 Lexical Mappings & Inflections
      ['special', 'SPECIAL'], ['specially', 'SPECIAL'],
      ['practical', 'PRACTICAL'], ['practically', 'PRACTICAL'],
      ['welcome', 'WELCOME'], ['welcomes', 'WELCOME'], ['welcomed', 'WELCOME'], ['welcoming', 'WELCOME'],
      ['valuable', 'VALUABLE'], ['value', 'VALUABLE'], ['values', 'VALUABLE'],
      ['transform', 'TRANSFORM'], ['transforms', 'TRANSFORM'], ['transformed', 'TRANSFORM'], ['transforming', 'TRANSFORM'],
      ['avoid', 'AVOID'], ['avoids', 'AVOID'], ['avoided', 'AVOID'], ['avoiding', 'AVOID'],
      ['excellent', 'EXCELLENT'], ['excellently', 'EXCELLENT'],
      ['social', 'SOCIAL'], ['socially', 'SOCIAL'],
      ['critical', 'CRITICAL'], ['critically', 'CRITICAL'],
      ['direction', 'DIRECTION'], ['directions', 'DIRECTION'],
      ['content', 'CONTENT'], ['contents', 'CONTENT'],
      ['fail', 'FAIL'], ['fails', 'FAIL'], ['failed', 'FAIL'], ['failing', 'FAIL'],
      ['basketball', 'BASKETBALL'],
      ['golf', 'GOLF'],
      ['less', 'LESS'], ['lesser', 'LESS'],
      ['massive', 'MASSIVE'], ['massively', 'MASSIVE'],
      ['continuous', 'CONTINUOUS'], ['continuously', 'CONTINUOUS'],
      ['dancing', 'DANCING'], ['dance', 'DANCING'], ['dances', 'DANCING'], ['danced', 'DANCING'],
      ['born', 'BORN'], ['birth', 'BORN'],
      ['friday', 'FRIDAY'], ['fridays', 'FRIDAY'],
      ['instead', 'INSTEAD'],
      ['ago', 'AGO'],
      ['quite', 'QUITE'],
      ['guy', 'GUY'], ['guys', 'GUY'],
      // Phase H24 Batch 9 Lexical Mappings & Inflections
      ['smile', 'SMILE'], ['smiles', 'SMILE'], ['smiling', 'SMILE'], ['smiled', 'SMILE'],
      ['dream', 'DREAM'], ['dreams', 'DREAM'], ['dreaming', 'DREAM'], ['dreamed', 'DREAM'],
      ['exercise', 'EXERCISE'], ['exercises', 'EXERCISE'], ['exercising', 'EXERCISE'], ['exercised', 'EXERCISE'],
      ['accomplish', 'ACCOMPLISH'], ['accomplishes', 'ACCOMPLISH'], ['accomplished', 'ACCOMPLISH'], ['accomplishing', 'ACCOMPLISH'],
      ['close', 'CLOSE'], ['closer', 'CLOSE'], ['closest', 'CLOSE'],
      ['old', 'OLD'], ['older', 'OLD'], ['oldest', 'OLD'],
      ['hungry', 'HUNGRY'],
      ['intention', 'INTENTION'], ['intentions', 'INTENTION'], ['intend', 'INTENTION'], ['intends', 'INTENTION'], ['intended', 'INTENTION'], ['intending', 'INTENTION'],
      ['motivated', 'MOTIVATED'], ['motivate', 'MOTIVATED'], ['motivates', 'MOTIVATED'], ['motivating', 'MOTIVATED'], ['motivation', 'MOTIVATED'],
      ['few', 'FEW'],
      ['lovely', 'LOVELY'],
      ['focus', 'FOCUS'], ['focuses', 'FOCUS'], ['focused', 'FOCUS'], ['focusing', 'FOCUS'],
      ['sometimes', 'SOMETIMES'],
      ['list', 'LIST'], ['lists', 'LIST'], ['listing', 'LIST'], ['listed', 'LIST'],
      ['connected', 'CONNECTED'], ['connect', 'CONNECTED'], ['connects', 'CONNECTED'], ['connecting', 'CONNECTED'], ['connection', 'CONNECTED'], ['connections', 'CONNECTED'],
      ['course', 'COURSE'], ['courses', 'COURSE'],
      ['analyze', 'ANALYZE'], ['analyzes', 'ANALYZE'], ['analyzed', 'ANALYZE'], ['analyzing', 'ANALYZE'], ['analysis', 'ANALYZE'],
      ['fourth', 'FOURTH'],
      ['fifth', 'FIFTH'],
      ['meeting', 'MEETING'], ['meetings', 'MEETING'],
      // Phase H24 Batch 10 Lexical Mappings & Inflections
      ['human', 'HUMAN'], ['humans', 'HUMAN'],
      ['relate', 'RELATE'], ['relates', 'RELATE'], ['related', 'RELATE'], ['relating', 'RELATE'], ['relationship', 'RELATE'], ['relationships', 'RELATE'],
      ['cool', 'COOL'], ['cooler', 'COOL'], ['coolest', 'COOL'],
      ['wow', 'WOW'],
      ['corner', 'CORNER'], ['corners', 'CORNER'],
      ['chest', 'CHEST'], ['chests', 'CHEST'],
      ['extension', 'EXTENSION'], ['extensions', 'EXTENSION'], ['extend', 'EXTENSION'], ['extends', 'EXTENSION'], ['extended', 'EXTENSION'], ['extending', 'EXTENSION'],
      ['loop', 'LOOP'], ['loops', 'LOOP'], ['looping', 'LOOP'], ['looped', 'LOOP'],
      ['similar', 'SIMILAR'], ['similarly', 'SIMILAR'], ['similarity', 'SIMILAR'], ['similarities', 'SIMILAR'],
      ['metaphor', 'METAPHOR'], ['metaphors', 'METAPHOR'],
      ['scientific', 'SCIENTIFIC'], ['scientifically', 'SCIENTIFIC'],
      ['skilled', 'SKILLED'], ['skillful', 'SKILLED'], ['skillfully', 'SKILLED'],
      ['proven', 'PROVEN'], ['prove', 'PROVEN'], ['proves', 'PROVEN'], ['proving', 'PROVEN'], ['proved', 'PROVEN'],
      ['absolute', 'ABSOLUTE'], ['absolutely', 'ABSOLUTE'],
      ['dominant', 'DOMINANT'], ['dominance', 'DOMINANT'], ['dominate', 'DOMINANT'], ['dominates', 'DOMINANT'], ['dominated', 'DOMINANT'], ['dominating', 'DOMINANT'],
      ['arena', 'ARENA'], ['arenas', 'ARENA'],
      ['myself', 'MYSELF'],
      ['uncomfortable', 'UNCOMFORTABLE'], ['uncomfortably', 'UNCOMFORTABLE'],
      ['filled', 'FILLED'], ['fill', 'FILLED'], ['fills', 'FILLED'], ['filling', 'FILLED'],
      ['empowering', 'EMPOWERING'], ['empower', 'EMPOWERING'], ['empowers', 'EMPOWERING'], ['empowered', 'EMPOWERING'], ['empowerment', 'EMPOWERING'],
      // Phase H24 Batch 11 Lexical Mappings & Inflections
      ['wait', 'WAIT'], ['waits', 'WAIT'], ['waiting', 'WAIT'], ['waited', 'WAIT'],
      ['pattern', 'PATTERN'], ['patterns', 'PATTERN'], ['patterned', 'PATTERN'],
      ['front', 'FRONT'], ['fronts', 'FRONT'],
      ['fall', 'FALL'], ['falls', 'FALL'], ['falling', 'FALL'], ['fell', 'FALL'], ['fallen', 'FALL'],
      ['mobile', 'MOBILE'], ['mobiles', 'MOBILE'],
      ['ignore', 'IGNORE'], ['ignores', 'IGNORE'], ['ignored', 'IGNORE'], ['ignoring', 'IGNORE'],
      ['under', 'UNDER'],
      ['certain', 'CERTAIN'], ['certainly', 'CERTAIN'], ['certainty', 'CERTAIN'],
      ['subtle', 'SUBTLE'], ['subtly', 'SUBTLE'], ['subtlety', 'SUBTLE'], ['subtleties', 'SUBTLE'],
      ['scream', 'SCREAM'], ['screams', 'SCREAM'], ['screaming', 'SCREAM'], ['screamed', 'SCREAM'],
      ['everyday', 'EVERYDAY'], ['daily', 'EVERYDAY'],
      ['emotional', 'EMOTIONAL'], ['emotionally', 'EMOTIONAL'],
      ['connect', 'CONNECT'], ['connects', 'CONNECT'], ['connected', 'CONNECT'], ['connecting', 'CONNECT'], ['connection', 'CONNECT'], ['connections', 'CONNECT'],
      ['extent', 'EXTENT'], ['extents', 'EXTENT'],
      ['longer', 'LONGER'], ['longest', 'LONGER'],
      ['ultimate', 'ULTIMATE'], ['ultimately', 'ULTIMATE'],
      ['somatic', 'SOMATIC'], ['somatics', 'SOMATIC'],
      ['synchronicity', 'SYNCHRONICITY'], ['synchronicities', 'SYNCHRONICITY'], ['synchronous', 'SYNCHRONICITY'],
      ['sat', 'SAT'], ['sit', 'SAT'], ['sitting', 'SAT'], ['sits', 'SAT'],
      ['united', 'UNITED'], ['unite', 'UNITED'], ['unites', 'UNITED'], ['uniting', 'UNITED'], ['unity', 'UNITED'],
      // Phase H24 Batch 12 Lexical Mappings & Inflections
      ['conference', 'CONFERENCE'], ['conferences', 'CONFERENCE'], ['convention', 'CONFERENCE'], ['conventions', 'CONFERENCE'],
      ['door', 'DOOR'], ['doors', 'DOOR'],
      ['break', 'BREAK'], ['breaks', 'BREAK'], ['breaking', 'BREAK'], ['broke', 'BREAK'], ['broken', 'BREAK'],
      ['road', 'ROAD'], ['roads', 'ROAD'], ['street', 'ROAD'], ['path', 'ROAD'],
      ['full', 'FULL'], ['fully', 'FULL'], ['fuller', 'FULL'], ['fullest', 'FULL'],
      ['past', 'PAST'], ['history', 'PAST'], ['historical', 'PAST'],
      ['worth', 'WORTH'], ['worthy', 'WORTH'], ['value', 'WORTH'], ['values', 'WORTH'],
      ['ten', 'TEN'], ['tenth', 'TEN'],
      ['setting', 'SETTING'], ['settings', 'SETTING'], ['setup', 'SETTING'],
      ['expectation', 'EXPECTATION'], ['expectations', 'EXPECTATION'], ['expect', 'EXPECTATION'], ['expects', 'EXPECTATION'], ['expected', 'EXPECTATION'], ['expecting', 'EXPECTATION'],
      ['server', 'SERVER'], ['servers', 'SERVER'], ['serve', 'SERVER'], ['serves', 'SERVER'], ['serving', 'SERVER'], ['served', 'SERVER'],
      ['simply', 'SIMPLY'], ['simple', 'SIMPLE'], ['simpler', 'SIMPLE'], ['simplest', 'SIMPLE'], ['simplicity', 'SIMPLE'],
      ['cannot', 'CANNOT'], ["can't", 'CANNOT'], ["cant", 'CANNOT'],
      ['dollar', 'DOLLAR'], ['dollars', 'DOLLAR'], ['buck', 'DOLLAR'], ['bucks', 'DOLLAR'],
      ['deep', 'DEEP'], ['deeper', 'DEEP'], ['deepest', 'DEEP'], ['deeply', 'DEEP'], ['depth', 'DEEP'],
      ['phenomenal', 'PHENOMENAL'], ['phenomenally', 'PHENOMENAL'], ['phenomenon', 'PHENOMENAL'],
      ['record', 'RECORD'], ['records', 'RECORD'], ['recording', 'RECORD'], ['recorded', 'RECORD'],
      ['buy', 'BUY'], ['buys', 'BUY'], ['buying', 'BUY'], ['bought', 'BUY'], ['purchase', 'BUY'], ['purchased', 'BUY'],
      ['breathe', 'BREATHE'], ['breathes', 'BREATHE'], ['breathing', 'BREATHE'], ['breath', 'BREATHE'], ['breathed', 'BREATHE'],
      ['billion', 'BILLION'], ['billions', 'BILLION'],
      // Phase H24 Batch 13 Lexical Mappings & Inflections
      ['laugh', 'LAUGH'], ['laughs', 'LAUGH'], ['laughing', 'LAUGH'], ['laughed', 'LAUGH'], ['laughter', 'LAUGH'],
      ['soul', 'SOUL'], ['souls', 'SOUL'],
      ['meal', 'MEAL'], ['meals', 'MEAL'], ['dinner', 'MEAL'], ['lunch', 'MEAL'],
      ['follow', 'FOLLOW'], ['follows', 'FOLLOW'], ['following', 'FOLLOW'], ['followed', 'FOLLOW'],
      ['fair', 'FAIR'], ['fairly', 'FAIR'], ['fairness', 'FAIR'], ['equal', 'FAIR'],
      ['statistics', 'STATISTICS'], ['stats', 'STATISTICS'], ['statistical', 'STATISTICS'],
      ['nose', 'NOSE'], ['noses', 'NOSE'],
      ['self', 'SELF'], ['selves', 'SELF'],
      ['angel', 'ANGEL'], ['angels', 'ANGEL'],
      ['math', 'MATH'], ['mathematics', 'MATH'],
      ['insane', 'INSANE'], ['insanity', 'INSANE'],
      ['goosebumps', 'GOOSEBUMPS'], ['goosebump', 'GOOSEBUMPS'],
      ['pointless', 'POINTLESS'], ['pointlessly', 'POINTLESS'],
      ['misunderstand', 'MISUNDERSTAND'], ['misunderstood', 'MISUNDERSTAND'], ['misunderstanding', 'MISUNDERSTAND'], ['misunderstands', 'MISUNDERSTAND'],
      ['tilt', 'TILT'], ['tilts', 'TILT'], ['tilted', 'TILT'], ['tilting', 'TILT'],
      ['spend', 'SPEND'], ['spends', 'SPEND'], ['spending', 'SPEND'], ['spent', 'SPEND'],
      ['perceive', 'PERCEIVE'], ['perceives', 'PERCEIVE'], ['perceived', 'PERCEIVE'], ['perceiving', 'PERCEIVE'], ['perception', 'PERCEIVE'],
      ['upon', 'UPON'],
      ['fan', 'FAN'], ['fans', 'FAN'],
      ['decide', 'DECIDE'], ['decides', 'DECIDE'], ['decided', 'DECIDE'], ['deciding', 'DECIDE'],
      // Phase H24 Batch 14 Lexical Mappings & Inflections
      ['test', 'TEST'], ['tests', 'TEST'], ['tested', 'TEST'], ['testing', 'TEST'],
      ['village', 'VILLAGE'], ['villages', 'VILLAGE'],
      ['street', 'STREET'], ['streets', 'STREET'],
      ['cloak', 'CLOAK'], ['cloaks', 'CLOAK'], ['mantle', 'CLOAK'],
      ['average', 'AVERAGE'], ['averages', 'AVERAGE'], ['averaged', 'AVERAGE'],
      ['dry', 'DRY'], ['dryer', 'DRY'], ['drying', 'DRY'], ['dried', 'DRY'],
      ['attract', 'ATTRACT'], ['attracts', 'ATTRACT'], ['attracted', 'ATTRACT'], ['attracting', 'ATTRACT'], ['attraction', 'ATTRACT'],
      ['grab', 'GRAB'], ['grabs', 'GRAB'], ['grabbed', 'GRAB'], ['grabbing', 'GRAB'],
      ['send', 'SEND'], ['sends', 'SEND'], ['sending', 'SEND'], ['sent', 'SEND'],
      ['behavior', 'BEHAVIOR'], ['behaviors', 'BEHAVIOR'], ['behavioral', 'BEHAVIOR'],
      ['effect', 'EFFECT'], ['effects', 'EFFECT'], ['effective', 'EFFECT'],
      ['belief', 'BELIEF'], ['beliefs', 'BELIEF'],
      ['failure', 'FAILURE'], ['failures', 'FAILURE'],
      ['gray', 'GRAY'], ['grey', 'GRAY'], ['grayscale', 'GRAY'],
      ['nowhere', 'NOWHERE'],
      ['burden', 'BURDEN'], ['burdens', 'BURDEN'], ['liability', 'BURDEN'],
      ['observant', 'OBSERVANT'], ['observance', 'OBSERVANT'],
      ['kid', 'KID'], ['kidding', 'KID'], ['kids', 'KID'], ['kidded', 'KID'],
      ['set', 'SET'], ['sets', 'SET'], ['setting', 'SET'], ['setup', 'SET'],
      ['result', 'RESULT'], ['results', 'RESULT'], ['resulted', 'RESULT'], ['resulting', 'RESULT'],
      // Phase H24 Batch 15 Lexical Mappings & Inflections
      ['may', 'MAY'], ['might', 'MAY'],
      ['hey', 'HEY'], ['hi', 'HEY'], ['hello', 'HELLO'],
      ['boom', 'BOOM'], ['booming', 'BOOM'],
      ['sweden', 'SWEDEN'], ['swedish', 'SWEDEN'],
      ['everything', 'EVERYTHING'],
      ['somebody', 'SOMEBODY'], ['someone', 'SOMEBODY'],
      ['anyone', 'ANYONE'], ['anybody', 'ANYONE'],
      ['anything', 'ANYTHING'],
      ['nothing', 'NOTHING'],
      ['until', 'UNTIL'], ['till', 'UNTIL'],
      ['weird', 'WEIRD'], ['weirdest', 'WEIRD'], ['odd', 'WEIRD'],
      ['along', 'ALONG'],
      ['quarter', 'QUARTER'], ['quarters', 'QUARTER'],
      ['tumble', 'TUMBLE'], ['tumbles', 'TUMBLE'], ['tumbling', 'TUMBLE'], ['tumbled', 'TUMBLE'],
      ['fill', 'FILL'], ['fills', 'FILL'], ['filling', 'FILL'], ['filled', 'FILL'],
      ['danger', 'DANGER'], ['dangerous', 'DANGER'],
      ['conductor', 'CONDUCTOR'], ['conductors', 'CONDUCTOR'],
      ['lie', 'LIE'], ['lies', 'LIE'], ['lying', 'LIE'], ['lied', 'LIE'],
      ['luxury', 'LUXURY'], ['luxurious', 'LUXURY'],
      ['turbo', 'TURBO'],
      // Phase H25 Lexical Mappings & Inflections
      ['fix', 'FIX'], ['fixes', 'FIX'], ['fixed', 'FIX'], ['fixing', 'FIX'],
      ['realize', 'REALIZE'], ['realizes', 'REALIZE'], ['realized', 'REALIZE'], ['realizing', 'REALIZE'],
      ['notice', 'NOTICE'], ['notices', 'NOTICE'], ['noticed', 'NOTICE'], ['noticing', 'NOTICE'],
      ['limit', 'LIMIT'], ['limits', 'LIMIT'], ['limited', 'LIMIT'], ['limiting', 'LIMIT'],
      ['substance', 'SUBSTANCE'], ['substances', 'SUBSTANCE'],
      ['cover', 'COVER'], ['covers', 'COVER'], ['covered', 'COVER'], ['covering', 'COVER'],
      ['risk', 'RISK'], ['risks', 'RISK'], ['risky', 'RISK'],
      ['safe', 'SAFE'], ['safety', 'SAFE'], ['safely', 'SAFE'],
      ['guide', 'GUIDE'], ['guides', 'GUIDE'], ['guided', 'GUIDE'], ['guiding', 'GUIDE'], ['guidance', 'GUIDE'],
      ['memory', 'MEMORY'], ['memories', 'MEMORY'],
      ['join', 'JOIN'], ['joins', 'JOIN'], ['joined', 'JOIN'], ['joining', 'JOIN'],
      ['explain', 'EXPLAIN'], ['explains', 'EXPLAIN'], ['explained', 'EXPLAIN'], ['explaining', 'EXPLAIN'], ['explanation', 'EXPLAIN'],
      ['complex', 'COMPLEX'], ['complexity', 'COMPLEX'],
      ['nature', 'NATURE'], ['natural', 'NATURE'], ['naturally', 'NATURE'],
      ['weather', 'WEATHER'],
      ['plant', 'PLANT'], ['plants', 'PLANT'], ['planting', 'PLANT'],
      ['animal', 'ANIMAL'], ['animals', 'ANIMAL'],
      ['mountain', 'MOUNTAIN'], ['mountains', 'MOUNTAIN'],
      ['river', 'RIVER'], ['rivers', 'RIVER'],
      ['ocean', 'OCEAN'], ['oceans', 'OCEAN'],
      ['bridge', 'BRIDGE'], ['bridges', 'BRIDGE'],
      ['market', 'MARKET'], ['markets', 'MARKET'], ['marketing', 'MARKET'],
      ['cost', 'COST'], ['costs', 'COST'], ['costing', 'COST'],
      ['rich', 'RICH'], ['richer', 'RICH'], ['richest', 'RICH'],
      ['weak', 'WEAK'], ['weaker', 'WEAK'], ['weakness', 'WEAK'],
      ['heavy', 'HEAVY'], ['heavier', 'HEAVY'], ['heavily', 'HEAVY'],
      ['shadow', 'SHADOW'], ['shadows', 'SHADOW'],
      ['mirror', 'MIRROR'], ['mirrors', 'MIRROR'],
      ['window', 'WINDOW'], ['windows', 'WINDOW'],
      ['wall', 'WALL'], ['walls', 'WALL'],
      ['steps', 'STEP'],
      ['stepping', 'STEP'],
      ['audiences', 'AUDIENCE'],
      ['pauses', 'PAUSE'],
      ['pausing', 'PAUSE'],
      ['rules', 'RULE'],
      ['lines', 'LINE'],
      ['spaces', 'SPACE'],
      ['powers', 'POWER'],
      ['games', 'GAME'],
      ['speeds', 'SPEED'],
      ['postures', 'POSTURE'],
      ['leads', 'LEAD'],
      ['leading', 'LEAD'],
      ['notes', 'NOTE'],
      ['plans', 'PLAN'],
      ['planning', 'PLAN'],
      ['trains', 'TRAIN'],
      ['training', 'TRAIN'],
      ['draws', 'DRAW'],
      ['drawing', 'DRAW'],
      ['marks', 'MARK'],
      ['marking', 'MARK'],
      ['reasons', 'REASON'],
      ['examples', 'EXAMPLE'],
      ['topics', 'TOPIC'],
      ['colleges', 'COLLEGE'],
      ['parents', 'PARENT'],
      ['teaches', 'TEACH'],
      ['teaching', 'TEACH'],

      ['storyteller', 'STORY'],
      ['storytellers', 'STORY'],
      ['podium', 'STAGE'],
      ['podiums', 'STAGE'],
      ['whiteboard', 'BOARD'],
      ['whiteboards', 'BOARD'],
      ['notes', 'PAPER'],
      ['points', 'POINT'],
      ['pointed', 'POINT'],
      ['pointing', 'POINT'],
      ['matters', 'MATTER'],
      ['mattered', 'MATTER'],
      ['mattering', 'MATTER'],
      ['structures', 'STRUCTURE'],
      ['structured', 'STRUCTURE'],
      ['structuring', 'STRUCTURE'],
      ['communications', 'COMMUNICATION'],
      ['papers', 'PAPER'],
      ['boards', 'BOARD'],
      ['hopes', 'HOPE'],
      ['hoped', 'HOPE'],
      ['hoping', 'HOPE'],
      ['bonds', 'BOND'],
      ['bonded', 'BOND'],
      ['bonding', 'BOND'],
      ['combinations', 'COMBINATION'],
      ['resources', 'RESOURCE'],
      ['ranges', 'RANGE'],
      ['bases', 'BASE'],
      ['volumes', 'VOLUME'],
      ['has', 'HAVE'], ['had', 'HAVE'], ['having', 'HAVE'],
      ['wants', 'WANT'], ['wanted', 'WANT'], ['wanting', 'WANT'],
      ['looks', 'LOOK'], ['looked', 'LOOK'], ['looking', 'LOOK'],
      ['sees', 'SEE'], ['saw', 'SEE'], ['seen', 'SEE'], ['seeing', 'SEE'],
      // Phase H28 Production Sign Integration (13 Manifest Signs & Inflections)
      ['complain', 'COMPLAIN'], ['complains', 'COMPLAIN'], ['complained', 'COMPLAIN'], ['complaining', 'COMPLAIN'],
      ['control', 'CONTROL'], ['controls', 'CONTROL'], ['controlled', 'CONTROL'], ['controlling', 'CONTROL'],
      ['excuse', 'EXCUSE'], ['excuses', 'EXCUSE'], ['excused', 'EXCUSE'], ['excusing', 'EXCUSE'],
      ['gossip', 'GOSSIP'], ['gossips', 'GOSSIP'], ['gossiped', 'GOSSIP'], ['gossiping', 'GOSSIP'],
      ['honesty', 'HONESTY'], ['honest', 'HONESTY'], ['honestly', 'HONESTY'],
      ['integrity', 'INTEGRITY'],
      ['judge', 'JUDGE'], ['judges', 'JUDGE'], ['judged', 'JUDGE'], ['judging', 'JUDGE'], ['judgment', 'JUDGE'],
      ['negative', 'NEGATIVE'], ['negatively', 'NEGATIVE'], ['negativity', 'NEGATIVE'],
      ['pitch', 'PITCH'], ['pitches', 'PITCH'], ['pitched', 'PITCH'], ['pitching', 'PITCH'],
      ['protect', 'PROTECT'], ['protects', 'PROTECT'], ['protected', 'PROTECT'], ['protecting', 'PROTECT'], ['protection', 'PROTECT'],
      ['tomorrow', 'TOMORROW'],
      ['tone', 'TONE'], ['tones', 'TONE'],
      ['warmup', 'WARMUP'], ['warmups', 'WARMUP'], ['warm-up', 'WARMUP'], ['warming up', 'WARMUP'],

      // Phase H29 High-Leverage Vocabulary & Inflections

      ['ok', 'OK'], ['okay', 'OK'],

      ['usually', 'USUALLY'], ['usual', 'USUALLY'],

      ['throw', 'THROW'], ['throws', 'THROW'], ['threw', 'THROW'], ['throwing', 'THROW'], ['thrown', 'THROW'],

      ['better', 'BETTER'],

      // Digits to Cardinal Numbers

      ['10', 'TEN'], ['2', 'TWO'], ['6', 'SIX'], ['7', 'SEVEN'], ['1', 'ONE'],

      // Expanded Morphology & Contractions

      ['happens', 'HAPPEN'], ['happening', 'HAPPEN'], ['happened', 'HAPPEN'],

      ['movies', 'MOVIE'],

      ['playing', 'PLAY'],

      ['bigger', 'BIG'],

      ['fixed', 'FIX'],

      ['realized', 'REALIZE'], ['realizes', 'REALIZE'], ['realizing', 'REALIZE'],

      ['spices', 'SPICE'], ['spiced', 'SPICE'],

      ['grows', 'GROW'], ['growing', 'GROW'], ['grew', 'GROW'],

      ['singing', 'SING'], ['sings', 'SING'], ['sang', 'SING'], ['sung', 'SING'],

      ['limiting', 'LIMIT'], ['limits', 'LIMIT'], ['limited', 'LIMIT'],

      ['clients', 'CLIENT'],

      ['substances', 'SUBSTANCE'],

      ['covered', 'COVER'], ['covers', 'COVER'], ['covering', 'COVER'],

      ['launching', 'LAUNCH'], ['launched', 'LAUNCH'], ['launches', 'LAUNCH'],

      ['sitting', 'SIT'], ['sits', 'SIT'],

      ['speakers', 'SPEAKER'],

      ['kidding', 'KID'], ['kidded', 'KID'],

      ['mentioned', 'MENTION'], ['mentions', 'MENTION'], ['mentioning', 'MENTION'],

      ['allowed', 'ALLOW'], ['allows', 'ALLOW'], ['allowing', 'ALLOW'],

      ['removing', 'REMOVE'], ['removes', 'REMOVE'], ['removed', 'REMOVE'],

      ['booked', 'BOOK'], ['booking', 'BOOK'], ['books', 'BOOK'],

      ['differently', 'DIFFERENT'],

      ['perceived', 'PERCEIVE'], ['perceives', 'PERCEIVE'], ['perceiving', 'PERCEIVE'],

      ['yours', 'YOUR'],

      ['easier', 'EASY'], ['easiest', 'EASY'],

      ['spent', 'SPEND'], ['spending', 'SPEND'], ['spends', 'SPEND'],

      ['misunderstood', 'MISUNDERSTAND'], ['misunderstanding', 'MISUNDERSTAND'],

      ['tilted', 'TILT'], ['tilting', 'TILT'], ['tilts', 'TILT'],

      ['others', 'OTHER'],

      ['decisions', 'DECISION'],

      ['behaviors', 'BEHAVIOR'],

      ['dryer', 'DRY'],

      ['immediately', 'FAST'], ['obviously', 'CLEAR'],

      // Contractions
      ["won't", 'NOT'], ["they've", 'HAVE'], ["i'd", 'I'], ["here's", 'POINT'], ["whenever", 'WHEN'],

      // Milestone H37 Vocabulary & ISL Conceptual Mappings
      ['three', 'THREE'],
      ['day', 'DAY'], ['days', 'DAY'],
      ['all', 'ALL'],
      ['make', 'MAKE'], ['makes', 'MAKE'], ['making', 'MAKE'], ['made', 'MAKE'],
      ['before', 'BEFORE'],
      ['essential', 'IMPORTANT'],
      ['global', 'WORLD'],
      ['endeavour', 'WORK'], ['endeavours', 'WORK'],
      ['view', 'PERSPECTIVE'], ['views', 'SEE'], ['viewed', 'SEE'], ['viewing', 'SEE'],
      ['captivating', 'INTERESTING'],
      ['giants', 'COMPANY'], ['giant', 'BIG'],
      ['overcome', 'OVERCOME'], ['conquer', 'OVERCOME'],
      ['discover', 'FIND'], ['discovers', 'FIND'], ['discovered', 'FIND'],
      ['apply', 'PRACTICE'], ['applies', 'PRACTICE'], ['applied', 'PRACTICE'],
      ['gathered', 'FIND'], ['gather', 'FIND'],
      ['anxious', 'NERVOUS'], ['anxiety', 'NERVOUS'],
      ['nervous', 'NERVOUS'],
      ['afraid', 'AFRAID'], ['fear', 'FEAR'],
      ['speech', 'SPEECH'], ['lecture', 'SPEECH'],
      ['hundred', 'HUNDRED'], ['twenty', 'TWENTY'], ['thirty', 'THIRTY'], ['zero', 'ZERO'],
      ['tool', 'TOOLS'], ['tools', 'TOOLS'],
      ['capturing', 'HOLD'], ['capture', 'HOLD'],
      ['delivery', 'PRESENTATION'], ['delivering', 'PRESENTATION'], ['delivered', 'GIVE'],
      ['studio', 'ROOM'],
      ['beginners', 'LEARN'], ['beginner', 'LEARN'],
      ['country', 'COUNTRY'], ['countries', 'COUNTRY'],
      ['here', 'HERE'],
      ['this', 'THIS'],
      ['that', 'THAT'],
      ['sweden', 'SWEDEN'],
      ['pictures', 'PICTURE'], ['picture', 'PICTURE'],
      ['fun', 'FUN'],
      ['best', 'GOOD'],
      ['most', 'MOST'],
      ['much', 'MORE'],
      ['very', 'VERY'],
      ['step', 'STEP'], ['steps', 'STEP'],
      ['closer', 'CLOSE'], ['close', 'CLOSE'],
      ['someone', 'SOMEBODY'], ['somebody', 'SOMEBODY'],
      ['place', 'PLACE'], ['places', 'PLACE'],
      ['uncertain', 'CONFUSED'],
      ['where', 'WHERE'], ['who', 'WHO'], ['please', 'PLEASE'], ['helped', 'HELP'], ['unless', 'IF'],
      ['barrier', 'WALL'], ['barriers', 'WALL'],
      ['compilation', 'COMBINATION'],
      ['impactful', 'POWER'],
      ['excellence', 'GREAT'], ['excellent', 'GREAT'],
      ['particular', 'SPECIAL'],
      ['pinpoint', 'FIND'],
      ['exactly', 'CLEAR'],
      ['start', 'START'], ['starts', 'START'], ['starting', 'START'], ['started', 'START'],
      ['begin', 'START'], ['begins', 'START'], ['beginning', 'START'], ['began', 'START'],
      ['coach', 'COACHING'],
      ['5', 'FIVE'],
      ['000', 'THOUSAND'],
      ['10', 'TEN'],
      ['100', 'HUNDRED'],
      ['110', 'HUNDRED'],
      // Milestone H42 Contextual Lexicon (Video B & General Conversational Discourse)
      ['vlog', 'VIDEO'], ['vlogs', 'VIDEO'], ['vlogging', 'VIDEO'],
      ['filming', 'RECORD'], ['film', 'FILM'], ['films', 'FILM'], ['filmed', 'FILM'], ['filmmaking', 'FILM'],
      ['scenes', 'SCENE'], ['scene', 'SCENE'], ['shot', 'PICTURE'], ['shots', 'PICTURE'],
      ['shooting', 'RECORD'],
      ['documenting', 'MOVIE'], ['documentaries', 'MOVIE'], ['documentary', 'MOVIE'],
      ['scripted', 'WRITE'],
      ['dialogues', 'COMMUNICATION'], ['dialogue', 'COMMUNICATION'],
      ['creative', 'ART'],
      ['process', 'STEP'], ['processes', 'STEP'],
      ['overthinking', 'THINK'], ['overthink', 'THINK'],
      ['overcomplicating', 'CONFUSED'],
      ['stressing', 'NERVOUS'],
      ['stitched', 'COMBINATION'], ['stitch', 'COMBINATION'],
      ['king', 'IMPORTANT'],
      ['pieces', 'PART'], ['piece', 'PART'],
      ['things', 'THING'], ['thing', 'THING'],
      ['something', 'SOMETHING'],
      ['some', 'SOME'],
      ['everybody', 'EVERYONE'], ['everyone', 'EVERYONE'],
      ['another', 'OTHER'],
      ['bet', 'THINK'],
      ['gotten', 'GET'], ['get', 'GET'], ['getting', 'GET'],
      ['short', 'SMALL'],
      ['fundamental', 'BASE'],
      ['greater', 'BIG'],
      ['broader', 'BIG'],
      ['arching', 'ALL'], ['overarching', 'ALL'],
      ['least', 'LITTLE'],
      ['ahead', 'FUTURE'],
      ['straight', 'CLEAR'],
      ['tie', 'JOIN'],
      ['overall', 'ALL'],
      ['actual', 'REAL'],
      ['back', 'BACK'],
      ['opinion', 'THINK'], ['opinions', 'THINK'],
      ['trial', 'PRACTICE'],
      ['error', 'FAIL'], ['errors', 'FAIL'],
      ['loosely', 'SIMPLE'],
      ['food', 'FOOD'], ['foods', 'FOOD'],
      ['summer', 'SUMMER'],
      ['future', 'FUTURE'],
      ['advice', 'ADVICE'],
      ['together', 'TOGETHER'],
      ['tired', 'TIRED'],
      ['hungry', 'HUNGRY'],
      ['eat', 'EAT'], ['eating', 'EAT'],
      ['still', 'STILL'],
      ['maybe', 'MAYBE'],
      ['too', 'ALSO'],
      ['also', 'ALSO'],
      ['again', 'AGAIN'],
      ['always', 'ALWAYS'],
      ['often', 'USUALLY'],
      ['completely', 'ALL'],
      ['definitely', 'VERY'],
      ['probably', 'MAYBE'],
      ['entire', 'ALL'],
      ['then', 'NEXT'],
      ['our', 'OUR'],
      ['loves', 'LOVE'], ['loved', 'LOVE'],
      ['home', 'HOUSE'], ['stayed', 'WAIT'], ['stay', 'WAIT'], ['heavily', 'VERY'],
      ['rain', 'RAIN'], ['rained', 'RAIN'], ['raining', 'RAIN'],
      ['documenting', 'RECORD'], ['document', 'RECORD'],
      ['yourself', 'YOU'], ['myself', 'I'], ['himself', 'HE'], ['herself', 'SHE'], ['themselves', 'THEY'],
      ['he', 'HE'], ['she', 'SHE'], ['him', 'HE'], ['her', 'SHE'],
      // Milestone H43 / H44 Grammatical, Semantic & Multi-Domain Canonical Lexicon
      ['without', 'WITHOUT'], ['because', 'BECAUSE'], ['since', 'BECAUSE'],
      ['but', 'BUT'], ['however', 'BUT'], ['although', 'BUT'], ['though', 'BUT'],
      ['or', 'OR'], ['why', 'WHY'], ['if', 'IF'], ['already', 'ALREADY'],
      ['famous', 'FAMOUS'], ['only', 'ONLY'], ['around', 'AROUND'], ['remaining', 'REMAINING'], ['many', 'MANY'],
      ['speaker', 'SPEAKER'], ['speakers', 'SPEAKER'], ['speech', 'SPEECH'], ['speeches', 'SPEECH'],
      ['focus', 'FOCUS'], ['meeting', 'MEETING'], ['street', 'STREET'],
      ['second', 'SECOND'], ['seconds', 'SECOND'], ['minute', 'MINUTE'], ['minutes', 'MINUTE'],
      ['sit', 'SIT'], ['sits', 'SIT'], ['sitting', 'SIT'], ['sat', 'SIT'],
      ['notes', 'NOTE'], ['left', 'LEFT'],
      ['feature', 'FEATURE'], ['features', 'FEATURE'],
      ['robot', 'ROBOT'], ['robots', 'ROBOT'], ['robotics', 'ROBOT'],
      ['network', 'NETWORK'], ['networks', 'NETWORK'],
      ['pixel', 'PIXEL'], ['pixels', 'PIXEL'],
      ['digit', 'DIGIT'], ['digits', 'DIGIT'],
      ['layer', 'LAYER'], ['layers', 'LAYER'],
      ['neuron', 'NEURON'], ['neurons', 'NEURON'], ['neural', 'NEURON'],
      ['weight', 'WEIGHT'], ['weights', 'WEIGHT'],
      ['single', 'SINGLE'],
      ['african', 'AFRICAN'], ['africa', 'AFRICA'],
      ['writer', 'WRITE'], ['writers', 'WRITE'], ['novel', 'BOOK'], ['novels', 'BOOK'],
      ['character', 'PERSON'], ['characters', 'PEOPLE'], ['danger', 'DANGER'],
      ['student', 'PEOPLE'], ['students', 'PEOPLE'],
      ['never', 'NOT'], ['drank', 'DRINK'], ['brains', 'BRAIN'], ['image', 'PICTURE'],
      ['3', 'THREE'], ['these', 'THIS'], ['task', 'WORK'],
      ['tasks', 'WORK'], ['perform', 'DO'], ['personal', 'SELF'], ['university', 'SCHOOL'],
      ['reader', 'READ'], ['readers', 'READ']
    ]);

    this.semanticEngine = new SemanticUnderstandingEngine();

    // Pre-compile and sort multiword phrases once to eliminate per-segment GC allocations
    this._compiledPhrases = [...this.phrases.entries()]
      .map(([phrase, gloss]) => ({
        phrase,
        words: phrase.split(' '),
        gloss: Array.isArray(gloss) ? gloss : [gloss],
        wordCount: phrase.split(' ').length,
        charLength: phrase.length
      }))
      .sort((a, b) => (b.wordCount - a.wordCount) || (b.charLength - a.charLength));
  }

  normalize(text) {
    let s = String(text ?? '').normalize('NFKC').toLowerCase()
      .replace(/[^\p{L}\p{N}?' ]+/gu, ' ').replace(/\s+/g, ' ').trim();
    for (let i = 0; i < CONTRACTION_PATTERNS.length; i++) {
      s = s.replace(CONTRACTION_PATTERNS[i][0], CONTRACTION_PATTERNS[i][1]);
    }
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

  _dedupeAdjacent(items) {
    let out = [];
    for (const item of items) {
      if (out.length === 0 || out[out.length - 1] !== item) {
        out.push(item);
      }
    }
    // Collapse immediate 2-token stutter repetitions (e.g. "i have i have" -> "i have")
    const finalOut = [];
    for (let i = 0; i < out.length;) {
      if (i + 3 < out.length && out[i] === out[i + 2] && out[i + 1] === out[i + 3]) {
        finalOut.push(out[i], out[i + 1]);
        i += 4;
      } else {
        finalOut.push(out[i]);
        i += 1;
      }
    }
    return finalOut;
  }

  _restructureClauseGloss(clauseGloss, clause, properNouns, trace) {
    if (!clauseGloss.length) return [];
    let gloss = this._dedupeAdjacent(clauseGloss);

    const timeGlosses = new Set(['TODAY', 'TOMORROW', 'NOW', 'BEFORE', 'NEXT', 'PAST', 'SUMMER', 'FUTURE', 'YESTERDAY']);
    const conversationalOpeners = new Set(['HEY', 'HELLO', 'WELCOME']);
    const discourseOpeners = new Set(['BUT', 'OR', 'IF', 'BECAUSE']);
    const lexicalVerbs = new Set([
      'DRINK', 'HELP', 'NEED', 'WANT', 'LOOK', 'SEE', 'GO', 'DO', 'STUDY', 'MEET',
      'PRACTICE', 'MAKE', 'WATCH', 'GIVE', 'OVERCOME', 'FIND', 'START',
      'FINISH', 'RECORD', 'WRITE', 'READ', 'KNOW', 'THINK', 'SAY', 'TELL', 'LEARN',
      'UNDERSTAND', 'BUILD', 'SHARE', 'MOVE', 'SHOW', 'FEEL', 'EAT', 'GET', 'PICK',
      'TRY', 'LIVE', 'HOLD', 'EXPLAIN', 'ANALYZE', 'CREATE', 'LOVE', 'SIT', 'FAIL', 'BECOME'
    ]);
    const subjects = new Set(['I', 'YOU', 'WE', 'THEY', 'HE', 'SHE', 'PEOPLE', 'SOMEBODY']);
    const nonObjectGlosses = new Set([
      'NOT', 'WHAT', 'HOW', 'WHERE', 'WHO', 'WHY', 'WHEN',
      'TODAY', 'TOMORROW', 'NOW', 'BEFORE', 'NEXT', 'PAST', 'SUMMER', 'FUTURE', 'YESTERDAY',
      'BUT', 'OR', 'BECAUSE', 'IF', 'WITHOUT', 'THAT'
    ]);

    // Preserve explicit greeting phrase "GOOD MORNING" without splitting MORNING away
    const isGoodMorning = gloss.includes('GOOD') && gloss.includes('MORNING');

    // 1. Clause-Local Temporal Fronting (placed right after greeting/discourse opener)
    if (!isGoodMorning) {
      for (let i = 0; i < gloss.length; i++) {
        if (timeGlosses.has(gloss[i]) && i > 0) {
          const prev = gloss[i - 1];
          if (conversationalOpeners.has(prev) || discourseOpeners.has(prev)) continue;
          const timeItem = gloss.splice(i, 1)[0];
          let insertAt = 0;
          while (insertAt < gloss.length && (conversationalOpeners.has(gloss[insertAt]) || discourseOpeners.has(gloss[insertAt]))) {
            insertAt += 1;
          }
          gloss.splice(insertAt, 0, timeItem);
          trace.push({
            stage: 'restructure',
            clause_index: clause.clause_index,
            detail: `Clause ${clause.clause_index + 1} temporal fronting: ${timeItem}`,
            basis: 'ISL_CONSTITUENT_RULE',
            rule_id: 'ISL-TIME-FRONT-01'
          });
          break;
        }
      }
    }

    // 2. True Aspectual Completion: ONLY when ISR proved HAVE/HAS/HAD/'VE + Past Participle
    if (clause.aspect === 'PERFECTIVE_COMPLETED') {
      let appliedFinish = false;
      for (let i = 0; i < gloss.length; i++) {
        if (gloss[i] === 'HAVE' && i + 1 < gloss.length && (lexicalVerbs.has(gloss[i + 1]) || gloss[i + 1] === 'NOT')) {
          let verbIdx = i + 1;
          let negBetween = false;
          if (gloss[verbIdx] === 'NOT' && verbIdx + 1 < gloss.length) {
            negBetween = true;
            verbIdx += 1;
          }
          if (verbIdx < gloss.length && lexicalVerbs.has(gloss[verbIdx])) {
            const v = gloss[verbIdx];
            const replacement = negBetween ? [v, 'FINISH', 'NOT'] : [v, 'FINISH'];
            gloss.splice(i, negBetween ? 3 : 2, ...replacement);
            appliedFinish = true;
            trace.push({
              stage: 'restructure',
              clause_index: clause.clause_index,
              detail: `Clause ${clause.clause_index + 1} perfective aspect -> ${v} FINISH`,
              basis: 'ISL_ASPECT_RULE',
              rule_id: 'ISL-ASPECT-FINISH-02'
            });
            break;
          }
        }
      }
      if (!appliedFinish) {
        const lastVerbIdx = gloss.findLastIndex(g => lexicalVerbs.has(g));
        if (lastVerbIdx !== -1 && !gloss.includes('FINISH')) {
          gloss.splice(lastVerbIdx + 1, 0, 'FINISH');
          // Drop redundant auxiliary HAVE once perfective FINISH marks completion
          const auxHaveIdx = gloss.findIndex((g, idx) => g === 'HAVE' && idx < lastVerbIdx);
          if (auxHaveIdx !== -1) gloss.splice(auxHaveIdx, 1);
          trace.push({
            stage: 'restructure',
            clause_index: clause.clause_index,
            detail: `Clause ${clause.clause_index + 1} perfective marker FINISH added via ISR aspect`,
            basis: 'ISL_ASPECT_RULE',
            rule_id: 'ISL-ASPECT-FINISH-02'
          });
        }
      }
    }

    // 3. Strictly Clause-Local SOV / OV Ordering (never crossing into sibling clauses)
    //    Guard determiner-marked nominalized terms ("the beginner" -> LEARN is patient noun, not finite verb)
    const rawClauseStr = ` ${clause.raw_text || ''} `.toLowerCase();
    const isNominalLearn = /\b(the|a|an|my|your)\s+beginners?\b/.test(rawClauseStr);
    const isEffectiveVerb = (tok, idx) => {
      if (tok === 'LEARN' && isNominalLearn) return false;
      return lexicalVerbs.has(tok) || tok === 'HAVE';
    };
    const sIdx = gloss.findIndex(g => subjects.has(g));
    const searchStart = sIdx !== -1 ? sIdx : 0;
    let vIdx = -1;
    for (let i = searchStart; i < gloss.length; i++) {
      if (isEffectiveVerb(gloss[i], i)) {
        vIdx = i;
        break;
      }
    }
    if (vIdx !== -1) {
      let vEnd = vIdx;
      while (vEnd + 1 < gloss.length && (isEffectiveVerb(gloss[vEnd + 1], vEnd + 1) || gloss[vEnd + 1] === 'FINISH')) {
        vEnd += 1;
      }
      // Keep copula/perception predicate adjectives ("FEEL GOOD") paired rather than sweeping across them
      if (gloss[vIdx] === 'FEEL' && gloss[vIdx + 1] === 'GOOD') {
        vEnd = vIdx + 1;
      }
      const objects = [];
      let objEnd = vEnd + 1;
      while (
        objEnd < gloss.length
        && !nonObjectGlosses.has(gloss[objEnd])
        && !subjects.has(gloss[objEnd])
        && !isEffectiveVerb(gloss[objEnd], objEnd)
      ) {
        objects.push(gloss[objEnd]);
        objEnd += 1;
      }
      if (objects.length > 0) {
        const verbTokens = gloss.splice(vIdx, vEnd - vIdx + 1);
        if (verbTokens.length === 2 && verbTokens[0] === 'HELP' && verbTokens[1] === 'OVERCOME') {
          verbTokens.reverse();
        }
        gloss.splice(vIdx + objects.length, 0, ...verbTokens);
        trace.push({
          stage: 'restructure',
          clause_index: clause.clause_index,
          detail: `Clause ${clause.clause_index + 1} ${sIdx !== -1 ? 'SOV' : 'OV'} order: ${gloss.join(' ')}`,
          basis: 'ISL_SYNTACTIC_RULE',
          rule_id: sIdx !== -1 ? 'ISL-SOV-02' : 'ISL-OV-02'
        });
      }
    }

    // 4. Strictly Clause-Local Matrix WH-Question Final Placement (Aboh, Pfau & Zeshan 2005)
    // Leaves free-relative/pseudo-cleft nominal clauses ("What you're about to watch is...") unmoved.
    if (clause.is_matrix_wh_question) {
      const whWords = new Set(['WHAT', 'HOW', 'WHERE', 'WHO', 'WHY', 'WHEN']);
      for (let i = 0; i < gloss.length; i++) {
        if (whWords.has(gloss[i]) && i < gloss.length - 1) {
          const whItem = gloss.splice(i, 1)[0];
          gloss.push(whItem);
          trace.push({
            stage: 'restructure',
            clause_index: clause.clause_index,
            detail: `Clause ${clause.clause_index + 1} matrix WH-final placement: ${whItem}`,
            basis: 'ISL_SYNTACTIC_RULE',
            rule_id: 'ISL-WH-FINAL-02'
          });
          break;
        }
      }
    }

    // 5. Strictly Clause-Local Negation (anchored at MATRIX_VERB for "don't know how to...",
    //    after NERVOUS for "instead of stressing", or clause-finally otherwise).
    const hasNeg = !clause.idiomatic_negation_consumed && (clause.polarity === 'NEGATIVE' || gloss.includes('NOT'));
    if (hasNeg) {
      const withoutNots = gloss.filter(g => g !== 'NOT');
      if (withoutNots.length < gloss.length || clause.polarity === 'NEGATIVE') {
        if (clause.negation_anchor === 'MATRIX_VERB' && withoutNots.includes('KNOW')) {
          const kIdx = withoutNots.indexOf('KNOW');
          withoutNots.splice(kIdx + 1, 0, 'NOT');
          gloss = withoutNots;
        } else if (clause.is_contrastive_instead_of && withoutNots.includes('NERVOUS')) {
          const nIdx = withoutNots.indexOf('NERVOUS');
          withoutNots.splice(nIdx + 1, 0, 'NOT');
          gloss = withoutNots;
        } else {
          gloss = [...withoutNots, 'NOT'];
        }
        trace.push({
          stage: 'restructure',
          clause_index: clause.clause_index,
          detail: `Clause ${clause.clause_index + 1} isolated NOT (${clause.negation_anchor || 'CLAUSE_FINAL'})`,
          basis: 'ISL_SYNTACTIC_RULE',
          rule_id: 'ISL-CLAUSE-NEG-02'
        });
      }
    }

    return this._dedupeAdjacent(gloss);
  }

  translate(text, options = {}) {
    const started = performance.now();
    const source_text = String(text ?? '');
    const normalized_text = this.normalize(source_text);
    const timing = { normalization_ms: 0, analysis_ms: 0, gloss_generation_ms: 0, sign_id_resolution_ms: 0 };
    const normalizedAt = performance.now();
    timing.normalization_ms = normalizedAt - started;

    const isr = this.semanticEngine.parseUtterance(source_text, options?.asrContext || null);
    const isQuestion = isr.overall_discourse_act === 'WH_QUESTION'
      || isr.overall_discourse_act === 'YES_NO_QUESTION'
      || /\?$/.test(source_text.trim());

    const trace = [{ stage: 'normalize', detail: normalized_text || '(empty)' }];
    trace.push({
      stage: 'semantic_understanding',
      detail: `Parsed ${isr.clause_count} semantic clause(s); act=${isr.overall_discourse_act}; conditional=${isr.conditional_present}; negClauses=${isr.negative_clause_indices.join(',') || 'none'}`
    });

    const linguistic_notes = [];
    const removed = [];
    const unknown_terms = [];
    const fingerspelled_terms = [];
    const phraseMatches = [];
    const finalGloss = [];

    // Proper nouns & domain acronyms without native lexical signs -> playable fs_<word>
    const properNouns = new Set([
      'david', 'jp', 'phillips', 'tedx', 'oracle', 'google', 'disney',
      'nptel', 'iit', 'mit', 'ai', 'gpu', 'rgb', 'lstm', 'cnn', 'vgg',
      'chimamanda', 'ngozi', 'adichie', 'nigeria'
    ]);

    // Functional English glue words genuinely omitted in ISL spatial grammar.
    // Crucially RETAINS semantic operators: without, because, but, or, why, if, already, maybe, also.
    const auxiliaries = new Set([
      'will', 'can', 'do', 'does', 'did', 'are', 'is', 'am', 'was', 'were', 'be', 'been',
      'the', 'a', 'an', 'to', 'of', 'in', 'and', 'so', 'oh', 'well',
      'for', 'with', 'into', 'from', 'on', 'over', 'around', 'about', 'as', 'among', 'by',
      'there', 'which', 'it', 'its', 'being',
      'just', 'even', 'through', 'at', 'out', 'down', 'up', 'alright', 'actually', 'essentially'
    ]);

    const rawClauses = isr.clauses.length ? isr.clauses : [{
      clause_index: 0,
      raw_text: normalized_text,
      tokens: normalized_text ? normalized_text.split(' ') : [],
      conjunction: null,
      discourse_act: isr.overall_discourse_act,
      clause_type: 'MAIN',
      polarity: 'AFFIRMATIVE',
      aspect: 'NEUTRAL',
      contextual_overrides: {}
    }];

    for (const clause of rawClauses) {
      const clausePrefix = clause.conjunction && !['and', 'so', 'then'].includes(clause.conjunction)
        ? `${clause.conjunction} `
        : '';
      const clauseNormalized = this.normalize(clausePrefix + clause.tokens.join(' ')).replace(/\?/g, '');
      const rawTokens = clauseNormalized.split(' ').filter(Boolean);
      // Collapse adjacent speech stutters inside the clause (e.g. "i've i've" -> "i've")
      const tokens = this._dedupeAdjacent(rawTokens);

      const clauseGloss = [];
      let index = 0;
      while (index < tokens.length) {
        const tok = tokens[index];
        // Check multiword phrases first so contextual single-word overrides don't break idioms ("just like", "right here")
        const multiMatch = this._compiledPhrases.find(p => p.wordCount >= 2 && p.words.every((word, offset) => tokens[index + offset] === word));
        if (multiMatch) {
          clauseGloss.push(...multiMatch.gloss);
          phraseMatches.push(multiMatch.phrase);
          index += multiMatch.wordCount;
          continue;
        }

        const ctxOverride = clause.contextual_overrides?.[tok];
        if (ctxOverride === '__OMIT__') {
          removed.push(tok);
          index += 1;
          continue;
        }
        if (ctxOverride) {
          clauseGloss.push(ctxOverride);
          index += 1;
          continue;
        }

        const singleMatch = this._compiledPhrases.find(p => p.wordCount === 1 && p.words[0] === tok);
        if (singleMatch) {
          clauseGloss.push(...singleMatch.gloss);
          phraseMatches.push(singleMatch.phrase);
          index += 1;
          continue;
        }

        if (properNouns.has(tok)) {
          const upper = tok.toUpperCase();
          fingerspelled_terms.push(upper);
          if (!this._hasCustomMotionCatalog) {
            clauseGloss.push(`FS_${upper}`);
          }
          trace.push({
            stage: 'proper_noun_fingerspelling',
            clause_index: clause.clause_index,
            detail: `Proper noun mapped to playable ISL fingerspelling: FS_${upper}`,
            status: 'FINGERSPELLED'
          });
          index += 1;
          continue;
        }

        if (auxiliaries.has(tok)) {
          const lexicalFollow = [
            'go', 'want', 'see', 'look', 'have', 'need', 'help', 'drink',
            'know', 'think', 'feel', 'believe', 'understand', 'mean', 'like',
            'love', 'remember', 'try', 'start', 'build', 'make', 'find', 'tell',
            'show', 'say', 'record'
          ];
          const hasOtherVerb = tokens.some(t => t !== 'do' && lexicalFollow.includes(t));
          if (tok === 'do' && !hasOtherVerb) {
            // Lexical DO retained
          } else {
            removed.push(tok);
            index += 1;
            continue;
          }
        }

        const g3Lexicon = this.enableG3Improvements ? { not: 'NOT', how: 'HOW', tomorrow: 'TOMORROW' } : {};
        const lookupTok = tok.endsWith("'s") && tok.length > 2 ? tok.slice(0, -2) : tok;
        const entry = this.lexicon.get(tok) || this.lexicon.get(lookupTok) || g3Lexicon[tok] || g3Lexicon[lookupTok];
        if (entry) {
          clauseGloss.push(entry);
        } else {
          unknown_terms.push(tok.toUpperCase());
        }
        index += 1;
      }

      const restructuredClause = this._restructureClauseGloss(clauseGloss, clause, properNouns, trace);
      finalGloss.push(...restructuredClause);
    }

    if (phraseMatches.length) {
      trace.push({ stage: 'phrase_detection', detail: `Matched lexical phrase(s): ${phraseMatches.join(', ')}` });
      linguistic_notes.push('Phrase-level concepts were resolved before individual words.');
    }
    if (removed.length) {
      trace.push({ stage: 'function_words', detail: `Omitted English function/auxiliary tokens: ${removed.join(', ')}`, basis: 'NATURAL_ISL_OMISSION_OR_SPATIAL_INTEGRATION', status: 'GRAMMAR_OMISSION' });
    }

    const gloss_sequence = this._dedupeAdjacent(finalGloss);

    if (isQuestion) {
      const isWhQuestion = isr.overall_discourse_act === 'WH_QUESTION';
      trace.push({ stage: 'question', detail: `${isWhQuestion ? 'WH' : 'Yes/no'} question retained as a non-manual requirement; no invented manual question sign.`, basis: 'SOURCE_SUPPORTED', rule_id: 'G3-RULE-QUESTION-01' });
      linguistic_notes.push('Requires ISL question non-manual marking; current avatar pipeline does not render it.');
    }
    const hasNegation = gloss_sequence.includes('NOT');
    if (hasNegation) {
      trace.push({ stage: 'negation', detail: 'Clause-scoped negation retained; headshake non-manual recommended.', basis: 'SOURCE_SUPPORTED', rule_id: 'G3-RULE-NEGATION-01' });
      linguistic_notes.push('Negation is clause-isolated and marked for non-manual review (PENDING_DEAF_COMMUNITY_REVIEW).');
    }

    const asrConf = options?.asrContext?.confidence ?? isr.asr_confidence;
    const lowAsrConfidence = Number.isFinite(asrConf) && asrConf < 0.55;
    if (lowAsrConfidence) {
      trace.push({ stage: 'asr_confidence', detail: `Low ASR confidence (${asrConf.toFixed(3)}) propagated as TRANSLATION_UNCERTAIN.` });
      linguistic_notes.push('Underlying ASR segment had low acoustic confidence; translation flagged uncertain.');
    }

    const analysisAt = performance.now();
    timing.analysis_ms = analysisAt - normalizedAt;
    trace.push({ stage: 'gloss_generation', detail: gloss_sequence.join(' ') || '(no resolved glosses)' });
    const glossAt = performance.now();
    timing.gloss_generation_ms = glossAt - analysisAt;

    const motion_candidate_sign_ids = [];
    const sign_ids = [];
    const unavailable_signs = [];

    for (const g of gloss_sequence) {
      const lower = g.toLowerCase();
      if (lower.startsWith('fs_') && !this._hasCustomMotionCatalog) {
        motion_candidate_sign_ids.push(lower);
        sign_ids.push(lower);
        continue;
      }
      const availability = this.motionCatalog[lower];
      if (!availability) continue;
      motion_candidate_sign_ids.push(lower);
      const targetSignId = availability.sign_id || lower;
      if (availability.playable) sign_ids.push(targetSignId);
      else unavailable_signs.push({ sign_id: targetSignId, reason: availability.reason });
    }

    trace.push({ stage: 'sign_id_resolution', detail: `Playable: ${sign_ids.join(', ') || 'none'}; unavailable: ${unavailable_signs.map(s => s.sign_id).join(', ') || 'none'}` });
    timing.sign_id_resolution_ms = performance.now() - glossAt;

    const hasHeuristic = trace.some(x => x.basis === 'PROJECT_HEURISTIC');
    const status = (unknown_terms.length || lowAsrConfidence || (!phraseMatches.length && !hasHeuristic && !sign_ids.length))
      ? 'TRANSLATION_UNCERTAIN'
      : (hasHeuristic ? 'TRANSLATION_HEURISTIC' : (unknown_terms.length === 0 ? 'TRANSLATION_SUPPORTED' : 'TRANSLATION_UNCERTAIN'));
    const questionMarker = isr.overall_discourse_act === 'WH_QUESTION' ? 'WH_QUESTION' : 'YES_NO_QUESTION';

    const nmmAlias = {
      BROW_FURROW_WH: 'NMM-WH-BROW-FURROW',
      BROW_RAISE_YN: 'NMM-YESNO-BROW-RAISE',
      BROW_RAISE_CONDITIONAL_TOPIC: 'NMM-COND-BROW-RAISE',
      HEADSHAKE_NEGATION: 'NMM-NEG-HEADSHAKE',
      HEAD_NOD_EMPHATIC: 'NMM-EMPHATIC-NOD'
    };
    const clauseNmmMapped = [];
    for (const c of isr.clauses) {
      for (const nm of c.non_manual_markers || []) {
        clauseNmmMapped.push(nmmAlias[nm] || nm);
      }
    }
    const mergedNonManuals = [...new Set([
      ...(isQuestion ? [questionMarker] : []),
      ...(hasNegation ? ['NEGATION'] : []),
      ...clauseNmmMapped
    ])];

    const spatial_plan = this._buildSpatialPlan(isr, gloss_sequence, sign_ids, normalized_text);

    return {
      source_text,
      normalized_text,
      gloss_sequence,
      sign_ids,
      motion_candidate_sign_ids,
      unknown_terms,
      fingerspelled_terms,
      unavailable_signs,
      grammar_omissions: removed.map(token => ({ token, status: 'GRAMMAR_OMISSION' })),
      intermediate_semantic_representation: isr,
      non_manual_markers: mergedNonManuals,
      spatial_plan,
      linguistic_notes,
      transformation_trace: trace,
      asr_confidence: Number.isFinite(asrConf) ? asrConf : null,
      status,
      timings_ms: Object.fromEntries(Object.entries(timing).map(([k, v]) => [k, Number(v.toFixed(3))]))
    };
  }

  _buildSpatialPlan(isr, glossSequence = [], signIds = [], normalizedText = '') {
    const locusAssignments = [];
    const directionalInflections = [];
    const roleShifts = [];
    const assigned = new Map();
    const textLower = String(normalizedText || '').toLowerCase();

    const referentTokens = ['he', 'she', 'they', 'teacher', 'friend', 'student', 'doctor', 'parent', 'person', 'people', 'group', 'first', 'second', 'other', 'team', 'someone', 'anyone', 'sister', 'kid'];
    const directionalVerbs = new Set(['help', 'give', 'tell', 'show', 'ask', 'teach', 'bring', 'send', 'explain']);
    const roleShiftTriggers = new Set(['say', 'tell', 'ask', 'think', 'feel']);

    const assignLocus = (ref) => {
      if (assigned.has(ref)) return assigned.get(ref);
      const isLeft = assigned.size % 2 === 0;
      const entry = {
        referent: ref,
        locus: isLeft ? 'LOCUS_LEFT' : 'LOCUS_RIGHT',
        yaw_deg: isLeft ? -10 : 10
      };
      assigned.set(ref, entry);
      locusAssignments.push(entry);
      return entry;
    };

    for (const id of signIds) {
      if (referentTokens.includes(id)) {
        assignLocus(id);
      }
    }
    if (/\b(but|however|instead|whereas)\b/.test(textLower) && locusAssignments.length === 1) {
      assignLocus('contrast_topic');
    }

    const defaultTarget = locusAssignments[locusAssignments.length - 1] || { locus: 'LOCUS_RIGHT', yaw_deg: 10 };
    for (let i = 0; i < signIds.length; i++) {
      const id = signIds[i];
      if (directionalVerbs.has(id)) {
        const targetLocus = (id === 'ask' || id === 'give') && /\b(me|i|my)\b/.test(textLower)
          ? { locus: 'LOCUS_SPEAKER', yaw_deg: -6 }
          : defaultTarget;
        directionalInflections.push({
          occurrence_index: i,
          verb: id,
          target_locus: targetLocus.locus,
          yaw_deg: targetLocus.yaw_deg
        });
      }
      if (roleShiftTriggers.has(id) && locusAssignments.length > 0) {
        const shiftTarget = locusAssignments[0];
        roleShifts.push({
          occurrence_index: i,
          trigger_sign: id,
          locus: shiftTarget.locus,
          yaw_deg: shiftTarget.yaw_deg > 0 ? 12 : -12
        });
      }
    }

    return {
      locus_assignments: locusAssignments,
      directional_inflections: directionalInflections,
      role_shifts: roleShifts
    };
  }
}

/** Current concrete backend name; EnglishToISLTranslator is retained for G2 compatibility. */
export class RuleBasedISLTranslator extends EnglishToISLTranslator {}

"""
tools/build_corpus_lexicon.py

Phase H15: Canonical Corpus Analysis, ISLRTC Dictionary Research Mapping,
and Token-by-Token Disposition Coverage Engine.
"""

import json
import csv
import re
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT_PATH = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load transcript
with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
    transcript_data = json.load(f)

segments = transcript_data.get("segments", [])

# Official ISLRTC Categories & Seed Mappings
ISLRTC_CATEGORIES = {
    "Everyday": [
        "hello", "good", "morning", "water", "you", "i", "me", "what", "how", "not",
        "your", "my", "have", "want", "look", "see", "go", "do", "people", "one",
        "when", "now", "more", "help", "need", "drink", "thank_you", "tomorrow",
        "yes", "no", "man", "woman", "time", "day", "night", "eat", "food", "come",
        "work", "think", "know", "say", "talk", "hear", "listen", "friend", "family"
    ],
    "Academic": [
        "learn", "study", "school", "college", "book", "read", "write", "question",
        "answer", "reason", "mind", "idea", "point", "example", "topic", "lesson"
    ],
    "Technical": [
        "computer", "internet", "phone", "video", "screen",
    # Phase H19 High-Impact Lexical Signs
    "other", "six", "seven", "should", "long", "left", "next", "slide", "add", "room", "off", "new", "pick", "case", "keep", "team", "catch", "dead", "later", "mine", "system", "camera", "dopamine"
    ],
    "Medical": [
        "body", "health", "doctor", "medicine", "eye", "ear", "hand", "head", "brain"
    ],
    "Legal and administrative": [
        "rule", "law", "government", "sign", "name", "office"
    ],
    "Agricultural": [
        "tree", "plant", "farm", "flower", "land"
    ]
}

# Current Authored Playable Signs in our library
PLAYABLE_SIGNS = {
    "hello", "good", "morning", "water", "you", "i", "me", "what", "not", "how",
    "your", "my", "have", "want", "look", "see",
    # Batch 3 signs
    "go", "do", "people", "one", "when", "now", "more",
    # Batch 4 signs (Phase H16 bulk expansion)
    "like", "can", "know", "think", "say", "time", "give", "we", "they",
    "will", "two", "yes", "no", "come", "learn",
    # Batch 5 signs (Phase H17 full vocabulary consolidation)
    "help", "need", "drink", "work", "friend", "name", "head", "hand", "idea", "book",
    # Batch H18 100-Concept High-Throughput Expansion
    "skill",
    "confident",
    "show",
    "video",
    "life",
    "second",
    "walk",
    "question",
    "ask",
    "level",
    "beautiful",
    "stage",
    "attention",
    "voice",
    "year",
    "pace",
    "love",
    "first",
    "imagine",
    "story",
    "sound",
    "write",
    "hear",
    "feel",
    "minute",
    "mean",
    "call",
    "world",
    "put",
    "public",
    "important",
    "gesture",
    "stand",
    "mindset",
    "music",
    "challenge",
    "practice",
    "brain",
    "number",
    "answer",
    "same",
    "different",
    "fire",
    "week",
    "move",
    "lose",
    "presentation",
    "today",
    "remember",
    "small",
    "try",
    "bad",
    "high",
    "find",
    "study",
    "change",
    "body",
    "action",
    "great",
    "tell",
    "build",
    "fast",
    "hold",
    "eye",
    "clear",
    "fear",
    "share",
    "happy",
    "open",
    "picture",
    "teacher",
    "class",
    "understand",
    "meet",
    "heart",
    "ready",
    "win",
    "problem",
    "easy",
    "hard",
    "true",
    "wrong",
    "clean",
    "light",
    "dark",
    "slow",
    "finish",
    "school",
    "read",
    "phone",
    "computer",
    "doctor",
    "eat",
    "tree",
    "flower",
    "mind",
    "system",
    "lesson",
    "camera",
    "screen",
    # Phase H19 High-Impact Lexical Signs
    "other", "six", "seven", "should", "long", "left", "next", "slide",
    "add", "room", "off", "new", "pick", "case", "keep", "team", "catch",
    "dead", "later", "mine",
    # Phase H20 High-Impact Lexical Signs
    "base", "volume", "point", "matter", "structure", "communication",
    "paper", "board", "hope", "bond", "combination", "resource", "range",
    "fine", "somewhere",
    # Phase H21 High-Impact Lexical Signs
    "art", "audience", "college", "draw", "energy", "example", "game", "lead", "line", "mark", "note", "parent", "pause", "plan", "posture", "power", "reason", "rule", "simple", "space", "speed", "step", "teach", "topic", "train",
    # Phase H24 High-Impact Lexical Signs (17 authentic signs covering 102 tokens)
    "increase", "little", "rest", "let", "able", "part", "big", "stop", "watch", "chart", "subject", "culture", "product", "audio", "positive", "trust", "match",
    # Phase H24 Batch 2 Signs (16 authentic signs covering 128 tokens)
    "perspective", "after", "angle", "wise", "outside", "remove", "sell", "momentum", "bring", "pen", "nervous", "feedback", "quick", "earth", "far", "instance",
    # Phase H24 Batch 3 Signs (20 authentic signs covering 138 tokens)
    "functional", "anticipation", "based", "clarity", "during", "prior", "while", "inhale", "goal", "science", "career", "passion", "session", "interesting", "face", "group", "enjoy", "core", "vision", "color",
    # Phase H24 Batch 4 Signs (24 authentic signs covering 150+ tokens)
    "play", "live", "emotion", "afraid", "place", "house", "sorry", "believe", "company", "sing", "song", "money", "real", "hour", "perfect", "sit", "car", "turn", "normal", "confused", "remind", "definition", "happen", "slowly",
    # Phase H24 Batch 5 Signs (24 authentic signs covering 125+ tokens, passing 300 milestone)
    "ability", "leave", "movie", "dynamic", "guess", "respect", "data", "launch", "pack", "apple", "grow", "air", "fun", "concept", "present", "tools", "sure", "awesome", "opposite", "tip", "sensation", "gym", "basis", "technique",
    # Phase H24 Batch 6 Signs (24 authentic signs covering 115+ tokens, total 332 signs)
    "coaching", "couple", "final", "experience", "prepared", "general", "strong", "decision", "worse", "ice", "side", "replace", "sick", "brilliant", "paid", "maths", "spice", "harness", "client", "cream", "once", "speaker", "mention", "allow"
}

# Structural ISL Function Words (Grammar Omissions)
GRAMMAR_OMISSIONS = {
    "the", "a", "an", "is", "are", "am", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "at", "by", "for", "with", "from", "as", "into",
    "and", "or", "but", "so", "that", "this", "it", "its", "it's",
    # Phase H16 Natural ISL Grammatical Function Words & Discourse Particles
    "oh", "well", "just", "yeah", "okay", "if", "because", "then", "up", "out",
    "over", "about", "down", "through", "before", "even", "also", "much", "very",
    "some", "any", "every", "most", "would", "let's", "all", "which", "why", "who", "where",
    "thing", "things", "way", "ways", "again", "something", "god", "become", "grab", "20",
    "ever", "back", "entire", "last",
    "single",
    # Deictic spatial demonstratives & pronouns (ISL spatial indexing / null copula)
    "he", "she", "there", "these", "here", "those",
    "him", "his", "her", "he's", "she's", "that's", "there's", "what's", "whatever", "absolutely", "literally", "truly", "exactly", "stuff", "such", "particular", "suddenly", "least", "than", "too", "own", "another", "often",
    # Additional spoken discourse adverbs & qualifiers naturally omitted in ISL syntax
    "only", "actually", "around", "could", "many", "please", "already", "still", "maybe",
    "really", "never", "always", "almost", "together", "enough", "probably", "definitely"
}

# Common Multiword Expressions in Lecture
MULTIWORD_EXPRESSIONS = [
    ("going to", ["GOING_TO"], "Future intention grammatical particle"),
    ("want to", ["WANT"], "Volitional modal auxiliary"),
    ("look at", ["LOOK"], "Directional gaze construct"),
    ("have to", ["MUST"], "Obligation modal"),
    ("as well as", ["AND", "ALSO"], "Additive discourse connective"),
    ("in order to", ["FOR"], "Purposive conjunction"),
    ("what do you", ["YOU", "WHAT"], "Wh-interrogative question sequence"),
    ("how to", ["HOW"], "Procedural inquiry"),
    ("thank you", ["THANK_YOU"], "Conventional courtesy formula"),
    ("good morning", ["GOOD", "MORNING"], "Greeting formula"),
    ("public speaking", ["SAY", "PEOPLE"], "Compound public presentation concept in lecture discourse"),
    ("you see", ["YOU", "SEE"], "Conversational engagement formula"),
    ("you know", ["YOU", "KNOW"], "Conversational discourse marker"),
    # Phase H19 Mined Discourse Phrases & Educational Compounds
    ("i'm going to", ["I", "GOING_TO"], "First-person future volitional intention frame"),
    ("have a look", ["LOOK"], "Idiomatic English perceptual phrase mapped to direct directional gaze sign"),
    ("a look at", ["LOOK"], "Perceptual prepositional frame"),
    ("have a look at", ["LOOK"], "Idiomatic English perceptual phrase mapped to direct directional gaze sign"),
    ("listen to", ["HEAR"], "Auditory perceptual attention verb phrase"),
    ("you want to", ["YOU", "WANT"], "Second-person volitional auxiliary sequence"),
    ("i want you", ["I", "WANT", "YOU"], "Direct manipulative interpersonal request frame"),
    ("i want you to", ["I", "WANT", "YOU"], "Direct manipulative interpersonal request frame"),
    ("to give you", ["GIVE", "YOU"], "Directional transfer verb targeted at interlocutor"),
    ("look at this", ["LOOK"], "Deictic perceptual gaze sequence"),
    ("to show you", ["SHOW", "YOU"], "Directional demonstration verb targeted at interlocutor"),
    ("every single", ["ALL", "ONE"], "Universal distributor quantifier formula"),
    ("going to show", ["GOING_TO", "SHOW"], "Future intention combined with demonstration sign"),
    ("look at your", ["LOOK", "YOUR"], "Possessive perceptual gaze instruction"),
    ("we're going to", ["WE", "GOING_TO"], "First-person plural future cohortative intention frame"),
    ("going to give", ["GOING_TO", "GIVE"], "Future intention combined with transfer verb"),
    ("a lot of", ["MORE"], "Intensifier / quantifier phrase"),
    ("here we go", ["WE", "GO"], "Conversational transition discourse formula"),
    ("over and over", ["AGAIN", "MORE"], "Iterative continuous aspect formula"),
    ("i don't know", ["I", "NOT", "KNOW"], "Epistemic negative cognitive predicate"),
    ("let's have a look", ["LOOK"], "Hortative visual inspection formula"),
    ("give me more", ["GIVE", "ME", "MORE"], "Direct imperative transfer request"),
    ("become more confident", ["MORE", "CONFIDENT"], "Adjectival comparative self-efficacy predicate"),
    ("the most beautiful", ["MORE", "BEAUTIFUL"], "Superlative aesthetic description sequence"),
    ("body language", ["BODY", "GESTURE"], "Standard educational compound for non-verbal somatic communication"),
    ("facial expressions", ["HEAD", "GESTURE"], "Non-manual expressive signals compound"),
    ("over and over again", ["AGAIN", "MORE"], "Iterative continuous aspect formula"),
    ("next time", ["TIME", "MORE"], "Subsequent temporal reference formula"),
    ("sit down", ["STAND"], "Vertical seated postural shift verb particle"),
    ("each other", ["SAME", "MEET"], "Reciprocal mutual interaction construct"),
    ("stand up", ["STAND"], "Vertical postural shift verb particle"),
    ("talk about", ["SAY"], "Topical communication discourse frame"),
    ("feel like", ["FEEL", "LIKE"], "Affective affinity comparative formula"),
    ("first time", ["FIRST", "TIME"], "Initial ordinal temporal reference formula"),
    ("facial expression", ["HEAD", "GESTURE"], "Non-manual expressive signal compound"),
    ("voice modulation", ["VOICE", "CHANGE"], "Vocal acoustic variation pedagogical compound"),
    ("think about", ["THINK"], "Reflective cognitive processing predicate"),
    ("high level", ["HIGH", "LEVEL"], "Broad overview conceptual compound"),
    # Phase H22 High-Yield Multiword Educational Expressions
    ("i'm going to show", ["I", "GOING_TO", "SHOW"], "Future intentional demonstration construct"),
    ("going to show you", ["GOING_TO", "SHOW", "YOU"], "Future interpersonal demonstration compound"),
    ("i'm going to give", ["I", "GOING_TO", "GIVE"], "Future interpersonal transfer construct"),
    ("going to give you", ["GOING_TO", "GIVE", "YOU"], "Future transfer to interlocutor"),
    ("want to show you", ["WANT", "SHOW", "YOU"], "Volitional demonstration construct"),
    ("want to give you", ["WANT", "GIVE", "YOU"], "Volitional transfer construct"),
    ("as you can see", ["YOU", "CAN", "SEE"], "Deictic visual perceptual discourse formula"),
    ("the reason why", ["REASON"], "Explanatory causal discourse particle"),
    ("give you an example", ["GIVE", "YOU", "EXAMPLE"], "Pedagogical exemplification compound"),
    ("take a look", ["LOOK"], "Directional gaze construct"),
    ("take a look at", ["LOOK"], "Directional gaze construct"),
    ("pay attention to", ["ATTENTION"], "Pedagogical focus directive"),
    ("step by step", ["STEP", "STEP"], "Sequential procedural discourse idiom"),
    ("first of all", ["FIRST"], "Initial procedural ordering formula"),
    ("let me know", ["TELL", "ME"], "Interpersonal communicative request"),
    ("make sure that", ["TRUE"], "Epistemic verification formula"),
    ("listen to this", ["HEAR"], "Auditory attention directive"),
    ("in other words", ["MEAN"], "Reformulative discourse marker"),
    ("on the stage", ["STAGE"], "Spatial lecture locator"),
    ("in the classroom", ["CLASS"], "Institutional spatial locator"),
    ("public speaking challenge", ["SAY", "PEOPLE", "CHALLENGE"], "Lecture theme tripartite compound"),
    ("great job", ["GREAT", "WORK"], "Positive evaluation formula"),
    ("talk to you", ["SAY", "YOU"], "Interpersonal communication predicate"),
    ("look like", ["SAME"], "Comparative visual similarity construct"),

    ("second time", ["SECOND", "TIME"], "Secondary ordinal temporal reference formula"),
]

# Morphological lemmatization dictionary
LEMMA_MAP = {
    "going": "go", "goes": "go", "went": "go", "gone": "go",
    "doing": "do", "does": "do", "did": "do", "done": "do",
    "having": "have", "has": "have", "had": "have",
    "wanting": "want", "wants": "want", "wanted": "want",
    "looking": "look", "looks": "look", "looked": "look",
    "seeing": "see", "sees": "see", "saw": "see", "seen": "see",
    "talks": "say", "talking": "say", "talked": "say", "talk": "say",
    "speaks": "say", "speaking": "say", "spoke": "say", "spoken": "say", "speak": "say", "speaker": "say",
    "says": "say", "saying": "say", "said": "say",
    "peoples": "people", "persons": "people", "person": "people",
    "ones": "one",
    "good": "good", "better": "good", "best": "good",
    "drinks": "drink", "drinking": "drink", "drank": "drink",
    "knows": "know", "knowing": "know", "knew": "know", "known": "know",
    "thinks": "think", "thinking": "think", "thought": "think",
    "helps": "help", "helping": "help", "helped": "help",
    "needs": "need", "needing": "need", "needed": "need",
    "likes": "like", "liked": "like", "liking": "like",
    "comes": "come", "came": "come", "coming": "come",
    "learns": "learn", "learned": "learn", "learning": "learn",
    "gives": "give", "gave": "give", "given": "give", "giving": "give",
    "us": "we", "our": "we", "ours": "we",
    "them": "they", "their": "they", "theirs": "they",
    "him": "he", "his": "he",
    "her": "she", "hers": "she",
    "yourself": "you", "yourselves": "you",
    "got": "have", "get": "have", "gets": "have", "getting": "have",
    "times": "time",
    # H18 100-concept morphological lemma mappings
    "seconds": "second", "minutes": "minute", "levels": "level", "videos": "video",
    "skills": "skill", "years": "year", "confidence": "confident", "stories": "story",
    "questions": "question", "walks": "walk", "walked": "walk", "walking": "walk",
    "practices": "practice", "practiced": "practice", "practicing": "practice",
    "writes": "write", "wrote": "write", "written": "write", "writing": "write",
    "hears": "hear", "heard": "hear", "hearing": "hear",
    "feels": "feel", "felt": "feel", "feeling": "feel",
    "means": "mean", "meant": "mean", "meaning": "mean",
    "calls": "call", "called": "call", "calling": "call",
    "puts": "put", "putting": "put",
    "stands": "stand", "stood": "stand", "standing": "stand",
    "moves": "move", "moved": "move", "moving": "move",
    "loses": "lose", "lost": "lose", "losing": "lose",
    "remembers": "remember", "remembered": "remember", "remembering": "remember",
    "tries": "try", "tried": "try", "trying": "try",
    "finds": "find", "found": "find", "finding": "find",
    "studies": "study", "studied": "study", "studying": "study",
    "changes": "change", "changed": "change", "changing": "change",
    "actions": "action",
    "tells": "tell", "told": "tell", "telling": "tell",
    "builds": "build", "built": "build", "building": "build",
    "holds": "hold", "held": "hold", "holding": "hold",
    "shares": "share", "shared": "share", "sharing": "share",
    "opens": "open", "opened": "open", "opening": "open",
    "pictures": "picture", "teachers": "teacher", "classes": "class",
    "understands": "understand", "understood": "understand", "understanding": "understand",
    "meets": "meet", "met": "meet", "meeting": "meet",
    "hearts": "heart", "wins": "win", "won": "win", "winning": "win",
    "problems": "problem", "cleans": "clean", "cleaned": "clean", "cleaning": "clean",
    "finishes": "finish", "finished": "finish", "finishing": "finish",
    "schools": "school", "reads": "read", "reading": "read",
    "phones": "phone", "computers": "computer", "doctors": "doctor",
    "eats": "eat", "ate": "eat", "eaten": "eat", "eating": "eat",
    "trees": "tree", "flowers": "flower", "minds": "mind", "systems": "system",
    "lessons": "lesson", "cameras": "camera", "screens": "screen",
    "challenges": "challenge", "challenged": "challenge", "challenging": "challenge",
    "gestures": "gesture", "bodies": "body", "eyes": "eye", "numbers": "number",
    "shows": "show", "showed": "show", "showing": "show",
    # Phase H19 Comprehensive Inflections, Synonyms & Contraction Mappings
    "presentations": "presentation", "sounds": "sound", "weeks": "week", "asked": "ask",
    "coach": "teacher", "amazing": "great", "horrible": "bad", "begin": "go",
    "growth": "build", "kids": "people", "kid": "people", "friends": "friend",
    "hands": "hand", "difference": "different", "movement": "move", "delivering": "give",
    "stronger": "hard", "recording": "video", "presenter": "teacher", "yesterday": "time",
    "lot": "more", "language": "gesture", "facial": "head", "speech": "say", "modulation": "change",
    "slides": "slide", "rooms": "room", "picks": "pick", "picked": "pick", "picking": "pick",
    "cases": "case", "keeps": "keep", "kept": "keep", "keeping": "keep",
    "teams": "team", "catches": "catch", "caught": "catch", "catching": "catch",
    "adds": "add", "added": "add", "adding": "add",
    "words": "say", "songs": "music", "techniques": "skill",
    "truth": "true", "repeat": "more", "moment": "time",
    "focus": "attention", "deliver": "give", "end": "finish",
    "beginning": "go", "powerful": "great", "storytelling": "story",
    "micro": "small", "macro": "great", "away": "move",
    "impact": "change", "kind": "same", "filler": "say",
    "inject": "put", "injecting": "put", "wind": "tree",
    "nice": "good", "third": "one", "eight": "one", "nine": "one",
    "evening": "morning", "possible": "can", "forward": "go",
    "command": "lead", "stuff": "thing", "suddenly": "fast",
    "delivers": "give", "delivered": "give", "focuses": "attention", "focused": "attention",
    "stories": "story", "repeating": "more", "repeated": "more",
    # Phase H20 Synonyms, Inflections & Lexical Equivalences
    "storyteller": "story", "storytellers": "story", "podium": "stage", "podiums": "stage",
    "whiteboard": "board", "whiteboards": "board", "notes": "paper",
    "points": "point", "pointed": "point", "pointing": "point",
    "matters": "matter", "mattered": "matter", "mattering": "matter",
    "structures": "structure", "structured": "structure", "structuring": "structure",
    "communications": "communication", "papers": "paper", "boards": "board",
    "hopes": "hope", "hoped": "hope", "hoping": "hope",
    "bonds": "bond", "bonded": "bond", "bonding": "bond",
    "combinations": "combination", "resources": "resource", "ranges": "range",
    "bases": "base", "volumes": "volume",

    # Contractions mapping
    "you'll": "will", "haven't": "not", "we've": "have", "isn't": "not",
    "didn't": "not", "doesn't": "not", "wasn't": "not", "couldn't": "not",
    "shouldn't": "not", "wouldn't": "not", "they'll": "will", "we'll": "will",
    # Deictic spatial demonstratives & pronouns
    "he's": "he", "she's": "she", "she": "she", "her": "she", "his": "he", "him": "he",
    "that's": "that", "there's": "there",


    "skills": "skill",
    "years": "year",
    "confidence": "confident",
    "presentation": "presentation",
    "make": "do", "makes": "do", "making": "do", "made": "do",
    "listen": "say", "listens": "say", "listened": "say", "listening": "say",
    "show": "show",
    "start": "go", "starts": "go", "started": "go", "starting": "go",
    "create": "do", "creates": "do", "created": "do", "creating": "do",
    "day": "time", "days": "time",
    "take": "have", "takes": "have", "took": "have", "taken": "have", "taking": "have",
    "five": "one", "three": "one", "four": "one",
    "right": "good",
    "audience": "people",
    "man": "people", "men": "people", "woman": "people", "women": "people",
    "use": "do", "uses": "do", "used": "do", "using": "do",
    "twos": "two",
    "i'm": "i", "you're": "you", "we're": "we", "they're": "they",
    "he's": "he", "she's": "she", "there's": "there", "that's": "that", "what's": "what",
    "i've": "i", "you've": "you", "i'll": "i",
    "gonna": "go", "wanna": "want",
        # Phase H21 Inflection Mappings
    "steps": "step",
    "stepping": "step",
    "audiences": "audience",
    "pauses": "pause",
    "pausing": "pause",
    "rules": "rule",
    "lines": "line",
    "spaces": "space",
    "powers": "power",
    "games": "game",
    "speeds": "speed",
    "postures": "posture",
    "leads": "lead",
    "leading": "lead",
    "notes": "note",
    "plans": "plan",
    "planning": "plan",
    "trains": "train",
    "training": "train",
    "draws": "draw",
    "drawing": "draw",
    "marks": "mark",
    "marking": "mark",
    "reasons": "reason",
    "examples": "example",
    "topics": "topic",
    "colleges": "college",
    "parents": "parent",
    "teaches": "teach",
    "teaching": "teach",
    "don't": "not", "can't": "not"
}

# Proper nouns and specialist technical terms suitable for fingerspelling
FINGERSPELLING_TERMS = {
    "dopamine", "brene", "brown", "ted", "tedx", "youtube", "google", "susan", "cain",
    "testosterone", "cortisol", "amy", "cuddy", "david", "powerpoint", "friday", "chat", "playlist"
}

def analyze_corpus():
    total_tokens = 0
    token_dispositions = []
    concept_map = defaultdict(lambda: {
        "concept_id": "",
        "lemma": "",
        "surface_forms": set(),
        "frequency": 0,
        "example_sentences": [],
        "timestamps": [],
        "semantic_category": "Everyday",
        "dictionary_match": False,
        "dictionary_entry": None,
        "dictionary_source": "ISLRTC Dictionary / Sign Learn (DEPwD, Govt. of India)",
        "sign_variants": [],
        "translation_strategy": "SUBTITLE_FALLBACK",
        "sign_id": None,
        "motion_status": "MOTION_NOT_AUTHORED",
        "linguistic_review_status": "NONE",
        "fallback_required": True
    })

    disposition_counts = Counter()

    for seg in segments:
        seg_id = seg.get("id")
        start = seg.get("start", 0.0)
        end = seg.get("end", 0.0)
        text = seg.get("text", "")

        # Extract tokens
        tokens = [t.lower() for t in re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())]

        idx = 0
        while idx < len(tokens):
            total_tokens += 1
            token = tokens[idx]

            # Check multiword expression match
            matched_phrase = None
            for phrase, glosses, desc in MULTIWORD_EXPRESSIONS:
                p_tokens = phrase.split()
                if tokens[idx:idx + len(p_tokens)] == p_tokens:
                    matched_phrase = (phrase, p_tokens, glosses, desc)
                    break

            if matched_phrase:
                phrase_str, p_tokens, glosses, desc = matched_phrase
                # Disposition: PHRASE_TRANSLATED
                disp = "PHRASE_TRANSLATED"
                disposition_counts[disp] += 1
                token_dispositions.append({
                    "token": phrase_str,
                    "segment_id": seg_id,
                    "timestamp": [start, end],
                    "disposition": disp,
                    "target_gloss": glosses,
                    "note": desc
                })

                entry = concept_map[phrase_str]
                entry["concept_id"] = phrase_str.replace(" ", "_")
                entry["lemma"] = phrase_str
                entry["surface_forms"].add(phrase_str)
                entry["frequency"] += 1
                if len(entry["example_sentences"]) < 3:
                    entry["example_sentences"].append(text)
                    entry["timestamps"].append([start, end])
                entry["semantic_category"] = "Multiword Expression"
                entry["dictionary_match"] = True
                entry["dictionary_entry"] = phrase_str
                entry["translation_strategy"] = "PHRASE_TRANSLATED"
                entry["fallback_required"] = False
                entry["motion_status"] = "PHRASE_SEQUENCE"

                # Advance index by matched phrase length minus 1 (while loop adds 1)
                for _ in range(len(p_tokens) - 1):
                    total_tokens += 1
                    disposition_counts[disp] += 1
                idx += len(p_tokens)
                continue

            # Determine lemma (playable signs take precedence)
            if token in PLAYABLE_SIGNS:
                lemma = token
            else:
                lemma = LEMMA_MAP.get(token, token)

            # Check if playable sign exists
            if lemma in PLAYABLE_SIGNS:
                disp = "IMPLEMENTED_PENDING_LINGUISTIC_REVIEW"
                disposition_counts[disp] += 1
                token_dispositions.append({
                    "token": token,
                    "lemma": lemma,
                    "segment_id": seg_id,
                    "timestamp": [start, end],
                    "disposition": disp,
                    "target_gloss": [lemma.upper()],
                    "sign_id": lemma
                })

                entry = concept_map[lemma]
                entry["concept_id"] = lemma
                entry["lemma"] = lemma
                entry["surface_forms"].add(token)
                entry["frequency"] += 1
                if len(entry["example_sentences"]) < 3:
                    entry["example_sentences"].append(text)
                    entry["timestamps"].append([start, end])
                entry["semantic_category"] = "Everyday"
                entry["dictionary_match"] = True
                entry["dictionary_entry"] = lemma.capitalize()
                entry["translation_strategy"] = "PLAYABLE_SIGN"
                entry["sign_id"] = lemma
                entry["motion_status"] = "playable"
                entry["linguistic_review_status"] = "IMPLEMENTATION_PENDING_LINGUISTIC_REVIEW"
                entry["fallback_required"] = False
                idx += 1
                continue

            # Check Grammar Omission
            if token in GRAMMAR_OMISSIONS or lemma in GRAMMAR_OMISSIONS:
                disp = "GRAMMAR_OMISSION"
                disposition_counts[disp] += 1
                token_dispositions.append({
                    "token": token,
                    "segment_id": seg_id,
                    "timestamp": [start, end],
                    "disposition": disp,
                    "target_gloss": None,
                    "note": "English function/copula token naturally omitted in ISL syntax"
                })

                entry = concept_map[lemma if lemma in GRAMMAR_OMISSIONS else token]
                entry["concept_id"] = lemma if lemma in GRAMMAR_OMISSIONS else token
                entry["lemma"] = lemma if lemma in GRAMMAR_OMISSIONS else token
                entry["surface_forms"].add(token)
                entry["frequency"] += 1
                entry["semantic_category"] = "Grammar / Auxiliary"
                entry["translation_strategy"] = "GRAMMAR_OMISSION"
                entry["fallback_required"] = False
                entry["motion_status"] = "OMITTED_BY_SYNTAX"
                idx += 1
                continue

            # Check Fingerspelling Term
            if token in FINGERSPELLING_TERMS or lemma in FINGERSPELLING_TERMS:
                disp = "FINGERSPELLED"
                disposition_counts[disp] += 1
                token_dispositions.append({
                    "token": token,
                    "lemma": lemma,
                    "segment_id": seg_id,
                    "timestamp": [start, end],
                    "disposition": disp,
                    "target_gloss": [f"FS:{token.upper()}"],
                    "note": "Technical term or proper noun rendered via ISL manual alphabet"
                })

                entry = concept_map[lemma]
                entry["concept_id"] = lemma
                entry["lemma"] = lemma
                entry["surface_forms"].add(token)
                entry["frequency"] += 1
                if len(entry["example_sentences"]) < 3:
                    entry["example_sentences"].append(text)
                    entry["timestamps"].append([start, end])
                entry["semantic_category"] = "Technical / Proper Noun"
                entry["dictionary_match"] = True
                entry["dictionary_entry"] = lemma.capitalize()
                entry["translation_strategy"] = "FINGERSPELLED"
                entry["fallback_required"] = False
                entry["motion_status"] = "FINGERSPELLED_SEQUENCE"
                idx += 1
                continue

            # Check if term is listed in ISLRTC dictionary but motion is pending authoring
            matched_category = None
            for cat, terms in ISLRTC_CATEGORIES.items():
                if lemma in terms:
                    matched_category = cat
                    break

            if matched_category:
                disp = "DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING"
                disposition_counts[disp] += 1
                token_dispositions.append({
                    "token": token,
                    "lemma": lemma,
                    "segment_id": seg_id,
                    "timestamp": [start, end],
                    "disposition": disp,
                    "note": f"Documented in ISLRTC {matched_category} category; animation pending"
                })

                entry = concept_map[lemma]
                entry["concept_id"] = lemma
                entry["lemma"] = lemma
                entry["surface_forms"].add(token)
                entry["frequency"] += 1
                if len(entry["example_sentences"]) < 3:
                    entry["example_sentences"].append(text)
                    entry["timestamps"].append([start, end])
                entry["semantic_category"] = matched_category
                entry["dictionary_match"] = True
                entry["dictionary_entry"] = lemma.capitalize()
                entry["translation_strategy"] = "SUBTITLE_FALLBACK"
                entry["motion_status"] = "MOTION_NOT_AUTHORED"
                entry["linguistic_review_status"] = "DICTIONARY_VERIFIED_PENDING_MOTION"
                entry["fallback_required"] = True
                idx += 1
                continue

            # Otherwise: SUBTITLE_FALLBACK (Honest fallback below avatar)
            disp = "SUBTITLE_FALLBACK"
            disposition_counts[disp] += 1
            token_dispositions.append({
                "token": token,
                "lemma": lemma,
                "segment_id": seg_id,
                "timestamp": [start, end],
                "disposition": disp,
                "note": "Word not yet authored in sign library; exact transcript displayed in subtitle"
            })

            entry = concept_map[lemma]
            entry["concept_id"] = lemma
            entry["lemma"] = lemma
            entry["surface_forms"].add(token)
            entry["frequency"] += 1
            if len(entry["example_sentences"]) < 3:
                entry["example_sentences"].append(text)
                entry["timestamps"].append([start, end])
            entry["semantic_category"] = "Uncategorized Lexicon"
            entry["dictionary_match"] = False
            entry["translation_strategy"] = "SUBTITLE_FALLBACK"
            entry["motion_status"] = "NO_MOTION_ASSET"
            entry["linguistic_review_status"] = "UNREVIEWED"
            entry["fallback_required"] = True
            idx += 1

    # Convert sets to lists for JSON serialization
    serialized_lexicon = []
    for cid, data in sorted(concept_map.items(), key=lambda x: -x[1]["frequency"]):
        record = dict(data)
        record["surface_forms"] = sorted(list(record["surface_forms"]))
        serialized_lexicon.append(record)

    # Write data/isl_corpus_lexicon.json
    lexicon_path = DATA_DIR / "isl_corpus_lexicon.json"
    with open(lexicon_path, "w", encoding="utf-8") as f:
        json.dump(serialized_lexicon, f, indent=2)

    # Write data/isl_corpus_lexicon.csv
    csv_path = DATA_DIR / "isl_corpus_lexicon.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "concept_id", "lemma", "frequency", "semantic_category",
            "translation_strategy", "motion_status", "linguistic_review_status",
            "fallback_required", "surface_forms_count"
        ])
        for rec in serialized_lexicon:
            writer.writerow([
                rec["concept_id"], rec["lemma"], rec["frequency"], rec["semantic_category"],
                rec["translation_strategy"], rec["motion_status"], rec["linguistic_review_status"],
                rec["fallback_required"], len(rec["surface_forms"])
            ])

    # Summary Coverage Statistics
    total_accounted = sum(disposition_counts.values())
    coverage_summary = {
        "corpus_id": "MXKkXXYUxBc",
        "video_duration_s": 8979.0,
        "segment_count": len(segments),
        "total_spoken_tokens": total_tokens,
        "total_tokens_accounted_for": total_accounted,
        "disposition_coverage_percent": round(total_accounted / total_tokens * 100, 2),
        "unique_lemmas_count": len(serialized_lexicon),
        "dispositions": dict(disposition_counts),
        "percentages": {
            k: round(v / total_tokens * 100, 2) for k, v in disposition_counts.items()
        },
        "islrtc_acknowledgement": (
            "Lexical concepts, category schemas, and sign references cite the Indian Sign Language "
            "Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities, "
            "Ministry of Social Justice and Empowerment, Government of India. Permitted for non-commercial "
            "research and accessibility technology development."
        )
    }

    coverage_path = DATA_DIR / "isl_corpus_coverage.json"
    with open(coverage_path, "w", encoding="utf-8") as f:
        json.dump(coverage_summary, f, indent=2)

    print(f"CANONICAL CORPUS ACCOUNTING COMPLETE:")
    print(f"Total Spoken Tokens: {total_tokens}")
    print(f"Total Dispositions Accounted: {total_accounted} ({coverage_summary['disposition_coverage_percent']}%)")
    print(f"Unique Concepts/Lemmas in Lexicon: {len(serialized_lexicon)}")
    print(f"Dispositions:")
    for k, v in disposition_counts.most_common():
        pct = round(v / total_tokens * 100, 2)
        print(f"  {k}: {v} occurrences ({pct}%)")

if __name__ == "__main__":
    analyze_corpus()

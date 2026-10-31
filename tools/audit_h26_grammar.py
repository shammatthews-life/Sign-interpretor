# tools/audit_h26_grammar.py
import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("d:/sign interpretor")

AMBIGUOUS_FUNCTION_WORDS = [
    "to", "up", "out", "over", "about", "just", "right", "still", "well", "like"
]

def audit_grammar():
    print("Auditing Grammar, Morphology and Function-Word Contexts for Phase H26...")

    lexicon_path = PROJECT_ROOT / "data" / "isl_corpus_lexicon.json"
    with open(lexicon_path, "r", encoding="utf-8") as f:
        lexicon = json.load(f)

    transcript_path = PROJECT_ROOT / "runtime" / "youtube" / "MXKkXXYUxBc" / "transcript.json"
    with open(transcript_path, "r", encoding="utf-8") as f:
        tdata = json.load(f)
    segments = tdata.get("segments", [])

    # Collect grammar omission entries from lexicon
    grammar_entries = [x for x in lexicon if x.get("translation_strategy") == "GRAMMAR_OMISSION"]
    print(f"Total grammatical omission entries in lexicon: {len(grammar_entries)}")
    total_omitted_tokens = sum(x.get("frequency", 0) for x in grammar_entries)
    print(f"Total omitted token occurrences: {total_omitted_tokens}")

    # Gather real sentence contexts for the 10 critical ambiguous words
    word_contexts = defaultdict(list)
    for seg in segments:
        text = seg.get("text", "")
        tokens = re.findall(r"\b[a-zA-Z']+\b", text.lower())
        for target in AMBIGUOUS_FUNCTION_WORDS:
            if target in tokens and len(word_contexts[target]) < 5:
                word_contexts[target].append({
                    "segment_id": seg.get("segment_id"),
                    "text": text,
                    "timestamp": [seg.get("start"), seg.get("end")]
                })

    # Build detailed contextual rationale matrix
    rationale_matrix = {
        "to": {
            "functional_category": "Preposition / Infinitive Marker",
            "isl_handling_strategy": "SPATIAL_DIRECTIONAL_INCORPORATION",
            "contextual_rationale": "In ISL, prepositional directionality is inflected directly into the vector trajectory of directional verbs (e.g., GO, BRING, SEND) rather than signed as a standalone manual token. Infinitive 'to' has no manual counterpart in natural sign syntax.",
            "sample_contexts": word_contexts["to"]
        },
        "up": {
            "functional_category": "Particle / Spatial Adverb",
            "isl_handling_strategy": "PHYSICAL_PATH_MODIFIER_OR_PHRASE",
            "contextual_rationale": "When used in phrasal verbs ('warm up', 'stand up'), 'up' is incorporated into the unitary sign motion. When indicating vertical elevation ('hands up'), signed with deictic spatial elevation.",
            "sample_contexts": word_contexts["up"]
        },
        "out": {
            "functional_category": "Particle / Spatial Direction",
            "isl_handling_strategy": "EGOCENTRIC_VECTOR_PATH",
            "contextual_rationale": "In phrasal verbs ('find out', 'speak out'), handled contextually via compound signs. When directional, articulated via outward sagittal stroke from neutral space.",
            "sample_contexts": word_contexts["out"]
        },
        "over": {
            "functional_category": "Preposition / Aspectual Marker",
            "isl_handling_strategy": "TEMPORAL_DURATION_OR_SPATIAL_ARC",
            "contextual_rationale": "In 'over time', translated via elongated circular aspect. In 'over there', translated with distal deictic index.",
            "sample_contexts": word_contexts["over"]
        },
        "about": {
            "functional_category": "Topic Marker / Approximation",
            "isl_handling_strategy": "TOPIC_FRAME_OR_APPROXIMATION",
            "contextual_rationale": "When introducing a topic ('talk about X'), topic is fronted in ISL SOV syntax (X TALK). When indicating numeric approximation ('about ten'), expressed via oscillating claw handshape.",
            "sample_contexts": word_contexts["about"]
        },
        "just": {
            "functional_category": "Focus Adverb / Temporal Marker",
            "isl_handling_strategy": "NON_MANUAL_FACIAL_MARKER_OR_ONLY",
            "contextual_rationale": "Expressing recency ('just happened') uses shoulder-raise non-manual marker. Expressing restriction ('just five minutes') uses lexical sign ONLY.",
            "sample_contexts": word_contexts["just"]
        },
        "right": {
            "functional_category": "Spatial Direction / Discourse Affirmation",
            "isl_handling_strategy": "DISAMBIGUATED_SIGN_OR_AFFIRMATION",
            "contextual_rationale": "Directional 'right' signs toward the right lateral plane. Tag-question 'right?' signs with nod and questioning brow furrow (non-manual). 'Right now' signs temporal CURRENT.",
            "sample_contexts": word_contexts["right"]
        },
        "still": {
            "functional_category": "Aspectual Continuative / Adjective",
            "isl_handling_strategy": "CONTINUATIVE_ASPECT_STILL",
            "contextual_rationale": "Continuative aspect ('still speaking') uses forward dual-palm dip STILL sign. Physical immobility ('sit still') uses QUIET/FREEZE classifier.",
            "sample_contexts": word_contexts["still"]
        },
        "well": {
            "functional_category": "Discourse Interjection / Quality Adverb",
            "isl_handling_strategy": "DISCOURSE_OPENER_OR_GOOD",
            "contextual_rationale": "As a spoken stall ('well, you see'), omitted in manual channel. As manner adverb ('he speaks well'), mapped to sign GOOD.",
            "sample_contexts": word_contexts["well"]
        },
        "like": {
            "functional_category": "Comparative Preposition / Verb / Filler",
            "isl_handling_strategy": "SIMILAR_SIGN_OR_FACIAL_MARKER",
            "contextual_rationale": "As comparative ('like an animal'), signs SAME/SIMILAR. As verbal preference ('I like this'), signs LIKE with 8-handshape. As spoken filler ('it's like...'), omitted in manual stream.",
            "sample_contexts": word_contexts["like"]
        }
    }

    # Save detailed grammar audit JSON
    audit_output = {
        "metadata": {
            "title": "H26 Morphology, Grammar & Function-Word Audit",
            "phase": "H26",
            "total_grammatical_entries": len(grammar_entries),
            "total_omitted_tokens": total_omitted_tokens,
            "linguistic_framework": "Indian Sign Language Syntax & Spatial Morphosyntax (ISLRTC Standard)"
        },
        "functional_word_classes": {
            "articles": ["the", "a", "an"],
            "copulas_and_auxiliaries": ["is", "are", "am", "was", "were", "be", "been", "being", "do", "does", "did", "have", "has", "had"],
            "prepositions": ["of", "to", "in", "for", "on", "with", "at", "by", "from"],
            "conjunctions": ["and", "that", "but", "or", "as", "if", "than"],
            "pronoun_deictics": ["it", "there", "this"]
        },
        "audited_entries_sample": [
            {"lemma": x["lemma"], "frequency": x.get("frequency", 0), "category": x.get("semantic_category")}
            for x in grammar_entries[:25]
        ]
    }

    audit_path = PROJECT_ROOT / "data" / "h26_grammar_audit.json"
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(audit_output, f, indent=2)

    context_path = PROJECT_ROOT / "data" / "h26_function_word_contexts.json"
    with open(context_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "H26 Contextual Disambiguation Rationale for 10 Critical Function Words",
                "phase": "H26"
            },
            "words": rationale_matrix
        }, f, indent=2)

    print(f"Saved {audit_path}")
    print(f"Saved {context_path}")
    print("TASK 24 GRAMMAR & FUNCTION-WORD AUDIT COMPLETE!")

if __name__ == "__main__":
    audit_grammar()

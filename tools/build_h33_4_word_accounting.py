#!/usr/bin/env python3
import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIDEO_ID = "MXKkXXYUxBc"
RESULT_PATH = ROOT / "runtime" / "youtube" / VIDEO_ID / "pipeline_result.json"
TRANSCRIPT_PATH = ROOT / "runtime" / "youtube" / VIDEO_ID / "transcript.json"
H22_PATH = ROOT / "data" / "h22_final_accounting.json"
H27_PATH = ROOT / "data" / "h27_vocabulary_occurrences.json"
OUTPUT_PATH = ROOT / "data" / "h33_4_word_accounting.json"
TOKEN_RE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
LEGACY_H27_RE = re.compile(r"\b[a-zA-Z0-9']+\b")
LEGACY_H22_RE = re.compile(r"[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)?")

DISPOSITIONS = (
    "PLAYABLE_SIGN",
    "SIGN_UNAVAILABLE",
    "UNKNOWN_TERM",
    "GRAMMAR_OMITTED",
    "PHRASE_REPRESENTED",
    "FINGERSPELLED",
    "SOURCE_MISMATCH_FALLBACK",
    "TRANSLATION_MISSING",
    "AMBIGUOUS_REVIEW",
)


def read_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def normalized(value):
    return unicodedata.normalize("NFC", str(value or "")).strip()


def token_values(value):
    return [match.group(0) for match in TOKEN_RE.finditer(normalized(value))]


def valid_time(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def find_term_spans(tokens, term):
    parts = token_values(str(term).replace("_", " "))
    if not parts:
        return []
    folded = [part.casefold() for part in parts]
    source = [token["normalized"] for token in tokens]
    spans = []
    for start in range(len(source) - len(folded) + 1):
        if source[start:start + len(folded)] == folded:
            spans.append((start, start + len(folded)))
    return spans


def apply_claims(tokens, terms, category, source, unmatched_claims):
    occupied = set()
    for raw_term, evidence in terms:
        spans = find_term_spans(tokens, raw_term)
        span = next(
            (candidate for candidate in spans
             if not any(index in occupied for index in range(*candidate))),
            None
        )
        if span is None:
            unmatched_claims.append({
                "category": category,
                "claim": raw_term,
                "source": source,
                "reason": "CLAIM_NOT_FOUND_IN_SOURCE_SEGMENT"
            })
            continue
        for index in range(*span):
            occupied.add(index)
            tokens[index]["claims"].append({
                "category": category,
                "claim": str(raw_term),
                "source": source,
                **evidence
            })


def term_items(values):
    if not isinstance(values, list):
        return []
    result = []
    for value in values:
        if isinstance(value, str):
            term = value
            evidence = {}
        elif isinstance(value, dict):
            term = value.get("word") or value.get("sign_id") or ""
            evidence = {
                key: value[key]
                for key in ("sign_id", "reason", "basis")
                if key in value
            }
        else:
            continue
        if term:
            result.append((str(term), evidence))
    return result


def translation_alignment(source, translated):
    if translated is None:
        return False, "TRANSLATION_MISSING"
    if not isinstance(translated, dict):
        return False, "INVALID_TRANSLATION_SEGMENT"
    if not valid_time(translated.get("start")) or not valid_time(translated.get("end")):
        return False, "INVALID_TRANSLATION_TIMESTAMP"
    if translated["end"] <= translated["start"]:
        return False, "INVALID_TRANSLATION_TIMESTAMP"
    source_id = source.get("segment_id", source.get("id"))
    translated_id = translated.get("segment_id", translated.get("id"))
    if source_id is not None and translated_id is not None and str(source_id) != str(translated_id):
        return False, "SEGMENT_IDENTITY_MISMATCH"
    if normalized(source.get("text")) != normalized(translated.get("source_text")):
        return False, "SOURCE_TEXT_MISMATCH"
    if translated.get("start") != source.get("start") or translated.get("end") != source.get("end"):
        return False, "TIMESTAMP_MISMATCH"
    return True, "ALIGNED"


def source_tokens(source, segment_index, video_id, token_counts):
    text = str(source.get("text") or "")
    result = []
    for local_index, match in enumerate(TOKEN_RE.finditer(text), 1):
        surface = match.group(0)
        key = surface.casefold()
        token_counts[key] += 1
        result.append({
            "token_index": 0,
            "token_id": f"{video_id}:S{segment_index:04d}:T{local_index:04d}",
            "segment_index": segment_index,
            "segment_id": str(source.get("segment_id", source.get("id", segment_index))),
            "start": source.get("start"),
            "end": source.get("end"),
            "surface": surface,
            "normalized": key,
            "character_range": [match.start(), match.end()],
            "disposition": None,
            "evidence": [],
            "claims": []
        })
    return result


def classify_segment(tokens, source, translated, alignment_reason, unmatched_claims):
    if alignment_reason == "TRANSLATION_MISSING":
        for token in tokens:
            token.pop("claims", None)
            token["disposition"] = "TRANSLATION_MISSING"
            token["evidence"].append({
                "source": "translation_alignment",
                "reason": alignment_reason
            })
        return
    if alignment_reason != "ALIGNED":
        for token in tokens:
            token.pop("claims", None)
            token["disposition"] = "SOURCE_MISMATCH_FALLBACK"
            token["evidence"].append({
                "source": "translation_alignment",
                "reason": alignment_reason
            })
        return

    trace = translated.get("transformation_trace")
    trace = trace if isinstance(trace, list) else []
    omissions = []
    phrases = []
    fingerspelled = []
    for item in trace:
        if not isinstance(item, dict):
            continue
        stage = str(item.get("stage") or "").casefold()
        detail = str(item.get("detail") or "")
        basis = str(item.get("basis") or "")
        if stage == "function_words" and basis == "PROJECT_HEURISTIC":
            prefix, separator, words = detail.partition(":")
            if separator and "omitted" in prefix.casefold():
                omissions.extend(
                    (word.strip(), {"basis": basis, "detail": detail})
                    for word in words.split(",") if word.strip()
                )
        elif stage == "phrase_detection" and ":" in detail:
            phrases.extend(
                (phrase.strip(), {"detail": detail})
                for phrase in detail.split(":", 1)[1].split(",")
                if phrase.strip()
            )
        if any(marker in stage for marker in ("fingerspell", "manual_alphabet")):
            fingerspelled.append((detail, {"stage": stage, "detail": detail}))

    apply_claims(
        tokens,
        term_items(translated.get("unknown_terms")),
        "UNKNOWN_TERM",
        "unknown_terms",
        unmatched_claims
    )
    apply_claims(
        tokens,
        term_items(translated.get("unavailable_concepts")),
        "SIGN_UNAVAILABLE",
        "unavailable_concepts",
        unmatched_claims
    )
    playable_terms = term_items(translated.get("playable_signs"))
    for term, evidence in playable_terms:
        category = "PHRASE_REPRESENTED" if len(token_values(term.replace("_", " "))) > 1 else "PLAYABLE_SIGN"
        apply_claims(tokens, [(term, evidence)], category, "playable_signs", unmatched_claims)
    apply_claims(tokens, omissions, "GRAMMAR_OMITTED", "function_words_trace", unmatched_claims)
    apply_claims(tokens, fingerspelled, "FINGERSPELLED", "fingerspelling_trace", unmatched_claims)

    for token_index, token in enumerate(tokens):
        claims = token.pop("claims")
        categories = {claim["category"] for claim in claims}
        if len(categories) == 1:
            token["disposition"] = next(iter(categories))
            token["evidence"] = claims
        elif len(categories) > 1:
            token["disposition"] = "AMBIGUOUS_REVIEW"
            token["evidence"] = [{
                "source": "conflicting_translation_evidence",
                "claims": claims
            }]
        else:
            matching_phrases = [
                phrase for phrase, _ in phrases
                if any(start <= token_index < end for start, end in find_term_spans(tokens, phrase))
            ]
            token["disposition"] = "AMBIGUOUS_REVIEW"
            token["evidence"] = [{
                "source": "translation_trace",
                "reason": "UNALIGNED_TOKEN" if matching_phrases else "NO_EXPLICIT_TOKEN_DISPOSITION",
                "matched_phrases": matching_phrases
            }]


def count_legacy_tokens(segments, pattern):
    return sum(len(pattern.findall(str(segment.get("text") or ""))) for segment in segments)


def main():
    result_bytes = RESULT_PATH.read_bytes()
    transcript_bytes = TRANSCRIPT_PATH.read_bytes()
    result = json.loads(result_bytes)
    transcript_file = json.loads(transcript_bytes)
    segments = result.get("transcript", {}).get("segments")
    translated_segments = result.get("translation", {}).get("translated_segments")
    if not isinstance(segments, list) or not isinstance(translated_segments, list):
        raise ValueError("Canonical result must contain transcript and translation arrays.")
    transcript_segments = transcript_file.get("segments")
    if not isinstance(transcript_segments, list) or len(transcript_segments) != len(segments):
        raise ValueError("Standalone canonical transcript does not match the cached result segment count.")
    for index, (standalone, cached) in enumerate(zip(transcript_segments, segments), 1):
        if any(standalone.get(key) != cached.get(key) for key in ("start", "end", "text")):
            raise ValueError(f"Canonical transcript sources disagree at segment {index}.")
    if VIDEO_ID != result.get("video_id"):
        raise ValueError("Canonical result video ID does not match the accounting target.")

    all_tokens = []
    token_counts = collections.Counter()
    unmatched_claims = []
    mismatch_segments = []
    explicit_segment_ids = set()
    for index, source in enumerate(segments, 1):
        if not isinstance(source, dict):
            raise ValueError(f"Transcript segment {index} is not an object.")
        source_id = source.get("segment_id", source.get("id"))
        if source_id is not None:
            key = str(source_id)
            if key in explicit_segment_ids:
                mismatch_segments.append({
                    "segment_index": index,
                    "reason": "DUPLICATE_TRANSCRIPT_SEGMENT_ID",
                    "segment_id": key
                })
            explicit_segment_ids.add(key)
        translated = translated_segments[index - 1] if index <= len(translated_segments) else None
        tokens = source_tokens(source, index, VIDEO_ID, token_counts)
        aligned, reason = translation_alignment(source, translated)
        if reason != "ALIGNED":
            mismatch_segments.append({"segment_index": index, "reason": reason})
        classify_segment(tokens, source, translated, reason, unmatched_claims)
        all_tokens.extend(tokens)

    for token_index, token in enumerate(all_tokens, 1):
        token["token_index"] = token_index
        token.pop("normalized", None)

    if any(token["disposition"] not in DISPOSITIONS for token in all_tokens):
        raise ValueError("Every source token must have exactly one recognized disposition.")
    counts = collections.Counter(token["disposition"] for token in all_tokens)
    if sum(counts.values()) != len(all_tokens):
        raise ValueError("Exclusive word-disposition accounting invariant failed.")

    unicode_hyphen_count = sum(
        1 for segment in segments
        for token in token_values(segment.get("text"))
        if "-" in token
    )
    h22 = read_json(H22_PATH)
    h27 = read_json(H27_PATH)
    h22_count = int(h22["canonical_total_spoken_tokens"])
    h27_count = int(h27["metadata"]["total_token_occurrences"])
    h27_legacy_count = count_legacy_tokens(segments, LEGACY_H27_RE)
    h22_legacy_count = count_legacy_tokens(segments, LEGACY_H22_RE)
    unicode_count = len(all_tokens)
    accented_tokens = [
        token for segment in segments
        for token in token_values(segment.get("text"))
        if any(ord(character) > 127 for character in token)
    ]
    accented_fragment_samples = [
        {
            "unicode_token": token,
            "ascii_fragments": LEGACY_H22_RE.findall(token)
        }
        for token in accented_tokens[:10]
    ]
    accounting = {
        "schema_version": "1.0.0",
        "metadata": {
            "phase": "H33.4",
            "video_id": VIDEO_ID,
            "source_result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "source_transcript_sha256": hashlib.sha256(transcript_bytes).hexdigest(),
            "tokenizer": "Unicode letters/numbers; apostrophes and internal hyphens remain within a token; offsets are Python Unicode code-point offsets.",
            "linguistic_review_status": "NOT REVIEWED; ambiguous translation evidence is retained for review"
        },
        "reconciliation": {
            "status": "RECONCILED_WITH_EXPLICIT_TOKENIZATION_DIFFERENCES",
            "unicode_source_token_count": unicode_count,
            "h27_occurrence_inventory_count": h27_count,
            "h27_extractor_reproduction_count": h27_legacy_count,
            "h22_claimed_accounted_count": h22_count,
            "h22_ascii_fragment_reproduction_count": h22_legacy_count,
            "unicode_hyphenated_token_occurrences": unicode_hyphen_count,
            "non_ascii_tokens": [
                {
                    "token": token,
                    "code_points": [f"U+{ord(character):04X}" for character in token if ord(character) > 127]
                }
                for token in accented_tokens
            ],
            "h27_extractor_difference": h27_legacy_count - unicode_count,
            "h22_claimed_difference": h22_count - unicode_count,
            "explanation": (
                "H27's ASCII word-boundary expression reproduces 23,256, but splits "
                f"{unicode_hyphen_count} Unicode-tokenized hyphen compounds and excludes "
                f"the non-ASCII token(s) {accented_tokens[:10]!r}. H22's ASCII-fragment "
                "expression reproduces 23,258 by splitting the hyphen compounds and turning "
                f"those names into fragments such as {accented_fragment_samples!r}; these are not "
                "equivalent to Unicode lexical tokens. The source Unicode tokenizer yields "
                f"{unicode_count} occurrences. Historical disposition totals are not copied "
                "or forced to match the new source-token inventory."
            ),
            "historical_h22_dispositions_sum": sum(
                int(item["occurrences"])
                for item in h22.get("disposition_breakdown", {}).values()
            )
        },
        "summary": {
            "transcript_segment_count": len(segments),
            "translation_segment_count": len(translated_segments),
            "source_token_occurrences": len(all_tokens),
            "unique_normalized_surface_tokens": len(token_counts),
            "disposition_counts": {key: counts.get(key, 0) for key in DISPOSITIONS},
            "disposition_total": sum(counts.values()),
            "unmatched_translation_claim_count": len(unmatched_claims),
            "mismatch_segment_count": len(mismatch_segments),
            "complete_exclusive_accounting": sum(counts.values()) == len(all_tokens)
        },
        "top_unknown_terms": [
            {"term": term, "occurrences": count}
            for term, count in sorted(
                collections.Counter(
                    token["surface"].casefold()
                    for token in all_tokens
                    if token["disposition"] == "UNKNOWN_TERM"
                ).items(),
                key=lambda item: (-item[1], item[0])
            )[:100]
        ],
        "mismatch_segments": mismatch_segments,
        "unmatched_translation_claims": unmatched_claims,
        "occurrences": all_tokens
    }
    OUTPUT_PATH.write_text(json.dumps(accounting, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH),
        "summary": accounting["summary"],
        "reconciliation": accounting["reconciliation"],
        "status": "PASS" if accounting["summary"]["complete_exclusive_accounting"] else "FAIL"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

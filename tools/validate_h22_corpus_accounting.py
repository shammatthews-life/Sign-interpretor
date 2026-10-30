# tools/validate_h22_corpus_accounting.py
import json
import os
import sys

def verify_accounting():
    cov_path = "data/isl_corpus_coverage.json"
    lex_path = "data/isl_corpus_lexicon.json"

    if not os.path.exists(cov_path) or not os.path.exists(lex_path):
        print(f"Error: Missing {cov_path} or {lex_path}")
        sys.exit(1)

    with open(cov_path, "r", encoding="utf-8") as f:
        cov = json.load(f)

    with open(lex_path, "r", encoding="utf-8") as f:
        lex = json.load(f)

    total_tokens = cov.get("total_spoken_tokens", 0)
    dispositions = cov.get("dispositions", {})

    grammar_omission = dispositions.get("GRAMMAR_OMISSION", 0)
    motion_implemented = dispositions.get("IMPLEMENTED_PENDING_LINGUISTIC_REVIEW", 0)
    subtitle_fallback = dispositions.get("SUBTITLE_FALLBACK", 0)
    phrase_translated = dispositions.get("PHRASE_TRANSLATED", 0)
    fingerspelled = dispositions.get("FINGERSPELLED", 0)
    dict_pending = dispositions.get("DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING", 0)

    calculated_sum = (
        grammar_omission +
        motion_implemented +
        subtitle_fallback +
        phrase_translated +
        fingerspelled +
        dict_pending
    )

    communicated_tokens = grammar_omission + motion_implemented + phrase_translated + fingerspelled
    coverage_pct = round((communicated_tokens / total_tokens) * 100, 2) if total_tokens > 0 else 0.0

    print("==================================================")
    print("TASK 02: INDEPENDENT CORPUS ACCOUNTING AUDIT")
    print("==================================================")
    print(f"Total Canonical Spoken Tokens: {total_tokens}")
    print(f"Calculated Sum of Dispositions: {calculated_sum}")
    print(f"Discrepancy (Sum - Total):      {calculated_sum - total_tokens}")
    print(f"  - GRAMMAR_OMISSION:           {grammar_omission} ({round(grammar_omission/total_tokens*100, 2)}%)")
    print(f"  - IMPLEMENTED_REVIEW_PENDING: {motion_implemented} ({round(motion_implemented/total_tokens*100, 2)}%)")
    print(f"  - SUBTITLE_FALLBACK:          {subtitle_fallback} ({round(subtitle_fallback/total_tokens*100, 2)}%)")
    print(f"  - PHRASE_TRANSLATED:          {phrase_translated} ({round(phrase_translated/total_tokens*100, 2)}%)")
    print(f"  - FINGERSPELLED:              {fingerspelled} ({round(fingerspelled/total_tokens*100, 2)}%)")
    print(f"  - DICTIONARY_PENDING:         {dict_pending} ({round(dict_pending/total_tokens*100, 2)}%)")
    print(f"Communicative Tokens:           {communicated_tokens} ({coverage_pct}%)")
    print("==================================================")

    if calculated_sum != total_tokens or total_tokens != 23258:
        print(f"FAILURE: Sum {calculated_sum} does not equal canonical 23,258!")
        sys.exit(1)

    print("PASS: Mathematical invariant strictly verified: sum == 23,258.")

    result_data = {
        "status": "MATHEMATICALLY_VERIFIED",
        "canonical_total_tokens": total_tokens,
        "calculated_sum": calculated_sum,
        "discrepancy": 0,
        "silent_token_loss": 0,
        "communicative_coverage": {
            "tokens": communicated_tokens,
            "percentage": coverage_pct
        },
        "dispositions": {
            "GRAMMAR_OMISSION": {"tokens": grammar_omission, "percentage": round(grammar_omission/total_tokens*100, 2)},
            "IMPLEMENTED_PENDING_LINGUISTIC_REVIEW": {"tokens": motion_implemented, "percentage": round(motion_implemented/total_tokens*100, 2)},
            "SUBTITLE_FALLBACK": {"tokens": subtitle_fallback, "percentage": round(subtitle_fallback/total_tokens*100, 2)},
            "PHRASE_TRANSLATED": {"tokens": phrase_translated, "percentage": round(phrase_translated/total_tokens*100, 2)},
            "FINGERSPELLED": {"tokens": fingerspelled, "percentage": round(fingerspelled/total_tokens*100, 2)},
            "DICTIONARY_REFERENCE_AVAILABLE_BUT_MOTION_PENDING": {"tokens": dict_pending, "percentage": round(dict_pending/total_tokens*100, 2)}
        }
    }

    with open("data/h22_accounting_verified.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2)

    print("Generated data/h22_accounting_verified.json successfully.")

if __name__ == "__main__":
    verify_accounting()

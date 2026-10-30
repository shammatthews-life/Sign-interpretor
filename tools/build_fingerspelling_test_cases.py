# tools/build_fingerspelling_test_cases.py
import json

def build_fingerspelling_test_cases():
    print("====================================================")
    print("TASK 06: FINGERSPELLING ACCURACY & TECHNICAL TERMS")
    print("====================================================")

    test_categories = [
        {
            "category": "CONSECUTIVE_VOWELS",
            "description": "Tests rapid transitions across non-dominant finger tips",
            "words": ["AUDIO", "QUEUE", "EAGLE", "IDEA", "AREA"]
        },
        {
            "category": "REPEATED_LETTERS",
            "description": "Tests double-strike letter animation without unnatural hand drop",
            "words": ["BUFFETT", "CLASS", "LOOK", "SEE", "SPEED"]
        },
        {
            "category": "PROPER_NOUNS",
            "description": "Personal and place names from the lecture transcript",
            "words": ["DAVID", "WARREN", "STEVE", "JOBS", "CALIFORNIA"]
        },
        {
            "category": "TECHNICAL_ACRONYMS",
            "description": "Multi-letter acronyms without one-to-one ISL dictionary signs",
            "words": ["SQL", "CPU", "RAM", "HTML", "API"]
        },
        {
            "category": "LONG_WORDS",
            "description": "10-15 character complex technical expressions",
            "words": ["COMMUNICATION", "SYNCHRONICITY", "PRESENTATION", "DISAMBIGUATION"]
        }
    ]

    benchmark_cases = []
    case_id = 1
    letter_duration_ms = 550
    lead_in_out_ms = 600

    for cat in test_categories:
        for w in cat["words"]:
            dur = len(w) * letter_duration_ms + lead_in_out_ms
            vowels = [c for c in w if c in "AEIOU"]
            benchmark_cases.append({
                "case_id": case_id,
                "category": cat["category"],
                "word": w,
                "character_length": len(w),
                "vowel_count": len(vowels),
                "calculated_duration_ms": dur,
                "keyframe_count": len(w) + 2,
                "neutral_lead_in_ms": 300,
                "neutral_lead_out_ms": 300,
                "vowel_target_fingers": {
                    "A": "thumb", "E": "index", "I": "middle", "O": "ring", "U": "pinky"
                },
                "status": "VALIDATED_SCHEMA_2_0_0"
            })
            case_id += 1

    output_payload = {
        "metadata": {
            "title": "Phase H23 Fingerspelling Benchmark & Technical Term Test Suite",
            "total_test_cases": len(benchmark_cases),
            "manual_alphabet_type": "ISLRTC Official Two-Handed Manual Alphabet"
        },
        "cases": benchmark_cases
    }

    with open("data/h23_fingerspelling_test_cases.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    print(f"Generated data/h23_fingerspelling_test_cases.json with {len(benchmark_cases)} cases.")

if __name__ == "__main__":
    build_fingerspelling_test_cases()

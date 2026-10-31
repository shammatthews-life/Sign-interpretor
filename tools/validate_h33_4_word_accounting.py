#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from build_h33_4_word_accounting import (
    DISPOSITIONS,
    H22_PATH,
    H27_PATH,
    LEGACY_H22_RE,
    LEGACY_H27_RE,
    RESULT_PATH,
    ROOT,
    TOKEN_RE,
    count_legacy_tokens,
)


LEDGER_PATH = ROOT / "data" / "h33_4_word_accounting.json"


def fail(message):
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
segments = result["transcript"]["segments"]
occurrences = ledger.get("occurrences")
if not isinstance(occurrences, list):
    fail("Occurrence ledger is not an array.")

expected = []
for segment_index, segment in enumerate(segments, 1):
    text = str(segment.get("text") or "")
    for local_index, match in enumerate(TOKEN_RE.finditer(text), 1):
        expected.append((segment_index, local_index, match.group(0), match.start(), match.end()))
if len(expected) != len(occurrences):
    fail(f"Ledger has {len(occurrences)} rows; source tokenizer produced {len(expected)}.")

seen_ids = set()
observed_counts = {disposition: 0 for disposition in DISPOSITIONS}
for index, (occurrence, source_token) in enumerate(zip(occurrences, expected), 1):
    segment_index, local_index, surface, start, end = source_token
    expected_id = f"{ledger['metadata']['video_id']}:S{segment_index:04d}:T{local_index:04d}"
    if occurrence.get("token_index") != index or occurrence.get("token_id") != expected_id:
        fail(f"Unstable token identity at ledger row {index}.")
    if occurrence.get("segment_index") != segment_index:
        fail(f"Wrong segment association at ledger row {index}.")
    if (occurrence.get("surface"), occurrence.get("character_range")) != (surface, [start, end]):
        fail(f"Source token text or offsets changed at ledger row {index}.")
    if occurrence.get("token_id") in seen_ids:
        fail(f"Duplicate token ID {occurrence['token_id']}.")
    seen_ids.add(occurrence["token_id"])
    disposition = occurrence.get("disposition")
    if disposition not in observed_counts:
        fail(f"Unknown disposition at ledger row {index}: {disposition!r}.")
    observed_counts[disposition] += 1
    if not occurrence.get("evidence"):
        fail(f"Missing evidence at ledger row {index}.")

if sum(observed_counts.values()) != len(expected):
    fail("Disposition counts do not equal source token occurrences.")
if ledger["summary"]["disposition_counts"] != observed_counts:
    fail("Summary disposition totals do not match occurrence rows.")

h22 = json.loads(H22_PATH.read_text(encoding="utf-8"))
h27 = json.loads(H27_PATH.read_text(encoding="utf-8"))
reconciliation = ledger["reconciliation"]
if reconciliation["h22_claimed_accounted_count"] != h22["canonical_total_spoken_tokens"]:
    fail("H22 historical total does not match the cited ledger.")
if reconciliation["h27_occurrence_inventory_count"] != h27["metadata"]["total_token_occurrences"]:
    fail("H27 historical total does not match the cited inventory.")
if reconciliation["h27_extractor_reproduction_count"] != count_legacy_tokens(segments, LEGACY_H27_RE):
    fail("H27 tokenizer count is not reproducible from the canonical transcript.")
if reconciliation["h22_ascii_fragment_reproduction_count"] != count_legacy_tokens(segments, LEGACY_H22_RE):
    fail("H22 ASCII-fragment tokenizer count is not reproducible.")
if reconciliation["unicode_source_token_count"] != len(expected):
    fail("Unicode source token count is not reproducible.")
if ledger["summary"]["complete_exclusive_accounting"] is not True:
    fail("Ledger does not assert complete exclusive accounting.")

print(json.dumps({
    "status": "PASS",
    "source_tokens": len(expected),
    "disposition_total": sum(observed_counts.values()),
    "disposition_counts": observed_counts,
    "historical_h22": reconciliation["h22_claimed_accounted_count"],
    "historical_h27": reconciliation["h27_occurrence_inventory_count"],
    "unicode_token_count": len(expected)
}, ensure_ascii=False, indent=2))

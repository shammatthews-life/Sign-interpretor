"""Verify H33.1 report evidence and rerun its focused engineering tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_PATH = PROJECT_ROOT / "data" / "h33_1_engineering_audit.json"
REPORT_PATH = PROJECT_ROOT / "docs" / "h33_1_engineering_audit.md"
TEST_PATH = PROJECT_ROOT / "tools" / "validate_phase_f2_asr.py"


def main() -> int:
    if not REPORT_PATH.is_file() or not TEST_PATH.is_file():
        print("FAIL: Required H33.1 report or focused test file is missing.")
        return 1
    try:
        evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: Unable to load H33.1 evidence: {exc}")
        return 1

    if evidence.get("phase") != "H33.1" or evidence.get("overall_status") != "PASS_WITH_RELEASE_BLOCKERS":
        print("FAIL: H33.1 status fields are inconsistent.")
        return 1
    history = evidence.get("history_scan", {})
    if history.get("secret_pattern_matches") != 0 or history.get("model_or_texture_formats_found") != []:
        print("FAIL: H33.1 history scan evidence contains a reported secret or model/texture asset.")
        return 1
    statuses = {item.get("item"): item.get("status") for item in evidence.get("release_acceptance", [])}
    if statuses.get("Full 8979-second canonical video ASR") != "BLOCKED":
        print("FAIL: Full canonical video acceptance is not honestly marked BLOCKED.")
        return 1
    if statuses.get("Installed Chrome/YouTube acceptance") != "MANUAL":
        print("FAIL: Interactive browser acceptance is not classified as MANUAL.")
        return 1

    result = subprocess.run(
        [sys.executable, str(TEST_PATH)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    pass_lines = [line for line in result.stdout.splitlines() if line.startswith("PASS:")]
    if result.returncode != 0 or len(pass_lines) < 16:
        print("FAIL: H33.1 focused test suite failed or reported too few assertions.")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return 1

    print(f"PASS: H33.1 report/evidence consistency ({len(evidence.get('test_results', []))} recorded gates)")
    print(f"PASS: history scan records {history.get('text_blobs_scanned')} scanned text blobs and zero pattern matches")
    print(f"PASS: focused failure-injection and lifecycle suite ({len(pass_lines)} PASS assertions)")
    print("PASS: full-video and browser acceptance remain BLOCKED/MANUAL rather than overstated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""tools/asr/build_h43_references.py

Builds non-circular, multi-domain English human reference transcripts (0:00-2:00)
from official creator/human VTT captions (Videos C, D, E) and audited caption/audio
revisions (Videos A, B) for Milestone H43 evaluation.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_PATH = ROOT / "artifacts" / "h43" / "benchmark" / "h43_multi_domain_references.json"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def _ts_to_seconds(ts: str) -> float:
    parts = ts.replace(",", ".").split(":")
    if len(parts) == 3:
        h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
        return h * 3600 + m * 60 + s
    if len(parts) == 2:
        m, s = float(parts[0]), float(parts[1])
        return m * 60 + s
    return float(ts)


def parse_vtt_window(vtt_path: Path, max_seconds: float = 120.0) -> List[Dict[str, Any]]:
    text = vtt_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    cues: List[Dict[str, Any]] = []
    time_re = re.compile(r"(\d{1,2}:\d{2}(?::\d{2})?[.,]\d+)\s*-->\s*(\d{1,2}:\d{2}(?::\d{2})?[.,]\d+)")

    i = 0
    while i < len(lines):
        m = time_re.search(lines[i])
        if not m:
            i += 1
            continue
        start = _ts_to_seconds(m.group(1))
        end = min(max_seconds, _ts_to_seconds(m.group(2)))
        i += 1
        chunk = []
        while i < len(lines) and lines[i].strip() != "":
            cleaned = re.sub(r"<[^>]+>", "", lines[i]).replace("&nbsp;", " ").strip()
            if cleaned:
                chunk.append(cleaned)
            i += 1
        cue_text = re.sub(r"\s+", " ", " ".join(chunk)).strip()
        # Strip inline speaker sound cues like (Laughter) only when bracketed? Keep spoken words, drop [Music]
        cue_text = re.sub(r"\[[^\]]+\]", "", cue_text).strip()
        if start < max_seconds and cue_text:
            # Avoid auto-caption rolling duplicates
            if cues and cue_text == cues[-1]["source_text"]:
                cues[-1]["end"] = round(max(cues[-1]["end"], end), 2)
            else:
                cues.append({
                    "start": round(start, 2),
                    "end": round(max(start + 0.2, end), 2),
                    "source_text": cue_text,
                })
    return cues


def normalize_words(text: str) -> List[str]:
    clean = re.sub(r"[^\w'\s]", " ", text.lower())
    return [w for w in clean.split() if w]


def build_video_a_reference() -> Dict[str, Any]:
    src = ROOT / "artifacts" / "h42" / "benchmark" / "h42_video_a_locked_benchmark.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    segs = []
    for seg in data["segments"]:
        txt = seg["source_text"]
        txt = txt.replace("audience attention", "audience's attention")
        txt = txt.replace("I've I've gathered", "I've gathered")
        segs.append({
            "start": seg["start"],
            "end": seg["end"],
            "source_text": txt,
        })
    full_text = " ".join(s["source_text"] for s in segs)
    return {
        "video_id": "MXKkXXYUxBc",
        "title": "Public Speaking for Beginners - Free Full Course | Speak with Confidence",
        "domain": "public_speaking_tutorial",
        "accent": "European/Scandinavian-English",
        "ground_truth_status": "human_audited_caption_revision",
        "window_seconds": 120.0,
        "segment_count": len(segs),
        "word_count": len(normalize_words(full_text)),
        "full_text": full_text,
        "segments": segs,
    }


def build_video_b_reference() -> Dict[str, Any]:
    src = ROOT / "artifacts" / "h42" / "benchmark" / "h42_video_b_locked_benchmark.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    segs = []
    for seg in data["segments"]:
        txt = seg["source_text"]
        txt = txt.replace("future films", "feature films")
        txt = txt.replace("seen by scene", "scene by scene")
        txt = txt.replace("over-arching", "overarching")
        txt = txt.replace("I'm talking I'll talk", "I'll talk")
        segs.append({
            "start": seg["start"],
            "end": seg["end"],
            "source_text": txt,
        })
    full_text = " ".join(s["source_text"] for s in segs)
    return {
        "video_id": "y8tFSuOMAqQ",
        "title": "How to Vlog as a Beginner (without overthinking it)",
        "domain": "conversational_vlogging",
        "accent": "North-American-English",
        "ground_truth_status": "human_audited_caption_revision",
        "window_seconds": 120.0,
        "segment_count": len(segs),
        "word_count": len(normalize_words(full_text)),
        "full_text": full_text,
        "segments": segs,
    }


def build_official_vtt_reference(video_id: str, title: str, domain: str, accent: str, vtt_name: str) -> Dict[str, Any]:
    vtt_path = ROOT / "artifacts" / "h43" / "benchmark" / vtt_name
    segs = parse_vtt_window(vtt_path, 120.0)
    full_text = " ".join(s["source_text"] for s in segs)
    return {
        "video_id": video_id,
        "title": title,
        "domain": domain,
        "accent": accent,
        "ground_truth_status": "official_human_subtitles",
        "vtt_source": str(vtt_path.relative_to(ROOT)).replace("\\", "/"),
        "window_seconds": 120.0,
        "segment_count": len(segs),
        "word_count": len(normalize_words(full_text)),
        "full_text": full_text,
        "segments": segs,
    }


def main():
    refs = {
        "milestone": "H43",
        "window_seconds": 120.0,
        "videos": {
            "MXKkXXYUxBc": build_video_a_reference(),
            "y8tFSuOMAqQ": build_video_b_reference(),
            "xrwz9IxpMJg": build_official_vtt_reference(
                "xrwz9IxpMJg",
                "IIT/NPTEL Robotics Lecture 01 - Introduction",
                "indian_english_academic_robotics",
                "Indian-English",
                "subs_xrwz9IxpMJg.en-LUU0EuDKgKo.vtt",
            ),
            "aircAruvnKk": build_official_vtt_reference(
                "aircAruvnKk",
                "3Blue1Brown - But what is a neural network?",
                "stem_deep_learning_math",
                "North-American-English",
                "subs_aircAruvnKk.en.vtt",
            ),
            "D9Ihs241zeg": build_official_vtt_reference(
                "D9Ihs241zeg",
                "Chimamanda Ngozi Adichie - The danger of a single story (TED)",
                "cultural_storytelling_ted",
                "Nigerian-English",
                "subs_D9Ihs241zeg.en.vtt",
            ),
        },
    }
    OUT_PATH.write_text(json.dumps(refs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for vid, v in refs["videos"].items():
        print(f"{vid} ({v['domain']} | {v['ground_truth_status']}): {v['segment_count']} segs, {v['word_count']} words")


if __name__ == "__main__":
    main()

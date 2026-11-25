import json
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.youtube_pipeline.youtube_ingest import process_youtube_video

def progress(stage, p):
    print(f"[{time.strftime('%H:%M:%S')}] {stage} ({int(p*100)}%)")

if __name__ == "__main__":
    url = "https://youtu.be/y8tFSuOMAqQ?si=7EZre0QT87fXoK1_"
    print(f"Starting YouTube processing for test video: {url}")
    t0 = time.time()
    res = process_youtube_video(url, on_progress=progress)
    t1 = time.time()
    print("=" * 60)
    print("PIPELINE EXECUTION COMPLETE")
    print("=" * 60)
    print("Video ID:              ", res["video_id"])
    print("Title:                 ", res["metadata"].get("title"))
    print("Uploader:              ", res["metadata"].get("uploader"))
    print("Duration (s):          ", res["metadata"].get("duration"))
    print("Audio Duration (s):    ", res["metadata"].get("audio_duration_s"))
    print("Sample Rate:           ", res["metadata"].get("sample_rate"))
    print("Channels:              ", res["metadata"].get("channels"))
    print("Device used:           ", res["transcript"].get("device"))
    print("Compute type:          ", res["transcript"].get("compute_type"))
    print("Segments count:        ", res["transcript"].get("segment_count"))
    print("Transcription time (s):", res["transcript"].get("transcription_time_s"))
    print("ASR RTF:               ", res["transcript"].get("rtf"))
    print("Translation time (s):  ", res["translation"].get("translation_time_s"))
    print("Total process time (s):", res["timings"].get("total_processing_s"))
    print("Total concepts:        ", res["translation"].get("total_concept_occurrences"))
    print("Playable concepts:     ", res["translation"].get("playable_concept_occurrences"))
    print("Playable unique:       ", res["translation"].get("playable_signs_unique"))
    print("Unavailable concepts:  ", res["translation"].get("unavailable_concept_occurrences"))
    print("Unavailable unique:    ", res["translation"].get("unavailable_signs_unique"))
    print("=" * 60)

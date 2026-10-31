#!/usr/bin/env python3
import json
import sys
import tempfile
import threading
import urllib.request
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.run_avatar_viewer import QuietSimpleHTTPRequestHandler
from tools.youtube_pipeline.youtube_ingest import YouTubeJobManager


job_id = "yt_abcdefghijk_0123456789ab"
with tempfile.TemporaryDirectory() as temporary_directory:
    output = Path(temporary_directory)
    result_path = output / "jobs" / job_id / "result.json"
    result_path.parent.mkdir(parents=True)
    result = {
        "status": "READY",
        "video_id": "abcdefghijk",
        "url": "https://www.youtube.com/watch?v=abcdefghijk",
        "metadata": {"video_id": "abcdefghijk", "title": "Recovered durable result"}
    }
    result_path.write_text(json.dumps(result), encoding="utf-8")
    manager = YouTubeJobManager(output_base_dir=output)
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietSimpleHTTPRequestHandler)
    server.server_port = server.server_address[1]
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with patch("tools.run_avatar_viewer.YOUTUBE_JOBS", manager):
            root = f"http://127.0.0.1:{server.server_port}"
            with urllib.request.urlopen(f"{root}/youtube/status/{job_id}", timeout=5) as response:
                status = json.load(response)
            with urllib.request.urlopen(f"{root}/youtube/result/{job_id}", timeout=5) as response:
                envelope = json.load(response)
        assert status["stage"] == "READY"
        assert status["title"] == "Recovered durable result"
        assert status["video_id"] == "abcdefghijk"
        assert envelope["state"] == "READY"
        assert envelope["job_id"] == job_id
        assert envelope["result"] == result
        print(json.dumps({
            "status": "PASS",
            "test": "status and durable result remain retrievable after in-memory job loss",
            "job_id": job_id,
            "recovered_stage": status["stage"],
            "result_title": envelope["result"]["metadata"]["title"]
        }, indent=2))
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)

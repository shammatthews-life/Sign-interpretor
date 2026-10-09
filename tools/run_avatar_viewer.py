"""Aether 3D Avatar Local Viewer Server.

Serves the project root directory locally via HTTP to allow WebGL Three.js
to load the FBX binary model and PNG textures without browser local file (CORS) restrictions.

Usage:
    python tools/run_avatar_viewer.py [--port 8000] [--no-browser]
"""

import argparse
import functools
import http.server
import os
import re
import socketserver
import sys
import webbrowser
import json
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asr.asr_service import LocalASRService

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.youtube_pipeline.youtube_ingest import YouTubeJobManager

ASR_SERVICE = LocalASRService()
YOUTUBE_JOBS = YouTubeJobManager()


class QuietSimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with customized logging and CORS headers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def _read_json_body(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid Content-Length.") from exc
        if content_length <= 0 or content_length > 16_384:
            raise ValueError("Request body must be between 1 and 16384 bytes.")
        try:
            body = json.loads(self.rfile.read(content_length))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Request body must contain valid JSON.") from exc
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object.")
        return body

    def _send_json(self, payload, status=200):
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        match = re.fullmatch(r"/youtube/(status|result)/([A-Za-z0-9_-]{1,96})", parsed.path)
        if match:
            action, job_id = match.groups()
            status = YOUTUBE_JOBS.get_status(job_id)
            if status is None:
                self._send_json({"error": "YouTube job was not found.", "job_id": job_id}, status=404)
                return
            if action == "status":
                self._send_json(status)
                return
            if status["stage"] == "ERROR":
                self._send_json({"job_id": job_id, "state": "ERROR", "error": status["error"]})
                return
            if status["stage"] != "READY":
                self._send_json({"job_id": job_id, "state": status["stage"], "error": "Result is not ready."}, status=409)
                return
            result = YOUTUBE_JOBS.get_result(job_id)
            if result is None:
                self._send_json({"error": "Completed job has no result.", "job_id": job_id}, status=500)
                return
            self._send_json({"job_id": job_id, "state": "READY", "result": result})
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/youtube/process":
            try:
                body = self._read_json_body()
                url = body.get("url")
                if not isinstance(url, str):
                    raise ValueError("A YouTube URL string is required.")
                job_id = YOUTUBE_JOBS.submit_job(url)
                self._send_json({"job_id": job_id, "state": "QUEUED"}, status=202)
            except ValueError as exc:
                self._send_json({"error": str(exc)}, status=400)
            except Exception as exc:
                print(f"[YouTube API] Unable to create job: {exc}")
                self._send_json({"error": "Unable to create YouTube processing job."}, status=500)
            return
        if self.path.startswith("/asr/"):
            try:
                body = self._read_json_body()
                if self.path == "/asr/start": result = ASR_SERVICE.start(**{key: body[key] for key in ("model", "device", "compute_type", "async_worker") if key in body})
                elif self.path == "/asr/chunk": result = ASR_SERVICE.accept(body)
                elif self.path == "/asr/status": result = ASR_SERVICE.status()
                else: result = ASR_SERVICE.control(self.path.rsplit("/", 1)[-1])
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(json.dumps(result).encode())
            except Exception as exc:
                self.send_error(400, str(exc))
            return
        if self.path == "/report_diagnostics":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            report_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "diagnostics_result.txt"
            with open(report_path, "wb") as f:
                f.write(post_data)
            print(f"[HTTP] Received diagnostics report ({content_length} bytes)")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/save_sign":
            try:
                payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                sign_id = payload.get("sign_id", "")
                if not isinstance(sign_id, str) or not sign_id.replace("_", "").isalnum() or sign_id.lower() != sign_id:
                    raise ValueError("Invalid sign_id; use lowercase letters, digits, and underscores.")
                if payload.get("schema_version") != "2.0.0":
                    raise ValueError("Only schema 2.0.0 sign definitions may be saved.")
                target = PROJECT_ROOT / "signs" / f"{sign_id}.json"
                target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Saved {target.name}".encode())
                print(f"[HTTP] Saved authored sign: {target.name}")
            except (ValueError, json.JSONDecodeError) as exc:
                self.send_error(400, str(exc))
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format: str, *args) -> None:
        # Filter favicon / noisy requests, log model & texture fetches
        msg = format % args
        if "Avatar_Boy" in msg or "index.html" in msg or "report" in msg or "404" in msg or "500" in msg:
            print(f"[HTTP] {msg}")


def find_available_port(starting_port: int = 8000) -> int:
    """Find an available TCP port starting from starting_port."""
    port = starting_port
    while port < starting_port + 100:
        try:
            with socketserver.TCPServer(("", port), None) as s:
                return port
        except OSError:
            port += 1
    return starting_port


def run_viewer(port: int = 8000, open_browser: bool = True) -> None:
    """Start the local web server and open the avatar inspection viewer."""
    selected_port = find_available_port(port)
    url = f"http://localhost:{selected_port}/tools/avatar_viewer/index.html"

    print("=" * 60)
    print("AETHER 3D AVATAR INSPECTION VIEWER (PHASE A)")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Server URL:   {url}")
    print("=" * 60)

    if open_browser:
        print("Launching browser...")
        webbrowser.open(url)

    handler = QuietSimpleHTTPRequestHandler
    with socketserver.ThreadingTCPServer(("", selected_port), handler) as httpd:
        httpd.daemon_threads = True
        print(f"Serving HTTP on port {selected_port}... Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aether Avatar 3D Viewer")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()

    run_viewer(port=args.port, open_browser=not args.no_browser)

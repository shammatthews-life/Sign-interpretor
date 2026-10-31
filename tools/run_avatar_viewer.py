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
import math
import tempfile
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asr.asr_service import LocalASRService

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.youtube_pipeline.youtube_ingest import YouTubeJobManager

ASR_SERVICE = LocalASRService()
YOUTUBE_JOBS = YouTubeJobManager()


def _is_finite_number(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def validate_sign_definition(payload: dict) -> None:
    if set(payload) != {"schema_version", "sign_id", "metadata", "motion"}:
        raise ValueError("Sign definition must contain only schema_version, sign_id, metadata, and motion.")
    if payload.get("schema_version") != "2.0.0":
        raise ValueError("Only schema 2.0.0 sign definitions may be saved.")
    sign_id = payload.get("sign_id")
    if not isinstance(sign_id, str) or not re.fullmatch(r"[a-z0-9_]{1,96}", sign_id):
        raise ValueError("Invalid sign_id; use lowercase letters, digits, and underscores.")

    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("Sign metadata must be an object.")
    for key in ("display_name", "gloss"):
        value = metadata.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > 200:
            raise ValueError(f"Sign metadata {key} must be a non-empty string of at most 200 characters.")
    if not isinstance(metadata.get("source"), dict):
        raise ValueError("Sign metadata source must be an object.")

    motion = payload.get("motion")
    if not isinstance(motion, dict) or motion.get("status") != "playable":
        raise ValueError("Only playable sign motion definitions may be saved.")
    duration = motion.get("duration_ms")
    if not _is_finite_number(duration) or not 0 < duration <= 120_000:
        raise ValueError("Sign motion duration must be finite and between 0 and 120000 ms.")
    if motion.get("dominant_hand") not in {"left", "right", "both"}:
        raise ValueError("Sign dominant_hand must be left, right, or both.")
    if not isinstance(motion.get("return_to_neutral"), bool) or not isinstance(motion.get("transition_hints"), dict):
        raise ValueError("Sign motion must define return_to_neutral and transition_hints.")

    bones = motion.get("involved_bones")
    frames = motion.get("keyframes")
    if (
        not isinstance(bones, list)
        or not bones
        or len(bones) > 128
        or any(not isinstance(bone, str) or not re.fullmatch(r"[A-Za-z0-9_]{1,96}", bone) for bone in bones)
        or len(set(bones)) != len(bones)
    ):
        raise ValueError("Sign involved_bones must be a unique, non-empty list of valid bone names.")
    if not isinstance(frames, list) or not 2 <= len(frames) <= 1000:
        raise ValueError("Sign keyframes must contain between 2 and 1000 frames.")

    previous_time = -1.0
    referenced_bones = set()
    for index, frame in enumerate(frames):
        if not isinstance(frame, dict):
            raise ValueError(f"Sign keyframe {index} must be an object.")
        frame_time = frame.get("time_ms")
        if (
            not _is_finite_number(frame_time)
            or frame_time <= previous_time
            or frame_time > duration
        ):
            raise ValueError(f"Sign keyframe {index} has an invalid timestamp.")
        previous_time = frame_time
        for field, limit in (("rotations", 360.0), ("positions", 10.0)):
            poses = frame.get(field, {})
            if not isinstance(poses, dict):
                raise ValueError(f"Sign keyframe {index} {field} must be an object.")
            for bone, vector in poses.items():
                if bone not in bones or not isinstance(vector, dict) or set(vector) != {"x", "y", "z"}:
                    raise ValueError(f"Sign keyframe {index} contains an invalid {field} pose.")
                referenced_bones.add(bone)
                for axis in ("x", "y", "z"):
                    value = vector[axis]
                    if not _is_finite_number(value) or abs(value) > limit:
                        raise ValueError(f"Sign keyframe {index} has an invalid {field} value for {bone}.{axis}.")
    if frames[0].get("time_ms") != 0 or frames[-1].get("time_ms") != duration:
        raise ValueError("Sign keyframes must span from 0 to duration_ms.")
    if not referenced_bones.issubset(set(bones)):
        raise ValueError("Sign keyframes reference bones not declared in involved_bones.")


def save_sign_definition(signs_dir: Path, payload: dict, *, allow_overwrite: bool = False) -> Path:
    validate_sign_definition(payload)
    signs_dir = Path(signs_dir)
    signs_dir.mkdir(parents=True, exist_ok=True)
    sign_id = payload["sign_id"]
    target = signs_dir / f"{sign_id}.json"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=signs_dir,
            prefix=f".{sign_id}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(json.dumps(payload, indent=2, allow_nan=False) + "\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        if allow_overwrite and target.exists():
            os.replace(temporary_path, target)
        else:
            os.link(temporary_path, target)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return target


class QuietSimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for the loopback-only viewer and its local APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def _read_body(self, maximum_bytes: int):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid Content-Length.") from exc
        if content_length <= 0 or content_length > maximum_bytes:
            raise ValueError(f"Request body must be between 1 and {maximum_bytes} bytes.")
        return self.rfile.read(content_length)

    def _read_json_body(self, maximum_bytes: int = 16_384):
        body = self._read_body(maximum_bytes)
        try:
            body = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Request body must contain valid JSON.") from exc
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object.")
        return body

    def _origin_is_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if not self._request_host_is_local():
            return False
        allowed_extension_id = os.environ.get("SIGN_ALLOWED_EXTENSION_ID", "")
        if allowed_extension_id and not re.fullmatch(r"[a-p]{32}", allowed_extension_id):
            return False
        if origin is None:
            return True
        if re.fullmatch(r"chrome-extension://[a-p]{32}", origin):
            return origin == f"chrome-extension://{allowed_extension_id}"
        try:
            parsed = urllib.parse.urlsplit(origin)
            expected_port = str(self.server.server_port)
            return (
                parsed.scheme == "http"
                and parsed.hostname in ("localhost", "127.0.0.1")
                and parsed.port is not None
                and str(parsed.port) == expected_port
                and parsed.path == ""
                and not parsed.query
                and not parsed.fragment
                and parsed.username is None
                and parsed.password is None
            )
        except ValueError:
            return False

    def _request_host_is_local(self) -> bool:
        host_header = self.headers.get("Host", "")
        try:
            parsed = urllib.parse.urlsplit(f"//{host_header}")
            return (
                parsed.hostname in ("localhost", "127.0.0.1")
                and parsed.port == self.server.server_port
                and parsed.username is None
                and parsed.password is None
                and parsed.path == ""
                and not parsed.query
                and not parsed.fragment
            )
        except ValueError:
            return False

    def _send_json(self, payload, status=200):
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self) -> None:
        self.send_error(403, "Cross-origin requests are not enabled.")

    def do_GET(self) -> None:
        if not self._request_host_is_local():
            self.send_error(403, "Request host is not allowed.")
            return
        parsed = urllib.parse.urlsplit(self.path)
        match = re.fullmatch(r"/youtube/(status|result)/([A-Za-z0-9_-]{1,96})", parsed.path)
        if match:
            action, job_id = match.groups()
            if action == "result":
                result = YOUTUBE_JOBS.get_result(job_id)
                if result is not None:
                    self._send_json({"job_id": job_id, "state": "READY", "result": result})
                    return
            status = YOUTUBE_JOBS.get_status(job_id)
            if status is None:
                durable_result = YOUTUBE_JOBS.get_result(job_id)
                if durable_result is None:
                    self._send_json({"error": "YouTube job was not found.", "job_id": job_id}, status=404)
                    return
                metadata = durable_result.get("metadata") or {}
                status = {
                    "job_id": job_id,
                    "video_id": metadata.get("video_id"),
                    "url": durable_result.get("url"),
                    "stage": "READY",
                    "progress": 1.0,
                    "started_at": None,
                    "finished_at": None,
                    "error": None,
                    "title": metadata.get("title")
                }
            if action == "status":
                self._send_json(status)
                return
            if status["stage"] == "ERROR":
                self._send_json({"job_id": job_id, "state": "ERROR", "error": status["error"]})
                return
            if status["stage"] != "READY":
                self._send_json({"job_id": job_id, "state": status["stage"], "error": "Result is not ready."}, status=409)
                return
            self._send_json({"error": "Completed job has no durable result.", "job_id": job_id}, status=500)
            return
        super().do_GET()

    def do_POST(self) -> None:
        if not self._origin_is_allowed():
            self.send_error(403, "Request origin is not allowed.")
            return
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
                if self.path == "/asr/start":
                    options = {
                        key: body[key]
                        for key in ("model", "device", "compute_type", "execution_mode", "device_index", "async_worker")
                        if key in body
                    }
                    if options.get("execution_mode") == "CPU_TEST_ONLY":
                        raise ValueError("CPU_TEST_ONLY is only available to local tests and diagnostics.")
                    result = ASR_SERVICE.start(**options)
                elif self.path == "/asr/chunk": result = ASR_SERVICE.accept(body)
                elif self.path == "/asr/status": result = ASR_SERVICE.status()
                else: result = ASR_SERVICE.control(self.path.rsplit("/", 1)[-1])
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(json.dumps(result).encode())
            except Exception as exc:
                self.send_error(400, str(exc))
            return
        if self.path == "/report_diagnostics":
            try:
                post_data = self._read_body(1_048_576)
            except ValueError as exc:
                self.send_error(400, str(exc))
                return
            report_path = PROJECT_ROOT / "tools" / "avatar_viewer" / "diagnostics_result.txt"
            with open(report_path, "wb") as f:
                f.write(post_data)
            print(f"[HTTP] Received diagnostics report ({len(post_data)} bytes)")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/save_sign":
            try:
                payload = self._read_json_body(1_048_576)
                overwrite = self.headers.get("X-Overwrite-Sign") == "true"
                try:
                    target = save_sign_definition(PROJECT_ROOT / "signs", payload, allow_overwrite=overwrite)
                except FileExistsError:
                    self.send_error(409, "Sign already exists; explicitly confirm overwrite in the authoring UI.")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Saved {target.name}".encode())
                print(f"[HTTP] Saved authored sign: {target.name}")
            except (ValueError, json.JSONDecodeError) as exc:
                self.send_error(400, str(exc))
            except OSError as exc:
                self.send_error(500, f"Unable to save sign atomically: {exc}")
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
    extension_id = os.environ.get("SIGN_ALLOWED_EXTENSION_ID", "")
    if extension_id and not re.fullmatch(r"[a-p]{32}", extension_id):
        raise ValueError("SIGN_ALLOWED_EXTENSION_ID must be the exact 32-character Chrome extension ID.")
    selected_port = find_available_port(port)
    url = f"http://localhost:{selected_port}/tools/avatar_viewer/index.html"

    print("=" * 60)
    print("AETHER 3D AVATAR INSPECTION VIEWER (PHASE A)")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Server URL:   {url}")
    if not extension_id:
        print("Extension API access is disabled; pass --extension-id to allow one installed extension.")
    print("=" * 60)

    if open_browser:
        print("Launching browser...")
        webbrowser.open(url)

    handler = QuietSimpleHTTPRequestHandler
    with socketserver.ThreadingTCPServer(("127.0.0.1", selected_port), handler) as httpd:
        httpd.daemon_threads = True
        httpd.server_port = selected_port
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
    parser.add_argument(
        "--extension-id",
        default=os.environ.get("SIGN_ALLOWED_EXTENSION_ID", ""),
        help="Exact Chrome extension ID allowed to call the local API.",
    )
    args = parser.parse_args()

    if args.extension_id:
        if not re.fullmatch(r"[a-p]{32}", args.extension_id):
            parser.error("--extension-id must be the exact 32-character Chrome extension ID.")
        os.environ["SIGN_ALLOWED_EXTENSION_ID"] = args.extension_id
    run_viewer(port=args.port, open_browser=not args.no_browser)

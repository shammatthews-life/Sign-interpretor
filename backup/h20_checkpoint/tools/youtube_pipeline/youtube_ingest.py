"""YouTube Audio Ingestion & Transcription Pipeline (Phase H7).

Development-mode pipeline:
  YouTube URL
      ↓
  URL validation / ID extraction (Safe, structured parsing)
      ↓
  yt-dlp (Audio-only stream extraction)
      ↓
  FFmpeg (Convert to mono 16 kHz PCM WAV)
      ↓
  faster-whisper (Timestamped speech-to-text segments)
      ↓
  Controlled segmentation
      ↓
  EnglishToISLTranslator (G2/G3 rules & motion availability resolution)
      ↓
  Playable filter & SignScheduler contract

Security guarantees:
- Rejects non-YouTube domains.
- Passes all subprocess parameters as structured arrays (no arbitrary shell injection).
- Audio only; never downloads unneeded video streams.
- Preserves official visual evidence gate (zero fabricated gestures).
"""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
import urllib.parse
import wave
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from asr.streaming_asr import ensure_cuda_support

# Supported YouTube URL patterns
YOUTUBE_URL_PATTERNS = [
    re.compile(r"^https?://(?:www\.|m\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    re.compile(r"^https?://(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    re.compile(r"^https?://(?:www\.|m\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    re.compile(r"^https?://(?:www\.|m\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
]


def validate_youtube_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Validate YouTube URL and extract 11-char video ID.

    Returns:
        (is_valid, video_id, canonical_url)
    """
    if not url or not isinstance(url, str):
        return False, None, None

    trimmed = url.strip()
    try:
        parsed = urllib.parse.urlparse(trimmed)
    except Exception:
        return False, None, None

    # Check hostname
    hostname = (parsed.hostname or "").lower()
    allowed_hosts = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
    if hostname not in allowed_hosts:
        return False, None, None

    # Try regex matching
    for pattern in YOUTUBE_URL_PATTERNS:
        match = pattern.match(trimmed)
        if match:
            video_id = match.group(1)
            canonical = f"https://www.youtube.com/watch?v={video_id}"
            return True, video_id, canonical

    # Query param fallback for youtube.com
    if "youtube.com" in hostname and parsed.path in ("/watch", "/watch/"):
        qs = urllib.parse.parse_qs(parsed.query)
        if "v" in qs and qs["v"] and len(qs["v"][0]) == 11:
            video_id = qs["v"][0]
            canonical = f"https://www.youtube.com/watch?v={video_id}"
            return True, video_id, canonical

    return False, None, None


def get_ffmpeg_path() -> str:
    """Find FFmpeg binary on PATH or via imageio-ffmpeg."""
    path = shutil.which("ffmpeg")
    if path:
        return path

    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except ImportError:
        pass

    raise RuntimeError(
        "FFmpeg is not installed or discoverable on PATH. "
        "Please install FFmpeg or install imageio-ffmpeg via 'pip install imageio-ffmpeg'."
    )


def get_ytdlp_executor() -> Tuple[str, bool]:
    """Find yt-dlp binary or Python module.

    Returns:
        (executor_type, is_module)
    """
    try:
        import yt_dlp  # noqa: F401
        return "module", True
    except ImportError:
        pass

    cli = shutil.which("yt-dlp")
    if cli:
        return cli, False

    venv_cli = PROJECT_ROOT / ".venv" / "Scripts" / "yt-dlp.exe"
    if venv_cli.exists():
        return str(venv_cli), False

    raise RuntimeError(
        "yt-dlp is not installed. Please install it via 'pip install yt-dlp'."
    )


def download_youtube_audio(
    url: str,
    output_dir: Path,
    force: bool = False,
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """Download audio stream using yt-dlp and convert to mono 16 kHz PCM WAV via FFmpeg."""
    is_valid, video_id, canonical_url = validate_youtube_url(url)
    if not is_valid or not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    target_wav = output_dir / "audio_16k.wav"
    metadata_json = output_dir / "metadata.json"

    # Cache check
    if not force and target_wav.exists() and metadata_json.exists():
        try:
            with open(metadata_json, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if on_progress:
                on_progress("CACHE_HIT", 1.0)
            return {
                "cached": True,
                "video_id": video_id,
                "metadata": meta,
                "audio_path": str(target_wav),
            }
        except Exception:
            pass  # Corrupted cache; re-download

    ffmpeg_bin = get_ffmpeg_path()
    executor_type, is_module = get_ytdlp_executor()

    if on_progress:
        on_progress("EXTRACTING_METADATA", 0.1)

    t_start = time.perf_counter()
    metadata: Dict[str, Any] = {}

    if is_module:
        import yt_dlp

        # Find node runtime if present
        node_bin = shutil.which("node")
        js_runtimes = {"node": {}} if node_bin else {}

        ydl_opts: Dict[str, Any] = {
            "format": "bestaudio/best",
            "outtmpl": str(output_dir / f"source_{video_id}.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "js_runtimes": js_runtimes,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if on_progress:
                on_progress("DOWNLOADING", 0.3)
            info = ydl.extract_info(canonical_url, download=True)
            if not info:
                raise RuntimeError(f"yt-dlp could not retrieve info for: {canonical_url}")

            metadata = {
                "video_id": video_id,
                "title": info.get("title", ""),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "") or info.get("channel", ""),
                "channel_id": info.get("channel_id", ""),
                "upload_date": info.get("upload_date", ""),
                "view_count": info.get("view_count", 0),
                "description": (info.get("description", "") or "")[:500],
                "webpage_url": canonical_url,
            }
    else:
        # CLI invocation
        if on_progress:
            on_progress("DOWNLOADING", 0.3)

        out_template = str(output_dir / f"source_{video_id}.%(ext)s")
        cmd = [
            executor_type,
            "-f", "bestaudio/best",
            "--no-playlist",
            "--dump-json",
            "-o", out_template,
            canonical_url,
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        try:
            info = json.loads(proc.stdout)
            metadata = {
                "video_id": video_id,
                "title": info.get("title", ""),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "") or info.get("channel", ""),
                "channel_id": info.get("channel_id", ""),
                "upload_date": info.get("upload_date", ""),
                "view_count": info.get("view_count", 0),
                "description": (info.get("description", "") or "")[:500],
                "webpage_url": canonical_url,
            }
        except Exception:
            metadata = {
                "video_id": video_id,
                "title": f"YouTube video {video_id}",
                "duration": 0,
                "uploader": "Unknown",
                "webpage_url": canonical_url,
            }

    # Find the downloaded source audio file
    candidate_sources = glob.glob(str(output_dir / f"source_{video_id}.*"))
    if not candidate_sources:
        raise FileNotFoundError(f"Failed to find downloaded audio source in {output_dir}")
    source_file = candidate_sources[0]

    if on_progress:
        on_progress("EXTRACTING_AUDIO", 0.6)

    # Convert to mono 16000 Hz PCM WAV using FFmpeg
    conv_cmd = [
        ffmpeg_bin,
        "-y",
        "-i", str(source_file),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(target_wav),
    ]
    subprocess.run(conv_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    t_download_extract = time.perf_counter() - t_start

    # Verify WAV file specifications
    with wave.open(str(target_wav), "rb") as wf:
        channels = wf.getnchannels()
        rate = wf.getframerate()
        sampwidth = wf.getsampwidth()
        frames = wf.getnframes()
        audio_duration = frames / float(rate)

    if channels != 1 or rate != 16000 or sampwidth != 2:
        raise ValueError(
            f"Invalid WAV format: channels={channels} (expected 1), rate={rate} (expected 16000), "
            f"sampwidth={sampwidth} (expected 2)"
        )

    metadata.update({
        "download_extract_time_s": round(t_download_extract, 3),
        "audio_duration_s": round(audio_duration, 3),
        "sample_rate": rate,
        "channels": channels,
        "sample_width": sampwidth,
    })

    with open(metadata_json, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    if on_progress:
        on_progress("AUDIO_READY", 0.7)

    return {
        "cached": False,
        "video_id": video_id,
        "metadata": metadata,
        "audio_path": str(target_wav),
    }


def transcribe_audio_file(
    audio_path: Path,
    output_dir: Path,
    model_name: str = "base.en",
    device: Optional[str] = None,
    compute_type: Optional[str] = None,
    force: bool = False,
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """Transcribe 16 kHz WAV audio file using existing faster-whisper configuration."""
    output_dir = Path(output_dir)
    transcript_json = output_dir / "transcript.json"
    transcript_txt = output_dir / "transcript.txt"

    if not force and transcript_json.exists() and transcript_txt.exists():
        try:
            with open(transcript_json, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            if on_progress:
                on_progress("TRANSCRIBE_CACHE_HIT", 1.0)
            return cached_data
        except Exception:
            pass

    if on_progress:
        on_progress("TRANSCRIBING", 0.8)

    # Determine device and compute type
    if device is None:
        has_cuda = ensure_cuda_support()
        try:
            import ctranslate2
            has_cuda = has_cuda and (ctranslate2.get_cuda_device_count() > 0)
        except Exception:
            has_cuda = False
        device = "cuda" if has_cuda else "cpu"

    if compute_type is None:
        compute_type = "float16" if device == "cuda" else "int8"

    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device=device, compute_type=compute_type)

    t_start = time.perf_counter()
    segments_generator, info = model.transcribe(
        str(audio_path),
        language="en",
        beam_size=1,
        condition_on_previous_text=False,
        vad_filter=True,
    )

    segments_list = []
    full_text_parts = []
    for s in segments_generator:
        text = s.text.strip()
        if text:
            segments_list.append({
                "start": round(s.start, 2),
                "end": round(s.end, 2),
                "text": text,
            })
            full_text_parts.append(text)

    t_transcribe = time.perf_counter() - t_start
    audio_duration = getattr(info, "duration", 0.0)
    rtf = t_transcribe / max(0.001, audio_duration)

    result_data = {
        "model": model_name,
        "device": device,
        "compute_type": compute_type,
        "language": getattr(info, "language", "en"),
        "audio_duration_s": round(audio_duration, 3),
        "transcription_time_s": round(t_transcribe, 3),
        "rtf": round(rtf, 4),
        "segment_count": len(segments_list),
        "segments": segments_list,
        "full_text": " ".join(full_text_parts),
    }

    with open(transcript_json, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2)

    with open(transcript_txt, "w", encoding="utf-8") as f:
        f.write(result_data["full_text"] + "\n")

    return result_data


def segment_and_translate(
    transcript_data: Dict[str, Any],
    output_dir: Path,
    force: bool = False,
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """Pass transcript segments through existing EnglishToISLTranslator via Node bridge."""
    output_dir = Path(output_dir)
    translation_json = output_dir / "translation.json"

    if not force and translation_json.exists():
        try:
            with open(translation_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    if on_progress:
        on_progress("TRANSLATING", 0.9)

    segments = transcript_data.get("segments", [])
    bridge_script = PROJECT_ROOT / "tools" / "youtube_pipeline" / "translate_segments.mjs"

    t_start = time.perf_counter()
    node_bin = shutil.which("node") or "node"
    proc = subprocess.run(
        [node_bin, str(bridge_script)],
        input=json.dumps(segments),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    t_translate = time.perf_counter() - t_start

    translated_segments = json.loads(proc.stdout)

    # Calculate overall linguistic statistics
    all_glosses: List[str] = []
    all_playable: List[str] = []
    all_unavailable: List[Dict[str, str]] = []
    all_unknown: List[str] = []

    for seg in translated_segments:
        all_glosses.extend(seg.get("gloss", []))
        all_playable.extend(seg.get("playable_signs", []))
        all_unavailable.extend(seg.get("unavailable_concepts", []))
        all_unknown.extend(seg.get("unknown_terms", []))

    summary = {
        "translation_time_s": round(t_translate, 3),
        "total_segments": len(translated_segments),
        "total_concept_occurrences": len(all_glosses),
        "playable_concept_occurrences": len(all_playable),
        "unavailable_concept_occurrences": len(all_unavailable),
        "unknown_term_occurrences": len(all_unknown),
        "playable_signs_unique": sorted(list(set(all_playable))),
        "unavailable_signs_unique": sorted(list(set(item["sign_id"] for item in all_unavailable if "sign_id" in item))),
        "translated_segments": translated_segments,
    }

    with open(translation_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def process_youtube_video(
    url: str,
    output_base_dir: Optional[Path] = None,
    force: bool = False,
    model_name: str = "base.en",
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """End-to-end YouTube ingestion, ASR, and ISL translation pipeline."""
    t_start = time.perf_counter()
    is_valid, video_id, canonical_url = validate_youtube_url(url)
    if not is_valid or not video_id:
        raise ValueError(f"Invalid or unsupported YouTube URL: {url}")

    if output_base_dir is None:
        output_base_dir = PROJECT_ROOT / "runtime" / "youtube"

    video_dir = output_base_dir / video_id
    video_dir.mkdir(parents=True, exist_ok=True)

    pipeline_result_file = video_dir / "pipeline_result.json"
    if not force and pipeline_result_file.exists():
        try:
            with open(pipeline_result_file, "r", encoding="utf-8") as f:
                cached_res = json.load(f)
            if on_progress:
                on_progress("READY", 1.0)
            return cached_res
        except Exception:
            pass

    # 1. Download & Extract Audio
    audio_res = download_youtube_audio(canonical_url, video_dir, force=force, on_progress=on_progress)
    metadata = audio_res["metadata"]
    audio_path = Path(audio_res["audio_path"])

    # 2. Transcribe Audio
    transcript_res = transcribe_audio_file(
        audio_path,
        video_dir,
        model_name=model_name,
        force=force,
        on_progress=on_progress,
    )

    # 3. Translate Segments
    translation_res = segment_and_translate(
        transcript_res,
        video_dir,
        force=force,
        on_progress=on_progress,
    )

    t_total = time.perf_counter() - t_start

    final_result = {
        "status": "READY",
        "video_id": video_id,
        "url": canonical_url,
        "metadata": metadata,
        "audio_path": str(audio_path),
        "transcript": transcript_res,
        "translation": translation_res,
        "timings": {
            "download_extract_s": metadata.get("download_extract_time_s", 0.0),
            "transcription_s": transcript_res.get("transcription_time_s", 0.0),
            "translation_s": translation_res.get("translation_time_s", 0.0),
            "total_processing_s": round(t_total, 3),
            "rtf": transcript_res.get("rtf", 0.0),
        },
    }

    with open(pipeline_result_file, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)

    if on_progress:
        on_progress("READY", 1.0)

    return final_result


class YouTubeJobManager:
    """Thread-safe background job runner for development HTTP endpoints."""

    def __init__(self, output_base_dir: Optional[Path] = None):
        self.output_base_dir = output_base_dir or (PROJECT_ROOT / "runtime" / "youtube")
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def submit_job(self, url: str, force: bool = False, model_name: str = "base.en") -> str:
        is_valid, video_id, canonical_url = validate_youtube_url(url)
        if not is_valid or not video_id:
            raise ValueError(f"Invalid YouTube URL: {url}")

        job_id = f"yt_{video_id}_{uuid.uuid4().hex[:12]}"
        with self._lock:
            self.jobs[job_id] = {
                "job_id": job_id,
                "video_id": video_id,
                "url": canonical_url,
                "stage": "QUEUED",
                "progress": 0.0,
                "started_at": time.time(),
                "finished_at": None,
                "error": None,
                "result": None,
            }

        worker = threading.Thread(
            target=self._run_job,
            args=(job_id, canonical_url, force, model_name),
            daemon=True,
            name=f"YTJobWorker-{job_id}",
        )
        worker.start()
        return job_id

    def _run_job(self, job_id: str, url: str, force: bool, model_name: str):
        def update_progress(stage: str, progress: float):
            if stage == "READY":
                return
            normalized_stage = {
                "INITIALIZING": "QUEUED",
                "EXTRACTING_METADATA": "DOWNLOADING",
                "DOWNLOADING": "DOWNLOADING",
                "EXTRACTING_AUDIO": "EXTRACTING_AUDIO",
                "AUDIO_READY": "TRANSCRIBING",
                "TRANSCRIBING": "TRANSCRIBING",
                "TRANSCRIBE_CACHE_HIT": "TRANSLATING",
                "TRANSLATING": "TRANSLATING",
                "CACHE_HIT": "TRANSLATING",
            }.get(stage, stage)
            with self._lock:
                if job_id in self.jobs:
                    self.jobs[job_id]["stage"] = normalized_stage
                    self.jobs[job_id]["progress"] = progress

        try:
            update_progress("INITIALIZING", 0.05)
            result = process_youtube_video(
                url,
                output_base_dir=self.output_base_dir,
                force=force,
                model_name=model_name,
                on_progress=update_progress,
            )
            with self._lock:
                self.jobs[job_id]["stage"] = "READY"
                self.jobs[job_id]["progress"] = 1.0
                self.jobs[job_id]["finished_at"] = time.time()
                self.jobs[job_id]["result"] = result
        except Exception as exc:
            with self._lock:
                self.jobs[job_id]["stage"] = "ERROR"
                self.jobs[job_id]["finished_at"] = time.time()
                self.jobs[job_id]["error"] = str(exc)

    def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                return None
            return {
                "job_id": job["job_id"],
                "video_id": job["video_id"],
                "url": job["url"],
                "stage": job["stage"],
                "progress": job["progress"],
                "started_at": job["started_at"],
                "finished_at": job["finished_at"],
                "error": job["error"],
                "title": (job.get("result") or {}).get("metadata", {}).get("title"),
            }

    def get_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                return None
            return job.get("result")

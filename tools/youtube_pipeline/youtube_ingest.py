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
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import tempfile
import time
import uuid
import urllib.parse
import wave
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from asr.gpu_execution import (
    ExecutionMode,
    get_shared_whisper_model,
    resolve_execution_configuration,
)

# Supported YouTube URL patterns
YOUTUBE_URL_PATTERNS = [
    re.compile(r"^https?://(?:www\.|m\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    re.compile(r"^https?://(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    re.compile(r"^https?://(?:www\.|m\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
    re.compile(r"^https?://(?:www\.|m\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})", re.IGNORECASE),
]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _atomic_write_json(path: Path, value: Any) -> None:
    _atomic_write_text(path, json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def _package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "not-installed"


def _asr_implementation_identity() -> dict:
    return {
        "faster_whisper": _package_version("faster-whisper"),
        "ctranslate2": _package_version("ctranslate2"),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }


def _translation_implementation_hash() -> str:
    digest = hashlib.sha256()
    for path in (
        PROJECT_ROOT / "tools" / "youtube_pipeline" / "translate_segments.mjs",
        PROJECT_ROOT / "tools" / "avatar_viewer" / "EnglishToISLTranslator.js",
    ):
        digest.update(path.name.encode("utf-8"))
        digest.update(bytes.fromhex(_sha256_file(path)))
    signs_dir = PROJECT_ROOT / "signs"
    for path in sorted(signs_dir.glob("*.json")):
        digest.update(path.name.encode("utf-8"))
        digest.update(bytes.fromhex(_sha256_file(path)))
    return digest.hexdigest()


def _translation_cache_identity(transcript_data: Dict[str, Any]) -> str:
    identity_data = {
        "segments": transcript_data.get("segments"),
        "implementation_sha256": _translation_implementation_hash(),
    }
    return hashlib.sha256(
        json.dumps(identity_data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _transcript_content_hash(transcript_data: Any) -> Optional[str]:
    if (
        not isinstance(transcript_data, dict)
        or not isinstance(transcript_data.get("segments"), list)
        or not isinstance(transcript_data.get("full_text"), str)
    ):
        return None
    content = {"segments": transcript_data["segments"], "full_text": transcript_data["full_text"]}
    return hashlib.sha256(
        json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


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
            actual_hash = _sha256_file(target_wav)
            with wave.open(str(target_wav), "rb") as wf:
                valid_audio = (
                    wf.getnchannels() == 1
                    and wf.getframerate() == 16000
                    and wf.getsampwidth() == 2
                    and wf.getnframes() > 0
                )
            if (
                isinstance(meta, dict)
                and meta.get("video_id") == video_id
                and meta.get("audio_sha256") == actual_hash
                and valid_audio
            ):
                if on_progress:
                    on_progress("CACHE_HIT", 1.0)
                return {
                    "cached": True,
                    "video_id": video_id,
                    "metadata": meta,
                    "audio_path": str(target_wav),
                }
            print(f"[YouTube Audio] Ignoring audio cache with mismatched content identity: {target_wav}", file=sys.stderr)
        except (OSError, json.JSONDecodeError, wave.Error) as exc:
            print(f"[YouTube Audio] Ignoring unreadable audio cache {target_wav}: {exc}", file=sys.stderr)

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
    converted_wav = output_dir / f".audio_16k.{uuid.uuid4().hex}.tmp.wav"
    conv_cmd = [
        ffmpeg_bin,
        "-y",
        "-i", str(source_file),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(converted_wav),
    ]
    try:
        subprocess.run(conv_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        t_download_extract = time.perf_counter() - t_start

        # Verify WAV file specifications before publishing the cache file.
        with wave.open(str(converted_wav), "rb") as wf:
            channels = wf.getnchannels()
            rate = wf.getframerate()
            sampwidth = wf.getsampwidth()
            frames = wf.getnframes()
            audio_duration = frames / float(rate)

        if channels != 1 or rate != 16000 or sampwidth != 2 or frames <= 0:
            raise ValueError(
                f"Invalid WAV format: channels={channels} (expected 1), rate={rate} (expected 16000), "
                f"sampwidth={sampwidth} (expected 2), frames={frames} (expected > 0)"
            )
        os.replace(converted_wav, target_wav)
    finally:
        converted_wav.unlink(missing_ok=True)

    metadata.update({
        "download_extract_time_s": round(t_download_extract, 3),
        "audio_duration_s": round(audio_duration, 3),
        "sample_rate": rate,
        "channels": channels,
        "sample_width": sampwidth,
        "audio_sha256": _sha256_file(target_wav),
    })

    _atomic_write_json(metadata_json, metadata)

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
    execution_mode: ExecutionMode = "GPU_REQUIRED",
    device_index: int = 0,
    force: bool = False,
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """Transcribe 16 kHz WAV audio file using existing faster-whisper configuration."""
    output_dir = Path(output_dir)
    transcript_json = output_dir / "transcript.json"
    transcript_txt = output_dir / "transcript.txt"

    resolved = resolve_execution_configuration(
        execution_mode,
        device=device,
        device_index=device_index,
        compute_type=compute_type,
    )
    device = resolved["device"]
    compute_type = resolved["compute_type"]
    resolved_device_index = resolved["device_index"]
    audio_sha256 = _sha256_file(Path(audio_path))
    asr_implementation = _asr_implementation_identity()

    if not force and transcript_json.exists() and transcript_txt.exists():
        try:
            with open(transcript_json, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            cached_text = transcript_txt.read_text(encoding="utf-8")
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"[YouTube ASR] Ignoring unreadable transcript cache {transcript_json}: {exc}", file=sys.stderr)
        else:
            expected_cache_metadata = {
                "model": model_name,
                "device": device,
                "device_index": resolved_device_index,
                "compute_type": compute_type,
                "execution_mode": execution_mode,
                "audio_sha256": audio_sha256,
                "asr_implementation": asr_implementation,
            }
            cache_matches = (
                isinstance(cached_data, dict)
                and all(cached_data.get(key) == value for key, value in expected_cache_metadata.items())
                and isinstance(cached_data.get("segments"), list)
                and isinstance(cached_data.get("full_text"), str)
                and cached_text == cached_data.get("full_text", "") + "\n"
            )
            if cache_matches:
                if on_progress:
                    on_progress("TRANSCRIBE_CACHE_HIT", 1.0)
                return cached_data
            print(
                f"[YouTube ASR] Ignoring transcript cache with mismatched execution provenance: {transcript_json}",
                file=sys.stderr,
            )

    if on_progress:
        on_progress("TRANSCRIBING", 0.8)

    model, inference_lock = get_shared_whisper_model(
        model_name,
        device=device,
        compute_type=compute_type,
        device_index=resolved_device_index,
    )

    t_start = time.perf_counter()
    segments_list = []
    full_text_parts = []
    with inference_lock:
        segments_generator, info = model.transcribe(
            str(audio_path),
            language="en",
            beam_size=1,
            condition_on_previous_text=False,
            vad_filter=True,
        )
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
        "device_index": resolved_device_index,
        "compute_type": compute_type,
        "execution_mode": execution_mode,
        "fallback_reason": resolved["fallback_reason"],
        "audio_sha256": audio_sha256,
        "asr_implementation": asr_implementation,
        "language": getattr(info, "language", "en"),
        "audio_duration_s": round(audio_duration, 3),
        "transcription_time_s": round(t_transcribe, 3),
        "rtf": round(rtf, 4),
        "segment_count": len(segments_list),
        "segments": segments_list,
        "full_text": " ".join(full_text_parts),
    }

    _atomic_write_json(transcript_json, result_data)
    _atomic_write_text(transcript_txt, result_data["full_text"] + "\n")

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
    cache_identity = _translation_cache_identity(transcript_data)

    if not force and translation_json.exists():
        try:
            with open(translation_json, "r", encoding="utf-8") as f:
                cached_translation = json.load(f)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"[YouTube Translation] Ignoring unreadable cache {translation_json}: {exc}", file=sys.stderr)
        else:
            if (
                isinstance(cached_translation, dict)
                and cached_translation.get("cache_identity") == cache_identity
                and isinstance(cached_translation.get("translated_segments"), list)
            ):
                return cached_translation
            print(f"[YouTube Translation] Ignoring cache with mismatched content identity: {translation_json}", file=sys.stderr)

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
        "cache_identity": cache_identity,
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

    _atomic_write_json(translation_json, summary)

    return summary


def process_youtube_video(
    url: str,
    output_base_dir: Optional[Path] = None,
    force: bool = False,
    model_name: str = "base.en",
    execution_mode: ExecutionMode = "GPU_REQUIRED",
    device_index: int = 0,
    on_progress: Optional[Callable[[str, float], None]] = None,
) -> Dict[str, Any]:
    """End-to-end YouTube ingestion, ASR, and ISL translation pipeline."""
    t_start = time.perf_counter()
    is_valid, video_id, canonical_url = validate_youtube_url(url)
    if not is_valid or not video_id:
        raise ValueError(f"Invalid or unsupported YouTube URL: {url}")

    if output_base_dir is None:
        output_base_dir = PROJECT_ROOT / "runtime" / "youtube"

    resolved = resolve_execution_configuration(
        execution_mode,
        device_index=device_index,
    )
    video_dir = output_base_dir / video_id
    video_dir.mkdir(parents=True, exist_ok=True)

    pipeline_result_file = video_dir / "pipeline_result.json"
    audio_cache_path = video_dir / "audio_16k.wav"
    audio_metadata_path = video_dir / "metadata.json"
    cached_audio_sha256 = None
    try:
        audio_metadata = json.loads(audio_metadata_path.read_text(encoding="utf-8"))
        with wave.open(str(audio_cache_path), "rb") as wf:
            valid_audio = (
                wf.getnchannels() == 1
                and wf.getframerate() == 16000
                and wf.getsampwidth() == 2
                and wf.getnframes() > 0
            )
        actual_audio_sha256 = _sha256_file(audio_cache_path)
        if (
            valid_audio
            and isinstance(audio_metadata, dict)
            and audio_metadata.get("video_id") == video_id
            and audio_metadata.get("audio_sha256") == actual_audio_sha256
        ):
            cached_audio_sha256 = actual_audio_sha256
        else:
            print(f"[YouTube Pipeline] Ignoring audio cache with mismatched content identity: {audio_cache_path}", file=sys.stderr)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError, wave.Error) as exc:
        print(f"[YouTube Pipeline] Audio cache cannot be verified: {exc}", file=sys.stderr)

    if not force and pipeline_result_file.exists():
        try:
            with open(pipeline_result_file, "r", encoding="utf-8") as f:
                cached_res = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[YouTube Pipeline] Ignoring unreadable result cache {pipeline_result_file}: {exc}", file=sys.stderr)
        else:
            cached_transcript = cached_res.get("transcript") if isinstance(cached_res, dict) else None
            transcript_cache_file = video_dir / "transcript.json"
            transcript_cache = None
            transcript_text_matches = False
            if cached_audio_sha256 and transcript_cache_file.exists():
                try:
                    transcript_cache = json.loads(transcript_cache_file.read_text(encoding="utf-8"))
                    transcript_text_matches = (
                        isinstance(transcript_cache, dict)
                        and isinstance(transcript_cache.get("full_text"), str)
                        and (video_dir / "transcript.txt").read_text(encoding="utf-8")
                        == transcript_cache.get("full_text", "") + "\n"
                    )
                except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                    print(f"[YouTube Pipeline] Ignoring unreadable transcript identity {transcript_cache_file}: {exc}", file=sys.stderr)
            expected_cache_metadata = {
                "model": model_name,
                "device": resolved["device"],
                "device_index": resolved["device_index"],
                "compute_type": resolved["compute_type"],
                "execution_mode": execution_mode,
                "audio_sha256": cached_audio_sha256,
                "asr_implementation": _asr_implementation_identity(),
            }
            transcript_identity = _transcript_content_hash(transcript_cache)
            if not transcript_text_matches or not isinstance(transcript_cache, dict) or transcript_cache.get("audio_sha256") != cached_audio_sha256:
                transcript_identity = None
            expected_provenance = {
                **expected_cache_metadata,
                "transcript_sha256": transcript_identity,
                "translation_identity": _translation_cache_identity(transcript_cache) if transcript_identity else None,
            }
            cache_matches = (
                isinstance(cached_res, dict)
                and isinstance(cached_transcript, dict)
                and all(cached_transcript.get(key) == value for key, value in expected_cache_metadata.items())
                and _transcript_content_hash(cached_transcript) == transcript_identity
                and isinstance(cached_res.get("cache_provenance"), dict)
                and cached_res["cache_provenance"] == expected_provenance
                and isinstance(cached_res.get("translation"), dict)
                and cached_res["translation"].get("cache_identity") == expected_provenance["translation_identity"]
            )
            if cache_matches:
                if on_progress:
                    on_progress("READY", 1.0)
                return cached_res
            print(
                f"[YouTube Pipeline] Ignoring result cache with mismatched execution provenance: {pipeline_result_file}",
                file=sys.stderr,
            )

    # 1. Download & Extract Audio
    audio_res = download_youtube_audio(canonical_url, video_dir, force=force, on_progress=on_progress)
    metadata = audio_res["metadata"]
    audio_path = Path(audio_res["audio_path"])

    # 2. Transcribe Audio
    transcript_res = transcribe_audio_file(
        audio_path,
        video_dir,
        model_name=model_name,
        execution_mode=execution_mode,
        device_index=device_index,
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
    audio_sha256 = metadata.get("audio_sha256") or _sha256_file(audio_path)
    if not isinstance(transcript_res.get("segments"), list) or not isinstance(transcript_res.get("full_text"), str):
        raise ValueError("ASR result must include a segments list and full_text string before translation.")
    transcript_identity = _transcript_content_hash(transcript_res)
    if transcript_identity is None:
        raise ValueError("ASR result could not be assigned a stable transcript content identity.")
    cache_provenance = {
        "model": model_name,
        "device": resolved["device"],
        "device_index": resolved["device_index"],
        "compute_type": resolved["compute_type"],
        "execution_mode": execution_mode,
        "audio_sha256": audio_sha256,
        "asr_implementation": transcript_res.get("asr_implementation"),
        "transcript_sha256": transcript_identity,
        "translation_identity": _translation_cache_identity(transcript_res),
    }

    t_total = time.perf_counter() - t_start

    final_result = {
        "status": "READY",
        "video_id": video_id,
        "url": canonical_url,
        "metadata": metadata,
        "audio_path": str(audio_path),
        "cache_provenance": cache_provenance,
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

    _atomic_write_json(pipeline_result_file, final_result)

    if on_progress:
        on_progress("READY", 1.0)

    return final_result


class YouTubeJobManager:
    """Thread-safe background job runner for development HTTP endpoints."""

    JOB_HISTORY_LIMIT = 100
    ACTIVE_JOB_LIMIT = 2

    def __init__(self, output_base_dir: Optional[Path] = None):
        self.output_base_dir = output_base_dir or (PROJECT_ROOT / "runtime" / "youtube")
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._active_video_jobs: Dict[str, str] = {}

    def _prune_jobs_locked(self) -> None:
        completed = sorted(
            (
                (job.get("finished_at") or job.get("started_at") or 0, job_id)
                for job_id, job in self.jobs.items()
                if job["stage"] in ("READY", "ERROR")
            )
        )
        while len(completed) > self.JOB_HISTORY_LIMIT:
            _finished_at, job_id = completed.pop(0)
            self.jobs.pop(job_id, None)

    def submit_job(self, url: str, force: bool = False, model_name: str = "base.en") -> str:
        is_valid, video_id, canonical_url = validate_youtube_url(url)
        if not is_valid or not video_id:
            raise ValueError(f"Invalid YouTube URL: {url}")

        with self._lock:
            self._prune_jobs_locked()
            active_job_id = self._active_video_jobs.get(video_id)
            if active_job_id and self.jobs[active_job_id]["stage"] not in ("READY", "ERROR"):
                return active_job_id
            if len(self._active_video_jobs) >= self.ACTIVE_JOB_LIMIT:
                raise RuntimeError(f"YouTube processing is at its {self.ACTIVE_JOB_LIMIT}-job concurrency limit.")

            job_id = f"yt_{video_id}_{uuid.uuid4().hex[:12]}"
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
                "result_path": str(self.output_base_dir / "jobs" / job_id / "result.json"),
                "title": None,
            }
            self._active_video_jobs[video_id] = job_id

        worker = threading.Thread(
            target=self._run_job,
            args=(job_id, canonical_url, force, model_name),
            daemon=True,
            name=f"YTJobWorker-{job_id}",
        )
        try:
            worker.start()
        except Exception as exc:
            with self._lock:
                self.jobs[job_id]["stage"] = "ERROR"
                self.jobs[job_id]["finished_at"] = time.time()
                self.jobs[job_id]["error"] = f"Unable to start YouTube worker: {exc}"
                self._active_video_jobs.pop(video_id, None)
                self._prune_jobs_locked()
            raise RuntimeError(f"Unable to start YouTube processing worker: {exc}") from exc
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
            result_path = Path(self.jobs[job_id]["result_path"])
            _atomic_write_json(result_path, result)
            with self._lock:
                self.jobs[job_id]["stage"] = "READY"
                self.jobs[job_id]["progress"] = 1.0
                self.jobs[job_id]["finished_at"] = time.time()
                self.jobs[job_id]["result"] = None
                self.jobs[job_id]["title"] = (result.get("metadata") or {}).get("title")
                self._active_video_jobs.pop(self.jobs[job_id]["video_id"], None)
                self._prune_jobs_locked()
        except Exception as exc:
            with self._lock:
                self.jobs[job_id]["stage"] = "ERROR"
                self.jobs[job_id]["finished_at"] = time.time()
                self.jobs[job_id]["error"] = str(exc)
                self._active_video_jobs.pop(self.jobs[job_id]["video_id"], None)
                self._prune_jobs_locked()

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
                "title": job.get("title"),
            }

    def get_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            job = self.jobs.get(job_id)
            if job and job["stage"] != "READY":
                return None
            if job:
                result_path = Path(job["result_path"])
            else:
                match = re.fullmatch(r"yt_[A-Za-z0-9_-]{11}_[a-f0-9]{12}", job_id)
                if not match:
                    return None
                result_path = self.output_base_dir / "jobs" / job_id / "result.json"
        if not result_path.exists():
            return None
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"[YouTube Jobs] Unable to read durable result {result_path}: {exc}", file=sys.stderr)
            return None
        if not isinstance(result, dict):
            raise ValueError(f"Durable result {result_path} must contain a JSON object.")
        return result

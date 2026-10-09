"""Generate repeatable local WAV fixtures using Windows' installed SAPI voice.

Fixtures are intentionally synthetic diagnostics, not a representative accent
benchmark. They avoid distributing third-party voice recordings.
"""
from __future__ import annotations

import subprocess
import requests
import wave
from pathlib import Path
import numpy as np

REFERENCE = "And so my fellow Americans ask not what your country can do for you ask what you can do for your country."
SHORT_REFERENCE = "And so my fellow Americans ask not what your country can do for you."
SOURCE_URL = "https://raw.githubusercontent.com/ggerganov/whisper.cpp/master/samples/jfk.wav"


def _speak_to_wav(text: str, rate: int, output: Path) -> None:
    escaped_text = text.replace("'", "''")
    escaped_path = str(output.resolve()).replace("'", "''")
    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$speaker.Rate = {rate}; "
        f"$speaker.SetOutputToWaveFile('{escaped_path}'); "
        f"$speaker.Speak('{escaped_text}'); $speaker.Dispose()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", command], check=True, capture_output=True, text=True)


def _download_source(target: Path) -> None:
    response = requests.get(SOURCE_URL, timeout=60)
    response.raise_for_status()
    target.write_bytes(response.content)


def _read_pcm(source: Path) -> tuple[wave._wave_params, np.ndarray]:
    with wave.open(str(source), "rb") as reader:
        params = reader.getparams()
        raw = reader.readframes(reader.getnframes())
    if params.sampwidth != 2 or params.nchannels != 1:
        raise ValueError("Benchmark WAV must be mono 16-bit PCM.")
    return params, np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0


def _write_pcm(target: Path, params: wave._wave_params, samples: np.ndarray) -> None:
    with wave.open(str(target), "wb") as writer:
        writer.setparams(params)
        writer.writeframes((np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes())


def _make_noisy(source: Path, target: Path) -> None:
    params, samples = _read_pcm(source)
    rng = np.random.default_rng(20261006)
    noisy = np.clip(samples + rng.normal(0, 0.012, len(samples)), -1, 1)
    _write_pcm(target, params, noisy)


def ensure_fixtures(output_dir: Path) -> dict[str, tuple[Path, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    normal = output_dir / "normal.wav"
    if not normal.exists(): _download_source(normal)
    params, samples = _read_pcm(normal)
    short = output_dir / "short.wav"
    if not short.exists(): _write_pcm(short, params, samples[: round(params.framerate * 6.3)])
    fast = output_dir / "fast.wav"
    if not fast.exists(): _write_pcm(fast, params, samples[::2])
    pause_rich = output_dir / "pause_rich.wav"
    if not pause_rich.exists():
        midpoint = len(samples) // 2
        _write_pcm(pause_rich, params, np.concatenate((samples[:midpoint], np.zeros(params.framerate), samples[midpoint:])))
    fixtures: dict[str, tuple[Path, str]] = {
        "short": (short, SHORT_REFERENCE), "normal": (normal, REFERENCE),
        "fast": (fast, REFERENCE), "pause_rich": (pause_rich, REFERENCE),
    }
    noisy_path = output_dir / "mild_noisy.wav"
    if not noisy_path.exists(): _make_noisy(fixtures["normal"][0], noisy_path)
    fixtures["mild_noisy"] = (noisy_path, REFERENCE)
    return fixtures


if __name__ == "__main__":
    fixtures = ensure_fixtures(Path(__file__).resolve().parent / "benchmark_audio")
    for name, (path, transcript) in fixtures.items(): print(f"{name}: {path.name} — {transcript}")

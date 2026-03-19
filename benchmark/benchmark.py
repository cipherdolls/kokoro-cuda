"""Benchmark and validation for Kokoro TTS.

Generates TTS audio files across multiple formats, measures latency/throughput,
and optionally validates content accuracy using a Whisper ASR service.

Usage:
    python benchmark.py                                    # TTS benchmark only
    python benchmark.py --whisper http://localhost:9000     # + Whisper validation
    python benchmark.py --save-report                      # write BENCHMARK.md
    python benchmark.py --formats wav mp3 opus flac        # test specific formats
"""

import argparse
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher

import requests

KOKORO_DEFAULT = "http://localhost:8880"
WHISPER_DEFAULT = "http://localhost:9000"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "benchmark_output")

ALL_FORMATS = ["wav", "mp3", "opus", "flac", "pcm"]
DEFAULT_RUNS = 3

TEST_CASES = [
    {
        "name": "short",
        "input": "Hello, this is a test.",
    },
    {
        "name": "medium",
        "input": "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet.",
    },
    {
        "name": "long",
        "input": (
            "Artificial intelligence has transformed the way we interact with technology. "
            "From voice assistants to self-driving cars, machine learning models are becoming "
            "an integral part of our daily lives. Text to speech synthesis is one of the most "
            "exciting applications, enabling natural sounding voice generation from written text."
        ),
    },
    {
        "name": "numbers",
        "input": "There are 7 continents, 195 countries, and over 8 billion people on Earth.",
    },
    {
        "name": "punctuation",
        "input": "Wait, what? Are you serious! That's incredible... I can't believe it.",
    },
    {
        "name": "very_long",
        "input": (
            "In the early morning hours, the city slowly comes to life. Street vendors set up their carts "
            "along the busy avenues, while commuters rush to catch the first trains of the day. The smell "
            "of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere "
            "in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries old oven, "
            "continuing a tradition passed down through generations. Meanwhile, across town, a young "
            "engineer sits at her desk, reviewing lines of code that will power a new artificial "
            "intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea "
            "and smiles, knowing that her work could save thousands of lives in the years to come. "
            "Outside her window, the sun begins to rise over the skyline, casting long shadows across "
            "the rooftops and painting the clouds in shades of orange and gold. It is going to be a "
            "beautiful day."
        ),
    },
]


def detect_gpu() -> str:
    """Detect GPU via nvidia-smi."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version,compute_cap",
             "--format=csv,noheader"],
            text=True, timeout=5,
        ).strip()
        return out
    except Exception:
        return "unknown"


def gpu_dir_name(gpu_info: str) -> str:
    """Convert GPU info to a directory name, e.g. 'NVIDIAGeForceRTX5090'."""
    gpu_name = gpu_info.split(",")[0].strip() if gpu_info != "unknown" else "unknown"
    return "".join(c for c in gpu_name if c.isalnum())


@dataclass
class Result:
    name: str
    input_text: str
    format: str
    bitrate: str = ""
    runs: int = 1
    duration_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    all_durations: list = None
    file_size: int = 0
    file_path: str = ""
    whisper_text: str = ""
    similarity: float = 0.0
    whisper_duration_ms: float = 0.0
    error: str = ""

    def __post_init__(self):
        if self.all_durations is None:
            self.all_durations = []


def tts_request(
    kokoro_url: str,
    text: str,
    voice: str,
    fmt: str,
    bitrate: str,
    output_path: str,
) -> tuple[float, int]:
    """Send TTS request, save audio, return (duration_ms, file_size)."""
    start = time.perf_counter()
    resp = requests.post(
        f"{kokoro_url}/v1/audio/speech",
        json={
            "input": text,
            "voice": voice,
            "response_format": fmt,
            "bitrate": bitrate,
        },
        stream=True,
    )
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    duration_ms = (time.perf_counter() - start) * 1000
    file_size = os.path.getsize(output_path)
    return duration_ms, file_size


def whisper_transcribe(whisper_url: str, audio_path: str) -> tuple[str, float]:
    """Transcribe audio file via Whisper, return (text, duration_ms)."""
    start = time.perf_counter()
    with open(audio_path, "rb") as f:
        resp = requests.post(
            f"{whisper_url}/asr",
            files={"audio_file": (os.path.basename(audio_path), f)},
            params={"output": "json", "language": "en"},
        )
    resp.raise_for_status()
    duration_ms = (time.perf_counter() - start) * 1000
    return resp.json()["text"], duration_ms


def text_similarity(a: str, b: str) -> float:
    """Normalized similarity between two strings (0.0 - 1.0)."""
    a = a.lower().strip()
    b = b.lower().strip()
    return SequenceMatcher(None, a, b).ratio()


def run_format_benchmark(
    kokoro_url: str,
    whisper_url: str | None,
    voice: str,
    fmt: str,
    bitrate: str,
    base_dir: str = OUTPUT_DIR,
    runs: int = DEFAULT_RUNS,
) -> list[Result]:
    """Run all test cases for a single format, repeating each N times for averaging."""
    fmt_dir = os.path.join(base_dir, fmt)
    os.makedirs(fmt_dir, exist_ok=True)
    results = []

    for tc in TEST_CASES:
        result = Result(name=tc["name"], input_text=tc["input"], format=fmt, bitrate=bitrate, runs=runs)
        output_path = os.path.join(fmt_dir, f"{tc['name']}.{fmt}")

        try:
            durations = []
            for i in range(runs):
                dur, size = tts_request(
                    kokoro_url, tc["input"], voice, fmt, bitrate, output_path
                )
                durations.append(dur)
                result.file_size = size  # last run's size (same each time)

            result.all_durations = durations
            result.duration_ms = sum(durations) / len(durations)
            result.min_ms = min(durations)
            result.max_ms = max(durations)
            result.file_path = output_path
        except Exception as e:
            result.error = str(e)
            results.append(result)
            continue

        # Whisper validation (skip pcm — Whisper can't read raw PCM)
        if whisper_url and fmt != "pcm":
            try:
                result.whisper_text, result.whisper_duration_ms = whisper_transcribe(
                    whisper_url, output_path
                )
                result.similarity = text_similarity(tc["input"], result.whisper_text)
            except Exception as e:
                result.error = f"ASR: {e}"

        results.append(result)

    return results


def run_benchmark(
    kokoro_url: str,
    whisper_url: str | None,
    voice: str,
    formats: list[str],
    bitrate: str,
    runs: int = DEFAULT_RUNS,
    save_report: bool = False,
) -> dict[str, list[Result]]:
    all_results: dict[str, list[Result]] = {}

    # GPU detection
    gpu_info = detect_gpu()
    print(f"GPU: {gpu_info}")

    # Create GPU-named output directory
    gpu_dir = os.path.join(OUTPUT_DIR, gpu_dir_name(gpu_info))
    os.makedirs(gpu_dir, exist_ok=True)

    # Health checks
    try:
        r = requests.get(f"{kokoro_url}/health")
        r.raise_for_status()
        kokoro_health = r.json()
        print(f"Kokoro health: {kokoro_health}")
    except Exception as e:
        print(f"ERROR: Kokoro not reachable at {kokoro_url}: {e}")
        return all_results

    whisper_health = None
    if whisper_url:
        try:
            r = requests.get(f"{whisper_url}/health")
            r.raise_for_status()
            whisper_health = r.json()
            print(f"Whisper health: {whisper_health}")
        except Exception as e:
            print(f"WARNING: Whisper not reachable at {whisper_url}: {e}")
            whisper_url = None

    # Run each format
    for fmt in formats:
        print(f"\n{'='*70}")
        print(f"Format: {fmt} (bitrate={bitrate}, voice={voice}, runs={runs})")
        print(f"{'='*70}")
        print(f"{'Test':<15} {'Avg ms':>8} {'Min ms':>8} {'Max ms':>8} {'Size':>10} {'Similarity':>11} {'Status'}")
        print("-" * 78)

        results = run_format_benchmark(kokoro_url, whisper_url, voice, fmt, bitrate, gpu_dir, runs)
        all_results[fmt] = results

        for r in results:
            if r.error and not r.file_path:
                print(f"{r.name:<15} {'ERROR':>8}   {r.error}")
                continue

            size_str = f"{r.file_size / 1024:.1f}KB"
            has_whisper = whisper_url and fmt != "pcm"
            sim_str = f"{r.similarity:.2f}" if has_whisper else "-"

            if has_whisper:
                status = f"{r.similarity:.0%}" + (" PASS" if r.similarity > 0.7 else " FAIL")
            else:
                status = "OK"

            print(f"{r.name:<15} {r.duration_ms:>7.0f}ms {r.min_ms:>7.0f}ms {r.max_ms:>7.0f}ms {size_str:>10} {sim_str:>10}  {status}")

        # Format summary
        successful = [r for r in results if not r.error or r.file_path]
        if successful:
            avg_tts = sum(r.duration_ms for r in successful) / len(successful)
            total_size = sum(r.file_size for r in successful)
            print(f"\n  Avg latency: {avg_tts:.0f}ms | Total size: {total_size / 1024:.1f}KB")

    # Overall summary
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")

    print(f"\n{'Format':<10} {'Avg Latency':>12} {'Avg Size':>10} {'Avg Similarity':>15}")
    print("-" * 50)

    for fmt, results in all_results.items():
        successful = [r for r in results if not r.error or r.file_path]
        if not successful:
            continue
        avg_tts = sum(r.duration_ms for r in successful) / len(successful)
        avg_size = sum(r.file_size for r in successful) / len(successful)
        has_whisper = whisper_url and fmt != "pcm"
        if has_whisper:
            avg_sim = sum(r.similarity for r in successful) / len(successful)
            sim_str = f"{avg_sim:.2%}"
        else:
            sim_str = "-"
        print(f"{fmt:<10} {avg_tts:>10.0f}ms {avg_size / 1024:>9.1f}KB {sim_str:>14}")

    # Detailed whisper comparison (use wav results as reference)
    if whisper_url and "wav" in all_results:
        print(f"\n--- Whisper Transcription Details (wav) ---")
        for r in all_results["wav"]:
            if r.whisper_text:
                print(f"\n[{r.name}]")
                print(f"  Expected: {r.input_text}")
                print(f"  Got:      {r.whisper_text}")
                print(f"  Match:    {r.similarity:.2%}")

    # Save report
    if save_report:
        report = generate_report(
            gpu_info=gpu_info,
            all_results=all_results,
            bitrate=bitrate,
            voice=voice,
            runs=runs,
            whisper_health=whisper_health,
            has_whisper=whisper_url is not None,
        )
        report_path = os.path.join(gpu_dir, "report.md")
        with open(report_path, "w") as f:
            f.write(report)
        print(f"\nReport saved:    {os.path.abspath(report_path)}")

    return all_results


def generate_report(
    gpu_info: str,
    all_results: dict[str, list[Result]],
    bitrate: str,
    voice: str,
    runs: int,
    whisper_health: dict | None,
    has_whisper: bool,
) -> str:
    """Generate a markdown benchmark report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Parse GPU fields
    gpu_parts = [p.strip() for p in gpu_info.split(",")] if gpu_info != "unknown" else []
    gpu_name = gpu_parts[0] if gpu_parts else "unknown"
    gpu_mem = gpu_parts[1] if len(gpu_parts) > 1 else ""
    gpu_driver = gpu_parts[2] if len(gpu_parts) > 2 else ""
    gpu_compute = gpu_parts[3] if len(gpu_parts) > 3 else ""

    lines = [
        "# Kokoro TTS Benchmark Results",
        "",
        f"**Date:** {now}",
        "",
        "## Hardware",
        "",
        "| Property | Value |",
        "|----------|-------|",
        f"| GPU | {gpu_name} |",
    ]
    if gpu_mem:
        lines.append(f"| VRAM | {gpu_mem} |")
    if gpu_driver:
        lines.append(f"| Driver | {gpu_driver} |")
    if gpu_compute:
        lines.append(f"| Compute Capability | {gpu_compute} |")

    lines += [
        "",
        "## Configuration",
        "",
        "| Setting | Value |",
        "|---------|-------|",
        f"| Model | Kokoro v1.0 (82M params) |",
        f"| Voice | {voice} |",
        f"| Formats Tested | {', '.join(all_results.keys())} |",
        f"| Bitrate (lossy) | {bitrate} |",
        f"| Sample Rate | 24000 Hz |",
        f"| Runs per test | {runs} |",
    ]
    if whisper_health:
        lines.append(f"| Whisper Model | {whisper_health.get('model', 'unknown')} |")

    # Format comparison
    lines += [
        "",
        "## Format Comparison",
        "",
        "| Format | Avg Latency | Avg File Size | Whisper Similarity |",
        "|--------|-------------|---------------|-------------------|",
    ]
    for fmt, results in all_results.items():
        successful = [r for r in results if not r.error or r.file_path]
        if not successful:
            continue
        avg_tts = sum(r.duration_ms for r in successful) / len(successful)
        avg_size = sum(r.file_size for r in successful) / len(successful)
        if has_whisper and fmt != "pcm":
            avg_sim = sum(r.similarity for r in successful) / len(successful)
            sim_str = f"{avg_sim:.2%}"
        else:
            sim_str = "n/a"
        lines.append(f"| {fmt} | {avg_tts:.0f}ms | {avg_size / 1024:.1f}KB | {sim_str} |")

    # Per-format detailed results
    for fmt, results in all_results.items():
        successful = [r for r in results if not r.error or r.file_path]
        if not successful:
            continue

        avg_tts = sum(r.duration_ms for r in successful) / len(successful)
        total_chars = sum(len(r.input_text) for r in successful)
        total_time = sum(r.duration_ms for r in successful)
        chars_per_sec = total_chars / (total_time / 1000) if total_time > 0 else 0

        lines += [
            "",
            f"## Results: {fmt.upper()}",
            "",
            "| Test | Input Length | Avg Latency | Min | Max | File Size |",
            "|------|-------------|-------------|-----|-----|-----------|",
        ]
        for r in successful:
            lines.append(f"| {r.name} | {len(r.input_text)} chars | {r.duration_ms:.0f}ms | {r.min_ms:.0f}ms | {r.max_ms:.0f}ms | {r.file_size / 1024:.1f}KB |")

        lines += [
            "",
            f"Avg latency: **{avg_tts:.0f}ms** | Throughput: **{chars_per_sec:.0f} chars/sec**",
        ]

    # Whisper validation details (wav as reference)
    if has_whisper and "wav" in all_results:
        lines += [
            "",
            "## Whisper Validation Details",
            "",
            "| Test | Similarity | Expected | Transcribed |",
            "|------|-----------|----------|-------------|",
        ]
        for r in all_results["wav"]:
            if r.whisper_text:
                lines.append(f"| {r.name} | {r.similarity:.0%} | {r.input_text} | {r.whisper_text} |")

    lines += [""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Kokoro TTS Benchmark")
    parser.add_argument("--kokoro", default=KOKORO_DEFAULT, help="Kokoro TTS URL")
    parser.add_argument("--whisper", default=None, help="Whisper ASR URL for validation")
    parser.add_argument("--voice", default="af_heart", help="Voice name")
    parser.add_argument("--formats", nargs="+", default=ALL_FORMATS, choices=ALL_FORMATS,
                        help="Audio formats to test (default: all)")
    parser.add_argument("--bitrate", default="192k", help="Bitrate for lossy formats")
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS, help="Runs per test case (default: 3)")
    parser.add_argument("--save-report", action="store_true", help="Save report.md")
    args = parser.parse_args()

    run_benchmark(args.kokoro, args.whisper, args.voice, args.formats, args.bitrate, args.runs, args.save_report)


if __name__ == "__main__":
    main()

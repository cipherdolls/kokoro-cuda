# Kokoro TTS Benchmark

Benchmark suite for Kokoro TTS with Whisper ASR validation.

Runs each test case multiple times across all audio formats (WAV, MP3, Opus, FLAC, PCM), measures avg/min/max latency, and validates output accuracy via Whisper transcription.

## Quick Start

```bash
docker compose up --build --abort-on-container-exit --exit-code-from benchmark
```

This starts 3 containers:
- **kokoro** — TTS service (port 8880)
- **whisper** — Whisper ASR for validation (port 9000)
- **benchmark** — runs tests, exits when done, stops all containers

## Output

Results are saved to `output/<GPU_NAME>/`:

```
output/NVIDIAGeForceRTX5090/
  report.md          # full benchmark report
  wav/               # generated audio files
  mp3/
  opus/
  flac/
  pcm/
```

## Configuration

Override defaults by editing the CMD in `Dockerfile`:

```dockerfile
CMD ["python3", "benchmark.py", \
  "--kokoro", "http://kokoro:8880", \
  "--whisper", "http://whisper:9000", \
  "--formats", "wav", "mp3", "opus", "flac", "pcm", \
  "--runs", "3", \
  "--bitrate", "192k", \
  "--save-report"]
```

| Flag | Default | Description |
|------|---------|-------------|
| --kokoro | http://localhost:8880 | Kokoro TTS URL |
| --whisper | (none) | Whisper ASR URL, omit to skip validation |
| --formats | wav mp3 opus flac pcm | Audio formats to test |
| --runs | 3 | Runs per test case for averaging |
| --bitrate | 192k | Bitrate for lossy formats |
| --voice | af_heart | Voice pack name |
| --save-report | (flag) | Write report.md to output dir |

## Running Locally (without Docker)

```bash
pip install requests

# TTS only
python benchmark.py --kokoro http://localhost:8880

# With Whisper validation
python benchmark.py --kokoro http://localhost:8880 --whisper http://localhost:9000 --save-report

# Single format, 5 runs
python benchmark.py --kokoro http://localhost:8880 --formats mp3 --runs 5
```

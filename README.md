# Kokoro CUDA

[![Docker Image](https://github.com/cipherdolls/kokoro-cuda/actions/workflows/docker.yml/badge.svg)](https://github.com/cipherdolls/kokoro-cuda/actions/workflows/docker.yml)

Minimal Kokoro TTS API with CUDA support for NVIDIA Blackwell GPUs.

**Source:** https://github.com/cipherdolls/kokoro-cuda

## Features

- Single FastAPI endpoint for text-to-speech
- Streaming audio (WAV/PCM) and encoded formats (MP3, Opus, FLAC)
- Configurable voice, speed, and bitrate
- Automatic model download on first start
- Swagger UI at `/docs`

## Quick Start

```bash
docker build -t kokoro-cuda .
docker run --gpus all -p 8880:8880 -v kokoro-models:/app/models -v kokoro-voices:/app/voices kokoro-cuda
```

## API

### `POST /v1/audio/speech`

```json
{
  "input": "Hello, this is a test.",
  "voice": "af_heart",
  "speed": 1.0,
  "response_format": "wav",
  "bitrate": "192k"
}
```

| Parameter | Default | Options |
|-----------|---------|---------|
| input | (required) | Any text |
| voice | af_heart | Any `.pt` voice pack |
| speed | 1.0 | 0.5 - 2.0 |
| response_format | wav | wav, mp3, opus, flac, pcm |
| bitrate | 192k | 128k, 192k, 320k |

### `GET /health`

Returns model status.

## Examples

```bash
# WAV
curl -X POST http://localhost:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world"}' -o hello.wav

# MP3 at 320k
curl -X POST http://localhost:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world", "response_format": "mp3", "bitrate": "320k"}' -o hello.mp3
```

## Benchmark

Run the full benchmark suite (Kokoro + Whisper validation):

```bash
cd benchmark
docker compose up --build --abort-on-container-exit --exit-code-from benchmark
```

Results are saved to `benchmark/output/<GPU_NAME>/report.md`. See [latest results](benchmark/output/NVIDIAGeForceRTX5090/report.md).

## Architecture

```
main.py            — FastAPI app, model loading, streaming TTS endpoint
download_model.py  — Downloads model + voice pack on first start
entrypoint.sh      — Runs download then starts uvicorn
Dockerfile         — CUDA 13.0 Blackwell image
benchmark/         — Benchmark suite with Whisper validation
```

## Requirements

- NVIDIA GPU with CUDA 13.0+ (Blackwell / SM 120)
- Docker with NVIDIA Container Toolkit

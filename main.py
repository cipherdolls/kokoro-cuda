"""Simplified Kokoro TTS API with streaming support."""

import io
import os
import struct
from contextlib import asynccontextmanager
from enum import Enum
from typing import Optional

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel
from pydub import AudioSegment

SAMPLE_RATE = 24000
MODEL_DIR = os.getenv("MODEL_DIR", "/app/models")
VOICES_DIR = os.getenv("VOICES_DIR", "/app/voices")

model = None
pipeline = None


class AudioFormat(str, Enum):
    wav = "wav"
    mp3 = "mp3"
    opus = "opus"
    flac = "flac"
    pcm = "pcm"


class TTSRequest(BaseModel):
    input: str
    voice: str = "af_heart"
    speed: float = 1.0
    response_format: AudioFormat = AudioFormat.wav
    bitrate: str = "192k"


def make_wav_header(data_size: int = 0xFFFFFFFF) -> bytes:
    """Create a 44-byte WAV header for 16-bit mono PCM at 24kHz."""
    channels = 1
    bits_per_sample = 16
    byte_rate = SAMPLE_RATE * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    return struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        data_size + 36 if data_size != 0xFFFFFFFF else 0xFFFFFFFF,
        b"WAVE",
        b"fmt ",
        16,
        1,  # PCM
        channels,
        SAMPLE_RATE,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size,
    )


def audio_to_pcm(audio: np.ndarray) -> bytes:
    """Convert float32 audio [-1, 1] to int16 PCM bytes."""
    return (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16).tobytes()


def encode_audio(pcm_data: bytes, fmt: AudioFormat, bitrate: str) -> tuple[bytes, str]:
    """Encode raw PCM to the requested format. Returns (bytes, media_type)."""
    if fmt == AudioFormat.pcm:
        return pcm_data, "audio/pcm"

    if fmt == AudioFormat.wav:
        buf = io.BytesIO()
        buf.write(make_wav_header(len(pcm_data)))
        buf.write(pcm_data)
        return buf.getvalue(), "audio/wav"

    if fmt == AudioFormat.flac:
        buf = io.BytesIO()
        samples = np.frombuffer(pcm_data, dtype=np.int16)
        sf.write(buf, samples, SAMPLE_RATE, format="FLAC")
        return buf.getvalue(), "audio/flac"

    # MP3 and Opus via pydub (requires ffmpeg)
    segment = AudioSegment(
        data=pcm_data,
        sample_width=2,
        frame_rate=SAMPLE_RATE,
        channels=1,
    )
    buf = io.BytesIO()
    if fmt == AudioFormat.mp3:
        segment.export(buf, format="mp3", bitrate=bitrate)
        return buf.getvalue(), "audio/mpeg"
    if fmt == AudioFormat.opus:
        segment.export(buf, format="opus", bitrate=bitrate)
        return buf.getvalue(), "audio/opus"

    return pcm_data, "application/octet-stream"


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, pipeline
    from kokoro import KModel, KPipeline

    config_path = os.path.join(MODEL_DIR, "config.json")
    model_path = os.path.join(MODEL_DIR, "kokoro-v1_0.pth")

    if not os.path.exists(model_path) or not os.path.exists(config_path):
        raise RuntimeError(
            f"Model files not found in {MODEL_DIR}. "
            "Run download_model.py first or set MODEL_DIR."
        )

    print(f"Loading Kokoro model from {MODEL_DIR}...")
    model = KModel(config=config_path, model=model_path).eval().cuda()
    pipeline = KPipeline(lang_code="a", model=model, device="cuda")
    print("Model loaded and ready.")
    yield


app = FastAPI(title="Kokoro TTS", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/v1/audio/speech")
async def synthesize(req: TTSRequest):
    if not pipeline:
        raise HTTPException(503, "Model not loaded")

    if not req.input.strip():
        raise HTTPException(400, "Input text is empty")

    voice_path = os.path.join(VOICES_DIR, f"{req.voice}.pt")
    if not os.path.exists(voice_path):
        raise HTTPException(404, f"Voice '{req.voice}' not found")

    # For WAV and PCM, stream chunks as they arrive
    if req.response_format in (AudioFormat.wav, AudioFormat.pcm):

        async def stream():
            header_sent = False
            for result in pipeline(req.input, voice=voice_path, speed=req.speed):
                if result.audio is None:
                    continue
                pcm = audio_to_pcm(result.audio.numpy())
                if not header_sent and req.response_format == AudioFormat.wav:
                    yield make_wav_header(0xFFFFFFFF)
                    header_sent = True
                yield pcm

        media_type = "audio/wav" if req.response_format == AudioFormat.wav else "audio/pcm"
        return StreamingResponse(stream(), media_type=media_type)

    # For MP3, Opus, FLAC: collect all audio then encode
    chunks = []
    for result in pipeline(req.input, voice=voice_path, speed=req.speed):
        if result.audio is None:
            continue
        chunks.append(result.audio.numpy())

    if not chunks:
        raise HTTPException(500, "No audio generated")

    full_audio = np.concatenate(chunks)
    pcm_data = audio_to_pcm(full_audio)
    encoded, media_type = encode_audio(pcm_data, req.response_format, req.bitrate)

    return Response(content=encoded, media_type=media_type)

FROM nvidia/cuda:12.8.0-base-ubuntu24.04

RUN apt-get update && apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --break-system-packages requests

WORKDIR /app

COPY benchmark.py .

ENV OUTPUT_DIR=/app/output

CMD ["python3", "benchmark.py", "--kokoro", "http://kokoro:8880", "--whisper", "http://whisper:9000", "--formats", "wav", "mp3", "opus", "flac", "pcm", "--save-report"]

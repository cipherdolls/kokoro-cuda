FROM nvcr.io/nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04

RUN apt-get update -y && \
    apt-get install -y python3.10 python3-venv espeak-ng espeak-ng-data \
      libsndfile1 ffmpeg curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /usr/share/espeak-ng-data && \
    ln -s /usr/lib/*/espeak-ng-data/* /usr/share/espeak-ng-data/ && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/

WORKDIR /app

COPY pyproject.toml .
RUN uv venv --python 3.10 && uv sync --extra gpu --no-cache

COPY main.py download_model.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TORCH_CUDA_ARCH_LIST="8.9;12.0" \
    PHONEMIZER_ESPEAK_PATH=/usr/bin \
    PHONEMIZER_ESPEAK_DATA=/usr/share/espeak-ng-data \
    ESPEAK_DATA_PATH=/usr/share/espeak-ng-data \
    MODEL_DIR=/app/models \
    VOICES_DIR=/app/voices

EXPOSE 8880

CMD ["./entrypoint.sh"]

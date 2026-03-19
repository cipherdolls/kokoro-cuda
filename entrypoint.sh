#!/bin/bash
set -e

echo "Checking for model files..."
python download_model.py --model-dir "$MODEL_DIR" --voices-dir "$VOICES_DIR"

echo "Starting Kokoro TTS server..."
exec python -m uvicorn main:app --host 0.0.0.0 --port 8880

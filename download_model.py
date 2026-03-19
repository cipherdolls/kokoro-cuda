"""Download Kokoro v1.0 model and default voice pack."""

import json
import os
from pathlib import Path
from urllib.request import urlretrieve


def download_model(model_dir: str) -> None:
    """Download model files from GitHub release."""
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "kokoro-v1_0.pth")
    config_path = os.path.join(model_dir, "config.json")

    if os.path.exists(model_path) and os.path.exists(config_path):
        if os.path.getsize(model_path) > 0:
            try:
                with open(config_path) as f:
                    json.load(f)
                print("Model files already exist and are valid")
                return
            except json.JSONDecodeError:
                pass

    base_url = "https://github.com/remsky/Kokoro-FastAPI/releases/download/v0.1.4"

    print("Downloading model file...")
    urlretrieve(f"{base_url}/kokoro-v1_0.pth", model_path)

    print("Downloading config file...")
    urlretrieve(f"{base_url}/config.json", config_path)

    print(f"Model files downloaded to {model_dir}")


def download_voices(voices_dir: str) -> None:
    """Download default voice pack from HuggingFace."""
    os.makedirs(voices_dir, exist_ok=True)

    voice_path = os.path.join(voices_dir, "af_heart.pt")
    if os.path.exists(voice_path) and os.path.getsize(voice_path) > 0:
        print("Voice files already exist")
        return

    base_url = "https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices"

    print("Downloading default voice (af_heart)...")
    urlretrieve(f"{base_url}/af_heart.pt", voice_path)

    print(f"Voice files downloaded to {voices_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Kokoro model and voices")
    parser.add_argument("--model-dir", default="/app/models")
    parser.add_argument("--voices-dir", default="/app/voices")
    args = parser.parse_args()

    download_model(args.model_dir)
    download_voices(args.voices_dir)

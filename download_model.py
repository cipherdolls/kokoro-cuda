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


VOICES = [
    "af_alloy", "af_aoede", "af_bella", "af_heart", "af_jessica", "af_kore",
    "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
    "am_onyx", "am_puck", "am_santa",
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
    "ef_dora", "em_alex", "em_santa",
    "ff_siwis",
    "hf_alpha", "hf_beta", "hm_omega", "hm_psi",
    "if_sara", "im_nicola",
    "jf_alpha", "jf_gongitsune", "jf_nezumi", "jf_tebukuro", "jm_kumo",
    "pf_dora", "pm_alex", "pm_santa",
    "zf_xiaobei", "zf_xiaoni", "zf_xiaoxiao", "zf_xiaoyi",
]


def download_voices(voices_dir: str) -> None:
    """Download all voice packs from HuggingFace."""
    os.makedirs(voices_dir, exist_ok=True)

    base_url = "https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices"
    existing = {f for f in os.listdir(voices_dir) if f.endswith(".pt") and os.path.getsize(os.path.join(voices_dir, f)) > 0}
    to_download = [v for v in VOICES if f"{v}.pt" not in existing]

    if not to_download:
        print(f"All {len(VOICES)} voices already exist")
        return

    print(f"Downloading {len(to_download)} voices ({len(existing)} already exist)...")
    for i, voice in enumerate(to_download, 1):
        print(f"  [{i}/{len(to_download)}] {voice}.pt")
        urlretrieve(f"{base_url}/{voice}.pt", os.path.join(voices_dir, f"{voice}.pt"))

    print(f"All {len(VOICES)} voices downloaded to {voices_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Kokoro model and voices")
    parser.add_argument("--model-dir", default="/app/models")
    parser.add_argument("--voices-dir", default="/app/voices")
    args = parser.parse_args()

    download_model(args.model_dir)
    download_voices(args.voices_dir)

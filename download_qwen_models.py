#!/usr/bin/env python3
"""
Download Qwen-Image-Edit-2509 GGUF models for ComfyUI

This script downloads the quantized Qwen image editing model and required text encoders.
Model sizes (choose based on VRAM):
  - Q4_K_M: 13.1 GB (recommended for 16-24GB VRAM)
  - Q5_K_M: 14.9 GB (better quality, 24GB+ VRAM)
  - Q6_K: 16.8 GB (high quality, 32GB+ VRAM)
  - Q8_0: 21.8 GB (best quality, 48GB+ VRAM)
"""

import os
import sys
from huggingface_hub import hf_hub_download

# Model repository
QWEN_REPO = "QuantStack/Qwen-Image-Edit-2509-GGUF"
TEXT_ENCODER_REPO = "Qwen/Qwen2.5-VL-7B"

# Target directories
UNET_DIR = "models/unet"
CLIP_DIR = "models/clip"

def download_qwen_unet(quantization="Q4_K_M"):
    """Download Qwen UNET model (GGUF)"""

    filename = f"Qwen-Image-Edit-2509-{quantization}.gguf"

    print(f"\n{'='*80}")
    print(f"📦 DOWNLOADING QWEN IMAGE EDIT MODEL")
    print(f"{'='*80}")
    print(f"Quantization: {quantization}")
    print(f"Repository: {QWEN_REPO}")
    print(f"File: {filename}")
    print(f"Target: {UNET_DIR}/")

    os.makedirs(UNET_DIR, exist_ok=True)

    try:
        downloaded_path = hf_hub_download(
            repo_id=QWEN_REPO,
            filename=filename,
            local_dir=UNET_DIR,
            local_dir_use_symlinks=False
        )
        print(f"✅ Downloaded: {downloaded_path}")
        return downloaded_path
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        return None


def download_text_encoder():
    """Download Qwen2.5-VL-7B text encoder"""

    print(f"\n{'='*80}")
    print(f"📦 DOWNLOADING TEXT ENCODER")
    print(f"{'='*80}")
    print(f"Repository: {TEXT_ENCODER_REPO}")
    print(f"Target: {CLIP_DIR}/")

    os.makedirs(CLIP_DIR, exist_ok=True)

    # Key files needed for text encoding
    files_to_download = [
        "model.safetensors",
        "config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "preprocessor_config.json",
    ]

    downloaded = []

    for filename in files_to_download:
        try:
            print(f"\n📥 Downloading {filename}...")
            downloaded_path = hf_hub_download(
                repo_id=TEXT_ENCODER_REPO,
                filename=filename,
                local_dir=f"{CLIP_DIR}/Qwen2.5-VL-7B",
                local_dir_use_symlinks=False
            )
            print(f"✅ {filename}")
            downloaded.append(downloaded_path)
        except Exception as e:
            print(f"⚠️  Could not download {filename}: {e}")

    return downloaded


def main():
    """Download all required models"""

    print("\n" + "="*80)
    print("🚀 QWEN-IMAGE-EDIT-2509 MODEL DOWNLOADER")
    print("="*80)
    print("\nThis will download:")
    print("  1. Qwen-Image-Edit-2509 UNET (GGUF quantized)")
    print("  2. Qwen2.5-VL-7B Text Encoder")
    print(f"\nTarget ComfyUI directories:")
    print(f"  • UNET: {UNET_DIR}")
    print(f"  • Text Encoder: {CLIP_DIR}")

    # Choose quantization level
    quantization = os.getenv("QWEN_QUANT", "Q4_K_M")

    print(f"\nSelected quantization: {quantization}")
    print("(Set QWEN_QUANT environment variable to change)")
    print("\nOptions: Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0")

    # Download UNET
    unet_path = download_qwen_unet(quantization)

    # Download text encoder
    encoder_paths = download_text_encoder()

    # Summary
    print("\n" + "="*80)
    print("✅ DOWNLOAD COMPLETE")
    print("="*80)

    if unet_path:
        print(f"\n📁 UNET Model: {unet_path}")

    if encoder_paths:
        print(f"\n📁 Text Encoder: {CLIP_DIR}/Qwen2.5-VL-7B/")
        print(f"   Files: {len(encoder_paths)}")

    print("\n📝 Next steps:")
    print("  1. Restart ComfyUI to load the new custom node")
    print("  2. Use 'Unet Loader (GGUF)' node from 'bootleg' category")
    print("  3. Load text encoder with appropriate CLIP loader")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        import huggingface_hub
    except ImportError:
        print("❌ huggingface_hub not installed!")
        print("Install with: pip install huggingface-hub")
        sys.exit(1)

    main()

#!/usr/bin/env python3
"""
Download High-Quality Models for DGX System
============================================

This script downloads state-of-the-art models optimized for photorealistic generation.
Perfect for DGX systems with high VRAM.
"""

import os
import subprocess
import sys

# Model directories
CHECKPOINT_DIR = "/home/raven/Documents/git/avatarforge/comfyui-dev/models/checkpoints"
LORA_DIR = "/home/raven/Documents/git/avatarforge/comfyui-dev/models/loras"
VAE_DIR = "/home/raven/Documents/git/avatarforge/comfyui-dev/models/vae"

# High-quality models for realistic generation
MODELS = {
    "checkpoint": [
        {
            "name": "realisticVisionV60B1_v51VAE.safetensors",
            "url": "https://civitai.com/api/download/models/130072",
            "dir": CHECKPOINT_DIR,
            "description": "Realistic Vision V6.0 - Top tier photorealistic model"
        },
        {
            "name": "epicrealism_naturalSinRC1VAE.safetensors",
            "url": "https://civitai.com/api/download/models/143906",
            "dir": CHECKPOINT_DIR,
            "description": "Epic Realism - Excellent for human portraits"
        }
    ],
    "lora": [
        {
            "name": "add_detail.safetensors",
            "url": "https://civitai.com/api/download/models/87153",
            "dir": LORA_DIR,
            "description": "Detail enhancement LoRA"
        },
        {
            "name": "epi_noiseoffset2.safetensors",
            "url": "https://civitai.com/api/download/models/16576",
            "dir": LORA_DIR,
            "description": "Noise offset for better contrast"
        }
    ]
}

def download_file(url, output_path, description):
    """Download file using wget or curl"""
    print(f"\n{'='*70}")
    print(f"📥 Downloading: {description}")
    print(f"{'='*70}")
    print(f"URL: {url}")
    print(f"Output: {output_path}")

    if os.path.exists(output_path):
        print(f"✅ Already exists, skipping...")
        return True

    # Try wget first
    try:
        cmd = ["wget", "-O", output_path, url, "--progress=bar:force"]
        result = subprocess.run(cmd, check=True)
        print(f"✅ Downloaded successfully!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Try curl
    try:
        cmd = ["curl", "-L", "-o", output_path, url, "--progress-bar"]
        result = subprocess.run(cmd, check=True)
        print(f"✅ Downloaded successfully!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ Failed to download. Please install wget or curl.")
        return False

def main():
    print("\n" + "="*70)
    print("🚀 HIGH-QUALITY MODEL SETUP FOR DGX SYSTEM")
    print("="*70)
    print("\nThis will download state-of-the-art models for photorealistic generation:")
    print("  • Realistic Vision V6.0 (~2GB)")
    print("  • Epic Realism Natural Sin (~2GB)")
    print("  • Detail enhancement LoRAs (~100MB)")
    print(f"\nTotal download size: ~4-5GB")
    print(f"\n⚠️  This may take 10-30 minutes depending on your connection.")

    response = input("\n📋 Proceed with download? (y/n): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Cancelled.")
        sys.exit(0)

    # Download checkpoints
    print("\n" + "="*70)
    print("📦 DOWNLOADING CHECKPOINT MODELS")
    print("="*70)

    for model in MODELS["checkpoint"]:
        download_file(model["url"], os.path.join(model["dir"], model["name"]), model["description"])

    # Download LoRAs
    print("\n" + "="*70)
    print("📦 DOWNLOADING LORA MODELS")
    print("="*70)

    for model in MODELS["lora"]:
        download_file(model["url"], os.path.join(model["dir"], model["name"]), model["description"])

    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\n📋 Downloaded models:")
    print(f"\nCheckpoints ({CHECKPOINT_DIR}):")
    for model in MODELS["checkpoint"]:
        print(f"  ✅ {model['name']}")

    print(f"\nLoRAs ({LORA_DIR}):")
    for model in MODELS["lora"]:
        print(f"  ✅ {model['name']}")

    print("\n🚀 You can now use these models with the enhanced test script!")
    print("\nNext step: Run the enhanced fitness influencer generator:")
    print("  python3 test_fitness_influencer_enhanced.py")
    print()

if __name__ == "__main__":
    main()

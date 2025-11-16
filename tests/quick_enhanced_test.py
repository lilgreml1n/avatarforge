#!/usr/bin/env python3
"""
QUICK Enhanced Test - Maximum quality from existing model
Uses aggressive settings optimized for DGX hardware
"""

import requests
import time
from datetime import datetime

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

def generate_best_quality():
    """Generate with maximum quality settings"""

    # Ultra-detailed prompt with quality keywords - FACE FOCUSED
    payload = {
        "prompt": (
            "professional portrait photograph, RAW photo, masterpiece, best quality, "
            "ultra high resolution, 8k uhd, photorealistic, hyperrealistic, "
            "beautiful caucasian fitness model, age 25-28, fair skin, "
            "gorgeous face, beautiful detailed eyes, beautiful detailed lips, "
            "extremely detailed face and eyes, symmetrical face, perfect proportions, "
            "soft natural smile, kind eyes, flawless complexion, "
            "long blonde ponytail hairstyle, light natural makeup, "
            "athletic toned physique, fit body, defined muscles, "
            "professional studio lighting, soft key light, rim lighting, "
            "clean neutral background, sharp focus on face, "
            "professional fashion photography, vogue style, "
            "film grain, kodak portra 400, "
            "detailed skin texture, realistic skin, subsurface scattering"
        ),
        "clothing": (
            "modern athletic wear, black sports bra, grey leggings, "
            "professional athletic outfit, clean simple design"
        ),
        "realism": True,

        # MAXIMUM QUALITY SETTINGS for better face
        "width": 768,        # Slightly smaller for more detail per pixel
        "height": 1152,      # Better for facial detail
        "steps": 80,         # MORE steps for higher quality
        "cfg": 7.5,          # Lower CFG to avoid artifacts
        "sampler_name": "dpmpp_2m_sde_gpu"  # GPU-optimized sampler
    }

    print("\n" + "="*80)
    print("🚀 GENERATING ULTRA-QUALITY WITH OPTIMIZED SETTINGS")
    print("="*80)
    print(f"\n⚙️  Settings:")
    print(f"   Resolution: {payload['width']}x{payload['height']} (2.4MP)")
    print(f"   Steps: {payload['steps']} (high quality)")
    print(f"   CFG Scale: {payload['cfg']} (strong prompt guidance)")
    print(f"   Sampler: {payload['sampler_name']} (best quality)")
    print(f"\n💡 Using enhanced prompt with quality keywords")
    print(f"   This will take ~3-5 minutes on your DGX\n")

    # Submit
    print("🚀 Submitting generation...")
    response = requests.post(f"{API_URL}/generate/avatar", json=payload, timeout=30)
    result = response.json()

    print(f"✅ Queued: {result['generation_id']}")

    # Wait
    print("\n⏳ Waiting for completion...")
    start = time.time()

    while (time.time() - start) < 600:
        elapsed = int(time.time() - start)
        print(f"\r   ⏱️  {elapsed}s", end="", flush=True)

        history = requests.get(f"{COMFYUI_URL}/history/{result['comfyui_prompt_id']}").json()

        if result['comfyui_prompt_id'] in history:
            data = history[result['comfyui_prompt_id']]
            if data.get("status", {}).get("completed"):
                for node_id, output in data.get("outputs", {}).items():
                    if output.get("images"):
                        filename = output["images"][0]["filename"]
                        url = f"{COMFYUI_URL}/view?filename={filename}&type=output"

                        print(f"\n\n✅ Complete in {elapsed}s!")

                        # Download
                        img_data = requests.get(url).content
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_file = f"fitness_ULTRA_{timestamp}.png"

                        with open(output_file, "wb") as f:
                            f.write(img_data)

                        size_mb = len(img_data) / (1024*1024)

                        print("\n" + "="*80)
                        print("🎉 ULTRA-QUALITY GENERATION COMPLETE!")
                        print("="*80)
                        print(f"\n💾 File: {output_file}")
                        print(f"📊 Size: {size_mb:.2f} MB")
                        print(f"🌐 URL: {url}")
                        print("\n" + "="*80)
                        return

        time.sleep(5)

if __name__ == "__main__":
    generate_best_quality()

#!/usr/bin/env python3
"""
Generate 5 Photorealistic Fitness Influencers
==============================================

Uses Realistic Vision v5.1 for maximum quality
"""

import requests
import time
from datetime import datetime

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

def generate_image(index):
    """Generate a single photorealistic image"""

    payload = {
        # Enhanced prompt with specific eye details
        "prompt": (
            "Caucasian woman, blonde hair, confident expression, wearing black workout set, at modern gym, "
            "clear sharp symmetrical eyes, focused eyes, bright eyes, detailed eyes, "
            "natural lighting, professional fitness photography, authentic, sharp focus, high quality, realistic, 4k"
        ),

        # Enhanced negative prompt with specific eye exclusions
        "negative_prompt": (
            "ugly, deformed, distorted, disfigured, bad anatomy, wrong anatomy, "
            "extra limbs, mutation, mutated, bad proportions, gross proportions, "
            "bad eyes, crossed eyes, asymmetric eyes, weird eyes, different sized eyes, "
            "blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes, "
            "lazy eye, uneven eyes, "
            "bad face, ugly face, distorted face, malformed face, "
            "bad shadows, harsh shadows, unrealistic shadows, "
            "blurry, low quality, lowres, jpeg artifacts, compression artifacts, "
            "cartoon, anime, drawing, painting, illustration, sketch, "
            "overexposed, underexposed, oversaturated, "
            "duplicate, clone, artificial, fake"
        ),

        "clothing": "black workout set",
        "realism": True,

        # Optimized settings for photorealism (35+ steps for better eyes)
        "width": 768,
        "height": 1024,
        "steps": 50,  # 35+ for eye quality
        "cfg": 7.0,
        "sampler_name": "dpmpp_2m_karras",
        "scheduler": "karras",
    }

    print(f"\n{'='*80}")
    print(f"📸 GENERATING IMAGE {index}/5")
    print(f"{'='*80}")
    print(f"\n⚙️  Settings: 768x1024, 50 steps, CFG 7.0, dpmpp_2m_karras")
    print(f"🎨 Model: Realistic Vision v5.1")
    print(f"\n🚀 Starting generation...")

    try:
        response = requests.post(
            f"{API_URL}/generate/avatar",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        print(f"✅ Queued: {result['generation_id']}")
        print(f"⏳ Processing...", end="", flush=True)

        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)

            try:
                history = requests.get(
                    f"{COMFYUI_URL}/history/{result['comfyui_prompt_id']}",
                    timeout=10
                ).json()

                if result['comfyui_prompt_id'] in history:
                    data = history[result['comfyui_prompt_id']]

                    if data.get("status", {}).get("completed"):
                        for node_id, output in data.get("outputs", {}).items():
                            if output.get("images"):
                                filename = output["images"][0]["filename"]
                                url = f"{COMFYUI_URL}/view?filename={filename}&type=output"

                                # Download
                                img_data = requests.get(url).content
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                output_file = f"photorealistic_{index}_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print(f"\n✅ Complete in {elapsed}s!")
                                print(f"📁 File: {output_file}")
                                print(f"💾 Size: {size_mb:.2f} MB")
                                print(f"🌐 URL: {url}")

                                return output_file

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout after {int(time.time() - start_time)}s")
        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def main():
    """Generate 5 images"""
    print("\n" + "="*80)
    print("📸 PHOTOREALISTIC BATCH GENERATION")
    print("="*80)
    print("\n🎯 Goal: Generate 5 high-quality photorealistic images")
    print("🎨 Model: Realistic Vision v5.1")
    print("⚙️  Settings: Optimized for maximum quality\n")

    results = []
    start_time = time.time()

    for i in range(1, 6):
        result = generate_image(i)
        if result:
            results.append(result)

        # Small delay between generations
        if i < 5:
            print(f"\n⏸️  Waiting 2 seconds before next generation...")
            time.sleep(2)

    total_time = int(time.time() - start_time)

    print("\n" + "="*80)
    print("🎉 BATCH GENERATION COMPLETE")
    print("="*80)
    print(f"\n📊 Results:")
    print(f"   Total images: {len(results)}/5")
    print(f"   Total time: {total_time}s ({total_time//60}m {total_time%60}s)")
    print(f"   Average: {total_time//len(results) if results else 0}s per image")

    print(f"\n📁 Generated files:")
    for i, filename in enumerate(results, 1):
        print(f"   {i}. {filename}")

    print(f"\n✨ All images use:")
    print(f"   • Realistic Vision v5.1 model")
    print(f"   • Professional photorealistic quality")
    print(f"   • Negative prompts for artifact removal")
    print(f"   • Optimized sampler (dpmpp_2m_karras)")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

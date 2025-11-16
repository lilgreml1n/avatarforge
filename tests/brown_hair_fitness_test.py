#!/usr/bin/env python3
"""
Quick Test: Brown-Haired Fitness Influencer
============================================

Generate a beautiful brown-haired fitness influencer
"""

import requests
import time
from datetime import datetime

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"


def generate_brown_hair_fitness():
    """Generate a brown-haired fitness influencer"""

    payload = {
        "prompt": (
            "beautiful 25 year old woman, fitness influencer, athletic physique, "
            "long flowing brown hair in high ponytail, warm brown eyes, "
            "radiant smile, confident expression, healthy glowing skin, "
            "wearing stylish athletic wear, black sports bra and matching leggings, "
            "at modern well-lit gym with equipment in background, "
            "professional fitness photography, natural lighting, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic, "
            "perfect face, detailed eyes, perfect proportions"
        ),
        "negative_prompt": (
            "ugly, old, deformed, bad anatomy, bad proportions, "
            "bad face, distorted face, asymmetrical face, "
            "blurry eyes, cross-eyed, lazy eye, weird eyes, "
            "blurry, low quality, jpeg artifacts, "
            "cartoon, anime, painting, sketch, drawing, "
            "nude, nsfw, blonde hair, red hair, gray hair"
        ),
        "clothing": "black athletic wear",
        "realism": True,
        "width": 768,
        "height": 1024,
        "steps": 50,
        "cfg": 7.0,
        "sampler_name": "dpmpp_2m_karras",
        "scheduler": "karras",
    }

    print("\n" + "="*80)
    print("💪 BROWN-HAIRED FITNESS INFLUENCER GENERATION")
    print("="*80)
    print("\n👤 Subject: 25-year-old fitness influencer")
    print("💇 Hair: Long brown hair in high ponytail")
    print("👗 Outfit: Black athletic wear")
    print("📸 Style: Professional fitness photography")
    print("\n🚀 Generating...")

    try:
        response = requests.post(f"{API_URL}/generate/avatar", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        print(f"✅ Queued: {result['generation_id']}")
        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)
            print(f"\r⏳ Processing... {elapsed}s", end="", flush=True)

            try:
                history = requests.get(f"{COMFYUI_URL}/history/{result['comfyui_prompt_id']}", timeout=10).json()

                if result['comfyui_prompt_id'] in history:
                    data = history[result['comfyui_prompt_id']]

                    if data.get("status", {}).get("completed"):
                        for node_id, output in data.get("outputs", {}).items():
                            if output.get("images"):
                                filename = output["images"][0]["filename"]
                                url = f"{COMFYUI_URL}/view?filename={filename}&type=output"
                                img_data = requests.get(url).content

                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                output_file = f"brown_hair_fitness_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print(f"\n✅ Complete in {elapsed}s!")
                                print(f"\n📊 Results:")
                                print(f"   File: {output_file}")
                                print(f"   Size: {size_mb:.2f} MB")
                                print(f"   URL: {url}")
                                print(f"\n✨ A beautiful brown-haired fitness influencer!")

                                return output_file, filename

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout")
        return None, None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    print("\n" + "="*80)
    print("🎨 BROWN-HAIRED FITNESS INFLUENCER TEST")
    print("="*80)

    output_file, filename = generate_brown_hair_fitness()

    if output_file:
        print("\n" + "="*80)
        print("🎉 GENERATION COMPLETE!")
        print("="*80)
        print(f"\n📁 Saved: {output_file}")
        print("\n💡 Next: Once Qwen models finish downloading,")
        print("   we can enhance this with AI-powered editing!")
    else:
        print("\n❌ Generation failed")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

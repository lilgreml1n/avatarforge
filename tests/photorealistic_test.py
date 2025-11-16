#!/usr/bin/env python3
"""
Photorealistic Fitness Influencer - Optimized Settings
======================================================

Maximum quality photorealistic generation
- Negative prompts for face quality
- Optimized sampler and settings
- Minimal focused prompt
"""

import requests
import time
from datetime import datetime

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

def generate_photorealistic():
    """Generate maximum quality photorealistic fitness woman"""

    payload = {
        # SIMPLE, FOCUSED PROMPT - Less is more for realism
        "prompt": (
            "professional photograph of a blonde fitness woman at modern gym, "
            "natural lighting, high quality, photorealistic, 8k uhd, detailed"
        ),

        # CRITICAL: Negative prompt to avoid artifacts
        "negative_prompt": (
            "ugly, deformed, distorted, disfigured, bad anatomy, wrong anatomy, "
            "extra limbs, mutation, mutated, bad proportions, gross proportions, "
            "bad eyes, crossed eyes, asymmetric eyes, weird eyes, different sized eyes, "
            "bad face, ugly face, distorted face, malformed face, "
            "bad shadows, harsh shadows, unrealistic shadows, "
            "blurry, low quality, lowres, jpeg artifacts, compression artifacts, "
            "cartoon, anime, drawing, painting, illustration, sketch, "
            "overexposed, underexposed, oversaturated, "
            "duplicate, clone, artificial, fake"
        ),

        "clothing": "black athletic workout set",
        "realism": True,

        # OPTIMIZED SETTINGS FOR PHOTOREALISM
        "width": 768,
        "height": 1024,
        "steps": 50,              # Higher for better quality
        "cfg": 7.0,               # Balanced - not too high, not too low
        "sampler_name": "dpmpp_2m_karras",  # Best quality sampler
        "scheduler": "karras",     # Better noise schedule
    }

    print("\n" + "="*80)
    print("📸 PHOTOREALISTIC GENERATION - OPTIMIZED")
    print("="*80)
    print("\n🎯 Goal: Maximum photorealism with current model")
    print("\n⚙️  Optimized Settings:")
    print(f"   Resolution: {payload['width']}x{payload['height']}")
    print(f"   Steps: {payload['steps']} (increased for quality)")
    print(f"   CFG: {payload['cfg']} (balanced)")
    print(f"   Sampler: {payload['sampler_name']} (best quality)")
    print(f"   Scheduler: {payload['scheduler']}")
    print("\n✨ Key Improvements:")
    print("   ✅ Negative prompt (removes artifacts)")
    print("   ✅ Better sampler (dpmpp_2m_karras)")
    print("   ✅ Optimized CFG (7.0)")
    print("   ✅ More steps (50)")
    print("   ✅ Minimal focused prompt")

    print("\n💡 Current Model Limitation:")
    print("   ⚠️  Using: SD 1.5 base (not specialized for photorealism)")
    print("   📥 Consider downloading better model (see recommendations below)")

    print("\n🚀 Generating...")

    try:
        response = requests.post(
            f"{API_URL}/generate/avatar",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        print(f"✅ Queued: {result['generation_id']}")
        print(f"\n⏳ Processing...")

        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)
            print(f"\r   ⏱️  {elapsed}s", end="", flush=True)

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

                                print(f"\n\n✅ Complete in {elapsed}s!")

                                # Download
                                img_data = requests.get(url).content
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                output_file = f"photorealistic_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print("\n" + "="*80)
                                print("📸 PHOTOREALISTIC RESULT")
                                print("="*80)
                                print(f"\n📊 Stats:")
                                print(f"   File: {output_file}")
                                print(f"   Size: {size_mb:.2f} MB")
                                print(f"   Time: {elapsed}s")
                                print(f"\n🌐 View URL:")
                                print(f"   {url}")

                                print("\n" + "="*80)
                                print("📥 RECOMMENDED MODELS FOR BETTER QUALITY")
                                print("="*80)
                                print("\nDownload one of these for photorealistic portraits:")
                                print("\n1. Realistic Vision v5.1 (BEST FOR PORTRAITS)")
                                print("   https://civitai.com/models/4201/realistic-vision-v51")
                                print("\n2. CyberRealistic v4.1 (EXCELLENT FACES)")
                                print("   https://civitai.com/models/15003/cyberrealistic")
                                print("\n3. Deliberate v3 (VERY PHOTOREALISTIC)")
                                print("   https://civitai.com/models/4823/deliberate")
                                print("\n4. epiCRealism (NATURAL PORTRAITS)")
                                print("   https://civitai.com/models/25694/epicrealism")

                                print("\n📝 How to install:")
                                print("   1. Download .safetensors file")
                                print("   2. Place in: ComfyUI/models/checkpoints/")
                                print("   3. Restart ComfyUI")
                                print("   4. Update avatarforge to use new model")

                                print("\n" + "="*80 + "\n")
                                return

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n\n⏰ Timeout")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    generate_photorealistic()

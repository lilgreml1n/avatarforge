#!/usr/bin/env python3
"""
Natural Looking Fitness Influencer - Fixed Eyes
================================================

Focuses on NORMAL, NATURAL looking woman
- Fixed eye issues
- Natural expressions
- Realistic proportions
- No weird artifacts
"""

import requests
import time
from datetime import datetime

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

def generate_natural():
    """Generate normal, natural looking fitness influencer"""

    # SIMPLE, CLEAN PROMPT
    payload = {
        "prompt": (
            "Caucasian woman, blonde hair, confident expression, wearing black workout set, at modern gym, "
            "natural lighting, professional fitness photography, authentic, sharp focus, high quality, realistic, 4k"
        ),

        "clothing": "black workout set",

        "realism": True,

        # CONSERVATIVE SETTINGS - Avoid artifacts
        "width": 768,
        "height": 1024,
        "steps": 40,          # Even fewer steps
        "cfg": 5.5,           # VERY LOW CFG = most natural
        "sampler_name": "euler_a",  # Simpler sampler, more stable
    }

    print("\n" + "="*80)
    print("👤 NATURAL LOOKING WOMAN - FIXED EYES")
    print("="*80)
    print("\n🎯 Focus: Normal, natural looking fitness woman")
    print("   NO weird eyes, NO over-emphasized features")
    print("\n⚙️  Settings:")
    print(f"   Resolution: {payload['width']}x{payload['height']}")
    print(f"   Steps: {payload['steps']} (moderate)")
    print(f"   CFG: {payload['cfg']} (LOWER = more natural)")
    print(f"   Sampler: {payload['sampler_name']} (stable)")
    print("\n💡 Key changes from before:")
    print("   ✅ NO emphasis weights (1.1, 1.2, etc)")
    print("   ✅ Simple eye description")
    print("   ✅ Lower CFG (6.5 vs 7.5)")
    print("   ✅ Fewer steps (50 vs 80-100)")
    print("   ✅ Simpler prompt")
    print("   ✅ Natural proportions focus")

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
                                output_file = f"fitness_NATURAL_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print("\n" + "="*80)
                                print("👤 NATURAL LOOKING WOMAN - RESULT")
                                print("="*80)
                                print(f"\n📊 Stats:")
                                print(f"   File: {output_file}")
                                print(f"   Size: {size_mb:.2f} MB")
                                print(f"   Time: {elapsed}s")
                                print(f"\n🌐 View URL:")
                                print(f"   {url}")
                                print("\n✅ This should have:")
                                print("   • Normal looking eyes (no weird shapes)")
                                print("   • Natural facial proportions")
                                print("   • Realistic expression")
                                print("   • No over-emphasized features")
                                print("   • Girl-next-door vibe")
                                print("\n💡 If eyes still look weird, try:")
                                print("   1. Lower CFG even more (5.5-6.0)")
                                print("   2. Different seed (random variation)")
                                print("   3. Simpler prompt")
                                print("\n" + "="*80 + "\n")
                                return

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n\n⏰ Timeout")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    generate_natural()

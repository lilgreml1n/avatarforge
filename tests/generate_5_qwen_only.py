#!/usr/bin/env python3
"""
Generate 5 Photorealistic Fitness Influencers - Qwen AI ONLY
=============================================================

Generate 5 different fitness influencer variations and enhance with Qwen-Image-Edit-2509 AI.
This uses ONLY the Qwen model for enhancement (NO inpainting at all).
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

import requests
import time
from datetime import datetime

COMFYUI_URL = "http://192.168.100.133:8188"
API_URL = "http://192.168.100.133:8000/avatarforge-controller"


# No QwenRequest class needed - we'll use direct ComfyUI workflow


# 5 different variations
VARIATIONS = [
    {
        "name": "Blonde Athletic",
        "prompt": (
            "beautiful Caucasian woman, 20-25 years old, fitness influencer, athletic physique, "
            "long blonde hair in high ponytail, youthful face, bright smile, confident expression, "
            "fair skin, natural makeup, "
            "wearing stylish white sports bra and black leggings, "
            "at modern gym with equipment in background, "
            "natural lighting, professional fitness photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),
    },
    {
        "name": "Brunette Yoga",
        "prompt": (
            "beautiful Caucasian woman, 22-26 years old, yoga fitness influencer, toned physique, "
            "long dark brown hair in braid, serene face, gentle smile, peaceful expression, "
            "fair skin, minimal makeup, "
            "wearing stylish purple yoga top and matching leggings, "
            "at bright yoga studio with plants in background, "
            "soft natural lighting, professional wellness photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),
    },
    {
        "name": "Redhead Crossfit",
        "prompt": (
            "beautiful Caucasian woman, 21-24 years old, crossfit fitness influencer, muscular athletic build, "
            "medium length red hair in messy bun, determined face, strong smile, intense expression, "
            "fair skin with freckles, natural makeup, "
            "wearing stylish grey sports bra and dark grey leggings, "
            "at industrial crossfit gym with weights in background, "
            "dramatic lighting, professional sports photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),
    },
    {
        "name": "Blonde Running",
        "prompt": (
            "beautiful Caucasian woman, 23-27 years old, running fitness influencer, lean athletic physique, "
            "short blonde hair in sporty style, energetic face, joyful smile, dynamic expression, "
            "fair skin, fresh makeup, "
            "wearing stylish neon pink sports bra and black running shorts, "
            "at outdoor track with trees in background, "
            "golden hour lighting, professional action photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),
    },
    {
        "name": "Brown Hair Pilates",
        "prompt": (
            "beautiful Caucasian woman, 24-28 years old, pilates fitness influencer, elegant toned physique, "
            "long light brown hair flowing down, graceful face, warm smile, calm expression, "
            "fair skin, soft makeup, "
            "wearing stylish teal sports bra and high-waisted black leggings, "
            "at modern pilates studio with reformer equipment in background, "
            "soft diffused lighting, professional wellness photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),
    },
]

# Shared negative prompt
NEGATIVE_PROMPT = (
    "ugly, old, mature, aged, deformed, distorted, disfigured, bad anatomy, wrong anatomy, "
    "Asian, African, dark skin, "
    "extra limbs, mutation, mutated, bad proportions, gross proportions, "
    "bad eyes, crossed eyes, asymmetric eyes, weird eyes, different sized eyes, "
    "blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes, "
    "lazy eye, uneven eyes, "
    "bad face, ugly face, distorted face, malformed face, "
    "bad shadows, harsh shadows, unrealistic shadows, "
    "blurry, low quality, lowres, jpeg artifacts, compression artifacts, "
    "cartoon, anime, drawing, painting, illustration, sketch, "
    "overexposed, underexposed, oversaturated, "
    "duplicate, clone, artificial, fake, nude, nsfw"
)


def generate_base(variation_data, index):
    """Step 1: Generate base fitness influencer"""

    payload = {
        "prompt": variation_data["prompt"],
        "negative_prompt": NEGATIVE_PROMPT,
        "clothing": "athletic wear, sports bra, leggings",
        "realism": True,

        # Optimized settings
        "width": 768,
        "height": 1024,
        "steps": 50,
        "cfg": 7.0,
        "sampler_name": "dpmpp_2m_karras",
        "scheduler": "karras",
    }

    print("\n" + "="*80)
    print(f"🎨 GENERATING #{index + 1}: {variation_data['name']}")
    print("="*80)
    print(f"\n⚙️  Settings: 768x1024, 50 steps, CFG 7.0")
    print("🎯 Model: Realistic Vision v5.1")
    print("\n🚀 Generating base image...")

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
                                safe_name = variation_data['name'].lower().replace(' ', '_')
                                output_file = f"{safe_name}_base_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print(f"\n✅ Base complete in {elapsed}s!")
                                print(f"📁 File: {output_file}")
                                print(f"💾 Size: {size_mb:.2f} MB")

                                return output_file

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout")
        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def qwen_enhance(base_local_file, variation_name, use_lightning=True):
    """Step 2: Enhance with Qwen AI - Simple workflow without inpainting"""

    print("\n🤖 Enhancing with Qwen AI...")

    # Upload base image to ComfyUI
    print(f"📤 Uploading base image...")
    with open(base_local_file, 'rb') as f:
        files = {'image': (base_local_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        base_upload = response.json()
        base_comfy_name = base_upload.get('name', base_local_file)

    # Natural language enhancement prompt
    enhancement_prompt = (
        "Enhance the entire image to be more photorealistic and detailed. "
        "Make the eyes crystal clear, bright, and perfectly symmetrical. "
        "Improve skin texture and lighting. "
        "Enhance facial features to look more natural and realistic. "
        "Make the overall image sharper and more professional."
    )

    # Build simple Qwen workflow (NO inpainting)
    steps = 4 if use_lightning else 20
    cfg = 2.5

    workflow = {
        "prompt": {
            "1": {
                "inputs": {
                    "image": base_comfy_name,
                    "upload": "image"
                },
                "class_type": "LoadImage",
                "_meta": {"title": "Load Base Image"}
            },
            "2": {
                "inputs": {
                    "unet_name": "Qwen-Image-Edit-2509-Q4_K_M.gguf",
                    "weight_dtype": "default"
                },
                "class_type": "UnetLoaderGGUF",
                "_meta": {"title": "Load Qwen GGUF"}
            },
            "3": {
                "inputs": {
                    "clip_name1": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                    "clip_name2": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                    "type": "flux"
                },
                "class_type": "DualCLIPLoader",
                "_meta": {"title": "Load CLIP"}
            },
            "4": {
                "inputs": {
                    "vae_name": "qwen_image_vae.safetensors"
                },
                "class_type": "VAELoader",
                "_meta": {"title": "Load VAE"}
            },
            "5": {
                "inputs": {
                    "text": enhancement_prompt,
                    "clip": ["3", 0]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "Positive Prompt"}
            },
            "6": {
                "inputs": {
                    "pixels": ["1", 0],
                    "vae": ["4", 0]
                },
                "class_type": "VAEEncode",
                "_meta": {"title": "VAE Encode"}
            },
            "7": {
                "inputs": {
                    "seed": int(time.time()),
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "simple",
                    "denoise": 0.75,
                    "model": ["2", 0],
                    "positive": ["5", 0],
                    "negative": ["5", 0],
                    "latent_image": ["6", 0]
                },
                "class_type": "KSampler",
                "_meta": {"title": "Qwen Sampler"}
            },
            "8": {
                "inputs": {
                    "samples": ["7", 0],
                    "vae": ["4", 0]
                },
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE Decode"}
            },
            "9": {
                "inputs": {
                    "filename_prefix": "qwen_enhanced",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage",
                "_meta": {"title": "Save Enhanced Image"}
            }
        }
    }

    print("🚀 Submitting Qwen workflow...")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)

        if response.status_code != 200:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            return None

        response.raise_for_status()
        result = response.json()

        prompt_id = result['prompt_id']
        print(f"✅ Queued: {prompt_id}")

        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)
            print(f"\r⏳ Qwen AI enhancing... {elapsed}s", end="", flush=True)

            try:
                history = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10).json()

                if prompt_id in history:
                    data = history[prompt_id]

                    if data.get("status", {}).get("completed"):
                        for node_id, output in data.get("outputs", {}).items():
                            if output.get("images"):
                                filename = output["images"][0]["filename"]
                                url = f"{COMFYUI_URL}/view?filename={filename}&type=output"
                                img_data = requests.get(url).content

                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                safe_name = variation_name.lower().replace(' ', '_')
                                output_file = f"{safe_name}_FINAL_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print(f"\n✅ Qwen enhancement complete in {elapsed}s!")
                                print(f"📁 File: {output_file}")
                                print(f"💾 Size: {size_mb:.2f} MB")

                                return output_file

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout")
        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Generate 5 Qwen-enhanced fitness influencers"""

    print("\n" + "="*80)
    print("🏋️ GENERATE 5 PHOTOREALISTIC FITNESS INFLUENCERS - QWEN AI ONLY")
    print("="*80)
    print("\n🎯 Workflow:")
    print("   1. Generate 5 different base fitness influencer variations")
    print("   2. Enhance each with Qwen-Image-Edit-2509 AI")
    print("\n✨ Variations:")
    for i, var in enumerate(VARIATIONS, 1):
        print(f"   {i}. {var['name']}")
    print("\n⚡ Using Qwen Lightning mode (4 steps, super fast!)")
    print("\n" + "="*80)

    results = []

    for i, variation in enumerate(VARIATIONS):
        print(f"\n\n{'='*80}")
        print(f"🎬 VARIATION {i + 1}/5: {variation['name']}")
        print("="*80)

        # Step 1: Generate base
        base_file = generate_base(variation, i)

        if not base_file:
            print(f"\n❌ Base generation failed for {variation['name']}")
            results.append({
                "name": variation['name'],
                "status": "failed",
                "base": None,
                "final": None
            })
            continue

        # Step 2: Qwen enhancement (Lightning mode for speed)
        final_file = qwen_enhance(base_file, variation['name'], use_lightning=True)

        if final_file:
            results.append({
                "name": variation['name'],
                "status": "success",
                "base": base_file,
                "final": final_file
            })
            print(f"\n✅ {variation['name']} complete!")
        else:
            results.append({
                "name": variation['name'],
                "status": "partial",
                "base": base_file,
                "final": None
            })
            print(f"\n⚠️  {variation['name']} base generated, Qwen enhancement failed")

    # Summary
    print("\n\n" + "="*80)
    print("🎉 ALL 5 GENERATIONS COMPLETE!")
    print("="*80)

    successful = [r for r in results if r['status'] == 'success']
    partial = [r for r in results if r['status'] == 'partial']
    failed = [r for r in results if r['status'] == 'failed']

    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {len(successful)}/5")
    print(f"   ⚠️  Partial: {len(partial)}/5")
    print(f"   ❌ Failed: {len(failed)}/5")

    if successful:
        print(f"\n✨ Successful Generations:")
        for r in successful:
            print(f"\n   {r['name']}:")
            print(f"      Base:  {r['base']}")
            print(f"      Final: {r['final']}")

    if partial:
        print(f"\n⚠️  Partial Generations (base only):")
        for r in partial:
            print(f"   {r['name']}: {r['base']}")

    if failed:
        print(f"\n❌ Failed Generations:")
        for r in failed:
            print(f"   {r['name']}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

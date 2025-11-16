#!/usr/bin/env python3
"""
Enhance 5 existing base images with Qwen AI
============================================
"""

import requests
import time
from datetime import datetime

COMFYUI_URL = "http://192.168.100.133:8188"

# The 5 base images we just generated
BASE_IMAGES = [
    "blonde_athletic_base_20251116_051333.png",
    "brunette_yoga_base_20251116_051348.png",
    "redhead_crossfit_base_20251116_051403.png",
    "blonde_running_base_20251116_051418.png",
    "brown_hair_pilates_base_20251116_051433.png",
]

NAMES = [
    "Blonde Athletic",
    "Brunette Yoga",
    "Redhead Crossfit",
    "Blonde Running",
    "Brown Hair Pilates",
]


def qwen_enhance(base_local_file, variation_name, use_lightning=True):
    """Enhance with Qwen AI"""

    print(f"\n🤖 Enhancing {variation_name}...")

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

    # Build simple Qwen workflow
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
    """Enhance 5 base images with Qwen"""

    print("\n" + "="*80)
    print("🤖 ENHANCE 5 BASE IMAGES WITH QWEN AI")
    print("="*80)
    print("\n⚡ Using Qwen Lightning mode (4 steps, super fast!)")
    print("\n" + "="*80)

    results = []

    for i, (base_file, name) in enumerate(zip(BASE_IMAGES, NAMES)):
        print(f"\n\n{'='*80}")
        print(f"🎬 ENHANCING {i + 1}/5: {name}")
        print("="*80)

        final_file = qwen_enhance(base_file, name, use_lightning=True)

        if final_file:
            results.append({
                "name": name,
                "status": "success",
                "base": base_file,
                "final": final_file
            })
            print(f"\n✅ {name} complete!")
        else:
            results.append({
                "name": name,
                "status": "failed",
                "base": base_file,
                "final": None
            })
            print(f"\n❌ {name} enhancement failed")

    # Summary
    print("\n\n" + "="*80)
    print("🎉 ALL 5 ENHANCEMENTS COMPLETE!")
    print("="*80)

    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']

    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {len(successful)}/5")
    print(f"   ❌ Failed: {len(failed)}/5")

    if successful:
        print(f"\n✨ Successful Enhancements:")
        for r in successful:
            print(f"\n   {r['name']}:")
            print(f"      Base:  {r['base']}")
            print(f"      Final: {r['final']}")

    if failed:
        print(f"\n❌ Failed Enhancements:")
        for r in failed:
            print(f"   {r['name']}: {r['base']}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

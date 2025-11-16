#!/usr/bin/env python3
"""
QWEN IMAGE EDIT 2509 - Fitness Influencer Eye Inpainting Test
==============================================================

This tests the NEW Qwen-Image-Edit-2509 GGUF model for inpainting.
Superior quality to traditional SD inpainting!

Features:
- State-of-the-art 20B parameter vision-language model
- Better context understanding
- More natural edits
- 4-step Lightning mode for speed (optional)
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_qwen_inpaint_workflow
import requests
import time
from datetime import datetime
from PIL import Image, ImageDraw

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"


class QwenInpaintRequest:
    """Request object for Qwen inpainting workflow"""
    def __init__(self, prompt, base_image, mask_image=None, negative_prompt="", use_lightning=False):
        self.prompt = prompt
        self.base_image = base_image
        self.mask_image = mask_image
        self.negative_prompt = negative_prompt
        self.use_lightning = use_lightning
        self.steps = 4 if use_lightning else 20
        self.cfg = 2.5


def generate_base_image():
    """Stage 1: Generate base fitness influencer"""

    payload = {
        "prompt": (
            "beautiful 23 year old woman, fitness influencer, athletic physique, "
            "blonde hair in ponytail, bright smile, confident expression, "
            "wearing stylish black athletic wear, sports bra and leggings, "
            "at modern gym with equipment in background, "
            "natural lighting, professional fitness photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),
        "negative_prompt": (
            "ugly, old, deformed, bad anatomy, bad proportions, "
            "bad face, distorted face, "
            "blurry, low quality, jpeg artifacts, "
            "cartoon, anime, painting, sketch, "
            "nude, nsfw"
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
    print("🎨 STAGE 1: GENERATING BASE IMAGE")
    print("="*80)
    print("\n👤 Subject: 23-year-old fitness influencer")
    print("🚀 Generating base image...")

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
                                output_file = f"qwen_base_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                print(f"\n✅ Complete in {elapsed}s!")
                                print(f"📁 File: {output_file}")
                                print(f"🌐 URL: {url}")

                                return output_file, filename

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout")
        return None, None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None, None


def create_eye_mask(image_path):
    """Stage 2: Create eye mask for surgical precision"""

    print("\n" + "="*80)
    print("🎭 STAGE 2: CREATING EYE MASK")
    print("="*80)

    img = Image.open(image_path)
    width, height = img.size

    # Create RGB mask (white = edit, black = keep)
    mask = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(mask)

    # Eye region (upper face)
    eye_top = int(height * 0.28)
    eye_bottom = int(height * 0.38)
    eye_left = int(width * 0.22)
    eye_right = int(width * 0.78)

    draw.ellipse([eye_left, eye_top, eye_right, eye_bottom], fill=(255, 255, 255))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_file = f"qwen_mask_{timestamp}.png"
    mask.save(mask_file)

    print(f"✅ Mask created: {mask_file}")

    # Upload mask to ComfyUI
    with open(mask_file, 'rb') as f:
        files = {'image': (mask_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        mask_upload = response.json()
        mask_name = mask_upload.get('name', mask_file)

    print(f"✅ Uploaded to ComfyUI: {mask_name}")

    return mask_file, mask_name


def qwen_inpaint_eyes(base_local_file, base_filename, mask_name, use_lightning=False):
    """Stage 3: QWEN inpainting - AI-powered eye fixing!"""

    print("\n" + "="*80)
    print("🤖 STAGE 3: QWEN AI IMAGE EDITING")
    print("="*80)

    mode = "⚡ Lightning (4 steps)" if use_lightning else "🎨 Quality (20 steps)"
    print(f"\n✨ Mode: {mode}")
    print("\n🧠 Using Qwen-Image-Edit-2509:")
    print("   • 20B parameter vision-language model")
    print("   • Natural language understanding")
    print("   • Context-aware editing")
    print("   • Superior quality vs traditional inpainting")

    # Upload base image to ComfyUI input folder
    print(f"\n📤 Uploading base image to ComfyUI...")
    with open(base_local_file, 'rb') as f:
        files = {'image': (base_local_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        base_upload = response.json()
        base_comfy_name = base_upload.get('name', base_local_file)

    print(f"✅ Base uploaded as: {base_comfy_name}")

    # Create Qwen inpaint request (natural language instruction!)
    inpaint_req = QwenInpaintRequest(
        prompt="Make the eyes clear, bright, and symmetrical with perfect focus and natural appearance",
        base_image=base_comfy_name,
        mask_image=mask_name,
        negative_prompt="blurry eyes, crossed eyes, asymmetrical eyes, unfocused eyes, weird pupils",
        use_lightning=use_lightning
    )

    # Build Qwen inpainting workflow
    workflow = build_qwen_inpaint_workflow(inpaint_req)

    print("\n🚀 Submitting Qwen workflow to ComfyUI...")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)

        # Check for errors
        if response.status_code != 200:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            print("\n💡 Debugging info:")
            print(f"   Base image: {base_comfy_name}")
            print(f"   Mask image: {mask_name}")
            print(f"   Use Lightning: {use_lightning}")
            return None

        response.raise_for_status()
        result = response.json()

        prompt_id = result['prompt_id']
        print(f"✅ Queued: {prompt_id}")

        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)
            print(f"\r⏳ Qwen editing... {elapsed}s", end="", flush=True)

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
                                mode_suffix = "lightning" if use_lightning else "quality"
                                output_file = f"qwen_inpaint_{mode_suffix}_{timestamp}.png"

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

        print(f"\n⏰ Timeout")
        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Complete Qwen inpainting workflow"""

    print("\n" + "="*80)
    print("🤖 QWEN-IMAGE-EDIT-2509 INPAINTING TEST")
    print("="*80)
    print("\n✨ Testing State-of-the-Art AI Image Editing:")
    print("   1. Generate base fitness influencer image")
    print("   2. Create precision eye mask")
    print("   3. Use Qwen AI to fix eyes (natural language!)")
    print("\n🎯 Comparing Quality vs Lightning modes")
    print("="*80)

    # Stage 1: Generate base
    base_file, base_comfy_name = generate_base_image()
    if not base_file:
        print("\n❌ Base generation failed")
        return

    # Stage 2: Create and upload mask
    mask_file, mask_comfy_name = create_eye_mask(base_file)

    # Stage 3a: Qwen Quality mode (20 steps)
    print("\n" + "="*80)
    print("📊 TEST 1: QUALITY MODE")
    print("="*80)
    final_quality = qwen_inpaint_eyes(base_file, base_comfy_name, mask_comfy_name, use_lightning=False)

    # Stage 3b: Qwen Lightning mode (4 steps)
    print("\n" + "="*80)
    print("📊 TEST 2: LIGHTNING MODE")
    print("="*80)
    final_lightning = qwen_inpaint_eyes(base_file, base_comfy_name, mask_comfy_name, use_lightning=True)

    # Summary
    print("\n" + "="*80)
    print("🎉 QWEN INPAINTING COMPLETE!")
    print("="*80)

    if final_quality or final_lightning:
        print(f"\n📊 Results:")
        print(f"   Base image: {base_file}")
        print(f"   Eye mask: {mask_file}")
        if final_quality:
            print(f"   Quality mode: {final_quality}")
        if final_lightning:
            print(f"   Lightning mode: {final_lightning}")

        print(f"\n✨ Compare the results:")
        print(f"   • Base: Original generation")
        print(f"   • Quality: 20 steps, best quality")
        print(f"   • Lightning: 4 steps, fast generation")
        print(f"   • Both should have perfectly fixed eyes!")
    else:
        print(f"\n⚠️  Qwen workflow had issues")
        print(f"   Base image saved: {base_file}")
        print(f"   Mask created: {mask_file}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

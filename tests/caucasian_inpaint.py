#!/usr/bin/env python3
"""
Brown-Haired Youth Fitness Influencer - TRUE Inpainting
========================================================

Complete workflow for generating a young brown-haired fitness influencer with perfect eyes.
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_inpaint_workflow
import requests
import time
from datetime import datetime
from PIL import Image, ImageDraw

COMFYUI_URL = "http://192.168.100.133:8188"


class InpaintRequest:
    """Request object for inpainting workflow"""
    def __init__(self, prompt, base_image, mask_image, negative_prompt="", denoise=0.75):
        self.prompt = prompt
        self.base_image = base_image
        self.mask_image = mask_image
        self.negative_prompt = negative_prompt
        self.denoise = denoise
        self.steps = 60
        self.cfg = 7.0
        self.sampler_name = "dpmpp_2m"
        self.scheduler = "karras"


def generate_base_caucasian():
    """Stage 1: Generate young brown-haired fitness influencer"""

    API_URL = "http://192.168.100.133:8000/avatarforge-controller"

    payload = {
        "prompt": (
            "beautiful young woman, 20 years old, fitness influencer, athletic physique, "
            "long brown hair in ponytail, youthful face, bright smile, confident expression, "
            "clear sharp symmetrical eyes, focused eyes, bright eyes, detailed eyes, "
            "wearing stylish black athletic wear, sports bra and leggings, "
            "at modern gym with equipment in background, "
            "natural lighting, professional fitness photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),

        "negative_prompt": (
            "ugly, old, mature, aged, deformed, distorted, disfigured, bad anatomy, wrong anatomy, "
            "blonde, blonde hair, red hair, black hair, "
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
        ),

        "clothing": "black athletic wear, sports bra, leggings",
        "realism": True,

        # Optimized settings for photorealism
        "width": 768,
        "height": 1024,
        "steps": 50,
        "cfg": 7.0,
        "sampler_name": "dpmpp_2m_karras",
        "scheduler": "karras",
    }

    print("\n" + "="*80)
    print("🎨 STAGE 1: GENERATING BROWN-HAIRED FITNESS INFLUENCER")
    print("="*80)
    print("\n👤 Subject: Young woman, 20 years old, brown hair")
    print("⚙️  Settings: 768x1024, 50 steps, CFG 7.0, dpmpp_2m_karras")
    print("🎯 Goal: Photorealistic with enhanced prompts")
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
                                output_file = f"caucasian_base_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print(f"\n✅ Complete in {elapsed}s!")
                                print(f"📁 File: {output_file}")
                                print(f"💾 Size: {size_mb:.2f} MB")
                                print(f"🌐 URL: {url}")

                                # Also save for ComfyUI upload
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
    """Stage 2: Create precision mask for eyes"""

    print("\n" + "="*80)
    print("🎭 STAGE 2: CREATING PRECISION EYE MASK")
    print("="*80)
    print("\n⚙️  Analyzing face proportions...")

    img = Image.open(image_path)
    width, height = img.size

    # Create mask (RGB for ComfyUI compatibility)
    mask = Image.new('RGB', (width, height), (0, 0, 0))  # Black background
    draw = ImageDraw.Draw(mask)

    # Eye region coordinates (optimized for portrait)
    eye_top = int(height * 0.28)
    eye_bottom = int(height * 0.38)
    eye_left = int(width * 0.22)
    eye_right = int(width * 0.78)

    # Draw white ellipse for eye region
    draw.ellipse(
        [eye_left, eye_top, eye_right, eye_bottom],
        fill=(255, 255, 255)
    )

    # Save mask
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_file = f"caucasian_eye_mask_{timestamp}.png"
    mask.save(mask_file)

    print(f"✅ Precision mask created: {mask_file}")
    print(f"   Region: Eye area (28-38% from top)")
    print(f"   Size: {width}x{height}")

    # Upload mask to ComfyUI
    print(f"\n📤 Uploading mask to ComfyUI...")
    with open(mask_file, 'rb') as f:
        files = {'image': (mask_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        mask_upload = response.json()
        mask_name = mask_upload.get('name', mask_file)

    print(f"✅ Uploaded to ComfyUI: {mask_name}")

    return mask_file, mask_name


def inpaint_eyes(base_local_file, base_comfy_name, mask_name):
    """Stage 3: TRUE inpainting - fix only the eyes"""

    print("\n" + "="*80)
    print("👁️  STAGE 3: INPAINTING EYES (TRUE INPAINTING)")
    print("="*80)
    print("\n🎯 Using surgical inpainting:")
    print("   • Only changes eye region")
    print("   • Preserves everything else")
    print("   • 60 steps for maximum quality")
    print("   • Denoise 0.75 (keeps 25% original)")

    # Upload base image to ComfyUI input folder
    print(f"\n📤 Uploading base image to ComfyUI...")
    with open(base_local_file, 'rb') as f:
        files = {'image': (base_local_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        base_upload = response.json()
        base_upload_name = base_upload.get('name', base_local_file)

    print(f"✅ Base uploaded as: {base_upload_name}")

    # Create inpaint request
    inpaint_req = InpaintRequest(
        prompt="detailed clear bright eyes, sharp symmetrical eyes, focused pupils, realistic human eyes, perfect eye details, natural eye color, photorealistic eyes, 8k detail",
        base_image=base_upload_name,
        mask_image=mask_name,
        negative_prompt="blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes, lazy eye, uneven eyes, bad eyes, crossed eyes, distorted eyes, closed eyes",
        denoise=0.75
    )

    # Build inpainting workflow
    workflow = build_inpaint_workflow(inpaint_req)

    print("\n🚀 Submitting inpainting workflow to ComfyUI...")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)
        response.raise_for_status()
        result = response.json()

        prompt_id = result['prompt_id']
        print(f"✅ Queued: {prompt_id}")

        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)
            print(f"\r⏳ Inpainting... {elapsed}s", end="", flush=True)

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
                                output_file = f"caucasian_FINAL_{timestamp}.png"

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
    """Complete workflow: Generate + Inpaint"""

    print("\n" + "="*80)
    print("👩 CAUCASIAN WOMAN (20s) FITNESS INFLUENCER")
    print("="*80)
    print("\n🎯 Complete Workflow:")
    print("   1. Generate base image (young, brown hair)")
    print("   2. Create precision eye mask")
    print("   3. Inpaint eyes with TRUE inpainting")
    print("\n✨ Result: Perfect eyes, professional quality")
    print("\n" + "="*80)

    # Stage 1: Generate base
    base_file, base_comfy_name = generate_base_caucasian()

    if not base_file:
        print("\n❌ Base generation failed")
        return

    # Stage 2: Create and upload mask
    mask_file, mask_comfy_name = create_eye_mask(base_file)

    # Stage 3: Inpaint eyes
    final_file = inpaint_eyes(base_file, base_comfy_name, mask_comfy_name)

    # Summary
    print("\n" + "="*80)
    print("🎉 BROWN-HAIRED INFLUENCER COMPLETE!")
    print("="*80)

    if final_file:
        print(f"\n📊 Results:")
        print(f"   Base image: {base_file}")
        print(f"   Eye mask: {mask_file}")
        print(f"   Final result: {final_file}")

        print(f"\n✨ Features:")
        print(f"   • Age: ~20 years old (youthful)")
        print(f"   • Hair: Long brown hair in ponytail")
        print(f"   • Type: Fitness influencer")
        print(f"   • Quality: Photorealistic")
        print(f"   • Eyes: Enhanced with TRUE inpainting")
        print(f"   • Model: Realistic Vision v5.1")

        print(f"\n💡 Compare the images:")
        print(f"   Base: {base_file}")
        print(f"   Final (perfect eyes): {final_file}")
    else:
        print(f"\n⚠️  Inpainting failed")
        print(f"   Base image saved: {base_file}")
        print(f"   Mask created: {mask_file}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

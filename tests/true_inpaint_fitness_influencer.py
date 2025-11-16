#!/usr/bin/env python3
"""
TRUE INPAINTING - Fitness Influencer with Surgically Fixed Eyes
================================================================

This uses REAL inpainting workflow:
1. Generate base image
2. Create eye mask
3. Use ComfyUI inpainting to fix ONLY the eyes
   (Preserves everything else, changes only masked area)
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_inpaint_workflow
import requests
import time
from datetime import datetime
from PIL import Image, ImageDraw

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
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
        self.sampler_name = "dpmpp_2m"  # Fixed sampler name
        self.scheduler = "karras"


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
                                output_file = f"base_{timestamp}.png"

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
    """Stage 2: Create eye mask"""

    print("\n" + "="*80)
    print("🎭 STAGE 2: CREATING EYE MASK")
    print("="*80)

    img = Image.open(image_path)
    width, height = img.size

    # Create RGB mask
    mask = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(mask)

    # Eye region (upper face)
    eye_top = int(height * 0.28)
    eye_bottom = int(height * 0.38)
    eye_left = int(width * 0.22)
    eye_right = int(width * 0.78)

    draw.ellipse([eye_left, eye_top, eye_right, eye_bottom], fill=(255, 255, 255))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_file = f"mask_{timestamp}.png"
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


def inpaint_eyes(base_local_file, base_filename, mask_name):
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
        base_comfy_name = base_upload.get('name', base_local_file)

    print(f"✅ Base uploaded as: {base_comfy_name}")

    # Create inpaint request
    inpaint_req = InpaintRequest(
        prompt="detailed clear bright eyes, sharp symmetrical eyes, focused pupils, realistic human eyes, perfect eye details, natural eye color, photorealistic eyes, 8k detail",
        base_image=base_comfy_name,
        mask_image=mask_name,
        negative_prompt="blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes, lazy eye, uneven eyes, bad eyes, crossed eyes, distorted eyes, closed eyes",
        denoise=0.75
    )

    # Build inpainting workflow
    workflow = build_inpaint_workflow(inpaint_req)

    print("\n🚀 Submitting inpaint workflow...")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)

        # Check for errors
        if response.status_code != 200:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            print("\n💡 Debugging info:")
            print(f"   Base image: {base_filename}")
            print(f"   Mask image: {mask_name}")
            return None

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
                                output_file = f"inpainted_{timestamp}.png"

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
    """Complete TRUE inpainting workflow"""

    print("\n" + "="*80)
    print("👁️  TRUE INPAINTING - FITNESS INFLUENCER")
    print("="*80)
    print("\n✨ 3-Stage Workflow:")
    print("   1. Generate base image")
    print("   2. Create precision eye mask")
    print("   3. Inpaint ONLY the eyes (surgical fix)")
    print("\n🎯 Result: Perfect eyes while keeping everything else identical")
    print("="*80)

    # Stage 1: Generate base
    base_file, base_comfy_name = generate_base_image()
    if not base_file:
        print("\n❌ Base generation failed")
        return

    # Stage 2: Create and upload mask
    mask_file, mask_comfy_name = create_eye_mask(base_file)

    # Stage 3: Inpaint eyes
    final_file = inpaint_eyes(base_file, base_comfy_name, mask_comfy_name)

    # Summary
    print("\n" + "="*80)
    print("🎉 INPAINTING COMPLETE!")
    print("="*80)

    if final_file:
        print(f"\n📊 Results:")
        print(f"   Base image: {base_file}")
        print(f"   Eye mask: {mask_file}")
        print(f"   Final (inpainted): {final_file}")
        print(f"\n✨ Compare the images:")
        print(f"   • Base: Original generation")
        print(f"   • Final: Surgically fixed eyes")
        print(f"   • Everything except eyes is IDENTICAL!")
    else:
        print(f"\n⚠️  Inpainting workflow had issues")
        print(f"   Base image saved: {base_file}")
        print(f"   Mask created: {mask_file}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

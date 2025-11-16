#!/usr/bin/env python3
"""
Inpainting Eye Fix - Two-Stage Generation
==========================================

Stage 1: Generate full image
Stage 2: Inpaint/fix eyes specifically with focused prompt

This approach gives you:
- Full control over the base image
- Ability to fix JUST the eyes without regenerating everything
- Higher quality eyes with focused inpainting
"""

import requests
import time
import base64
from datetime import datetime
from PIL import Image, ImageDraw
import io

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"


def generate_base_image():
    """Stage 1: Generate the full base image"""

    payload = {
        "prompt": (
            "Caucasian woman, blonde hair, confident expression, wearing black workout set, at modern gym, "
            "clear sharp symmetrical eyes, focused eyes, bright eyes, detailed eyes, "
            "natural lighting, professional fitness photography, authentic, sharp focus, high quality, realistic, 4k"
        ),
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
    print("\n⚙️  Settings: 768x1024, 50 steps, CFG 7.0")
    print("🚀 Starting generation...")

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
                                output_file = f"base_image_{timestamp}.png"

                                with open(output_file, "wb") as f:
                                    f.write(img_data)

                                size_mb = len(img_data) / (1024*1024)

                                print(f"\n✅ Complete in {elapsed}s!")
                                print(f"📁 File: {output_file}")
                                print(f"💾 Size: {size_mb:.2f} MB")
                                print(f"🌐 URL: {url}")

                                return output_file, img_data

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout")
        return None, None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None, None


def create_eye_mask(image_path):
    """Create a mask for the eye region"""

    print("\n" + "="*80)
    print("🎭 CREATING EYE MASK")
    print("="*80)
    print("\n⚙️  Generating mask for eye region...")

    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Create a mask (white = inpaint, black = keep)
    mask = Image.new('L', (width, height), 0)  # Start with black (keep everything)
    draw = ImageDraw.Draw(mask)

    # Draw white ellipse over eye region
    # Eyes are typically in upper-middle third of portrait
    # Adjust these coordinates based on typical face position
    eye_region_top = int(height * 0.25)
    eye_region_bottom = int(height * 0.40)
    eye_region_left = int(width * 0.20)
    eye_region_right = int(width * 0.80)

    # Draw ellipse for eye region
    draw.ellipse(
        [eye_region_left, eye_region_top, eye_region_right, eye_region_bottom],
        fill=255  # White = area to inpaint
    )

    # Save mask
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_file = f"eye_mask_{timestamp}.png"
    mask.save(mask_file)

    print(f"✅ Mask created: {mask_file}")
    print(f"   Region: eyes area (upper face)")

    return mask_file


def inpaint_eyes(base_image_path, mask_path):
    """Stage 2: Inpaint only the eye region with focused prompt"""

    print("\n" + "="*80)
    print("👁️  STAGE 2: INPAINTING EYES")
    print("="*80)
    print("\n⚙️  Focused eye repair with inpainting...")

    # Read and encode image and mask
    with open(base_image_path, 'rb') as f:
        base_image_b64 = base64.b64encode(f.read()).decode('utf-8')

    with open(mask_path, 'rb') as f:
        mask_b64 = base64.b64encode(f.read()).decode('utf-8')

    # Inpainting payload - focused ONLY on eyes
    payload = {
        "prompt": (
            "detailed clear bright eyes, sharp symmetrical eyes, focused pupils, "
            "realistic human eyes, perfect eye details, natural eye color, "
            "professional photography, high resolution, 8k detail"
        ),
        "negative_prompt": (
            "blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes, "
            "lazy eye, uneven eyes, bad eyes, crossed eyes, distorted eyes, "
            "multiple pupils, strange eyes, deformed eyes"
        ),
        "base_image": f"data:image/png;base64,{base_image_b64}",
        "mask_image": f"data:image/png;base64,{mask_b64}",
        "realism": True,
        "width": 768,
        "height": 1024,
        "steps": 60,  # More steps for quality inpainting
        "cfg": 7.0,
        "sampler_name": "dpmpp_2m_karras",
        "scheduler": "karras",
        "denoise": 0.75,  # Partial denoise - keeps most of original, fixes eyes
    }

    print("🎯 Inpainting parameters:")
    print(f"   Focus: Eye region only")
    print(f"   Steps: 60 (high quality)")
    print(f"   Denoise: 0.75 (balanced)")
    print(f"\n🚀 Starting inpaint...")

    try:
        # Note: This would need an inpaint endpoint in your API
        # For now, let's show what the request would look like
        print("\n⚠️  NOTE: Inpainting requires an inpaint-specific endpoint")
        print("📝 Payload prepared for inpainting:")
        print(f"   - Base image: {base_image_path}")
        print(f"   - Mask: {mask_path}")
        print(f"   - Prompt: Focus on eyes")
        print(f"   - Denoise: 0.75")

        # TODO: Implement actual inpaint endpoint call
        # response = requests.post(f"{API_URL}/inpaint", json=payload, timeout=30)

        print("\n💡 To implement inpainting, you need to:")
        print("   1. Add inpaint workflow to ComfyUI")
        print("   2. Create /inpaint endpoint in AvatarForge API")
        print("   3. Use VAEDecode + InpaintModelConditioning nodes")

        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def main():
    """Full inpainting workflow"""

    print("\n" + "="*80)
    print("👁️  INPAINTING EYE FIX - TWO-STAGE GENERATION")
    print("="*80)
    print("\n🎯 Workflow:")
    print("   1. Generate full base image")
    print("   2. Create mask for eye region")
    print("   3. Inpaint ONLY the eyes with focused prompt")
    print("\n💡 Benefit: Fix eyes without regenerating entire image\n")

    # Stage 1: Generate base
    base_image, img_data = generate_base_image()

    if not base_image:
        print("\n❌ Failed to generate base image")
        return

    # Stage 2: Create mask
    mask_file = create_eye_mask(base_image)

    # Stage 3: Inpaint eyes
    final_image = inpaint_eyes(base_image, mask_file)

    print("\n" + "="*80)
    print("📊 WORKFLOW SUMMARY")
    print("="*80)
    print(f"\n✅ Base image generated: {base_image}")
    print(f"✅ Eye mask created: {mask_file}")
    print(f"\n⚠️  Inpainting endpoint needs to be implemented")
    print("\nNext steps:")
    print("1. Review base image and mask")
    print("2. Implement inpaint workflow in ComfyUI")
    print("3. Add /inpaint endpoint to AvatarForge API")
    print("4. Re-run this script to complete eye fix\n")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

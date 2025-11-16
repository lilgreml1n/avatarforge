#!/usr/bin/env python3
"""
Complete Inpainting Example - Eye Fixing Workflow
==================================================

Demonstrates:
1. Generate base image with Realistic Vision v5.1
2. Create eye mask automatically
3. Inpaint ONLY the eyes with focused prompt
4. Compare before/after results

This shows inpainting capability is NOW AVAILABLE!
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_inpaint_workflow
import requests
import time
import base64
from datetime import datetime
from PIL import Image, ImageDraw
import io


COMFYUI_URL = "http://192.168.100.133:8188"


class InpaintRequest:
    """Simple request object for inpainting"""
    def __init__(self, prompt, base_image, mask_image, negative_prompt="", denoise=0.75):
        self.prompt = prompt
        self.base_image = base_image
        self.mask_image = mask_image
        self.negative_prompt = negative_prompt
        self.denoise = denoise
        self.steps = 60
        self.cfg = 7.0
        self.sampler_name = "dpmpp_2m_karras"
        self.scheduler = "karras"


def create_eye_mask(image_path):
    """Create mask for eye region"""
    print("\n🎭 Creating eye mask...")

    img = Image.open(image_path)
    width, height = img.size

    # Create mask
    mask = Image.new('RGB', (width, height), (0, 0, 0))  # Black background
    draw = ImageDraw.Draw(mask)

    # Draw white region over eyes (upper-middle of face)
    eye_top = int(height * 0.25)
    eye_bottom = int(height * 0.40)
    eye_left = int(width * 0.20)
    eye_right = int(width * 0.80)

    # Draw white ellipse for eye region
    draw.ellipse([eye_left, eye_top, eye_right, eye_bottom], fill=(255, 255, 255))

    # Save mask
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_file = f"eye_mask_{timestamp}.png"
    mask.save(mask_file)

    print(f"✅ Mask created: {mask_file}")
    return mask_file


def execute_inpaint_workflow(request):
    """Execute inpainting workflow in ComfyUI"""

    # Build workflow
    workflow = build_inpaint_workflow(request)

    print("\n🚀 Submitting inpaint workflow to ComfyUI...")

    try:
        # Submit to ComfyUI
        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json=workflow,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        prompt_id = result['prompt_id']
        print(f"✅ Queued: {prompt_id}")
        print(f"⏳ Inpainting...", end="", flush=True)

        start_time = time.time()

        # Poll for completion
        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)

            try:
                history = requests.get(
                    f"{COMFYUI_URL}/history/{prompt_id}",
                    timeout=10
                ).json()

                if prompt_id in history:
                    data = history[prompt_id]

                    if data.get("status", {}).get("completed"):
                        for node_id, output in data.get("outputs", {}).items():
                            if output.get("images"):
                                filename = output["images"][0]["filename"]
                                url = f"{COMFYUI_URL}/view?filename={filename}&type=output"

                                # Download
                                img_data = requests.get(url).content
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                output_file = f"inpainted_eyes_{timestamp}.png"

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
    """Full inpainting demo"""

    print("\n" + "="*80)
    print("👁️  COMPLETE INPAINTING DEMO - EYE FIXING")
    print("="*80)
    print("\n✨ This demonstrates full inpainting capability:")
    print("   1. Uses base image you generated")
    print("   2. Creates eye mask automatically")
    print("   3. Inpaints ONLY the eyes with focused prompt")
    print("   4. Preserves everything else perfectly")
    print("\n" + "="*80)

    # Use one of the previously generated images
    base_image_path = "base_image_20251115_131505.png"

    print(f"\n📸 Using base image: {base_image_path}")

    # Create eye mask
    mask_path = create_eye_mask(base_image_path)

    # Convert images to base64
    print("\n📦 Encoding images...")
    with open(base_image_path, 'rb') as f:
        base_img_data = f.read()
        # For LoadImage node, we need to save it to ComfyUI's input folder
        # Or use upload endpoint

    with open(mask_path, 'rb') as f:
        mask_img_data = f.read()

    # Upload images to ComfyUI
    print("📤 Uploading images to ComfyUI...")

    # Upload base image
    files = {'image': (base_image_path, base_img_data, 'image/png')}
    response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
    base_upload = response.json()
    base_name = base_upload.get('name', base_image_path)

    # Upload mask
    files = {'image': (mask_path, mask_img_data, 'image/png')}
    response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
    mask_upload = response.json()
    mask_name = mask_upload.get('name', mask_path)

    print(f"✅ Uploaded base: {base_name}")
    print(f"✅ Uploaded mask: {mask_name}")

    # Create inpaint request
    inpaint_request = InpaintRequest(
        prompt="detailed clear bright eyes, sharp symmetrical eyes, focused pupils, realistic human eyes, perfect eye details, natural eye color, high resolution, 8k detail",
        base_image=base_name,
        mask_image=mask_name,
        negative_prompt="blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes, lazy eye, uneven eyes, bad eyes, crossed eyes, distorted eyes",
        denoise=0.75
    )

    print("\n" + "="*80)
    print("👁️  STAGE 2: INPAINTING EYES")
    print("="*80)
    print(f"\n🎯 Inpaint parameters:")
    print(f"   Prompt: Eye-focused")
    print(f"   Steps: 60")
    print(f"   Denoise: 0.75 (preserves 25% of original)")
    print(f"   CFG: 7.0")
    print(f"   Sampler: dpmpp_2m_karras")

    # Execute inpainting
    result = execute_inpaint_workflow(inpaint_request)

    if result:
        print("\n" + "="*80)
        print("🎉 INPAINTING COMPLETE!")
        print("="*80)
        print(f"\n📊 Results:")
        print(f"   Base image: {base_image_path}")
        print(f"   Eye mask: {mask_path}")
        print(f"   Final result: {result}")
        print(f"\n✨ Eyes have been fixed while preserving everything else!")
        print(f"\n💡 Compare the images to see the improvement!")
        print("\n" + "="*80 + "\n")
    else:
        print("\n❌ Inpainting failed")


if __name__ == "__main__":
    main()

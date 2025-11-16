#!/usr/bin/env python3
"""
QWEN AI ENHANCEMENT - Brown Hair Fitness Influencer
====================================================

Use Qwen-Image-Edit-2509 to enhance the existing brown-haired fitness influencer!
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_qwen_inpaint_workflow
import requests
import time
from datetime import datetime
from PIL import Image, ImageDraw

COMFYUI_URL = "http://192.168.100.133:8188"


class QwenInpaintRequest:
    """Request object for Qwen inpainting workflow"""
    def __init__(self, prompt, base_image, mask_image=None, negative_prompt="", use_lightning=True):
        self.prompt = prompt
        self.base_image = base_image
        self.mask_image = mask_image
        self.negative_prompt = negative_prompt
        self.use_lightning = use_lightning
        self.steps = 4 if use_lightning else 20
        self.cfg = 2.5


def create_face_mask(image_path):
    """Create a face region mask for enhancement"""

    print("\n" + "="*80)
    print("🎭 CREATING FACE ENHANCEMENT MASK")
    print("="*80)

    img = Image.open(image_path)
    width, height = img.size

    # Create RGB mask (white = enhance, black = keep)
    mask = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(mask)

    # Face region (upper portion including eyes, nose, mouth)
    face_top = int(height * 0.15)
    face_bottom = int(height * 0.50)
    face_left = int(width * 0.20)
    face_right = int(width * 0.80)

    draw.ellipse([face_left, face_top, face_right, face_bottom], fill=(255, 255, 255))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mask_file = f"qwen_face_mask_{timestamp}.png"
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


def qwen_enhance_image(base_local_file, mask_name=None, use_lightning=True):
    """Qwen AI Enhancement"""

    print("\n" + "="*80)
    print("🤖 QWEN AI IMAGE ENHANCEMENT")
    print("="*80)

    mode = "⚡ Lightning (4 steps)" if use_lightning else "🎨 Quality (20 steps)"
    print(f"\n✨ Mode: {mode}")
    print("\n🧠 Using Qwen-Image-Edit-2509 (20B parameters):")
    print("   • State-of-the-art vision-language model")
    print("   • Natural language understanding")
    print("   • Context-aware editing")
    print("   • Superior quality vs traditional methods")

    # Upload base image to ComfyUI input folder
    print(f"\n📤 Uploading base image to ComfyUI...")
    with open(base_local_file, 'rb') as f:
        files = {'image': (base_local_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        base_upload = response.json()
        base_comfy_name = base_upload.get('name', base_local_file)

    print(f"✅ Base uploaded as: {base_comfy_name}")

    # Create Qwen enhancement request with natural language!
    enhancement_prompt = (
        "Enhance the facial features to be more detailed and photorealistic. "
        "Make the eyes crystal clear, bright, and perfectly symmetrical. "
        "Improve skin texture and lighting. "
        "Make the face more detailed and natural looking."
    )

    inpaint_req = QwenInpaintRequest(
        prompt=enhancement_prompt,
        base_image=base_comfy_name,
        mask_image=mask_name,  # Can be None for full image enhancement
        negative_prompt="blurry, low quality, distorted, artificial, fake, bad anatomy, asymmetrical",
        use_lightning=use_lightning
    )

    # Build Qwen workflow
    workflow = build_qwen_inpaint_workflow(inpaint_req)

    print("\n🚀 Submitting Qwen workflow to ComfyUI...")
    print(f"💬 Prompt: {enhancement_prompt}")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)

        # Check for errors
        if response.status_code != 200:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            print("\n💡 Debugging info:")
            print(f"   Base image: {base_comfy_name}")
            if mask_name:
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
                                mode_suffix = "lightning" if use_lightning else "quality"
                                output_file = f"qwen_enhanced_{mode_suffix}_{timestamp}.png"

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
    """Qwen AI Enhancement Workflow"""

    base_image = "brown_hair_fitness_20251115_201324.png"

    print("\n" + "="*80)
    print("🤖 QWEN AI IMAGE ENHANCEMENT TEST")
    print("="*80)
    print(f"\n📸 Base Image: {base_image}")
    print("\n✨ Enhancement Plan:")
    print("   1. Upload base brown-haired fitness influencer")
    print("   2. Create face enhancement mask")
    print("   3. Use Qwen AI to enhance facial features")
    print("   4. Natural language: 'Make face more detailed and realistic'")
    print("\n🎯 Testing Lightning mode (4 steps) for speed!")
    print("="*80)

    # Create face mask for targeted enhancement
    mask_file, mask_comfy_name = create_face_mask(base_image)

    # Qwen Lightning enhancement (4 steps, super fast!)
    print("\n" + "="*80)
    print("⚡ QWEN LIGHTNING MODE TEST")
    print("="*80)
    enhanced_file = qwen_enhance_image(base_image, mask_comfy_name, use_lightning=True)

    # Summary
    print("\n" + "="*80)
    print("🎉 QWEN ENHANCEMENT COMPLETE!")
    print("="*80)

    if enhanced_file:
        print(f"\n📊 Results:")
        print(f"   Original: {base_image}")
        print(f"   Face mask: {mask_file}")
        print(f"   Enhanced (Qwen AI): {enhanced_file}")
        print(f"\n✨ Compare the images:")
        print(f"   • Original: Brown-haired fitness influencer")
        print(f"   • Enhanced: AI-improved facial features with Qwen-2509")
        print(f"   • Look for: Clearer eyes, better skin, more detail!")
    else:
        print(f"\n⚠️  Qwen enhancement had issues")
        print(f"   Original image: {base_image}")
        print(f"   Mask created: {mask_file}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

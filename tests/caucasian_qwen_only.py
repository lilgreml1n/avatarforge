#!/usr/bin/env python3
"""
Caucasian Woman (20s) - Qwen AI Enhancement ONLY
==================================================

Generate a Caucasian woman in her 20s and enhance with Qwen-Image-Edit-2509 AI.
This uses ONLY the Qwen model for enhancement (no traditional inpainting).
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_qwen_inpaint_workflow
import requests
import time
from datetime import datetime

COMFYUI_URL = "http://192.168.100.133:8188"
API_URL = "http://192.168.100.133:8000/avatarforge-controller"


class QwenRequest:
    """Request object for Qwen enhancement workflow"""
    def __init__(self, prompt, base_image, mask_image=None, negative_prompt="", use_lightning=True):
        self.prompt = prompt
        self.base_image = base_image
        self.mask_image = mask_image
        self.negative_prompt = negative_prompt
        self.use_lightning = use_lightning
        self.steps = 4 if use_lightning else 20
        self.cfg = 2.5


def generate_base_caucasian():
    """Step 1: Generate base Caucasian woman in her 20s"""

    payload = {
        "prompt": (
            "beautiful Caucasian woman, 20-25 years old, fitness influencer, athletic physique, "
            "long brown hair in ponytail, youthful face, bright smile, confident expression, "
            "fair skin, natural makeup, "
            "wearing stylish black athletic wear, sports bra and leggings, "
            "at modern gym with equipment in background, "
            "natural lighting, professional fitness photography, "
            "authentic, sharp focus, high quality, realistic, 4k, photorealistic"
        ),

        "negative_prompt": (
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
        ),

        "clothing": "black athletic wear, sports bra, leggings",
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
    print("🎨 STEP 1: GENERATING BASE CAUCASIAN WOMAN")
    print("="*80)
    print("\n👤 Subject: Caucasian woman, 20-25 years old, brown hair")
    print("⚙️  Settings: 768x1024, 50 steps, CFG 7.0")
    print("🎯 Model: Realistic Vision v5.1")
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

                                return output_file

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n⏰ Timeout")
        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def qwen_enhance(base_local_file, use_lightning=True):
    """Step 2: Enhance with Qwen AI"""

    print("\n" + "="*80)
    print("🤖 STEP 2: QWEN AI ENHANCEMENT")
    print("="*80)

    mode = "⚡ Lightning (4 steps)" if use_lightning else "🎨 Quality (20 steps)"
    print(f"\n✨ Mode: {mode}")
    print("\n🧠 Using Qwen-Image-Edit-2509 (20B parameters):")
    print("   • State-of-the-art vision-language model")
    print("   • Natural language understanding")
    print("   • Context-aware editing")
    print("   • Superior quality vs traditional methods")

    # Upload base image to ComfyUI
    print(f"\n📤 Uploading base image to ComfyUI...")
    with open(base_local_file, 'rb') as f:
        files = {'image': (base_local_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        base_upload = response.json()
        base_comfy_name = base_upload.get('name', base_local_file)

    print(f"✅ Uploaded as: {base_comfy_name}")

    # Natural language enhancement prompt
    enhancement_prompt = (
        "Enhance the entire image to be more photorealistic and detailed. "
        "Make the eyes crystal clear, bright, and perfectly symmetrical. "
        "Improve skin texture and lighting. "
        "Enhance facial features to look more natural and realistic. "
        "Make the overall image sharper and more professional."
    )

    qwen_req = QwenRequest(
        prompt=enhancement_prompt,
        base_image=base_comfy_name,
        mask_image=None,  # No mask = enhance entire image
        negative_prompt="blurry, low quality, distorted, artificial, fake, bad anatomy, asymmetrical eyes, cross-eyed, weird pupils, unfocused eyes",
        use_lightning=use_lightning
    )

    # Build Qwen workflow
    workflow = build_qwen_inpaint_workflow(qwen_req)

    print("\n🚀 Submitting Qwen workflow to ComfyUI...")
    print(f"💬 Prompt: {enhancement_prompt}")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)

        # Check for errors
        if response.status_code != 200:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            print("\n💡 Troubleshooting:")
            print("   1. ComfyUI needs to be restarted to load GGUF node")
            print("   2. Run: cd /home/raven/Documents/git/avatarforge && ./restart_comfyui.sh")
            print("   3. Then run this script again")
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
                                output_file = f"caucasian_qwen_{mode_suffix}_{timestamp}.png"

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
    """Qwen-only enhancement workflow"""

    print("\n" + "="*80)
    print("👩 CAUCASIAN WOMAN (20s) - QWEN AI ONLY")
    print("="*80)
    print("\n🎯 Workflow:")
    print("   1. Generate base Caucasian woman (20s, brown hair)")
    print("   2. Enhance ENTIRE image with Qwen AI (no traditional inpainting)")
    print("\n✨ Qwen Benefits:")
    print("   • Natural language: 'Make eyes clear and bright'")
    print("   • Context-aware: Understands faces and features")
    print("   • Superior quality: 20B parameter model")
    print("   • Lightning fast: 4 steps (~10 seconds)")
    print("\n" + "="*80)

    # Step 1: Generate base
    base_file = generate_base_caucasian()

    if not base_file:
        print("\n❌ Base generation failed")
        return

    # Step 2: Qwen enhancement (Lightning mode for speed)
    print("\n⚡ Using Qwen Lightning mode (4 steps, super fast!)...")
    final_file = qwen_enhance(base_file, use_lightning=True)

    # Summary
    print("\n" + "="*80)
    print("🎉 QWEN ENHANCEMENT COMPLETE!")
    print("="*80)

    if final_file:
        print(f"\n📊 Results:")
        print(f"   Base image: {base_file}")
        print(f"   Qwen enhanced: {final_file}")

        print(f"\n✨ Features:")
        print(f"   • Age: 20-25 years old")
        print(f"   • Ethnicity: Caucasian")
        print(f"   • Hair: Long brown hair")
        print(f"   • Enhancement: Qwen-Image-Edit-2509 (Lightning)")
        print(f"   • Quality: State-of-the-art AI enhancement")

        print(f"\n💡 Compare:")
        print(f"   Before: {base_file}")
        print(f"   After:  {final_file}")
        print(f"\n   Qwen enhanced: Eyes, skin, details, overall quality!")
    else:
        print(f"\n⚠️  Qwen enhancement failed")
        print(f"   Base image saved: {base_file}")
        print(f"\n🔧 This likely means ComfyUI needs to be restarted:")
        print(f"   cd /home/raven/Documents/git/avatarforge")
        print(f"   ./restart_comfyui.sh")
        print(f"\n   Then run this script again!")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

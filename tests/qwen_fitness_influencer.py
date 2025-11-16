#!/usr/bin/env python3
"""
QWEN Image Edit 2509 - Fitness Influencer with Perfect Eyes
============================================================

Using state-of-the-art Qwen-Image-Edit-2509 model:
- Natural language editing prompts
- Superior quality compared to traditional SD inpainting
- Lightning-fast 4-step inference with LoRA
- Vision-language understanding

Based on:
- Qwen Image Edit 2509 GGUF: https://huggingface.co/QuantStack/Qwen2.5-VL-7B-Instruct-GGUF
- Encoders and VAE: https://docs.comfy.org/tutorials/image_editing
- Lightning LoRA: https://huggingface.co/lightx2v/Qwen-Image-Edit-Lightning
- Workflow: https://huggingface.co/datasets/theairesearch/qwen-edit-workflows
"""

import sys
sys.path.insert(0, '/home/raven/Documents/git/avatarforge')

from avatarforge.services.workflow_builder import build_qwen_inpaint_workflow
import requests
import time
from datetime import datetime

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"


class QwenRequest:
    """Request for Qwen Image Edit"""
    def __init__(self, prompt, base_image, mask_image=None, negative_prompt="", use_lightning=True):
        self.prompt = prompt
        self.base_image = base_image
        self.mask_image = mask_image
        self.negative_prompt = negative_prompt
        self.use_lightning = use_lightning
        self.steps = 4 if use_lightning else 20
        self.cfg = 2.5


def generate_base_influencer():
    """Step 1: Generate base fitness influencer"""

    payload = {
        "prompt": (
            "beautiful 23 year old woman, fitness influencer, athletic physique, "
            "blonde hair in ponytail, confident expression, "
            "wearing black athletic wear, sports bra and leggings, "
            "at modern gym, natural lighting, professional photography, "
            "photorealistic, high quality"
        ),
        "negative_prompt": "ugly, old, deformed, low quality, blurry, cartoon, anime",
        "clothing": "black athletic wear",
        "realism": True,
        "width": 768,
        "height": 1024,
        "steps": 40,
        "cfg": 7.0,
        "sampler_name": "dpmpp_2m",
        "scheduler": "karras",
    }

    print("\n" + "="*80)
    print("🎨 STEP 1: GENERATING BASE FITNESS INFLUENCER")
    print("="*80)
    print("\n🚀 Generating with Realistic Vision v5.1...")

    try:
        response = requests.post(f"{API_URL}/generate/avatar", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        print(f"✅ Queued: {result['generation_id']}")
        start_time = time.time()

        while (time.time() - start_time) < 300:
            elapsed = int(time.time() - start_time)
            print(f"\r⏳ Generating... {elapsed}s", end="", flush=True)

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

        return None, None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None, None


def qwen_enhance_eyes(base_local_file, base_comfy_name):
    """Step 2: Use Qwen AI to enhance eyes with natural language"""

    print("\n" + "="*80)
    print("🤖 STEP 2: QWEN AI EYE ENHANCEMENT")
    print("="*80)
    print("\n✨ Using Qwen-Image-Edit-2509 (20B parameters)")
    print("   • State-of-the-art vision-language model")
    print("   • Natural language understanding")
    print("   • Lightning LoRA for 4-step inference")
    print("   • Superior quality vs traditional inpainting")

    # Upload base image
    print(f"\n📤 Uploading to ComfyUI...")
    with open(base_local_file, 'rb') as f:
        files = {'image': (base_local_file, f, 'image/png')}
        response = requests.post(f"{COMFYUI_URL}/upload/image", files=files)
        upload = response.json()
        uploaded_name = upload.get('name', base_local_file)

    print(f"✅ Uploaded as: {uploaded_name}")

    # Natural language prompt for Qwen!
    enhancement_prompt = (
        "Fix the eyes to be perfectly clear, bright, and symmetrical. "
        "Make them detailed and photorealistic with natural eye shine. "
        "Enhance facial features to look more natural and realistic."
    )

    qwen_req = QwenRequest(
        prompt=enhancement_prompt,
        base_image=uploaded_name,
        mask_image=None,  # No mask = full image enhancement
        negative_prompt="blurry eyes, cross-eyed, asymmetrical eyes, distorted, low quality, fake",
        use_lightning=True  # 4-step Lightning mode
    )

    # Build workflow
    workflow = build_qwen_inpaint_workflow(qwen_req)

    print(f"\n💬 Natural Language Prompt:")
    print(f"   '{enhancement_prompt}'")
    print(f"\n⚡ Lightning Mode: 4 steps (super fast!)")
    print(f"\n🚀 Submitting to ComfyUI...")

    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json=workflow, timeout=30)

        if response.status_code != 200:
            print(f"\n❌ Error {response.status_code}")
            print(f"Response: {response.text[:500]}")

            # Check if Qwen model is installed
            print(f"\n💡 Common issues:")
            print(f"   1. Qwen models not downloaded")
            print(f"   2. ComfyUI-GGUF node not installed")
            print(f"   3. Wrong model paths")

            return None

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
                                output_file = f"qwen_final_{timestamp}.png"

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

        return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Complete Qwen AI Workflow"""

    print("\n" + "="*80)
    print("🤖 QWEN AI FITNESS INFLUENCER - 2-STEP WORKFLOW")
    print("="*80)
    print("\n✨ Plan:")
    print("   Step 1: Generate base fitness influencer")
    print("   Step 2: Qwen AI enhances eyes with natural language")
    print("\n🎯 Result: Professional quality with perfect eyes!")
    print("="*80)

    # Step 1: Generate base
    base_file, base_comfy = generate_base_influencer()

    if not base_file:
        print("\n❌ Base generation failed")
        return

    # Step 2: Qwen enhancement
    final_file = qwen_enhance_eyes(base_file, base_comfy)

    # Summary
    print("\n" + "="*80)
    print("🎉 QWEN AI WORKFLOW COMPLETE!")
    print("="*80)

    if final_file:
        print(f"\n📊 Results:")
        print(f"   Base (SD): {base_file}")
        print(f"   Enhanced (Qwen AI): {final_file}")
        print(f"\n✨ Comparison:")
        print(f"   • Base: Generated with Realistic Vision v5.1")
        print(f"   • Final: Enhanced with Qwen-Image-Edit-2509")
        print(f"   • Method: Natural language AI editing")
        print(f"   • Speed: Lightning fast (4 steps)")
        print(f"\n💡 The Qwen version should have:")
        print(f"   • More natural, realistic eyes")
        print(f"   • Better facial detail")
        print(f"   • Professional photography quality")
    else:
        print(f"\n⚠️  Qwen enhancement failed")
        print(f"   Base image saved: {base_file}")
        print(f"\n💡 Qwen requirements:")
        print(f"   1. Download Qwen-Image-Edit-2509 GGUF model")
        print(f"   2. Install ComfyUI-GGUF custom node")
        print(f"   3. Download Qwen encoders and VAE")
        print(f"   4. Optional: Lightning LoRA for 4-step")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()

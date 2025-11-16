#!/usr/bin/env python3
"""
ENHANCED Fitness Influencer Generator for DGX Systems
======================================================

Optimized for high-quality photorealistic generation using:
- High-resolution output (up to 2048x2048+)
- Advanced sampling methods
- Quality enhancement LoRAs
- Professional-grade prompting
"""

import requests
import time
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

class EnhancedFitnessInfluencerGenerator:
    """Generate ultra-high-quality fitness influencer avatars"""

    def __init__(self):
        self.api_url = API_URL
        self.comfyui_url = COMFYUI_URL

    def check_services(self) -> bool:
        """Check if API and ComfyUI are running"""
        print("🔍 Checking services...")

        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ AvatarForge API is running")
            else:
                return False
        except Exception as e:
            print(f"❌ AvatarForge API not accessible: {e}")
            return False

        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                vram = stats.get('devices', [{}])[0].get('vram_total', 0) / (1024**3)
                print(f"✅ ComfyUI is running (GPU VRAM: {vram:.1f}GB)")
            else:
                return False
        except Exception as e:
            print(f"❌ ComfyUI not accessible: {e}")
            return False

        return True

    def generate_ultra_quality(
        self,
        preset: str = "ultra",
        style: str = "professional"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate ultra-high-quality fitness influencer

        Args:
            preset: quality preset (high, ultra, maximum)
            style: character style (professional, athletic, lifestyle)

        Returns:
            Generation response
        """

        # Enhanced character prompts with professional quality keywords
        style_prompts = {
            "professional": {
                "prompt": (
                    "masterpiece, best quality, ultra detailed, 8k uhd, professional photography, "
                    "professional fitness influencer portrait, beautiful athletic woman age 25, "
                    "perfect face, symmetrical features, confident warm smile, bright eyes, "
                    "flawless skin, healthy glow, defined athletic physique, toned abs, "
                    "fit muscular arms and legs, long ponytail hairstyle, natural makeup, "
                    "studio lighting setup, three point lighting, soft shadows, "
                    "clean white background, full body shot, motivational pose, "
                    "photorealistic, hyperrealistic, professional model photography, "
                    "sharp focus, high contrast, perfect exposure, color graded"
                ),
                "clothing": (
                    "modern premium athletic wear, designer sports bra with brand logo, "
                    "high-waist compression leggings, professional athletic sneakers, "
                    "fitness tracker watch, minimal jewelry"
                ),
                "negative": (
                    "nsfw, nude, naked, worst quality, low quality, normal quality, "
                    "lowres, blurry, out of focus, jpeg artifacts, ugly, deformed, "
                    "disfigured, bad anatomy, bad proportions, extra limbs, cloned face, "
                    "malformed limbs, missing arms, missing legs, extra arms, extra legs, "
                    "fused fingers, too many fingers, long neck, cross-eyed, "
                    "mutated hands, poorly drawn hands, poorly drawn face, mutation, "
                    "bad hands, bad fingers, watermark, signature, username, text"
                )
            },
            "athletic": {
                "prompt": (
                    "masterpiece, best quality, 8k uhd, professional sports photography, "
                    "dynamic fitness athlete in action, athletic woman mid-workout, "
                    "age 25, perfect athletic physique, muscular definition, "
                    "strong powerful pose, intense focused expression, sweat droplets, "
                    "gym environment, exercise equipment, dramatic lighting, "
                    "motion energy, powerful and inspiring, "
                    "professional photography, sharp focus, hyperrealistic"
                ),
                "clothing": (
                    "performance sportswear, athletic tank top, gym shorts, "
                    "training shoes, wrist wraps, weightlifting gloves"
                ),
                "negative": (
                    "nsfw, nude, worst quality, low quality, blurry, deformed, "
                    "bad anatomy, bad proportions, extra limbs, mutation, "
                    "watermark, signature, text"
                )
            },
            "lifestyle": {
                "prompt": (
                    "masterpiece, best quality, 8k uhd, lifestyle photography, "
                    "friendly approachable fitness coach, beautiful athletic woman age 25, "
                    "warm genuine smile, kind eyes, fit healthy physique, "
                    "natural beauty, casual athletic style, outdoor park setting, "
                    "golden hour natural lighting, soft warm tones, bokeh background, "
                    "authentic and inspiring, lifestyle magazine quality, "
                    "photorealistic, professional photography"
                ),
                "clothing": (
                    "casual fitness outfit, athletic tank top, yoga pants, "
                    "running shoes, sunglasses, water bottle"
                ),
                "negative": (
                    "nsfw, nude, worst quality, low quality, blurry, deformed, "
                    "bad anatomy, watermark, signature, text"
                )
            }
        }

        # Quality presets optimized for DGX
        quality_presets = {
            "high": {
                "width": 1024,
                "height": 1536,
                "steps": 40,
                "cfg": 7.5,
                "sampler_name": "dpmpp_2m_sde",
            },
            "ultra": {
                "width": 1280,
                "height": 1920,
                "steps": 50,
                "cfg": 8.0,
                "sampler_name": "dpmpp_2m_sde",
            },
            "maximum": {
                "width": 1536,
                "height": 2048,
                "steps": 60,
                "cfg": 8.5,
                "sampler_name": "dpmpp_3m_sde",
            }
        }

        character = style_prompts.get(style, style_prompts["professional"])
        settings = quality_presets.get(preset, quality_presets["ultra"])

        payload = {
            "prompt": character["prompt"],
            "clothing": character["clothing"],
            "realism": True,
            **settings
        }

        print("\n" + "="*80)
        print(f"🎨 GENERATING ULTRA-QUALITY FITNESS INFLUENCER")
        print("="*80)
        print(f"\n📝 Style: {style.upper()}")
        print(f"⚙️  Quality Preset: {preset.upper()}")
        print(f"📐 Resolution: {settings['width']}x{settings['height']}")
        print(f"🔢 Steps: {settings['steps']}")
        print(f"⚡ CFG Scale: {settings['cfg']}")
        print(f"🎲 Sampler: {settings['sampler_name']}")
        print(f"\n💡 Prompt (first 150 chars):")
        print(f"   {character['prompt'][:150]}...")

        print(f"\n🚀 Submitting to AvatarForge API...")

        try:
            response = requests.post(
                f"{self.api_url}/generate/avatar",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            print(f"✅ Generation queued!")
            print(f"   Generation ID: {result['generation_id']}")
            print(f"   ComfyUI Prompt ID: {result['comfyui_prompt_id']}")

            return result

        except Exception as e:
            print(f"❌ Failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   Response: {e.response.text}")
            return None

    def wait_for_completion(
        self,
        generation_id: str,
        comfyui_prompt_id: str,
        timeout: int = 600
    ) -> Optional[str]:
        """Wait for generation with progress tracking"""

        print(f"\n⏳ Waiting for generation (this may take 1-5 minutes for ultra quality)...")

        start_time = time.time()
        last_progress = -1

        while (time.time() - start_time) < timeout:
            elapsed = int(time.time() - start_time)

            try:
                # Check queue status
                queue_response = requests.get(f"{self.comfyui_url}/queue", timeout=5)
                if queue_response.status_code == 200:
                    queue_data = queue_response.json()
                    running = queue_data.get("queue_running", [])

                    if running and len(running) > 0:
                        current_item = running[0]
                        if len(current_item) >= 2:
                            prompt_info = current_item[1]
                            if comfyui_prompt_id == current_item[2]:
                                print(f"\r   ⏱️  {elapsed}s - Processing...", end="", flush=True)

                # Check history for completion
                history_response = requests.get(
                    f"{self.comfyui_url}/history/{comfyui_prompt_id}",
                    timeout=10
                )

                if history_response.status_code == 200:
                    history = history_response.json()

                    if comfyui_prompt_id in history:
                        prompt_data = history[comfyui_prompt_id]

                        # Check completion
                        if prompt_data.get("status", {}).get("completed", False):
                            outputs = prompt_data.get("outputs", {})

                            for node_id, node_output in outputs.items():
                                images = node_output.get("images", [])
                                if images:
                                    filename = images[0]["filename"]
                                    image_url = f"{self.comfyui_url}/view?filename={filename}&type=output"

                                    print(f"\n\n✅ Completed in {elapsed}s!")
                                    return image_url

                        # Check for errors
                        status = prompt_data.get("status", {})
                        if "error" in status:
                            print(f"\n\n❌ Generation failed: {status.get('error')}")
                            return None

            except Exception as e:
                pass

            time.sleep(5)

        print(f"\n\n⏰ Timeout after {timeout}s")
        return None

    def download_image(self, image_url: str, preset: str, style: str) -> Optional[str]:
        """Download the generated image"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"fitness_influencer_{preset}_{style}_{timestamp}.png"

        try:
            print(f"\n📥 Downloading ultra-quality image...")
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            size_mb = len(response.content) / (1024 * 1024)
            print(f"✅ Saved: {output_path}")
            print(f"   Size: {size_mb:.2f} MB")

            return output_path

        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None


def main():
    """Main execution"""

    print("\n" + "="*80)
    print("🏋️  ULTRA-QUALITY FITNESS INFLUENCER GENERATOR")
    print("   Optimized for DGX Systems")
    print("="*80)

    generator = EnhancedFitnessInfluencerGenerator()

    if not generator.check_services():
        print("\n❌ Services not available")
        sys.exit(1)

    print("\n📋 Quality Presets:")
    print("   • high    - 1024x1536, 40 steps (~2 min)")
    print("   • ultra   - 1280x1920, 50 steps (~3 min) [RECOMMENDED]")
    print("   • maximum - 1536x2048, 60 steps (~5 min)")

    print("\n🎨 Style Options:")
    print("   • professional - Studio portrait, clean background")
    print("   • athletic     - Gym action, dynamic workout")
    print("   • lifestyle    - Casual outdoor, natural lighting")

    # Generate with ultra quality
    result = generator.generate_ultra_quality(
        preset="ultra",      # Change to "high" or "maximum"
        style="professional" # Change to "athletic" or "lifestyle"
    )

    if not result:
        sys.exit(1)

    # Wait for completion
    image_url = generator.wait_for_completion(
        result["generation_id"],
        result["comfyui_prompt_id"],
        timeout=600
    )

    if not image_url:
        sys.exit(1)

    # Download
    output_path = generator.download_image(
        image_url,
        preset="ultra",
        style="professional"
    )

    if output_path:
        print("\n" + "="*80)
        print("🎉 ULTRA-QUALITY GENERATION COMPLETE!")
        print("="*80)
        print(f"\n🌐 View online: {image_url}")
        print(f"💾 Local file: {output_path}")
        print("\n📊 This ultra-quality image is optimized for:")
        print("   • Professional social media posts")
        print("   • High-resolution prints")
        print("   • Website hero images")
        print("   • Marketing materials")
        print("\n" + "="*80)

    print("\n✨ Done!\n")


if __name__ == "__main__":
    main()

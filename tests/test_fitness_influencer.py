#!/usr/bin/env python3
"""
Test Script: Realistic AI Fitness Influencer Generation
========================================================

This script generates a real-to-life AI fitness influencer using the AvatarForge API.
The influencer will have a realistic, professional appearance suitable for social media.

Character Profile: "FitLife Maya"
----------------------------------
- Age: Mid-20s to early 30s
- Style: Athletic, professional, motivational
- Clothing: Modern athletic wear, fitness apparel
- Setting: Gym/outdoor fitness environments
- Vibe: Energetic, confident, inspiring

"""

import requests
import time
import json
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

class FitnessInfluencerGenerator:
    """Generate realistic fitness influencer avatars"""

    def __init__(self):
        self.api_url = API_URL
        self.comfyui_url = COMFYUI_URL

    def check_services(self) -> bool:
        """Check if API and ComfyUI are running"""
        print("🔍 Checking services...")

        try:
            # Check AvatarForge API
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ AvatarForge API is running")
            else:
                print("❌ AvatarForge API returned unexpected status")
                return False
        except Exception as e:
            print(f"❌ AvatarForge API is not accessible: {e}")
            return False

        try:
            # Check ComfyUI
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            if response.status_code == 200:
                print("✅ ComfyUI is running")
            else:
                print("❌ ComfyUI returned unexpected status")
                return False
        except Exception as e:
            print(f"❌ ComfyUI is not accessible: {e}")
            return False

        return True

    def generate_influencer(
        self,
        style: str = "professional",
        quality: str = "high"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a fitness influencer avatar

        Args:
            style: professional, casual, or athletic
            quality: draft, standard, or high

        Returns:
            Generation response data
        """

        # Character prompts for different styles
        prompts = {
            "professional": {
                "prompt": "professional fitness influencer, athletic woman in mid-20s, confident smile, "
                          "toned athletic physique, healthy glowing skin, natural makeup, long ponytail hairstyle, "
                          "studio lighting, clean background, motivational pose, professional photography, "
                          "high detail, realistic, 8k quality",
                "clothing": "modern athletic wear, fitted sports bra, high-waist leggings, stylish sneakers",
            },
            "casual": {
                "prompt": "friendly fitness coach, athletic woman, warm genuine smile, fit physique, "
                          "natural beauty, casual athletic style, outdoor setting, natural lighting, "
                          "approachable and inspiring, high quality photo",
                "clothing": "tank top, yoga pants, running shoes, fitness tracker watch",
            },
            "athletic": {
                "prompt": "dynamic fitness athlete, strong athletic woman, determined expression, "
                          "muscular definition, action pose, gym environment, dramatic lighting, "
                          "powerful and inspiring, professional sports photography",
                "clothing": "performance sportswear, compression clothing, athletic sneakers, sweatbands",
            }
        }

        # Quality presets
        quality_settings = {
            "draft": {
                "width": 512,
                "height": 768,
                "steps": 20,
                "cfg": 7.0,
                "sampler_name": "euler"
            },
            "standard": {
                "width": 768,
                "height": 1024,
                "steps": 30,
                "cfg": 8.0,
                "sampler_name": "dpmpp_2m"
            },
            "high": {
                "width": 1024,
                "height": 1536,
                "steps": 40,
                "cfg": 8.5,
                "sampler_name": "dpmpp_2m"
            }
        }

        # Build request payload
        character = prompts.get(style, prompts["professional"])
        settings = quality_settings.get(quality, quality_settings["standard"])

        payload = {
            **character,
            **settings,
            "realism": True,  # Photorealistic style
            "style": None  # No art style modifier for realism
        }

        print("\n" + "="*70)
        print(f"🎨 GENERATING FITNESS INFLUENCER - '{style.upper()}' STYLE")
        print("="*70)
        print(f"\n📝 Character Details:")
        print(f"   Prompt: {character['prompt'][:100]}...")
        print(f"   Clothing: {character['clothing']}")
        print(f"\n⚙️  Generation Settings:")
        print(f"   Quality: {quality.upper()}")
        print(f"   Resolution: {settings['width']}x{settings['height']}")
        print(f"   Steps: {settings['steps']}")
        print(f"   CFG Scale: {settings['cfg']}")
        print(f"   Sampler: {settings['sampler_name']}")
        print(f"   Realism: Enabled (Photorealistic)")

        # Submit generation request
        print(f"\n🚀 Submitting generation request...")

        try:
            response = requests.post(
                f"{self.api_url}/generate/avatar",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            print(f"✅ Generation queued successfully!")
            print(f"   Generation ID: {result['generation_id']}")
            print(f"   ComfyUI Prompt ID: {result['comfyui_prompt_id']}")
            print(f"   Status: {result['status']}")

            return result

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to submit generation: {e}")
            return None

    def wait_for_completion(
        self,
        generation_id: str,
        comfyui_prompt_id: str,
        timeout: int = 300,
        check_interval: int = 5
    ) -> Optional[str]:
        """
        Wait for generation to complete and return image URL

        Args:
            generation_id: AvatarForge generation ID
            comfyui_prompt_id: ComfyUI prompt ID
            timeout: Maximum wait time in seconds
            check_interval: Seconds between status checks

        Returns:
            Image URL if successful, None otherwise
        """
        print(f"\n⏳ Waiting for generation to complete...")
        print(f"   Checking every {check_interval} seconds (timeout: {timeout}s)")

        start_time = time.time()

        while (time.time() - start_time) < timeout:
            elapsed = int(time.time() - start_time)
            print(f"\r   ⏱️  Elapsed: {elapsed}s", end="", flush=True)

            try:
                # Check ComfyUI history for completion
                response = requests.get(
                    f"{self.comfyui_url}/history/{comfyui_prompt_id}",
                    timeout=10
                )

                if response.status_code == 200:
                    history = response.json()

                    if comfyui_prompt_id in history:
                        prompt_data = history[comfyui_prompt_id]

                        # Check if completed
                        if prompt_data.get("status", {}).get("completed", False):
                            outputs = prompt_data.get("outputs", {})

                            # Find SaveImage node output (usually node "7")
                            for node_id, node_output in outputs.items():
                                images = node_output.get("images", [])
                                if images:
                                    filename = images[0]["filename"]
                                    image_url = f"{self.comfyui_url}/view?filename={filename}&type=output"

                                    print(f"\n\n✅ Generation completed in {elapsed}s!")
                                    return image_url

                        # Check for errors
                        status = prompt_data.get("status", {})
                        if "error" in status or status.get("status_str") == "error":
                            error_msg = status.get("error", "Unknown error")
                            print(f"\n\n❌ Generation failed: {error_msg}")
                            return None

            except Exception as e:
                print(f"\n⚠️  Error checking status: {e}")

            time.sleep(check_interval)

        print(f"\n\n⏰ Timeout reached after {timeout}s")
        return None

    def download_image(self, image_url: str, output_path: str = None) -> bool:
        """
        Download the generated image

        Args:
            image_url: URL to download from
            output_path: Where to save (auto-generated if None)

        Returns:
            True if successful
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"fitness_influencer_{timestamp}.png"

        try:
            print(f"\n📥 Downloading image...")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Image saved to: {output_path}")
            print(f"   File size: {len(response.content) / 1024:.1f} KB")
            return True

        except Exception as e:
            print(f"❌ Failed to download image: {e}")
            return False

    def display_results(self, image_url: str, output_path: str):
        """Display final results summary"""
        print("\n" + "="*70)
        print("🎉 FITNESS INFLUENCER GENERATION COMPLETE!")
        print("="*70)
        print(f"\n🌐 Image URL (view in browser):")
        print(f"   {image_url}")
        print(f"\n💾 Saved locally:")
        print(f"   {output_path}")
        print(f"\n📋 Next Steps:")
        print(f"   • Open the image URL in your browser")
        print(f"   • Review the generated influencer")
        print(f"   • Use for social media mockups or branding")
        print(f"   • Generate more variations with different styles")
        print("\n" + "="*70)


def main():
    """Main test execution"""
    print("\n" + "="*70)
    print("🏋️  REALISTIC AI FITNESS INFLUENCER GENERATOR")
    print("="*70)
    print("\nCharacter: 'FitLife Maya'")
    print("Purpose: Professional fitness influencer for social media")
    print("Style: Realistic, athletic, inspiring")

    generator = FitnessInfluencerGenerator()

    # Check services
    if not generator.check_services():
        print("\n❌ Services not available. Please ensure:")
        print("   1. AvatarForge API is running: python main.py")
        print("   2. ComfyUI is running on port 8188")
        sys.exit(1)

    # Generate the influencer
    # Options: style = "professional" | "casual" | "athletic"
    # Options: quality = "draft" | "standard" | "high"

    result = generator.generate_influencer(
        style="professional",  # Change to "casual" or "athletic" for different looks
        quality="standard"      # Change to "high" for best quality (slower)
    )

    if not result:
        print("\n❌ Generation failed to start")
        sys.exit(1)

    # Wait for completion
    image_url = generator.wait_for_completion(
        generation_id=result["generation_id"],
        comfyui_prompt_id=result["comfyui_prompt_id"],
        timeout=300,  # 5 minutes max
        check_interval=5
    )

    if not image_url:
        print("\n❌ Generation did not complete successfully")
        sys.exit(1)

    # Download the image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"fitness_influencer_{timestamp}.png"

    if generator.download_image(image_url, output_path):
        generator.display_results(image_url, output_path)
    else:
        print(f"\n⚠️  Could not download, but you can view it here:")
        print(f"   {image_url}")

    print("\n✨ Test complete!\n")


if __name__ == "__main__":
    main()

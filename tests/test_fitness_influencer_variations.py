#!/usr/bin/env python3
"""
Test Script: Multiple Fitness Influencer Variations
===================================================

Generates multiple variations of a realistic AI fitness influencer
with different poses, styles, and settings.
"""

import requests
import time
import json
from datetime import datetime
from typing import List, Dict, Any

API_URL = "http://192.168.100.133:8000/avatarforge-controller"
COMFYUI_URL = "http://192.168.100.133:8188"

class InfluencerVariationGenerator:
    """Generate multiple fitness influencer variations"""

    def __init__(self):
        self.api_url = API_URL
        self.comfyui_url = COMFYUI_URL
        self.results = []

    def generate_variation(
        self,
        name: str,
        prompt: str,
        clothing: str,
        width: int = 768,
        height: int = 1024,
        steps: int = 30
    ) -> Dict[str, Any]:
        """Generate a single variation"""

        payload = {
            "prompt": prompt,
            "clothing": clothing,
            "realism": True,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg": 8.0,
            "sampler_name": "dpmpp_2m"
        }

        print(f"\n{'='*70}")
        print(f"🎨 Generating: {name}")
        print(f"{'='*70}")
        print(f"📝 {prompt[:80]}...")

        try:
            response = requests.post(
                f"{self.api_url}/generate/avatar",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            print(f"✅ Queued: {result['generation_id']}")
            return {
                "name": name,
                "generation_id": result["generation_id"],
                "comfyui_prompt_id": result["comfyui_prompt_id"],
                "prompt": prompt,
                "clothing": clothing
            }

        except Exception as e:
            print(f"❌ Failed: {e}")
            return None

    def wait_and_download(self, variation: Dict[str, Any]) -> bool:
        """Wait for generation and download result"""

        print(f"\n⏳ Waiting for '{variation['name']}'...", end="", flush=True)

        start_time = time.time()
        timeout = 120

        while (time.time() - start_time) < timeout:
            try:
                response = requests.get(
                    f"{self.comfyui_url}/history/{variation['comfyui_prompt_id']}",
                    timeout=10
                )

                if response.status_code == 200:
                    history = response.json()
                    prompt_id = variation['comfyui_prompt_id']

                    if prompt_id in history:
                        prompt_data = history[prompt_id]

                        if prompt_data.get("status", {}).get("completed", False):
                            outputs = prompt_data.get("outputs", {})

                            for node_id, node_output in outputs.items():
                                images = node_output.get("images", [])
                                if images:
                                    filename = images[0]["filename"]
                                    image_url = f"{self.comfyui_url}/view?filename={filename}&type=output"

                                    elapsed = int(time.time() - start_time)
                                    print(f" Done! ({elapsed}s)")

                                    # Download
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    output_path = f"influencer_{variation['name'].lower().replace(' ', '_')}_{timestamp}.png"

                                    img_response = requests.get(image_url, timeout=30)
                                    with open(output_path, "wb") as f:
                                        f.write(img_response.content)

                                    print(f"💾 Saved: {output_path}")
                                    variation["image_url"] = image_url
                                    variation["output_path"] = output_path
                                    variation["elapsed_time"] = elapsed
                                    return True

            except Exception as e:
                print(f"\n⚠️  Error: {e}")

            time.sleep(3)

        print(f" ⏰ Timeout")
        return False

    def generate_all_variations(self):
        """Generate all fitness influencer variations"""

        print("\n" + "="*70)
        print("🏋️  GENERATING MULTIPLE FITNESS INFLUENCER VARIATIONS")
        print("="*70)

        # Define variations
        variations = [
            {
                "name": "Professional Studio",
                "prompt": (
                    "professional fitness influencer, athletic woman in mid-20s, "
                    "confident smile, toned athletic physique, healthy glowing skin, "
                    "natural makeup, long ponytail hairstyle, studio lighting, "
                    "clean white background, motivational pose, professional photography, "
                    "high detail, realistic, 8k quality"
                ),
                "clothing": "modern athletic wear, fitted sports bra, high-waist leggings",
                "width": 768,
                "height": 1024
            },
            {
                "name": "Gym Action",
                "prompt": (
                    "dynamic fitness trainer in action, athletic woman doing workout, "
                    "determined expression, strong muscular definition, gym environment, "
                    "exercise equipment in background, dramatic lighting, "
                    "action photography, inspiring and motivational, high quality"
                ),
                "clothing": "performance sportswear, tank top, athletic shorts, training shoes",
                "width": 1024,
                "height": 768
            },
            {
                "name": "Outdoor Yoga",
                "prompt": (
                    "serene yoga instructor, fit athletic woman in yoga pose, "
                    "peaceful expression, flexible and strong, outdoor natural setting, "
                    "sunrise golden hour lighting, zen and balanced, "
                    "lifestyle photography, inspirational wellness, realistic detail"
                ),
                "clothing": "yoga outfit, sports bra, yoga leggings, bare feet",
                "width": 768,
                "height": 1024
            },
            {
                "name": "Running Athlete",
                "prompt": (
                    "professional runner, athletic woman mid-sprint, focused intense expression, "
                    "lean muscular build, running track or outdoor trail, "
                    "motion blur background, athletic photography, "
                    "powerful and energetic, high performance, realistic"
                ),
                "clothing": "running gear, athletic top, running shorts, professional running shoes",
                "width": 1024,
                "height": 768
            },
            {
                "name": "Casual Fitness Lifestyle",
                "prompt": (
                    "friendly fitness coach lifestyle portrait, athletic woman with warm smile, "
                    "approachable and inspiring, healthy lifestyle vibe, "
                    "natural casual setting, soft natural lighting, "
                    "authentic and relatable, lifestyle photography, realistic"
                ),
                "clothing": "casual athletic wear, hoodie, leggings, trendy sneakers",
                "width": 768,
                "height": 1024
            }
        ]

        # Generate all variations
        print(f"\n📋 Queueing {len(variations)} variations...\n")

        queued = []
        for var_def in variations:
            result = self.generate_variation(**var_def)
            if result:
                queued.append(result)
                time.sleep(2)  # Small delay between requests

        print(f"\n✅ Queued {len(queued)} variations successfully")

        # Wait for all to complete
        print(f"\n⏳ Waiting for all generations to complete...")
        print("="*70)

        successful = []
        for variation in queued:
            if self.wait_and_download(variation):
                successful.append(variation)
                self.results.append(variation)

        return successful

    def display_summary(self, results: List[Dict[str, Any]]):
        """Display final summary of all generations"""

        print("\n" + "="*70)
        print("🎉 GENERATION SUMMARY")
        print("="*70)

        print(f"\n📊 Total Variations: {len(results)}")

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']}")
            print(f"   ⏱️  Time: {result['elapsed_time']}s")
            print(f"   💾 File: {result['output_path']}")
            print(f"   🌐 URL: {result['image_url']}")

        print("\n" + "="*70)
        print("✨ All variations generated successfully!")
        print("="*70)
        print("\n📋 Next Steps:")
        print("   • Review all generated images")
        print("   • Choose your favorite for branding")
        print("   • Use across social media platforms")
        print("   • Generate more variations as needed")
        print("\n")


def main():
    """Main execution"""

    generator = InfluencerVariationGenerator()

    # Generate all variations
    results = generator.generate_all_variations()

    # Display summary
    if results:
        generator.display_summary(results)
    else:
        print("\n❌ No variations were generated successfully")


if __name__ == "__main__":
    main()

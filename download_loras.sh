#!/bin/bash
# Download professional LoRAs for enhanced quality

cd /home/raven/Documents/git/avatarforge/comfyui-dev/models/loras

echo "Downloading Detail Enhancement LoRAs..."

# 1. Add Detail LoRA - Enhances fine details
echo "1/3 - Detail Tweaker..."
wget -O "add_detail.safetensors" \
  "https://civitai.com/api/download/models/87153" \
  --progress=bar:force

# 2. Perfect Eyes LoRA - Better eye quality
echo "2/3 - Perfect Eyes..."
wget -O "perfect_eyes.safetensors" \
  "https://civitai.com/api/download/models/9768" \
  --progress=bar:force

# 3. Better Hands LoRA - Fixes hand issues
echo "3/3 - Better Hands..."
wget -O "beautiful_detailed_hands.safetensors" \
  "https://civitai.com/api/download/models/10738" \
  --progress=bar:force

echo ""
echo "✅ LoRAs downloaded!"
ls -lh

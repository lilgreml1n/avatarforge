#!/bin/bash
# Clean up failed/incomplete Qwen3 model downloads

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMFYUI_PATH="$SCRIPT_DIR/comfyui-dev"

echo "Cleaning up incomplete Qwen3 downloads..."

cd "$COMFYUI_PATH"

# Remove empty or very small files (likely error pages)
find models/diffusion_models -name "qwen*.safetensors" -size -1M -delete 2>/dev/null && echo "✓ Removed incomplete diffusion models"
find models/text_encoders -name "qwen*.safetensors" -size -1M -delete 2>/dev/null && echo "✓ Removed incomplete text encoders"
find models/vae -name "qwen*.safetensors" -size -1M -delete 2>/dev/null && echo "✓ Removed incomplete VAE models"
find models/loras -name "Qwen*.safetensors" -size -1M -delete 2>/dev/null && echo "✓ Removed incomplete LoRA models"

echo "Cleanup complete!"

#!/bin/bash
# AvatarForge Model Download Script
# Downloads all required models for photorealistic 4K generation

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ComfyUI path (relative to script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMFYUI_PATH="$SCRIPT_DIR/comfyui-dev"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  AvatarForge Model Setup${NC}"
echo -e "${BLUE}  Downloading models for stunning 4K photos${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "ComfyUI path: ${GREEN}${COMFYUI_PATH}${NC}"
echo ""

# Check if ComfyUI exists
if [ ! -d "$COMFYUI_PATH" ]; then
    echo -e "${RED}Error: ComfyUI not found at $COMFYUI_PATH${NC}"
    exit 1
fi

cd "$COMFYUI_PATH"

# Model directories should already exist, but let's verify
echo -e "${GREEN}Verifying model directories...${NC}"
mkdir -p models/checkpoints
mkdir -p models/diffusion_models
mkdir -p models/text_encoders
mkdir -p models/vae
mkdir -p models/loras
mkdir -p models/upscale_models

echo -e "${GREEN}✓ Directories ready${NC}"
echo ""

# ============================================
# QWEN3 IMAGE EDIT MODELS
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Downloading Qwen3 Image Edit Models${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. Qwen3 Diffusion Model (4.3 GB)
echo -e "${YELLOW}[1/4] Downloading Qwen3 diffusion model (4.3 GB)...${NC}"
if [ -f "models/diffusion_models/qwen_image_edit_fp8_e4m3fn.safetensors" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/diffusion_models/qwen_image_edit_fp8_e4m3fn.safetensors \
        "https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models/resolve/main/qwen_image_edit_fp8_e4m3fn.safetensors?download=true"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

# 2. Text Encoder (4.7 GB)
echo -e "${YELLOW}[2/4] Downloading Qwen2.5-VL text encoder (4.7 GB)...${NC}"
if [ -f "models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors \
        "https://huggingface.co/Comfy-Org/Qwen2.5-VL_text_encoders/resolve/main/qwen_2.5_vl_7b_fp8_scaled.safetensors?download=true"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

# 3. VAE Model (157 MB)
echo -e "${YELLOW}[3/4] Downloading Qwen VAE model (157 MB)...${NC}"
if [ -f "models/vae/qwen_image_vae.safetensors" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/vae/qwen_image_vae.safetensors \
        "https://huggingface.co/Comfy-Org/Qwen-Image_vae/resolve/main/qwen_image_vae.safetensors?download=true"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

# 4. Lightning LoRA (291 MB)
echo -e "${YELLOW}[4/4] Downloading Lightning LoRA (291 MB)...${NC}"
if [ -f "models/loras/Qwen-Image-Lightning-4steps-V1.0.safetensors" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/loras/Qwen-Image-Lightning-4steps-V1.0.safetensors \
        "https://huggingface.co/Comfy-Org/Qwen-Image_loras/resolve/main/Qwen-Image-Lightning-4steps-V1.0.safetensors?download=true"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

echo ""
echo -e "${GREEN}✓ Qwen3 models complete!${NC}"
echo ""

# ============================================
# UPSCALER MODELS
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Downloading 4K Upscaler Models${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. RealESRGAN 4x+ (64 MB)
echo -e "${YELLOW}[1/3] Downloading RealESRGAN 4x+ (64 MB)...${NC}"
if [ -f "models/upscale_models/RealESRGAN_x4plus.pth" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/upscale_models/RealESRGAN_x4plus.pth \
        "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

# 2. 4x-UltraSharp (67 MB)
echo -e "${YELLOW}[2/3] Downloading 4x-UltraSharp (67 MB)...${NC}"
if [ -f "models/upscale_models/4x-UltraSharp.pth" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/upscale_models/4x-UltraSharp.pth \
        "https://huggingface.co/Kim2091/UltraSharp/resolve/main/4x-UltraSharp.pth?download=true"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

# 3. 4x_foolhardy_Remacri (67 MB)
echo -e "${YELLOW}[3/3] Downloading 4x_foolhardy_Remacri (67 MB)...${NC}"
if [ -f "models/upscale_models/4x_foolhardy_Remacri.pth" ]; then
    echo -e "${GREEN}✓ Already exists, skipping${NC}"
else
    curl -L -C - -o models/upscale_models/4x_foolhardy_Remacri.pth \
        "https://huggingface.co/FacehugmanIII/4x_foolhardy_Remacri/resolve/main/4x_foolhardy_Remacri.pth?download=true"
    echo -e "${GREEN}✓ Downloaded${NC}"
fi

echo ""
echo -e "${GREEN}✓ Upscaler models complete!${NC}"
echo ""

# ============================================
# SUMMARY
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Automatic Downloads Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check model sizes
echo -e "${GREEN}Downloaded models:${NC}"
echo ""
echo -e "Qwen3 Models:"
ls -lh models/diffusion_models/qwen_image_edit_fp8_e4m3fn.safetensors 2>/dev/null || echo "  - diffusion model: not found"
ls -lh models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors 2>/dev/null || echo "  - text encoder: not found"
ls -lh models/vae/qwen_image_vae.safetensors 2>/dev/null || echo "  - VAE: not found"
ls -lh models/loras/Qwen-Image-Lightning-4steps-V1.0.safetensors 2>/dev/null || echo "  - Lightning LoRA: not found"
echo ""
echo -e "Upscaler Models:"
ls -lh models/upscale_models/RealESRGAN_x4plus.pth 2>/dev/null || echo "  - RealESRGAN: not found"
ls -lh models/upscale_models/4x-UltraSharp.pth 2>/dev/null || echo "  - UltraSharp: not found"
ls -lh models/upscale_models/4x_foolhardy_Remacri.pth 2>/dev/null || echo "  - Remacri: not found"
echo ""

# ============================================
# MANUAL DOWNLOADS REQUIRED
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}⚠️  MANUAL DOWNLOADS REQUIRED${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}The following models require a Civitai account:${NC}"
echo ""
echo -e "${GREEN}1. RealVisXL V5.0${NC} (Recommended - Photorealistic)"
echo -e "   URL: ${BLUE}https://civitai.com/models/139562/realvisxl-v50${NC}"
echo -e "   File: RealVisXL_V5.0.safetensors (~6.5 GB)"
echo -e "   Save to: ${GREEN}$COMFYUI_PATH/models/checkpoints/${NC}"
echo -e "            ${GREEN}(or comfyui-dev/models/checkpoints/ from avatarforge directory)${NC}"
echo ""
echo -e "${GREEN}2. JuggernautXL V10${NC} (Recommended - Versatile)"
echo -e "   URL: ${BLUE}https://civitai.com/models/133005/juggernaut-xl${NC}"
echo -e "   File: JuggernautXL_v10.safetensors (~6.5 GB)"
echo -e "   Save to: ${GREEN}$COMFYUI_PATH/models/checkpoints/${NC}"
echo -e "            ${GREEN}(or comfyui-dev/models/checkpoints/ from avatarforge directory)${NC}"
echo ""
echo -e "${YELLOW}Optional (choose one or both):${NC}"
echo ""
echo -e "${GREEN}3. NightVision XL${NC} (Great for landscapes)"
echo -e "   URL: ${BLUE}https://civitai.com/models/128607/nightvision-xl${NC}"
echo -e "   File: NightVisionXL_v0931.safetensors (~6.5 GB)"
echo ""
echo -e "${GREEN}4. Copax Timeless XL${NC} (Superior color accuracy)"
echo -e "   URL: ${BLUE}https://civitai.com/models/118111/copax-timeless-sdxl${NC}"
echo -e "   File: CopaxTimelessxlSDXL1_v12.safetensors (~6.5 GB)"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo -e "1. Download at least ONE checkpoint from Civitai (RealVisXL recommended)"
echo -e "2. Place .safetensors file in: ${GREEN}$COMFYUI_PATH/models/checkpoints/${NC}"
echo -e "3. Start ComfyUI: ${YELLOW}cd $COMFYUI_PATH && python main.py${NC}"
echo -e "4. Start AvatarForge API: ${YELLOW}cd ~/Documents/git/avatarforge && uv run python main.py${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Setup complete! Ready for stunning 4K generation! 🚀${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

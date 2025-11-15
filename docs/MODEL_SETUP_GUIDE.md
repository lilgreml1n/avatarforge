# AvatarForge Model Setup Guide
## Stunning 4K Photorealistic Generation with Qwen3

Last Updated: 2025-11-15

---

## Overview

This guide will help you set up ComfyUI with the best models for **stunning, photorealistic 4K avatar generation** using:
- **Qwen3 Image Edit** - Advanced image editing and generation
- **Premium SDXL Checkpoints** - Photorealistic quality (no plastic AI look)
- **Professional Upscalers** - True 4K output with crisp details

---

## Required ComfyUI Directory Structure

```
ComfyUI/
├── models/
│   ├── checkpoints/              # Main generation models
│   ├── diffusion_models/         # Qwen3 models
│   ├── text_encoders/            # Qwen VL encoder
│   ├── vae/                      # VAE models
│   ├── loras/                    # LoRA models
│   └── upscale_models/           # Upscaler models
└── custom_nodes/                 # ComfyUI extensions
```

---

## 🎯 Part 1: Qwen3 Image Edit Models

### What is Qwen3 Image Edit?
Qwen3 Image Edit (Qwen-Image-Edit-2509) is a revolutionary 20B parameter model that supports:
- Precise image editing with text instructions
- Dual semantic/appearance editing
- Multi-image editing with consistency
- Bilingual support (English/Chinese)

### Required Files

#### 1. Main Diffusion Model (4.3 GB)
```bash
# Download to: ComfyUI/models/diffusion_models/
wget https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models/resolve/main/qwen_image_edit_fp8_e4m3fn.safetensors
```

#### 2. Lightning LoRA (4-step fast generation) (291 MB)
```bash
# Download to: ComfyUI/models/loras/
wget https://huggingface.co/Comfy-Org/Qwen-Image_loras/resolve/main/Qwen-Image-Lightning-4steps-V1.0.safetensors
```

#### 3. VAE Model (157 MB)
```bash
# Download to: ComfyUI/models/vae/
wget https://huggingface.co/Comfy-Org/Qwen-Image_vae/resolve/main/qwen_image_vae.safetensors
```

#### 4. Text Encoder (4.7 GB)
```bash
# Download to: ComfyUI/models/text_encoders/
wget https://huggingface.co/Comfy-Org/Qwen2.5-VL_text_encoders/resolve/main/qwen_2.5_vl_7b_fp8_scaled.safetensors
```

### Low-VRAM Alternative (8GB+ VRAM)
If you have limited VRAM, use the GGUF quantized version:
```bash
# Download GGUF variant (requires less VRAM)
wget https://huggingface.co/city96/Qwen-Image-Edit-GGUF/resolve/main/qwen_image_edit-Q4_K_S.gguf
```

### License
Apache 2.0 - **Commercially usable** with attribution

---

## 🎨 Part 2: Photorealistic SDXL Checkpoints

Choose ONE of these models based on your preference. All produce stunning, realistic results.

### Top Recommendations (Download to: ComfyUI/models/checkpoints/)

#### 1. **RealVisXL V5.0** (Recommended for Portraits)
- **Best for:** Hyper-realistic human portraits, skin/hair texture
- **Size:** ~6.5 GB
- **Download:** https://civitai.com/models/139562/realvisxl-v50
```bash
# Direct download (Civitai requires account)
# Visit link above and download RealVisXL_V5.0.safetensors
```
**Why:** Virtually indistinguishable from real photos, incredible detail

#### 2. **Juggernaut XL V10** (Recommended for Versatility)
- **Best for:** Portraits, full-body shots, versatile realism
- **Size:** ~6.5 GB
- **Download:** https://civitai.com/models/133005/juggernaut-xl
```bash
# Visit link and download JuggernautXL_v10.safetensors
```
**Why:** Enhanced detail, perfect blend of digital artistry and photography

#### 3. **NightVision XL** (Recommended for Landscapes/Architecture)
- **Best for:** Photorealistic landscapes, vehicles, architecture, animals
- **Size:** ~6.5 GB
- **Download:** https://civitai.com/models/128607/nightvision-xl
- **Baked VAE:** Yes (no separate VAE needed)
```bash
# Visit link and download NightVisionXL_v0931.safetensors
```
**Why:** Doesn't require complex prompts, excellent at photoreal scenes

#### 4. **Copax Timeless XL** (Recommended for Color Accuracy)
- **Best for:** Vibrant colors, superior contrast, detailed shadows
- **Size:** ~6.5 GB
- **Download:** https://civitai.com/models/118111/copax-timeless-sdxl
```bash
# Visit link and download CopaxTimelessxlSDXL1_v12.safetensors
```
**Why:** Fine-tuned on SDXL 1.0, exceptional color accuracy

### Lightning Models (Faster Generation - 4 steps)

#### **RealVis Lightning SDXL** (Fast + Photorealistic)
- **Best for:** Fast iteration, same quality as RealVisXL
- **Steps:** 4-6 (vs. 20-40 for regular models)
- **Download:** https://civitai.com/models/361593/realvis-xl-lightning
```bash
# Visit link and download RealvisXL_Lightning.safetensors
```

---

## 🚀 Part 3: 4K Upscaler Models

Download **ALL THREE** for best results (Download to: ComfyUI/models/upscale_models/)

### 1. **4x-UltraSharp** (Primary - Sharp Digital Art)
- **Best for:** Sharp edges, digital art, AI-generated images
- **Upscale:** 4x (512px → 2048px)
- **Size:** ~67 MB
```bash
wget https://huggingface.co/Kim2091/UltraSharp/resolve/main/4x-UltraSharp.pth
```

### 2. **RealESRGAN 4x+** (Primary - Photos)
- **Best for:** Real-world photos, versatile, excellent results
- **Upscale:** 4x (512px → 2048px)
- **Size:** ~64 MB
```bash
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x4plus.pth
```

### 3. **4x_foolhardy_Remacri** (Secondary - Fine Details)
- **Best for:** Additional detail enhancement, post-upscale
- **Upscale:** 4x
- **Size:** ~67 MB
```bash
wget https://huggingface.co/FacehugmanIII/4x_foolhardy_Remacri/resolve/main/4x_foolhardy_Remacri.pth
```

### Optional Advanced Upscalers

#### **4xNomos2_otf_esrgan** (Universal)
- **Best for:** Balanced upscaling for any content type
```bash
wget https://huggingface.co/gemasai/4x_Nomos8k_atd_jpg/resolve/main/4xNomos2_otf_esrgan.pth
```

#### **4x_NMKD-Superscale-SP** (Extreme Sharpness)
- **Best for:** Maximum sharpness for AI art
```bash
wget https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_NMKD-Superscale-SP_178000_G.pth
```

### More Models Available At:
https://openmodeldb.info/ - Comprehensive upscaler database

---

## 📦 Complete Setup Script

Save this as `setup_models.sh` and run it:

```bash
#!/bin/bash
# AvatarForge Model Setup Script
# Run this from your ComfyUI directory

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  AvatarForge Model Setup - Premium Quality${NC}"
echo -e "${BLUE}================================================${NC}"

# Create directories
echo -e "${GREEN}Creating model directories...${NC}"
mkdir -p models/checkpoints
mkdir -p models/diffusion_models
mkdir -p models/text_encoders
mkdir -p models/vae
mkdir -p models/loras
mkdir -p models/upscale_models

# Qwen3 Image Edit Models
echo -e "${GREEN}Downloading Qwen3 Image Edit models...${NC}"
cd models/diffusion_models
wget -nc https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models/resolve/main/qwen_image_edit_fp8_e4m3fn.safetensors

cd ../text_encoders
wget -nc https://huggingface.co/Comfy-Org/Qwen2.5-VL_text_encoders/resolve/main/qwen_2.5_vl_7b_fp8_scaled.safetensors

cd ../vae
wget -nc https://huggingface.co/Comfy-Org/Qwen-Image_vae/resolve/main/qwen_image_vae.safetensors

cd ../loras
wget -nc https://huggingface.co/Comfy-Org/Qwen-Image_loras/resolve/main/Qwen-Image-Lightning-4steps-V1.0.safetensors

# Upscalers
echo -e "${GREEN}Downloading 4K upscaler models...${NC}"
cd ../upscale_models
wget -nc https://huggingface.co/Kim2091/UltraSharp/resolve/main/4x-UltraSharp.pth
wget -nc https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x4plus.pth
wget -nc https://huggingface.co/FacehugmanIII/4x_foolhardy_Remacri/resolve/main/4x_foolhardy_Remacri.pth

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}Model setup complete!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo "Note: You'll need to manually download SDXL checkpoints from Civitai:"
echo "  1. RealVisXL V5.0: https://civitai.com/models/139562"
echo "  2. Juggernaut XL V10: https://civitai.com/models/133005"
echo "  3. NightVision XL: https://civitai.com/models/128607"
echo ""
echo "Place checkpoint files in: models/checkpoints/"
```

Make executable and run:
```bash
chmod +x setup_models.sh
./setup_models.sh
```

---

## 🔧 ComfyUI Configuration

### Update AvatarForge Config

Edit `.env` in your AvatarForge project:

```env
# ComfyUI Backend
COMFYUI_URL=http://localhost:8188

# Model Configuration
DEFAULT_CHECKPOINT=RealVisXL_V5.0.safetensors
REALISTIC_CHECKPOINT=RealVisXL_V5.0.safetensors
ANIME_CHECKPOINT=JuggernautXL_v10.safetensors

# Upscaler Configuration
PRIMARY_UPSCALER=RealESRGAN_x4plus.pth
SECONDARY_UPSCALER=4x-UltraSharp.pth

# Quality Settings for Photorealism
DEFAULT_STEPS=30           # Higher = better quality
DEFAULT_CFG=7.0           # Guidance scale
DEFAULT_SAMPLER=dpmpp_2m_sde_gpu  # Best for photorealism
DEFAULT_SCHEDULER=karras   # Better quality
```

---

## 📊 VRAM Requirements

| Model Setup | VRAM Required | Generation Time (est.) |
|-------------|---------------|------------------------|
| Qwen3 + SDXL + 4K Upscale | 16 GB+ | 30-60 seconds |
| Qwen3 GGUF + SDXL | 12 GB | 40-80 seconds |
| Qwen3 Lightning + Fast | 10 GB | 15-30 seconds |
| SDXL only (no Qwen) | 8 GB | 20-40 seconds |

**Optimization Tips:**
- Use `fp8` models to reduce VRAM usage
- Use Lightning models for faster generation
- Use GGUF quantized models for low VRAM
- Enable `--lowvram` or `--medvram` flags when starting ComfyUI

---

## 🎨 Workflow Updates Needed

The following files need to be updated to use these models:

### 1. `avatarforge/services/workflow_builder.py`
- Replace `v1-5-pruned-emaonly.safetensors` with `RealVisXL_V5.0.safetensors`
- Add upscaling nodes (4x-UltraSharp + RealESRGAN)
- Update sampler to `dpmpp_2m_sde_gpu` for photorealism
- Increase default steps to 30
- Add VAE selection

### 2. `avatarforge/core/config.py`
- Add model configuration options
- Add upscaler selection
- Add quality presets (draft/normal/high/ultra)

---

## ✅ Testing Your Setup

Once models are installed, test with:

```bash
# 1. Start ComfyUI
cd /path/to/ComfyUI
python main.py

# 2. Start AvatarForge API
cd /path/to/avatarforge
uv run python main.py

# 3. Test photorealistic generation
curl -X POST http://localhost:8000/avatarforge-controller/generate/avatar \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "professional headshot of a confident business woman, sharp focus, studio lighting, detailed skin texture, 35mm lens",
    "realism": true,
    "steps": 30,
    "cfg": 7.0,
    "width": 1024,
    "height": 1024
  }'
```

Expected output: Photorealistic 4K image (upscaled from 1024x1024 to 4096x4096)

---

## 🚨 Common Issues

### Issue: "Model not found"
**Solution:** Check model is in correct directory and filename matches exactly

### Issue: Out of VRAM
**Solution:**
- Use GGUF models
- Reduce batch size
- Lower resolution (768x768 instead of 1024x1024)
- Start ComfyUI with `--lowvram` flag

### Issue: Plastic/fake looking results
**Solution:**
- Use RealVisXL or Juggernaut XL checkpoint
- Increase steps to 30-40
- Add "detailed skin texture, pores, natural lighting" to prompt
- Use negative prompt: "plastic, doll, fake, smooth skin, oversharpened"
- Lower CFG to 5-7 (too high = plastic look)

---

## 🎯 Next Steps

1. ✅ Download all models using the setup script
2. ✅ Manually download SDXL checkpoint from Civitai
3. ✅ Update `workflow_builder.py` with new models
4. ✅ Test generation pipeline
5. ✅ Fine-tune prompts for best results

---

## 📚 Additional Resources

- **Qwen3 Documentation:** https://github.com/QwenLM/Qwen-Image
- **ComfyUI Workflows:** https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit
- **SDXL Best Practices:** https://stable-diffusion-art.com/sdxl/
- **Upscaler Database:** https://openmodeldb.info/

---

**Ready to generate stunning, photorealistic 4K avatars! 🚀**

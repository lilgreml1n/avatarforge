#!/bin/bash
################################################################################
# Qwen Image Edit 2509 Setup Script
################################################################################
#
# This script installs everything needed for Qwen-Image-Edit-2509:
# 1. ComfyUI-GGUF custom node
# 2. Qwen-Image-Edit-2509 GGUF model (Q4_K_M quantization)
# 3. Qwen text encoders (CLIP)
# 4. Qwen VAE
# 5. Optional: Lightning LoRA for 4-step inference
#
# Based on:
# - https://huggingface.co/QuantStack/Qwen2.5-VL-7B-Instruct-GGUF
# - https://docs.comfy.org/tutorials/image_editing
# - https://huggingface.co/lightx2v/Qwen-Image-Edit-Lightning
#
################################################################################

set -e  # Exit on error

COMFYUI_DIR="/home/raven/Documents/ComfyUI"
CUSTOM_NODES_DIR="$COMFYUI_DIR/custom_nodes"
MODELS_DIR="$COMFYUI_DIR/models"

echo "================================================================================"
echo "🤖 QWEN IMAGE EDIT 2509 SETUP"
echo "================================================================================"
echo ""
echo "📦 Installing Qwen-Image-Edit-2509 for ComfyUI"
echo ""
echo "This will install:"
echo "  • ComfyUI-GGUF custom node"
echo "  • Qwen-Image-Edit-2509 GGUF model (~2.5GB)"
echo "  • Qwen text encoders"
echo "  • Qwen VAE"
echo "  • Lightning LoRA (optional, for 4-step inference)"
echo ""
echo "================================================================================"
echo ""

# Step 1: Install ComfyUI-GGUF custom node
echo "📥 Step 1: Installing ComfyUI-GGUF custom node..."
echo ""

if [ -d "$CUSTOM_NODES_DIR/ComfyUI-GGUF" ]; then
    echo "✅ ComfyUI-GGUF already installed"
else
    cd "$CUSTOM_NODES_DIR"
    git clone https://github.com/city96/ComfyUI-GGUF.git
    cd ComfyUI-GGUF
    pip install -r requirements.txt
    echo "✅ ComfyUI-GGUF installed"
fi

echo ""

# Step 2: Download Qwen UNET (GGUF format)
echo "📥 Step 2: Downloading Qwen-Image-Edit-2509 UNET (Q4_K_M quantization)..."
echo "   Model: ~2.5GB (Q4_K_M quantized for efficiency)"
echo ""

UNET_DIR="$MODELS_DIR/unet"
mkdir -p "$UNET_DIR"

if [ -f "$UNET_DIR/Qwen-Image-Edit-2509-Q4_K_M.gguf" ]; then
    echo "✅ Qwen UNET already downloaded"
else
    cd "$UNET_DIR"
    wget -O "Qwen-Image-Edit-2509-Q4_K_M.gguf" \
        "https://huggingface.co/QuantStack/Qwen-Image-Edit-2509-GGUF/resolve/main/Qwen-Image-Edit-2509-Q4_K_M.gguf"
    echo "✅ Qwen UNET downloaded"
fi

echo ""

# Step 3: Download Qwen Text Encoder (CLIP)
echo "📥 Step 3: Downloading Qwen text encoder (CLIP)..."
echo ""

CLIP_DIR="$MODELS_DIR/clip"
mkdir -p "$CLIP_DIR"

if [ -f "$CLIP_DIR/qwen_2.5_vl_7b_fp8_scaled.safetensors" ]; then
    echo "✅ Qwen CLIP already downloaded"
else
    cd "$CLIP_DIR"
    wget "https://huggingface.co/Comfy-Org/Qwen2.5-VL-7B-fp8-scaled/resolve/main/qwen_2.5_vl_7b_fp8_scaled.safetensors"
    echo "✅ Qwen CLIP downloaded"
fi

echo ""

# Step 4: Download Qwen VAE
echo "📥 Step 4: Downloading Qwen VAE..."
echo ""

VAE_DIR="$MODELS_DIR/vae"
mkdir -p "$VAE_DIR"

if [ -f "$VAE_DIR/qwen_image_vae.safetensors" ]; then
    echo "✅ Qwen VAE already downloaded"
else
    cd "$VAE_DIR"
    wget "https://huggingface.co/Qwen/Qwen2-VL-7B/resolve/main/vae/qwen_image_vae.safetensors"
    echo "✅ Qwen VAE downloaded"
fi

echo ""

# Step 5: Download Lightning LoRA (optional, for 4-step)
echo "📥 Step 5: Downloading Lightning LoRA (4-step inference)..."
echo "   This is OPTIONAL but highly recommended for speed"
echo ""

LORA_DIR="$MODELS_DIR/loras"
mkdir -p "$LORA_DIR"

if [ -f "$LORA_DIR/Qwen-Image-Edit-Lightning-4steps-V1.0.safetensors" ]; then
    echo "✅ Lightning LoRA already downloaded"
else
    cd "$LORA_DIR"
    wget "https://huggingface.co/lightx2v/Qwen-Image-Edit-Lightning/resolve/main/Qwen-Image-Edit-Lightning-4steps-V1.0.safetensors"
    echo "✅ Lightning LoRA downloaded"
fi

echo ""
echo "================================================================================"
echo "🎉 QWEN SETUP COMPLETE!"
echo "================================================================================"
echo ""
echo "📊 Installed Components:"
echo "   ✅ ComfyUI-GGUF custom node"
echo "   ✅ Qwen-Image-Edit-2509 UNET (Q4_K_M)"
echo "   ✅ Qwen text encoder (CLIP)"
echo "   ✅ Qwen VAE"
echo "   ✅ Lightning LoRA (4-step)"
echo ""
echo "📁 Model Locations:"
echo "   UNET:  $UNET_DIR/Qwen-Image-Edit-2509-Q4_K_M.gguf"
echo "   CLIP:  $CLIP_DIR/qwen_2.5_vl_7b_fp8_scaled.safetensors"
echo "   VAE:   $VAE_DIR/qwen_image_vae.safetensors"
echo "   LoRA:  $LORA_DIR/Qwen-Image-Edit-Lightning-4steps-V1.0.safetensors"
echo ""
echo "🔄 Next Steps:"
echo "   1. Restart ComfyUI to load the new custom node"
echo "   2. Run: python3 qwen_fitness_influencer.py"
echo "   3. Enjoy 4-step lightning-fast AI image editing!"
echo ""
echo "💡 Usage:"
echo "   • Lightning mode: 4 steps (~5-10 seconds)"
echo "   • Quality mode: 20 steps (~20-30 seconds)"
echo "   • Natural language prompts: 'Fix the eyes to be clear and bright'"
echo ""
echo "================================================================================"
echo ""

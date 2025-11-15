# Manual Download Guide for Qwen3 Models

## Network Issue

Your network is blocking HuggingFace downloads with a `403 Forbidden` error. This means you need to download the Qwen3 models manually from a machine/network that has access to HuggingFace.

## Required Downloads

### Qwen3 Image Edit Models

Download these files from HuggingFace and transfer them to your `comfyui-dev/models/` directories:

#### 1. Diffusion Model (4.3 GB)
- **URL**: https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models/resolve/main/qwen_image_edit_fp8_e4m3fn.safetensors
- **Direct Download**: Click "Download" button on the file page
- **Save to**: `comfyui-dev/models/diffusion_models/qwen_image_edit_fp8_e4m3fn.safetensors`

#### 2. Text Encoder (4.7 GB)
- **URL**: https://huggingface.co/Comfy-Org/Qwen2.5-VL_text_encoders/resolve/main/qwen_2.5_vl_7b_fp8_scaled.safetensors
- **Direct Download**: Click "Download" button on the file page
- **Save to**: `comfyui-dev/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors`

#### 3. VAE Model (157 MB)
- **URL**: https://huggingface.co/Comfy-Org/Qwen-Image_vae/resolve/main/qwen_image_vae.safetensors
- **Direct Download**: Click "Download" button on the file page
- **Save to**: `comfyui-dev/models/vae/qwen_image_vae.safetensors`

#### 4. Lightning LoRA (291 MB)
- **URL**: https://huggingface.co/Comfy-Org/Qwen-Image_loras/resolve/main/Qwen-Image-Lightning-4steps-V1.0.safetensors
- **Direct Download**: Click "Download" button on the file page
- **Save to**: `comfyui-dev/models/loras/Qwen-Image-Lightning-4steps-V1.0.safetensors`

## Download Options

### Option 1: Download via Browser (Easiest)

1. Use a machine/network that has access to HuggingFace
2. Open each URL above in your browser
3. Click the "Download" button
4. Transfer files to your spark machine using:
   - USB drive
   - Network file share (scp, rsync, etc.)
   - Cloud storage (Dropbox, Google Drive, etc.)

**Example transfer using scp:**
```bash
# From the machine where you downloaded the files:
scp qwen_image_edit_fp8_e4m3fn.safetensors raven@spark-a72f:~/Documents/git/avatarforge/comfyui-dev/models/diffusion_models/

scp qwen_2.5_vl_7b_fp8_scaled.safetensors raven@spark-a72f:~/Documents/git/avatarforge/comfyui-dev/models/text_encoders/

scp qwen_image_vae.safetensors raven@spark-a72f:~/Documents/git/avatarforge/comfyui-dev/models/vae/

scp Qwen-Image-Lightning-4steps-V1.0.safetensors raven@spark-a72f:~/Documents/git/avatarforge/comfyui-dev/models/loras/
```

### Option 2: Download via git-lfs (If you have git-lfs installed)

```bash
# On a machine with HuggingFace access:
git lfs install

# Clone the repositories
git clone https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models
git clone https://huggingface.co/Comfy-Org/Qwen2.5-VL_text_encoders
git clone https://huggingface.co/Comfy-Org/Qwen-Image_vae
git clone https://huggingface.co/Comfy-Org/Qwen-Image_loras

# Then transfer the .safetensors files to your spark machine
```

### Option 3: Use HuggingFace CLI (If installed)

```bash
# On a machine with HuggingFace access:
pip install huggingface-hub

# Download files
huggingface-cli download Comfy-Org/Qwen-Image-Edit_diffusion_models qwen_image_edit_fp8_e4m3fn.safetensors
huggingface-cli download Comfy-Org/Qwen2.5-VL_text_encoders qwen_2.5_vl_7b_fp8_scaled.safetensors
huggingface-cli download Comfy-Org/Qwen-Image_vae qwen_image_vae.safetensors
huggingface-cli download Comfy-Org/Qwen-Image_loras Qwen-Image-Lightning-4steps-V1.0.safetensors

# Then transfer to your spark machine
```

## Verification

After transferring files, run the download script again to verify:

```bash
cd ~/Documents/git/avatarforge
bash download_models.sh
```

You should see:
```
✓ Already exists (4.3G)  # diffusion model
✓ Already exists (4.7G)  # text encoder
✓ Already exists (157M)  # VAE
✓ Already exists (291M)  # Lightning LoRA
```

## Cleanup Failed Downloads

If you have incomplete/empty files from failed download attempts:

```bash
cd ~/Documents/git/avatarforge
bash cleanup_failed_downloads.sh
```

## Total Download Size

- **Qwen3 Models**: ~9.5 GB total
- **Upscalers**: ~200 MB (already downloaded ✓)
- **SDXL Checkpoints** (Civitai): ~6.5 GB each (manual download required)

Make sure you have at least **20 GB** free space in `comfyui-dev/models/` for all models.

## Need Help?

If you're having trouble downloading or transferring files, check:
1. Do you have access to HuggingFace from another network/machine?
2. Do you have enough disk space? (`df -h ~/Documents/git/avatarforge/comfyui-dev`)
3. Are the model directories created? (`ls -la comfyui-dev/models/`)

Run `bash download_models.sh` to see current status and missing files.

# Photorealistic 4K Avatar Generation - Examples

## 🎯 Stunning Photorealistic Generation (No Plastic AI Look!)

This guide shows you how to generate **stunning, photorealistic 4K avatars** using the updated AvatarForge API with SDXL models and professional upscalers.

---

## 🚀 Quick Start - Professional Headshot

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "professional headshot of a confident business woman in her 30s, sharp focus, studio lighting, detailed skin texture",
    "realism": true,
    "upscale": true,
    "steps": 35,
    "cfg": 7.0
  }'
```

**What this does:**
- Uses **RealVisXL V5.0** for photorealistic generation
- Automatically adds quality tags (skin texture, natural pores, etc.)
- Applies anti-plastic negative prompts
- Upscales to **4K** using RealESRGAN
- **~30-60 seconds** generation time

---

## 📸 Example 1: Natural Portrait (Outdoor Lighting)

```json
{
  "prompt": "portrait of a young man with short brown hair and stubble, natural outdoor lighting, golden hour, authentic expression, casual clothing",
  "clothing": "navy blue henley shirt, denim jacket",
  "realism": true,
  "upscale": true,
  "steps": 35,
  "cfg": 6.5,
  "width": 1024,
  "height": 1024
}
```

**Result:** 4096x4096 photorealistic portrait with natural lighting and detailed textures

---

## 💼 Example 2: Corporate Professional

```json
{
  "prompt": "corporate executive woman, elegant professional appearance, confident posture, modern office background",
  "clothing": "charcoal grey blazer, white silk blouse, pearl necklace",
  "realism": true,
  "upscale": true,
  "use_secondary_upscaler": true,
  "steps": 40,
  "cfg": 7.0,
  "sampler_name": "dpmpp_2m_sde_gpu",
  "width": 1024,
  "height": 1536
}
```

**Advanced Features:**
- `use_secondary_upscaler: true` - Applies **both** RealESRGAN + UltraSharp for extra sharpness
- Portrait orientation (1024x1536)
- Higher steps (40) for maximum quality
- Result: **4096x6144** ultra-sharp corporate headshot

---

## 🎨 Example 3: Creative Artist Portrait

```json
{
  "prompt": "creative artist in studio, paint-stained hands, authentic work environment, natural window light, thoughtful expression",
  "clothing": "paint-stained denim apron over casual clothes",
  "style": "documentary photography",
  "realism": true,
  "upscale": true,
  "steps": 35,
  "cfg": 6.0,
  "width": 1024,
  "height": 1024
}
```

**Note:** Lower CFG (6.0) prevents oversharpening and maintains natural look

---

## 🏃 Example 4: Athletic/Fitness Portrait

```json
{
  "prompt": "athletic woman after workout, natural gym environment, authentic fitness photography, genuine expression, slight sweat",
  "clothing": "black athletic wear, sports bra, yoga pants",
  "realism": true,
  "upscale": true,
  "steps": 35,
  "cfg": 7.0,
  "width": 768,
  "height": 1024
}
```

**Result:** 3072x4096 realistic fitness portrait

---

## 👴 Example 5: Character Portrait (Elderly Subject)

```json
{
  "prompt": "distinguished elderly gentleman, weathered features, wise expression, life experience visible in face, natural wrinkles and age lines",
  "clothing": "vintage tweed jacket, white dress shirt, wire-rimmed glasses",
  "realism": true,
  "upscale": true,
  "steps": 40,
  "cfg": 6.5,
  "width": 1024,
  "height": 1024
}
```

**Why this works:**
- Emphasizing "natural wrinkles" and "weathered features" prevents AI from smoothing skin
- Lower CFG (6.5) maintains realistic imperfections
- Anti-plastic negative prompts preserve authentic aging

---

## 🎭 Example 6: Multi-Pose Generation (All Views)

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate_all_poses" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "professional model, confident posture, natural expression",
    "clothing": "black turtleneck sweater, dark jeans",
    "realism": true,
    "upscale": true,
    "steps": 35,
    "cfg": 7.0
  }'
```

**Generates 4 views:** Front, Back, Side, Quarter - all in 4K photorealistic quality

---

## ⚙️ Parameter Guide

### Core Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | *required* | Detailed description of the subject |
| `realism` | boolean | `false` | `true` = photorealistic, `false` = anime/stylized |
| `clothing` | string | `null` | Specific clothing details |
| `style` | string | `null` | Art style modifier (e.g., "documentary photography") |

### Quality Parameters

| Parameter | Type | Default (Realistic) | Description |
|-----------|------|---------------------|-------------|
| `steps` | integer | `35` | Sampling steps (20-50, higher = better quality) |
| `cfg` | float | `7.0` | Guidance scale (5-9, lower = more natural) |
| `sampler_name` | string | `dpmpp_2m_sde_gpu` | Sampling algorithm |
| `scheduler` | string | `karras` | Scheduler type |
| `width` | integer | `1024` | Base width (before upscaling) |
| `height` | integer | `1024` | Base height (before upscaling) |

### Upscaling Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `upscale` | boolean | `true` | Enable 4K upscaling |
| `upscale_model` | string | `RealESRGAN_x4plus.pth` | Primary upscaler |
| `use_secondary_upscaler` | boolean | `false` | Apply second upscaler for extra sharpness |
| `secondary_upscale_model` | string | `4x-UltraSharp.pth` | Secondary upscaler |

---

## 🎨 Prompting Tips for Photorealism

### ✅ DO Use These Terms:
- "detailed skin texture"
- "natural pores"
- "realistic lighting"
- "professional photography"
- "sharp focus"
- "authentic expression"
- "natural imperfections"
- "subtle wrinkles" (if appropriate)
- "soft shadows"
- "natural colors"

### ❌ AVOID These Terms:
- "perfect skin" (causes plastic look)
- "flawless"
- "smooth" (over-smooths skin)
- "airbrushed"
- "doll-like"
- "porcelain skin"
- "immaculate"

### 💡 Pro Tips:
1. **Lower CFG for natural results:** 6.0-7.0 is ideal (8.0+ often looks plastic)
2. **Specify lighting:** "natural window light", "golden hour", "studio lighting"
3. **Add environment context:** "in modern office", "outdoor park", "home studio"
4. **Describe expression:** "confident", "thoughtful", "genuine smile"
5. **Include subtle imperfections:** "slight stubble", "casual hair", "natural makeup"

---

## 🔧 Avoiding the "Plastic AI Look"

The updated workflow automatically prevents plastic-looking results by:

### 1. **Enhanced Negative Prompts** (Automatic)
When `realism: true`, these are automatically added to negative prompt:
```
plastic, doll, fake, mannequin, smooth skin, oversharpened,
artificial, synthetic, airbrushed, waxy skin, porcelain skin
```

### 2. **Quality Tags** (Automatic)
These are automatically added to your prompt:
```
detailed skin texture, natural pores, realistic lighting,
professional photography, sharp focus, 8k uhd, high quality,
natural colors, soft shadows, realistic depth of field
```

### 3. **Optimal Sampler Settings**
- **Sampler:** `dpmpp_2m_sde_gpu` (best for photorealism)
- **Scheduler:** `karras` (smoother, more natural results)
- **Steps:** 30-40 (sweet spot for quality vs. speed)

### 4. **Premium SDXL Models**
- **RealVisXL V5.0** - Hyper-realistic, especially skin/hair
- **JuggernautXL V10** - Versatile photorealism
- **NightVision XL** - Excellent for natural scenes

---

## 📊 Quality Presets

### Draft Quality (Fast)
```json
{
  "realism": true,
  "steps": 20,
  "cfg": 7.0,
  "upscale": false
}
```
**Time:** ~15-20 seconds | **Resolution:** 1024x1024

### Standard Quality (Balanced)
```json
{
  "realism": true,
  "steps": 30,
  "cfg": 7.0,
  "upscale": true
}
```
**Time:** ~30-45 seconds | **Resolution:** 4096x4096

### High Quality (Recommended)
```json
{
  "realism": true,
  "steps": 35,
  "cfg": 6.5,
  "upscale": true,
  "sampler_name": "dpmpp_2m_sde_gpu"
}
```
**Time:** ~40-60 seconds | **Resolution:** 4096x4096

### Ultra Quality (Maximum Detail)
```json
{
  "realism": true,
  "steps": 40,
  "cfg": 6.0,
  "upscale": true,
  "use_secondary_upscaler": true,
  "sampler_name": "dpmpp_2m_sde_gpu",
  "scheduler": "karras"
}
```
**Time:** ~60-90 seconds | **Resolution:** 4096x4096 (extra sharp)

---

## 🖼️ Resolution Guide

### Standard Sizes (Pre-Upscale)

| Size | Dimensions | Aspect Ratio | Use Case | Final 4K Size |
|------|------------|--------------|----------|---------------|
| Square | 1024x1024 | 1:1 | Profile pictures | 4096x4096 |
| Portrait | 768x1024 | 3:4 | Headshots | 3072x4096 |
| Tall Portrait | 1024x1536 | 2:3 | Full body | 4096x6144 |
| Landscape | 1024x768 | 4:3 | Wide shots | 4096x3072 |

**Note:** All sizes are 4x upscaled when `upscale: true`

---

## 🚨 Troubleshooting

### Issue: "Model not found" error
**Solution:**
```bash
# Check if models are installed
ls -la /path/to/ComfyUI/models/checkpoints/
ls -la /path/to/ComfyUI/models/upscale_models/

# Download models using setup script from MODEL_SETUP_GUIDE.md
```

### Issue: Still getting plastic/fake look
**Solution:**
1. Lower CFG to 6.0-6.5
2. Add more natural descriptors to prompt
3. Avoid words like "perfect", "flawless", "smooth"
4. Increase steps to 40+
5. Try different checkpoint (JuggernautXL vs RealVisXL)

### Issue: Out of VRAM
**Solution:**
1. Reduce base resolution: `"width": 768, "height": 768`
2. Lower steps: `"steps": 25`
3. Disable secondary upscaler: `"use_secondary_upscaler": false`
4. Start ComfyUI with `--lowvram` flag

### Issue: Too slow
**Solution:**
1. Use Lightning model: `"checkpoint": "RealvisXL_Lightning.safetensors"`
2. Reduce steps: `"steps": 6` (for Lightning models)
3. Skip upscaling for drafts: `"upscale": false`

---

## 📚 Complete Working Example

```bash
#!/bin/bash
# Generate a stunning photorealistic 4K portrait

API_URL="http://localhost:8000/avatarforge-controller/generate/avatar"

curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "professional portrait of a software engineer in modern office, natural confident expression, looking at camera, tech workspace background",
    "clothing": "casual tech company attire, hoodie over collared shirt",
    "realism": true,
    "upscale": true,
    "steps": 35,
    "cfg": 6.5,
    "width": 1024,
    "height": 1024,
    "sampler_name": "dpmpp_2m_sde_gpu",
    "scheduler": "karras"
  }' | jq .

# Wait for completion
GENERATION_ID=$(curl -s "$API_URL" ... | jq -r '.generation_id')

# Check status
curl "http://localhost:8000/avatarforge-controller/generations/$GENERATION_ID" | jq .

# Download result
curl "http://localhost:8000/avatarforge-controller/files/{file_id}" -o result_4k.png
```

---

## 🎯 Next Steps

1. ✅ Set up models using `docs/MODEL_SETUP_GUIDE.md`
2. ✅ Start ComfyUI: `cd ComfyUI && python main.py`
3. ✅ Start AvatarForge API: `cd avatarforge && uv run python main.py`
4. ✅ Test with example above
5. ✅ Experiment with different prompts and settings
6. ✅ Check output quality - should see **stunning, realistic photos!**

---

**Ready to generate photorealistic 4K avatars that look like real photography! 📸✨**

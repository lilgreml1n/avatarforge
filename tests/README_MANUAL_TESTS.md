# Manual Test Scripts

This directory contains manual test scripts for generating and testing AI influencer images with various quality settings.

## 📁 Directory Structure

```
tests/
├── unit/                          # Unit tests (pytest)
├── integration/                   # Integration tests (pytest)
├── test_*.py                      # Automated pytest tests
└── Manual Tests (below)           # Manual generation scripts
```

## 🎨 Photorealistic Generation Tests

### `generate_5_photorealistic.py` ⭐ **RECOMMENDED**
**Generates 5 high-quality photorealistic images with optimized settings**

**Features:**
- ✅ Realistic Vision v5.1 model
- ✅ Enhanced eye-fixing prompts
- ✅ Negative prompts for artifact removal
- ✅ Optimized sampler (dpmpp_2m_karras)
- ✅ 50 steps, CFG 7.0
- ✅ Batch generation (5 images)

**Usage:**
```bash
cd /home/raven/Documents/git/avatarforge/tests
python3 generate_5_photorealistic.py
```

**Output:**
- 5 images: `photorealistic_1_*.png` through `photorealistic_5_*.png`
- Average: 16s per image
- Resolution: 768x1024

---

### `photorealistic_test.py`
**Single photorealistic image generation with optimized settings**

**Features:**
- Realistic Vision v5.1 model
- Negative prompts
- Better sampler
- Single image generation

**Usage:**
```bash
python3 photorealistic_test.py
```

**Output:**
- Single image: `photorealistic_*.png`

---

### `natural_looking_test.py`
**Natural looking fitness influencer with simpler settings**

**Features:**
- Simple, clean prompts
- Lower CFG (5.5) for more natural results
- 40 steps
- Front view

**Usage:**
```bash
python3 natural_looking_test.py
```

**Output:**
- Single image: `fitness_NATURAL_*.png`

---

## 👁️ Inpainting Tests (Advanced)

### `inpaint_complete_example.py`
**Complete inpainting workflow demonstration**

**Features:**
- Stage 1: Generate base image
- Stage 2: Create eye mask automatically
- Stage 3: Inpaint ONLY the eyes with focused prompt
- Preserves everything except masked area

**Usage:**
```bash
python3 inpaint_complete_example.py
```

**Output:**
- `base_image_*.png` - Original generated image
- `eye_mask_*.png` - Mask for eye region
- `inpainted_eyes_*.png` - Final result with fixed eyes

**Note:** Requires inpainting endpoint to be fully functional

---

### `inpaint_eyes_fix.py`
**Inpainting eye fix demo (conceptual)**

Demonstrates the concept of inpainting for eye fixes.

**Usage:**
```bash
python3 inpaint_eyes_fix.py
```

---

## 🧪 Legacy/Experimental Tests

### `test_fitness_influencer.py`
Original fitness influencer test with basic settings

### `test_fitness_influencer_enhanced.py`
Enhanced version with better quality settings

### `test_fitness_influencer_variations.py`
Tests multiple variations of fitness influencer

### `quick_enhanced_test.py`
Quick test with enhanced settings

### `ultimate_quality_test.py`
Maximum quality test with highest settings

---

## 📊 Comparison of Test Scripts

| Script | Model | Steps | CFG | Sampler | Eye Fix | Batch | Quality |
|--------|-------|-------|-----|---------|---------|-------|---------|
| `generate_5_photorealistic.py` | RV 5.1 | 50 | 7.0 | dpmpp_2m_karras | ✅ | 5 | ⭐⭐⭐⭐⭐ |
| `photorealistic_test.py` | RV 5.1 | 50 | 7.0 | dpmpp_2m_karras | ✅ | 1 | ⭐⭐⭐⭐⭐ |
| `natural_looking_test.py` | RV 5.1 | 40 | 5.5 | euler_a | ❌ | 1 | ⭐⭐⭐⭐ |
| `ultimate_quality_test.py` | RV 5.1 | 80-100 | 7.5 | Various | ⚠️ | 1 | ⭐⭐⭐⭐ |
| `inpaint_complete_example.py` | RV 5.1 | 60 | 7.0 | dpmpp_2m_karras | ✅✅ | 1 | ⭐⭐⭐⭐⭐ |

**Legend:**
- RV 5.1 = Realistic Vision v5.1
- Eye Fix: ✅ = Enhanced prompts, ✅✅ = Inpainting, ❌ = None, ⚠️ = Basic
- Quality: More stars = better results

---

## 🎯 Recommended Workflow

For best results, use this workflow:

### 1. Quick Single Test
```bash
python3 photorealistic_test.py
```

### 2. Batch Generation (5 images)
```bash
python3 generate_5_photorealistic.py
```

### 3. Advanced: Inpaint Fix (if needed)
```bash
python3 inpaint_complete_example.py
```

---

## 🔧 Configuration Notes

### Model Requirements
All photorealistic tests require:
- **Model:** `realisticVisionV51_v51VAE.safetensors`
- **Location:** `/home/raven/Documents/ComfyUI/models/checkpoints/`
- **Size:** ~2.0 GB
- **Download:** Already installed ✅

### API Endpoints
- **Generation API:** `http://192.168.100.133:8000/avatarforge-controller`
- **ComfyUI:** `http://192.168.100.133:8188`

### Eye-Fixing Prompts
The enhanced scripts use:

**Positive:**
```
clear sharp symmetrical eyes, focused eyes, bright eyes, detailed eyes
```

**Negative:**
```
blurry eyes, cross-eyed, asymmetrical eyes, weird pupils, unfocused eyes,
lazy eye, uneven eyes
```

---

## 📝 Adding New Tests

To add a new manual test:

1. Create your script in `tests/` directory
2. Use descriptive naming: `test_[feature]_[variation].py`
3. Follow the existing structure
4. Update this README with:
   - Script description
   - Usage instructions
   - Output format
   - Comparison table entry

---

## 🐛 Troubleshooting

### Images have weird eyes
- ✅ Use `generate_5_photorealistic.py` (has eye-fixing prompts)
- ✅ Try `inpaint_complete_example.py` for surgical fixes

### Poor quality/unrealistic
- ✅ Check model is Realistic Vision v5.1
- ✅ Increase steps to 50+
- ✅ Use dpmpp_2m_karras sampler
- ✅ Add negative prompts

### Slow generation
- ⚡ Reduce steps (40 minimum)
- ⚡ Use euler_a sampler
- ⚡ Lower resolution (512x768)

### API errors
- 🔧 Check ComfyUI is running: http://192.168.100.133:8188
- 🔧 Check AvatarForge API is running
- 🔧 Verify model is loaded

---

## 📚 Additional Resources

- **Main Documentation:** `/home/raven/Documents/git/avatarforge/docs/`
- **API Reference:** See API documentation
- **Model Setup:** `setup_high_quality_models.py` (root directory)
- **Test Results:** `FITNESS_INFLUENCER_TEST_RESULTS.md` (root directory)

---

**Last Updated:** 2025-11-15
**Model Version:** Realistic Vision v5.1
**Best Script:** `generate_5_photorealistic.py` ⭐

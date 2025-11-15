# Avatar Generation Guide

Complete guide to generating avatars using the AvatarForge API.

## Table of Contents
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Generation Parameters](#generation-parameters)
- [Step-by-Step Process](#step-by-step-process)
- [Advanced Usage](#advanced-usage)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
1. AvatarForge API server running on `http://localhost:8000` (or your server IP)
2. ComfyUI running on `http://localhost:8188`

### Simplest Generation

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "fantasy warrior with sword",
    "realism": false
  }'
```

---

## API Endpoints

### 1. Generate Avatar
**Endpoint:** `POST /avatarforge-controller/generate/avatar`

Generate a single avatar with full customization.

### 2. Generate Specific Pose
**Endpoint:** `POST /avatarforge-controller/generate_pose?pose={pose_type}`

Generate avatar with specific pose (front, back, side, quarter).

### 3. Generate All Poses
**Endpoint:** `POST /avatarforge-controller/generate_all_poses`

Generate all 4 pose views in one request.

### 4. Check Generation Status
**Endpoint:** `GET /avatarforge-controller/generations/{generation_id}`

Check the status and retrieve results.

### 5. List All Generations
**Endpoint:** `GET /avatarforge-controller/generations`

List all your generations.

---

## Generation Parameters

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `prompt` | string | Detailed description of the avatar | `"female warrior, blue armor"` |

### Optional Parameters

| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `clothing` | string | `null` | Specific clothing details | `"leather jacket, jeans"` |
| `realism` | boolean | `false` | true=photorealistic, false=anime/stylized | `true` |
| `style` | string | `null` | Art style modifier | `"watercolor"` |
| `width` | integer | `512` | Image width in pixels | `768` |
| `height` | integer | `512` | Image height in pixels | `768` |
| `steps` | integer | `20` | Generation steps (more = better quality) | `35` |
| `cfg` | float | `7.0` | CFG scale (prompt adherence strength) | `8.5` |
| `sampler_name` | string | `"euler"` | Sampler algorithm | `"dpmpp_2m"` |
| `pose_file_id` | string | `null` | Uploaded pose reference image ID | `"file_abc123"` |
| `reference_file_id` | string | `null` | Uploaded style reference image ID | `"file_def456"` |

### Available Samplers
- `euler` - Fast, simple (default)
- `euler_a` - Ancestral, more creative
- `dpmpp_2m` - High quality, recommended for detailed images
- `dpmpp_sde` - Very high quality, slower
- `ddim` - Deterministic, consistent results

### Available Styles
- `"cel-shaded"` - Cartoon/comic book style
- `"watercolor"` - Watercolor painting
- `"oil painting"` - Oil painting style
- `"pixel art"` - Retro pixel art
- `"comic book"` - Comic book illustration

---

## Step-by-Step Process

### Method 1: Using cURL (Command Line)

#### Step 1: Submit Generation Request

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cyberpunk hacker with neon visor",
    "clothing": "black leather jacket, tech accessories",
    "realism": false,
    "width": 768,
    "height": 768,
    "steps": 30,
    "cfg": 8.0,
    "sampler_name": "dpmpp_2m"
  }' | jq
```

**Response:**
```json
{
  "generation_id": "790e89ad-1772-4017-a593-36f95c336c83",
  "status": "processing",
  "message": "Generation processing",
  "comfyui_prompt_id": "49150e32-9387-4711-85a5-697981e50bbf",
  "created_at": "2025-11-15T13:39:21",
  "started_at": "2025-11-15T13:39:21.937374"
}
```

#### Step 2: Wait for Generation

Wait 20-60 seconds depending on resolution and steps.

#### Step 3: Check Status

```bash
curl "http://localhost:8000/avatarforge-controller/generations/790e89ad-1772-4017-a593-36f95c336c83" | jq
```

#### Step 4: Retrieve Image

Once complete, get the image from ComfyUI:

```bash
# Method 1: Direct URL (view in browser)
http://localhost:8188/view?filename=avatarforge_00005_.png&type=output

# Method 2: Download via curl
curl "http://localhost:8188/view?filename=avatarforge_00005_.png&type=output" \
  -o my_avatar.png
```

### Method 2: Using Python

```python
import requests
import time
import json

# Configuration
API_URL = "http://localhost:8000/avatarforge-controller"
COMFYUI_URL = "http://localhost:8188"

# Step 1: Submit generation request
payload = {
    "prompt": "epic dragon warrior, detailed armor",
    "clothing": "ornate plate armor with dragon motifs",
    "realism": False,
    "width": 768,
    "height": 768,
    "steps": 30,
    "cfg": 8.0,
    "sampler_name": "dpmpp_2m"
}

response = requests.post(f"{API_URL}/generate/avatar", json=payload)
result = response.json()

generation_id = result["generation_id"]
comfyui_prompt_id = result["comfyui_prompt_id"]

print(f"Generation started: {generation_id}")
print(f"ComfyUI Prompt ID: {comfyui_prompt_id}")

# Step 2: Wait for completion
print("Waiting for generation...")
time.sleep(40)  # Adjust based on your settings

# Step 3: Check ComfyUI for result
history_response = requests.get(f"{COMFYUI_URL}/history/{comfyui_prompt_id}")
history = history_response.json()

if comfyui_prompt_id in history:
    outputs = history[comfyui_prompt_id].get("outputs", {})
    if "7" in outputs:  # Node 7 is SaveImage in our workflow
        images = outputs["7"].get("images", [])
        if images:
            filename = images[0]["filename"]
            image_url = f"{COMFYUI_URL}/view?filename={filename}&type=output"

            print(f"\n✅ Generation complete!")
            print(f"📷 Image URL: {image_url}")

            # Optional: Download the image
            image_response = requests.get(image_url)
            with open("avatar.png", "wb") as f:
                f.write(image_response.content)
            print(f"💾 Downloaded to: avatar.png")
```

### Method 3: Using JavaScript/TypeScript

```javascript
const API_URL = "http://localhost:8000/avatarforge-controller";
const COMFYUI_URL = "http://localhost:8188";

async function generateAvatar() {
  // Step 1: Submit generation request
  const response = await fetch(`${API_URL}/generate/avatar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: "mystical elf archer in forest",
      clothing: "green cloak, leather armor",
      realism: false,
      width: 768,
      height: 768,
      steps: 30,
      cfg: 8.0,
      sampler_name: "dpmpp_2m"
    })
  });

  const result = await response.json();
  console.log("Generation started:", result.generation_id);

  // Step 2: Wait for completion
  await new Promise(resolve => setTimeout(resolve, 40000));

  // Step 3: Get result from ComfyUI
  const historyResponse = await fetch(
    `${COMFYUI_URL}/history/${result.comfyui_prompt_id}`
  );
  const history = await historyResponse.json();

  const outputs = history[result.comfyui_prompt_id]?.outputs;
  const filename = outputs?.["7"]?.images?.[0]?.filename;

  if (filename) {
    const imageUrl = `${COMFYUI_URL}/view?filename=${filename}&type=output`;
    console.log("✅ Image ready:", imageUrl);
    return imageUrl;
  }
}

generateAvatar();
```

---

## Advanced Usage

### Multi-Pose Generation

Generate all 4 poses (front, back, side, quarter) of the same character:

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate_all_poses" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight in silver armor",
    "clothing": "full plate armor, red cape",
    "realism": false
  }' | jq
```

### Using Reference Images

#### Step 1: Upload Reference Image

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/upload/pose_image" \
  -F "file=@/path/to/pose_reference.png"
```

**Response:**
```json
{
  "file_id": "pose_abc123",
  "filename": "pose_reference.png",
  "content_hash": "sha256_hash_here"
}
```

#### Step 2: Generate with Reference

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "warrior in battle stance",
    "pose_file_id": "pose_abc123",
    "realism": false
  }'
```

### Quality Presets

#### Draft Quality (Fast)
```json
{
  "width": 512,
  "height": 512,
  "steps": 15,
  "cfg": 7.0,
  "sampler_name": "euler"
}
```

#### Standard Quality
```json
{
  "width": 768,
  "height": 768,
  "steps": 25,
  "cfg": 7.5,
  "sampler_name": "dpmpp_2m"
}
```

#### High Quality (Slow)
```json
{
  "width": 1024,
  "height": 1024,
  "steps": 40,
  "cfg": 8.5,
  "sampler_name": "dpmpp_sde"
}
```

---

## Examples

### Example 1: Photorealistic Portrait

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "professional headshot of a business executive, confident expression, studio lighting",
    "clothing": "grey suit, blue tie",
    "realism": true,
    "width": 768,
    "height": 768,
    "steps": 35,
    "cfg": 8.0,
    "sampler_name": "dpmpp_2m"
  }'
```

### Example 2: Fantasy Character

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "powerful wizard casting spell, magical aura, dramatic pose",
    "clothing": "purple robes with golden runes, wizard hat, staff",
    "realism": false,
    "style": "oil painting",
    "width": 768,
    "height": 1024,
    "steps": 30,
    "cfg": 8.5
  }'
```

### Example 3: Cyberpunk Style

```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cyberpunk netrunner with glowing implants, neon city background",
    "clothing": "black tactical jacket, tech visor, cybernetic arms",
    "realism": false,
    "width": 768,
    "height": 768,
    "steps": 30,
    "cfg": 8.0
  }'
```

---

## Troubleshooting

### Issue: Generation stays in "processing" status

**Cause:** ComfyUI may have encountered an error.

**Solution:**
1. Check ComfyUI logs
2. Verify ComfyUI is running: `http://localhost:8188`
3. Check ComfyUI history directly: `curl http://localhost:8188/history/{comfyui_prompt_id}`

### Issue: Low quality images

**Solutions:**
- Increase `steps` (25-40)
- Increase `cfg` (7.5-9.0)
- Use better sampler: `"dpmpp_2m"` or `"dpmpp_sde"`
- Increase resolution: `768x768` or higher
- Add quality keywords to prompt: "detailed", "high quality", "8k", "masterpiece"

### Issue: Generation too slow

**Solutions:**
- Reduce `steps` (15-20)
- Reduce resolution (`512x512`)
- Use faster sampler: `"euler"`
- Upgrade hardware (GPU)

### Issue: Image doesn't match prompt

**Solutions:**
- Increase `cfg` value (8.0-10.0)
- Make prompt more specific and detailed
- Add negative prompts (currently hardcoded)
- Try different samplers

---

## Best Practices

### 1. Prompt Writing Tips

**Good prompts:**
- Be specific and detailed
- Include style keywords
- Mention lighting and composition
- Describe character features clearly

**Example:**
```
"medieval knight in ornate silver armor, noble expression,
holding longsword, castle background, dramatic lighting,
high detail, fantasy art style"
```

### 2. Parameter Tuning

- **Draft/Testing:** `steps=15-20, cfg=7.0, 512x512`
- **Production:** `steps=25-35, cfg=7.5-8.5, 768x768`
- **High Quality:** `steps=35-50, cfg=8.0-9.0, 1024x1024`

### 3. CFG Scale Guidelines

- `5.0-6.0`: Very creative, may deviate from prompt
- `7.0-8.0`: Balanced (recommended)
- `8.5-10.0`: Strong adherence to prompt
- `10.0+`: May over-saturate or distort

### 4. Performance Tips

- Start with lower resolution and steps for testing
- Use `euler` sampler for quick iterations
- Switch to `dpmpp_2m` for final generation
- Consider batch generation during off-peak hours

---

## API Reference

### Interactive Documentation

Access the full interactive API documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Response Format

All generation endpoints return:

```json
{
  "generation_id": "uuid-string",
  "status": "queued|processing|completed|failed",
  "message": "Human-readable status message",
  "workflow": { /* ComfyUI workflow JSON */ },
  "output_files": ["filename1.png", "filename2.png"],
  "created_at": "ISO-8601 timestamp",
  "started_at": "ISO-8601 timestamp",
  "completed_at": "ISO-8601 timestamp",
  "error": "Error message if failed",
  "comfyui_prompt_id": "uuid-string"
}
```

---

## Remote Access

### From Another Computer

Replace `localhost` with your server's IP address:

```bash
# If server IP is 192.168.1.100
curl -X POST "http://192.168.1.100:8000/avatarforge-controller/generate/avatar" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "warrior", "realism": false}'

# View image
http://192.168.1.100:8188/view?filename=avatarforge_00001_.png&type=output
```

---

## Next Steps

- Check out [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) for complete API reference
- See [TODO.md](../TODO.md) for upcoming features
- Review [README.md](../README.md) for installation and setup

---

**Last Updated:** 2025-01-15

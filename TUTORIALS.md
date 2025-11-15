# AvatarForge - Complete Tutorial Series

**From zero to hero. Step-by-step. Every skill level.**

Complete tutorial series covering everything from installation to advanced automation.

---

## 📚 Tutorial Index

### Beginner Tutorials
1. [Getting Started - Your First Avatar](#tutorial-1-getting-started---your-first-avatar) (15 min)
2. [Upload and Use Pose Images](#tutorial-2-upload-and-use-pose-images) (20 min)
3. [Understanding Prompts](#tutorial-3-understanding-prompts) (25 min)
4. [Working with Different Poses](#tutorial-4-working-with-different-poses) (20 min)

### Intermediate Tutorials
5. [Batch Avatar Generation](#tutorial-5-batch-avatar-generation) (30 min)
6. [Creating Character Sheets](#tutorial-6-creating-character-sheets) (30 min)
7. [Smart File Management](#tutorial-7-smart-file-management) (25 min)
8. [Building a Simple Web Interface](#tutorial-8-building-a-simple-web-interface) (45 min)

### Advanced Tutorials
9. [Automated Workflow with Python](#tutorial-9-automated-workflow-with-python) (40 min)
10. [Integration with Discord Bot](#tutorial-10-integration-with-discord-bot) (60 min)
11. [Building a Character Generator App](#tutorial-11-building-a-character-generator-app) (90 min)
12. [Performance Optimization](#tutorial-12-performance-optimization) (30 min)

---

## Tutorial 1: Getting Started - Your First Avatar

**Time:** 15 minutes
**Level:** Beginner
**Prerequisites:** None

### What You'll Learn
- Install and set up AvatarForge
- Start the API server
- Generate your first avatar
- View and download results

### Step 1: Installation

**1.1 Clone the repository**
```bash
# Open terminal
cd ~/Projects

# Clone repo
git clone https://github.com/yourusername/avatarforge.git
cd avatarforge
```

**1.2 Set up Python environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Verify activation
which python
# Should show path to venv/bin/python
```

**1.3 Install dependencies**
```bash
# Install all required packages
pip install -r requirements.txt

# This will take 2-3 minutes
```

**1.4 Set up configuration**
```bash
# Copy example environment file
cp .env.example .env

# Open .env in your editor
nano .env  # or vim, code, etc.

# Edit these values:
SECRET_KEY=change-this-to-something-random
COMFYUI_URL=http://localhost:8188
DATABASE_URL=sqlite:///./avatarforge.db
```

**1.5 Initialize database**
```bash
python -m avatarforge.database.init_db

# You should see:
# ✓ Database initialized successfully
```

### Step 2: Start ComfyUI

**2.1 Navigate to ComfyUI directory**
```bash
# In a NEW terminal window
cd /path/to/ComfyUI
```

**2.2 Start ComfyUI**
```bash
python main.py

# Wait for:
# "To see the GUI go to: http://127.0.0.1:8188"
```

**2.3 Verify ComfyUI is running**
```bash
# Open browser to:
http://localhost:8188

# You should see the ComfyUI interface
```

### Step 3: Start AvatarForge API

**3.1 Start the server (in avatarforge directory)**
```bash
# Make sure you're in avatarforge directory
cd ~/Projects/avatarforge

# Activate venv if not already active
source venv/bin/activate

# Start server
python main.py

# Or with uvicorn directly:
uvicorn main:app --reload
```

**3.2 Verify API is running**
```bash
# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**3.3 Test API health**
```bash
# In a new terminal:
curl http://localhost:8000/avatarforge-controller/health

# Should return:
# {
#   "api_status": "healthy",
#   "comfyui": {"status": "healthy", ...}
# }
```

### Step 4: Generate Your First Avatar

**4.1 Open Swagger UI**
```
Open browser to: http://localhost:8000/docs
```

**4.2 Find the generate avatar endpoint**
```
Scroll to: POST /avatarforge-controller/generate/avatar
Click "Try it out"
```

**4.3 Enter your prompt**
```json
{
  "prompt": "female warrior character, blue armor, long white hair, determined expression",
  "realism": false
}
```

**4.4 Click "Execute"**

**4.5 Copy the generation_id from response**
```json
{
  "generation_id": "abc-123-def-456",
  "status": "processing",
  ...
}
```

### Step 5: Check Generation Status

**5.1 Find the status endpoint**
```
Scroll to: GET /avatarforge-controller/generations/{generation_id}
Click "Try it out"
```

**5.2 Paste your generation_id**
```
generation_id: abc-123-def-456
Click "Execute"
```

**5.3 Wait for completion**
```
Keep clicking "Execute" every few seconds

When status changes to "completed", you'll see:
{
  "status": "completed",
  "output_files": [
    {
      "filename": "output.png",
      "url": "/outputs/abc-123-def-456/output.png"
    }
  ]
}
```

### Step 6: View Your Avatar

**6.1 Access the image**
```
Open in browser:
http://localhost:8000/outputs/abc-123-def-456/output.png
```

**6.2 Download the image**
```bash
# Or download with curl:
curl http://localhost:8000/outputs/abc-123-def-456/output.png \
  --output my_first_avatar.png
```

**6.3 Celebrate!**
```
🎉 You just generated your first avatar!
```

### Step 7: Try Different Prompts

**Experiment with these prompts:**

```json
// Fantasy mage
{
  "prompt": "male mage character, purple robes, staff, wise expression",
  "realism": false
}

// Cyberpunk character
{
  "prompt": "cyberpunk character, neon hair, tech implants, leather jacket",
  "realism": false
}

// Realistic portrait
{
  "prompt": "professional portrait, business attire, confident smile",
  "realism": true
}
```

### Troubleshooting

**Problem:** ComfyUI not found
```
Solution: Verify COMFYUI_URL in .env matches where ComfyUI is running
```

**Problem:** Generation stuck in "processing"
```
Solution: Check ComfyUI terminal for errors
Restart ComfyUI if needed
```

**Problem:** "Model not found" error
```
Solution: Download required models
See MODEL_SETUP.md
```

### What's Next?

✅ Tutorial 1 Complete!

**Next Steps:**
- Tutorial 2: Learn to use pose images
- Tutorial 3: Master prompt writing
- Tutorial 4: Generate multiple pose views

---

## Tutorial 2: Upload and Use Pose Images

**Time:** 20 minutes
**Level:** Beginner
**Prerequisites:** Tutorial 1 completed

### What You'll Learn
- Upload pose reference images
- Use poses in generation
- Understand deduplication
- Download and reuse files

### Step 1: Prepare Pose Images

**1.1 Find or create pose images**
```
Sources:
- Your own photos
- Stock photo sites (Unsplash, Pexels)
- Pose reference sites (JustSketchMe, PoseManiacs)
```

**1.2 Ensure image meets requirements**
```
Format: PNG, JPG, JPEG, or WEBP
Size: Under 50MB
Dimensions: 64x64 to 4096x4096 pixels
```

**1.3 Save image locally**
```bash
# Example
~/Pictures/pose_standing.png
```

### Step 2: Upload Via API

**2.1 Using curl**
```bash
curl -X POST http://localhost:8000/avatarforge-controller/upload/pose_image \
  -F "file=@~/Pictures/pose_standing.png"
```

**2.2 Response**
```json
{
  "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "pose_standing.png",
  "content_hash": "sha256hash...",
  "size": 1024567,
  "mime_type": "image/png",
  "dimensions": {"width": 512, "height": 768},
  "url": "/files/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "is_duplicate": false,
  "created_at": "2025-01-15T10:30:00Z"
}
```

**2.3 Save the file_id**
```bash
# Copy this for later use:
a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### Step 3: Upload Via Swagger UI

**3.1 Open Swagger**
```
http://localhost:8000/docs
```

**3.2 Find upload endpoint**
```
POST /avatarforge-controller/upload/pose_image
Click "Try it out"
```

**3.3 Select file**
```
Click "Choose File"
Select your pose image
Click "Execute"
```

**3.4 Copy file_id from response**

### Step 4: Use Pose in Generation

**4.1 Generate with pose**
```json
{
  "prompt": "warrior character, blue armor, combat stance",
  "pose_file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "realism": false
}
```

**4.2 Execute and wait for completion**

**4.3 Compare results**
```
Generated avatar should match the pose from your uploaded image!
```

### Step 5: Understanding Deduplication

**5.1 Upload the same image again**
```bash
curl -X POST http://localhost:8000/avatarforge-controller/upload/pose_image \
  -F "file=@~/Pictures/pose_standing.png"
```

**5.2 Notice the response**
```json
{
  "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",  // Same ID!
  "is_duplicate": true,  // Flagged as duplicate
  ...
}
```

**5.3 Benefits of deduplication**
```
✓ Saves storage space
✓ Faster uploads (file already exists)
✓ Same file_id can be reused
✓ Automatic reference counting
```

### Step 6: Download Uploaded Files

**6.1 Using curl**
```bash
curl http://localhost:8000/avatarforge-controller/files/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  --output downloaded_pose.png
```

**6.2 Using browser**
```
http://localhost:8000/files/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**6.3 Verify file**
```bash
# Check downloaded file
file downloaded_pose.png
# Should show: PNG image data
```

### Step 7: Upload Multiple Poses

**7.1 Create a script**
```python
# upload_poses.py
import requests
import os

def upload_pose(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/avatarforge-controller/upload/pose_image',
            files={'file': f}
        )

    result = response.json()
    print(f"✓ {os.path.basename(file_path)}: {result['file_id']}")
    return result['file_id']

# Upload multiple poses
poses = [
    '~/Pictures/pose_standing.png',
    '~/Pictures/pose_sitting.png',
    '~/Pictures/pose_running.png'
]

file_ids = {}
for pose in poses:
    expanded_path = os.path.expanduser(pose)
    name = os.path.basename(pose)
    file_ids[name] = upload_pose(expanded_path)

print("\n Uploaded file IDs:")
for name, file_id in file_ids.items():
    print(f"{name}: {file_id}")
```

**7.2 Run script**
```bash
python upload_poses.py
```

**7.3 Save file IDs for later**
```bash
# Output:
# pose_standing.png: a1b2c3d4...
# pose_sitting.png: b2c3d4e5...
# pose_running.png: c3d4e5f6...
```

### Step 8: Upload Reference Image

**8.1 What's a reference image?**
```
Reference image = style/appearance reference
Pose image = position/pose reference

You can use both together!
```

**8.2 Upload reference**
```bash
curl -X POST http://localhost:8000/avatarforge-controller/upload/reference_image \
  -F "file=@~/Pictures/armor_style.jpg"
```

**8.3 Use both in generation**
```json
{
  "prompt": "warrior character, determined expression",
  "pose_file_id": "a1b2c3d4-...",      // Standing pose
  "reference_file_id": "d4e5f6g7-...", // Armor style
  "realism": false
}
```

### Practice Exercise

**Create 3 avatars with different poses:**

1. Upload 3 different pose images
2. Generate warrior with each pose
3. Compare the results
4. Download all 3 generated avatars

### Key Takeaways

✓ Upload images before using them
✓ Deduplication saves storage automatically
✓ Reuse file_ids across multiple generations
✓ Combine pose + reference for best results

---

## Tutorial 3: Understanding Prompts

**Time:** 25 minutes
**Level:** Beginner
**Prerequisites:** Tutorial 1, 2 completed

### What You'll Learn
- Write effective prompts
- Use prompt structure
- Understand prompt elements
- Avoid common mistakes

### Part 1: Prompt Basics

**3.1 What makes a good prompt?**
```
Good prompts are:
✓ Specific and detailed
✓ Well-structured
✓ Use descriptive adjectives
✓ Include style guidance
```

**3.2 Bad vs Good prompts**

**Bad:**
```json
{"prompt": "person"}
```
Too vague, unclear what to generate

**Better:**
```json
{"prompt": "warrior"}
```
More specific but still lacking detail

**Good:**
```json
{"prompt": "female warrior character, blue armor, long white hair"}
```
Detailed with key elements

**Best:**
```json
{"prompt": "female warrior character, blue plate armor with gold trim, long flowing white hair, determined expression, battle-ready stance"}
```
Very detailed with appearance, mood, and pose

### Part 2: Prompt Structure

**3.3 Basic structure**
```
[Subject] [Appearance] [Clothing] [Expression] [Setting/Action]
```

**Examples:**

```json
// Character fantasy
{
  "prompt": "male elf ranger, green leather armor, brown hair, calm expression, forest setting"
}

// Character modern
{
  "prompt": "young woman, casual jeans and t-shirt, brown hair in ponytail, friendly smile, city street"
}

// Character sci-fi
{
  "prompt": "space marine, futuristic power armor, helmet on, heroic pose, spaceship background"
}
```

### Part 3: Key Prompt Elements

**3.4 Subject (Who/What)**
```
Examples:
- "female warrior"
- "male mage"
- "cyberpunk hacker"
- "medieval knight"
- "elven archer"
```

**3.5 Appearance (Physical traits)**
```
Examples:
- "long white hair"
- "blue eyes"
- "muscular build"
- "young adult"
- "pale skin"
- "pointed ears"
```

**3.6 Clothing/Equipment**
```
Examples:
- "blue plate armor"
- "leather jacket"
- "wizard robes"
- "combat gear"
- "formal suit"
```

**3.7 Expression/Mood**
```
Examples:
- "determined expression"
- "friendly smile"
- "serious face"
- "angry"
- "calm and peaceful"
```

**3.8 Pose/Action**
```
Examples:
- "standing confidently"
- "battle stance"
- "sitting casually"
- "running"
- "casting spell"
```

**3.9 Style (optional)**
```
Examples:
- "watercolor painting"
- "digital art"
- "anime style"
- "photorealistic"
- "pixel art"
```

### Part 4: Advanced Techniques

**3.10 Using the clothing parameter**
```json
{
  "prompt": "warrior character, determined expression",
  "clothing": "full plate armor with red cape, silver gauntlets, ornate helmet"
}
```

**3.11 Using the style parameter**
```json
{
  "prompt": "female mage character, purple robes",
  "style": "watercolor painting, soft colors, dreamy atmosphere"
}
```

**3.12 Combining all elements**
```json
{
  "prompt": "female warrior character, long white hair, blue eyes, determined expression, battle stance",
  "clothing": "blue plate armor with gold trim, red cape, sword at side",
  "style": "digital art, dramatic lighting, epic composition",
  "realism": false
}
```

### Part 5: Realism Mode

**3.13 Realism vs Stylized**

**Stylized (realism: false):**
```json
{
  "prompt": "warrior character, blue armor, heroic pose",
  "realism": false
}
```
- More artistic
- Can be more creative
- Better for fantasy/anime

**Realistic (realism: true):**
```json
{
  "prompt": "professional portrait, business attire, confident expression",
  "realism": true
}
```
- Photorealistic
- Natural appearance
- Better for modern/realistic scenes

### Part 6: Common Mistakes

**3.14 Too vague**
```json
// ✗ Bad
{"prompt": "character"}

// ✓ Good
{"prompt": "female warrior character, blue armor, long white hair"}
```

**3.15 Contradictory elements**
```json
// ✗ Bad
{"prompt": "young elderly warrior"}

// ✓ Good
{"prompt": "young warrior" OR "elderly warrior"}
```

**3.16 Too many details**
```json
// ✗ Bad (too long)
{"prompt": "female warrior with blue armor and gold trim and red cape and silver boots and bronze helmet and emerald eyes and..."}

// ✓ Good (concise key details)
{"prompt": "female warrior, blue armor with gold trim, red cape, emerald eyes"}
```

**3.17 Using quality terms**
```json
// ✗ Less effective
{"prompt": "warrior, 8k, high quality, detailed, masterpiece"}

// ✓ Better
{"prompt": "warrior character, blue armor, intricate details"}
```

### Part 7: Practice Exercises

**Exercise 1: Character Design**
```
Design 3 characters:
1. Fantasy warrior
2. Modern professional
3. Sci-fi pilot

Write detailed prompts for each
```

**Exercise 2: Mood Variation**
```
Same character, different expressions:
1. Happy and confident
2. Serious and focused
3. Sad and thoughtful
```

**Exercise 3: Style Exploration**
```
Same prompt, different styles:
1. Watercolor painting
2. Digital art
3. Anime style
```

### Part 8: Prompt Templates

**3.18 Fantasy warrior template**
```json
{
  "prompt": "[gender] [race] warrior, [armor color] armor, [hair description], [expression]",
  "clothing": "[armor details], [cape/accessories]",
  "style": "fantasy art, [lighting]"
}
```

**Example:**
```json
{
  "prompt": "female elf warrior, silver armor, long blonde hair, confident expression",
  "clothing": "ornate elven plate armor, flowing green cape",
  "style": "fantasy art, magical lighting"
}
```

**3.19 Modern character template**
```json
{
  "prompt": "[age] [gender], [hair], [expression], [setting]",
  "clothing": "[outfit description]",
  "style": "photorealistic, [lighting style]"
}
```

**Example:**
```json
{
  "prompt": "young woman, brown hair in bun, friendly smile, office setting",
  "clothing": "professional business suit, glasses",
  "style": "photorealistic, natural lighting"
}
```

**3.20 Sci-fi character template**
```json
{
  "prompt": "[role] [description], [tech elements], [expression]",
  "clothing": "[futuristic outfit/armor]",
  "style": "sci-fi digital art, [color scheme]"
}
```

**Example:**
```json
{
  "prompt": "space marine soldier, cybernetic enhancements, determined expression",
  "clothing": "futuristic power armor, energy weapons",
  "style": "sci-fi digital art, blue and orange color scheme"
}
```

### Key Takeaways

✓ Be specific and detailed
✓ Use clear structure
✓ Include key elements (subject, appearance, clothing, expression)
✓ Experiment with different styles
✓ Avoid contradictions and excessive detail

---

## Tutorial 4: Working with Different Poses

**Time:** 20 minutes
**Level:** Beginner
**Prerequisites:** Tutorials 1, 2, 3 completed

### What You'll Learn
- Generate specific pose views
- Create character sheets
- Understand pose types
- Use multi-view generation

### Part 1: Available Poses

**4.1 Four standard poses**

```
1. Front - Front-facing view, standard proportions
2. Back - Back view, different lighting
3. Side - Side profile, narrow aspect ratio
4. Quarter - 3/4 view, showing partial features
```

**4.2 When to use each**

**Front:**
- Character sheets
- Profile pictures
- Main character views
- Portfolio pieces

**Back:**
- Full character design
- Showing back details (cape, armor back, etc.)
- Turn-around sheets

**Side:**
- Profile shots
- Silhouettes
- Proportion reference

**Quarter:**
- Dynamic poses
- More natural view
- Game character portraits

### Part 2: Generate Specific Pose

**4.3 Using the pose parameter**

**Front view:**
```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=front" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor, red cape",
    "realism": false
  }'
```

**Back view:**
```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=back" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor, red cape",
    "realism": false
  }'
```

**Side view:**
```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=side" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor, red cape",
    "realism": false
  }'
```

**Quarter view:**
```bash
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=quarter" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor, red cape",
    "realism": false
  }'
```

### Part 3: Generate All Poses

**4.4 Create complete character sheet**

```bash
curl -X POST http://localhost:8000/avatarforge-controller/generate_all_poses \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor, red cape",
    "clothing": "full plate armor with ornate details",
    "realism": false
  }'
```

**4.5 Response**
```json
{
  "generation_id": "abc-123-def-456",
  "status": "processing",
  "message": "Generating all 4 pose views"
}
```

**4.6 Check status**
```bash
curl http://localhost:8000/avatarforge-controller/generations/abc-123-def-456
```

**4.7 Completed response**
```json
{
  "status": "completed",
  "output_files": [
    {
      "filename": "front.png",
      "url": "/outputs/abc-123-def-456/front.png",
      "pose_type": "front"
    },
    {
      "filename": "back.png",
      "url": "/outputs/abc-123-def-456/back.png",
      "pose_type": "back"
    },
    {
      "filename": "side.png",
      "url": "/outputs/abc-123-def-456/side.png",
      "pose_type": "side"
    },
    {
      "filename": "quarter.png",
      "url": "/outputs/abc-123-def-456/quarter.png",
      "pose_type": "quarter"
    }
  ]
}
```

### Part 4: Python Script for All Poses

**4.8 Create automated script**

```python
# generate_character_sheet.py
import requests
import time
import os

def generate_character_sheet(prompt, output_dir='character_sheet'):
    """Generate all 4 pose views and download them."""

    # Start generation
    print(f"🎨 Generating character sheet for: {prompt}")
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate_all_poses',
        json={"prompt": prompt, "realism": False}
    )

    generation_id = response.json()['generation_id']
    print(f"✓ Started: {generation_id}\n")

    # Wait for completion
    print("⏳ Waiting for completion", end="")
    while True:
        status = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        ).json()

        if status['status'] == 'completed':
            print("\n\n✅ Generation complete!\n")
            break
        elif status['status'] == 'failed':
            print(f"\n❌ Failed: {status.get('error')}")
            return None

        print(".", end="", flush=True)
        time.sleep(3)

    # Download files
    os.makedirs(output_dir, exist_ok=True)

    print(f"📥 Downloading to {output_dir}/")
    for output in status['output_files']:
        pose_type = output.get('pose_type', 'output')
        filename = f"{pose_type}.png"
        filepath = os.path.join(output_dir, filename)

        url = f"http://localhost:8000{output['url']}"
        response = requests.get(url)

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"   ✓ {filename}")

    print(f"\n✅ Character sheet complete!")
    print(f"   Location: {output_dir}/")

# Usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_character_sheet.py 'your prompt here'")
        sys.exit(1)

    prompt = sys.argv[1]
    generate_character_sheet(prompt)
```

**4.9 Use the script**
```bash
python generate_character_sheet.py "warrior character, blue armor"

# Creates:
# character_sheet/
#   front.png
#   back.png
#   side.png
#   quarter.png
```

### Part 5: Practice Exercises

**Exercise 1: Single Pose Variation**
```
Generate the same character in all 4 poses separately:
1. Generate front view
2. Generate back view
3. Generate side view
4. Generate quarter view

Compare with generate_all_poses
```

**Exercise 2: Multiple Characters**
```
Create character sheets for:
1. Warrior (heavy armor)
2. Mage (robes)
3. Rogue (light leather)
```

**Exercise 3: Style Comparison**
```
Generate same character sheet with different styles:
1. Fantasy art style
2. Realistic style
3. Anime style
```

### Key Takeaways

✓ Use specific poses for targeted views
✓ Generate all poses for complete character sheets
✓ Each pose serves different purposes
✓ Automate with scripts for efficiency

**Continue to Tutorial 5 for batch generation!**

---

## Tutorial 5: Batch Avatar Generation

**Time:** 30 minutes
**Level:** Intermediate
**Prerequisites:** Tutorials 1-4 completed

### What You'll Learn
- Generate multiple avatars efficiently
- Process prompts from files
- Use parallel processing
- Manage batch operations

### Part 1: Sequential Batch Generation

**5.1 Create prompt list**
```python
# batch_sequential.py
import requests
import time

prompts = [
    "warrior character, blue armor, sword",
    "mage character, purple robes, staff",
    "rogue character, leather armor, daggers",
    "paladin character, golden armor, holy symbol",
    "ranger character, green cloak, bow"
]

def generate_avatar(prompt):
    """Generate single avatar."""
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate/avatar',
        json={"prompt": prompt, "realism": False}
    )
    generation_id = response.json()['generation_id']

    # Wait for completion
    while True:
        status = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        ).json()

        if status['status'] in ['completed', 'failed']:
            return status

        time.sleep(2)

# Generate all sequentially
print(f"Generating {len(prompts)} avatars...")
for i, prompt in enumerate(prompts, 1):
    print(f"\n[{i}/{len(prompts)}] {prompt[:40]}...")
    result = generate_avatar(prompt)

    if result['status'] == 'completed':
        print(f"   ✓ Complete")
    else:
        print(f"   ✗ Failed: {result.get('error')}")

print("\n✅ All generations complete!")
```

**5.2 Run sequential batch**
```bash
python batch_sequential.py

# Takes: ~5 minutes for 5 avatars
```

### Part 2: Parallel Batch Generation

**5.3 Use concurrent processing**

```python
# batch_parallel.py
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

prompts = [
    "warrior character, blue armor",
    "mage character, purple robes",
    "rogue character, leather armor",
    "paladin character, golden armor",
    "ranger character, green cloak"
]

def generate_one(prompt, index):
    """Generate single avatar with polling."""
    print(f"[{index}] Starting: {prompt[:40]}...")

    # Start generation
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate/avatar',
        json={"prompt": prompt, "realism": False}
    )
    generation_id = response.json()['generation_id']

    # Poll for completion
    while True:
        status = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        ).json()

        if status['status'] == 'completed':
            print(f"[{index}] ✓ Complete")
            return {'index': index, 'prompt': prompt, 'status': 'completed', 'data': status}
        elif status['status'] == 'failed':
            print(f"[{index}] ✗ Failed")
            return {'index': index, 'prompt': prompt, 'status': 'failed'}

        time.sleep(2)

# Generate in parallel (max 3 at once)
print(f"Generating {len(prompts)} avatars in parallel...\n")

results = []
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(generate_one, prompt, i): (i, prompt)
        for i, prompt in enumerate(prompts, 1)
    }

    for future in as_completed(futures):
        result = future.result()
        results.append(result)

# Summary
completed = [r for r in results if r['status'] == 'completed']
print(f"\n✅ Completed {len(completed)}/{len(prompts)} generations")
```

**5.4 Run parallel batch**
```bash
python batch_parallel.py

# Takes: ~2 minutes for 5 avatars (faster!)
```

### Part 3: Load Prompts from File

**5.5 Create prompts file**
```bash
# prompts.txt
warrior character, blue armor, sword and shield
mage character, purple robes, magical staff
rogue character, dark leather, twin daggers
paladin character, shining golden armor, holy aura
ranger character, forest green cloak, longbow
druid character, natural robes, wooden staff
cleric character, white robes, divine symbol
monk character, simple robes, fighting stance
```

**5.6 Load and process**
```python
# batch_from_file.py
import requests
import time
from pathlib import Path

def load_prompts(file_path):
    """Load prompts from text file."""
    with open(file_path) as f:
        prompts = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith('#')
        ]
    return prompts

def generate_batch(prompts_file, output_dir='batch_output'):
    """Generate avatars from file and download results."""
    prompts = load_prompts(prompts_file)
    print(f"📝 Loaded {len(prompts)} prompts from {prompts_file}\n")

    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {prompt[:50]}...")

        # Generate
        response = requests.post(
            'http://localhost:8000/avatarforge-controller/generate/avatar',
            json={"prompt": prompt, "realism": False}
        )
        generation_id = response.json()['generation_id']

        # Wait for completion
        while True:
            status = requests.get(
                f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
            ).json()

            if status['status'] == 'completed':
                results.append((i, prompt, status))
                print(f"   ✓ Complete")
                break
            elif status['status'] == 'failed':
                print(f"   ✗ Failed")
                break

            time.sleep(2)

    # Download all
    Path(output_dir).mkdir(exist_ok=True)
    print(f"\n📥 Downloading {len(results)} images to {output_dir}/")

    for index, prompt, status in results:
        if status['output_files']:
            output_url = status['output_files'][0]['url']
            filename = f"{index:03d}_{generation_id[:8]}.png"

            url = f"http://localhost:8000{output_url}"
            response = requests.get(url)

            with open(f"{output_dir}/{filename}", 'wb') as f:
                f.write(response.content)

            print(f"   ✓ {filename}")

    print(f"\n✅ Batch complete: {len(results)} avatars in {output_dir}/")

# Usage
if __name__ == '__main__':
    generate_batch('prompts.txt')
```

**5.7 Run batch from file**
```bash
python batch_from_file.py

# Creates batch_output/ with all generated images
```

### Part 4: CSV Batch Processing

**5.8 Create CSV with metadata**
```csv
# characters.csv
id,prompt,clothing,style,realism
001,warrior character,blue plate armor,fantasy art,false
002,mage character,purple wizard robes,magical,false
003,rogue character,dark leather armor,stealth,false
004,paladin character,golden holy armor,divine,false
005,ranger character,forest green gear,natural,false
```

**5.9 Process CSV**
```python
# batch_csv.py
import csv
import requests
import time

def process_csv(csv_file):
    """Generate avatars from CSV with metadata."""
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"📊 Processing {len(rows)} rows from CSV\n")

    for row in rows:
        row_id = row['id']
        print(f"[{row_id}] {row['prompt'][:40]}...")

        # Build request
        request_data = {"prompt": row['prompt']}

        if row.get('clothing'):
            request_data['clothing'] = row['clothing']
        if row.get('style'):
            request_data['style'] = row['style']
        if row.get('realism'):
            request_data['realism'] = row['realism'].lower() == 'true'

        # Generate
        response = requests.post(
            'http://localhost:8000/avatarforge-controller/generate/avatar',
            json=request_data
        )
        generation_id = response.json()['generation_id']

        # Wait
        while True:
            status = requests.get(
                f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
            ).json()

            if status['status'] in ['completed', 'failed']:
                print(f"   ✓ {status['status']}")
                break

            time.sleep(2)

    print("\n✅ CSV processing complete!")

# Usage
if __name__ == '__main__':
    process_csv('characters.csv')
```

### Part 5: Progress Tracking

**5.10 Add progress bar**
```python
# batch_with_progress.py
import requests
import time
from tqdm import tqdm

prompts = [
    "warrior character, blue armor",
    "mage character, purple robes",
    "rogue character, leather armor",
    "paladin character, golden armor",
    "ranger character, green cloak"
]

def generate_with_progress(prompts):
    """Generate with progress bar."""
    results = []

    # Progress bar for all prompts
    with tqdm(total=len(prompts), desc="Generating") as pbar:
        for prompt in prompts:
            # Start generation
            response = requests.post(
                'http://localhost:8000/avatarforge-controller/generate/avatar',
                json={"prompt": prompt, "realism": False}
            )
            generation_id = response.json()['generation_id']

            # Poll with sub-progress
            while True:
                status = requests.get(
                    f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
                ).json()

                if status['status'] in ['completed', 'failed']:
                    results.append(status)
                    pbar.update(1)
                    break

                time.sleep(2)

    completed = [r for r in results if r['status'] == 'completed']
    print(f"\n✅ Completed {len(completed)}/{len(prompts)}")

# Usage
generate_with_progress(prompts)
```

### Part 6: Error Handling

**5.11 Robust batch processing**
```python
# batch_robust.py
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_with_retry(prompt, max_retries=3):
    """Generate with automatic retries."""
    for attempt in range(max_retries):
        try:
            # Start generation
            response = requests.post(
                'http://localhost:8000/avatarforge-controller/generate/avatar',
                json={"prompt": prompt, "realism": False},
                timeout=30
            )
            response.raise_for_status()
            generation_id = response.json()['generation_id']

            # Wait for completion
            timeout = time.time() + 300  # 5 minutes
            while time.time() < timeout:
                status = requests.get(
                    f'http://localhost:8000/avatarforge-controller/generations/{generation_id}',
                    timeout=10
                ).json()

                if status['status'] == 'completed':
                    return {'success': True, 'data': status}
                elif status['status'] == 'failed':
                    raise Exception(f"Generation failed: {status.get('error')}")

                time.sleep(2)

            raise Exception("Timeout waiting for generation")

        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return {'success': False, 'error': str(e)}
            time.sleep(5)  # Wait before retry

# Usage
prompts = ["warrior", "mage", "rogue"]
for prompt in prompts:
    result = generate_with_retry(prompt)
    if result['success']:
        print(f"✓ {prompt}")
    else:
        print(f"✗ {prompt}: {result['error']}")
```

### Key Takeaways

✓ Use parallel processing for faster batches
✓ Load prompts from files for large batches
✓ Add progress tracking for user feedback
✓ Implement error handling and retries
✓ Organize outputs with meaningful names

**Continue to Tutorial 6 for character sheets!**

---

## Tutorial 6: Creating Character Sheets

**Time:** 30 minutes
**Level:** Intermediate
**Prerequisites:** Tutorials 1-5 completed

### What You'll Learn
- Generate complete character sheets
- Organize multi-view outputs
- Create consistent characters across views
- Build an automated character sheet generator
- Export character sheets for different uses

### Part 1: Understanding Character Sheets

**6.1 What is a character sheet?**
```
A character sheet contains multiple views of the same character:
- Front view
- Back view
- Side view (profile)
- Quarter view (3/4 angle)

Used for:
✓ Game development (3D modeling reference)
✓ Animation (turnaround sheets)
✓ Character design portfolios
✓ Consistent character reference
```

**6.2 Character sheet best practices**
```
✓ Use same prompt for all views
✓ Keep clothing/appearance consistent
✓ Use descriptive, detailed prompts
✓ Organize outputs in dedicated folders
✓ Name files clearly (front.png, back.png, etc.)
```

### Part 2: Manual Character Sheet Creation

**6.3 Generate each view separately**

```python
# manual_character_sheet.py
import requests
import time
import os

def generate_single_pose(prompt, pose_type, output_dir):
    """Generate a single pose view."""
    print(f"Generating {pose_type} view...")

    # Generate specific pose
    response = requests.post(
        f'http://localhost:8000/avatarforge-controller/generate_pose?pose={pose_type}',
        json={"prompt": prompt, "realism": False}
    )

    generation_id = response.json()['generation_id']

    # Wait for completion
    while True:
        status = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        ).json()

        if status['status'] == 'completed':
            # Download
            output_url = status['output_files'][0]['url']
            filename = f"{pose_type}.png"
            filepath = os.path.join(output_dir, filename)

            url = f"http://localhost:8000{output_url}"
            response = requests.get(url)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"   ✓ {filename}")
            return filepath

        elif status['status'] == 'failed':
            print(f"   ✗ Failed: {status.get('error')}")
            return None

        time.sleep(2)

def create_manual_character_sheet(prompt, character_name):
    """Create character sheet manually (one view at a time)."""
    output_dir = f"character_sheets/{character_name}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎨 Creating character sheet: {character_name}\n")

    poses = ['front', 'back', 'side', 'quarter']
    files = {}

    for pose in poses:
        filepath = generate_single_pose(prompt, pose, output_dir)
        if filepath:
            files[pose] = filepath

    print(f"\n✅ Character sheet complete!")
    print(f"   Location: {output_dir}/")
    print(f"   Files: {len(files)}/4")

    return files

# Usage
if __name__ == '__main__':
    prompt = "female warrior character, blue plate armor, long white hair, determined expression"
    create_manual_character_sheet(prompt, "blue_warrior")
```

**6.4 Run manual generation**
```bash
python manual_character_sheet.py

# Creates:
# character_sheets/blue_warrior/
#   front.png
#   back.png
#   side.png
#   quarter.png
```

### Part 3: Automated Character Sheet (All Poses at Once)

**6.5 Use generate_all_poses endpoint**

```python
# auto_character_sheet.py
import requests
import time
import os
from pathlib import Path

def create_character_sheet(prompt, character_name, clothing=None, style=None):
    """Create complete character sheet automatically."""
    print(f"🎨 Creating character sheet: {character_name}")
    print(f"   Prompt: {prompt}\n")

    # Build request
    request_data = {"prompt": prompt, "realism": False}
    if clothing:
        request_data['clothing'] = clothing
    if style:
        request_data['style'] = style

    # Generate all poses at once
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate_all_poses',
        json=request_data
    )

    generation_id = response.json()['generation_id']
    print(f"✓ Started: {generation_id}\n")

    # Wait for completion with progress
    print("⏳ Generating", end="")
    start_time = time.time()

    while True:
        status = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        ).json()

        if status['status'] == 'completed':
            elapsed = time.time() - start_time
            print(f"\n\n✅ Complete in {elapsed:.1f}s!\n")
            break
        elif status['status'] == 'failed':
            print(f"\n\n✗ Failed: {status.get('error')}")
            return None

        print(".", end="", flush=True)
        time.sleep(3)

    # Download all files
    output_dir = f"character_sheets/{character_name}"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"📥 Downloading to {output_dir}/")
    files = {}

    for output in status['output_files']:
        pose_type = output.get('pose_type', 'output')
        filename = f"{pose_type}.png"
        filepath = os.path.join(output_dir, filename)

        url = f"http://localhost:8000{output['url']}"
        response = requests.get(url)

        with open(filepath, 'wb') as f:
            f.write(response.content)

        files[pose_type] = filepath
        size_mb = len(response.content) / 1024 / 1024
        print(f"   ✓ {filename} ({size_mb:.1f} MB)")

    print(f"\n✅ Character sheet ready!")
    print(f"   Location: {output_dir}/")

    return files

# Usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python auto_character_sheet.py <name> '<prompt>'")
        print("Example: python auto_character_sheet.py warrior 'warrior character, blue armor'")
        sys.exit(1)

    name = sys.argv[1]
    prompt = sys.argv[2]

    create_character_sheet(prompt, name)
```

**6.6 Use the automated script**
```bash
# Simple
python auto_character_sheet.py warrior "warrior character, blue armor"

# With detailed prompt
python auto_character_sheet.py mage "female mage character, purple robes, long black hair, wise expression"

# Creates organized folders:
# character_sheets/warrior/
# character_sheets/mage/
```

### Part 4: Batch Character Sheet Creation

**6.7 Create multiple character sheets**

```python
# batch_character_sheets.py
import requests
import time
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def create_one_sheet(character_data):
    """Create single character sheet."""
    name = character_data['name']
    prompt = character_data['prompt']
    clothing = character_data.get('clothing')

    print(f"\n[{name}] Starting...")

    # Build request
    request_data = {"prompt": prompt, "realism": False}
    if clothing:
        request_data['clothing'] = clothing

    # Generate
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate_all_poses',
        json=request_data
    )
    generation_id = response.json()['generation_id']

    # Wait
    while True:
        status = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        ).json()

        if status['status'] in ['completed', 'failed']:
            break
        time.sleep(3)

    if status['status'] == 'failed':
        print(f"[{name}] ✗ Failed")
        return None

    # Download
    output_dir = f"character_sheets/{name}"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for output in status['output_files']:
        pose = output.get('pose_type', 'output')
        filename = f"{pose}.png"
        filepath = os.path.join(output_dir, filename)

        url = f"http://localhost:8000{output['url']}"
        response = requests.get(url)

        with open(filepath, 'wb') as f:
            f.write(response.content)

    print(f"[{name}] ✓ Complete ({len(status['output_files'])} poses)")
    return output_dir

def create_batch_sheets(characters, max_workers=2):
    """Create multiple character sheets in parallel."""
    print(f"🎨 Creating {len(characters)} character sheets\n")

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(create_one_sheet, char): char
            for char in characters
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    print(f"\n✅ Completed {len(results)}/{len(characters)} character sheets")
    return results

# Usage
if __name__ == '__main__':
    # Define your party/characters
    party = [
        {
            'name': 'warrior',
            'prompt': 'male warrior character, blue armor, sword and shield',
            'clothing': 'heavy plate armor with blue and silver colors'
        },
        {
            'name': 'mage',
            'prompt': 'female mage character, purple robes, staff',
            'clothing': 'flowing wizard robes with mystical symbols'
        },
        {
            'name': 'rogue',
            'prompt': 'male rogue character, dark leather, daggers',
            'clothing': 'black leather armor, hooded cloak'
        },
        {
            'name': 'cleric',
            'prompt': 'female cleric character, white robes, holy symbol',
            'clothing': 'white and gold priestly vestments'
        }
    ]

    create_batch_sheets(party, max_workers=2)
```

**6.8 Run batch creation**
```bash
python batch_character_sheets.py

# Creates complete sheets for entire party
# character_sheets/warrior/
# character_sheets/mage/
# character_sheets/rogue/
# character_sheets/cleric/
```

### Part 5: Character Sheet Organization

**6.9 Organized file structure**

```bash
# Good structure
character_sheets/
├── blue_warrior/
│   ├── front.png
│   ├── back.png
│   ├── side.png
│   ├── quarter.png
│   └── info.txt          # Character metadata
├── purple_mage/
│   ├── front.png
│   ├── back.png
│   ├── side.png
│   ├── quarter.png
│   └── info.txt
└── party_complete/        # Combined sheets
    └── all_characters.png
```

**6.10 Create metadata file**

```python
# add_metadata.py
import json
import os

def save_character_info(name, prompt, clothing, style, output_dir):
    """Save character metadata."""
    info = {
        "name": name,
        "prompt": prompt,
        "clothing": clothing or "Not specified",
        "style": style or "fantasy art",
        "poses": ["front", "back", "side", "quarter"],
        "created": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save as JSON
    json_path = os.path.join(output_dir, "info.json")
    with open(json_path, 'w') as f:
        json.dump(info, f, indent=2)

    # Save as text
    txt_path = os.path.join(output_dir, "info.txt")
    with open(txt_path, 'w') as f:
        f.write(f"Character: {name}\n")
        f.write(f"Prompt: {prompt}\n")
        f.write(f"Clothing: {info['clothing']}\n")
        f.write(f"Style: {info['style']}\n")
        f.write(f"Created: {info['created']}\n")
        f.write(f"\nPoses included:\n")
        for pose in info['poses']:
            f.write(f"  - {pose}.png\n")

    print(f"   ✓ Saved metadata")
```

### Part 6: Advanced Character Sheet Features

**6.11 Create contact sheet (all views in one image)**

```python
# create_contact_sheet.py
from PIL import Image
import os

def create_contact_sheet(character_dir, output_filename="contact_sheet.png"):
    """Combine all pose views into one image."""
    poses = ['front', 'back', 'side', 'quarter']
    images = []

    # Load all images
    for pose in poses:
        img_path = os.path.join(character_dir, f"{pose}.png")
        if os.path.exists(img_path):
            images.append(Image.open(img_path))

    if not images:
        print("No images found")
        return None

    # Calculate dimensions (2x2 grid)
    width = images[0].width * 2
    height = images[0].height * 2

    # Create contact sheet
    contact = Image.new('RGB', (width, height), 'white')

    # Paste images
    positions = [
        (0, 0),                    # front (top-left)
        (images[0].width, 0),      # back (top-right)
        (0, images[0].height),     # side (bottom-left)
        (images[0].width, images[0].height)  # quarter (bottom-right)
    ]

    for img, pos in zip(images, positions):
        contact.paste(img, pos)

    # Save
    output_path = os.path.join(character_dir, output_filename)
    contact.save(output_path, quality=95)

    print(f"✓ Contact sheet saved: {output_filename}")
    return output_path

# Usage
create_contact_sheet("character_sheets/warrior")
```

**6.12 Add labels to contact sheet**

```python
# labeled_contact_sheet.py
from PIL import Image, ImageDraw, ImageFont
import os

def create_labeled_sheet(character_dir, character_name):
    """Create contact sheet with labels."""
    poses = ['front', 'back', 'side', 'quarter']
    images = []

    # Load images
    for pose in poses:
        img_path = os.path.join(character_dir, f"{pose}.png")
        if os.path.exists(img_path):
            images.append(Image.open(img_path))

    # Create larger canvas for labels
    img_width = images[0].width
    img_height = images[0].height
    label_height = 40

    # Grid size
    grid_width = img_width * 2
    grid_height = (img_height + label_height) * 2

    # Create sheet
    sheet = Image.new('RGB', (grid_width, grid_height), 'white')
    draw = ImageDraw.Draw(sheet)

    # Try to use a font (fallback to default)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Positions and labels
    layout = [
        ((0, 0), 'FRONT'),
        ((img_width, 0), 'BACK'),
        ((0, img_height + label_height), 'SIDE'),
        ((img_width, img_height + label_height), '3/4 VIEW')
    ]

    # Paste images with labels
    for i, (img, (pos, label)) in enumerate(zip(images, layout)):
        x, y = pos

        # Draw label
        label_y = y if i < 2 else y - label_height
        draw.text((x + 10, label_y + 10), label, fill='black', font=font)

        # Paste image below label
        img_y = y + label_height if i < 2 else y
        sheet.paste(img, (x, img_y))

    # Add title
    title = f"{character_name.upper()} - CHARACTER SHEET"
    title_width = draw.textlength(title, font=font) if hasattr(draw, 'textlength') else len(title) * 12
    title_x = (grid_width - title_width) // 2
    draw.text((title_x, grid_height - label_height + 10), title, fill='black', font=font)

    # Save
    output_path = os.path.join(character_dir, "character_sheet.png")
    sheet.save(output_path, quality=95)

    print(f"✓ Labeled sheet saved: {output_path}")
    return output_path

# Usage
create_labeled_sheet("character_sheets/warrior", "Blue Warrior")
```

### Part 7: Export for Different Uses

**6.13 Export for game development**

```python
# export_for_game.py
import os
import shutil
from pathlib import Path

def export_for_unity(character_dir, game_name):
    """
    Export character sheet in Unity-friendly format.

    Structure:
    game_assets/<game_name>/Characters/<character>/
        Textures/
            character_front.png
            character_back.png
            character_side.png
            character_quarter.png
    """
    character_name = os.path.basename(character_dir)
    export_dir = f"game_assets/{game_name}/Characters/{character_name}/Textures"
    Path(export_dir).mkdir(parents=True, exist_ok=True)

    poses = ['front', 'back', 'side', 'quarter']

    for pose in poses:
        src = os.path.join(character_dir, f"{pose}.png")
        if os.path.exists(src):
            dst = os.path.join(export_dir, f"{character_name}_{pose}.png")
            shutil.copy2(src, dst)
            print(f"✓ Exported: {character_name}_{pose}.png")

    print(f"\n✅ Exported for Unity")
    print(f"   Location: {export_dir}/")

# Usage
export_for_unity("character_sheets/warrior", "MyRPG")
```

**6.14 Export for portfolio**

```python
# export_for_portfolio.py
import os
import shutil
from PIL import Image

def export_for_portfolio(character_dir, portfolio_dir="portfolio"):
    """Export high-quality character sheet for portfolio."""
    character_name = os.path.basename(character_dir)
    output_dir = os.path.join(portfolio_dir, character_name)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Create contact sheet
    create_labeled_sheet(character_dir, character_name)

    # Copy contact sheet
    contact_src = os.path.join(character_dir, "character_sheet.png")
    contact_dst = os.path.join(output_dir, f"{character_name}_sheet.png")

    if os.path.exists(contact_src):
        shutil.copy2(contact_src, contact_dst)
        print(f"✓ Portfolio sheet: {character_name}_sheet.png")

    # Copy individual high-res views
    for pose in ['front', 'back', 'side', 'quarter']:
        src = os.path.join(character_dir, f"{pose}.png")
        if os.path.exists(src):
            dst = os.path.join(output_dir, f"{character_name}_{pose}.png")
            shutil.copy2(src, dst)

    # Create README
    readme_path = os.path.join(output_dir, "README.txt")
    with open(readme_path, 'w') as f:
        f.write(f"Character: {character_name}\n")
        f.write(f"Package includes:\n")
        f.write(f"  - Full character sheet (2x2 grid)\n")
        f.write(f"  - Individual pose views\n")
        f.write(f"  - All views at original resolution\n")

    print(f"\n✅ Portfolio package ready: {output_dir}/")

# Usage
export_for_portfolio("character_sheets/warrior")
```

### Practice Exercises

**Exercise 1: Create Your First Character Sheet**
```
1. Design a character (warrior, mage, etc.)
2. Write detailed prompt
3. Generate complete character sheet
4. Organize files properly
```

**Exercise 2: Create a Party**
```
Create character sheets for a 4-person party:
- Tank (warrior/paladin)
- DPS (rogue/ranger)
- Healer (cleric)
- Mage

Use batch processing for efficiency
```

**Exercise 3: Export Pipeline**
```
Create full export pipeline:
1. Generate character sheet
2. Create contact sheet
3. Add labels
4. Export for game/portfolio
5. Organize with metadata
```

### Key Takeaways

✓ Use generate_all_poses for complete sheets
✓ Organize outputs in character-specific folders
✓ Create contact sheets for easy viewing
✓ Add metadata for reference
✓ Export in formats for different uses
✓ Automate the entire pipeline

**Continue to Tutorial 7 for smart file management!**

---

## Tutorial 7: Smart File Management

**Time:** 25 minutes
**Level:** Intermediate
**Prerequisites:** Tutorials 1-6 completed

### What You'll Learn
- Avoid duplicate uploads with hash checking
- Track and manage uploaded files
- Implement efficient file reuse
- Clean up unused files
- Optimize storage usage

### Part 1: Understanding File Deduplication

**7.1 How deduplication works**
```
1. File uploaded → API calculates SHA256 hash
2. Hash checked against database
3. If hash exists → Return existing file_id
4. If hash new → Store file and create new file_id

Benefits:
✓ Saves storage space
✓ Faster "uploads" (file already exists)
✓ Consistent file_ids for same content
✓ Automatic reference counting
```

**7.2 Hash calculation**
```python
import hashlib

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        # Read file in chunks (memory efficient)
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()

# Usage
file_hash = calculate_file_hash('pose.png')
print(f"Hash: {file_hash}")
```

### Part 2: Smart Upload (Check Before Upload)

**7.3 Basic smart upload**

```python
# smart_upload.py
import hashlib
import requests

def smart_upload(file_path, upload_type='pose'):
    """Upload only if file doesn't already exist."""

    # Calculate hash
    print(f"Checking file: {file_path}")
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    print(f"   Hash: {file_hash[:16]}...")

    # Check if exists
    check_response = requests.get(
        f'http://localhost:8000/avatarforge-controller/files/hash/{file_hash}'
    )
    check_data = check_response.json()

    if check_data['exists']:
        print(f"   ✓ Already exists: {check_data['file_id']}")
        print(f"   ⚡ Saved upload time!")
        return check_data['file_id']

    # Upload new file
    print(f"   ⬆ Uploading new file...")

    endpoint = (
        'upload/pose_image' if upload_type == 'pose'
        else 'upload/reference_image'
    )

    with open(file_path, 'rb') as f:
        upload_response = requests.post(
            f'http://localhost:8000/avatarforge-controller/{endpoint}',
            files={'file': f}
        )

    upload_data = upload_response.json()
    print(f"   ✓ Uploaded: {upload_data['file_id']}")

    return upload_data['file_id']

# Usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python smart_upload.py <file>")
        sys.exit(1)

    file_id = smart_upload(sys.argv[1])
    print(f"\nFile ID: {file_id}")
```

**7.4 Use smart upload**
```bash
# First time - uploads
python smart_upload.py pose1.png

# Second time - reuses
python smart_upload.py pose1.png  # Instant!
```

### Part 3: File Tracking System

**7.5 Create file tracker**

```python
# file_tracker.py
import json
import os
import hashlib
import requests
from datetime import datetime

class FileTracker:
    """Track uploaded files to avoid duplicates."""

    def __init__(self, cache_file='file_cache.json'):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self):
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file) as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def _calculate_hash(self, file_path):
        """Calculate file hash."""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def upload_smart(self, file_path, upload_type='pose', tags=None):
        """Upload with caching and tracking."""
        abs_path = os.path.abspath(file_path)

        # Check local cache first
        file_hash = self._calculate_hash(abs_path)

        if file_hash in self.cache:
            cached = self.cache[file_hash]
            print(f"✓ Found in cache: {cached['file_id']}")
            print(f"  Originally uploaded: {cached['uploaded_at']}")
            return cached['file_id']

        # Check server
        check_response = requests.get(
            f'http://localhost:8000/avatarforge-controller/files/hash/{file_hash}'
        )
        check_data = check_response.json()

        if check_data['exists']:
            file_id = check_data['file_id']
            print(f"✓ Found on server: {file_id}")

            # Add to cache
            self.cache[file_hash] = {
                'file_id': file_id,
                'file_path': abs_path,
                'file_name': os.path.basename(abs_path),
                'type': upload_type,
                'tags': tags or [],
                'uploaded_at': datetime.now().isoformat(),
                'hash': file_hash
            }
            self._save_cache()

            return file_id

        # Upload new file
        print(f"⬆ Uploading: {os.path.basename(abs_path)}")

        endpoint = (
            'upload/pose_image' if upload_type == 'pose'
            else 'upload/reference_image'
        )

        with open(abs_path, 'rb') as f:
            upload_response = requests.post(
                f'http://localhost:8000/avatarforge-controller/{endpoint}',
                files={'file': f}
            )

        upload_data = upload_response.json()
        file_id = upload_data['file_id']

        # Cache it
        self.cache[file_hash] = {
            'file_id': file_id,
            'file_path': abs_path,
            'file_name': os.path.basename(abs_path),
            'type': upload_type,
            'tags': tags or [],
            'uploaded_at': datetime.now().isoformat(),
            'hash': file_hash,
            'size': upload_data['size'],
            'mime_type': upload_data['mime_type']
        }
        self._save_cache()

        print(f"✓ Uploaded: {file_id}")
        return file_id

    def list_cached(self, type_filter=None):
        """List all cached files."""
        print("\nCached Files:")
        print("=" * 70)

        for file_hash, data in self.cache.items():
            if type_filter and data['type'] != type_filter:
                continue

            print(f"\nFile: {data['file_name']}")
            print(f"  ID: {data['file_id']}")
            print(f"  Type: {data['type']}")
            print(f"  Path: {data['file_path']}")
            print(f"  Hash: {file_hash[:16]}...")
            print(f"  Uploaded: {data['uploaded_at']}")

            if data.get('tags'):
                print(f"  Tags: {', '.join(data['tags'])}")

    def find_by_tags(self, tags):
        """Find files by tags."""
        results = []

        for file_hash, data in self.cache.items():
            file_tags = set(data.get('tags', []))
            if set(tags).intersection(file_tags):
                results.append(data)

        return results

    def clear_cache(self):
        """Clear the cache."""
        self.cache = {}
        self._save_cache()
        print("✓ Cache cleared")

# Usage
if __name__ == '__main__':
    tracker = FileTracker()

    # Upload with tags
    file_id1 = tracker.upload_smart('warrior_pose.png', tags=['warrior', 'pose', 'combat'])
    file_id2 = tracker.upload_smart('mage_pose.png', tags=['mage', 'pose', 'casting'])

    # List all
    tracker.list_cached()

    # Find by tags
    combat_files = tracker.find_by_tags(['combat'])
    print(f"\nFound {len(combat_files)} combat-related files")
```

**7.6 Use file tracker**
```bash
python file_tracker.py

# Creates file_cache.json with all uploads
# Reuses file_ids automatically
```

### Part 4: Batch Upload with Deduplication

**7.7 Smart batch upload**

```python
# batch_upload_smart.py
import os
import hashlib
import requests
from pathlib import Path

def find_duplicate_files(directory):
    """Find local duplicates before uploading."""
    file_hashes = {}
    duplicates = []

    print(f"Scanning {directory} for duplicates...")

    # Find all images
    image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    image_files = []

    for ext in image_extensions:
        image_files.extend(Path(directory).rglob(f'*{ext}'))

    # Calculate hashes
    for file_path in image_files:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        if file_hash in file_hashes:
            duplicates.append({
                'original': file_hashes[file_hash],
                'duplicate': str(file_path)
            })
        else:
            file_hashes[file_hash] = str(file_path)

    print(f"Found {len(file_hashes)} unique files")
    print(f"Found {len(duplicates)} local duplicates")

    return file_hashes, duplicates

def batch_upload_unique(directory, upload_type='pose'):
    """Upload only unique files from directory."""
    unique_files, duplicates = find_duplicate_files(directory)

    # Report duplicates
    if duplicates:
        print("\nLocal duplicates found:")
        for dup in duplicates:
            print(f"  {dup['duplicate']}")
            print(f"    → Same as {dup['original']}")

    # Upload unique files
    print(f"\n⬆ Uploading {len(unique_files)} unique files...\n")

    uploaded = {}
    skipped = 0

    for file_hash, file_path in unique_files.items():
        # Check server
        check_response = requests.get(
            f'http://localhost:8000/avatarforge-controller/files/hash/{file_hash}'
        )

        if check_response.json().get('exists'):
            file_id = check_response.json()['file_id']
            print(f"⚡ {os.path.basename(file_path)}: already on server")
            uploaded[file_path] = file_id
            skipped += 1
            continue

        # Upload
        endpoint = (
            'upload/pose_image' if upload_type == 'pose'
            else 'upload/reference_image'
        )

        with open(file_path, 'rb') as f:
            upload_response = requests.post(
                f'http://localhost:8000/avatarforge-controller/{endpoint}',
                files={'file': f}
            )

        file_id = upload_response.json()['file_id']
        print(f"✓ {os.path.basename(file_path)}: {file_id}")
        uploaded[file_path] = file_id

    print(f"\n✅ Upload complete:")
    print(f"   Total unique: {len(unique_files)}")
    print(f"   Actually uploaded: {len(uploaded) - skipped}")
    print(f"   Skipped (on server): {skipped}")
    print(f"   Local duplicates avoided: {len(duplicates)}")

    return uploaded

# Usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python batch_upload_smart.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    batch_upload_unique(directory)
```

**7.8 Use smart batch upload**
```bash
python batch_upload_smart.py ./my_poses/

# Finds duplicates locally
# Checks server before uploading
# Only uploads truly new files
```

### Part 5: File Cleanup

**7.9 Clean up unused files**

```python
# cleanup_files.py
import requests
from datetime import datetime, timedelta

def list_all_files():
    """List all uploaded files."""
    # Note: This would need a list files endpoint
    # For now, we'll track via generations

    response = requests.get(
        'http://localhost:8000/avatarforge-controller/generations?limit=1000'
    )

    all_gens = response.json()['generations']

    # Collect file IDs
    file_ids = set()

    for gen in all_gens:
        if gen.get('pose_file_id'):
            file_ids.add(gen['pose_file_id'])
        if gen.get('reference_file_id'):
            file_ids.add(gen['reference_file_id'])

    return file_ids

def delete_unused_files(dry_run=True):
    """Delete files not referenced by any generation."""
    print("🗑️ Cleanup mode:", "DRY RUN" if dry_run else "LIVE")

    # This is a conceptual example
    # Actual implementation depends on API having list_files endpoint

    print("\nNote: Server handles automatic cleanup via reference counting")
    print("Files are automatically cleaned when:")
    print("  - Reference count reaches 0")
    print("  - File marked as deleted")
    print("  - Cleanup job runs (scheduled)")

# Usage
if __name__ == '__main__':
    delete_unused_files(dry_run=True)
```

### Part 6: Storage Optimization

**7.10 Storage usage report**

```python
# storage_report.py
import os
import requests

def analyze_storage():
    """Analyze storage usage."""
    print("📊 Storage Analysis\n")

    # Get all generations
    response = requests.get(
        'http://localhost:8000/avatarforge-controller/generations?limit=1000'
    )

    generations = response.json()['generations']

    total_outputs = 0
    total_size_estimate = 0

    for gen in generations:
        if gen.get('output_files'):
            for output in gen['output_files']:
                total_outputs += 1
                # Estimate 2MB per output (adjust based on your settings)
                total_size_estimate += 2

    print(f"Generations: {len(generations)}")
    print(f"Output files: {total_outputs}")
    print(f"Estimated size: {total_size_estimate} MB ({total_size_estimate/1024:.1f} GB)")

    # Check actual storage directory
    storage_path = './storage'
    if os.path.exists(storage_path):
        total_size = 0
        file_count = 0

        for dirpath, dirnames, filenames in os.walk(storage_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
                file_count += 1

        print(f"\nActual storage:")
        print(f"  Files: {file_count}")
        print(f"  Size: {total_size/1024/1024:.1f} MB ({total_size/1024/1024/1024:.2f} GB)")

# Usage
analyze_storage()
```

### Part 7: Best Practices

**7.11 File management checklist**

```python
# best_practices.py

"""
File Management Best Practices:

1. ALWAYS use hash checking before upload
   ✓ Use smart_upload() instead of direct upload
   ✓ Saves bandwidth and time
   ✓ Prevents duplicate storage

2. Track your files
   ✓ Use FileTracker for organization
   ✓ Tag files appropriately
   ✓ Keep local cache

3. Organize locally
   ✓ Group by project/character
   ✓ Use meaningful names
   ✓ Keep originals separate from generated

4. Clean up regularly
   ✓ Delete old generations
   ✓ Remove unused references
   ✓ Run cleanup scripts

5. Monitor storage
   ✓ Check usage periodically
   ✓ Archive old projects
   ✓ Optimize file sizes before upload
"""

def good_workflow_example():
    """Example of good file management workflow."""
    tracker = FileTracker()

    # 1. Upload poses for character
    warrior_poses = {
        'standing': tracker.upload_smart('poses/warrior_standing.png',
                                         tags=['warrior', 'standing']),
        'combat': tracker.upload_smart('poses/warrior_combat.png',
                                       tags=['warrior', 'combat'])
    }

    # 2. Upload reference images
    warrior_refs = {
        'armor': tracker.upload_smart('refs/blue_armor.jpg',
                                     upload_type='reference',
                                     tags=['warrior', 'armor', 'blue'])
    }

    # 3. Generate with tracked files
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate/avatar',
        json={
            "prompt": "warrior character, blue armor",
            "pose_file_id": warrior_poses['standing'],
            "reference_file_id": warrior_refs['armor']
        }
    )

    # 4. Track generation
    generation_id = response.json()['generation_id']

    print("✅ Workflow complete!")
    print(f"   Files tracked and reusable")
    print(f"   Generation: {generation_id}")

    return generation_id
```

### Practice Exercises

**Exercise 1: Build Your File Tracker**
```
1. Create FileTracker instance
2. Upload 5 different pose images with tags
3. Try uploading same images again (should skip)
4. List all cached files
5. Find files by specific tags
```

**Exercise 2: Optimize Batch Upload**
```
1. Collect 10-20 pose images in folder
2. Use smart batch upload
3. Check how many were deduplicated
4. Calculate time/bandwidth saved
```

**Exercise 3: Storage Analysis**
```
1. Run storage analysis
2. Identify largest files
3. Find duplicate files
4. Clean up old generations
5. Measure storage reduction
```

### Key Takeaways

✓ Always check hash before uploading
✓ Use caching to avoid redundant API calls
✓ Track files with tags for organization
✓ Batch operations save time
✓ Regular cleanup prevents bloat
✓ Monitor storage usage
✓ Automate file management workflows

**Continue to Tutorial 8 for web interface!**

---

**Last Updated:** 2025-01-15
**Tutorials Completed:** 7/12

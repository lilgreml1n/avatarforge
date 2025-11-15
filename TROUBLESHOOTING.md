# AvatarForge - Complete Troubleshooting Guide

**Every error. Every solution. Every platform. Every scenario.**

This is the most comprehensive troubleshooting guide you'll find. If you encounter an error, the solution is here.

---

## 📋 Table of Contents

1. [Installation & Setup Issues](#installation--setup-issues)
2. [ComfyUI Connection Issues](#comfyui-connection-issues)
3. [File Upload Issues](#file-upload-issues)
4. [Generation Issues](#generation-issues)
5. [Database Issues](#database-issues)
6. [Model Download Issues](#model-download-issues)
7. [API Error Messages](#api-error-messages)
8. [Performance Issues](#performance-issues)
9. [Platform-Specific Issues](#platform-specific-issues)
10. [Network & Firewall Issues](#network--firewall-issues)
11. [Dependency Conflicts](#dependency-conflicts)
12. [Docker Issues](#docker-issues)

---

## Installation & Setup Issues

### Issue 1: "Command 'python' not found"

**Symptoms:**
```bash
bash: python: command not found
```

**Platforms:** Linux, macOS

**Solutions:**

**Solution 1: Use python3**
```bash
# Instead of:
python main.py

# Use:
python3 main.py
```

**Solution 2: Create alias**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias python=python3

# Reload
source ~/.bashrc
```

**Solution 3: Install Python**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS (Homebrew)
brew install python3

# Windows
# Download from python.org
```

**Verification:**
```bash
python3 --version
# Should show: Python 3.10.x or higher
```

---

### Issue 2: "ModuleNotFoundError: No module named 'fastapi'"

**Symptoms:**
```python
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'uvicorn'
ModuleNotFoundError: No module named 'sqlalchemy'
```

**Cause:** Dependencies not installed

**Solutions:**

**Solution 1: Install with pip**
```bash
pip install -r requirements.txt

# Or with python3
python3 -m pip install -r requirements.txt
```

**Solution 2: Use uv (recommended)**
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Or run directly
uv run python main.py
```

**Solution 3: Virtual environment**
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install
pip install -r requirements.txt
```

**Verification:**
```bash
pip list | grep fastapi
# Should show fastapi and version
```

---

### Issue 3: "Permission denied" when installing packages

**Symptoms:**
```bash
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Platforms:** Linux, macOS

**Solutions:**

**Solution 1: Use --user flag**
```bash
pip install --user -r requirements.txt
```

**Solution 2: Use virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 3: Fix permissions (not recommended)**
```bash
# Only if you must
sudo pip install -r requirements.txt
```

---

### Issue 4: Database initialization fails

**Symptoms:**
```bash
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
```

**Cause:** Database directory doesn't exist or no write permissions

**Solutions:**

**Solution 1: Create directory**
```bash
# Check .env for DATABASE_URL
cat .env | grep DATABASE

# If using SQLite, ensure directory exists
mkdir -p $(dirname avatarforge.db)
```

**Solution 2: Fix permissions**
```bash
# Give write permissions to current directory
chmod u+w .

# Or specific database directory
chmod u+w /path/to/database/dir
```

**Solution 3: Change database location**
```bash
# Edit .env
DATABASE_URL=sqlite:///./avatarforge.db

# Or use absolute path
DATABASE_URL=sqlite:////home/user/avatarforge/avatarforge.db
```

**Solution 4: Initialize database manually**
```bash
python3 -m avatarforge.database.init_db
```

**Verification:**
```bash
# Check database file exists
ls -lh avatarforge.db

# Should show file with size > 0
```

---

### Issue 5: ".env file not found" or environment variables not loaded

**Symptoms:**
```
KeyError: 'SECRET_KEY'
Config validation error
```

**Cause:** .env file missing or not loaded

**Solutions:**

**Solution 1: Create .env from example**
```bash
cp .env.example .env

# Edit .env with your values
nano .env  # or vim, code, etc.
```

**Solution 2: Set environment variables manually**
```bash
export SECRET_KEY=your-secret-key-here
export COMFYUI_URL=http://localhost:8188
export DATABASE_URL=sqlite:///./avatarforge.db

# Then run
python main.py
```

**Solution 3: Load .env in code (already done in project)**
```python
# Should be in main.py or config
from dotenv import load_dotenv
load_dotenv()
```

**Verification:**
```bash
# Check .env exists
cat .env

# Should show your configuration
```

---

### Issue 6: Port 8000 already in use

**Symptoms:**
```bash
ERROR: [Errno 48] Address already in use
OSError: [Errno 98] Address already in use
```

**Cause:** Another process using port 8000

**Solutions:**

**Solution 1: Kill process on port**
```bash
# Find process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill it
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

**Solution 2: Use different port**
```bash
# Run on different port
uvicorn main:app --port 8001

# Or edit .env
PORT=8001
```

**Solution 3: Stop previous instance**
```bash
# Find all python processes
ps aux | grep python

# Kill specific one
kill <PID>
```

---

## ComfyUI Connection Issues

### Issue 7: "ComfyUI unavailable" in health check

**Symptoms:**
```json
{
  "api_status": "healthy",
  "comfyui": {
    "status": "unavailable",
    "error": "Connection refused"
  }
}
```

**Cause:** ComfyUI not running or wrong URL

**Solutions:**

**Solution 1: Start ComfyUI**
```bash
# Navigate to ComfyUI directory
cd /path/to/ComfyUI

# Start ComfyUI
python main.py

# Or with specific port
python main.py --port 8188
```

**Solution 2: Check ComfyUI URL**
```bash
# Check .env file
cat .env | grep COMFYUI_URL

# Should be:
COMFYUI_URL=http://localhost:8188

# Test ComfyUI directly
curl http://localhost:8188/system_stats
```

**Solution 3: Verify ComfyUI is accessible**
```bash
# Open in browser
open http://localhost:8188

# Should show ComfyUI interface
```

**Solution 4: Check firewall**
```bash
# Allow port 8188
sudo ufw allow 8188  # Linux
```

**Verification:**
```bash
curl http://localhost:8000/avatarforge-controller/health

# Should show ComfyUI: healthy
```

---

### Issue 8: ComfyUI times out during generation

**Symptoms:**
```
requests.exceptions.Timeout: HTTPSConnectionPool
Generation stuck in 'processing' forever
```

**Cause:** ComfyUI crashed, overloaded, or very slow

**Solutions:**

**Solution 1: Check ComfyUI logs**
```bash
# In ComfyUI terminal, look for errors like:
# - Out of memory
# - CUDA out of memory
# - Model not found
```

**Solution 2: Restart ComfyUI**
```bash
# Stop ComfyUI (Ctrl+C)
# Start again
python main.py
```

**Solution 3: Reduce batch size**
```bash
# If generating multiple, reduce concurrent requests
# Only send 1-2 generations at a time
```

**Solution 4: Increase timeout**
```python
# In your code or .env
COMFYUI_TIMEOUT=600  # 10 minutes
```

**Solution 5: Check GPU memory**
```bash
# NVIDIA
nvidia-smi

# If memory full, reduce image size or restart ComfyUI
```

---

### Issue 9: "Model not found" errors from ComfyUI

**Symptoms:**
```json
{
  "status": "failed",
  "error": "Model not found: v1-5-pruned-emaonly.safetensors"
}
```

**Cause:** Required model files not downloaded

**Solutions:**

**Solution 1: Run model download script**
```bash
# If you have download_models.sh
bash download_models.sh

# Get HuggingFace token first
export HF_TOKEN='your_token_here'
bash download_models.sh
```

**Solution 2: Download models manually**
```bash
# SD 1.5 model
cd /path/to/ComfyUI/models/checkpoints
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
```

**Solution 3: Update workflow to use available models**
```bash
# Check what models you have
ls /path/to/ComfyUI/models/checkpoints/

# Update code to use available model
# In avatarforge/services/workflow_builder.py
```

**Verification:**
```bash
# List all checkpoint models
ls -lh /path/to/ComfyUI/models/checkpoints/

# Should show .safetensors or .ckpt files
```

---

## File Upload Issues

### Issue 10: "File too large" error

**Symptoms:**
```json
{
  "detail": "File size exceeds maximum allowed size"
}
```
**HTTP Status:** 413 Payload Too Large

**Cause:** File exceeds 50MB limit

**Solutions:**

**Solution 1: Resize image before upload**
```python
from PIL import Image

def resize_image(input_path, output_path, max_size=2048):
    img = Image.open(input_path)
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    img.save(output_path, optimize=True, quality=85)

resize_image('huge.png', 'resized.png')
```

**Solution 2: Compress image**
```bash
# Using ImageMagick
convert input.png -quality 85 -resize 2048x2048\> output.png

# Using pngquant
pngquant --quality 80-95 input.png
```

**Solution 3: Change to JPEG (if PNG)**
```python
from PIL import Image

img = Image.open('input.png')
img = img.convert('RGB')
img.save('output.jpg', quality=85, optimize=True)
```

**Solution 4: Increase server limit (not recommended)**
```python
# In .env
MAX_FILE_SIZE=104857600  # 100MB

# Requires server restart
```

**Verification:**
```bash
# Check file size
ls -lh image.png

# Should be under 50MB
```

---

### Issue 11: "Invalid image file" error

**Symptoms:**
```json
{
  "detail": "File is not a valid image"
}
```
**HTTP Status:** 400 Bad Request

**Cause:** File is corrupted or not a supported format

**Solutions:**

**Solution 1: Check file format**
```bash
# Check file type
file image.png

# Should show: PNG image data
```

**Solution 2: Convert to supported format**
```bash
# Supported: PNG, JPG, JPEG, WEBP

# Convert to PNG
convert input.bmp output.png

# Or with Python
from PIL import Image
img = Image.open('input.bmp')
img.save('output.png')
```

**Solution 3: Repair corrupted image**
```bash
# Try opening and re-saving
python3 << EOF
from PIL import Image
img = Image.open('corrupted.png')
img.save('repaired.png')
EOF
```

**Solution 4: Validate image**
```python
from PIL import Image

try:
    img = Image.open('test.png')
    img.verify()
    print("✓ Image is valid")
except Exception as e:
    print(f"✗ Image is invalid: {e}")
```

---

### Issue 12: Upload succeeds but file_id not returned

**Symptoms:**
```json
{
  "detail": "Internal server error"
}
```

**Cause:** Database write failure, storage path issue

**Solutions:**

**Solution 1: Check storage directory**
```bash
# Check .env
cat .env | grep STORAGE_PATH

# Ensure directory exists
mkdir -p ./storage/files
mkdir -p ./storage/outputs
mkdir -p ./storage/temp

# Fix permissions
chmod -R u+w ./storage
```

**Solution 2: Check database**
```bash
# Test database connection
python3 << EOF
from avatarforge.database.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("✓ Database OK")
EOF
```

**Solution 3: Check logs**
```bash
# Run server with debug logging
uvicorn main:app --log-level debug

# Check error messages
```

**Solution 4: Reinitialize database**
```bash
# Backup first!
cp avatarforge.db avatarforge.db.backup

# Reinitialize
python3 -m avatarforge.database.init_db
```

---

### Issue 13: Upload works but file hash check fails

**Symptoms:**
```bash
# Upload returns file_id
# But hash check returns "not found"
```

**Cause:** Hash mismatch, race condition

**Solutions:**

**Solution 1: Wait after upload**
```python
import time

# Upload
result = upload_file('image.png')
file_id = result['file_id']

# Wait for database write
time.sleep(0.5)

# Now check hash
hash_check = check_hash(file_hash)
```

**Solution 2: Use file_id instead of hash**
```python
# Instead of checking hash, just use returned file_id
file_id = upload_result['file_id']

# Use directly in generation
generate_avatar(prompt, pose_file_id=file_id)
```

**Solution 3: Verify hash calculation**
```python
import hashlib

# Calculate same way as server
with open('image.png', 'rb') as f:
    file_hash = hashlib.sha256(f.read()).hexdigest()

print(f"Hash: {file_hash}")
# Compare with upload response
```

---

## Generation Issues

### Issue 14: Generation stuck in "queued" status

**Symptoms:**
```json
{
  "status": "queued",
  "created_at": "2025-01-15T10:00:00Z"
}
```

**Cause:** ComfyUI not picking up jobs

**Solutions:**

**Solution 1: Check ComfyUI queue**
```bash
curl http://localhost:8188/queue

# Should show pending jobs
```

**Solution 2: Restart ComfyUI**
```bash
# Stop ComfyUI
# Start again
cd /path/to/ComfyUI
python main.py
```

**Solution 3: Cancel stuck job**
```bash
# In ComfyUI interface, click "Cancel All"
# Or via API:
curl -X POST http://localhost:8188/interrupt
```

**Solution 4: Check ComfyUI logs**
```bash
# Look for errors in ComfyUI terminal
# Common issues:
# - Model loading failed
# - Out of memory
# - Invalid workflow
```

---

### Issue 15: Generation fails with "out of memory"

**Symptoms:**
```json
{
  "status": "failed",
  "error": "CUDA out of memory"
}
```

**Cause:** Insufficient GPU memory

**Solutions:**

**Solution 1: Reduce image size**
```python
# Instead of 1024x1024
generate_avatar(prompt, width=512, height=512)
```

**Solution 2: Reduce batch size**
```bash
# Don't generate multiple at once
# Wait for each to complete
```

**Solution 3: Free GPU memory**
```bash
# Check GPU usage
nvidia-smi

# Kill other GPU processes
kill -9 <PID>

# Or restart ComfyUI to free memory
```

**Solution 4: Use CPU instead of GPU**
```bash
# In ComfyUI
python main.py --cpu
```

**Solution 5: Enable model offloading**
```bash
# In ComfyUI, use --lowvram or --normalvram flags
python main.py --lowvram
```

---

### Issue 16: Generation completes but no output files

**Symptoms:**
```json
{
  "status": "completed",
  "output_files": []
}
```

**Cause:** ComfyUI didn't save outputs, path mismatch

**Solutions:**

**Solution 1: Check ComfyUI output directory**
```bash
ls /path/to/ComfyUI/output/

# Should show generated images
```

**Solution 2: Check storage path**
```bash
# In .env
cat .env | grep STORAGE_PATH

# Check directory exists
ls -la ./storage/outputs/
```

**Solution 3: Check file permissions**
```bash
# Ensure ComfyUI can write to output dir
chmod -R u+w /path/to/ComfyUI/output/
```

**Solution 4: Check ComfyUI config**
```bash
# In ComfyUI, check output path settings
# Should match expected location
```

---

### Issue 17: "Prompt too long" error

**Symptoms:**
```json
{
  "detail": "Prompt exceeds maximum length"
}
```

**Cause:** Text prompt too long (usually >77 tokens for SD)

**Solutions:**

**Solution 1: Shorten prompt**
```python
# Bad (too long):
prompt = "highly detailed photorealistic portrait of a warrior character with blue armor and intricate gold trim, standing in a dramatic pose with sword raised, cinematic lighting, 8k resolution, unreal engine, trending on artstation"

# Good (concise):
prompt = "warrior character, blue armor, gold trim, dramatic pose, sword raised"
```

**Solution 2: Use negative prompts**
```python
# Move quality terms to settings instead of prompt
generate_avatar(
    prompt="warrior character, blue armor",
    # Quality handled by model/settings
)
```

**Solution 3: Prioritize key terms**
```python
# Focus on what matters most
prompt = "female warrior, blue plate armor, long white hair, determined expression"
```

---

### Issue 18: Weird/bad generation results

**Symptoms:**
- Distorted images
- Wrong subject
- Low quality
- Artifacts

**Cause:** Poor prompt, wrong settings, model issues

**Solutions:**

**Solution 1: Improve prompt**
```python
# Bad:
prompt = "person"

# Good:
prompt = "female warrior character, blue armor, long white hair, confident expression, detailed face"

# Add detail and specificity
```

**Solution 2: Adjust steps**
```python
# Too low (bad quality)
steps = 10

# Good balance
steps = 30

# High quality (slower)
steps = 50
```

**Solution 3: Adjust CFG scale**
```python
# Too low (ignores prompt)
cfg_scale = 3

# Balanced
cfg_scale = 7

# Very strict to prompt
cfg_scale = 12
```

**Solution 4: Try different seed**
```python
# Bad result with seed
generate_avatar(prompt, seed=12345)

# Try different seed
generate_avatar(prompt, seed=67890)

# Or random
generate_avatar(prompt)  # Random seed each time
```

**Solution 5: Check model**
```bash
# Ensure using correct model
# Some models are better for certain styles

# Realistic: RealVisXL, JuggernautXL
# Anime: animagine, anything-v5
```

---

## Database Issues

### Issue 19: "Table doesn't exist" error

**Symptoms:**
```bash
sqlalchemy.exc.OperationalError: no such table: uploaded_files
```

**Cause:** Database not initialized

**Solutions:**

**Solution 1: Initialize database**
```bash
python3 -m avatarforge.database.init_db
```

**Solution 2: Verify database file**
```bash
# Check database exists
ls -lh avatarforge.db

# Should show file > 0 bytes
```

**Solution 3: Check DATABASE_URL**
```bash
cat .env | grep DATABASE_URL

# Should point to correct file
DATABASE_URL=sqlite:///./avatarforge.db
```

**Solution 4: Recreate database**
```bash
# Backup first!
mv avatarforge.db avatarforge.db.old

# Reinitialize
python3 -m avatarforge.database.init_db
```

**Verification:**
```bash
# Check tables exist
sqlite3 avatarforge.db ".tables"

# Should show:
# generations  uploaded_files
```

---

### Issue 20: "Database is locked" error

**Symptoms:**
```bash
sqlite3.OperationalError: database is locked
```

**Cause:** Another process accessing database, or journal file stuck

**Solutions:**

**Solution 1: Close other connections**
```bash
# Stop all instances of the API
killall python3

# Or find and kill specific process
ps aux | grep "main.py"
kill <PID>
```

**Solution 2: Remove lock files**
```bash
# Remove SQLite journal files
rm avatarforge.db-journal
rm avatarforge.db-shm
rm avatarforge.db-wal
```

**Solution 3: Use PostgreSQL instead**
```bash
# For production, use PostgreSQL
# Install PostgreSQL
sudo apt install postgresql

# Update .env
DATABASE_URL=postgresql://user:pass@localhost/avatarforge
```

**Solution 4: Increase timeout**
```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    connect_args={"timeout": 30}  # Increase from default 5
)
```

---

### Issue 21: Database corruption

**Symptoms:**
```bash
sqlite3.DatabaseError: database disk image is malformed
```

**Cause:** Improper shutdown, disk full, corruption

**Solutions:**

**Solution 1: Dump and restore**
```bash
# Dump database
sqlite3 avatarforge.db ".dump" > backup.sql

# Create new database
mv avatarforge.db avatarforge.db.corrupt

# Restore
sqlite3 avatarforge.db < backup.sql
```

**Solution 2: Use integrity check**
```bash
# Check integrity
sqlite3 avatarforge.db "PRAGMA integrity_check;"

# Should return: ok
```

**Solution 3: Recover what you can**
```bash
# Try to recover
sqlite3 avatarforge.db ".recover" | sqlite3 recovered.db

# Use recovered database
mv avatarforge.db avatarforge.db.bad
mv recovered.db avatarforge.db
```

**Solution 4: Start fresh (last resort)**
```bash
# Backup corrupt database
mv avatarforge.db avatarforge.db.corrupt

# Initialize new database
python3 -m avatarforge.database.init_db

# You'll lose data, but API will work
```

---

## Model Download Issues

### Issue 22: "401 Unauthorized" downloading Qwen models

**Symptoms:**
```bash
curl: (22) The requested URL returned error: 401
```

**Cause:** HuggingFace token not provided or invalid

**Solutions:**

**Solution 1: Get HuggingFace token**
```bash
# 1. Visit https://huggingface.co/settings/tokens
# 2. Create new token (READ access)
# 3. Copy token

# Set token
export HF_TOKEN='hf_your_token_here'

# Run download script
bash download_models.sh
```

**Solution 2: Use huggingface-cli**
```bash
# Install
pip install -U huggingface_hub

# Login (saves token)
huggingface-cli login

# Paste your token when prompted

# Now run download script
bash download_models.sh
```

**Solution 3: Verify token**
```bash
# Test token
curl -H "Authorization: Bearer $HF_TOKEN" \
  https://huggingface.co/api/whoami

# Should return your username
```

---

### Issue 23: Model downloads but file is 0 bytes or corrupted

**Symptoms:**
```bash
-rw-r--r-- 1 user user 0 Nov 15 08:00 qwen_image_edit_fp8_e4m3fn.safetensors
```

**Cause:** Download interrupted, network issue

**Solutions:**

**Solution 1: Delete and re-download**
```bash
# Delete corrupt files
rm comfyui-dev/models/diffusion_models/*.safetensors
rm comfyui-dev/models/text_encoders/*.safetensors
rm comfyui-dev/models/vae/*.safetensors
rm comfyui-dev/models/loras/*.safetensors

# Re-run download script
bash download_models.sh
```

**Solution 2: Check disk space**
```bash
df -h

# Ensure you have enough space
# Qwen models need ~10GB total
```

**Solution 3: Check network**
```bash
# Test connection to HuggingFace
curl -I https://huggingface.co

# Should return 200 OK
```

**Solution 4: Download with wget instead of curl**
```bash
# Manual download with wget
wget --header="Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models/resolve/main/qwen_image_edit_fp8_e4m3fn.safetensors?download=true" \
  -O qwen_image_edit_fp8_e4m3fn.safetensors
```

---

### Issue 24: Download script shows "file too small" but re-downloads keep failing

**Symptoms:**
```bash
⚠ File exists but is too small (29MB < 4000MB), re-downloading...
✗ Download failed - file too small (29MB < 4000MB)
```

**Cause:** Repeated 401/403 errors downloading HTML error pages

**Solutions:**

**Solution 1: Verify token is set**
```bash
# Check token is exported
echo $HF_TOKEN

# Should show: hf_xxxx...
```

**Solution 2: Check file contents**
```bash
# See what's actually being downloaded
cat comfyui-dev/models/diffusion_models/qwen_image_edit_fp8_e4m3fn.safetensors

# If you see HTML or error message, it's a failed download
```

**Solution 3: Download manually via browser**
```bash
# 1. Visit https://huggingface.co/Comfy-Org/Qwen-Image-Edit_diffusion_models
# 2. Click on file
# 3. Download button
# 4. Save to correct location
```

**Solution 4: Check HuggingFace status**
```bash
# Visit https://status.huggingface.co
# Check if service is down
```

---

## API Error Messages

### Issue 25: 400 Bad Request - Validation Error

**Symptoms:**
```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Cause:** Missing required field in request

**Solutions:**

**Solution 1: Check required fields**
```python
# Minimal required request
{
    "prompt": "your description here"
}

# All fields
{
    "prompt": "warrior character",  # REQUIRED
    "pose_file_id": "optional-uuid",
    "reference_file_id": "optional-uuid",
    "clothing": "optional description",
    "style": "optional style",
    "realism": false  # optional, default false
}
```

**Solution 2: Validate before sending**
```python
def validate_request(data):
    if 'prompt' not in data:
        raise ValueError("prompt is required")
    if not isinstance(data.get('realism', False), bool):
        raise ValueError("realism must be boolean")
    return True

# Use
request_data = {"prompt": "warrior"}
validate_request(request_data)
```

---

### Issue 26: 404 Not Found - Resource doesn't exist

**Symptoms:**
```json
{
  "detail": "Generation not found"
}
```
**HTTP Status:** 404

**Cause:** Invalid ID or resource deleted

**Solutions:**

**Solution 1: Verify ID is correct**
```python
# Check generation_id format
# Should be UUID: 550e8400-e29b-41d4-a716-446655440000

# Not:
# - "abc123" (too short)
# - 12345 (number)
# - malformed UUID
```

**Solution 2: List generations to find valid ID**
```bash
curl http://localhost:8000/avatarforge-controller/generations?limit=10

# Get valid IDs from response
```

**Solution 3: Check if deleted**
```python
# Resource may have been deleted
# Create new generation instead
```

---

### Issue 27: 422 Unprocessable Entity - Invalid field values

**Symptoms:**
```json
{
  "detail": [
    {
      "loc": ["body", "width"],
      "msg": "ensure this value is greater than 64",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**Cause:** Field value out of range

**Solutions:**

**Solution 1: Check value constraints**
```python
# Width/Height: 64 - 4096
{
    "width": 512,   # ✓ Valid
    "height": 768   # ✓ Valid
}

# Not:
{
    "width": 32,    # ✗ Too small
    "height": 5000  # ✗ Too large
}
```

**Solution 2: Check type**
```python
# Steps must be integer
{
    "steps": 30  # ✓ Valid
}

# Not:
{
    "steps": "30"  # ✗ String
}
```

---

### Issue 28: 500 Internal Server Error

**Symptoms:**
```json
{
  "detail": "Internal server error"
}
```
**HTTP Status:** 500

**Cause:** Server-side bug, database issue, or dependency failure

**Solutions:**

**Solution 1: Check server logs**
```bash
# Run with debug logging
uvicorn main:app --log-level debug

# Look for Python traceback
```

**Solution 2: Test database**
```bash
python3 -m avatarforge.database.init_db

# Should complete without errors
```

**Solution 3: Restart server**
```bash
# Stop server (Ctrl+C)
# Start again
uvicorn main:app --reload
```

**Solution 4: Report bug**
```bash
# If persistent, report with:
# - Request you sent
# - Full error message
# - Server logs
```

---

### Issue 29: 503 Service Unavailable - ComfyUI not accessible

**Symptoms:**
```json
{
  "detail": "ComfyUI service unavailable"
}
```
**HTTP Status:** 503

**Cause:** ComfyUI not running or not accessible

**Solutions:**

See [Issue 7: ComfyUI unavailable](#issue-7-comfyui-unavailable-in-health-check)

---

## Performance Issues

### Issue 30: API very slow to respond

**Symptoms:**
- Requests take 10+ seconds
- Timeout errors
- Sluggish performance

**Cause:** Database issues, disk I/O, resource constraints

**Solutions:**

**Solution 1: Check database size**
```bash
# Check database file size
ls -lh avatarforge.db

# If huge (> 1GB), may need cleanup
```

**Solution 2: Clean old generations**
```python
# Use cleanup script from EXAMPLES.md
python cleanup.py --days 30 --status completed --live
```

**Solution 3: Check disk I/O**
```bash
# Check disk usage
df -h

# Check I/O wait
top
# Look for high %wa (wait)
```

**Solution 4: Use PostgreSQL**
```bash
# SQLite slower for concurrent access
# Switch to PostgreSQL for better performance
```

**Solution 5: Add database indexes**
```python
# Already included in schema
# If custom queries, add indexes
```

---

### Issue 31: Generation takes very long time

**Symptoms:**
- 5+ minutes per generation
- Slow progress

**Cause:** Hardware constraints, large image size, high steps

**Solutions:**

**Solution 1: Reduce image size**
```python
# 1024x1024 is slow
# Use 512x512 for faster generation
generate_avatar(prompt, width=512, height=512)
```

**Solution 2: Reduce steps**
```python
# 50 steps is slow
# 20-30 steps usually sufficient
generate_avatar(prompt, steps=25)
```

**Solution 3: Check GPU usage**
```bash
nvidia-smi

# Should show GPU at 90-100% during generation
# If low, may be CPU-bottlenecked
```

**Solution 4: Check GPU vs CPU**
```bash
# Ensure using GPU
# CPU generation is 10-100x slower

# Check ComfyUI startup logs
# Should show: "Using GPU"
```

---

### Issue 32: High memory usage

**Symptoms:**
```bash
# Server using 4GB+ RAM
# System becoming slow
```

**Cause:** Memory leaks, large caching, many concurrent requests

**Solutions:**

**Solution 1: Restart server periodically**
```bash
# Add to cron
# Restart every 24 hours
```

**Solution 2: Limit concurrent requests**
```python
# Process generations one at a time
# Don't batch 100 requests at once
```

**Solution 3: Monitor memory**
```bash
# Check memory usage
top
# or
htop

# Look for python processes
```

**Solution 4: Check for leaks**
```bash
# Run with memory profiling
pip install memory_profiler

# Profile code
python -m memory_profiler main.py
```

---

## Platform-Specific Issues

### Issue 33: Windows - "No module named '_sqlite3'"

**Symptoms:**
```
ModuleNotFoundError: No module named '_sqlite3'
```

**Platform:** Windows

**Cause:** Python installation missing SQLite support

**Solutions:**

**Solution 1: Reinstall Python**
```bash
# Download Python from python.org
# During install, check "Add Python to PATH"
# Check "pip" and "tcl/tk and IDLE"
```

**Solution 2: Use conda**
```bash
# Install Anaconda or Miniconda
# Create environment
conda create -n avatarforge python=3.11
conda activate avatarforge

# Install dependencies
pip install -r requirements.txt
```

---

### Issue 34: macOS - "Operation not permitted" errors

**Symptoms:**
```bash
OSError: [Errno 1] Operation not permitted
```

**Platform:** macOS

**Cause:** macOS security restrictions

**Solutions:**

**Solution 1: Grant Full Disk Access**
```
1. Open System Preferences > Security & Privacy
2. Go to Privacy tab
3. Select "Full Disk Access"
4. Click lock to make changes
5. Add Terminal or your IDE
```

**Solution 2: Use different location**
```bash
# Move project out of protected directories
# Not in: ~/Desktop, ~/Documents, ~/Downloads

# Use:
cd ~/Projects
git clone ...
```

---

### Issue 35: Linux - Permission denied on storage directory

**Symptoms:**
```bash
PermissionError: [Errno 13] Permission denied: './storage/files'
```

**Platform:** Linux

**Cause:** Wrong file ownership or permissions

**Solutions:**

**Solution 1: Fix ownership**
```bash
# Take ownership
sudo chown -R $USER:$USER ./storage

# Set permissions
chmod -R u+rw ./storage
```

**Solution 2: Check SELinux (if applicable)**
```bash
# Check SELinux status
getenforce

# If Enforcing, may need to adjust
sudo setenforce 0  # Temporary
```

---

## Network & Firewall Issues

### Issue 36: Cannot access API from other machines

**Symptoms:**
```
Connection refused from 192.168.1.x
Cannot access http://server-ip:8000
```

**Cause:** Server bound to localhost only, firewall blocking

**Solutions:**

**Solution 1: Bind to all interfaces**
```bash
# Instead of:
uvicorn main:app --host 127.0.0.1

# Use:
uvicorn main:app --host 0.0.0.0
```

**Solution 2: Open firewall**
```bash
# Ubuntu/Debian
sudo ufw allow 8000

# CentOS/RHEL
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload

# macOS
# System Preferences > Security > Firewall > Firewall Options
# Add port 8000
```

**Solution 3: Check network**
```bash
# On server, check what's listening
netstat -tuln | grep 8000

# Should show 0.0.0.0:8000 not 127.0.0.1:8000
```

---

### Issue 37: CORS errors in browser

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Cause:** CORS not configured for frontend origin

**Solutions:**

**Solution 1: Add origin to .env**
```bash
# In .env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Restart server
```

**Solution 2: Allow all origins (development only)**
```python
# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠ Dev only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Solution 3: Use proxy**
```bash
# In React/Vue, use proxy in package.json
{
  "proxy": "http://localhost:8000"
}
```

---

## Dependency Conflicts

### Issue 38: Conflicting package versions

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Cause:** Version conflicts between packages

**Solutions:**

**Solution 1: Use virtual environment**
```bash
# Create clean environment
python3 -m venv venv_fresh
source venv_fresh/bin/activate

# Install from scratch
pip install -r requirements.txt
```

**Solution 2: Use uv (faster, better resolver)**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Solution 3: Pin versions**
```bash
# Generate exact versions
pip freeze > requirements-lock.txt

# Install from lock file
pip install -r requirements-lock.txt
```

---

### Issue 39: "ImportError: cannot import name 'X' from 'Y'"

**Symptoms:**
```python
ImportError: cannot import name 'BaseModel' from 'pydantic'
```

**Cause:** Wrong package version installed

**Solutions:**

**Solution 1: Check installed version**
```bash
pip show pydantic

# Should match requirements.txt
```

**Solution 2: Reinstall specific package**
```bash
pip install --force-reinstall pydantic==2.5.0
```

**Solution 3: Reinstall all**
```bash
pip install --force-reinstall -r requirements.txt
```

---

## Docker Issues

### Issue 40: Docker container exits immediately

**Symptoms:**
```bash
docker ps
# Container not running

docker logs avatarforge
# Shows error and exit
```

**Cause:** Startup error, missing dependencies, port conflict

**Solutions:**

**Solution 1: Check logs**
```bash
docker logs avatarforge

# Look for Python errors
```

**Solution 2: Run interactively**
```bash
# Debug mode
docker run -it avatarforge /bin/bash

# Try running manually
python main.py
```

**Solution 3: Check ports**
```bash
# Ensure port not in use
lsof -i :8000

# Kill conflicting process or use different port
docker run -p 8001:8000 avatarforge
```

---

### Issue 41: Cannot connect to ComfyUI from Docker

**Symptoms:**
```
Connection refused to http://localhost:8188
```

**Cause:** Docker networking, localhost not accessible

**Solutions:**

**Solution 1: Use host network**
```bash
docker run --network host avatarforge
```

**Solution 2: Use host.docker.internal**
```bash
# In .env
COMFYUI_URL=http://host.docker.internal:8188

# Or in docker-compose.yml
environment:
  - COMFYUI_URL=http://host.docker.internal:8188
```

**Solution 3: Run ComfyUI in Docker too**
```yaml
# docker-compose.yml
services:
  comfyui:
    image: comfyui:latest
    ports:
      - "8188:8188"

  avatarforge:
    image: avatarforge:latest
    environment:
      - COMFYUI_URL=http://comfyui:8188
    depends_on:
      - comfyui
```

---

## Quick Reference: Common Solutions

### Database Issues → Reinitialize
```bash
python3 -m avatarforge.database.init_db
```

### File Upload Issues → Check Storage
```bash
mkdir -p ./storage/{files,outputs,temp}
chmod -R u+rw ./storage
```

### ComfyUI Issues → Check Health
```bash
curl http://localhost:8188/system_stats
```

### Dependencies Issues → Fresh Install
```bash
python3 -m venv venv_fresh
source venv_fresh/bin/activate
pip install -r requirements.txt
```

### Port Conflicts → Use Different Port
```bash
uvicorn main:app --port 8001
```

### Performance Issues → Clean Database
```bash
python cleanup.py --days 30 --status all --live
```

---

## Still Having Issues?

### Debug Checklist

1. **Check health endpoint:**
   ```bash
   curl http://localhost:8000/avatarforge-controller/health
   ```

2. **Check ComfyUI:**
   ```bash
   curl http://localhost:8188/system_stats
   ```

3. **Check database:**
   ```bash
   ls -lh avatarforge.db
   sqlite3 avatarforge.db ".tables"
   ```

4. **Check storage:**
   ```bash
   ls -la storage/
   ```

5. **Check logs:**
   ```bash
   uvicorn main:app --log-level debug
   ```

6. **Check dependencies:**
   ```bash
   pip list
   ```

### Get Help

If none of these solutions work:

1. **Check GitHub Issues:** Search existing issues
2. **Create New Issue:** Include:
   - Error message (full traceback)
   - What you tried (solutions attempted)
   - Platform (OS, Python version)
   - Logs (server logs, ComfyUI logs)

---

**Last Updated:** 2025-01-15
**Version:** 1.0

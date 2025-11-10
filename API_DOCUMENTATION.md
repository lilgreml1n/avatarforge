# AvatarForge API Documentation

Complete API reference for the AvatarForge avatar generation system with file management and deduplication.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repo-url>
cd avatarforge

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python -m avatarforge.database.init_db

# Start server
uvicorn avatarforge.main:app --reload
```

### 2. Basic Usage

```python
import requests

# Upload a pose reference image
with open('pose.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/upload/pose_image',
        files={'file': f}
    )
    file_id = response.json()['file_id']

# Generate avatar with uploaded pose
response = requests.post(
    'http://localhost:8000/avatarforge-controller/generate/avatar',
    json={
        'prompt': 'female warrior, blue armor, long white hair',
        'pose_file_id': file_id,
        'realism': False
    }
)

generation_id = response.json()['generation_id']

# Check generation status
status = requests.get(
    f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
)
print(status.json())
```

---

## 📂 File Management Endpoints

### Upload Pose Image

**POST** `/avatarforge-controller/upload/pose_image`

Upload a pose reference image with automatic deduplication.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload

**File Requirements:**
- Format: PNG, JPG, JPEG, WEBP
- Max size: 50MB
- Dimensions: 64x64 to 4096x4096 pixels

**Response:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "pose.png",
  "content_hash": "a1b2c3d4...",
  "size": 1024000,
  "mime_type": "image/png",
  "dimensions": {"width": 512, "height": 512},
  "url": "/files/550e8400-e29b-41d4-a716-446655440000",
  "is_duplicate": false,
  "created_at": "2025-01-09T12:00:00Z"
}
```

**Deduplication:**
If you upload the same image twice (same content hash), you'll get the same `file_id` back with `is_duplicate: true`. This saves storage space!

---

### Upload Reference Image

**POST** `/avatarforge-controller/upload/reference_image`

Upload a style reference image. Same behavior as pose image upload.

---

### Download File

**GET** `/avatarforge-controller/files/{file_id}`

Download a previously uploaded file.

**Response:**
- Returns the actual image file with appropriate MIME type

---

### Check File Hash

**GET** `/avatarforge-controller/files/hash/{content_hash}`

Check if a file with a specific SHA256 hash already exists.

**Use Case:** Calculate hash locally before uploading to check if file already exists.

**Response:**
```json
{
  "exists": true,
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "File exists: pose.png"
}
```

**Hash Calculation Example:**
```python
import hashlib

with open('image.png', 'rb') as f:
    content_hash = hashlib.sha256(f.read()).hexdigest()

response = requests.get(f'/files/hash/{content_hash}')
if response.json()['exists']:
    file_id = response.json()['file_id']
    # Skip upload, use existing file_id
```

---

### Delete File

**DELETE** `/avatarforge-controller/files/{file_id}?force=false`

Delete an uploaded file.

**Behavior:**
- If file has references: Soft delete (marked as deleted)
- If no references: Hard delete (removed from disk)
- Use `force=true` to force deletion

---

## 🎨 Avatar Generation Endpoints

### Generate Avatar

**POST** `/avatarforge-controller/generate/avatar`

Generate an avatar from a text prompt with optional pose and reference images.

**Request Body:**
```json
{
  "prompt": "female warrior, blue armor, long white hair",
  "pose_file_id": "550e8400-e29b-41d4-a716-446655440000",
  "reference_file_id": "660e8400-e29b-41d4-a716-446655440000",
  "clothing": "full plate armor, red cape",
  "style": "watercolor",
  "realism": false
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | ✅ | Detailed avatar description |
| `pose_file_id` | string | ❌ | ID of uploaded pose image |
| `reference_file_id` | string | ❌ | ID of uploaded reference image |
| `clothing` | string | ❌ | Specific clothing details |
| `style` | string | ❌ | Art style: 'watercolor', 'pixel art', etc. |
| `realism` | boolean | ❌ | true=realistic, false=anime (default: false) |
| `pose_image` | string | ❌ | [LEGACY] Base64 encoded image |
| `reference_image` | string | ❌ | [LEGACY] Base64 encoded image |

**Response:**
```json
{
  "generation_id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Generation processing",
  "created_at": "2025-01-09T12:00:00Z",
  "started_at": "2025-01-09T12:00:01Z",
  "completed_at": null,
  "error": null,
  "comfyui_prompt_id": "abc123"
}
```

**Workflow:**
1. Upload pose/reference images (optional)
2. POST to this endpoint with prompt + file IDs
3. Receive `generation_id`
4. Poll `GET /generations/{id}` to check status
5. Download results when `status='completed'`

---

### Generate Specific Pose

**POST** `/avatarforge-controller/generate_pose?pose=front`

Generate avatar in a specific pose view.

**Query Parameters:**
- `pose`: One of `front`, `back`, `side`, `quarter`

**Pose Types:**
- **front**: Front-facing view, standard proportions
- **back**: Back view, different lighting
- **side**: Side profile, narrow aspect ratio
- **quarter**: 3/4 view, partial features

**Request Body:** Same as Generate Avatar

---

### Generate All Poses

**POST** `/avatarforge-controller/generate_all_poses`

Generate avatar in all 4 pose views (front, back, side, quarter) at once.

**Perfect for:**
- Character sheets
- Game assets
- Complete character references

**Note:** Takes longer as it creates 4 separate images.

---

## 📊 Generation Management Endpoints

### Get Generation Status

**GET** `/avatarforge-controller/generations/{generation_id}`

Check status and get results when complete.

**Status Values:**
- `queued`: Waiting to start
- `processing`: Currently generating
- `completed`: Done! Results in `output_files`
- `failed`: Error occurred, see `error` field

**Response (Completed):**
```json
{
  "generation_id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "message": "Generation completed",
  "output_files": [
    {
      "filename": "avatarforge_00001.png",
      "url": "/outputs/770e8400-e29b-41d4-a716-446655440000/output.png",
      "pose_type": "front",
      "size": 2048000,
      "dimensions": {"width": 512, "height": 512}
    }
  ],
  "created_at": "2025-01-09T12:00:00Z",
  "started_at": "2025-01-09T12:00:01Z",
  "completed_at": "2025-01-09T12:00:30Z"
}
```

**Polling Pattern:**
```python
import time

while True:
    response = requests.get(f'/generations/{generation_id}')
    status = response.json()['status']

    if status in ['completed', 'failed']:
        break

    time.sleep(2)  # Wait 2 seconds between checks
```

---

### List Generations

**GET** `/avatarforge-controller/generations?limit=50&offset=0&status=completed`

List all generations with pagination and filtering.

**Query Parameters:**
- `limit`: Results per page (1-100, default: 50)
- `offset`: Skip N results (for pagination)
- `status`: Filter by status

**Response:**
```json
{
  "total": 150,
  "generations": [...],
  "limit": 50,
  "offset": 0
}
```

---

### Delete Generation

**DELETE** `/avatarforge-controller/generations/{generation_id}`

Delete a generation and decrement file references.

**What Happens:**
1. Generation record deleted
2. File reference counts decremented
3. Files with 0 references eligible for cleanup

---

## 🛠️ Utility Endpoints

### Health Check

**GET** `/avatarforge-controller/health`

Check API and ComfyUI backend health.

**Response:**
```json
{
  "api_status": "healthy",
  "comfyui": {
    "status": "healthy",
    "url": "http://localhost:8188",
    "stats": {...}
  }
}
```

---

### List Poses

**GET** `/avatarforge-controller/poses`

Get all supported pose types with descriptions.

---

## 🔄 Complete Workflows

### Workflow 1: Simple Text-to-Avatar

```python
# No images, just text
response = requests.post('/generate/avatar', json={
    'prompt': 'cyberpunk character, neon hair, tech implants',
    'realism': False
})

generation_id = response.json()['generation_id']
# Poll for results...
```

---

### Workflow 2: Avatar with Pose Reference

```python
# 1. Upload pose image
with open('reference_pose.png', 'rb') as f:
    upload_response = requests.post(
        '/upload/pose_image',
        files={'file': f}
    )
    pose_file_id = upload_response.json()['file_id']

# 2. Generate with pose
gen_response = requests.post('/generate/avatar', json={
    'prompt': 'warrior character, blue armor',
    'pose_file_id': pose_file_id,
    'realism': False
})
```

---

### Workflow 3: Reuse Existing File (Deduplication)

```python
import hashlib

# Calculate hash before uploading
with open('pose.png', 'rb') as f:
    content = f.read()
    file_hash = hashlib.sha256(content).hexdigest()

# Check if file already exists
check_response = requests.get(f'/files/hash/{file_hash}')

if check_response.json()['exists']:
    # File exists, reuse it!
    file_id = check_response.json()['file_id']
    print(f"File already exists, using {file_id}")
else:
    # Upload new file
    with open('pose.png', 'rb') as f:
        upload_response = requests.post(
            '/upload/pose_image',
            files={'file': f}
        )
        file_id = upload_response.json()['file_id']

# Use file_id in generation
requests.post('/generate/avatar', json={
    'prompt': 'character',
    'pose_file_id': file_id
})
```

---

### Workflow 4: Generate All Poses for Character Sheet

```python
# Generate all 4 pose views
response = requests.post('/generate_all_poses', json={
    'prompt': 'knight character, silver armor, red cape',
    'clothing': 'full plate armor',
    'realism': False
})

generation_id = response.json()['generation_id']

# Poll until complete
while True:
    status = requests.get(f'/generations/{generation_id}')
    if status.json()['status'] == 'completed':
        output_files = status.json()['output_files']
        for file in output_files:
            print(f"Pose: {file['pose_type']} - URL: {file['url']}")
        break
    time.sleep(2)
```

---

## 🎯 Best Practices

### 1. File Upload Optimization

**DO:**
- Check file hash before uploading to avoid duplicates
- Reuse existing file IDs when possible
- Delete files when no longer needed

**DON'T:**
- Upload the same file multiple times
- Use base64 encoding when file upload is available
- Keep unused files indefinitely

---

### 2. Generation Management

**DO:**
- Poll with reasonable intervals (2-5 seconds)
- Handle all status values (queued, processing, completed, failed)
- Clean up old generations

**DON'T:**
- Poll continuously without delay
- Assume instant completion
- Ignore error responses

---

### 3. Error Handling

```python
try:
    response = requests.post('/generate/avatar', json=request_data)
    response.raise_for_status()

    generation = response.json()

    if generation['status'] == 'failed':
        print(f"Generation failed: {generation.get('error')}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
```

---

## 📝 Environment Variables

See `.env.example` for all configuration options:

```bash
# Storage
STORAGE_PATH=./storage
MAX_FILE_SIZE=52428800  # 50MB
MAX_IMAGE_DIMENSION=4096
MIN_IMAGE_DIMENSION=64
FILE_CLEANUP_DAYS=30

# ComfyUI
COMFYUI_URL=http://localhost:8188

# Database
DATABASE_URL=sqlite:///./avatarforge.db
```

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Upload file
curl -X POST http://localhost:8000/avatarforge-controller/upload/pose_image \
  -F "file=@pose.png"

# Generate avatar
curl -X POST http://localhost:8000/avatarforge-controller/generate/avatar \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "warrior character",
    "realism": false
  }'

# Check status
curl http://localhost:8000/avatarforge-controller/generations/{generation_id}
```

---

## 🐛 Troubleshooting

### File Upload Fails

**Error:** "File too large"
- **Solution:** Check `MAX_FILE_SIZE` in config, compress image

**Error:** "Invalid image file"
- **Solution:** Ensure file is PNG, JPG, or WEBP

### Generation Stuck in "Processing"

- Check ComfyUI is running: `GET /health`
- Check ComfyUI logs for errors
- Verify `COMFYUI_URL` is correct

### Database Errors

- Ensure database is initialized: `python -m avatarforge.database.init_db`
- Check `DATABASE_URL` in `.env`

---

## 📚 Additional Resources

- **Swagger UI:** http://localhost:8000/docs (when server is running)
- **ReDoc:** http://localhost:8000/redoc
- **ComfyUI Documentation:** https://github.com/comfyanonymous/ComfyUI

---

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Implement authentication for file uploads
- Set up file size limits appropriately
- Regular cleanup of orphaned files

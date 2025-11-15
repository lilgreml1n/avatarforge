# AvatarForge API - Comprehensive Usage Guide

Complete guide with working examples, real payloads, and integration patterns for the AvatarForge avatar generation API.

## 📖 Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication & Setup](#authentication--setup)
3. [Working Examples - All Endpoints](#working-examples---all-endpoints)
4. [Common Workflows](#common-workflows)
5. [Integration Examples](#integration-examples)
6. [Error Handling](#error-handling)
7. [Performance & Optimization](#performance--optimization)
8. [Production Deployment](#production-deployment)

---

## Quick Start

### Prerequisites

```bash
# 1. Start ComfyUI
cd /path/to/comfyui
python main.py

# 2. Start AvatarForge API
cd /path/to/avatarforge
uv run python main.py

# 3. Verify it's running
curl http://localhost:8000/avatarforge-controller/health
```

### First Avatar in 30 Seconds

```bash
# Simple text-to-avatar
curl -X POST http://localhost:8000/avatarforge-controller/generate/avatar \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "female warrior, blue armor, long white hair, determined expression",
    "realism": false
  }'

# Response:
{
  "generation_id": "abc-123",
  "status": "processing",
  "message": "Generation started"
}

# Check status (repeat until status = "completed")
curl http://localhost:8000/avatarforge-controller/generations/abc-123
```

---

## Authentication & Setup

### Environment Configuration

Create `.env` file:

```bash
# Storage Settings
STORAGE_PATH=./storage
MAX_FILE_SIZE=52428800  # 50MB
MAX_IMAGE_DIMENSION=4096
MIN_IMAGE_DIMENSION=64
FILE_CLEANUP_DAYS=30

# ComfyUI Connection
COMFYUI_URL=http://localhost:8188

# Database
DATABASE_URL=sqlite:///./avatarforge.db

# Security
SECRET_KEY=your-secret-key-change-in-production

# Optional: File Cleanup Schedule
ENABLE_SCHEDULER=true
```

### Database Initialization

```bash
# Initialize database (creates tables)
python -m avatarforge.database.init_db

# Verify tables exist
python -c "from avatarforge.database.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

---

## Working Examples - All Endpoints

### 1. Health Check

**Check API and ComfyUI Status**

```bash
curl http://localhost:8000/avatarforge-controller/health
```

**Response:**
```json
{
  "api_status": "healthy",
  "comfyui": {
    "status": "healthy",
    "url": "http://localhost:8188",
    "stats": {
      "queue_pending": 0,
      "queue_running": 1
    }
  }
}
```

**Python Example:**
```python
import requests

response = requests.get('http://localhost:8000/avatarforge-controller/health')
health = response.json()

if health['api_status'] == 'healthy' and health['comfyui']['status'] == 'healthy':
    print("✓ System ready")
else:
    print("✗ System issues detected")
```

**JavaScript Example:**
```javascript
async function checkHealth() {
  const response = await fetch('http://localhost:8000/avatarforge-controller/health');
  const health = await response.json();

  if (health.api_status === 'healthy') {
    console.log('✓ API is healthy');
  }
  return health;
}
```

---

### 2. Upload Pose Image

**Upload with curl:**

```bash
curl -X POST http://localhost:8000/avatarforge-controller/upload/pose_image \
  -F "file=@/path/to/pose.png" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "pose.png",
  "content_hash": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890",
  "size": 1024000,
  "mime_type": "image/png",
  "dimensions": {
    "width": 512,
    "height": 512
  },
  "url": "/files/550e8400-e29b-41d4-a716-446655440000",
  "is_duplicate": false,
  "created_at": "2025-01-15T12:00:00Z"
}
```

**Python Example with Error Handling:**

```python
import requests
from pathlib import Path

def upload_pose_image(image_path: str) -> dict:
    """Upload a pose image with error handling."""

    # Validate file exists
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Prepare file upload
    with open(image_path, 'rb') as f:
        files = {'file': (Path(image_path).name, f, 'image/png')}

        try:
            response = requests.post(
                'http://localhost:8000/avatarforge-controller/upload/pose_image',
                files=files,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()

            if result.get('is_duplicate'):
                print(f"✓ File already exists, reusing: {result['file_id']}")
            else:
                print(f"✓ Uploaded new file: {result['file_id']}")

            return result

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 413:
                raise Exception("File too large (max 50MB)")
            elif e.response.status_code == 400:
                raise Exception("Invalid image format (use PNG, JPG, or WEBP)")
            else:
                raise Exception(f"Upload failed: {e.response.text}")
        except requests.exceptions.Timeout:
            raise Exception("Upload timed out after 30 seconds")

# Usage
try:
    result = upload_pose_image('my_pose.png')
    file_id = result['file_id']
except Exception as e:
    print(f"Error: {e}")
```

**JavaScript/TypeScript Example:**

```typescript
interface UploadResponse {
  file_id: string;
  filename: string;
  content_hash: string;
  size: number;
  mime_type: string;
  dimensions: { width: number; height: number };
  url: string;
  is_duplicate: boolean;
  created_at: string;
}

async function uploadPoseImage(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(
      'http://localhost:8000/avatarforge-controller/upload/pose_image',
      {
        method: 'POST',
        body: formData,
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    const result: UploadResponse = await response.json();

    if (result.is_duplicate) {
      console.log('File already exists, reusing:', result.file_id);
    }

    return result;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}

// Usage in React
function ImageUploader() {
  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const result = await uploadPoseImage(file);
      console.log('Uploaded:', result.file_id);
    } catch (error) {
      alert('Upload failed: ' + error.message);
    }
  };

  return <input type="file" accept="image/*" onChange={handleUpload} />;
}
```

---

### 3. Upload Reference Image

Same as pose image upload, just different endpoint:

```bash
curl -X POST http://localhost:8000/avatarforge-controller/upload/reference_image \
  -F "file=@/path/to/reference.jpg"
```

---

### 4. Check File by Hash (Avoid Duplicate Uploads)

**Calculate hash locally, then check:**

```bash
# Calculate SHA256 hash
HASH=$(sha256sum pose.png | awk '{print $1}')

# Check if file exists
curl "http://localhost:8000/avatarforge-controller/files/hash/$HASH"
```

**Python Example:**

```python
import hashlib
import requests

def check_file_exists(image_path: str) -> dict | None:
    """Check if file already exists by hash."""

    # Calculate SHA256 hash
    with open(image_path, 'rb') as f:
        content_hash = hashlib.sha256(f.read()).hexdigest()

    # Check if exists
    response = requests.get(
        f'http://localhost:8000/avatarforge-controller/files/hash/{content_hash}'
    )

    result = response.json()

    if result.get('exists'):
        return result  # Returns file_id, can reuse
    return None

# Smart upload: check before uploading
existing = check_file_exists('pose.png')
if existing:
    file_id = existing['file_id']
    print(f"File already exists: {file_id}")
else:
    # Upload new file
    result = upload_pose_image('pose.png')
    file_id = result['file_id']
```

---

### 5. Download File

```bash
# Download file
curl http://localhost:8000/avatarforge-controller/files/550e8400-e29b-41d4-a716-446655440000 \
  --output downloaded_image.png
```

**Python Example:**

```python
def download_file(file_id: str, output_path: str):
    """Download a file by ID."""

    response = requests.get(
        f'http://localhost:8000/avatarforge-controller/files/{file_id}',
        stream=True
    )
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✓ Downloaded to: {output_path}")

# Usage
download_file('550e8400-e29b-41d4-a716-446655440000', 'pose.png')
```

---

### 6. Generate Avatar (Basic)

**Minimal Request:**

```bash
curl -X POST http://localhost:8000/avatarforge-controller/generate/avatar \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "female warrior, blue armor, long white hair",
    "realism": false
  }'
```

**Full Request with All Options:**

```bash
curl -X POST http://localhost:8000/avatarforge-controller/generate/avatar \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "female warrior, determined expression, battle stance",
    "pose_file_id": "550e8400-e29b-41d4-a716-446655440000",
    "reference_file_id": "660e8400-e29b-41d4-a716-446655440000",
    "clothing": "full plate armor, red cape, silver trim",
    "style": "watercolor painting",
    "realism": false
  }'
```

**Response:**
```json
{
  "generation_id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Generation started",
  "created_at": "2025-01-15T12:00:00Z",
  "started_at": "2025-01-15T12:00:01Z",
  "completed_at": null,
  "error": null,
  "comfyui_prompt_id": "abc123"
}
```

**Python Example:**

```python
from typing import Optional

def generate_avatar(
    prompt: str,
    pose_file_id: Optional[str] = None,
    reference_file_id: Optional[str] = None,
    clothing: Optional[str] = None,
    style: Optional[str] = None,
    realism: bool = False
) -> str:
    """Generate an avatar and return generation_id."""

    payload = {
        "prompt": prompt,
        "realism": realism
    }

    # Add optional parameters
    if pose_file_id:
        payload["pose_file_id"] = pose_file_id
    if reference_file_id:
        payload["reference_file_id"] = reference_file_id
    if clothing:
        payload["clothing"] = clothing
    if style:
        payload["style"] = style

    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate/avatar',
        json=payload
    )
    response.raise_for_status()

    result = response.json()
    generation_id = result['generation_id']

    print(f"✓ Generation started: {generation_id}")
    return generation_id

# Usage
generation_id = generate_avatar(
    prompt="cyberpunk warrior, neon blue hair, tech implants",
    clothing="leather jacket, combat boots",
    style="digital art",
    realism=False
)
```

---

### 7. Generate Specific Pose

```bash
# Front view
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=front" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor",
    "realism": false
  }'

# Back view
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=back" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor",
    "realism": false
  }'

# Side view
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=side" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor",
    "realism": false
  }'

# Quarter view (3/4)
curl -X POST "http://localhost:8000/avatarforge-controller/generate_pose?pose=quarter" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor",
    "realism": false
  }'
```

---

### 8. Generate All Poses (Character Sheet)

```bash
curl -X POST http://localhost:8000/avatarforge-controller/generate_all_poses \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character, silver armor, red cape",
    "clothing": "full plate armor",
    "realism": false
  }'
```

**Python Example with Polling:**

```python
import time

def generate_character_sheet(prompt: str, clothing: str = None) -> list:
    """Generate all 4 pose views for character sheet."""

    payload = {"prompt": prompt, "realism": False}
    if clothing:
        payload["clothing"] = clothing

    # Start generation
    response = requests.post(
        'http://localhost:8000/avatarforge-controller/generate_all_poses',
        json=payload
    )
    response.raise_for_status()

    generation_id = response.json()['generation_id']
    print(f"✓ Generating character sheet: {generation_id}")

    # Poll for completion
    while True:
        status_response = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        )
        status = status_response.json()

        if status['status'] == 'completed':
            print("✓ Character sheet complete!")
            return status['output_files']
        elif status['status'] == 'failed':
            raise Exception(f"Generation failed: {status.get('error')}")

        print(f"  Status: {status['status']}...")
        time.sleep(3)

# Usage
try:
    files = generate_character_sheet(
        prompt="warrior character, blue armor",
        clothing="full plate armor, red cape"
    )

    for file in files:
        print(f"  {file['pose_type']}: {file['url']}")
except Exception as e:
    print(f"Error: {e}")
```

---

### 9. Get Generation Status

```bash
curl http://localhost:8000/avatarforge-controller/generations/770e8400-e29b-41d4-a716-446655440000
```

**Response (Processing):**
```json
{
  "generation_id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Generation in progress",
  "created_at": "2025-01-15T12:00:00Z",
  "started_at": "2025-01-15T12:00:01Z",
  "completed_at": null,
  "error": null
}
```

**Response (Completed):**
```json
{
  "generation_id": "770e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "message": "Generation completed successfully",
  "output_files": [
    {
      "filename": "avatarforge_00001.png",
      "url": "/outputs/770e8400-e29b-41d4-a716-446655440000/output.png",
      "pose_type": "front",
      "size": 2048000,
      "dimensions": {"width": 512, "height": 512}
    }
  ],
  "created_at": "2025-01-15T12:00:00Z",
  "started_at": "2025-01-15T12:00:01Z",
  "completed_at": "2025-01-15T12:00:45Z",
  "error": null
}
```

**Python Polling Example:**

```python
import time
from typing import Dict, Any

def wait_for_generation(generation_id: str, timeout: int = 300) -> Dict[str, Any]:
    """
    Poll generation status until complete or timeout.

    Args:
        generation_id: ID of generation to monitor
        timeout: Maximum seconds to wait (default: 5 minutes)

    Returns:
        Final generation status dict

    Raises:
        TimeoutError: If generation doesn't complete within timeout
        Exception: If generation fails
    """
    start_time = time.time()
    poll_interval = 2  # seconds

    while True:
        # Check timeout
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Generation timed out after {timeout}s")

        # Get status
        response = requests.get(
            f'http://localhost:8000/avatarforge-controller/generations/{generation_id}'
        )
        response.raise_for_status()
        status = response.json()

        # Check if complete
        if status['status'] == 'completed':
            elapsed = time.time() - start_time
            print(f"✓ Generation complete in {elapsed:.1f}s")
            return status
        elif status['status'] == 'failed':
            raise Exception(f"Generation failed: {status.get('error', 'Unknown error')}")

        # Still processing
        print(f"  {status['status']}... ({int(time.time() - start_time)}s)")
        time.sleep(poll_interval)

# Usage
generation_id = generate_avatar("warrior character")
result = wait_for_generation(generation_id)

# Download outputs
for output_file in result['output_files']:
    print(f"Output: {output_file['url']}")
```

---

### 10. List Generations

**All Generations:**

```bash
curl "http://localhost:8000/avatarforge-controller/generations?limit=50&offset=0"
```

**Filter by Status:**

```bash
# Only completed
curl "http://localhost:8000/avatarforge-controller/generations?status=completed&limit=100"

# Only failed
curl "http://localhost:8000/avatarforge-controller/generations?status=failed&limit=20"

# Only processing
curl "http://localhost:8000/avatarforge-controller/generations?status=processing"
```

**Pagination:**

```bash
# First page (0-49)
curl "http://localhost:8000/avatarforge-controller/generations?limit=50&offset=0"

# Second page (50-99)
curl "http://localhost:8000/avatarforge-controller/generations?limit=50&offset=50"

# Third page (100-149)
curl "http://localhost:8000/avatarforge-controller/generations?limit=50&offset=100"
```

**Response:**
```json
{
  "total": 250,
  "generations": [
    {
      "generation_id": "770e8400...",
      "status": "completed",
      "created_at": "2025-01-15T12:00:00Z",
      "output_files": [...]
    },
    ...
  ],
  "limit": 50,
  "offset": 0
}
```

**Python Pagination Example:**

```python
def get_all_generations(status: str = None) -> list:
    """Get all generations with automatic pagination."""

    all_generations = []
    limit = 100
    offset = 0

    while True:
        # Build URL
        url = f'http://localhost:8000/avatarforge-controller/generations?limit={limit}&offset={offset}'
        if status:
            url += f'&status={status}'

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        all_generations.extend(data['generations'])

        # Check if we have all results
        if offset + limit >= data['total']:
            break

        offset += limit

    print(f"✓ Retrieved {len(all_generations)} generations")
    return all_generations

# Usage
completed = get_all_generations(status='completed')
print(f"Total completed: {len(completed)}")
```

---

### 11. Delete Generation

```bash
curl -X DELETE http://localhost:8000/avatarforge-controller/generations/770e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "message": "Generation deleted successfully",
  "generation_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

---

### 12. Delete File

**Soft Delete (if has references):**

```bash
curl -X DELETE http://localhost:8000/avatarforge-controller/files/550e8400-e29b-41d4-a716-446655440000
```

**Force Delete:**

```bash
curl -X DELETE "http://localhost:8000/avatarforge-controller/files/550e8400-e29b-41d4-a716-446655440000?force=true"
```

---

### 13. List Available Poses

```bash
curl http://localhost:8000/avatarforge-controller/poses
```

**Response:**
```json
{
  "poses": [
    {
      "name": "front",
      "description": "Front-facing view with standard proportions"
    },
    {
      "name": "back",
      "description": "Back view with different lighting"
    },
    {
      "name": "side",
      "description": "Side profile with narrow aspect ratio"
    },
    {
      "name": "quarter",
      "description": "3/4 view showing partial features"
    }
  ]
}
```

---

## Common Workflows

### Workflow 1: Simple Text-to-Avatar

**Complete Python Example:**

```python
import requests
import time

BASE_URL = 'http://localhost:8000/avatarforge-controller'

def simple_generation(prompt: str):
    """Generate avatar from text prompt only."""

    # 1. Generate
    print(f"Generating: {prompt}")
    response = requests.post(
        f'{BASE_URL}/generate/avatar',
        json={"prompt": prompt, "realism": False}
    )
    generation_id = response.json()['generation_id']

    # 2. Poll for completion
    while True:
        status = requests.get(f'{BASE_URL}/generations/{generation_id}').json()

        if status['status'] == 'completed':
            print("✓ Complete!")
            return status['output_files'][0]['url']
        elif status['status'] == 'failed':
            raise Exception(status.get('error'))

        time.sleep(2)

# Usage
url = simple_generation("cyberpunk warrior, neon hair")
print(f"Download: {url}")
```

---

### Workflow 2: Upload Pose + Generate

```python
def generate_with_pose(prompt: str, pose_image_path: str):
    """Upload pose image and generate avatar."""

    # 1. Upload pose image
    with open(pose_image_path, 'rb') as f:
        upload_response = requests.post(
            f'{BASE_URL}/upload/pose_image',
            files={'file': f}
        )
    pose_file_id = upload_response.json()['file_id']
    print(f"✓ Uploaded pose: {pose_file_id}")

    # 2. Generate with pose
    gen_response = requests.post(
        f'{BASE_URL}/generate/avatar',
        json={
            "prompt": prompt,
            "pose_file_id": pose_file_id,
            "realism": False
        }
    )
    generation_id = gen_response.json()['generation_id']

    # 3. Wait for completion
    while True:
        status = requests.get(f'{BASE_URL}/generations/{generation_id}').json()
        if status['status'] == 'completed':
            return status['output_files'][0]
        time.sleep(2)

# Usage
result = generate_with_pose("warrior character", "my_pose.png")
print(f"Generated: {result['url']}")
```

---

### Workflow 3: Smart Upload (Check Hash First)

```python
import hashlib

def smart_upload_and_generate(prompt: str, image_path: str):
    """Check if file exists before uploading."""

    # 1. Calculate hash
    with open(image_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # 2. Check if file already exists
    check_response = requests.get(f'{BASE_URL}/files/hash/{file_hash}')
    check_data = check_response.json()

    if check_data['exists']:
        file_id = check_data['file_id']
        print(f"✓ File already exists: {file_id}")
    else:
        # 3. Upload new file
        with open(image_path, 'rb') as f:
            upload_response = requests.post(
                f'{BASE_URL}/upload/pose_image',
                files={'file': f}
            )
        file_id = upload_response.json()['file_id']
        print(f"✓ Uploaded new file: {file_id}")

    # 4. Generate
    gen_response = requests.post(
        f'{BASE_URL}/generate/avatar',
        json={"prompt": prompt, "pose_file_id": file_id}
    )

    return gen_response.json()['generation_id']
```

---

### Workflow 4: Batch Generation

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_generate(prompts: list[str]) -> list[dict]:
    """Generate multiple avatars in parallel."""

    def generate_one(prompt: str) -> dict:
        # Start generation
        response = requests.post(
            f'{BASE_URL}/generate/avatar',
            json={"prompt": prompt, "realism": False}
        )
        generation_id = response.json()['generation_id']

        # Wait for completion
        while True:
            status = requests.get(f'{BASE_URL}/generations/{generation_id}').json()
            if status['status'] in ['completed', 'failed']:
                return status
            time.sleep(2)

    # Execute in parallel
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(generate_one, prompt): prompt for prompt in prompts}

        for future in as_completed(futures):
            prompt = futures[future]
            try:
                result = future.result()
                print(f"✓ Completed: {prompt}")
                results.append(result)
            except Exception as e:
                print(f"✗ Failed: {prompt} - {e}")

    return results

# Usage
prompts = [
    "warrior character, blue armor",
    "mage character, purple robes",
    "rogue character, leather armor",
]
results = batch_generate(prompts)
print(f"Generated {len(results)} avatars")
```

---

## Integration Examples

### React Integration

```typescript
// hooks/useAvatarGeneration.ts
import { useState, useCallback } from 'react';

interface GenerationStatus {
  generation_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  output_files?: any[];
  error?: string;
}

export function useAvatarGeneration() {
  const [status, setStatus] = useState<GenerationStatus | null>(null);
  const [loading, setLoading] = useState(false);

  const generate = useCallback(async (prompt: string, poseFileId?: string) => {
    setLoading(true);

    try {
      // Start generation
      const response = await fetch(
        'http://localhost:8000/avatarforge-controller/generate/avatar',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt, pose_file_id: poseFileId, realism: false }),
        }
      );

      const data = await response.json();
      setStatus(data);

      // Poll for completion
      const generationId = data.generation_id;
      const pollInterval = setInterval(async () => {
        const statusResponse = await fetch(
          `http://localhost:8000/avatarforge-controller/generations/${generationId}`
        );
        const statusData = await statusResponse.json();
        setStatus(statusData);

        if (statusData.status === 'completed' || statusData.status === 'failed') {
          clearInterval(pollInterval);
          setLoading(false);
        }
      }, 2000);

    } catch (error) {
      console.error('Generation error:', error);
      setLoading(false);
    }
  }, []);

  return { generate, status, loading };
}

// Component usage
function AvatarGenerator() {
  const { generate, status, loading } = useAvatarGeneration();
  const [prompt, setPrompt] = useState('');

  const handleGenerate = () => {
    generate(prompt);
  };

  return (
    <div>
      <input
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter avatar description"
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Avatar'}
      </button>

      {status?.status === 'completed' && status.output_files && (
        <div>
          <h3>Results:</h3>
          {status.output_files.map((file, i) => (
            <img key={i} src={file.url} alt={`Result ${i}`} />
          ))}
        </div>
      )}

      {status?.status === 'failed' && (
        <div style={{color: 'red'}}>Error: {status.error}</div>
      )}
    </div>
  );
}
```

---

### Node.js/Express Integration

```javascript
// server.js
const express = require('express');
const axios = require('axios');
const FormData = require('form-data');
const multer = require('multer');

const app = express();
const upload = multer({ dest: 'uploads/' });

const AVATARFORGE_API = 'http://localhost:8000/avatarforge-controller';

// Endpoint: Upload and generate
app.post('/api/avatar/create', upload.single('pose'), async (req, res) => {
  try {
    const { prompt, clothing, style } = req.body;
    let poseFileId = null;

    // Upload pose if provided
    if (req.file) {
      const formData = new FormData();
      formData.append('file', fs.createReadStream(req.file.path));

      const uploadResponse = await axios.post(
        `${AVATARFORGE_API}/upload/pose_image`,
        formData,
        { headers: formData.getHeaders() }
      );

      poseFileId = uploadResponse.data.file_id;
    }

    // Start generation
    const genResponse = await axios.post(`${AVATARFORGE_API}/generate/avatar`, {
      prompt,
      pose_file_id: poseFileId,
      clothing,
      style,
      realism: false,
    });

    const generationId = genResponse.data.generation_id;

    // Poll for completion
    const pollStatus = async () => {
      const statusResponse = await axios.get(
        `${AVATARFORGE_API}/generations/${generationId}`
      );
      return statusResponse.data;
    };

    // Wait for completion (with timeout)
    let attempts = 0;
    const maxAttempts = 150; // 5 minutes max

    while (attempts < maxAttempts) {
      const status = await pollStatus();

      if (status.status === 'completed') {
        return res.json({
          success: true,
          generation_id: generationId,
          outputs: status.output_files,
        });
      } else if (status.status === 'failed') {
        return res.status(500).json({
          success: false,
          error: status.error,
        });
      }

      await new Promise((resolve) => setTimeout(resolve, 2000));
      attempts++;
    }

    res.status(408).json({ success: false, error: 'Generation timeout' });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

### Python Flask Integration

```python
from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)
AVATARFORGE_API = 'http://localhost:8000/avatarforge-controller'

@app.route('/api/generate', methods=['POST'])
def generate_avatar():
    """Endpoint to generate avatar."""

    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt required'}), 400

    # Start generation
    response = requests.post(
        f'{AVATARFORGE_API}/generate/avatar',
        json={'prompt': prompt, 'realism': False}
    )

    if response.status_code != 200:
        return jsonify({'error': 'Generation failed'}), 500

    generation_id = response.json()['generation_id']

    # Poll for completion
    timeout = 300  # 5 minutes
    start_time = time.time()

    while time.time() - start_time < timeout:
        status_response = requests.get(
            f'{AVATARFORGE_API}/generations/{generation_id}'
        )
        status = status_response.json()

        if status['status'] == 'completed':
            return jsonify({
                'generation_id': generation_id,
                'outputs': status['output_files']
            })
        elif status['status'] == 'failed':
            return jsonify({'error': status.get('error')}), 500

        time.sleep(2)

    return jsonify({'error': 'Timeout'}), 408

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Error Handling

### Common Error Codes

| Status Code | Meaning | Common Cause | Solution |
|-------------|---------|--------------|----------|
| 400 | Bad Request | Invalid payload, missing required fields | Check request body matches schema |
| 404 | Not Found | Invalid file_id or generation_id | Verify IDs are correct |
| 413 | Payload Too Large | File exceeds 50MB | Compress or resize image |
| 422 | Validation Error | Invalid field values | Check error details in response |
| 500 | Internal Server Error | Server-side issue | Check logs, contact support |
| 503 | Service Unavailable | ComfyUI not running | Start ComfyUI backend |

### Error Response Format

```json
{
  "detail": "Validation error message",
  "errors": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Comprehensive Error Handling

```python
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

class AvatarForgeClient:
    """Robust client with error handling."""

    def __init__(self, base_url: str = 'http://localhost:8000/avatarforge-controller'):
        self.base_url = base_url

    def generate_avatar(self, prompt: str, **kwargs):
        """Generate avatar with comprehensive error handling."""

        payload = {'prompt': prompt, **kwargs}

        try:
            response = requests.post(
                f'{self.base_url}/generate/avatar',
                json=payload,
                timeout=30
            )

            # Raise HTTP errors
            response.raise_for_status()

            return response.json()

        except HTTPError as e:
            if e.response.status_code == 400:
                error_detail = e.response.json().get('detail', 'Bad request')
                raise ValueError(f"Invalid request: {error_detail}")
            elif e.response.status_code == 422:
                errors = e.response.json().get('errors', [])
                raise ValueError(f"Validation error: {errors}")
            elif e.response.status_code == 503:
                raise ConnectionError("ComfyUI service unavailable")
            else:
                raise Exception(f"HTTP {e.response.status_code}: {e.response.text}")

        except Timeout:
            raise TimeoutError("Request timed out after 30 seconds")

        except RequestException as e:
            raise ConnectionError(f"Network error: {e}")

    def wait_for_generation(self, generation_id: str, timeout: int = 300):
        """Poll generation with timeout and error handling."""

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    f'{self.base_url}/generations/{generation_id}',
                    timeout=10
                )
                response.raise_for_status()
                status = response.json()

                if status['status'] == 'completed':
                    return status
                elif status['status'] == 'failed':
                    error_msg = status.get('error', 'Unknown error')
                    raise Exception(f"Generation failed: {error_msg}")

                time.sleep(2)

            except HTTPError as e:
                if e.response.status_code == 404:
                    raise ValueError(f"Generation not found: {generation_id}")
                raise

        raise TimeoutError(f"Generation timed out after {timeout}s")

# Usage
client = AvatarForgeClient()

try:
    result = client.generate_avatar(
        prompt="warrior character",
        realism=False
    )
    generation_id = result['generation_id']

    final_status = client.wait_for_generation(generation_id)
    print("Success:", final_status['output_files'])

except ValueError as e:
    print(f"Invalid input: {e}")
except TimeoutError as e:
    print(f"Timeout: {e}")
except ConnectionError as e:
    print(f"Connection issue: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Performance & Optimization

### 1. Minimize Uploads with Hash Checking

```python
def optimized_upload(image_path: str) -> str:
    """Upload only if file doesn't exist."""

    # Calculate hash
    with open(image_path, 'rb') as f:
        content_hash = hashlib.sha256(f.read()).hexdigest()

    # Check existence
    check = requests.get(f'{BASE_URL}/files/hash/{content_hash}')
    if check.json().get('exists'):
        return check.json()['file_id']  # Reuse existing

    # Upload new
    with open(image_path, 'rb') as f:
        upload = requests.post(f'{BASE_URL}/upload/pose_image', files={'file': f})

    return upload.json()['file_id']
```

### 2. Batch Operations

```python
def batch_delete_old_generations(days_old: int = 30):
    """Delete generations older than N days."""

    cutoff_date = datetime.now() - timedelta(days=days_old)

    # Get all generations
    all_gens = get_all_generations()

    deleted = 0
    for gen in all_gens:
        created = datetime.fromisoformat(gen['created_at'].replace('Z', '+00:00'))
        if created < cutoff_date:
            requests.delete(f'{BASE_URL}/generations/{gen["generation_id"]}')
            deleted += 1

    print(f"Deleted {deleted} old generations")
```

### 3. Connection Pooling

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session():
    """Create session with connection pooling and retries."""

    session = requests.Session()

    # Retry strategy
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )

    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=10,
        pool_maxsize=20
    )

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session

# Usage
session = create_session()
response = session.post(f'{BASE_URL}/generate/avatar', json={...})
```

---

## Production Deployment

### Environment Variables for Production

```bash
# .env.production
STORAGE_PATH=/var/avatarforge/storage
MAX_FILE_SIZE=52428800
DATABASE_URL=postgresql://user:pass@localhost/avatarforge
SECRET_KEY=your-production-secret-key-here
COMFYUI_URL=http://localhost:8188
ENABLE_SCHEDULER=true

# CORS (if needed)
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/avatarforge/api.log
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/avatarforge
server {
    listen 80;
    server_name api.yourdomain.com;

    # File upload size limit
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for long-running requests
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
    }

    # Serve uploaded files directly
    location /files/ {
        alias /var/avatarforge/storage/files/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    location /outputs/ {
        alias /var/avatarforge/storage/outputs/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Systemd Service

```ini
# /etc/systemd/system/avatarforge.service
[Unit]
Description=AvatarForge API Service
After=network.target

[Service]
Type=simple
User=avatarforge
WorkingDirectory=/opt/avatarforge
Environment="PATH=/opt/avatarforge/venv/bin"
ExecStart=/opt/avatarforge/venv/bin/uvicorn avatarforge.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create storage directories
RUN mkdir -p storage/files storage/outputs storage/temp

# Initialize database
RUN python -m avatarforge.database.init_db

EXPOSE 8000

CMD ["uvicorn", "avatarforge.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  avatarforge:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./storage:/app/storage
      - ./avatarforge.db:/app/avatarforge.db
    environment:
      - COMFYUI_URL=http://comfyui:8188
      - DATABASE_URL=sqlite:////app/avatarforge.db
    depends_on:
      - comfyui

  comfyui:
    image: comfyui:latest
    ports:
      - "8188:8188"
    volumes:
      - ./comfyui_models:/app/models
```

---

## Summary

This guide covers:
- ✅ All 13 API endpoints with working examples
- ✅ curl, Python, JavaScript/TypeScript examples
- ✅ Common workflows and integration patterns
- ✅ Comprehensive error handling
- ✅ Performance optimization techniques
- ✅ Production deployment configurations

For more details:
- **Swagger UI**: http://localhost:8000/docs
- **Original API Docs**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **GitHub Issues**: Report bugs and request features

---

**Last Updated:** 2025-01-15

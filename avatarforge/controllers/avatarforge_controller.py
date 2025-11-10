"""
AvatarForge Controller - Complete Implementation
=================================================

Provides endpoints for:
- Avatar generation with pose and reference images
- File upload with automatic deduplication
- Generation tracking and management
- File management

All endpoints include comprehensive tooltips and documentation.
"""
import requests
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from ..schemas.avatarforge_schema import (
    AvatarRequest,
    AvatarResponse,
    GenerationListResponse,
    OutputFile
)
from ..schemas.file_schema import (
    FileUploadResponse,
    FileInfo,
    FileHashCheckResponse
)
from ..services.file_service import FileService
from ..services.generation_service import GenerationService
from ..database.session import get_db

router = APIRouter()


# ============================================================================
# FILE UPLOAD ENDPOINTS
# ============================================================================

@router.post(
    "/upload/pose_image",
    response_model=FileUploadResponse,
    summary="Upload Pose Reference Image",
    description="""
    Upload a pose reference image with automatic deduplication.

    **How it works:**
    1. Upload an image file (PNG, JPG, WEBP)
    2. System calculates SHA256 hash of the content
    3. If file already exists (same hash), returns existing file_id
    4. If new, saves file and returns new file_id

    **Use the returned file_id in generation requests:**
    ```json
    {
        "prompt": "warrior character",
        "pose_file_id": "550e8400-e29b-41d4-a716-446655440000"
    }
    ```

    **File Requirements:**
    - Format: PNG, JPG, JPEG, or WEBP
    - Max size: 50MB
    - Dimensions: 64x64 to 4096x4096 pixels

    **Deduplication:**
    If you upload the same image twice, you'll get the same file_id back
    (is_duplicate will be true). This saves storage space and upload time!
    """,
    tags=["File Management"]
)
async def upload_pose_image(
    file: UploadFile = File(..., description="Image file to upload for pose reference"),
    db: Session = Depends(get_db)
) -> FileUploadResponse:
    """Upload a pose reference image with automatic deduplication"""
    file_service = FileService(db)
    uploaded_file = await file_service.upload_file(file, file_type="pose_image")

    # Check if this was a duplicate
    is_duplicate = uploaded_file.reference_count > 0

    return FileUploadResponse(
        file_id=uploaded_file.file_id,
        filename=uploaded_file.filename,
        content_hash=uploaded_file.content_hash,
        size=uploaded_file.size,
        mime_type=uploaded_file.mime_type,
        dimensions={"width": uploaded_file.width, "height": uploaded_file.height},
        url=f"/files/{uploaded_file.file_id}",
        is_duplicate=is_duplicate,
        created_at=uploaded_file.created_at
    )


@router.post(
    "/upload/reference_image",
    response_model=FileUploadResponse,
    summary="Upload Style Reference Image",
    description="""
    Upload a reference image for style matching with automatic deduplication.

    Use this to upload an image that represents the art style or character
    design you want to match. The system will use this as a reference during
    generation.

    **Same deduplication benefits as pose images:**
    - Duplicate detection via SHA256 hash
    - Instant response if file already exists
    - Storage optimization

    See /upload/pose_image for detailed documentation on file requirements.
    """,
    tags=["File Management"]
)
async def upload_reference_image(
    file: UploadFile = File(..., description="Image file to upload for style reference"),
    db: Session = Depends(get_db)
) -> FileUploadResponse:
    """Upload a reference image for style matching"""
    file_service = FileService(db)
    uploaded_file = await file_service.upload_file(file, file_type="reference_image")

    is_duplicate = uploaded_file.reference_count > 0

    return FileUploadResponse(
        file_id=uploaded_file.file_id,
        filename=uploaded_file.filename,
        content_hash=uploaded_file.content_hash,
        size=uploaded_file.size,
        mime_type=uploaded_file.mime_type,
        dimensions={"width": uploaded_file.width, "height": uploaded_file.height},
        url=f"/files/{uploaded_file.file_id}",
        is_duplicate=is_duplicate,
        created_at=uploaded_file.created_at
    )


@router.get(
    "/files/{file_id}",
    response_class=FileResponse,
    summary="Download File by ID",
    description="""
    Download a previously uploaded file by its ID.

    **Usage:**
    - Get file_id from upload response
    - Use this endpoint to download or display the file
    - Files are served with appropriate MIME types

    **Returns:** The actual file content (image)
    """,
    tags=["File Management"]
)
async def get_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve an uploaded file by ID"""
    file_service = FileService(db)
    uploaded_file = file_service.get_file_by_id(file_id)

    if not uploaded_file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = file_service.get_file_path(uploaded_file)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=str(file_path),
        media_type=uploaded_file.mime_type,
        filename=uploaded_file.filename
    )


@router.get(
    "/files/hash/{content_hash}",
    response_model=FileHashCheckResponse,
    summary="Check if File Hash Exists",
    description="""
    Check if a file with a specific SHA256 hash already exists.

    **Use Case:**
    Before uploading a large file, you can calculate its hash locally
    and check if it already exists. If it does, you can skip the upload
    and use the existing file_id!

    **Example Workflow:**
    1. Calculate SHA256 hash of your file locally
    2. GET /files/hash/{hash}
    3. If exists=true, use the returned file_id
    4. If exists=false, proceed with upload

    **Hash Calculation (Python):**
    ```python
    import hashlib
    with open('image.png', 'rb') as f:
        hash = hashlib.sha256(f.read()).hexdigest()
    ```
    """,
    tags=["File Management"]
)
async def check_file_hash(
    content_hash: str,
    db: Session = Depends(get_db)
) -> FileHashCheckResponse:
    """Check if a file with the given hash exists"""
    file_service = FileService(db)
    existing_file = file_service.get_file_by_hash(content_hash)

    if existing_file:
        return FileHashCheckResponse(
            exists=True,
            file_id=existing_file.file_id,
            message=f"File exists: {existing_file.filename}"
        )
    else:
        return FileHashCheckResponse(
            exists=False,
            file_id=None,
            message="File does not exist"
        )


@router.delete(
    "/files/{file_id}",
    summary="Delete File",
    description="""
    Delete a file (soft delete if still referenced by generations).

    **Behavior:**
    - If file is used by active generations: Soft delete (marked as deleted)
    - If file has no references: Hard delete (removed from disk)
    - Returns error if file is still actively referenced

    **Force Delete:**
    Use force=true query parameter to delete regardless (use with caution!)
    """,
    tags=["File Management"]
)
async def delete_file(
    file_id: str,
    force: bool = Query(False, description="Force delete even if referenced"),
    db: Session = Depends(get_db)
):
    """Delete an uploaded file"""
    file_service = FileService(db)

    try:
        deleted = file_service.delete_file(file_id, force=force)
        if deleted:
            return {"message": "File deleted successfully", "file_id": file_id}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# GENERATION ENDPOINTS
# ============================================================================

@router.post(
    "/generate/avatar",
    response_model=AvatarResponse,
    summary="Generate Avatar",
    description="""
    Generate an avatar from a text prompt with optional pose and reference images.

    **Two Ways to Provide Images:**

    1. **Recommended: Use uploaded file IDs**
       ```json
       {
           "prompt": "warrior character, blue armor",
           "pose_file_id": "550e8400-e29b-41d4-a716-446655440000",
           "reference_file_id": "660e8400-e29b-41d4-a716-446655440000",
           "realism": false
       }
       ```
       Benefits: Deduplication, faster, better tracking

    2. **Legacy: Use base64 strings**
       ```json
       {
           "prompt": "warrior character",
           "pose_image": "data:image/png;base64,iVBORw0KG...",
           "realism": false
       }
       ```
       Still supported for backward compatibility

    **Workflow:**
    1. (Optional) Upload pose/reference images first
    2. POST to this endpoint with prompt and file IDs
    3. Receive generation_id in response
    4. Poll GET /generations/{id} to check status
    5. Download results when status='completed'

    **Parameters Explained:**
    - **prompt**: Describe what you want (required)
    - **clothing**: Add specific outfit details (optional)
    - **style**: Art style modifier like 'watercolor', 'pixel art' (optional)
    - **realism**: true=photorealistic, false=anime/stylized (default: false)
    - **pose_file_id**: ID from /upload/pose_image (optional)
    - **reference_file_id**: ID from /upload/reference_image (optional)
    """,
    tags=["Avatar Generation"]
)
async def generate_avatar(
    request: AvatarRequest,
    db: Session = Depends(get_db)
) -> AvatarResponse:
    """Generate an avatar with full customization options"""
    gen_service = GenerationService(db)

    # Create generation record
    generation = gen_service.create_generation(
        prompt=request.prompt,
        clothing=request.clothing,
        style=request.style,
        realism=request.realism,
        pose_file_id=request.pose_file_id,
        reference_file_id=request.reference_file_id,
        pose_image=request.pose_image,
        reference_image=request.reference_image
    )

    # Execute generation
    try:
        gen_service.execute_generation(generation.generation_id)
    except HTTPException:
        # Generation failed, but record exists
        pass

    # Return generation info
    return AvatarResponse(
        generation_id=generation.generation_id,
        status=generation.status,
        message=f"Generation {generation.status}",
        created_at=generation.created_at,
        started_at=generation.started_at,
        completed_at=generation.completed_at,
        error=generation.error_message,
        comfyui_prompt_id=generation.comfyui_prompt_id
    )


@router.post(
    "/generate_pose",
    response_model=AvatarResponse,
    summary="Generate Specific Pose",
    description="""
    Generate an avatar in a specific pose view.

    **Available Poses:**
    - **front**: Front-facing view, standard proportions
    - **back**: Back view, different lighting emphasis
    - **side**: Side profile, narrow aspect ratio
    - **quarter**: 3/4 view, partial features

    **Usage:**
    ```
    POST /generate_pose?pose=front
    {
        "prompt": "warrior character, blue armor",
        "realism": false
    }
    ```

    Each pose type uses a different model optimized for that viewpoint.
    See /generate/avatar for full parameter documentation.
    """,
    tags=["Avatar Generation"]
)
async def generate_pose(
    pose: str = Query(..., description="Pose type: front, back, side, or quarter"),
    request: AvatarRequest = None,
    db: Session = Depends(get_db)
) -> AvatarResponse:
    """Generate an avatar with a specific pose"""
    if pose not in ["front", "back", "side", "quarter"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid pose: {pose}. Must be one of: front, back, side, quarter"
        )

    gen_service = GenerationService(db)

    generation = gen_service.create_generation(
        prompt=request.prompt,
        clothing=request.clothing,
        style=request.style,
        realism=request.realism,
        pose_type=pose,
        pose_file_id=request.pose_file_id,
        reference_file_id=request.reference_file_id,
        pose_image=request.pose_image,
        reference_image=request.reference_image
    )

    try:
        gen_service.execute_generation(generation.generation_id)
    except HTTPException:
        pass

    return AvatarResponse(
        generation_id=generation.generation_id,
        status=generation.status,
        message=f"Generation {generation.status} for pose: {pose}",
        created_at=generation.created_at,
        started_at=generation.started_at,
        completed_at=generation.completed_at,
        error=generation.error_message,
        comfyui_prompt_id=generation.comfyui_prompt_id
    )


@router.post(
    "/generate_all_poses",
    response_model=AvatarResponse,
    summary="Generate All Pose Views",
    description="""
    Generate avatars in all pose views (front, back, side, quarter) at once.

    **Perfect for:**
    - Character sheets
    - Game asset creation
    - Complete character references

    **Returns:**
    A single generation that produces 4 images (one for each pose).
    All images maintain consistent character appearance across views.

    **Note:** This takes longer than single pose generation as it creates
    4 separate images. Check status with GET /generations/{id}.
    """,
    tags=["Avatar Generation"]
)
async def generate_all_poses(
    request: AvatarRequest,
    db: Session = Depends(get_db)
) -> AvatarResponse:
    """Generate an avatar with all pose views"""
    gen_service = GenerationService(db)

    generation = gen_service.create_generation(
        prompt=request.prompt,
        clothing=request.clothing,
        style=request.style,
        realism=request.realism,
        pose_type="all",
        pose_file_id=request.pose_file_id,
        reference_file_id=request.reference_file_id,
        pose_image=request.pose_image,
        reference_image=request.reference_image
    )

    try:
        gen_service.execute_generation(generation.generation_id)
    except HTTPException:
        pass

    return AvatarResponse(
        generation_id=generation.generation_id,
        status=generation.status,
        message="Generating all poses (front, back, side, quarter)",
        created_at=generation.created_at,
        started_at=generation.started_at,
        completed_at=generation.completed_at,
        error=generation.error_message,
        comfyui_prompt_id=generation.comfyui_prompt_id
    )


# ============================================================================
# GENERATION MANAGEMENT ENDPOINTS
# ============================================================================

@router.get(
    "/generations/{generation_id}",
    response_model=AvatarResponse,
    summary="Get Generation Status",
    description="""
    Check the status of a generation and get results when complete.

    **Status Values:**
    - **queued**: Waiting to start
    - **processing**: Currently generating
    - **completed**: Done! Results available in output_files
    - **failed**: Error occurred, see error field

    **Polling Pattern:**
    ```python
    while True:
        response = requests.get(f"/generations/{generation_id}")
        if response.json()["status"] in ["completed", "failed"]:
            break
        time.sleep(2)  # Wait 2 seconds between checks
    ```

    **When Completed:**
    The response will include output_files with download URLs.
    """,
    tags=["Generation Management"]
)
async def get_generation(
    generation_id: str,
    db: Session = Depends(get_db)
) -> AvatarResponse:
    """Get generation status and results"""
    gen_service = GenerationService(db)
    generation = gen_service.get_generation(generation_id)

    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")

    # Parse output files if available
    output_files = None
    if generation.output_files:
        output_files = [OutputFile(**f) for f in generation.output_files]

    return AvatarResponse(
        generation_id=generation.generation_id,
        status=generation.status,
        message=f"Generation {generation.status}",
        workflow=generation.workflow if generation.workflow else None,
        output_files=output_files,
        created_at=generation.created_at,
        started_at=generation.started_at,
        completed_at=generation.completed_at,
        error=generation.error_message,
        comfyui_prompt_id=generation.comfyui_prompt_id
    )


@router.get(
    "/generations",
    response_model=GenerationListResponse,
    summary="List Generations",
    description="""
    List all generations with optional filtering.

    **Query Parameters:**
    - **limit**: Max results per page (default: 50, max: 100)
    - **offset**: Skip this many results (for pagination)
    - **status**: Filter by status (queued, processing, completed, failed)

    **Pagination Example:**
    ```
    # Page 1
    GET /generations?limit=10&offset=0

    # Page 2
    GET /generations?limit=10&offset=10

    # Only completed
    GET /generations?status=completed
    ```
    """,
    tags=["Generation Management"]
)
async def list_generations(
    limit: int = Query(50, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
) -> GenerationListResponse:
    """List generations with pagination and filtering"""
    gen_service = GenerationService(db)

    generations = gen_service.list_generations(
        limit=limit,
        offset=offset,
        status=status
    )

    # Get total count
    total_query = db.query(Generation)
    if status:
        from ..models.generation import Generation
        total_query = total_query.filter(Generation.status == status)
    total = total_query.count()

    # Convert to response models
    generation_responses = []
    for gen in generations:
        output_files = None
        if gen.output_files:
            output_files = [OutputFile(**f) for f in gen.output_files]

        generation_responses.append(AvatarResponse(
            generation_id=gen.generation_id,
            status=gen.status,
            message=f"Generation {gen.status}",
            output_files=output_files,
            created_at=gen.created_at,
            started_at=gen.started_at,
            completed_at=gen.completed_at,
            error=gen.error_message,
            comfyui_prompt_id=gen.comfyui_prompt_id
        ))

    return GenerationListResponse(
        total=total,
        generations=generation_responses,
        limit=limit,
        offset=offset
    )


@router.delete(
    "/generations/{generation_id}",
    summary="Delete Generation",
    description="""
    Delete a generation and decrement file references.

    **What Happens:**
    1. Generation record is deleted from database
    2. File reference counts are decremented
    3. Files with zero references become eligible for cleanup

    **Note:** This does NOT delete the output files, only the generation
    record. Output files can be cleaned up separately.
    """,
    tags=["Generation Management"]
)
async def delete_generation(
    generation_id: str,
    db: Session = Depends(get_db)
):
    """Delete a generation"""
    gen_service = GenerationService(db)
    deleted = gen_service.delete_generation(generation_id)

    if deleted:
        return {"message": "Generation deleted", "generation_id": generation_id}
    else:
        raise HTTPException(status_code=404, detail="Generation not found")


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get(
    "/health",
    summary="Health Check",
    description="""
    Check the health of AvatarForge API and ComfyUI backend.

    **Returns:**
    - API status (always "healthy" if you get a response)
    - ComfyUI connection status
    - ComfyUI system stats (if available)

    **Use this to:**
    - Verify API is running
    - Check if ComfyUI backend is accessible
    - Monitor system resources
    """,
    tags=["Utility"]
)
async def health_check(db: Session = Depends(get_db)):
    """Health check for API and ComfyUI"""
    gen_service = GenerationService(db)
    comfyui_health = gen_service.check_comfyui_health()

    return {
        "api_status": "healthy",
        "comfyui": comfyui_health
    }


@router.get(
    "/poses",
    summary="List Available Poses",
    description="""
    Get a list of all supported pose types.

    **Returns:**
    List of pose types with descriptions for each.
    Use these values in the 'pose' query parameter for /generate_pose.
    """,
    tags=["Utility"]
)
async def list_poses():
    """List all available pose types"""
    return {
        "poses": [
            {
                "name": "front",
                "description": "Front-facing view with standard proportions and full body visibility"
            },
            {
                "name": "back",
                "description": "Back view with emphasis on rear features and different lighting"
            },
            {
                "name": "side",
                "description": "Side profile view with narrow aspect ratio"
            },
            {
                "name": "quarter",
                "description": "3/4 view showing partial features from an angle"
            }
        ]
    }

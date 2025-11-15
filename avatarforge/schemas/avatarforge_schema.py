"""AvatarForge request and response schemas"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime


class AvatarRequest(BaseModel):
    """
    Avatar generation request model (supports both legacy base64 and new file_id approach)

    Examples:
        Basic anime character:
        {
            "prompt": "female warrior, blue armor, long white hair",
            "realism": false
        }

        Using uploaded file ID (recommended):
        {
            "prompt": "male business professional, suit and tie, confident expression",
            "pose_file_id": "550e8400-e29b-41d4-a716-446655440000",
            "realism": true
        }

        Legacy base64 support:
        {
            "prompt": "cyberpunk hacker, neon colors",
            "pose_image": "base64_encoded_image_or_url",
            "clothing": "hoodie, tactical vest, cargo pants",
            "realism": false
        }
    """
    prompt: str = Field(
        ...,
        description="Detailed text description of the avatar. Examples: 'female mage with purple robes', 'muscular warrior with sword', 'elegant elf archer'",
        min_length=3,
        examples=[
            "female warrior, blue armor, long white hair, fantasy style",
            "male business professional, suit and tie, confident expression",
            "cyberpunk character, neon hair, tech implants, futuristic outfit"
        ]
    )

    # New file ID approach (recommended)
    pose_file_id: Optional[str] = Field(
        None,
        description="ID of uploaded pose reference image. Upload files via POST /upload/pose_image first, then use the returned file_id here. This approach supports automatic deduplication."
    )

    reference_file_id: Optional[str] = Field(
        None,
        description="ID of uploaded reference image for style matching. Upload files via POST /upload/reference_image first, then use the returned file_id here."
    )

    # Legacy base64 support (for backward compatibility)
    pose_image: Optional[str] = Field(
        None,
        description="[LEGACY] Base64 encoded image or file path for pose reference. For new integrations, prefer using pose_file_id instead. Accepts: base64 string, local file path, or URL"
    )

    reference_image: Optional[str] = Field(
        None,
        description="[LEGACY] Base64 encoded reference image for character appearance/style. For new integrations, prefer using reference_file_id instead."
    )

    clothing: Optional[str] = Field(
        None,
        description="Specific clothing details to add to the avatar. Examples: 'leather jacket, jeans', 'medieval armor, cape', 'casual t-shirt and shorts'",
        examples=[
            "leather jacket, ripped jeans, combat boots",
            "medieval plate armor, red cape, crown",
            "casual hoodie, track pants, sneakers"
        ]
    )

    realism: bool = Field(
        False,
        description="Toggle between realistic (True) and anime/stylized (False) rendering style. True = photorealistic, False = anime/cartoon style"
    )

    style: Optional[str] = Field(
        None,
        description="Art style modifier. Examples: 'cel-shaded', 'watercolor', 'oil painting', 'pixel art', 'comic book'",
        examples=["cel-shaded", "watercolor", "oil painting", "pixel art", "comic book", "sketch"]
    )


class OutputFile(BaseModel):
    """Information about a generated output file"""
    filename: str = Field(..., description="Name of the generated file")
    url: str = Field(..., description="URL to download the file")
    pose_type: Optional[str] = Field(None, description="Pose type if applicable: 'front', 'back', 'side', 'quarter'")
    size: int = Field(..., description="File size in bytes")
    dimensions: Optional[Dict[str, int]] = Field(None, description="Image dimensions", json_schema_extra={"example": {"width": 512, "height": 512}})


class AvatarResponse(BaseModel):
    """Enhanced avatar generation response model"""
    generation_id: str = Field(..., description="Unique generation ID for tracking")
    status: str = Field(..., description="Generation status: 'queued', 'processing', 'completed', 'failed'")
    message: str = Field(..., description="Human-readable status message")
    workflow: Optional[Dict[str, Any]] = Field(None, description="ComfyUI workflow JSON (only included if requested)")
    output_files: Optional[List[OutputFile]] = Field(None, description="Generated output files (only when status='completed')")
    created_at: datetime = Field(..., description="When the generation was created")
    started_at: Optional[datetime] = Field(None, description="When processing started")
    completed_at: Optional[datetime] = Field(None, description="When processing completed")
    error: Optional[str] = Field(None, description="Error message if status='failed'")
    comfyui_prompt_id: Optional[str] = Field(None, description="ComfyUI's internal prompt ID")

    model_config = ConfigDict(from_attributes=True)


class GenerationListResponse(BaseModel):
    """Response for listing generations"""
    total: int = Field(..., description="Total number of generations matching filter")
    generations: List[AvatarResponse] = Field(..., description="List of generation records")
    limit: int = Field(..., description="Number of results per page")
    offset: int = Field(..., description="Number of results skipped")

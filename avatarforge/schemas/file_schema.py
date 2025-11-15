"""File upload and management schemas"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from datetime import datetime


class FileUploadResponse(BaseModel):
    """
    Response model for file uploads

    Contains file metadata and deduplication information
    """
    file_id: str = Field(
        ...,
        description="Unique file identifier (UUID). Use this ID in generation requests."
    )
    filename: str = Field(
        ...,
        description="Original filename from upload"
    )
    content_hash: str = Field(
        ...,
        description="SHA256 hash of file content. Used for deduplication."
    )
    size: int = Field(
        ...,
        description="File size in bytes"
    )
    mime_type: str = Field(
        ...,
        description="MIME type (e.g., 'image/png', 'image/jpeg')"
    )
    dimensions: Dict[str, int] = Field(
        ...,
        description="Image dimensions in pixels",
        json_schema_extra={"example": {"width": 512, "height": 512}}
    )
    url: str = Field(
        ...,
        description="URL to access the uploaded file"
    )
    is_duplicate: bool = Field(
        ...,
        description="True if this file already existed (deduplication). False if newly uploaded."
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when file was first uploaded"
    )

    model_config = ConfigDict(from_attributes=True)


class FileInfo(BaseModel):
    """Basic file information"""
    file_id: str
    filename: str
    content_hash: str
    size: int
    mime_type: str
    width: Optional[int]
    height: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FileHashCheckResponse(BaseModel):
    """Response for hash existence check"""
    exists: bool = Field(
        ...,
        description="True if a file with this hash already exists"
    )
    file_id: Optional[str] = Field(
        None,
        description="File ID if exists, null otherwise"
    )
    message: str = Field(
        ...,
        description="Human-readable message"
    )


class CleanupResponse(BaseModel):
    """Response for cleanup operation"""
    files_deleted: int = Field(
        ...,
        description="Number of files permanently deleted"
    )
    cleanup_days: int = Field(
        ...,
        description="Files older than this many days were deleted"
    )
    message: str = Field(
        ...,
        description="Summary message"
    )

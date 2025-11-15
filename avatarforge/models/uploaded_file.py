"""Database model for uploaded files with deduplication support"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from ..database.base import Base


class UploadedFile(Base):
    """
    Tracks uploaded files with content-based deduplication

    Attributes:
        file_id: Unique identifier (UUID)
        filename: Original filename from upload
        content_hash: SHA256 hash of file content (for deduplication)
        file_type: Type of file ('pose_image', 'reference_image', 'output')
        mime_type: MIME type (image/png, image/jpeg, etc.)
        size: File size in bytes
        width: Image width in pixels
        height: Image height in pixels
        storage_path: Relative path in storage system
        reference_count: Number of generations using this file
        user_id: User who uploaded the file (nullable for backward compatibility)
        created_at: Upload timestamp
        last_accessed: Last time file was used
        is_deleted: Soft delete flag
    """
    __tablename__ = "uploaded_files"

    file_id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    content_hash = Column(String, nullable=False, index=True, unique=True)
    file_type = Column(String, nullable=False)  # 'pose_image', 'reference_image', 'output'
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    storage_path = Column(String, nullable=False)
    reference_count = Column(Integer, default=0)
    user_id = Column(String, nullable=True, index=True)  # User who uploaded the file
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"<UploadedFile(file_id={self.file_id}, filename={self.filename}, hash={self.content_hash[:8]}...)>"

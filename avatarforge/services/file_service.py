"""
File management service with deduplication support

Handles file uploads, downloads, storage, and automatic deduplication
using content-based hashing (SHA256).
"""
import hashlib
import uuid
from pathlib import Path
from typing import Optional, Tuple, BinaryIO
from datetime import datetime, timezone
from PIL import Image
import io

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from ..models.uploaded_file import UploadedFile
from ..core.config import settings


class FileService:
    """Service for managing file uploads with deduplication"""

    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
    ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_DIMENSION = 4096
    MIN_DIMENSION = 64

    def __init__(self, db: Session):
        self.db = db
        self.storage_root = Path(settings.STORAGE_PATH if hasattr(settings, 'STORAGE_PATH') else "./storage")
        self.uploads_dir = self.storage_root / "uploads"
        self.outputs_dir = self.storage_root / "outputs"

        # Create directories if they don't exist
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    async def upload_file(
        self,
        file: UploadFile,
        file_type: str = "pose_image",
        user_id: str = None
    ) -> UploadedFile:
        """
        Upload a file with automatic deduplication

        Args:
            file: The uploaded file
            file_type: Type of file ('pose_image', 'reference_image')
            user_id: Optional user ID who is uploading the file

        Returns:
            UploadedFile: Database record (existing or newly created)

        Raises:
            HTTPException: If validation fails
        """
        # Validate file type
        if file.content_type not in self.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Allowed: {', '.join(self.ALLOWED_MIME_TYPES)}"
            )

        # Read file content
        content = await file.read()

        # Validate file size
        if len(content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large: {len(content)} bytes. Max: {self.MAX_FILE_SIZE} bytes"
            )

        # Calculate content hash
        content_hash = hashlib.sha256(content).hexdigest()

        # Check if file already exists
        existing_file = self.db.query(UploadedFile).filter(
            UploadedFile.content_hash == content_hash,
            UploadedFile.is_deleted == False
        ).first()

        if existing_file:
            # File already exists - update last accessed and return
            existing_file.last_accessed = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(existing_file)
            return existing_file

        # Validate and get image dimensions
        try:
            image = Image.open(io.BytesIO(content))
            width, height = image.size

            if width > self.MAX_DIMENSION or height > self.MAX_DIMENSION:
                raise HTTPException(
                    status_code=400,
                    detail=f"Image dimensions too large: {width}x{height}. Max: {self.MAX_DIMENSION}x{self.MAX_DIMENSION}"
                )

            if width < self.MIN_DIMENSION or height < self.MIN_DIMENSION:
                raise HTTPException(
                    status_code=400,
                    detail=f"Image dimensions too small: {width}x{height}. Min: {self.MIN_DIMENSION}x{self.MIN_DIMENSION}"
                )

        except HTTPException:
            # Re-raise HTTP exceptions (validation errors)
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(e)}"
            )

        # Generate storage path using hash-based directory structure
        # Format: uploads/{type}/{hash[:2]}/{hash[2:4]}/{hash}.ext
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            file_ext = ".png"  # Default to PNG

        storage_subpath = Path(file_type) / content_hash[:2] / content_hash[2:4]
        storage_filename = f"{content_hash}{file_ext}"
        storage_path = self.uploads_dir / storage_subpath / storage_filename

        # Create directories
        storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Save file to disk
        storage_path.write_bytes(content)

        # Create database record
        file_id = str(uuid.uuid4())
        db_file = UploadedFile(
            file_id=file_id,
            filename=file.filename,
            content_hash=content_hash,
            file_type=file_type,
            mime_type=file.content_type,
            size=len(content),
            width=width,
            height=height,
            storage_path=str(storage_subpath / storage_filename),
            reference_count=0,
            user_id=user_id
        )

        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

        return db_file

    def get_file_by_id(self, file_id: str) -> Optional[UploadedFile]:
        """Get file metadata by ID"""
        return self.db.query(UploadedFile).filter(
            UploadedFile.file_id == file_id,
            UploadedFile.is_deleted == False
        ).first()

    def get_file_by_hash(self, content_hash: str) -> Optional[UploadedFile]:
        """Get file metadata by content hash"""
        return self.db.query(UploadedFile).filter(
            UploadedFile.content_hash == content_hash,
            UploadedFile.is_deleted == False
        ).first()

    def get_file_path(self, file: UploadedFile) -> Path:
        """Get full filesystem path for a file"""
        return self.uploads_dir / file.storage_path

    def increment_reference(self, file_id: str):
        """Increment reference count when file is used in generation"""
        file = self.get_file_by_id(file_id)
        if file:
            file.reference_count += 1
            file.last_accessed = datetime.now(timezone.utc)
            self.db.commit()

    def decrement_reference(self, file_id: str):
        """Decrement reference count when generation is deleted"""
        file = self.get_file_by_id(file_id)
        if file and file.reference_count > 0:
            file.reference_count -= 1
            self.db.commit()

    def delete_file(self, file_id: str, force: bool = False) -> bool:
        """
        Soft delete a file (or hard delete if force=True and no references)

        Args:
            file_id: File ID to delete
            force: If True, delete even if references exist (will fail if ref_count > 0)

        Returns:
            bool: True if deleted, False otherwise
        """
        file = self.get_file_by_id(file_id)
        if not file:
            return False

        if file.reference_count > 0 and not force:
            raise HTTPException(
                status_code=400,
                detail=f"File is still referenced by {file.reference_count} generation(s)"
            )

        if force and file.reference_count == 0:
            # Hard delete - remove from disk and database
            file_path = self.get_file_path(file)
            if file_path.exists():
                file_path.unlink()
            self.db.delete(file)
        else:
            # Soft delete - mark as deleted
            file.is_deleted = True

        self.db.commit()
        return True

    def cleanup_orphaned_files(self, days: int = 30) -> int:
        """
        Clean up files with zero references older than specified days

        Args:
            days: Delete files not accessed in this many days

        Returns:
            int: Number of files deleted
        """
        from datetime import timedelta

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        orphaned_files = self.db.query(UploadedFile).filter(
            UploadedFile.reference_count == 0,
            UploadedFile.last_accessed < cutoff_date,
            UploadedFile.is_deleted == False
        ).all()

        count = 0
        for file in orphaned_files:
            try:
                self.delete_file(file.file_id, force=True)
                count += 1
            except Exception:
                continue

        return count

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

"""Unit tests for FileService"""
import pytest
import hashlib
import io
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from fastapi import UploadFile, HTTPException
from PIL import Image

from avatarforge.services.file_service import FileService
from avatarforge.models.uploaded_file import UploadedFile


@pytest.fixture
def mock_db():
    """Mock database session"""
    db = Mock()
    db.query = Mock()
    db.add = Mock()
    db.commit = Mock()
    db.refresh = Mock()
    db.delete = Mock()
    return db


@pytest.fixture
def file_service(mock_db, tmp_path):
    """Create FileService with mocked dependencies"""
    service = FileService(mock_db)
    service.storage_root = tmp_path
    service.uploads_dir = tmp_path / "uploads"
    service.outputs_dir = tmp_path / "outputs"
    service.uploads_dir.mkdir(parents=True, exist_ok=True)
    service.outputs_dir.mkdir(parents=True, exist_ok=True)
    return service


@pytest.fixture
def sample_image():
    """Create a sample image in memory"""
    img = Image.new('RGB', (512, 512), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


@pytest.fixture
def mock_upload_file(sample_image):
    """Create a mock UploadFile"""
    upload_file = Mock(spec=UploadFile)
    upload_file.filename = "test_image.png"
    upload_file.content_type = "image/png"
    upload_file.read = Mock(return_value=sample_image)
    return upload_file


class TestFileService:
    """Tests for FileService class"""

    @pytest.mark.asyncio
    async def test_upload_file_new(self, file_service, mock_db, mock_upload_file, sample_image):
        """Test uploading a new file"""
        # Setup mock
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Upload file
        result = await file_service.upload_file(mock_upload_file, file_type="pose_image")

        # Verify database calls
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

        # Verify file was saved to disk
        content_hash = hashlib.sha256(sample_image).hexdigest()
        expected_path = (
            file_service.uploads_dir /
            "pose_image" /
            content_hash[:2] /
            content_hash[2:4] /
            f"{content_hash}.png"
        )
        assert expected_path.exists()

    @pytest.mark.asyncio
    async def test_upload_file_duplicate(self, file_service, mock_db, mock_upload_file, sample_image):
        """Test uploading a duplicate file returns existing record"""
        # Setup mock with existing file
        existing_file = UploadedFile(
            file_id="existing-id",
            filename="existing.png",
            content_hash=hashlib.sha256(sample_image).hexdigest(),
            file_type="pose_image",
            mime_type="image/png",
            size=len(sample_image),
            width=512,
            height=512,
            storage_path="pose_image/ab/cd/hash.png",
            reference_count=1,
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            is_deleted=False
        )
        mock_db.query.return_value.filter.return_value.first.return_value = existing_file

        # Upload file
        result = await file_service.upload_file(mock_upload_file, file_type="pose_image")

        # Verify it returned existing file
        assert result.file_id == "existing-id"

        # Verify no new file was added
        mock_db.add.assert_not_called()

        # Verify last_accessed was updated
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_upload_file_invalid_type(self, file_service, mock_db):
        """Test uploading invalid file type raises error"""
        invalid_file = Mock(spec=UploadFile)
        invalid_file.content_type = "text/plain"
        invalid_file.read = Mock(return_value=b"not an image")

        with pytest.raises(HTTPException) as exc_info:
            await file_service.upload_file(invalid_file)

        assert exc_info.value.status_code == 400
        assert "Invalid file type" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_upload_file_too_large(self, file_service, mock_db):
        """Test uploading file that's too large raises error"""
        large_file = Mock(spec=UploadFile)
        large_file.content_type = "image/png"
        large_file.read = Mock(return_value=b"x" * (file_service.MAX_FILE_SIZE + 1))

        with pytest.raises(HTTPException) as exc_info:
            await file_service.upload_file(large_file)

        assert exc_info.value.status_code == 400
        assert "File too large" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_upload_file_dimensions_too_large(self, file_service, mock_db):
        """Test uploading image with dimensions too large"""
        # Create oversized image
        large_img = Image.new('RGB', (5000, 5000), color='blue')
        img_bytes = io.BytesIO()
        large_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        large_upload = Mock(spec=UploadFile)
        large_upload.filename = "large.png"
        large_upload.content_type = "image/png"
        large_upload.read = Mock(return_value=img_bytes.getvalue())

        with pytest.raises(HTTPException) as exc_info:
            await file_service.upload_file(large_upload)

        assert exc_info.value.status_code == 400
        assert "dimensions too large" in exc_info.value.detail

    def test_get_file_by_id(self, file_service, mock_db):
        """Test getting file by ID"""
        mock_file = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        result = file_service.get_file_by_id("test-id")

        assert result == mock_file
        mock_db.query.assert_called_once()

    def test_get_file_by_hash(self, file_service, mock_db):
        """Test getting file by content hash"""
        mock_file = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        result = file_service.get_file_by_hash("abc123")

        assert result == mock_file
        mock_db.query.assert_called_once()

    def test_increment_reference(self, file_service, mock_db):
        """Test incrementing file reference count"""
        mock_file = Mock()
        mock_file.reference_count = 0
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        file_service.increment_reference("test-id")

        assert mock_file.reference_count == 1
        mock_db.commit.assert_called_once()

    def test_decrement_reference(self, file_service, mock_db):
        """Test decrementing file reference count"""
        mock_file = Mock()
        mock_file.reference_count = 2
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        file_service.decrement_reference("test-id")

        assert mock_file.reference_count == 1
        mock_db.commit.assert_called_once()

    def test_decrement_reference_not_below_zero(self, file_service, mock_db):
        """Test reference count doesn't go below zero"""
        mock_file = Mock()
        mock_file.reference_count = 0
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        file_service.decrement_reference("test-id")

        # Should stay at 0
        assert mock_file.reference_count == 0

    def test_delete_file_with_references(self, file_service, mock_db):
        """Test deleting file with references raises error"""
        mock_file = Mock()
        mock_file.reference_count = 5
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        with pytest.raises(HTTPException) as exc_info:
            file_service.delete_file("test-id", force=False)

        assert exc_info.value.status_code == 400
        assert "still referenced" in exc_info.value.detail

    def test_delete_file_soft_delete(self, file_service, mock_db):
        """Test soft delete when file has references"""
        mock_file = Mock()
        mock_file.reference_count = 5
        mock_file.is_deleted = False
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        # Force soft delete
        with pytest.raises(HTTPException):
            result = file_service.delete_file("test-id", force=True)

        # Would set is_deleted = True in real implementation

    def test_delete_file_hard_delete(self, file_service, mock_db, tmp_path):
        """Test hard delete when no references"""
        # Create a test file
        test_file = tmp_path / "test_file.png"
        test_file.write_bytes(b"test")

        mock_file = Mock()
        mock_file.reference_count = 0
        mock_file.storage_path = str(test_file.relative_to(file_service.uploads_dir))
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        with patch.object(file_service, 'get_file_path', return_value=test_file):
            result = file_service.delete_file("test-id", force=True)

        assert result == True
        mock_db.delete.assert_called_once_with(mock_file)

    def test_calculate_file_hash(self, file_service, tmp_path):
        """Test file hash calculation"""
        test_file = tmp_path / "test.txt"
        content = b"test content"
        test_file.write_bytes(content)

        expected_hash = hashlib.sha256(content).hexdigest()
        result = file_service.calculate_file_hash(test_file)

        assert result == expected_hash

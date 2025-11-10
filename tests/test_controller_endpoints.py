"""Integration tests for controller endpoints"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import io
from PIL import Image

from backend.main import app
from avatarforge.database.session import get_db


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    db = Mock()
    db.query = Mock()
    db.add = Mock()
    db.commit = Mock()
    db.refresh = Mock()
    return db


@pytest.fixture
def override_get_db(mock_db_session):
    """Override database dependency"""
    def _get_db():
        try:
            yield mock_db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def sample_image_file():
    """Create a sample image file for upload"""
    img = Image.new('RGB', (512, 512), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return ("test.png", img_bytes, "image/png")


class TestFileUploadEndpoints:
    """Tests for file upload endpoints"""

    @patch('avatarforge.services.file_service.FileService.upload_file')
    def test_upload_pose_image(self, mock_upload, client, override_get_db, sample_image_file):
        """Test POST /upload/pose_image"""
        # Mock upload response
        mock_file = Mock()
        mock_file.file_id = "test-file-id"
        mock_file.filename = "test.png"
        mock_file.content_hash = "abc123"
        mock_file.size = 1024
        mock_file.mime_type = "image/png"
        mock_file.width = 512
        mock_file.height = 512
        mock_file.created_at = "2025-01-01T00:00:00"
        mock_file.reference_count = 0
        mock_upload.return_value = mock_file

        response = client.post(
            "/avatarforge-controller/upload/pose_image",
            files={"file": sample_image_file}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["file_id"] == "test-file-id"
        assert data["is_duplicate"] == False

    @patch('avatarforge.services.file_service.FileService.upload_file')
    def test_upload_reference_image(self, mock_upload, client, override_get_db, sample_image_file):
        """Test POST /upload/reference_image"""
        mock_file = Mock()
        mock_file.file_id = "ref-file-id"
        mock_file.filename = "ref.png"
        mock_file.content_hash = "def456"
        mock_file.size = 2048
        mock_file.mime_type = "image/png"
        mock_file.width = 512
        mock_file.height = 512
        mock_file.created_at = "2025-01-01T00:00:00"
        mock_file.reference_count = 0
        mock_upload.return_value = mock_file

        response = client.post(
            "/avatarforge-controller/upload/reference_image",
            files={"file": sample_image_file}
        )

        assert response.status_code == 200
        assert response.json()["file_id"] == "ref-file-id"

    def test_get_file_not_found(self, client, override_get_db):
        """Test GET /files/{file_id} with non-existent file"""
        with patch('avatarforge.services.file_service.FileService.get_file_by_id', return_value=None):
            response = client.get("/avatarforge-controller/files/invalid-id")

        assert response.status_code == 404

    def test_check_file_hash_exists(self, client, override_get_db):
        """Test GET /files/hash/{hash} when hash exists"""
        mock_file = Mock()
        mock_file.file_id = "existing-id"
        mock_file.filename = "existing.png"

        with patch('avatarforge.services.file_service.FileService.get_file_by_hash', return_value=mock_file):
            response = client.get("/avatarforge-controller/files/hash/abc123")

        assert response.status_code == 200
        data = response.json()
        assert data["exists"] == True
        assert data["file_id"] == "existing-id"

    def test_check_file_hash_not_exists(self, client, override_get_db):
        """Test GET /files/hash/{hash} when hash doesn't exist"""
        with patch('avatarforge.services.file_service.FileService.get_file_by_hash', return_value=None):
            response = client.get("/avatarforge-controller/files/hash/nonexistent")

        assert response.status_code == 200
        data = response.json()
        assert data["exists"] == False
        assert data["file_id"] is None

    def test_delete_file_success(self, client, override_get_db):
        """Test DELETE /files/{file_id} success"""
        with patch('avatarforge.services.file_service.FileService.delete_file', return_value=True):
            response = client.delete("/avatarforge-controller/files/test-id")

        assert response.status_code == 200

    def test_delete_file_not_found(self, client, override_get_db):
        """Test DELETE /files/{file_id} not found"""
        with patch('avatarforge.services.file_service.FileService.delete_file', return_value=False):
            response = client.delete("/avatarforge-controller/files/invalid-id")

        assert response.status_code == 404


class TestGenerationEndpoints:
    """Tests for generation endpoints"""

    @patch('avatarforge.services.generation_service.GenerationService.create_generation')
    @patch('avatarforge.services.generation_service.GenerationService.execute_generation')
    def test_generate_avatar(self, mock_execute, mock_create, client, override_get_db):
        """Test POST /generate/avatar"""
        mock_gen = Mock()
        mock_gen.generation_id = "gen-123"
        mock_gen.status = "processing"
        mock_gen.created_at = "2025-01-01T00:00:00"
        mock_gen.started_at = "2025-01-01T00:00:01"
        mock_gen.completed_at = None
        mock_gen.error_message = None
        mock_gen.comfyui_prompt_id = "comfy-123"

        mock_create.return_value = mock_gen
        mock_execute.return_value = mock_gen

        response = client.post(
            "/avatarforge-controller/generate/avatar",
            json={
                "prompt": "warrior character, blue armor",
                "realism": False
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["generation_id"] == "gen-123"
        assert data["status"] == "processing"

    @patch('avatarforge.services.generation_service.GenerationService.create_generation')
    @patch('avatarforge.services.generation_service.GenerationService.execute_generation')
    def test_generate_avatar_with_file_id(self, mock_execute, mock_create, client, override_get_db):
        """Test POST /generate/avatar with file IDs"""
        mock_gen = Mock()
        mock_gen.generation_id = "gen-456"
        mock_gen.status = "queued"
        mock_gen.created_at = "2025-01-01T00:00:00"
        mock_gen.started_at = None
        mock_gen.completed_at = None
        mock_gen.error_message = None
        mock_gen.comfyui_prompt_id = None

        mock_create.return_value = mock_gen

        response = client.post(
            "/avatarforge-controller/generate/avatar",
            json={
                "prompt": "cyberpunk character",
                "pose_file_id": "file-123",
                "reference_file_id": "file-456",
                "realism": True
            }
        )

        assert response.status_code == 200
        mock_create.assert_called_once()

    @patch('avatarforge.services.generation_service.GenerationService.create_generation')
    @patch('avatarforge.services.generation_service.GenerationService.execute_generation')
    def test_generate_pose_front(self, mock_execute, mock_create, client, override_get_db):
        """Test POST /generate_pose with front pose"""
        mock_gen = Mock()
        mock_gen.generation_id = "gen-789"
        mock_gen.status = "processing"
        mock_gen.created_at = "2025-01-01T00:00:00"
        mock_gen.started_at = "2025-01-01T00:00:01"
        mock_gen.completed_at = None
        mock_gen.error_message = None
        mock_gen.comfyui_prompt_id = "comfy-789"

        mock_create.return_value = mock_gen

        response = client.post(
            "/avatarforge-controller/generate_pose?pose=front",
            json={"prompt": "knight character"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "front" in data["message"].lower()

    def test_generate_pose_invalid(self, client, override_get_db):
        """Test POST /generate_pose with invalid pose"""
        response = client.post(
            "/avatarforge-controller/generate_pose?pose=invalid",
            json={"prompt": "character"}
        )

        assert response.status_code == 400

    @patch('avatarforge.services.generation_service.GenerationService.create_generation')
    @patch('avatarforge.services.generation_service.GenerationService.execute_generation')
    def test_generate_all_poses(self, mock_execute, mock_create, client, override_get_db):
        """Test POST /generate_all_poses"""
        mock_gen = Mock()
        mock_gen.generation_id = "gen-all"
        mock_gen.status = "processing"
        mock_gen.created_at = "2025-01-01T00:00:00"
        mock_gen.started_at = "2025-01-01T00:00:01"
        mock_gen.completed_at = None
        mock_gen.error_message = None
        mock_gen.comfyui_prompt_id = "comfy-all"

        mock_create.return_value = mock_gen

        response = client.post(
            "/avatarforge-controller/generate_all_poses",
            json={"prompt": "warrior, silver armor"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "all poses" in data["message"].lower()


class TestGenerationManagementEndpoints:
    """Tests for generation management endpoints"""

    @patch('avatarforge.services.generation_service.GenerationService.get_generation')
    def test_get_generation(self, mock_get, client, override_get_db):
        """Test GET /generations/{id}"""
        mock_gen = Mock()
        mock_gen.generation_id = "gen-123"
        mock_gen.status = "completed"
        mock_gen.created_at = "2025-01-01T00:00:00"
        mock_gen.started_at = "2025-01-01T00:00:01"
        mock_gen.completed_at = "2025-01-01T00:00:30"
        mock_gen.error_message = None
        mock_gen.comfyui_prompt_id = "comfy-123"
        mock_gen.workflow = None
        mock_gen.output_files = None

        mock_get.return_value = mock_gen

        response = client.get("/avatarforge-controller/generations/gen-123")

        assert response.status_code == 200
        data = response.json()
        assert data["generation_id"] == "gen-123"
        assert data["status"] == "completed"

    @patch('avatarforge.services.generation_service.GenerationService.get_generation')
    def test_get_generation_not_found(self, mock_get, client, override_get_db):
        """Test GET /generations/{id} not found"""
        mock_get.return_value = None

        response = client.get("/avatarforge-controller/generations/invalid-id")

        assert response.status_code == 404

    @patch('avatarforge.services.generation_service.GenerationService.list_generations')
    def test_list_generations(self, mock_list, client, override_get_db, mock_db_session):
        """Test GET /generations"""
        mock_gens = [Mock(), Mock()]
        for i, gen in enumerate(mock_gens):
            gen.generation_id = f"gen-{i}"
            gen.status = "completed"
            gen.created_at = "2025-01-01T00:00:00"
            gen.started_at = "2025-01-01T00:00:01"
            gen.completed_at = "2025-01-01T00:00:30"
            gen.error_message = None
            gen.comfyui_prompt_id = f"comfy-{i}"
            gen.output_files = None

        mock_list.return_value = mock_gens
        mock_db_session.query.return_value.count.return_value = 2

        response = client.get("/avatarforge-controller/generations?limit=10&offset=0")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["generations"]) == 2

    @patch('avatarforge.services.generation_service.GenerationService.delete_generation')
    def test_delete_generation(self, mock_delete, client, override_get_db):
        """Test DELETE /generations/{id}"""
        mock_delete.return_value = True

        response = client.delete("/avatarforge-controller/generations/gen-123")

        assert response.status_code == 200

    @patch('avatarforge.services.generation_service.GenerationService.delete_generation')
    def test_delete_generation_not_found(self, mock_delete, client, override_get_db):
        """Test DELETE /generations/{id} not found"""
        mock_delete.return_value = False

        response = client.delete("/avatarforge-controller/generations/invalid-id")

        assert response.status_code == 404


class TestUtilityEndpoints:
    """Tests for utility endpoints"""

    @patch('avatarforge.services.generation_service.GenerationService.check_comfyui_health')
    def test_health_check(self, mock_health, client, override_get_db):
        """Test GET /health"""
        mock_health.return_value = {
            "status": "healthy",
            "url": "http://localhost:8188"
        }

        response = client.get("/avatarforge-controller/health")

        assert response.status_code == 200
        data = response.json()
        assert data["api_status"] == "healthy"

    def test_list_poses(self, client):
        """Test GET /poses"""
        response = client.get("/avatarforge-controller/poses")

        assert response.status_code == 200
        data = response.json()
        assert "poses" in data
        assert len(data["poses"]) == 4
        pose_names = [p["name"] for p in data["poses"]]
        assert "front" in pose_names
        assert "back" in pose_names
        assert "side" in pose_names
        assert "quarter" in pose_names

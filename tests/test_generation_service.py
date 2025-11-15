"""Unit tests for GenerationService"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
import requests

from avatarforge.services.generation_service import GenerationService
from avatarforge.models.generation import Generation
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
def generation_service(mock_db):
    """Create GenerationService with mocked dependencies"""
    return GenerationService(mock_db, comfyui_url="http://localhost:8188")


class TestGenerationService:
    """Tests for GenerationService class"""

    def test_create_generation_basic(self, generation_service, mock_db):
        """Test creating a basic generation"""
        result = generation_service.create_generation(
            prompt="test warrior",
            realism=False
        )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_create_generation_with_files(self, generation_service, mock_db):
        """Test creating generation with file references"""
        # Mock file lookup
        mock_file = Mock(spec=UploadedFile)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_file

        with patch.object(generation_service.file_service, 'get_file_by_id', return_value=mock_file):
            with patch.object(generation_service.file_service, 'increment_reference'):
                result = generation_service.create_generation(
                    prompt="test character",
                    pose_file_id="file-123",
                    reference_file_id="file-456",
                    realism=True
                )

        mock_db.add.assert_called_once()

    def test_create_generation_invalid_pose_file(self, generation_service, mock_db):
        """Test creating generation with invalid pose file ID"""
        with patch.object(generation_service.file_service, 'get_file_by_id', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                generation_service.create_generation(
                    prompt="test",
                    pose_file_id="invalid-id"
                )

        assert exc_info.value.status_code == 404
        assert "Pose file not found" in exc_info.value.detail

    def test_create_generation_invalid_reference_file(self, generation_service, mock_db):
        """Test creating generation with invalid reference file ID"""
        mock_pose_file = Mock(spec=UploadedFile)

        def mock_get_file(file_id):
            if file_id == "valid-id":
                return mock_pose_file
            return None

        with patch.object(generation_service.file_service, 'get_file_by_id', side_effect=mock_get_file):
            with patch.object(generation_service.file_service, 'increment_reference'):
                with pytest.raises(HTTPException) as exc_info:
                    generation_service.create_generation(
                        prompt="test",
                        pose_file_id="valid-id",
                        reference_file_id="invalid-id"
                    )

        assert exc_info.value.status_code == 404
        assert "Reference file not found" in exc_info.value.detail

    def test_build_workflow_for_generation(self, generation_service, mock_db):
        """Test building workflow from generation"""
        mock_gen = Mock(spec=Generation)
        mock_gen.prompt = "test prompt"
        mock_gen.clothing = "armor"
        mock_gen.style = "watercolor"
        mock_gen.realism = 0
        mock_gen.pose_type = None
        mock_gen.pose_file_id = None
        mock_gen.reference_file_id = None

        workflow = generation_service.build_workflow_for_generation(mock_gen)

        assert workflow is not None
        assert "prompt" in workflow

    def test_build_workflow_with_pose_file(self, generation_service, mock_db, tmp_path):
        """Test building workflow with pose file"""
        # Create mock file
        mock_file = Mock(spec=UploadedFile)
        test_path = tmp_path / "test.png"
        test_path.write_bytes(b"test")

        mock_gen = Mock(spec=Generation)
        mock_gen.prompt = "test"
        mock_gen.clothing = None
        mock_gen.style = None
        mock_gen.realism = 0
        mock_gen.pose_type = None
        mock_gen.pose_file_id = "file-123"
        mock_gen.reference_file_id = None

        with patch.object(generation_service.file_service, 'get_file_by_id', return_value=mock_file):
            with patch.object(generation_service.file_service, 'get_file_path', return_value=test_path):
                workflow = generation_service.build_workflow_for_generation(mock_gen)

        assert workflow is not None

    @patch('avatarforge.services.generation_service.requests.post')
    def test_execute_generation_success(self, mock_post, generation_service, mock_db):
        """Test successful generation execution"""
        # Setup mock generation
        mock_gen = Mock(spec=Generation)
        mock_gen.generation_id = "gen-123"
        mock_gen.status = "queued"
        mock_gen.prompt = "test"
        mock_gen.clothing = None
        mock_gen.style = None
        mock_gen.realism = 0
        mock_gen.pose_type = None
        mock_gen.pose_file_id = None
        mock_gen.reference_file_id = None

        mock_db.query.return_value.filter.return_value.first.return_value = mock_gen

        # Mock ComfyUI response
        mock_response = Mock()
        mock_response.json.return_value = {"prompt_id": "comfy-123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = generation_service.execute_generation("gen-123")

        assert result.status == "processing"
        mock_post.assert_called_once()

    @patch('avatarforge.services.generation_service.requests.post')
    def test_execute_generation_comfyui_error(self, mock_post, generation_service, mock_db):
        """Test generation execution with ComfyUI error"""
        mock_gen = Mock(spec=Generation)
        mock_gen.generation_id = "gen-123"
        mock_gen.status = "queued"
        mock_gen.prompt = "test"
        mock_gen.clothing = None
        mock_gen.style = None
        mock_gen.realism = 0
        mock_gen.pose_type = None
        mock_gen.pose_file_id = None
        mock_gen.reference_file_id = None

        mock_db.query.return_value.filter.return_value.first.return_value = mock_gen

        # Mock ComfyUI error
        mock_post.side_effect = requests.exceptions.RequestException("Connection failed")

        with pytest.raises(HTTPException) as exc_info:
            generation_service.execute_generation("gen-123")

        assert exc_info.value.status_code == 500
        assert mock_gen.status == "failed"

    def test_execute_generation_not_found(self, generation_service, mock_db):
        """Test executing non-existent generation"""
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            generation_service.execute_generation("invalid-id")

        assert exc_info.value.status_code == 404

    def test_execute_generation_already_processing(self, generation_service, mock_db):
        """Test executing generation that's already processing"""
        mock_gen = Mock(spec=Generation)
        mock_gen.status = "processing"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_gen

        with pytest.raises(HTTPException) as exc_info:
            generation_service.execute_generation("gen-123")

        assert exc_info.value.status_code == 400

    def test_get_generation(self, generation_service, mock_db):
        """Test getting generation by ID"""
        mock_gen = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_gen

        result = generation_service.get_generation("gen-123")

        assert result == mock_gen

    def test_list_generations(self, generation_service, mock_db):
        """Test listing generations"""
        mock_gens = [Mock(), Mock(), Mock()]
        mock_db.query.return_value.order_by.return_value.limit.return_value.offset.return_value.all.return_value = mock_gens

        result = generation_service.list_generations(limit=10, offset=0)

        assert len(result) == 3

    def test_list_generations_with_status_filter(self, generation_service, mock_db):
        """Test listing generations with status filter"""
        mock_gens = [Mock()]

        # Setup the mock chain properly
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.all.return_value = mock_gens

        result = generation_service.list_generations(status="completed")

        assert len(result) == 1
        # Verify filter was called with status
        mock_query.filter.assert_called_once()

    def test_update_generation_status(self, generation_service, mock_db):
        """Test updating generation status"""
        mock_gen = Mock(spec=Generation)
        mock_gen.status = "processing"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_gen

        result = generation_service.update_generation_status(
            "gen-123",
            status="completed",
            output_files=[{"filename": "output.png"}]
        )

        assert mock_gen.status == "completed"
        assert mock_gen.output_files == [{"filename": "output.png"}]
        mock_db.commit.assert_called_once()

    def test_delete_generation(self, generation_service, mock_db):
        """Test deleting generation"""
        mock_gen = Mock(spec=Generation)
        mock_gen.pose_file_id = "pose-123"
        mock_gen.reference_file_id = "ref-456"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_gen

        with patch.object(generation_service.file_service, 'decrement_reference'):
            result = generation_service.delete_generation("gen-123")

        assert result == True
        mock_db.delete.assert_called_once()

    def test_delete_generation_not_found(self, generation_service, mock_db):
        """Test deleting non-existent generation"""
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = generation_service.delete_generation("invalid-id")

        assert result == False

    @patch('avatarforge.services.generation_service.requests.get')
    def test_check_comfyui_health_success(self, mock_get, generation_service):
        """Test ComfyUI health check success"""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = generation_service.check_comfyui_health()

        assert result["status"] == "healthy"

    @patch('avatarforge.services.generation_service.requests.get')
    def test_check_comfyui_health_failure(self, mock_get, generation_service):
        """Test ComfyUI health check failure"""
        mock_get.side_effect = requests.exceptions.RequestException("Connection refused")

        result = generation_service.check_comfyui_health()

        assert result["status"] == "unhealthy"
        assert "error" in result

"""Unit tests for health endpoints"""
import pytest
from avatarforge.schemas.health import HealthResponse


def test_health_response_model():
    """Test HealthResponse schema"""
    response = HealthResponse(status="healthy", message="Test message")
    assert response.status == "healthy"
    assert response.message == "Test message"


def test_health_response_validation():
    """Test HealthResponse validation"""
    with pytest.raises(Exception):
        HealthResponse(status="healthy")  # Missing required field

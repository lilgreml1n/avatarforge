"""Health check endpoints"""
from fastapi import APIRouter
from avatarforge.schemas.health import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns the current status of the API
    """
    return HealthResponse(status="healthy", message="AvatarForge API is running")

"""REST API routes and endpoints"""
from fastapi import APIRouter
from avatarforge.rest import health

api_router = APIRouter()

# Include route modules
api_router.include_router(health.router, prefix="/health", tags=["health"])

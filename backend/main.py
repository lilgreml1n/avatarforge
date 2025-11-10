"""
AvatarForge FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from avatarforge.core.config import settings
from avatarforge.rest import api_router
from avatarforge.controllers.avatarforge_controller import router as controller_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AvatarForge API - Avatar generation with file management and deduplication",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Include AvatarForge Controller router
app.include_router(controller_router, prefix="/avatarforge-controller", tags=["controller"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AvatarForge API",
        "version": settings.VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


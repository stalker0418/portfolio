"""Health check API endpoints."""

from fastapi import APIRouter
from src.portfolio.models.chat import HealthResponse
import time

router = APIRouter(tags=["health"])

# Store startup time for uptime calculation
startup_time = time.time()


@router.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Manas Sanjay Portfolio API is running!",
        version="1.0.0",
        uptime=time.time() - startup_time
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check."""
    return HealthResponse(
        status="healthy",
        message="All systems operational",
        version="1.0.0",
        uptime=time.time() - startup_time
    )


@router.get("/debug")
async def debug_info():
    """Debug endpoint to check configuration."""
    from config.simple_settings import settings
    return {
        "together_api_key_set": bool(settings.together_api_key),
        "together_api_key_length": len(settings.together_api_key) if settings.together_api_key else 0,
        "default_model": settings.default_model,
        "debug_mode": settings.debug
    }

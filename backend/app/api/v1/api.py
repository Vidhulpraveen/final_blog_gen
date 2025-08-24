"""
Main API router for Blu Blog Gen Backend
"""

from fastapi import APIRouter
from app.api.v1 import blogs, auth, users, projects, wordpress, api_keys

# Create main API router
api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])
api_router.include_router(wordpress.router, prefix="/wordpress", tags=["WordPress"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["API Keys"])

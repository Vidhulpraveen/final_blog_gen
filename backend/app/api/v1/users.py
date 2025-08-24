"""
Users API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from app.models.blog import UserProfileUpdate, UserProfileResponse
from app.core.database import get_supabase_client
from supabase import Client

router = APIRouter()

@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    client: Client = Depends(get_supabase_client)
):
    """Get user profile (no authentication required - returns test user)"""
    try:
        # Return a test user profile for testing
        test_user = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "test@example.com",
            "full_name": "Test User",
            "role": "user",
            "is_active": True,
            "subscription_plan": "free",
            "subscription_expires_at": None,
            "api_usage_limit": 100,
            "api_usage_current": 0,
            "last_login": None,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        return test_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch profile: {str(e)}")

@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile: UserProfileUpdate,
    client: Client = Depends(get_supabase_client)
):
    """Update user profile (no authentication required)"""
    try:
        # For testing, just return the updated profile data
        updated_profile = {
            "id": "test-user-123",
            "email": "test@example.com",
            "full_name": profile.full_name or "Test User",
            "role": profile.role or "user",
            "is_active": True,
            "subscription_plan": profile.subscription_plan or "free",
            "subscription_expires_at": None,
            "api_usage_limit": profile.api_usage_limit or 100,
            "api_usage_current": 0,
            "last_login": None,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        return updated_profile
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update profile: {str(e)}")

@router.get("/stats")
async def get_user_stats(
    client: Client = Depends(get_supabase_client)
):
    """Get user statistics (no authentication required)"""
    try:
        # Return test statistics
        stats = {
            "total_projects": 5,
            "total_blogs": 25,
            "completed_blogs": 20,
            "failed_blogs": 2,
            "generating_blogs": 3,
            "total_word_count": 15000,
            "average_word_count": 750
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch stats: {str(e)}")

@router.get("/settings")
async def get_user_settings(
    client: Client = Depends(get_supabase_client)
):
    """Get user settings (no authentication required)"""
    try:
        # Return test settings
        settings = {
            "ai_model_preference": "claude-3-sonnet",
            "content_length_preference": "medium",
            "auto_publish": False,
            "notification_preferences": {
                "email": True,
                "push": False
            },
            "theme": "light"
        }
        return settings
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch settings: {str(e)}")

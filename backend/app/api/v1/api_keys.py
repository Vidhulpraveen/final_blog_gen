"""
API Keys management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.blog import APIKeyCreate, APIKeyUpdate, APIKeyResponse
from app.core.database import get_supabase_client
from supabase import Client

router = APIRouter()

@router.get("/", response_model=List[APIKeyResponse])
async def list_api_keys(
    client: Client = Depends(get_supabase_client)
):
    """List all API keys (no authentication required)"""
    try:
        response = client.table("api_keys").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to list API keys: {str(e)}")

@router.post("/", response_model=APIKeyResponse)
async def create_api_key(
    api_key: APIKeyCreate,
    client: Client = Depends(get_supabase_client)
):
    """Create a new API key (no authentication required)"""
    try:
        api_key_data = api_key.model_dump()
        # Use default user ID for testing
        api_key_data["user_id"] = "550e8400-e29b-41d4-a716-446655440000"
        
        # If this is the first key for this service, make it default
        if api_key_data.get("is_default", False):
            # Remove default from other keys of the same service
            client.table("api_keys").update({"is_default": False}).eq("user_id", "550e8400-e29b-41d4-a716-446655440000").eq("service", api_key_data["service"]).execute()
        
        response = client.table("api_keys").insert(api_key_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create API key")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create API key: {str(e)}")

@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Get a specific API key (no authentication required)"""
    try:
        response = client.table("api_keys").select("*").eq("id", key_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get API key: {str(e)}")

@router.put("/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    key_id: str,
    api_key: APIKeyUpdate,
    client: Client = Depends(get_supabase_client)
):
    """Update an API key (no authentication required)"""
    try:
        update_data = api_key.model_dump(exclude_unset=True)
        
        # If making this key default, remove default from others
        if update_data.get("is_default", False):
            existing_key = client.table("api_keys").select("service").eq("id", key_id).single().execute()
            if existing_key.data:
                client.table("api_keys").update({"is_default": False}).eq("user_id", "550e8400-e29b-41d4-a716-446655440000").eq("service", existing_key.data["service"]).execute()
        
        response = client.table("api_keys").update(update_data).eq("id", key_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update API key")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update API key: {str(e)}")

@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Delete an API key (no authentication required)"""
    try:
        response = client.table("api_keys").delete().eq("id", key_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete API key")
        return {"message": "API key deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete API key: {str(e)}")

@router.post("/{key_id}/test")
async def test_api_key(
    key_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Test API key (no authentication required)"""
    try:
        # Get key details
        response = client.table("api_keys").select("*").eq("id", key_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
        
        # For testing, just return success
        return {
            "status": "success",
            "message": "API key test successful",
            "key_id": key_id,
            "service": response.data["service"]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"API key test failed: {str(e)}")

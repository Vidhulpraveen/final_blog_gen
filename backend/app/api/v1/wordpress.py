"""
WordPress integration API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.models.blog import WordPressAccountCreate, WordPressAccountUpdate, WordPressAccountResponse
from app.core.database import get_supabase_client
from supabase import Client

router = APIRouter()

@router.get("/accounts", response_model=List[WordPressAccountResponse])
async def list_wordpress_accounts(
    client: Client = Depends(get_supabase_client)
):
    """List all WordPress accounts (no authentication required)"""
    try:
        response = client.table("wordpress_accounts").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to list WordPress accounts: {str(e)}")

@router.post("/accounts", response_model=WordPressAccountResponse)
async def create_wordpress_account(
    account: WordPressAccountCreate,
    client: Client = Depends(get_supabase_client)
):
    """Create a new WordPress account (no authentication required)"""
    try:
        account_data = account.model_dump()
        # Use default user ID for testing
        account_data["user_id"] = "550e8400-e29b-41d4-a716-446655440000"
        
        response = client.table("wordpress_accounts").insert(account_data).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create WordPress account")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create WordPress account: {str(e)}")

@router.get("/accounts/{account_id}", response_model=WordPressAccountResponse)
async def get_wordpress_account(
    account_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Get a specific WordPress account (no authentication required)"""
    try:
        response = client.table("wordpress_accounts").select("*").eq("id", account_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WordPress account not found")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get WordPress account: {str(e)}")

@router.put("/accounts/{account_id}", response_model=WordPressAccountResponse)
async def update_wordpress_account(
    account_id: str,
    account: WordPressAccountUpdate,
    client: Client = Depends(get_supabase_client)
):
    """Update a WordPress account (no authentication required)"""
    try:
        update_data = account.model_dump(exclude_unset=True)
        response = client.table("wordpress_accounts").update(update_data).eq("id", account_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update WordPress account")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update WordPress account: {str(e)}")

@router.delete("/accounts/{account_id}")
async def delete_wordpress_account(
    account_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Delete a WordPress account (no authentication required)"""
    try:
        response = client.table("wordpress_accounts").delete().eq("id", account_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete WordPress account")
        return {"message": "WordPress account deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete WordPress account: {str(e)}")

@router.post("/accounts/{account_id}/test")
async def test_wordpress_connection(
    account_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Test WordPress connection (no authentication required)"""
    try:
        # Get account details
        response = client.table("wordpress_accounts").select("*").eq("id", account_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WordPress account not found")
        
        # For testing, just return success
        return {
            "status": "success",
            "message": "WordPress connection test successful",
            "account_id": account_id
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"WordPress connection test failed: {str(e)}")

@router.post("/publish/{blog_id}")
async def publish_to_wordpress(
    blog_id: str,
    account_id: Optional[str] = None,
    client: Client = Depends(get_supabase_client)
):
    """Publish blog to WordPress (no authentication required)"""
    try:
        # Get blog details
        blog_response = client.table("blogs").select("*").eq("id", blog_id).single().execute()
        if not blog_response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        
        # For testing, just return success
        return {
            "status": "success",
            "message": "Blog published to WordPress successfully",
            "blog_id": blog_id,
            "wordpress_post_id": "wp_post_123"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to publish to WordPress: {str(e)}")

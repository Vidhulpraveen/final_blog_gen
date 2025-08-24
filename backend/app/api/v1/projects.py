"""
Projects API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.models.blog import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.blog_service import BlogService
from app.core.database import get_supabase_client
from supabase import Client
import logging

router = APIRouter()
blog_service = BlogService()
logger = logging.getLogger(__name__)

@router.get("/")
async def list_projects():
    """List all projects"""
    try:
        logger.info("Listing projects")
        
        # Try to get real data from database
        try:
            from app.core.database import get_supabase_client
            client = get_supabase_client()
            
            if client:
                response = client.table("projects").select("*").order("created_at", desc=True).execute()
                if response.data:
                    logger.info(f"Retrieved {len(response.data)} projects from database")
                    return response.data
                else:
                    logger.info("No projects found in database, returning mock data")
            else:
                logger.info("Database client not available, returning mock data")
                
        except Exception as db_error:
            logger.warning(f"Database operation failed: {str(db_error)}")
            logger.info("Falling back to mock data")
        
        # Return mock data as fallback
        mock_projects = [
            {
                "id": "mock-project-1",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Digital Marketing Mastery",
                "description": "A comprehensive guide to digital marketing strategies",
                "total_blogs": 5,
                "completed_blogs": 0,
                "status": "pending",
                "draft_creation_model": "gpt-4",
                "content_vetting_model": "gpt-4",
                "generated_topics": [],
                "model_settings": {},
                "workflow_preferences": {},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": "mock-project-2",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "AI Content Creation",
                "description": "Exploring AI-powered content generation techniques",
                "total_blogs": 3,
                "completed_blogs": 0,
                "status": "pending",
                "draft_creation_model": "gpt-4",
                "content_vetting_model": "gpt-4",
                "generated_topics": [],
                "model_settings": {},
                "workflow_preferences": {},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        return mock_projects
        
    except Exception as e:
        logger.error(f"Failed to list projects: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to list projects: {str(e)}")

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate
):
    """Create a new project"""
    try:
        project_data = project.model_dump()
        
        # Try to create project in database
        try:
            from app.core.database import get_supabase_client
            client = get_supabase_client()
            
            if client:
                # Prepare project data for database
                db_project_data = {
                    "name": project_data["name"],
                    "description": project_data["description"],
                    "total_blogs": project_data["total_blogs"],
                    "completed_blogs": 0,
                    "status": "pending",
                    "draft_creation_model": project_data["draft_creation_model"],
                    "content_vetting_model": project_data["content_vetting_model"],
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "wordpress_account_id": project_data.get("wordpress_account_id"),
                    "model_settings": project_data.get("model_settings", {}),
                    "workflow_preferences": project_data.get("workflow_preferences", {}),
                    "generated_topics": []
                }
                
                # Insert project into database
                response = client.table("projects").insert(db_project_data).execute()
                
                if response.data:
                    created_project = response.data[0]
                    logger.info(f"Successfully created project in database: {created_project['id']}")
                    return created_project
                else:
                    logger.error("Failed to create project in database - no data returned")
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create project in database")
            else:
                logger.warning("Database client not available, falling back to mock data")
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database service unavailable")
                
        except Exception as db_error:
            logger.error(f"Database operation failed: {str(db_error)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create project: {str(db_error)}")
                
    except Exception as e:
        logger.error(f"Failed to create project: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create project: {str(e)}")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Get a specific project (no authentication required)"""
    try:
        response = client.table("projects").select("*").eq("id", project_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get project: {str(e)}")

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    client: Client = Depends(get_supabase_client)
):
    """Update a project (no authentication required)"""
    try:
        update_data = project.model_dump(exclude_unset=True)
        response = client.table("projects").update(update_data).eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update project")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update project: {str(e)}")

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    client: Client = Depends(get_supabase_client)
):
    """Delete a project (no authentication required)"""
    try:
        response = client.table("projects").delete().eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete project")
        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete project: {str(e)}")

@router.get("/{project_id}/topics")
async def get_project_topics(project_id: str):
    """Get generated topics for a specific project"""
    try:
        logger.info(f"Getting topics for project {project_id}")
        
        # Try to get real data from database
        try:
            from app.core.database import get_supabase_client
            client = get_supabase_client()
            
            if client:
                response = client.table("projects").select("generated_topics").eq("id", project_id).execute()
                if response.data and response.data[0].get("generated_topics"):
                    topics = response.data[0]["generated_topics"]
                    logger.info(f"Retrieved {len(topics)} topics from database for project {project_id}")
                    return {
                        "project_id": project_id,
                        "total_topics": len(topics),
                        "topics": topics
                    }
                else:
                    logger.info(f"No topics found in database for project {project_id}, returning mock data")
            else:
                logger.info("Database client not available, returning mock data")
                
        except Exception as db_error:
            logger.warning(f"Database operation failed: {str(db_error)}")
            logger.info("Falling back to mock data")
        
        # Return mock data as fallback
        mock_topics = [
            {
                "title": "Digital Marketing Fundamentals",
                "description": "Core concepts and principles of digital marketing",
                "content_length": "long",
                "keywords": ["digital marketing", "fundamentals", "principles"],
                "target_audience": "marketing beginners",
                "generated_at": "2024-01-01T00:00:00Z"
            },
            {
                "title": "Social Media Marketing Strategies",
                "description": "Effective strategies for social media marketing",
                "content_length": "medium",
                "keywords": ["social media", "marketing", "strategies"],
                "target_audience": "social media managers",
                "generated_at": "2024-01-01T00:00:00Z"
            },
            {
                "title": "Email Marketing Best Practices",
                "description": "Best practices for email marketing campaigns",
                "content_length": "medium",
                "keywords": ["email marketing", "best practices", "campaigns"],
                "target_audience": "email marketers",
                "generated_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        return {
            "project_id": project_id,
            "total_topics": len(mock_topics),
            "topics": mock_topics
        }
        
    except Exception as e:
        logger.error(f"Failed to get project topics: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get project topics: {str(e)}")

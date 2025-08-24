"""
Blog-related data models for Blu Blog Gen Backend
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# =============================================================================
# BLOG GENERATION MODELS
# =============================================================================

class BlogGenerationRequest(BaseModel):
    """Request model for blog generation"""
    project_id: str = Field(..., description="Project ID to generate blogs for")
    topic: str = Field(..., min_length=1, max_length=200, description="Main topic for blog generation")
    blog_count: int = Field(default=10, ge=1, le=50, description="Number of blogs to generate")

class BlogResponse(BaseModel):
    """Blog response model"""
    id: str = Field(..., description="Blog ID")
    project_id: str = Field(..., description="Project ID")
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., description="Blog title")
    topic: str = Field(..., description="Blog topic")
    content: Optional[str] = Field(None, description="Blog content (HTML)")
    draft_content: Optional[str] = Field(None, description="Draft content")
    keywords: List[str] = Field(default_factory=list, description="Keywords for the blog")
    target_audience: str = Field(default="general", description="Target audience")
    content_length: str = Field(default="medium", description="Content length (short/medium/long)")
    status: str = Field(..., description="Blog status")
    word_count: Optional[int] = Field(None, description="Word count")
    generation_progress: int = Field(default=0, description="Generation progress (0-100)")
    research_data: Optional[Dict[str, Any]] = Field(None, description="Research data")
    research_model: str = Field(default="claude-3-sonnet", description="AI model used for research")
    draft_model: str = Field(default="gpt-4", description="AI model used for content generation")
    error_message: Optional[str] = Field(None, description="Error message if generation failed")
    generation_started_at: Optional[datetime] = Field(None, description="When generation started")
    generation_completed_at: Optional[datetime] = Field(None, description="When generation completed")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

# =============================================================================
# PROJECT MODELS
# =============================================================================

class ProjectCreate(BaseModel):
    """Create project request model"""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    total_blogs: int = Field(default=10, ge=1, le=1000, description="Total blogs to generate")
    wordpress_account_id: Optional[str] = Field(None, description="Associated WordPress account ID")
    draft_creation_model: str = Field(default="openai", description="AI model for draft creation")
    content_vetting_model: str = Field(default="openai", description="AI model for content vetting")
    model_settings: Optional[Dict[str, Any]] = Field(default_factory=dict, description="AI model settings")
    workflow_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Workflow preferences")

class ProjectUpdate(BaseModel):
    """Update project request model"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    total_blogs: Optional[int] = Field(None, ge=1, le=1000, description="Total blogs to generate")
    wordpress_account_id: Optional[str] = Field(None, description="Associated WordPress account ID")
    draft_creation_model: Optional[str] = Field(None, description="AI model for draft creation")
    content_vetting_model: Optional[str] = Field(None, description="AI model for content vetting")
    model_settings: Optional[Dict[str, Any]] = Field(None, description="AI model settings")
    workflow_preferences: Optional[Dict[str, Any]] = Field(None, description="Workflow preferences")

class ProjectResponse(BaseModel):
    """Project response model"""
    id: str = Field(..., description="Project ID")
    user_id: str = Field(..., description="User ID")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    total_blogs: int = Field(..., description="Total blogs to generate")
    completed_blogs: int = Field(default=0, description="Completed blogs count")
    status: str = Field(..., description="Project status")
    wordpress_account_id: Optional[str] = Field(None, description="Associated WordPress account ID")
    draft_creation_model: str = Field(..., description="AI model for draft creation")
    content_vetting_model: str = Field(..., description="AI model for content vetting")
    generated_topics: List[Dict[str, Any]] = Field(default_factory=list, description="Topics generated by LLM")
    model_settings: Dict[str, Any] = Field(default_factory=dict, description="AI model settings")
    workflow_preferences: Dict[str, Any] = Field(default_factory=dict, description="Workflow preferences")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

# =============================================================================
# USER PROFILE MODELS
# =============================================================================

class UserProfileUpdate(BaseModel):
    """Update user profile request model"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name")
    role: Optional[str] = Field(None, description="User role")
    subscription_plan: Optional[str] = Field(None, description="Subscription plan")
    api_usage_limit: Optional[int] = Field(None, ge=0, description="API usage limit")

class UserProfileResponse(BaseModel):
    """User profile response model"""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="Full name")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Whether user is active")
    subscription_plan: str = Field(..., description="Subscription plan")
    subscription_expires_at: Optional[datetime] = Field(None, description="Subscription expiry")
    api_usage_limit: int = Field(..., description="API usage limit")
    api_usage_current: int = Field(..., description="Current API usage")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

# =============================================================================
# WORDPRESS ACCOUNT MODELS
# =============================================================================

class WordPressAccountCreate(BaseModel):
    """Create WordPress account request model"""
    account_name: str = Field(..., min_length=1, max_length=255, description="Account name")
    site_url: str = Field(..., description="WordPress site URL")
    username: str = Field(..., min_length=1, description="WordPress username")
    password: str = Field(..., min_length=1, description="WordPress password or API key")
    api_endpoint: Optional[str] = Field(None, description="Custom API endpoint")
    is_default: bool = Field(default=False, description="Whether this is the default account")

class WordPressAccountUpdate(BaseModel):
    """Update WordPress account request model"""
    account_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Account name")
    site_url: Optional[str] = Field(None, description="WordPress site URL")
    username: Optional[str] = Field(None, min_length=1, description="WordPress username")
    password: Optional[str] = Field(None, min_length=1, description="WordPress password or API key")
    api_endpoint: Optional[str] = Field(None, description="Custom API endpoint")
    is_default: Optional[bool] = Field(None, description="Whether this is the default account")

class WordPressAccountResponse(BaseModel):
    """WordPress account response model"""
    id: str = Field(..., description="Account ID")
    user_id: str = Field(..., description="User ID")
    account_name: str = Field(..., description="Account name")
    site_url: str = Field(..., description="WordPress site URL")
    username: str = Field(..., description="WordPress username")
    api_endpoint: Optional[str] = Field(None, description="Custom API endpoint")
    is_default: bool = Field(..., description="Whether this is the default account")
    is_active: bool = Field(..., description="Whether account is active")
    last_used: Optional[datetime] = Field(None, description="Last time account was used")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

# =============================================================================
# API KEY MODELS
# =============================================================================

class APIKeyCreate(BaseModel):
    """Create API key request model"""
    service: str = Field(..., description="AI service (openai, anthropic, gemini)")
    api_key: str = Field(..., min_length=1, description="API key for the service")
    is_default: bool = Field(default=False, description="Whether this is the default key for the service")
    description: Optional[str] = Field(None, description="Key description")

class APIKeyUpdate(BaseModel):
    """Update API key request model"""
    api_key: Optional[str] = Field(None, min_length=1, description="API key for the service")
    is_default: Optional[bool] = Field(None, description="Whether this is the default key for the service")
    description: Optional[str] = Field(None, description="Key description")
    is_active: Optional[bool] = Field(None, description="Whether key is active")

class APIKeyResponse(BaseModel):
    """API key response model"""
    id: str = Field(..., description="Key ID")
    user_id: str = Field(..., description="User ID")
    service: str = Field(..., description="AI service")
    api_key: str = Field(..., description="Masked API key")
    is_default: bool = Field(..., description="Whether this is the default key")
    description: Optional[str] = Field(None, description="Key description")
    is_active: bool = Field(..., description="Whether key is active")
    last_used: Optional[datetime] = Field(None, description="Last time key was used")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

# =============================================================================
# VALIDATORS
# =============================================================================

@validator('content_length')
def validate_content_length(cls, v):
    """Validate content length"""
    if v not in ['short', 'medium', 'long']:
        raise ValueError('content_length must be short, medium, or long')
    return v

@validator('status')
def validate_status(cls, v):
    """Validate blog status"""
    valid_statuses = ['pending', 'generating', 'completed', 'failed', 'published', 'archived']
    if v not in valid_statuses:
        raise ValueError(f'status must be one of: {", ".join(valid_statuses)}')
    return v

@validator('subscription_plan')
def validate_subscription_plan(cls, v):
    """Validate subscription plan"""
    valid_plans = ['free', 'starter', 'professional', 'enterprise', 'internal']
    if v not in valid_plans:
        raise ValueError(f'subscription_plan must be one of: {", ".join(valid_plans)}')
    return v

@validator('role')
def validate_role(cls, v):
    """Validate user role"""
    valid_roles = ['user', 'moderator', 'admin']
    if v not in valid_roles:
        raise ValueError(f'role must be one of: {", ".join(valid_roles)}')
    return v

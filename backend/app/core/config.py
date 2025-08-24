"""
Configuration management for Blu Blog Gen Backend
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Blu Blog Gen Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js frontend
        "http://localhost:8000",  # Backend
        "https://yourdomain.com"  # Production domain
    ]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "") # Now required
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Now optional
    
    # AI Service Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # SERP API for research
    SERP_API_KEY: Optional[str] = os.getenv("SERP_API_KEY")
    
    # WordPress Integration
    WORDPRESS_API_URL: Optional[str] = os.getenv("WORDPRESS_API_URL")
    WORDPRESS_USERNAME: Optional[str] = os.getenv("WORDPRESS_USERNAME")
    WORDPRESS_PASSWORD: Optional[str] = os.getenv("WORDPRESS_PASSWORD")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    # Feature Flags
    ENABLE_AI_GENERATION: bool = os.getenv("ENABLE_AI_GENERATION", "true").lower() == "true"
    ENABLE_WORDPRESS_INTEGRATION: bool = os.getenv("ENABLE_WORDPRESS_INTEGRATION", "true").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }


# Create settings instance
settings = Settings()

# Validation
def validate_settings():
    """Validate required settings"""
    required_settings = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY"
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")


# Validate on import
if not settings.DEBUG:
    validate_settings()

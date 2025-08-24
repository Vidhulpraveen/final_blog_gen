"""
Database connection and management for Blu Blog Gen Backend
"""

from supabase import create_client, Client
from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Global Supabase client
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Optional[Client]:
    """Get Supabase client instance - simplified and robust"""
    global _supabase_client
    
    # If client exists, return it
    if _supabase_client is not None:
        return _supabase_client
    
    # Try to create client if it doesn't exist
    try:
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            logger.warning("Missing Supabase configuration")
            return None
        
        # Use anon key by default, fallback to service role if available
        api_key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
        
        _supabase_client = create_client(
            settings.SUPABASE_URL,
            api_key
        )
        
        # Test connection
        try:
            response = _supabase_client.table("users").select("id").limit(1).execute()
            logger.info("Database connection established successfully")
        except Exception as test_error:
            logger.warning(f"Database connection test failed: {str(test_error)}")
            # Don't fail completely, just log the warning
            # The client might still work for other operations
        
        return _supabase_client
        
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {str(e)}")
        _supabase_client = None
        return None


async def init_db():
    """Initialize database connection - async wrapper"""
    try:
        client = get_supabase_client()
        if client:
            logger.info("Database initialized successfully")
        else:
            logger.warning("Database initialization failed, will use fallback mode")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")


async def close_db():
    """Close database connection"""
    global _supabase_client
    
    if _supabase_client:
        _supabase_client = None
        logger.info("Database connection closed")


# FastAPI dependency function
async def get_supabase_client_dep() -> Optional[Client]:
    """FastAPI dependency function to get Supabase client"""
    return get_supabase_client()


# Database utility functions
class DatabaseManager:
    """Database operations manager"""
    
    def __init__(self):
        self._client = None
    
    @property
    def client(self):
        if not self._client:
            self._client = get_supabase_client()
        return self._client
    
    async def execute_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            response = client.rpc('exec_sql', {'query': query, 'params': params or {}})
            return response
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    async def insert_record(self, table: str, data: dict):
        """Insert record into table"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            response = client.table(table).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Insert failed for table {table}: {str(e)}")
            raise
    
    async def get_record(self, table: str, filters: dict):
        """Get single record from table"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            query = client.table(table).select("*")
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.limit(1).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Get record failed for table {table}: {str(e)}")
            raise
    
    async def get_records(self, table: str, filters: dict = None, limit: int = 100):
        """Get multiple records from table"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            query = client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.limit(limit).execute()
            return response.data
        except Exception as e:
            logger.error(f"Get records failed for table {table}: {str(e)}")
            raise
    
    async def update_record(self, table: str, filters: dict, data: dict):
        """Update record in table"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            query = client.table(table).update(data)
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Update failed for table {table}: {str(e)}")
            raise
    
    async def delete_record(self, table: str, filters: dict):
        """Delete record from table"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            query = client.table(table).delete()
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Delete failed for table {table}: {str(e)}")
            raise
    
    async def count_records(self, table: str, filters: dict = None):
        """Count records in table"""
        try:
            client = self.client
            if not client:
                raise RuntimeError("Database client not available")
            query = client.table(table).select("*", count="exact")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.execute()
            return response.count or 0
        except Exception as e:
            logger.error(f"Count failed for table {table}: {str(e)}")
            raise


# Create global database manager instance
db_manager = DatabaseManager()

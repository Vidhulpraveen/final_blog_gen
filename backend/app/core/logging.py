"""
Logging configuration for Blu Blog Gen Backend
"""

import logging
import sys
from typing import Dict, Any
import structlog
from app.core.config import settings

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


def setup_logging():
    """Setup logging configuration"""
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        fmt=settings.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured successfully - Level: {settings.LOG_LEVEL}, Format: {settings.LOG_FORMAT}")


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class RequestLogger:
    """Request logging middleware"""
    
    def __init__(self):
        self.logger = get_logger("request")
    
    def log_request(self, request_data: Dict[str, Any]):
        """Log incoming request"""
        self.logger.info("Incoming request",
                        method=request_data.get("method"),
                        url=request_data.get("url"),
                        client_ip=request_data.get("client_ip"),
                        user_agent=request_data.get("user_agent"))
    
    def log_response(self, request_data: Dict[str, Any], response_data: Dict[str, Any]):
        """Log response"""
        self.logger.info("Response sent",
                        method=request_data.get("method"),
                        url=request_data.get("url"),
                        status_code=response_data.get("status_code"),
                        response_time=response_data.get("response_time"))
    
    def log_error(self, request_data: Dict[str, Any], error_data: Dict[str, Any]):
        """Log error"""
        self.logger.error("Request error",
                         method=request_data.get("method"),
                         url=request_data.get("url"),
                         error_type=error_data.get("error_type"),
                         error_message=error_data.get("error_message"),
                         stack_trace=error_data.get("stack_trace"))


# Create global request logger instance
request_logger = RequestLogger()

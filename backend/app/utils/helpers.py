"""
Utility helper functions for Blu Blog Gen Backend
"""

import re
import hashlib
from typing import List, Dict, Any
from datetime import datetime, timezone


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    
    # Remove special characters except hyphens
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    
    # Replace multiple spaces/hyphens with single hyphen
    slug = re.sub(r'[\s-]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def sanitize_html(html_content: str) -> str:
    """Sanitize HTML content for safe storage"""
    # Basic HTML sanitization - in production, use a proper library like bleach
    allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    
    # Remove script tags and other potentially dangerous content
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
    html_content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
    html_content = re.sub(r'javascript:', '', html_content, flags=re.IGNORECASE)
    
    return html_content


def calculate_reading_time(content: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes"""
    word_count = len(content.split())
    reading_time = max(1, word_count // words_per_minute)
    return reading_time


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract potential keywords from text"""
    # Simple keyword extraction - in production, use NLP libraries
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an'}
    
    # Count word frequency
    word_freq = {}
    for word in words:
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:max_keywords]]
    
    return keywords


def generate_hash(content: str) -> str:
    """Generate hash for content to detect duplicates"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def generate_random_id(length: int = 8) -> str:
    """Generate random alphanumeric ID"""
    import random
    import string
    
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries, with dict2 values taking precedence"""
    result = dict1.copy()
    result.update(dict2)
    return result


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from nested dictionary"""
    keys = key.split('.')
    current = data
    
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

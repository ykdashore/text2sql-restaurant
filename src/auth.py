from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
import logging

logger = logging.getLogger("text2sql_api.auth")

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_valid_api_keys():
    """Load valid API keys from environment variable."""
    keys_str = os.getenv("API_KEYS", "")
    if not keys_str:
        logger.warning("No API_KEYS found in environment")
        return set()
    
    keys = [key.strip() for key in keys_str.split(",") if key.strip()]
    logger.info(f"Loaded {len(keys)} API key(s)")
    return set(keys)

VALID_API_KEYS = get_valid_api_keys()

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    """Verify the API key from request header."""
    if not VALID_API_KEYS:
        logger.error("No valid API keys configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API authentication not configured"
        )
    
    if not api_key:
        logger.warning("Missing API key in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    
    if api_key not in VALID_API_KEYS:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return api_key

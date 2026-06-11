from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt, JWTError
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.config import settings
from .jwt import TokenPayload

REFRESH_TOKEN_EXPIRE_DAYS = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)

def create_refresh_token(subject: Union[str, Any]) -> str:
    """Create a new long-lived JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def verify_refresh_token(token: str) -> str:
    """
    Verify the refresh token and return the subject (user_id).
    Raises HTTPException if token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        token_data = TokenPayload(**payload)
        
        if not token_data.sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return token_data.sub
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

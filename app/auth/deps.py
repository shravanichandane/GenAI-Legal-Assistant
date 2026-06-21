import uuid
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import User
from app.config import settings
from .jwt import TokenPayload

# Keep OAuth2PasswordBearer for Swagger UI compatibility, but make it optional
# so cookie-based auth can take priority.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,  # Don't raise if header is missing; we check cookies first
)

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    bearer_token: Optional[str] = Depends(reusable_oauth2),
) -> User:
    """
    FastAPI dependency to get the current authenticated user.
    Reads JWT from the access_token HttpOnly cookie first,
    falling back to the Authorization: Bearer header for API clients.
    """
    # 1. Try cookie first
    token = request.cookies.get("access_token")

    # 2. Fall back to Authorization header
    if not token:
        token = bearer_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    if not token_data.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    try:
        user_id = uuid.UUID(token_data.sub)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subject in token",
        )
        
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """FastAPI dependency to get the current active authenticated user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

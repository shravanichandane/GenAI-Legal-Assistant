from datetime import datetime, timedelta, timezone
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a password hash using bcrypt."""
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any],
    role: Union[str, None] = None,
    org_id: Union[str, None] = None,
    expires_delta: timedelta = None
) -> str:
    """Create a new JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    if role:
        to_encode["role"] = role
    if org_id:
        to_encode["org_id"] = str(org_id)
        
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

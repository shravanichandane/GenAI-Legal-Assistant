from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.database import get_db
from app.db.models import User
from app.config import settings
from . import security
from .jwt import Token
from .refresh_tokens import create_refresh_token
from .audit_security import AuthAuditLogger

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create new user.
    """
    stmt = select(User).where(User.email == user_in.email)
    user = db.execute(stmt).scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    from app.db.models import Organization
    import uuid
    org_id = uuid.uuid4()
    new_org = Organization(
        id=org_id,
        name=f"{user_in.email}'s Organization"
    )
    db.add(new_org)
    
    new_user = User(
        id=uuid.uuid4(),
        organization_id=org_id,
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully."}

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login_access_token(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    client_ip = request.client.host if request.client else None
    
    stmt = select(User).where(User.email == form_data.username)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        AuthAuditLogger.log_event(
            action=AuthAuditLogger.ACTION_LOGIN_FAILED,
            user_id=form_data.username,
            ip_address=client_ip,
            details="Incorrect email or password"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        AuthAuditLogger.log_event(
            action=AuthAuditLogger.ACTION_LOGIN_FAILED,
            user_id=str(user.id),
            organization_id=str(getattr(user, "organization_id", "")),
            ip_address=client_ip,
            details="Inactive user"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    role = getattr(user, "role", None)
    org_id = getattr(user, "organization_id", None)
    
    access_token = security.create_access_token(
        subject=str(user.id),
        role=role,
        org_id=org_id,
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(subject=str(user.id))
    
    AuthAuditLogger.log_event(
        action=AuthAuditLogger.ACTION_LOGIN_SUCCESS,
        user_id=str(user.id),
        organization_id=str(org_id) if org_id else None,
        ip_address=client_ip,
        details="Successfully logged in"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

from .refresh_tokens import verify_refresh_token
from pydantic import BaseModel

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=Token)
def refresh_access_token(
    request_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using a long-lived refresh token.
    """
    user_id_str = verify_refresh_token(request_data.refresh_token)
    
    stmt = select(User).where(User.id == user_id_str)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive or deleted user",
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    role = getattr(user, "role", None)
    org_id = getattr(user, "organization_id", None)
    
    access_token = security.create_access_token(
        subject=str(user.id),
        role=role,
        org_id=org_id,
        expires_delta=access_token_expires
    )
    
    # Optionally issue a new refresh token (refresh token rotation)
    new_refresh_token = create_refresh_token(subject=str(user.id))
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token
    }

from .deps import get_current_user

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": getattr(current_user, "role", "user")
    }


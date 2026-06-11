from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """Token model for returning access and refresh tokens."""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenPayload(BaseModel):
    """Payload model for JWT token."""
    sub: Optional[str] = None
    org_id: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None

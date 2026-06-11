from typing import List
from fastapi import Depends, HTTPException, status

from app.db.models import User
from .deps import get_current_active_user

class RoleChecker:
    """
    Role based access control dependency.
    
    It verifies that the current active user has a role that is allowed
    to access the endpoint.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        # Assuming the User model has a `role` attribute or property.
        user_role = getattr(current_user, "role", None)
        
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Requires one of: {self.allowed_roles}"
            )
        
        return current_user

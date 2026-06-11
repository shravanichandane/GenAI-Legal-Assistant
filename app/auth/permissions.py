from typing import List, Dict, Set
from fastapi import Depends, HTTPException, status
from app.db.models import User
from .deps import get_current_active_user

# Define granular permissions
class Permissions:
    CONTRACT_CREATE = "contract:create"
    CONTRACT_READ = "contract:read"
    CONTRACT_UPDATE = "contract:update"
    CONTRACT_DELETE = "contract:delete"
    CONTRACT_APPROVE = "contract:approve"
    CONTRACT_UPLOAD = "contract:upload"
    USER_MANAGE = "user:manage"
    ORG_MANAGE = "org:manage"

# Map roles to their allowed permissions
ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "admin": {
        Permissions.CONTRACT_CREATE,
        Permissions.CONTRACT_READ,
        Permissions.CONTRACT_UPDATE,
        Permissions.CONTRACT_DELETE,
        Permissions.CONTRACT_APPROVE,
        Permissions.CONTRACT_UPLOAD,
        Permissions.USER_MANAGE,
        Permissions.ORG_MANAGE,
    },
    "manager": {
        Permissions.CONTRACT_CREATE,
        Permissions.CONTRACT_READ,
        Permissions.CONTRACT_UPDATE,
        Permissions.CONTRACT_APPROVE,
        Permissions.CONTRACT_UPLOAD,
    },
    "user": {
        Permissions.CONTRACT_READ,
        Permissions.CONTRACT_UPLOAD,
    },
}

class PermissionChecker:
    """
    Permission based access control dependency.
    
    Verifies that the current active user has the required permissions
    to access the endpoint based on their role.
    """
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = set(required_permissions)

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        user_role = getattr(current_user, "role", "user")
        
        user_permissions = ROLE_PERMISSIONS.get(user_role, set())
        
        if not self.required_permissions.issubset(user_permissions):
            missing_perms = self.required_permissions - user_permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Missing permissions: {list(missing_perms)}"
            )
        
        return current_user

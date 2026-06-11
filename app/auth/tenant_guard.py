from typing import Any
from fastapi import HTTPException, status

class TenantGuard:
    """
    Enforces tenant isolation by verifying that a resource belongs
    to the same organization as the current user.
    """
    
    @staticmethod
    def verify(resource: Any, current_user: Any) -> None:
        """
        Verify that the resource's organization_id matches the user's organization_id.
        Raises 403 Forbidden if they mismatch.
        """
        if not hasattr(resource, "organization_id"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Resource missing organization_id attribute for tenant verification."
            )
            
        if not hasattr(current_user, "organization_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User missing organization_id for tenant verification."
            )
            
        if str(resource.organization_id) != str(current_user.organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Resource does not belong to your organization."
            )

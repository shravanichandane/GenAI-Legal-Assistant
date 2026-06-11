import logging
from datetime import datetime, timezone
from typing import Optional

# Configure standard logger
logger = logging.getLogger("auth_audit")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class AuthAuditLogger:
    """
    Security audit logger for authentication and authorization events.
    """
    
    ACTION_LOGIN_SUCCESS = "LOGIN_SUCCESS"
    ACTION_LOGIN_FAILED = "LOGIN_FAILED"
    ACTION_ROLE_CHANGED = "ROLE_CHANGED"
    
    @staticmethod
    def log_event(
        action: str,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Log an auth security event with structured data.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        log_data = {
            "action": action,
            "timestamp": timestamp,
            "user_id": user_id or "UNKNOWN",
            "organization_id": organization_id or "UNKNOWN",
            "ip_address": ip_address or "UNKNOWN",
        }
        
        if details:
            log_data["details"] = details
            
        # Log as a structured message
        message = (
            f"AUDIT_EVENT: {action} | "
            f"User: {log_data['user_id']} | "
            f"Org: {log_data['organization_id']} | "
            f"IP: {log_data['ip_address']}"
        )
        if details:
            message += f" | Details: {details}"
            
        if action == AuthAuditLogger.ACTION_LOGIN_FAILED:
            logger.warning(message, extra={"audit_data": log_data})
        else:
            logger.info(message, extra={"audit_data": log_data})

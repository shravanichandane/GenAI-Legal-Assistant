import json
import os
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    """
    An audit logger that writes reviewer actions to a JSON lines file,
    simulating the upcoming Postgres DB in Week 9.
    """
    def __init__(self, log_file_path: str = "audit_log.jsonl"):
        """
        Initialize the AuditLogger.
        
        Args:
            log_file_path (str): The path to the JSON lines log file.
        """
        self.log_file_path = log_file_path
        
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
    def log_action(self, reviewer_id: str, document_id: str, original_risk_score: float, action_taken: str, comments: str = "") -> None:
        """
        Log an action taken by a reviewer.
        
        Args:
            reviewer_id (str): The ID of the reviewer performing the action.
            document_id (str): The ID of the document being reviewed.
            original_risk_score (float): The original risk score of the document.
            action_taken (str): The action taken (e.g., APPROVED, REJECTED, MODIFIED).
            comments (str): Optional comments regarding the action.
        """
        log_entry = {
            "reviewer_id": reviewer_id,
            "document_id": document_id,
            "timestamp": datetime.now().isoformat(),
            "original_risk_score": original_risk_score,
            "action_taken": action_taken,
            "comments": comments
        }
        
        with open(self.log_file_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
    def get_logs(self) -> list[Dict[str, Any]]:
        """
        Retrieve all audit logs.
        """
        if not os.path.exists(self.log_file_path):
            return []
            
        logs = []
        with open(self.log_file_path, "r") as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        return logs

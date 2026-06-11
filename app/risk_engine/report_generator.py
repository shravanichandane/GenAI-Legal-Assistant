import json
from typing import Dict, Any

class ReportGenerator:
    """
    Utility for generating summary risk reports.
    """
    
    @staticmethod
    def generate_dashboard_payload(contract_id: str, evaluation_results: Dict[str, Any]) -> str:
        """
        Formats the final score and status into a JSON payload for the frontend dashboard.
        
        Args:
            contract_id: Unique identifier for the contract.
            evaluation_results: Dictionary containing 'score' and 'status'.
            
        Returns:
            str: JSON formatted string payload.
        """
        score = evaluation_results.get("score", 0)
        status = evaluation_results.get("status", "UNKNOWN")
        
        # Determine risk category based on score if status is not CRITICAL
        if status != "CRITICAL":
            if score >= 70:
                risk_category = "High Risk"
            elif score >= 40:
                risk_category = "Medium Risk"
            else:
                risk_category = "Low Risk"
        else:
            risk_category = "Critical Risk"
            
        payload = {
            "contract_id": contract_id,
            "risk_summary": {
                "overall_score": score,
                "status": status,
                "risk_category": risk_category
            },
            "metadata": {
                "review_recommended": status == "CRITICAL" or score >= 70
            }
        }
        
        return json.dumps(payload, indent=2)

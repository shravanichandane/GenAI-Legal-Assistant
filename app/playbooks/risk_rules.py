"""
Playbook Risk Rules module.
Implements deterministic logic to analyze a clause against a playbook rule
and return a baseline risk score.
"""
from typing import Optional, Dict, Any
from app.playbooks.models import PlaybookRule

def evaluate_clause_risk(parsed_clause_data: Dict[str, Any], playbook_rule: PlaybookRule) -> str:
    """
    Evaluates a parsed clause's extracted metadata against the playbook rule 
    using deterministic logic.
    
    Args:
        parsed_clause_data: A dictionary containing extracted information from the clause.
                            For example: {"notice_days": 7} for a termination clause.
        playbook_rule: The corresponding PlaybookRule object.
        
    Returns:
        A string representing the baseline risk score ('LOW', 'MEDIUM', 'HIGH').
    """
    if not playbook_rule:
        return "HIGH"
        
    risk_score = playbook_rule.risk_level.upper()
    
    # Deterministic check: Notice Days for termination clauses
    if playbook_rule.minimum_notice_days is not None:
        extracted_notice_days = parsed_clause_data.get("notice_days")
        if extracted_notice_days is None:
            # Missing critical information is high risk
            return "HIGH"
            
        try:
            days = int(extracted_notice_days)
            if days < playbook_rule.minimum_notice_days:
                # E.g., if notice_days (7) < minimum_notice_days (30)
                return "HIGH"
            else:
                return "LOW"
        except (ValueError, TypeError):
            # Invalid data type for notice days
            return "HIGH"
            
    # Other deterministic rules can be added here
    return risk_score

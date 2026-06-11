from typing import List, Dict, Any

def apply_critical_overrides(clauses: List[Dict[str, Any]]) -> str:
    """
    Applies hardcoded deterministic rules to determine if the contract 
    has a CRITICAL status.
    
    Args:
        clauses: A list of clause analysis results (typically from RAGResponse).
                 Each clause should be a dictionary containing 'risk_level' 
                 and 'requires_human_review'.
                 
    Returns:
        str: 'CRITICAL' if critical rules are met, otherwise 'NORMAL'.
    """
    for clause in clauses:
        risk_level = clause.get("risk_level", "").upper()
        requires_human_review = clause.get("requires_human_review", False)
        
        if risk_level == "HIGH" and requires_human_review:
            return "CRITICAL"
            
    return "NORMAL"

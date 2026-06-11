from typing import List, Any
from .rules import apply_critical_overrides

class RiskAggregator:
    """
    Aggregates risk scores from multiple RAG responses to calculate an overall
    contract risk score.
    """
    
    RISK_WEIGHTS = {
        "HIGH": 30,
        "MEDIUM": 15,
        "LOW": 5
    }
    
    def __init__(self):
        pass

    def calculate_overall_risk(self, rag_responses: List[Any]) -> int:
        """
        Calculates the overall contract risk score.
        
        Args:
            rag_responses: A list of RAGResponse objects containing clause analysis.
                           Assumes each response has a 'risk_level' attribute or key.
                           
        Returns:
            int: The aggregated risk score, capped at 100.
        """
        total_score = 0
        
        for response in rag_responses:
            # Handle both dictionary and object attribute access
            if isinstance(response, dict):
                risk_level = response.get("risk_level", "LOW")
            else:
                risk_level = getattr(response, "risk_level", "LOW")
                
            risk_level_upper = str(risk_level).upper()
            total_score += self.RISK_WEIGHTS.get(risk_level_upper, 0)
            
        return min(total_score, 100)
        
    def evaluate_contract(self, rag_responses: List[Any]) -> dict:
        """
        Evaluates the full contract, calculating the score and applying overrides.
        
        Args:
            rag_responses: List of RAGResponse objects.
            
        Returns:
            dict: Evaluation results including score and status.
        """
        score = self.calculate_overall_risk(rag_responses)
        
        # Convert responses to dicts for rules engine if they are objects
        clauses_for_rules = []
        for response in rag_responses:
            if isinstance(response, dict):
                clauses_for_rules.append(response)
            else:
                clauses_for_rules.append({
                    "risk_level": getattr(response, "risk_level", "LOW"),
                    "requires_human_review": getattr(response, "requires_human_review", False)
                })
                
        status = apply_critical_overrides(clauses_for_rules)
        
        return {
            "score": score,
            "status": status
        }

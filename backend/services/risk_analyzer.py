### backend/services/risk_analyzer.py

from typing import Dict, Any
from .llm_service import llm_service

class RiskAnalyzer:
    def __init__(self):
        self.risk_weights = {
            "INDEMNITY": 1.5,
            "LIABILITY": 1.4, 
            "TERMINATION": 1.1,
            "PAYMENT": 0.8,
            "CONFIDENTIALITY": 1.2,
            "GENERAL": 0.5
        }
    
    def analyze_clause_risk(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """Analyze risk for a specific clause"""
        # Get LLM risk analysis
        risk_analysis = llm_service.analyze_risk(clause_text, clause_type)
        
        # Apply type-based weighting
        base_score = risk_analysis.get("risk_score", 3.0)
        weight = self.risk_weights.get(clause_type, 1.0)
        adjusted_score = min(10.0, base_score * weight)
        
        # Determine risk level
        if adjusted_score <= 3.0:
            risk_level = "LOW"
        elif adjusted_score <= 6.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return {
            "risk_score": round(adjusted_score, 2),
            "risk_level": risk_level,
            "reasoning": risk_analysis.get("reasoning", "Risk assessment based on clause type and content.")
        }
    
    def calculate_document_risk(self, clauses: list) -> Dict[str, Any]:
        """Calculate overall document risk metrics"""
        if not clauses:
            return {"overall_score": 0.0, "overall_level": "LOW", "high_risk_count": 0}
        
        scores = [clause.risk_score for clause in clauses if clause.risk_score is not None]
        if not scores:
            return {"overall_score": 0.0, "overall_level": "LOW", "high_risk_count": 0}
        
        avg_score = sum(scores) / len(scores)
        high_risk_count = len([s for s in scores if s > 6.0])
        
        if avg_score <= 3.0:
            overall_level = "LOW"
        elif avg_score <= 6.0:
            overall_level = "MEDIUM"
        else:
            overall_level = "HIGH"
        
        return {
            "overall_score": round(avg_score, 2),
            "overall_level": overall_level,
            "high_risk_count": high_risk_count,
            "total_clauses": len(clauses)
        }

risk_analyzer = RiskAnalyzer()

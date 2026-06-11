"""
Risk Explainer utility for generating structured Markdown justifications for risk scores.
"""
from typing import Dict, Any, List

class RiskExplainer:
    """
    Generates structured Markdown justifications explaining why a specific 
    risk score was assigned to a contract clause.
    """
    
    @staticmethod
    def generate_explanation(
        clause_text: str,
        risk_score: str,
        risk_factors: List[str],
        playbook_rule: str,
        mitigation_suggestion: str
    ) -> str:
        """
        Generate a Markdown formatted explanation for the risk score.
        
        Args:
            clause_text: The original text of the clause.
            risk_score: The assigned risk score (e.g., 'HIGH', 'MEDIUM', 'LOW').
            risk_factors: List of reasons for the risk score.
            playbook_rule: The playbook rule that was violated or analyzed.
            mitigation_suggestion: Recommended changes to mitigate the risk.
            
        Returns:
            A formatted Markdown string containing the explanation.
        """
        md_factors = "\n".join([f"- **Factor**: {factor}" for factor in risk_factors])
        
        template = f"""### Risk Assessment: {risk_score.upper()}

**Analyzed Clause:**
> {clause_text}

**Playbook Rule Applied:**
* {playbook_rule}

**Key Risk Factors:**
{md_factors}

**Recommended Mitigation:**
* {mitigation_suggestion}
"""
        return template

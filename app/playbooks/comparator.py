"""
Playbook Comparator module.
Implements logic to compare a parsed contract clause against the corresponding playbook rule.
"""
import json
from typing import Dict, Any
from app.playbooks.models import PlaybookRule

def compare_clause_to_playbook(parsed_clause_text: str, playbook_rule: PlaybookRule) -> str:
    """
    Outputs a formatted JSON string highlighting differences between the parsed clause 
    and the playbook preferred/fallback language. This context is useful for RAG pipelines.
    
    Args:
        parsed_clause_text: The actual text of the clause parsed from the contract.
        playbook_rule: The playbook rule corresponding to the clause type.
        
    Returns:
        A formatted JSON string providing prompt context for LLM evaluation.
    """
    comparison_context: Dict[str, Any] = {
        "clause_type": playbook_rule.clause_type,
        "playbook_preferred_language": playbook_rule.preferred_language,
        "playbook_fallback_language": playbook_rule.fallback_language,
        "contract_clause_text": parsed_clause_text,
        "instructions": (
            "Compare the 'contract_clause_text' against the 'playbook_preferred_language' "
            "and 'playbook_fallback_language'. Highlight any deviations, missing protections, "
            "or added obligations that are not present in the playbook language."
        )
    }
    
    # Adding specific condition checks if present in the rule
    if playbook_rule.minimum_notice_days is not None:
        comparison_context["additional_checks"] = (
            f"Ensure the contract clause explicitly states a minimum of "
            f"{playbook_rule.minimum_notice_days} notice days."
        )
        
    return json.dumps(comparison_context, indent=4)

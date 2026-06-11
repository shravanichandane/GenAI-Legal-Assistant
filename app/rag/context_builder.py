from typing import Any, Dict, List

def build_context(clause: str, playbook_rule: str, deterministic_violations: List[str]) -> Dict[str, Any]:
    """
    Builds a clean dictionary containing context for the RAG pipeline.
    
    Args:
        clause (str): The clause text to analyze.
        playbook_rule (str): The relevant playbook rule.
        deterministic_violations (List[str]): Violations found by deterministic rules.
        
    Returns:
        Dict[str, Any]: The context dictionary.
    """
    return {
        "clause": clause.strip(),
        "playbook_rule": playbook_rule.strip(),
        "deterministic_violations": deterministic_violations,
    }

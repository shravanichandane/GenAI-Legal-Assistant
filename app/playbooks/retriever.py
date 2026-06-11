"""
Playbook Retriever module.
Contains logic to fetch a PlaybookRule for a given clause type.
"""
from typing import Optional, Dict
from app.playbooks.models import PlaybookRule

# Dummy database of playbook rules
_PLAYBOOK_DB: Dict[str, PlaybookRule] = {
    "termination": PlaybookRule(
        clause_type="termination",
        risk_level="high",
        preferred_language="Either party may terminate this Agreement at any time upon thirty (30) days written notice to the other party.",
        fallback_language="This Agreement may be terminated by either party upon fifteen (15) days written notice.",
        minimum_notice_days=30
    ),
    "confidentiality": PlaybookRule(
        clause_type="confidentiality",
        risk_level="medium",
        preferred_language="The Receiving Party shall maintain the Confidential Information in strict confidence for a period of five (5) years.",
        fallback_language="The Receiving Party shall maintain the Confidential Information in strict confidence for a period of three (3) years.",
        minimum_notice_days=None
    ),
    "indemnity": PlaybookRule(
        clause_type="indemnity",
        risk_level="high",
        preferred_language="The Vendor shall indemnify and hold harmless the Company against all third-party claims.",
        fallback_language="The Vendor shall indemnify the Company against direct damages arising from gross negligence.",
        minimum_notice_days=None
    )
}

def get_playbook_rule(clause_type: str) -> Optional[PlaybookRule]:
    """
    Retrieves the PlaybookRule for a specific clause type.
    
    Args:
        clause_type: A string representing the clause type (e.g., 'termination').
        
    Returns:
        The PlaybookRule object if found, else None.
    """
    normalized_clause_type = clause_type.strip().lower()
    return _PLAYBOOK_DB.get(normalized_clause_type)

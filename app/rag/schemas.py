from pydantic import BaseModel
from typing import List, Dict, Optional

class RAGResponse(BaseModel):
    clause_id: str = ""
    text_snippet: str = ""
    clause_type: str
    risk_level: str
    policy_violation: bool
    confidence: float
    summary: str
    recommendation: str
    evidence: List[Dict[str, str]]
    requires_human_review: bool
    boundingBox: Optional[Dict[str, float]] = None

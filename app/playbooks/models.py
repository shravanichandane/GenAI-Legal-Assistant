"""
Playbook Models module.
Defines the Pydantic schema for the Legal Playbook rules.
"""
from typing import Optional
from pydantic import BaseModel, Field


class PlaybookRule(BaseModel):
    """
    PlaybookRule defines the enterprise company policies for a specific contract clause.
    """
    clause_type: str = Field(..., description="The type of the clause, e.g., 'termination', 'indemnity'")
    risk_level: str = Field(..., description="The baseline risk level associated with this clause type, e.g., 'low', 'medium', 'high'")
    preferred_language: str = Field(..., description="The preferred standard language for this clause.")
    fallback_language: str = Field(..., description="The acceptable fallback language if preferred is not accepted.")
    minimum_notice_days: Optional[int] = Field(None, description="Optional minimum number of notice days required (e.g., for termination).")

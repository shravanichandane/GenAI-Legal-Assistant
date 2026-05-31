### backend/services/clause_extractor.py

from typing import List, Dict, Any
from .llm_service import llm_service
import re

class ClauseExtractor:
    def __init__(self):
        self.clause_patterns = {
            "INDEMNITY": [r"indemnif\w+", r"hold\s+harmless", r"defend\s+against"],
            "LIABILITY": [r"liability", r"liable", r"damages", r"loss"],
            "TERMINATION": [r"terminat\w+", r"end\s+this", r"expire", r"dissolution"],
            "PAYMENT": [r"payment", r"invoice", r"fee", r"cost", r"price"],
            "CONFIDENTIALITY": [r"confidential", r"non-disclosure", r"proprietary", r"trade\s+secret"]
        }
    
    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract clauses using LLM and pattern matching"""
        # Get LLM-based extraction
        llm_clauses = llm_service.extract_clauses(text)
        
        # Enhance with pattern-based classification if AI didn't classify it specifically
        enhanced_clauses = []
        for clause in llm_clauses:
            current_type = clause.get("clause_type")
            if not current_type or current_type == "GENERAL":
                clause["clause_type"] = self._classify_clause_type(clause.get("clause_text", ""))
            enhanced_clauses.append(clause)
        
        return enhanced_clauses
    
    def _classify_clause_type(self, clause_text: str) -> str:
        """Classify clause type using pattern matching"""
        clause_lower = clause_text.lower()
        
        for clause_type, patterns in self.clause_patterns.items():
            for pattern in patterns:
                if re.search(pattern, clause_lower):
                    return clause_type
        
        return "GENERAL"

clause_extractor = ClauseExtractor()

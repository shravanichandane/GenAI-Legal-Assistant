### backend/services/semantic_search.py

from typing import List, Dict, Any
import re
from sqlalchemy.orm import Session
from ..models import Document, Clause

class SemanticSearchService:
    def __init__(self):
        # In a production environment, you'd use Pinecone/Weaviate here
        # For now, we'll implement basic text search
        pass
    
    def search_clauses(self, db: Session, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search clauses using semantic/text matching"""
        # Simple text-based search for demo
        # In production, this would use vector embeddings
        
        query_lower = query.lower()
        query_terms = query_lower.split()
        
        all_clauses = db.query(Clause).all()
        scored_results = []
        
        for clause in all_clauses:
            score = self._calculate_relevance_score(clause, query_terms)
            if score > 0:
                scored_results.append({
                    "clause": clause,
                    "score": score,
                    "highlighted_text": self._highlight_matches(clause.clause_text, query_terms)
                })
        
        # Sort by relevance score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_results[:limit]
    
    def _calculate_relevance_score(self, clause: Clause, query_terms: List[str]) -> float:
        """Calculate relevance score for a clause"""
        text_lower = clause.clause_text.lower()
        summary_lower = (clause.summary or "").lower()
        
        score = 0.0
        
        # Exact phrase matches get highest score
        full_query = " ".join(query_terms)
        if full_query in text_lower:
            score += 10.0
        elif full_query in summary_lower:
            score += 8.0
        
        # Individual term matches
        for term in query_terms:
            if term in text_lower:
                score += 3.0
            elif term in summary_lower:
                score += 2.0
            elif term in clause.clause_type.lower():
                score += 5.0
        
        # Boost high-risk clauses slightly
        if clause.risk_level == "HIGH":
            score *= 1.1
        
        return score
    
    def _highlight_matches(self, text: str, query_terms: List[str]) -> str:
        """Add highlighting to matching terms"""
        highlighted = text
        for term in query_terms:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            highlighted = pattern.sub(f"**{term}**", highlighted)
        return highlighted

semantic_search = SemanticSearchService()

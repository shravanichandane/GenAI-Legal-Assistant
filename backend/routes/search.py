### backend/routes/search.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.semantic_search import semantic_search
from ..auth import get_current_user, User
from typing import List

router = APIRouter()

@router.get("/search")
async def search_clauses(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, description="Maximum number of results"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = semantic_search.search_clauses(db, query, limit)
    
    # Format results for frontend
    formatted_results = []
    for result in results:
        clause = result["clause"]
        formatted_results.append({
            "id": clause.id,
            "document_id": clause.document_id,
            "clause_text": result["highlighted_text"],
            "summary": clause.summary,
            "risk_level": clause.risk_level,
            "risk_score": clause.risk_score,
            "clause_type": clause.clause_type,
            "relevance_score": result["score"],
            "document_filename": clause.document.filename if clause.document else "Unknown"
        })
    
    return {
        "query": query,
        "results": formatted_results,
        "total_found": len(formatted_results)
    }

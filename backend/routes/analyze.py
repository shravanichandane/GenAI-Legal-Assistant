### backend/routes/analyze.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Document, Clause, ClauseResponse, ClauseUpdate
from ..services.clause_extractor import clause_extractor
from ..services.risk_analyzer import risk_analyzer
from ..services.llm_service import llm_service
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze/{document_id}", response_model=List[ClauseResponse])
async def analyze_document(document_id: int, db: Session = Depends(get_db)):
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if document has content
    if not document.content or len(document.content.strip()) < 10:
        raise HTTPException(status_code=400, detail="Document has insufficient content for analysis")
    
    # Check if document already has clauses to avoid overwriting user edits
    existing_clauses = db.query(Clause).filter(Clause.document_id == document_id).all()
    if existing_clauses:
        return existing_clauses
    
    try:
        # Extract clauses from document content
        extracted_clauses = clause_extractor.extract_from_text(document.content)
        
        if not extracted_clauses:
            # If no clauses extracted, create a general clause from the content
            first_paragraph = document.content[:500] + "..." if len(document.content) > 500 else document.content
            extracted_clauses = [{
                "clause_text": first_paragraph,
                "clause_type": "GENERAL",
                "description": "Document content for review"
            }]
        
        # Process and save clauses
        db_clauses = []
        for clause_data in extracted_clauses:
            try:
                # Debug: Check if clause_data is a dict
                if not isinstance(clause_data, dict):
                    logger.error(f"Expected dict but got {type(clause_data)}: {clause_data}")
                    continue
                
                # Analyze risk
                risk_analysis = risk_analyzer.analyze_clause_risk(
                    clause_data["clause_text"], 
                    clause_data.get("clause_type", "GENERAL")
                )
                
                # Generate summary
                summary = llm_service.summarize_clause(clause_data["clause_text"])
                
                # Create clause record
                db_clause = Clause(
                    document_id=document_id,
                    clause_text=clause_data["clause_text"],  # Store full clause text
                    clause_type=clause_data.get("clause_type", "GENERAL"),
                    summary=summary if summary else None,  # Store full summary
                    risk_score=risk_analysis["risk_score"],
                    risk_level=risk_analysis["risk_level"]
                )
                
                db.add(db_clause)
                db_clauses.append(db_clause)
                
            except Exception as e:
                logger.error(f"Error processing clause: {e}")
                continue  # Skip problematic clauses but continue with others
        
        if not db_clauses:
            raise HTTPException(status_code=500, detail="Failed to process any clauses from the document")
        
        db.commit()
        
        # Refresh all clauses
        for clause in db_clauses:
            db.refresh(clause)
        
        logger.info(f"Successfully analyzed document {document_id}: {len(db_clauses)} clauses extracted")
        return db_clauses
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error analyzing document {document_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal error during document analysis")

@router.get("/clauses", response_model=List[ClauseResponse])
async def get_all_clauses(db: Session = Depends(get_db)):
    clauses = db.query(Clause).all()
    return clauses

@router.get("/clauses/{document_id}", response_model=List[ClauseResponse])
async def get_document_clauses(document_id: int, db: Session = Depends(get_db)):
    clauses = db.query(Clause).filter(Clause.document_id == document_id).all()
    return clauses

@router.put("/clauses/{clause_id}", response_model=ClauseResponse)
async def update_clause(
    clause_id: int, 
    clause_update: ClauseUpdate, 
    db: Session = Depends(get_db)
):
    clause = db.query(Clause).filter(Clause.id == clause_id).first()
    if not clause:
        raise HTTPException(status_code=404, detail="Clause not found")
    
    # Update fields
    update_data = clause_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(clause, field, value)
    
    db.commit()
    db.refresh(clause)
    return clause

@router.get("/documents", response_model=List[dict])
async def get_all_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    result = []
    for doc in documents:
        clause_count = db.query(Clause).filter(Clause.document_id == doc.id).count()
        high_risk_count = db.query(Clause).filter(
            Clause.document_id == doc.id, 
            Clause.risk_level == "HIGH"
        ).count()
        
        result.append({
            "id": doc.id,
            "filename": doc.filename,
            "upload_date": doc.upload_date,
            "clause_count": clause_count,
            "high_risk_count": high_risk_count
        })
    
    return result

@router.get("/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    total_docs = db.query(Document).count()
    total_clauses = db.query(Clause).count()
    high_risk_clauses = db.query(Clause).filter(Clause.risk_level == "HIGH").count()
    
    # Risk distribution
    risk_dist = {}
    for level in ["LOW", "MEDIUM", "HIGH"]:
        count = db.query(Clause).filter(Clause.risk_level == level).count()
        risk_dist[level] = count
    
    # Clause type distribution
    clause_types = {}
    for clause_type in ["INDEMNITY", "LIABILITY", "TERMINATION", "PAYMENT", "CONFIDENTIALITY", "GENERAL"]:
        count = db.query(Clause).filter(Clause.clause_type == clause_type).count()
        if count > 0:
            clause_types[clause_type] = count
    
    # Average risk score
    avg_risk = db.query(Clause).filter(Clause.risk_score.isnot(None)).all()
    avg_risk_score = sum([c.risk_score for c in avg_risk]) / len(avg_risk) if avg_risk else 0.0
    
    return {
        "total_documents": total_docs,
        "total_clauses": total_clauses,
        "high_risk_clauses": high_risk_clauses,
        "high_risk_percentage": (high_risk_clauses / total_clauses * 100) if total_clauses > 0 else 0,
        "average_risk_score": round(avg_risk_score, 2),
        "risk_distribution": risk_dist,
        "clause_type_distribution": clause_types
    }

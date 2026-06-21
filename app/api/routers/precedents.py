import logging
import io
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Precedent, PlaybookRule, User
from app.auth.deps import get_current_active_user
from app.services.pipeline import get_pipeline
from app.parsers.document_parser import HierarchicalParser

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_precedent(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload a Gold Standard template to be indexed as precedents.
    """
    if not file.filename.endswith(('.txt', '.pdf')):
        raise HTTPException(status_code=400, detail="Only TXT and PDF files supported for templates.")

    content_bytes = await file.read()
    
    # Simple extraction for now
    if file.filename.lower().endswith('.pdf'):
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
                pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                text_content = "\n".join(pages_text)
        except ImportError:
            raise HTTPException(status_code=500, detail="pdfplumber is not installed.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    else:
        text_content = content_bytes.decode('utf-8', errors='ignore')
        
    if not text_content.strip():
        raise HTTPException(status_code=400, detail="Document contains no text.")
        
    pipeline = await asyncio.to_thread(get_pipeline)
    
    # Get Organization Rules
    db_rules = db.query(PlaybookRule).filter(PlaybookRule.organization_id == current_user.organization_id).all()
    if not db_rules:
        raise HTTPException(status_code=400, detail="No playbook rules defined for this organization to tag against.")
        
    rule_texts = [r.rule_description for r in db_rules]
    rule_embeddings = pipeline.classifier.encode(rule_texts)
    
    # Parse into clauses
    flat_clauses = HierarchicalParser.extract_flat_clauses(text_content)
    
    added_count = 0
    namespace = str(current_user.organization_id)
    
    docs_to_index = []
    meta_to_index = []
    
    for clause in flat_clauses:
        clause_text = clause.get("text", "").strip()
        if not clause_text or len(clause_text) < 15:
            continue
            
        # Classify the clause using Playbook Rules
        clause_emb = pipeline.classifier.encode([clause_text])
        best_match_idx, best_score = pipeline.classifier.compute_similarity(clause_emb, rule_embeddings)
        
        # Only index if it matches a known playbook rule category with some confidence
        if best_score > 0.4:
            matched_rule = db_rules[best_match_idx]
            clause_type = matched_rule.clause_type.upper()
            
            # Save to DB
            new_precedent = Precedent(
                organization_id=current_user.organization_id,
                title=f"{file.filename} - {clause_type}",
                content=clause_text,
                tags=[clause_type, "gold_template"]
            )
            db.add(new_precedent)
            
            # Prepare for FAISS
            docs_to_index.append(clause_text)
            meta_to_index.append({
                "text": clause_text,
                "clause_type": clause_type,
                "source_file": file.filename
            })
            added_count += 1
            
    db.commit()
    
    # Push to FAISS
    if docs_to_index:
        pipeline.retriever.add_documents(namespace, docs_to_index, meta_to_index)
        
    return {
        "status": "success",
        "message": f"Successfully ingested {added_count} precedent clauses from {file.filename}.",
        "clauses_indexed": added_count
    }

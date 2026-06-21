from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.services.pipeline import get_pipeline
from app.db.database import get_db, SessionLocal
from app.db.models import Contract, ContractStatus, Organization
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_default_org(db: Session):
    org = db.query(Organization).first()
    if not org:
        org = Organization(name="Default Org")
        db.add(org)
        db.commit()
        db.refresh(org)
    return org

@router.post("/upload")
async def upload_contract(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.pdf', '.txt', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and DOCX files are supported.")
    
    content_bytes = await file.read()
    
    if file.filename.lower().endswith('.pdf'):
        import io
        try:
            import pdfplumber
        except ImportError:
            raise HTTPException(status_code=500, detail="pdfplumber is not installed on the server.")
            
        try:
            with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
                pages_text = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                text_content = "\n".join(pages_text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    else:
        text_content = content_bytes.decode('utf-8', errors='ignore')
    
    org = get_default_org(db)
    
    new_contract = Contract(
        organization_id=org.id,
        title=file.filename,
        status=ContractStatus.DRAFT,
        content_text=text_content,
        metadata_json={
            "status": "processing",
            "progress": 0,
            "risks": [],
            "risk_score": 0
        }
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    
    contract_id = str(new_contract.id)
    
    background_tasks.add_task(_run_pipeline_background, contract_id, text_content)
    
    return {
        "status": "success",
        "contract_id": contract_id,
        "filename": file.filename,
        "message": "Processing started"
    }

async def _run_pipeline_background(contract_id: str, text: str):
    import asyncio
    pipeline = await asyncio.to_thread(get_pipeline)
    
    with SessionLocal() as db:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            return
            
        try:
            contract.metadata_json = {**contract.metadata_json, "progress": 25}
            db.commit()
            
            result = await pipeline.analyze(text)
            
            contract.status = ContractStatus.REVIEW
            contract.metadata_json = {
                **contract.metadata_json,
                "status": "analyzed",
                "progress": 100,
                "risks": result["risks"],
                "risk_score": result["overall_score"]
            }
            db.commit()
        except Exception as e:
            logger.error(f"Pipeline failed for {contract_id}: {e}")
            contract.metadata_json = {
                **contract.metadata_json,
                "status": "failed",
                "error": str(e)
            }
            db.commit()

@router.get("/{contract_id}/status")
async def get_contract_status(contract_id: str, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract.metadata_json

@router.get("/{contract_id}/risks")
async def get_contract_risks(contract_id: str, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    meta = contract.metadata_json or {}
    if meta.get("status") != "analyzed":
        return {"id": contract_id, "status": meta.get("status", "unknown"), "risk_score": 0, "findings": []}
        
    return {
        "id": contract_id,
        "status": "analyzed",
        "risk_score": meta.get("risk_score", 0),
        "findings": _map_risks_to_ui(meta.get("risks", []))
    }

def _map_risks_to_ui(pipeline_risks):
    mapped = []
    for idx, r in enumerate(pipeline_risks):
        mapped.append({
            "id": r.get("clause_id", f"clause_{idx}"),
            "severity": str(r.get("risk_level", "low")).lower(),
            "title": r.get("clause_type", "General Clause"),
            "description": r.get("summary", ""),
            "playbookRule": r.get("recommendation", ""),
            "clauseId": r.get("clause_id", f"Clause {idx+1}"),
            "textSnippet": r.get("text_snippet", "")
        })
    return mapped

@router.post("/{contract_id}/action")
async def review_action(contract_id: str, action: dict, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    act = action.get("action")
    if act == "approved":
        contract.status = ContractStatus.APPROVED
    elif act == "rejected":
        contract.status = ContractStatus.ARCHIVED
        
    db.commit()
    return {"status": "success", "message": f"Action {act} recorded."}

@router.get("/{contract_id}/risk-score")
async def get_risk_score(contract_id: str, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return {"score": 0}
    return {"score": (contract.metadata_json or {}).get("risk_score", 0)}

@router.get("/")
async def list_contracts(db: Session = Depends(get_db)):
    contracts = []
    db_contracts = db.query(Contract).order_by(Contract.created_at.desc()).all()
    for job in db_contracts:
        meta = job.metadata_json or {}
        
        status_text = "Pending Review"
        if meta.get("status") == "processing":
            status_text = "Processing"
        elif meta.get("status") == "failed":
            status_text = "Failed"
        elif meta.get("status") == "analyzed":
            score = meta.get("risk_score", 0)
            if score > 60:
                status_text = "Critical Risk"
            elif score > 30:
                status_text = "Warning"
            else:
                status_text = "Approved"
                
        if job.status == ContractStatus.APPROVED:
            status_text = "Approved"
            
        date_str = job.created_at.strftime("%b %d, %Y") if job.created_at else "Just now"
            
        contracts.append({
            "id": str(job.id),
            "name": job.title,
            "vendor": "Extracted Vendor (WIP)",
            "status": status_text,
            "score": meta.get("risk_score", 0),
            "date": date_str,
            "type": "Contract"
        })
    return contracts

@router.get("/{contract_id}/content")
async def get_contract_content(contract_id: str, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"content": contract.content_text or ""}

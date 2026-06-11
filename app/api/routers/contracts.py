from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.pipeline import get_pipeline
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory store for MVP so frontend can poll /status
# In production, this goes to PostgreSQL DB via SQLAlchemy.
_JOB_STORE = {}

@router.post("/upload")
async def upload_contract(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.txt', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and DOCX files are supported.")
    
    contract_id = f"cnt_{uuid.uuid4().hex[:8]}"
    content_bytes = await file.read()
    # Decode text for now
    text_content = content_bytes.decode('utf-8', errors='ignore')
    
    _JOB_STORE[contract_id] = {
        "status": "processing",
        "progress": 0,
        "risks": [],
        "risk_score": 0,
        "filename": file.filename
    }
    
    # Run the pipeline in the background (simulating Celery worker behavior)
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
    try:
        _JOB_STORE[contract_id]["progress"] = 25
        result = await pipeline.analyze(text)
        _JOB_STORE[contract_id]["status"] = "analyzed"
        _JOB_STORE[contract_id]["progress"] = 100
        _JOB_STORE[contract_id]["risks"] = result["risks"]
        _JOB_STORE[contract_id]["risk_score"] = result["overall_score"]
    except Exception as e:
        logger.error(f"Pipeline failed for {contract_id}: {e}")
        _JOB_STORE[contract_id]["status"] = "failed"
        _JOB_STORE[contract_id]["error"] = str(e)

@router.get("/{contract_id}/status")
async def get_contract_status(contract_id: str):
    if contract_id not in _JOB_STORE:
        # Check if the UI is trying to poll a hardcoded mock ID from before
        if contract_id.startswith("cnt_"):
            return {"status": "analyzed", "progress": 100}
        raise HTTPException(status_code=404, detail="Contract not found")
    return _JOB_STORE[contract_id]

@router.get("/{contract_id}/risks")
async def get_contract_risks(contract_id: str):
    if contract_id not in _JOB_STORE:
        # Provide a mock fallback for UI if it's polling something else
        if contract_id.startswith("cnt_"):
             return {"id": contract_id, "status": "analyzed", "risk_score": 0, "findings": []}
        raise HTTPException(status_code=404, detail="Contract not found")
    job = _JOB_STORE[contract_id]
    if job["status"] != "analyzed":
        # Return empty list while processing instead of 400 so UI doesn't crash
        return {"id": contract_id, "status": job["status"], "risk_score": 0, "findings": []}
    return {
        "id": contract_id,
        "status": "analyzed",
        "risk_score": job["risk_score"],
        "findings": _map_risks_to_ui(job["risks"])
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
async def review_action(contract_id: str, action: dict):
    if contract_id not in _JOB_STORE:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"status": "success", "message": f"Action {action.get('action')} recorded."}

@router.get("/{contract_id}/risk-score")
async def get_risk_score(contract_id: str):
    if contract_id not in _JOB_STORE:
        return {"score": 0}
    return {"score": _JOB_STORE[contract_id].get("risk_score", 0)}

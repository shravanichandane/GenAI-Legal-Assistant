from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PlaybookRule, User
from app.auth.deps import get_current_active_user
from pydantic import BaseModel
import uuid

router = APIRouter()

class PlaybookRuleCreate(BaseModel):
    clause_type: str
    rule_description: str
    is_mandatory: bool = False

class PlaybookRuleUpdate(BaseModel):
    clause_type: str | None = None
    rule_description: str | None = None
    is_mandatory: bool | None = None

@router.get("/rules")
async def list_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    rules = db.query(PlaybookRule).filter(
        PlaybookRule.organization_id == current_user.organization_id,
    ).order_by(PlaybookRule.created_at.desc()).all()
    return [{
        "id": str(rule.id),
        "clause_type": rule.clause_type,
        "rule_description": rule.rule_description,
        "is_mandatory": rule.is_mandatory,
        "created_at": rule.created_at.isoformat() if rule.created_at else None
    } for rule in rules]

@router.post("/rules")
async def create_rule(
    rule_in: PlaybookRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    new_rule = PlaybookRule(
        organization_id=current_user.organization_id,
        clause_type=rule_in.clause_type,
        rule_description=rule_in.rule_description,
        is_mandatory=rule_in.is_mandatory
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return {
        "id": str(new_rule.id),
        "clause_type": new_rule.clause_type,
        "rule_description": new_rule.rule_description,
        "is_mandatory": new_rule.is_mandatory
    }

@router.put("/rules/{rule_id}")
async def update_rule(
    rule_id: str,
    rule_in: PlaybookRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        rule_uuid = uuid.UUID(rule_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rule ID format")
        
    rule = db.query(PlaybookRule).filter(
        PlaybookRule.id == rule_uuid,
        PlaybookRule.organization_id == current_user.organization_id,
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    if rule_in.clause_type is not None:
        rule.clause_type = rule_in.clause_type
    if rule_in.rule_description is not None:
        rule.rule_description = rule_in.rule_description
    if rule_in.is_mandatory is not None:
        rule.is_mandatory = rule_in.is_mandatory
        
    db.commit()
    db.refresh(rule)
    return {"status": "success", "id": str(rule.id)}

@router.delete("/rules/{rule_id}")
async def delete_rule(
    rule_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        rule_uuid = uuid.UUID(rule_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rule ID format")
        
    rule = db.query(PlaybookRule).filter(
        PlaybookRule.id == rule_uuid,
        PlaybookRule.organization_id == current_user.organization_id,
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    db.delete(rule)
    db.commit()
    return {"status": "success", "message": "Rule deleted"}

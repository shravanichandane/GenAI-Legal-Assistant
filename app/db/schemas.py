from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from .models import ContractStatus

class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

# --- Organization ---
class OrganizationBase(BaseModel):
    name: str
    domain: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None

class OrganizationRead(OrganizationBase, ORMBase):
    pass

# --- User ---
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    organization_id: uuid.UUID

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(UserBase, ORMBase):
    pass

# --- Contract ---
class ContractBase(BaseModel):
    title: str
    status: ContractStatus = ContractStatus.DRAFT
    content_text: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    organization_id: uuid.UUID

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[ContractStatus] = None
    content_text: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

class ContractRead(ContractBase, ORMBase):
    pass

# --- Clause ---
class ClauseBase(BaseModel):
    contract_id: uuid.UUID
    clause_type: Optional[str] = None
    content: str
    organization_id: uuid.UUID

class ClauseCreate(ClauseBase):
    pass

class ClauseUpdate(BaseModel):
    clause_type: Optional[str] = None
    content: Optional[str] = None

class ClauseRead(ClauseBase, ORMBase):
    pass

# --- PlaybookRule ---
class PlaybookRuleBase(BaseModel):
    clause_type: str
    rule_description: str
    is_mandatory: bool = False
    organization_id: uuid.UUID

class PlaybookRuleCreate(PlaybookRuleBase):
    pass

class PlaybookRuleUpdate(BaseModel):
    clause_type: Optional[str] = None
    rule_description: Optional[str] = None
    is_mandatory: Optional[bool] = None

class PlaybookRuleRead(PlaybookRuleBase, ORMBase):
    pass

# --- Precedent ---
class PrecedentBase(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    organization_id: uuid.UUID

class PrecedentCreate(PrecedentBase):
    pass

class PrecedentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class PrecedentRead(PrecedentBase, ORMBase):
    pass

# --- RiskPolicy ---
class RiskPolicyBase(BaseModel):
    name: str
    severity_level: str
    condition_json: Dict[str, Any] = Field(default_factory=dict)
    organization_id: uuid.UUID

class RiskPolicyCreate(RiskPolicyBase):
    pass

class RiskPolicyUpdate(BaseModel):
    name: Optional[str] = None
    severity_level: Optional[str] = None
    condition_json: Optional[Dict[str, Any]] = None

class RiskPolicyRead(RiskPolicyBase, ORMBase):
    pass

# --- AuditEvent ---
class AuditEventBase(BaseModel):
    user_id: Optional[uuid.UUID] = None
    action: str
    resource_type: str
    resource_id: Optional[uuid.UUID] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    organization_id: uuid.UUID

class AuditEventCreate(AuditEventBase):
    pass

class AuditEventRead(AuditEventBase, ORMBase):
    pass

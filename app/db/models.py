import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text, DateTime, JSON, Enum as SQLEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def uuid_gen() -> uuid.UUID:
    return uuid.uuid4()

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class BaseEntity(Base):
    __abstract__ = True
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid_gen)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

class Organization(BaseEntity):
    __tablename__ = "organizations"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=True)
    
    users: Mapped[list["User"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    contracts: Mapped[list["Contract"]] = relationship(back_populates="organization", cascade="all, delete-orphan")

class User(BaseEntity):
    __tablename__ = "users"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    organization: Mapped["Organization"] = relationship(back_populates="users")

class ContractStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    ARCHIVED = "ARCHIVED"

class Contract(BaseEntity):
    __tablename__ = "contracts"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[ContractStatus] = mapped_column(SQLEnum(ContractStatus), default=ContractStatus.DRAFT)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=True, default=dict)
    
    organization: Mapped["Organization"] = relationship(back_populates="contracts")
    clauses: Mapped[list["Clause"]] = relationship(back_populates="contract", cascade="all, delete-orphan")

class Clause(BaseEntity):
    __tablename__ = "clauses"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    contract_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True)
    clause_type: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    contract: Mapped["Contract"] = relationship(back_populates="clauses")

class PlaybookRule(BaseEntity):
    __tablename__ = "playbook_rules"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    clause_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    rule_description: Mapped[str] = mapped_column(Text, nullable=False)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=False)
    
class Precedent(BaseEntity):
    __tablename__ = "precedents"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=list)

class RiskPolicy(BaseEntity):
    __tablename__ = "risk_policies"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    severity_level: Mapped[str] = mapped_column(String(50), nullable=False)
    condition_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

class AuditEvent(BaseEntity):
    __tablename__ = "audit_events"
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    details: Mapped[dict] = mapped_column(JSON, nullable=True, default=dict)

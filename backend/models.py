### backend/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    clauses = relationship("Clause", back_populates="document")
    owner = relationship("User", back_populates="documents")

class Clause(Base):
    __tablename__ = "clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    clause_text = Column(Text)
    summary = Column(Text)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")
    clause_type = Column(String, default="GENERAL")
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="clauses")

# Pydantic schemas
class ClauseBase(BaseModel):
    clause_text: str
    summary: Optional[str] = None
    risk_score: Optional[float] = 0.0
    risk_level: Optional[str] = "LOW"
    clause_type: Optional[str] = "GENERAL"

class ClauseCreate(ClauseBase):
    document_id: int

class ClauseUpdate(BaseModel):
    summary: Optional[str] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    clause_type: Optional[str] = None

class ClauseResponse(ClauseBase):
    id: int
    document_id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    filename: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    upload_date: datetime
    clauses: List[ClauseResponse] = []
    
    class Config:
        from_attributes = True
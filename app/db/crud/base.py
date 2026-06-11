from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    def get(self, db: Session, id: UUID, organization_id: UUID) -> Optional[ModelType]:
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.organization_id == organization_id
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(
        self, db: Session, organization_id: UUID, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        stmt = select(self.model).where(
            self.model.organization_id == organization_id
        ).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def create(self, db: Session, *, obj_in: CreateSchemaType, organization_id: UUID) -> ModelType:
        obj_in_data = obj_in.model_dump()
        # Force the organization_id to ensure multi-tenancy at repository level
        obj_in_data["organization_id"] = organization_id
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        organization_id: UUID
    ) -> ModelType:
        # Check ownership before update (defense in depth)
        if getattr(db_obj, "organization_id", None) != organization_id:
            raise ValueError("Cross-tenant update attempted")
            
        obj_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        for field in obj_data:
            if field in update_data and field != "organization_id": # prevent changing org_id
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID, organization_id: UUID) -> Optional[ModelType]:
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.organization_id == organization_id
        )
        obj = db.execute(stmt).scalar_one_or_none()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

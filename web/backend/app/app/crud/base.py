from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, created_by: Optional[int] = None
    ) -> List[ModelType]:
        query = db.query(self.model)
        if type(created_by) is int and hasattr(self.model, "created_by"):
            query = query.filter(self.model.created_by == created_by)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, created_by: Optional[int] = None) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        if (hasattr(db_obj, "created_at")):
            db_obj.created_at = datetime.utcnow()
        if (hasattr(db_obj, "created_by") and type(created_by) is int):
            db_obj.created_by = created_by
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
        updated_by: int = None
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if (hasattr(db_obj, 'updated_at')):
            db_obj.updated_at = datetime.utcnow()
        if (hasattr(db_obj, 'updated_by') and type(updated_by) is int):
            db_obj.updated_by = updated_by

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(
        self, db: Session,
        *,
        created_by: Optional[int] = None
    ) -> int:
        query = db.query(func.count(self.model.id))
        if (created_by is not None):
            query = query.filter(self.model.created_by == created_by)
        return query.scalar()

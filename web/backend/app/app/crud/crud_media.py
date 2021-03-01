from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaUpdate


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):
    def create_with_creator(
        self, db: Session, *, obj_in: MediaCreate, created_by: int
    ) -> Media:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_by=created_by, created_at=datetime.utcnow())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_creator(
        self, db: Session, *, created_by: int, skip: int = 0, limit: int = 100
    ) -> List[Media]:
        return (
            db.query(self.model)
            .filter(Media.created_by == created_by)
            .offset(skip)
            .limit(limit)
            .all()
        )


media = CRUDMedia(Media)

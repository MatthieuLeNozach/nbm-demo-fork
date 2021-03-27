from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaUpdate


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):
    def get_duration_sum(self, db: Session, *, created_by: Optional[int] = None) -> int:
        query = db.query(func.sum(Media.duration))

        if (created_by is not None):
            query = query.filter(Media.created_by == created_by)

        return query.scalar()

media = CRUDMedia(Media)

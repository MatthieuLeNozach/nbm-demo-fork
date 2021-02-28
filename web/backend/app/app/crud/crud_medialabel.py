from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.medialabel import MediaLabel
from app.schemas.medialabel import MediaLabelCreate, MediaLabelUpdate


class CRUDMediaLabel(CRUDBase[MediaLabel, MediaLabelCreate, MediaLabelUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: MediaLabelCreate, owner_id: int
    ) -> MediaLabel:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_by=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[MediaLabel]:
        return (
            db.query(self.model)
            .filter(MediaLabel.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


medialabel = CRUDMediaLabel(MediaLabel)

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.standardlabel import StandardLabel
from app.schemas.standardlabel import StandardLabelCreate, StandardLabelUpdate


class CRUDStandardLabel(CRUDBase[StandardLabel, StandardLabelCreate, StandardLabelUpdate]):
    def get_multi_by_name(
        self, db: Session, *, name: str, skip: int = 0, limit: int = 100
    ) -> List[StandardLabel]:
        return (
            db.query(self.model)
            .filter(StandardLabel.name.ilike(f"%{name}%"))
            .order_by(StandardLabel.name)
            .offset(skip)
            .limit(limit)
            .all()
        )

standardlabel = CRUDStandardLabel(StandardLabel)

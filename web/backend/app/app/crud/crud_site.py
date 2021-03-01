from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate

from datetime import datetime

class CRUDSite(CRUDBase[Site, SiteCreate, SiteUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: SiteCreate, user_id: int
    ) -> Site:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_by=user_id, created_at=datetime.utcnow())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Site]:
        return (
            db.query(self.model)
            .filter(Site.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


site = CRUDSite(Site)

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate

from datetime import datetime

class CRUDSite(CRUDBase[Site, SiteCreate, SiteUpdate]):
    def get_multi_public(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Site]:
        return (
            db.query(self.model)
            .filter(Site.is_private == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

site = CRUDSite(Site)

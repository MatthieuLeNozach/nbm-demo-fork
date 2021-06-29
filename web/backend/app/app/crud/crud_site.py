from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.models import Site, User
from app.schemas.site import SiteCreate, SiteUpdate

from datetime import datetime

class CRUDSite(CRUDBase[Site, SiteCreate, SiteUpdate]):
    def count_public(
        self, db: Session,
        *,
        created_by: Optional[int] = None
    ) -> int:
        return (db
                .query(func.count(self.model.id))
                .filter(
                    or_(Site.is_private == False, Site.created_by == created_by)
                )
                .scalar())


    def get_multi_public(
        self, db: Session, *,
        current_user: int,
        skip: int = 0,
        limit: int = 100,
        name: str = None,
        created_by: int = None
    ) -> List[Site]:
        query = (db.query(self.model).filter(
                    or_(Site.is_private == False, Site.created_by == current_user)
                ))

        if name is not None:
            query = query.filter(Site.name.ilike(f"%{name}%"))

        if created_by is not None:
            query = query.filter(self.model.created_by == created_by)

        return query.order_by(Site.id).offset(skip).limit(limit).all()


site = CRUDSite(Site)

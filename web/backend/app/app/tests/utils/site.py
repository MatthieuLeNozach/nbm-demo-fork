from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.site import SiteCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.faker import fake

def create_random_site(db: Session, *, created_by: Optional[int] = None, is_private: Optional[bool] = None) -> models.Site:
    if created_by is None:
        creator = create_random_user(db)
        created_by = creator.id

    geo_info = fake.location_on_land()

    if is_private is None:
        is_private = fake.boolean()
    site_in = SiteCreate(latitude = geo_info[0],
                        longitude = geo_info[1],
                        name = geo_info[2],
                        is_private = is_private)
    return crud.site.create(db=db, obj_in=site_in, created_by=created_by)

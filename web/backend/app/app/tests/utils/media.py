from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.media import MediaCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.site import create_random_site
from app.tests.utils.device import create_random_device
from app.tests.utils.faker import fake


def create_random_media(db: Session, *, created_by: Optional[int] = None) -> models.Media:
    if created_by is None:
        user = create_random_user(db)
        created_by = user.id

    file_source = fake.sentence()
    file_url = f"{fake.uri()}{fake.file_name()}"
    type = "sound"

    site = create_random_site(db)
    device = create_random_device(db)

    begin_date = fake.date_time_this_century()
    duration = fake.time_object()

    media_in = MediaCreate(file_source=file_source,
                            file_url=file_url,
                            type=type,
                            site_id=site.id,
                            begin_date=begin_date,
                            device_id=device.id,
                            duration=duration)

    return crud.media.create(db=db, obj_in=media_in, created_by=created_by)

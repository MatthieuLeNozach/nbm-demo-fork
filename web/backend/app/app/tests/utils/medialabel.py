from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.medialabel import MediaLabelCreate

from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.faker import fake

def create_random_medialabel(db: Session, *, created_by: Optional[int] = None) -> models.MediaLabel:
    if created_by is None:
        creator = create_random_user(db)
        created_by = creator.id

    media = create_random_media(db)

    begin_time = fake.pyfloat()
    end_time = fake.pyfloat()
    low_freq = fake.pyfloat()
    high_freq = fake.pyfloat()
    label = fake.sentence()

    medialabel_in = MediaLabelCreate(begin_time=begin_time,
                            end_time=end_time,
                            low_freq=low_freq,
                            high_freq=high_freq,
                            label=label,
                            media_id=media.id)

    return crud.medialabel.create(db=db, obj_in=medialabel_in, created_by=created_by)

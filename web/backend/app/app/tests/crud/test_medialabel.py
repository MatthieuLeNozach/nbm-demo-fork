from sqlalchemy.orm import Session

from app import crud
from app.schemas.medialabel import MediaLabelCreate, MediaLabelUpdate
from app.tests.utils.medialabel import create_random_medialabel
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.standardlabel import create_random_standardlabel
from datetime import datetime
from app.tests.utils.faker import fake
from math import ceil, floor

def test_create_medialabel(db: Session) -> None:
    creator = create_random_user(db)
    media = create_random_media(db)
    label = create_random_standardlabel(db)

    begin_time = fake.pyfloat(positive=True)
    end_time = fake.pyfloat(positive=True, min_value=ceil(begin_time))
    low_freq = fake.pyfloat(positive=True)
    high_freq = fake.pyfloat(positive=True, min_value=ceil(low_freq))

    medialabel_in = MediaLabelCreate(begin_time=begin_time,
                            end_time=end_time,
                            low_freq=low_freq,
                            high_freq=high_freq,
                            label_id=label.id,
                            media_id=media.id)

    medialabel = crud.medialabel.create(db=db, obj_in=medialabel_in, created_by=creator.id)

    assert medialabel.begin_time == begin_time
    assert medialabel.end_time == end_time
    assert medialabel.low_freq == low_freq
    assert medialabel.high_freq == high_freq
    assert medialabel.label_id == label.id
    assert medialabel.created_by == creator.id
    assert type(medialabel.id) is int
    assert type(medialabel.created_at) is datetime
    assert medialabel.updated_by is None
    assert medialabel.updated_at is None


def test_get_medialabel(db: Session) -> None:
    medialabel = create_random_medialabel(db)
    stored_medialabel = crud.medialabel.get(db=db, id=medialabel.id)
    assert stored_medialabel is not None
    assert medialabel.begin_time == stored_medialabel.begin_time
    assert medialabel.end_time == stored_medialabel.end_time
    assert medialabel.low_freq == stored_medialabel.low_freq
    assert medialabel.high_freq == stored_medialabel.high_freq
    assert medialabel.label_id == stored_medialabel.label_id
    assert medialabel.id == stored_medialabel.id
    assert medialabel.created_at == stored_medialabel.created_at
    assert medialabel.created_by == stored_medialabel.created_by
    assert stored_medialabel.updated_by is None
    assert stored_medialabel.updated_at is None

def test_get_medialabels_by_creator(db: Session) -> None:
    create_random_medialabel(db)

    creator = create_random_user(db)
    owned_medialabel = create_random_medialabel(db, created_by=creator.id)

    medialabels = crud.medialabel.get_multi(db=db, filters={"created_by": creator.id})

    assert type(medialabels) is list
    assert len(medialabels) == 1 #allow us to test if one AND ONLY one medialabel has been created with creator.id

    tested_medialabel = medialabels[0]

    assert tested_medialabel.begin_time == owned_medialabel.begin_time
    assert tested_medialabel.end_time == owned_medialabel.end_time
    assert tested_medialabel.low_freq == owned_medialabel.low_freq
    assert tested_medialabel.high_freq == owned_medialabel.high_freq
    assert tested_medialabel.label_id == owned_medialabel.label_id
    assert tested_medialabel.id == owned_medialabel.id
    assert tested_medialabel.created_at == owned_medialabel.created_at
    assert tested_medialabel.created_by == owned_medialabel.created_by
    assert tested_medialabel.updated_by is None
    assert tested_medialabel.updated_at is None

def test_update_medialabel(db: Session) -> None:
    medialabel = create_random_medialabel(db)

    assert medialabel.updated_at is None
    assert medialabel.updated_by is None

    new_begin_time = fake.pyfloat(positive=True, max_value=floor(medialabel.end_time))
    medialabel_update_in = MediaLabelUpdate(begin_time=new_begin_time) #just want to change begintime
    updated_medialabel = crud.medialabel.update(db=db, db_obj=medialabel, obj_in=medialabel_update_in, updated_by=medialabel.created_by)

    assert updated_medialabel.begin_time == new_begin_time
    assert medialabel.end_time == updated_medialabel.end_time
    assert medialabel.low_freq == updated_medialabel.low_freq
    assert medialabel.high_freq == updated_medialabel.high_freq
    assert medialabel.label_id == updated_medialabel.label_id
    assert medialabel.id == updated_medialabel.id
    assert medialabel.created_at == updated_medialabel.created_at
    assert medialabel.created_by == updated_medialabel.created_by
    assert type(updated_medialabel.updated_at) is datetime
    assert medialabel.updated_at != updated_medialabel.created_at
    assert type(medialabel.updated_by) is int
    assert medialabel.updated_by == updated_medialabel.created_by


def test_delete_medialabel(db: Session) -> None:
    medialabel = create_random_medialabel(db)
    removed_medialabel = crud.medialabel.remove(db=db, id=medialabel.id)
    after_remove_medialabel = crud.medialabel.get(db=db, id=medialabel.id)
    assert after_remove_medialabel is None
    #following lines confirm that removed_medialabel data are equal to medialabel when removing
    assert medialabel.begin_time == removed_medialabel.begin_time
    assert medialabel.end_time == removed_medialabel.end_time
    assert medialabel.low_freq == removed_medialabel.low_freq
    assert medialabel.high_freq == removed_medialabel.high_freq
    assert medialabel.label_id == removed_medialabel.label_id
    assert medialabel.id == removed_medialabel.id
    assert medialabel.created_at == removed_medialabel.created_at
    assert medialabel.created_by == removed_medialabel.created_by
    assert removed_medialabel.updated_at is None
    assert removed_medialabel.updated_by is None

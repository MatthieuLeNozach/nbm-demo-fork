from sqlalchemy.orm import Session

from app import crud
from app.schemas.medialabel import MediaLabelCreate, MediaLabelUpdate
from app.tests.utils.medialabel import create_random_medialabel
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from datetime import datetime
from app.tests.utils.faker import fake

def test_create_medialabel(db: Session) -> None:
    creator = create_random_user(db)
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

    medialabel = crud.medialabel.create(db=db, obj_in=medialabel_in, created_by=creator.id)

    assert medialabel.begin_time == begin_time
    assert medialabel.end_time == end_time
    assert medialabel.low_freq == low_freq
    assert medialabel.high_freq == high_freq
    assert medialabel.label == label
    assert medialabel.created_by == creator.id
    assert type(medialabel.id) is int
    assert type(medialabel.created_at) is datetime
    assert medialabel.updated_by is None
    assert medialabel.updated_at is None


def test_get_medialabel(db: Session) -> None:
    medialabel = create_random_medialabel(db)
    stored_medialabel = crud.medialabel.get(db=db, id=medialabel.id)
    assert stored_medialabel
    assert medialabel.begin_time == stored_medialabel.begin_time
    assert medialabel.end_time == stored_medialabel.end_time
    assert medialabel.low_freq == stored_medialabel.low_freq
    assert medialabel.high_freq == stored_medialabel.high_freq
    assert medialabel.label == stored_medialabel.label
    assert medialabel.id == stored_medialabel.id
    assert medialabel.created_at == stored_medialabel.created_at
    assert medialabel.created_by == stored_medialabel.created_by
    assert stored_medialabel.updated_by is None
    assert stored_medialabel.updated_at is None

def test_get_medialabels_by_creator(db: Session) -> None:
    create_random_medialabel(db)

    creator = create_random_user(db)
    owned_medialabel = create_random_medialabel(db, created_by=creator.id)

    medialabels = crud.medialabel.get_multi(db=db, created_by=creator.id)

    assert type(medialabels) is list
    assert len(medialabels) == 1 #allow us to test if one AND ONLY one medialabel has been created with creator.id 
    
    tested_medialabel = medialabels[0]
    
    assert tested_medialabel.begin_time == owned_medialabel.begin_time
    assert tested_medialabel.end_time == owned_medialabel.end_time
    assert tested_medialabel.low_freq == owned_medialabel.low_freq
    assert tested_medialabel.high_freq == owned_medialabel.high_freq
    assert tested_medialabel.label == owned_medialabel.label
    assert tested_medialabel.id == owned_medialabel.id
    assert tested_medialabel.created_at == owned_medialabel.created_at
    assert tested_medialabel.created_by == owned_medialabel.created_by
    assert tested_medialabel.updated_by is None
    assert tested_medialabel.updated_at is None

def test_update_medialabel(db: Session) -> None:
    medialabel = create_random_medialabel(db)

    assert medialabel.updated_at is None
    assert medialabel.updated_by is None

    begin_time2 = fake.pyfloat()
    medialabel_update = MediaLabelUpdate(begin_time=begin_time2) #just want to change begintime 
    medialabel2 = crud.medialabel.update(db=db, db_obj=medialabel, obj_in=medialabel_update, updated_by=medialabel.created_by)

    assert medialabel2.begin_time == begin_time2
    assert medialabel.end_time == medialabel2.end_time
    assert medialabel.low_freq == medialabel2.low_freq
    assert medialabel.high_freq == medialabel2.high_freq
    assert medialabel.label == medialabel2.label
    assert medialabel.id == medialabel2.id
    assert medialabel.created_at == medialabel2.created_at
    assert medialabel.created_by == medialabel2.created_by
    assert type(medialabel2.updated_at) is datetime
    assert medialabel.updated_at != medialabel2.created_at
    assert type(medialabel.updated_by) is int
    assert medialabel.updated_by == medialabel2.created_by


def test_delete_medialabel(db: Session) -> None:
    medialabel = create_random_medialabel(db)
    medialabel2 = crud.medialabel.remove(db=db, id=medialabel.id)
    medialabel3 = crud.medialabel.get(db=db, id=medialabel.id)
    assert medialabel3 is None
    #following lines confirm that medialabel2 data are equal to medialabel when removing 
    assert medialabel.begin_time == medialabel2.begin_time
    assert medialabel.end_time == medialabel2.end_time
    assert medialabel.low_freq == medialabel2.low_freq
    assert medialabel.high_freq == medialabel2.high_freq
    assert medialabel.label == medialabel2.label
    assert medialabel.id == medialabel2.id
    assert medialabel.created_at == medialabel2.created_at
    assert medialabel.created_by == medialabel2.created_by
    assert medialabel2.updated_at is None
    assert medialabel2.updated_by is None

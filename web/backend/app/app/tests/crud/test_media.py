from sqlalchemy.orm import Session

from app import crud
from app.schemas.media import MediaCreate, MediaUpdate
from app.tests.utils.media import create_random_media
from app.tests.utils.site import create_random_site
from app.tests.utils.device import create_random_device
from app.tests.utils.user import create_random_user

from datetime import datetime
from app.tests.utils.faker import fake

def test_create_media(db: Session) -> None:
    file_source = fake.sentence()
    file_url = f"{fake.uri()}{fake.file_name()}"
    file_type = "sound"

    creator = create_random_user(db)
    site = create_random_site(db)
    device = create_random_device(db)

    begin_date = fake.date_time_this_century()
    duration = fake.time_object()

    media_in = MediaCreate(file_source=file_source,
                            file_url=file_url,
                            type=file_type,
                            site_id=site.id,
                            begin_date=begin_date,
                            device_id=device.id,
                            duration=duration)

    media = crud.media.create(db=db, obj_in=media_in, created_by=creator.id)

    assert media.file_source == file_source
    assert media.file_url == file_url
    assert media.type == file_type
    assert media.site_id == site.id
    assert media.begin_date == begin_date
    assert media.device_id == device.id
    assert media.duration == duration
    assert media.created_by == creator.id
    assert type(media.id) is int
    assert type(media.created_at) is datetime
    assert media.updated_by is None
    assert media.updated_at is None


def test_get_media(db: Session) -> None:
    media = create_random_media(db)
    stored_media = crud.media.get(db=db, id=media.id)
    assert stored_media is not None
    assert media.file_source == stored_media.file_source
    assert media.file_url == stored_media.file_url
    assert media.type == stored_media.type
    assert media.site_id == stored_media.site_id
    assert media.begin_date == stored_media.begin_date
    assert media.device_id == stored_media.device_id
    assert media.duration == stored_media.duration
    assert media.id == stored_media.id
    assert media.created_at == stored_media.created_at
    assert media.created_by == stored_media.created_by
    assert stored_media.updated_by is None
    assert stored_media.updated_at is None

def test_get_mediae_by_creator(db: Session) -> None:
    create_random_media(db)

    creator = create_random_user(db)
    owned_media = create_random_media(db, created_by=creator.id)

    mediae = crud.media.get_multi(db=db, filters={"created_by": creator.id})

    assert type(mediae) is list
    assert len(mediae) == 1 #allow us to test if one AND ONLY one media has been created with creator.id

    tested_media = mediae[0]

    assert tested_media.file_source == owned_media.file_source
    assert tested_media.file_url == owned_media.file_url
    assert tested_media.type == owned_media.type
    assert tested_media.site_id == owned_media.site_id
    assert tested_media.begin_date == owned_media.begin_date
    assert tested_media.device_id == owned_media.device_id
    assert tested_media.duration == owned_media.duration
    assert tested_media.id == owned_media.id
    assert tested_media.created_by == creator.id
    assert tested_media.updated_by is None
    assert tested_media.updated_at is None

def test_update_media(db: Session) -> None:
    media = create_random_media(db)

    assert media.updated_at is None
    assert media.updated_by is None

    new_file_source = fake.sentence()
    media_update_in = MediaUpdate(file_source=new_file_source) #just want to change filesource
    updated_media = crud.media.update(db=db, db_obj=media, obj_in=media_update_in, updated_by=media.created_by)

    assert updated_media.file_source == new_file_source
    assert media.file_url == updated_media.file_url
    assert media.type == updated_media.type
    assert media.site_id == updated_media.site_id
    assert media.begin_date == updated_media.begin_date
    assert media.device_id == updated_media.device_id
    assert media.duration == updated_media.duration
    assert media.id == updated_media.id
    assert media.created_at == updated_media.created_at
    assert media.created_by == updated_media.created_by
    assert type(updated_media.updated_at) is datetime
    assert media.updated_at != updated_media.created_at
    assert media.updated_by == updated_media.created_by


def test_delete_media(db: Session) -> None:
    media = create_random_media(db)
    removed_media = crud.media.remove(db=db, id=media.id)
    after_remove_media = crud.media.get(db=db, id=media.id)
    assert after_remove_media is None
    #following lines confirm that removed_media data are equal to media when removing
    assert media.file_source == removed_media.file_source
    assert media.file_url == removed_media.file_url
    assert media.type == removed_media.type
    assert media.site_id == removed_media.site_id
    assert media.begin_date == removed_media.begin_date
    assert media.device_id == removed_media.device_id
    assert media.duration == removed_media.duration
    assert media.id == removed_media.id
    assert media.created_at == removed_media.created_at
    assert media.created_by == removed_media.created_by
    assert removed_media.updated_at is None
    assert removed_media.updated_by is None

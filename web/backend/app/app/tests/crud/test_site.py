from sqlalchemy.orm import Session

from app import crud
from app.schemas.site import SiteCreate, SiteUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.site import create_random_site

from datetime import datetime
from app.tests.utils.faker import fake

def test_create_site(db: Session) -> None:
    user = create_random_user(db)

    geo_info = fake.location_on_land()
    is_private = fake.boolean()
    site_in = SiteCreate(latitude = geo_info[0], longitude = geo_info[1], name = geo_info[2], is_private = is_private)

    site = crud.site.create(db=db, obj_in=site_in, created_by=user.id)

    assert site.latitude == float(geo_info[0])
    assert site.longitude == float(geo_info[1])
    assert site.name == geo_info[2]
    assert site.is_private == is_private
    assert site.created_by == user.id
    assert type(site.created_at) is datetime

def test_get_site(db: Session) -> None:
    site = create_random_site(db)
    stored_site = crud.site.get(db=db, id=site.id)

    assert stored_site is not None
    assert site.latitude == stored_site.latitude
    assert site.longitude == stored_site.longitude
    assert site.name == stored_site.name
    assert site.is_private == stored_site.is_private
    assert site.created_by == stored_site.created_by
    assert site.created_at == stored_site.created_at
    assert stored_site.updated_by is None
    assert stored_site.updated_at is None

def test_get_sites_by_creator(db: Session) -> None:
    create_random_site(db)

    creator = create_random_user(db)
    owned_site = create_random_site(db, created_by=creator.id)

    sites = crud.site.get_multi(db=db, created_by=creator.id)

    assert type(sites) is list
    assert len(sites) == 1

    tested_site = sites[0]

    assert tested_site.latitude == owned_site.latitude
    assert tested_site.longitude == owned_site.longitude
    assert tested_site.name == owned_site.name
    assert tested_site.is_private == owned_site.is_private
    assert tested_site.created_at == owned_site.created_at
    assert tested_site.created_by == creator.id
    assert tested_site.updated_by is None
    assert tested_site.updated_at is None

def test_update_site(db: Session) -> None:
    site = create_random_site(db)

    assert site.updated_at is None
    assert site.updated_by is None

    new_name = fake.sentence()
    site_update_in = SiteUpdate(name=new_name)
    updated_site = crud.site.update(db=db, db_obj=site, obj_in=site_update_in, updated_by=site.created_by)

    assert site.id == updated_site.id
    assert site.latitude == updated_site.latitude
    assert site.longitude == updated_site.longitude
    assert site.is_private == updated_site.is_private
    assert updated_site.name == new_name
    assert site.created_by == updated_site.created_by
    assert site.created_at == updated_site.created_at
    assert type(updated_site.updated_at) is datetime
    assert updated_site.updated_at != site.created_at
    assert updated_site.updated_by == site.created_by


def test_delete_site(db: Session) -> None:
    site = create_random_site(db)
    removed_site = crud.site.remove(db=db, id=site.id)
    after_remove_site = crud.site.get(db=db, id=site.id)
    assert after_remove_site is None
    assert site.latitude == removed_site.latitude
    assert site.longitude == removed_site.longitude
    assert site.is_private == removed_site.is_private
    assert site.name == removed_site.name

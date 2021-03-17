from sqlalchemy.orm import Session

from app import crud
from app.schemas.standardlabel import StandardLabelCreate, StandardLabelUpdate
from app.tests.utils.standardlabel import create_random_standardlabel
from app.tests.utils.species import create_random_species
from app.tests.utils.user import create_random_user
from datetime import datetime
from app.tests.utils.faker import fake

def test_create_standardlabel(db: Session) -> None:
    name = fake.sentence()
    species = create_random_species(db)
    standardlabel_in = StandardLabelCreate(name=name,
                            species_id=species.id)

    creator = create_random_user(db)
    standardlabel = crud.standardlabel.create(db=db, obj_in=standardlabel_in, created_by=creator.id)

    assert standardlabel.name == name
    assert standardlabel.species_id == species.id
    assert standardlabel.created_by == creator.id
    assert type(standardlabel.id) is int
    assert type(standardlabel.created_at) is datetime
    assert standardlabel.updated_by is None
    assert standardlabel.updated_at is None


def test_get_standardlabel(db: Session) -> None:
    standardlabel = create_random_standardlabel(db)
    stored_standardlabel = crud.standardlabel.get(db=db, id=standardlabel.id)
    assert stored_standardlabel is not None
    assert standardlabel.name == stored_standardlabel.name
    assert standardlabel.species_id == stored_standardlabel.species_id
    assert standardlabel.id == stored_standardlabel.id
    assert standardlabel.created_at == stored_standardlabel.created_at
    assert standardlabel.created_by == stored_standardlabel.created_by
    assert stored_standardlabel.updated_by is None
    assert stored_standardlabel.updated_at is None

def test_get_standardlabels_by_creator(db: Session) -> None:
    create_random_standardlabel(db)

    creator = create_random_user(db)
    owned_standardlabel = create_random_standardlabel(db, created_by=creator.id)

    standardlabels = crud.standardlabel.get_multi(db=db, created_by=creator.id)

    assert type(standardlabels) is list
    assert len(standardlabels) == 1 #allow us to test if one AND ONLY one standardlabel has been created with creator.id

    tested_standardlabel = standardlabels[0]

    assert tested_standardlabel.name == owned_standardlabel.name
    assert tested_standardlabel.species_id == owned_standardlabel.species_id
    assert tested_standardlabel.id == owned_standardlabel.id
    assert tested_standardlabel.created_at == owned_standardlabel.created_at
    assert tested_standardlabel.created_by == owned_standardlabel.created_by
    assert tested_standardlabel.updated_by is None
    assert tested_standardlabel.updated_at is None

def test_update_standardlabel(db: Session) -> None:
    standardlabel = create_random_standardlabel(db)

    assert standardlabel.updated_at is None
    assert standardlabel.updated_by is None

    new_name = fake.sentence()
    standardlabel_in = StandardLabelUpdate(name=new_name) #just want to change begintime
    updated_standardlabel = crud.standardlabel.update(db=db, db_obj=standardlabel, obj_in=standardlabel_in, updated_by=standardlabel.created_by)

    assert updated_standardlabel.name == new_name
    assert standardlabel.species_id == updated_standardlabel.species_id
    assert standardlabel.id == updated_standardlabel.id
    assert standardlabel.created_at == updated_standardlabel.created_at
    assert standardlabel.created_by == updated_standardlabel.created_by
    assert type(updated_standardlabel.updated_at) is datetime
    assert standardlabel.updated_at != updated_standardlabel.created_at
    assert type(standardlabel.updated_by) is int
    assert standardlabel.updated_by == updated_standardlabel.created_by


def test_delete_standardlabel(db: Session) -> None:
    standardlabel = create_random_standardlabel(db)
    removed_standardlabel = crud.standardlabel.remove(db=db, id=standardlabel.id)
    after_remove_standardlabel = crud.standardlabel.get(db=db, id=standardlabel.id)
    assert after_remove_standardlabel is None
    #following lines confirm that removed_standardlabel data are equal to standardlabel when removing
    assert standardlabel.name == removed_standardlabel.name
    assert standardlabel.species_id == removed_standardlabel.species_id
    assert standardlabel.id == removed_standardlabel.id
    assert standardlabel.created_at == removed_standardlabel.created_at
    assert standardlabel.created_by == removed_standardlabel.created_by
    assert removed_standardlabel.updated_at is None
    assert removed_standardlabel.updated_by is None

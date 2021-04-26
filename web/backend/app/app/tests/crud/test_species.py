from sqlalchemy.orm import Session

from app import crud
from app.schemas.species import SpeciesCreate, SpeciesUpdate
from app.tests.utils.species import create_random_species
from app.tests.utils.faker import fake

def test_create_species(db: Session) -> None:
    name = fake.sentence()
    is_bird = fake.boolean()
    code = fake.pyint()
    species_in = SpeciesCreate(name=name, is_bird=is_bird, code=code)
    species = crud.species.create(db=db, obj_in=species_in)

    assert species.name == name
    assert species.is_bird == is_bird
    assert species.code == code


def test_get_species(db: Session) -> None:
    species = create_random_species(db)
    stored_species = crud.species.get(db=db, id=species.id)

    assert stored_species is not None
    assert species.name == stored_species.name
    assert species.is_bird == stored_species.is_bird
    assert species.code == stored_species.code
    assert species.id == stored_species.id

def test_get_multiple_species(db: Session) -> None:
    create_random_species(db)
    create_random_species(db)
    multiple_species = crud.species.get_multi(db=db)

    assert type(multiple_species) is list
    assert len(multiple_species) > 1

    tested_species = multiple_species[0]

    assert type(tested_species.name) is str
    assert type(tested_species.is_bird) is bool
    assert type(tested_species.code) is int
    assert type(tested_species.id) is int

def test_update_species(db: Session) -> None:
    species = create_random_species(db)

    new_name = fake.sentence()
    species_in = SpeciesUpdate(name=new_name) #just want to change name
    updated_species = crud.species.update(db=db, db_obj=species, obj_in=species_in)

    assert updated_species.name == new_name
    assert species.is_bird == updated_species.is_bird
    assert species.code == updated_species.code
    assert species.id == updated_species.id


def test_delete_species(db: Session) -> None:
    created_species = create_random_species(db)
    removed_species = crud.species.remove(db=db, id=created_species.id)
    after_remove_species = crud.species.get(db=db, id=created_species.id)
    assert after_remove_species is None
    #following lines confirm that created_species data are equal to removed_species when removing
    assert created_species.name == removed_species.name
    assert created_species.is_bird == removed_species.is_bird
    assert created_species.code == removed_species.code
    assert created_species.id == removed_species.id

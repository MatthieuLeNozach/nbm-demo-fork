from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.species import SpeciesCreate

from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.faker import fake

def create_random_species(db: Session) -> models.Species:
    species_in = SpeciesCreate(name=fake.sentence(), is_bird=fake.boolean(), code=fake.pyint())
    return crud.species.create(db=db, obj_in=species_in)

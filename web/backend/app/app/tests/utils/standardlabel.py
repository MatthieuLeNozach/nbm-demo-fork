from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.standardlabel import StandardLabelCreate

from app.tests.utils.species import create_random_species
from app.tests.utils.user import create_random_user
from app.tests.utils.faker import fake


def create_random_standardlabel(
    db: Session, *, created_by: Optional[int] = None, species_id: Optional[int] = None
) -> models.StandardLabel:
    if created_by is None:
        creator = create_random_user(db)
        created_by = creator.id

    if species_id is None:
        species = create_random_species(db)
        species_id = species.id

    standardlabel_in = StandardLabelCreate(name=fake.sentence(), species_id=species_id)

    return crud.standardlabel.create(db=db, obj_in=standardlabel_in, created_by=created_by)

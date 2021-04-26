from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.schemas import SpeciesCreate, StandardLabelCreate, User
from app.db import base  # noqa: F401

import json

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

initial_data_path = 'app/db/initial_data/'

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    super_user = create_super_user(db)
    create_species_and_labels(db, super_user)
    create_standardlabels(db, super_user)


def create_super_user(db: Session):
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if user:
        return user

    user_in = schemas.UserCreate(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    return crud.user.create(db, obj_in=user_in)  # noqa: F841


def create_species_and_labels(db: Session, super_user: User):
    with open(initial_data_path + 'species.json') as json_file:
        species_from_json = json.load(json_file)
        for current_species_data in species_from_json:
            species_from_db = crud.species.get_multi_by_name(db, name=current_species_data['name'])

            if len(species_from_db) == 0:
                species_in = SpeciesCreate(
                    name=current_species_data['name'],
                    is_bird=current_species_data['is_bird'],
                    code=current_species_data['code']
                )
                species = crud.species.create(db=db, obj_in=species_in)
            else:
                species = species_from_db[0]

            standardlabel_from_db = crud.standardlabel.get_multi_by_name(db, name=species.name)

            if len(standardlabel_from_db) == 0:
                standard_label_in = StandardLabelCreate(name=species.name, species_id=species.id)
                crud.standardlabel.create(db=db, obj_in=standard_label_in, created_by=super_user.id)

            if not 'standardlabels' in current_species_data:
                continue

            for current_standardlabel_data in current_species_data['standardlabels']:
                standardlabel_from_db = crud.standardlabel.get_multi_by_name(db, name=current_standardlabel_data['name'])

                if len(standardlabel_from_db) == 0:
                    standard_label_in = StandardLabelCreate(name=current_standardlabel_data['name'], species_id=species.id)
                    crud.standardlabel.create(db=db, obj_in=standard_label_in, created_by=super_user.id)


def create_standardlabels(db: Session, super_user: User):
    with open(initial_data_path + 'standardlabels.json') as json_file:
        standardlabels_from_json = json.load(json_file)
        for current_standardlabel_data in standardlabels_from_json:
            standardlabel_from_db = crud.standardlabel.get_multi_by_name(db, name=current_standardlabel_data['name'])
            if len(standardlabel_from_db) == 0:
                standardlabel_in = StandardLabelCreate(name=current_standardlabel_data['name'])
                crud.standardlabel.create(db=db, obj_in=standardlabel_in, created_by=super_user.id)

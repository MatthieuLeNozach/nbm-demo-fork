from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.species import Species
from app.schemas.species import SpeciesCreate, SpeciesUpdate


class CRUDSpecies(CRUDBase[Species, SpeciesCreate, SpeciesUpdate]):
    pass

species = CRUDSpecies(Species)

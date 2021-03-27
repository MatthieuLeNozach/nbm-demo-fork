from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.models import Species, MediaLabel, StandardLabel
from app.schemas.species import SpeciesCreate, SpeciesUpdate


class CRUDSpecies(CRUDBase[Species, SpeciesCreate, SpeciesUpdate]):
    def get_count_by_annotations(self, db: Session, *, annotated_by: Optional[int] = None) -> int:
        query = (db.query(Species)
                    .join(StandardLabel, Species.id == StandardLabel.species_id)
                    .join(MediaLabel, StandardLabel.id == MediaLabel.label_id)
                    .group_by(Species.id))

        if (annotated_by is not None):
            query = query.filter(MediaLabel.created_by == annotated_by)

        return query.count()


species = CRUDSpecies(Species)

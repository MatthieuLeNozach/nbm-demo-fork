from typing import List

from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models import Species, MediaLabel, StandardLabel
from app.schemas.statistics import StatisticsAnnotationSpecies


class CRUDStatistics:
    def get_species_annotations(self, db: Session) -> List[StatisticsAnnotationSpecies]:
        query = (
            select(Species.id, Species.name, func.count(MediaLabel.id).label("total"))
            .join(StandardLabel, MediaLabel.label_id == StandardLabel.id)
            .join(Species, StandardLabel.species_id == Species.id)
            .group_by(Species.id)
            .order_by(text('total DESC'))
        )

        return db.execute(query).all()


statistics = CRUDStatistics()

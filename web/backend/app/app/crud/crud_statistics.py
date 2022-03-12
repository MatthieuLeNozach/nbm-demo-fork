from typing import List, Optional

from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models import Species, MediaLabel, StandardLabel, User
from app.schemas.statistics import StatisticsAnnotationSpecies


class CRUDStatistics:
    def get_species_annotations(self, db: Session) -> List[StatisticsAnnotationSpecies]:
        query = (
            select(Species.id, Species.name, func.count(MediaLabel.id).label("total"))
            .join(StandardLabel, MediaLabel.label_id == StandardLabel.id)
            .join(Species, StandardLabel.species_id == Species.id)
            .group_by(Species.id)
            .order_by(text("total DESC"))
        )

        return db.execute(query).all()

    def get_species_annotations_by_user(self, db: Session, user: User) -> List[StatisticsAnnotationSpecies]:
        query = (
            select(
                Species.id,
                Species.name,
                func.count(Species.name).label("total"),
                MediaLabel.created_by,
            )
            .join(StandardLabel, MediaLabel.label_id == StandardLabel.id)
            .join(Species, StandardLabel.species_id == Species.id)
            .where(MediaLabel.created_by == user.id)
            .group_by(Species.name, Species.id, MediaLabel.created_by)
        )

        return db.execute(query).all()


statistics = CRUDStatistics()

from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.get("/species_annotations", response_model=List[schemas.StatisticsAnnotationSpecies])
def get_species_annotations(db: Session = Depends(deps.get_db)) -> List[schemas.StatisticsAnnotationSpecies]:
    """
    Retrieve annotations for each species.
    """
    return crud.statistics.get_species_annotations(db)

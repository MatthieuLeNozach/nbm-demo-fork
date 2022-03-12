from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api import deps


router = APIRouter()


@router.get(
    "/species_annotations",
    response_model=List[schemas.StatisticsAnnotationSpecies],
)
def get_species_annotations(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_optional_current_active_user),
) -> List[schemas.StatisticsAnnotationSpecies]:
    """
    Retrieve annotations for each species.
    """
    user_result = []

    if current_user is not None:
        user_result = crud.statistics.get_species_annotations_by_user(db, user=current_user)

    species = crud.statistics.get_species_annotations(db)
    result = [r._asdict() for r in species]
    result = [dict(item, total_by_user=0) for item in result]

    if len(user_result) > 0:
        for user_item in user_result:
            for index, item in enumerate(result):
                if item["name"] == user_item["name"]:
                    result[index]["total_by_user"] = user_item["total"]

    return result

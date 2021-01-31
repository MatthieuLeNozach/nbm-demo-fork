from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Media])
def read_mediae(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Medias.
    """
    if crud.user.is_superuser(current_user):
        mediae = crud.media.get_multi(db, skip=skip, limit=limit)
    else:
        mediae = crud.media.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return mediae

@router.post("/", response_model=schemas.Media)
def create_media(
    *,
    db: Session = Depends(deps.get_db),
    media_in: schemas.MediaCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new media.
    """
    media = crud.media.create_with_owner(db=db, obj_in=media_in, owner_id=current_user.id)
    return media
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
    created_by: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Mediae.
    """
    return crud.media.get_multi(db, skip=skip, limit=limit, created_by=created_by)

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
    media = crud.media.create(db=db, obj_in=media_in, created_by=current_user.id)
    return media

@router.get("/{id}", response_model=schemas.Media)
def read_media(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get media by ID.
    """
    media = crud.media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

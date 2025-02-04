from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.MediaLabel])
def read_medialabels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve medialabels.
    """
    return crud.medialabel.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.MediaLabel)
def create_medialabel(
    *,
    db: Session = Depends(deps.get_db),
    medialabel_in: schemas.MediaLabelCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new medialabel.
    """
    medialabel = crud.medialabel.create(db=db, obj_in=medialabel_in, created_by=current_user.id)
    return medialabel


@router.put("/{id}", response_model=schemas.MediaLabel)
def update_medialabel(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    medialabel_in: schemas.MediaLabelUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an medialabel.
    """
    medialabel = crud.medialabel.get(db=db, id=id)
    if not medialabel:
        raise HTTPException(status_code=404, detail="MediaLabel not found")
    if not crud.user.is_superuser(current_user) and (medialabel.created_by != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    medialabel = crud.medialabel.update(db=db, db_obj=medialabel, obj_in=medialabel_in, updated_by=current_user.id)
    return medialabel


@router.get("/{id}", response_model=schemas.MediaLabel)
def read_medialabel(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get medialabel by ID.
    """
    medialabel = crud.medialabel.get(db=db, id=id)
    if not medialabel:
        raise HTTPException(status_code=404, detail="MediaLabel not found")
    return medialabel


@router.delete("/{id}", response_model=schemas.MediaLabel)
def delete_medialabel(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an medialabel.
    """
    medialabel = crud.medialabel.get(db=db, id=id)
    if not medialabel:
        raise HTTPException(status_code=404, detail="MediaLabel not found")
    if not crud.user.is_superuser(current_user) and (medialabel.created_by != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    medialabel = crud.medialabel.remove(db=db, id=id)
    return medialabel

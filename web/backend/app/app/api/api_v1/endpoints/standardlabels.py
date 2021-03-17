from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

@router.get("/", response_model=List[schemas.StandardLabel])
def read_standardlabels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve standardlabels.
    """
    return crud.standardlabel.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.StandardLabel)
def create_standardlabel(
    *,
    db: Session = Depends(deps.get_db),
    standardlabel_in: schemas.StandardLabelCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new standardlabel.
    """
    standardlabel = crud.standardlabel.create(db=db, obj_in=standardlabel_in, created_by=current_user.id)
    return standardlabel


@router.put("/{id}", response_model=schemas.StandardLabel)
def update_standardlabel(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    standardlabel_in: schemas.StandardLabelUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an standardlabel.
    """
    standardlabel = crud.standardlabel.get(db=db, id=id)
    if not standardlabel:
        raise HTTPException(status_code=404, detail="StandardLabel not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    standardlabel = crud.standardlabel.update(db=db, db_obj=standardlabel, obj_in=standardlabel_in, updated_by=current_user.id)
    return standardlabel


@router.get("/{id}", response_model=schemas.StandardLabel)
def read_standardlabel(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get standardlabel by ID.
    """
    standardlabel = crud.standardlabel.get(db=db, id=id)
    if not standardlabel:
        raise HTTPException(status_code=404, detail="StandardLabel not found")
    return standardlabel


@router.delete("/{id}", response_model=schemas.StandardLabel)
def delete_standardlabel(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an standardlabel.
    """
    standardlabel = crud.standardlabel.get(db=db, id=id)
    if not standardlabel:
        raise HTTPException(status_code=404, detail="StandardLabel not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    standardlabel = crud.standardlabel.remove(db=db, id=id)
    return standardlabel

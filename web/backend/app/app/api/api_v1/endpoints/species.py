from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

@router.get("/", response_model=List[schemas.Species])
def read_multiple_species(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve multiple species.
    """
    return crud.species.get_multi(db, skip=skip, limit=limit)

@router.get("/me", response_model=List[schemas.SpeciesUser])
def read_all_species_with_user_information(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all species with the user information 
    """
    return crud.species.get_all_species_with_the_user_information(db, user=current_user, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Species)
def create_species(
    *,
    db: Session = Depends(deps.get_db),
    species_in: schemas.SpeciesCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new species.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Forbidden. Only SuperAdmin users can create devices.")

    species = crud.species.create(db=db, obj_in=species_in)
    return species


@router.put("/{id}", response_model=schemas.Species)
def update_species(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    species_in: schemas.SpeciesUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an species.
    """
    species = crud.species.get(db=db, id=id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    species = crud.species.update(db=db, db_obj=species, obj_in=species_in)
    return species


@router.get("/{id}", response_model=schemas.Species)
def read_species(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get species by ID.
    """
    species = crud.species.get(db=db, id=id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species


@router.delete("/{id}", response_model=schemas.Species)
def delete_species(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an species.
    """
    species = crud.species.get(db=db, id=id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    species = crud.species.remove(db=db, id=id)
    return species

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Site])
def read_sites(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Sites.
    """
    if crud.user.is_superuser(current_user):
        sites = crud.site.get_multi(db, skip=skip, limit=limit)
    else:
        sites = crud.site.get_multi_public(
            db=db, skip=skip, limit=limit
        )
    return sites

@router.post("/", response_model=schemas.Site)
def create_site(
    *,
    db: Session = Depends(deps.get_db),
    site_in: schemas.SiteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new site.
    """
    site = crud.site.create(db=db, obj_in=site_in, created_by=current_user.id)
    return site

@router.get("/{id}", response_model=schemas.Site)
def read_site(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get site by ID.
    """
    site = crud.site.get(db=db, id=id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

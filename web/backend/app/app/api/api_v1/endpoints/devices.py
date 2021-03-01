from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Device])
def read_devices(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Devices.
    """
    if crud.user.is_superuser(current_user):
        devices = crud.device.get_multi(db, skip=skip, limit=limit)
    else:
        devices = crud.device.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return devices

@router.post("/", response_model=schemas.Device)
def create_device(
    *,
    db: Session = Depends(deps.get_db),
    device_in: schemas.DeviceCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new device.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Forbidden. Only SuperAdmin users can create devices.")
    device = crud.device.create(db=db, obj_in=device_in)
    return device
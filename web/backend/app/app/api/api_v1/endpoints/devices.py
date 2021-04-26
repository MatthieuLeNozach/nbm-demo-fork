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
    model_name: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Devices.
    """
    if (type(model_name) is str):
        devices = crud.device.get_multi_by_model(db, skip=skip, limit=limit, model_name=model_name)
    else:
        devices = crud.device.get_multi(db, skip=skip, limit=limit)
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

    duplicatedDevices = crud.device.get_multi_by_model(db=db, model_name=device_in.model_name)
    if len(duplicatedDevices) > 0:
        raise HTTPException(status_code=409, detail="A device with the same model name already exists")

    device = crud.device.create(db=db, obj_in=device_in)
    return device

@router.get("/{id}", response_model=schemas.Device)
def read_device(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get device by ID.
    """
    device = crud.device.get(db=db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

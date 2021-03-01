from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    pass


device = CRUDDevice(Device)

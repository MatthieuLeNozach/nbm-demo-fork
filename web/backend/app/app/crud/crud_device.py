from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def get_multi_by_model(
        self, db: Session, *, device_model: str, skip: int = 0, limit: int = 100
    ) -> List[Device]:
        return (
            db.query(self.model)
            .filter(Device.device_model == device_model)
            .offset(skip)
            .limit(limit)
            .all()
        )


device = CRUDDevice(Device)

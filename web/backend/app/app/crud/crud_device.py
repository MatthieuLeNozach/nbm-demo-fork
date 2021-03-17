from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def get_multi_by_model(
        self, db: Session, *, model_name: str, skip: int = 0, limit: int = 100
    ) -> List[Device]:
        return (
            db.query(self.model)
            .filter(Device.model_name.ilike(f"%{model_name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )


device = CRUDDevice(Device)

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.device import DeviceCreate
from app.tests.utils.faker import fake


def create_random_device(db: Session) -> models.Device:
    device_model = fake.pystr()
    device_in = DeviceCreate(device_model=device_model)
    return crud.device.create(db=db, obj_in=device_in)

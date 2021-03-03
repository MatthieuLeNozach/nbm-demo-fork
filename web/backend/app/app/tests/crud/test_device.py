from sqlalchemy.orm import Session

from app import crud
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.tests.utils.device import create_random_device

from app.tests.utils.faker import fake

def test_create_device(db: Session) -> None:
    device_model = fake.pystr()
    device_in = DeviceCreate(device_model=device_model)
    device = crud.device.create(db=db, obj_in=device_in)
    assert device.device_model == device_model
    assert type(device.id) is int

def test_get_device(db: Session) -> None:
    device = create_random_device(db)
    stored_device = crud.device.get(db=db, id=device.id)
    assert stored_device is not None  
    assert device.id == stored_device.id
    assert device.device_model == stored_device.device_model


def test_update_device(db: Session) -> None:
    device = create_random_device(db)
    new_device_model = fake.pystr()
    device_update = DeviceUpdate(device_model=new_device_model)
    updated_device = crud.device.update(db=db, db_obj=device, obj_in=device_update)
    assert device.id == updated_device.id
    assert updated_device.device_model == new_device_model


def test_delete_device(db: Session) -> None:
    device = create_random_device(db)
    device2 = crud.device.remove(db=db, id=device.id)
    device3 = crud.device.get(db=db, id=device.id)
    assert device3 is None
    assert device2.id == device.id
    assert device2.device_model == device.device_model

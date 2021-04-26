from sqlalchemy.orm import Session

from app import crud
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.tests.utils.device import create_random_device

from app.tests.utils.faker import fake

def test_create_device(db: Session) -> None:
    model_name = fake.pystr()
    device_in = DeviceCreate(model_name=model_name)
    device = crud.device.create(db=db, obj_in=device_in)
    assert device.model_name == model_name
    assert type(device.id) is int

def test_get_device(db: Session) -> None:
    device = create_random_device(db)
    stored_device = crud.device.get(db=db, id=device.id)
    assert stored_device is not None
    assert device.id == stored_device.id
    assert device.model_name == stored_device.model_name


def test_update_device(db: Session) -> None:
    device = create_random_device(db)
    new_model_name = fake.pystr()
    device_update = DeviceUpdate(model_name=new_model_name)
    updated_device = crud.device.update(db=db, db_obj=device, obj_in=device_update)
    assert device.id == updated_device.id
    assert updated_device.model_name == new_model_name


def test_delete_device(db: Session) -> None:
    device = create_random_device(db)
    removed_device = crud.device.remove(db=db, id=device.id)
    after_remove_device = crud.device.get(db=db, id=device.id)
    assert after_remove_device is None
    assert removed_device.id == device.id
    assert removed_device.model_name == device.model_name

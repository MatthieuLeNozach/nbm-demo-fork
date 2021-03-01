from typing import Optional

from pydantic import BaseModel

# Shared properties
class DeviceBase(BaseModel):
    device_model: str


# Properties to receive on device creation
class DeviceCreate(DeviceBase):
    pass


# Properties to receive on device update
class DeviceUpdate(DeviceBase):
    pass


# Properties shared by models stored in DB
class DeviceInDBBase(DeviceBase):
    id: int
    class Config:
        orm_mode = True


# Properties to return to client
class Device(DeviceInDBBase):
    pass


# Properties properties stored in DB
class DeviceInDB(DeviceInDBBase):
    pass

from typing import Optional

from datetime import datetime, date

from pydantic import BaseModel, Field

from enum import Enum

class MediaType(str, Enum):
    UNDEFINED = "undefined"
    SOUND = "sound"
    IMAGE = "image"

# Shared properties
class MediaBase(BaseModel):
    file_url: Optional[str] = None
    file_blob: Optional[str] = None
    type: MediaType = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)


# Properties to receive on media creation
class MediaCreate(MediaBase):
    title: str


# Properties to receive on Media update
class MediaUpdate(MediaBase):
    pass


# Properties shared by models stored in DB
class MediaInDBBase(MediaBase):
    id: int
    file_url: str
    file_blob: str
    owner_id: int
    class Config:
        orm_mode = True


# Properties to return to client
class Media(MediaInDBBase):
    pass


# Properties properties stored in DB
class MediaInDB(MediaInDBBase):
    pass
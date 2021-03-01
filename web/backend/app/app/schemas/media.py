from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field

from enum import Enum

class MediaType(str, Enum):
    UNDEFINED = "undefined"
    SOUND = "sound"
    IMAGE = "image"

# Shared properties
class MediaBase(BaseModel):
    file_url: str
    file_source: str
    type: MediaType

# Properties to receive on media creation
class MediaCreate(MediaBase):
    pass

# Properties to receive on Media update
class MediaUpdate(MediaBase):
    pass

# Properties shared by models stored in DB
class MediaInDBBase(MediaBase):
    id: int
    created_by: int
    created_at: datetime
    updated_by: Optional[int]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# Properties to return to client
class Media(MediaInDBBase):
    pass

# Properties properties stored in DB
class MediaInDB(MediaInDBBase):
    pass

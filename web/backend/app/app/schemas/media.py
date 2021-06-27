from typing import Optional, List
from datetime import datetime, time
from pydantic import BaseModel
from enum import Enum
from app.schemas.medialabel import MediaLabel

class MediaType(str, Enum):
    UNDEFINED = "undefined"
    SOUND = "sound"
    IMAGE = "image"

# Shared properties
class MediaBase(BaseModel):
    file_url: str
    file_source: str
    type: Optional[MediaType]
    begin_date: datetime
    site_id: Optional[int]
    device_id: Optional[int]
    origin_id: Optional[int]
    meta: Optional[str]

# Properties to receive on media creation
class MediaCreate(MediaBase):
    duration: time

# Properties to receive on Media update
class MediaUpdate(MediaBase):
    file_url: Optional[str]
    file_source: Optional[str]
    type: Optional[MediaType]
    begin_date: Optional[datetime]

# Properties shared by models stored in DB
class MediaInDBBase(MediaBase):
    id: int
    created_by: int
    created_at: datetime
    updated_by: int = None
    updated_at: datetime = None
    duration: time
    class Config:
        orm_mode = True

# Properties to return to client
class Media(MediaInDBBase):
    pass
# Properties to return to client when fetching with id
class MediaWithMedialabels(MediaInDBBase):
    medialabels: List[MediaLabel]


# Properties to return to client when fetching list
class MediaWithMedialabelsCount(MediaInDBBase):
    medialabels_count: int

# Properties stored in DB
class MediaInDB(MediaInDBBase):
    pass

class InvalidAnnotation(BaseModel):
    line: int
    content: str
    detail: Optional[str]

class MediaUploadResponse(BaseModel):
    media: Media
    medialabels: List[MediaLabel]
    invalid_lines: List[InvalidAnnotation]

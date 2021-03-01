from typing import Optional

from datetime import datetime, date

from pydantic import BaseModel, Field

from enum import Enum

 
# Shared properties
class MediaLabelBase(BaseModel):
    begin_time: float
    end_time: float
    low_freq: float
    high_freq: float
    label: str

# Properties to receive on MedialLabel creation
class MediaLabelCreate(MediaLabelBase):
    media_id: int

# Properties to receive on MediaLabel update
class MediaLabelUpdate(MediaLabelBase):
    pass

# Properties shared by models stored in DB
class MediaLabelInDBBase(MediaLabelBase):
    id: int
    media_id: int
    created_by: int
    created_at: datetime
    updated_by: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class MediaLabel(MediaLabelInDBBase):
    pass


# Properties properties stored in DB
class MediaLabelInDB(MediaLabelInDBBase):
    pass

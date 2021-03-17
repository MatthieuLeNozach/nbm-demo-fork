from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator, confloat

# Shared properties
class MediaLabelBase(BaseModel):
    begin_time: confloat(ge=0)
    end_time: confloat(ge=0)
    low_freq: Optional[confloat(ge=0)]
    high_freq: Optional[confloat(ge=0)]
    label_id: int

    @validator('high_freq')
    def frequencies_order(cls, v, values, **kwargs):
        if 'low_freq' in values and values['low_freq'] is not None and v <= values['low_freq']:
            raise ValueError('low frequency must be lower than high frequency')
        return v

    @validator('end_time')
    def time_chronology(cls, v, values, **kwargs):
        if 'begin_time' in values and v <= values['begin_time']:
            raise ValueError('Begin time must be lower than end time')
        return v

# Properties to receive on MedialLabel creation
class MediaLabelCreate(MediaLabelBase):
    media_id: int

# Properties to receive on MediaLabel update
class MediaLabelUpdate(MediaLabelBase):
    begin_time: Optional[confloat(ge=0)]
    end_time: Optional[confloat(ge=0)]
    label_id: Optional[int]

# Properties shared by models stored in DB
class MediaLabelInDBBase(MediaLabelBase):
    id: int
    media_id: int
    created_by: int
    created_at: datetime
    updated_by: int = None
    updated_at: datetime = None

    class Config:
        orm_mode = True

# Properties to return to client
class MediaLabel(MediaLabelInDBBase):
    pass

# Properties properties stored in DB
class MediaLabelInDB(MediaLabelInDBBase):
    pass

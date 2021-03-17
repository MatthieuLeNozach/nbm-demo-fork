from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class SiteBase(BaseModel):
    name: str
    longitude: float
    latitude: float
    is_private: bool = False

# Properties to receive on site creation
class SiteCreate(SiteBase):
    pass

# Properties to receive on site update
class SiteUpdate(SiteBase):
    name: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    is_private: Optional[bool]

# Properties shared by models stored in DB
class SiteInDBBase(SiteBase):
    id: int
    created_by: int
    created_at: datetime
    updated_by: int = None
    updated_at: datetime = None

    class Config:
        orm_mode = True

# Properties to return to client
class Site(SiteInDBBase):
    pass

# Properties properties stored in DB
class SiteInDB(SiteInDBBase):
    pass

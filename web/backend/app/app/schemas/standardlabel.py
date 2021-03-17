from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class StandardLabelBase(BaseModel):
    name: str
    species_id: Optional[int]

# Properties to receive on StandardlLabel creation
class StandardLabelCreate(StandardLabelBase):
    pass

# Properties to receive on StandardLabel update
class StandardLabelUpdate(StandardLabelBase):
    name: Optional[str]

# Properties shared by models stored in DB
class StandardLabelInDBBase(StandardLabelBase):
    id: int
    created_by: int
    created_at: datetime
    updated_by: int = None
    updated_at: datetime = None
    class Config:
        orm_mode = True

# Properties to return to client
class StandardLabel(StandardLabelInDBBase):
    pass

# Properties properties stored in DB
class StandardLabelInDB(StandardLabelInDBBase):
    pass

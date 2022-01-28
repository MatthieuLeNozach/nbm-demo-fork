from typing import Optional
from pydantic import BaseModel

# Shared properties
class SpeciesBase(BaseModel):
    name: str
    code: int
    is_bird: Optional[bool]

class SpeciesUser(SpeciesBase):
    total: int
    total_user: int

# Properties to receive on StandardlLabel creation
class SpeciesCreate(SpeciesBase):
    pass

# Properties to receive on Species update
class SpeciesUpdate(SpeciesBase):
    name: Optional[str]
    code: Optional[int]

# Properties shared by models stored in DB
class SpeciesInDBBase(SpeciesBase):
    id: int
    class Config:
        orm_mode = True

# Properties to return to client
class Species(SpeciesInDBBase):
    pass

# Properties properties stored in DB
class SpeciesInDB(SpeciesInDBBase):
    pass

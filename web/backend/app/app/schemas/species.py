from typing import Optional
from pydantic import BaseModel

# Shared properties
class SpeciesBase(BaseModel):
    name: str
    is_bird: Optional[bool]

# Properties to receive on StandardlLabel creation
class SpeciesCreate(SpeciesBase):
    pass

# Properties to receive on Species update
class SpeciesUpdate(SpeciesBase):
    name: Optional[str]

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
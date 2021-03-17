from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String
)
from app.db.base_class import Base

class Species(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_bird = Column(Boolean, default=False)

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String
)
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Species(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    is_bird = Column(Boolean, default=False)
    code = Column(Integer, index=True, nullable=False)
    standardlabels = relationship("StandardLabel", back_populates="species")

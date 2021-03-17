from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class StandardLabel(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    species_id = Column(Integer, ForeignKey("species.id"))
    medialabels = relationship("MediaLabel", back_populates="label")
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)

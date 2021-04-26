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
    name = Column(String, index=True, nullable=False)
    species_id = Column(Integer, ForeignKey("species.id"))
    species = relationship("Species", foreign_keys=[species_id]) #allow to get creator from media without run query manually with id
    medialabels = relationship("MediaLabel", back_populates="label")
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)

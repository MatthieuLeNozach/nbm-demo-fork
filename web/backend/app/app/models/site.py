from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, Integer, String, ForeignKey, DateTime, Enum 
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.schemas import MediaType

if TYPE_CHECKING:
    from .item import Item  # noqa: F401

class Site(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey("user.id"), index=True) #a site is created by a user 
    updated_by = Column(Integer, ForeignKey("user.id"), index=True)
    created_at = Column(DateTime) 
    updated_at = Column(DateTime)
    longitude = Column(Float, index=True)
    latitude = Column(Float, index=True)
    name = Column(String, index=True)
    is_private = Column(Boolean(), default=False) # Is this site visible to anyone ?
    locality_precision = Column(Float, index = True) #a person can choose a radius of precision with which the site will be visible for others
    mediae = relationship("Media", back_populates="site")

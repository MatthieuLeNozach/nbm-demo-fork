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
    updated_by = Column(Integer, ForeignKey("user.id"), index=True) #update user
    created_at = Column(DateTime) #creation date
    updated_at = Column(DateTime) #update date
    longitude = Column(Float, index=True) #Angular distance of the site from Greenwich meridian
    latitude = Column(Float, index=True) #Angular distance of the site from the equator.
    name = Column(String, index=True) #name of site
    is_private = Column(Boolean(), default=False) # true if this site is invisible for everyone
    locality_precision = Column(Float, index = True) #a person can choose a radius of precision with which the site will be visible for others
    mediae = relationship("Media", back_populates="site") #list of mediae recorded in this site

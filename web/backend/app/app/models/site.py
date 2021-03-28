from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.schemas import MediaType

if TYPE_CHECKING: # pragma: no cover
    from .media import Media  # noqa: F401

class Site(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False) #a site is created by a user
    updated_by = Column(Integer, ForeignKey("user.id")) #update user
    created_at = Column(DateTime, nullable=False) #creation date
    updated_at = Column(DateTime) #update date
    longitude = Column(Float, index=True, nullable=False) #Angular distance of the site from Greenwich meridian
    latitude = Column(Float, index=True, nullable=False) #Angular distance of the site from the equator.
    name = Column(String, index=True, nullable=False) #name of site
    is_private = Column(Boolean(), default=False) # true if this site is invisible for everyone
    locality_precision = Column(Float) #a person can choose a radius of precision with which the site will be visible for others
    mediae = relationship("Media", back_populates="site")

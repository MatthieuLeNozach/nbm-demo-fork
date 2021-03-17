from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.schemas import MediaType

if TYPE_CHECKING: # pragma: no cover
    from .media import Media  # noqa: F401


class Device(Base):
    id = Column(Integer, primary_key=True)
    model_name = Column(String, index=True, unique=True)
    mediae = relationship("Media", back_populates="device")

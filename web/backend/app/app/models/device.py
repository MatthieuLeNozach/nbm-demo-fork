from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.schemas import MediaType

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Device(Base):
    id = Column(Integer, primary_key=True, index=True)
    device_model = Column(String, index=True, unique=True) #device model name
    mediae = relationship("Media", back_populates="device") #list of mediae recorded with this device

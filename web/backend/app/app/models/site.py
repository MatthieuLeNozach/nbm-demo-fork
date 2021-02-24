from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.schemas import MediaType

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class Site(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    created_at = Column(DateTime)
    longitude = Column(Float, index=True)
    latitude = Column(Float, index=True)
    name = Column(String, index=True)
    public_private = Column(String, index=True)
    masked_coord = Column(Boolean, index=True)

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


class MediaLabel(Base):
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media.id"), index=True)
    created_by = Column(Integer, ForeignKey("user.id"), index=True)
    created_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("user.id"), index=True)
    updated_at = Column(DateTime)
    begin_time = Column(Float, index=True)
    end_time = Column(Float, index=True)
    low_freq = Column(Float, index=True)
    high_freq = Column(Float, index=True)
    label = Column(String, index=True)
    label_type = Column(String, index=True)
    label_confidence = Column(Float, index=True)

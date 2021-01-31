from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import JSONB


from app.db.base_class import Base
from app.schemas import MediaType

if TYPE_CHECKING:
    from .item import Item  # noqa: F401

class Media(Base):
    id = Column(Integer, primary_key=True, index=True)
    origin_id = Column(Integer, ForeignKey('media.id'), index=True)
    type = Column(
        Enum(MediaType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=MediaType.SOUND.value,
    )
    file_url = Column(String, unique=False, index=True, nullable=True)
    file_source = Column(String, unique=False, index=True, nullable=True)
    meta = Column(JSONB, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    derivates = relationship("Media", backref='origin', remote_side=[id])
    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    owner = relationship("User", back_populates="mediae")
    

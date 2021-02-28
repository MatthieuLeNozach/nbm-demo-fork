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
    origin_id = Column(Integer, ForeignKey("media.id"), index=True) # id of the parent media if exists 
    type = Column(
        Enum(MediaType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=MediaType.SOUND.value,
    ) #sound, image, video or other type of media
    file_url = Column(String, unique=False, index=False, nullable=True) #url where the media is stored, url must allow download 
    file_source = Column(String, unique=False, index=False, nullable=True) #Gaëtan ? 
    meta = Column(JSONB, nullable=True) #Gaëtan ? 
    created_at = Column(DateTime) # creation date 
    updated_at = Column(DateTime) # update date 
    derivates = relationship("Media", backref="origin", remote_side=[id]) #Gaëtan ? 
    owner_id = Column(Integer, ForeignKey("user.id"), index=True) #user of the platform that owns the file 
    owner = relationship("User", back_populates="mediae") # Gaëtan ? 
    device_id = Column(Integer, ForeignKey("device.id"), index=True) 

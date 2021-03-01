from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum, Time
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
    file_source = Column(String, unique=False, index=False, nullable=True) #context of the file's recuperation (source (owner, website and all informations))
    meta = Column(JSONB, nullable=True) #file metadata
    derivates = relationship("Media", backref="origin", remote_side=[id]) #associated mediae to this media, reversed by origin_id
    created_at = Column(DateTime) #creation date
    created_by = Column(Integer, ForeignKey("user.id"), index=True) #user of the platform that owns the file (created_by)
    creator = relationship("User", foreign_keys=[created_by]) #allow to get creator from media without run query manually with id
    updated_at = Column(DateTime) #update date
    updated_by = Column(Integer, ForeignKey("user.id"), index=True) #update user
    device_id = Column(Integer, ForeignKey("device.id"), index=True) #media has been produced by one device
    device = relationship("Device", back_populates="mediae") #allow to get device from media without run query manually with id
    site_id = Column(Integer, ForeignKey("site.id"), index=True) #media has been produced at one place (if place is not a point, how do we manage it ?)
    site = relationship("Site", back_populates="mediae") #allow to get site from media without run query manually with id
    begin_date = Column(DateTime) #media has been recorded at one date (write begin date)
    duration = Column(Time) #sound or video medias have durations

#We might think that the url you can find are not owned by a platform user. Need to improve the model consequently.

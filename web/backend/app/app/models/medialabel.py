from sqlalchemy import (
    Column,
    Float,
    Integer,
    ForeignKey,
    DateTime,
    UniqueConstraint
)
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class MediaLabel(Base):
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id"))
    media = relationship("Media", back_populates="medialabels")
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)
    begin_time = Column(Float)
    end_time = Column(Float)
    low_freq = Column(Float, nullable=True)
    high_freq = Column(Float, nullable=True)
    label_id = Column(Integer, ForeignKey("standardlabel.id"))
    label = relationship("StandardLabel", back_populates="medialabels")
    label_confidence = Column(Float, index=True)
    __table_args__ = (UniqueConstraint('begin_time', 'media_id', 'label_id'),)


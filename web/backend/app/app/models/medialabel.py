from sqlalchemy import (
    Column,
    String,
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
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    media = relationship("Media", back_populates="medialabels")
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime)
    begin_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    low_freq = Column(Float)
    high_freq = Column(Float)
    label_id = Column(Integer, ForeignKey("standardlabel.id"))
    label = relationship("StandardLabel", back_populates="medialabels")
    label_confidence = Column(Float, index=True)
    invalid_label_text = Column(String)

    __table_args__ = (UniqueConstraint('begin_time', 'end_time', 'media_id', 'label_id'),)


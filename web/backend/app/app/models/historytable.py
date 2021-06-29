from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base

class HistoryTable(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    most_recent_downloaded_file = Column(DateTime)
    download_date = Column(DateTime)
    
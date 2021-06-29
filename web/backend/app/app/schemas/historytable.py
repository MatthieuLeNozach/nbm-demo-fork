from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Shared properties
class HistoryTableBase(BaseModel):
    user_id: Optional[int]
    most_recent_downloaded_file: datetime
    download_date: datetime

# Properties to receive on site creation
class HistoryTableCreate(HistoryTableBase):
    pass

# Properties to receive on site update
class HistoryTableUpdate(HistoryTableBase):
    pass

# Properties shared by models stored in DB
class HistoryTableInDBBase(HistoryTableBase):
    pass

# Properties to return to client
class HistoryTable(HistoryTableInDBBase):
    pass

# Properties properties stored in DB
class HistoryTableInDB(HistoryTableInDBBase):
    pass

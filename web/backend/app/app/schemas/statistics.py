from typing import Optional

from pydantic import BaseModel


class StatisticsAnnotationSpecies(BaseModel):
    id: int
    name: str
    total: int
    total_by_user: Optional[int]

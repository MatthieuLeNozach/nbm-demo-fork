from pydantic import BaseModel


class StatisticsAnnotationSpecies(BaseModel):
    id: int
    name: str
    total: int

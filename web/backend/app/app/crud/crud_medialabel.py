from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.medialabel import MediaLabel
from app.schemas.medialabel import MediaLabelCreate, MediaLabelUpdate


class CRUDMediaLabel(CRUDBase[MediaLabel, MediaLabelCreate, MediaLabelUpdate]):
    pass

medialabel = CRUDMediaLabel(MediaLabel)

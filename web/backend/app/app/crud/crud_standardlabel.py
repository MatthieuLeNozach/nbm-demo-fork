from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.standardlabel import StandardLabel
from app.schemas.standardlabel import StandardLabelCreate, StandardLabelUpdate


class CRUDStandardLabel(CRUDBase[StandardLabel, StandardLabelCreate, StandardLabelUpdate]):
    pass

standardlabel = CRUDStandardLabel(StandardLabel)

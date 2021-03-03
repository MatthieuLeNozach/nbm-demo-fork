from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.media import Media
from app.schemas.media import MediaCreate, MediaUpdate


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):
    pass

media = CRUDMedia(Media)

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils.medialabel import get_medialabel_schemas_from_file_content
from math import floor
from datetime import time

import uuid, json, requests, tempfile, os, soundfile

router = APIRouter()

@router.get("/", response_model=List[schemas.Media])
def read_mediae(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    created_by: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Mediae.
    """
    return crud.media.get_multi(db, skip=skip, limit=limit, created_by=created_by)

@router.post("/", response_model=schemas.Media)
def create_media(
    *,
    db: Session = Depends(deps.get_db),
    media_in: schemas.MediaCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new media.
    """
    media = crud.media.create(db=db, obj_in=media_in, created_by=current_user.id)
    return media

@router.get("/{id}", response_model=schemas.Media)
def read_media(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get media by ID.
    """
    media = crud.media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media


@router.post("/upload", response_model=schemas.MediaUploadResponse, status_code=200)
async def upload_audio(
    *,
    db: Session = Depends(deps.get_db),
    audio: UploadFile = File(...),
    annotations: UploadFile = File(...),
    begin_date: str = Form(...),
    device_id: str = Form(...),
    file_source: str = Form(...),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    if not settings.NEXTCLOUD_HOST or not settings.NEXTCLOUD_USER or not settings.NEXTCLOUD_PASSWORD: # pragma: no cover
        raise HTTPException(status_code=400, detail=[{"type": "next_cloud_config"}])


    # create current user directory in nextcloud
    file_directory = f"mediae/audio/{current_user.id}/"
    try:
        requests.request('MKCOL',
                     f"{settings.NEXTCLOUD_HOST}/remote.php/dav/files/{settings.NEXTCLOUD_USER}/{file_directory}",
                     auth=(settings.NEXTCLOUD_USER, settings.NEXTCLOUD_PASSWORD))
    except OSError:
        raise HTTPException(status_code=500, detail=[{"type": "nextcloud_connection_fail"}])


    # make a copy before read info => It's a trick to avoid soundfile read issue on already opened tmp file
    file_unique_id = str(uuid.uuid4())
    new_temp_path = os.path.join(tempfile.gettempdir(), file_unique_id)
    audio_content = await audio.read()
    with open(new_temp_path, "wb+") as file_object:
        file_object.write(audio_content)

    # get audio info from file
    try:
        audio_info = soundfile.info(new_temp_path)
    except RuntimeError:
        raise HTTPException(status_code=400, detail=[{"type": "invalid_audio"}])

    os.remove(new_temp_path)

    # upload audio file into nextcloud created directory
    extension = audio_info.format.lower()
    file_name = f"{file_unique_id}.{extension}"

    res = requests.put(f"{settings.NEXTCLOUD_HOST}/remote.php/dav/files/{settings.NEXTCLOUD_USER}/{file_directory}{file_name}",
                         data=audio_content,
                         auth=(settings.NEXTCLOUD_USER, settings.NEXTCLOUD_PASSWORD))

    if (res.status_code != 201): # pragma: no cover
        raise HTTPException(status_code=500, detail=[{"type": "audio_upload_fail"}])

    # get metadata to fill media model
    meta = {"samplerate": audio_info.samplerate,
            "channels": audio_info.channels,
            "sections": audio_info.sections,
            "format": audio_info.format,
            "subtype": audio_info.subtype }

    # get duration to fill media model
    seconds = floor(audio_info.duration)
    microseconds = int((audio_info.duration - seconds) * 100000)
    minutes, seconds = divmod(seconds, 60)
    hour, minutes = divmod(minutes, 60)
    duration = time(hour=hour, minute=minutes, second=seconds, microsecond=microseconds)

    # create media in database
    media_in = schemas.MediaCreate(file_url=f"{file_directory}{file_name}",
                                    file_source=file_source,
                                    begin_date=begin_date,
                                    device_id=device_id,
                                    meta=json.dumps(meta),
                                    duration=duration)

    media = crud.media.create(db=db, obj_in=media_in, created_by=current_user.id)

    # get information from annotations file
    annotations_content = await annotations.read()
    existing_labels = crud.standardlabel.get_multi(db, limit=9999)
    (medialabel_schemas, invalid_lines) = get_medialabel_schemas_from_file_content(annotations_content,
                                                                    media.id,
                                                                    existing_labels)
    # create medialabels in database from previous annotations file processing
    medialabels = []
    for medialabel_schema in medialabel_schemas:
        medialabel = crud.medialabel.create(db=db, obj_in=medialabel_schema, created_by=current_user.id)
        medialabels.append(medialabel)

    response = schemas.MediaUploadResponse(medialabels=medialabels,
                                            media=media,
                                            invalid_lines=invalid_lines)
    return response



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

@router.get("/", response_model=List[schemas.MediaWithMedialabelsCount])
def read_mediae(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    created_by: int = None,
    site: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Mediae.
    """
    filters={}
    if created_by is not None:
        if created_by == 0:
            filters["created_by"] = None
        else:
            filters["created_by"] = created_by
    if site is not None:
        if site == 0:
            filters["site_id"] = None
        else:
            filters["site_id"] = site

    mediae = crud.media.get_multi(db, skip=skip, limit=limit, filters=filters)
    for media in mediae:
        media.medialabels_count = len(media.medialabels)
    return mediae

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

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def upload_to_nextcloud(audio_file: UploadFile, current_user: models.User):
    if not settings.NEXTCLOUD_HOST or not settings.NEXTCLOUD_USER or not settings.NEXTCLOUD_PASSWORD:
        logger.error("Nextcloud configuration is missing")
        raise HTTPException(status_code=400, detail=[{"type": "next_cloud_config"}])

    logger.debug(f"Nextcloud Host: {settings.NEXTCLOUD_HOST}")
    logger.debug(f"Nextcloud User: {settings.NEXTCLOUD_USER}")
    logger.debug(f"Nextcloud Password: {settings.NEXTCLOUD_PASSWORD}")

    file_directory = f"mediae/audio/{current_user.id}/"
    try:
        logger.debug(f"Creating directory in Nextcloud: {file_directory}")
        mkcol_url = f"{settings.NEXTCLOUD_HOST}/remote.php/dav/files/{settings.NEXTCLOUD_USER}/{file_directory}"
        logger.debug(f"MKCOL URL: {mkcol_url}")
        mkcol_response = requests.request('MKCOL', mkcol_url, auth=(settings.NEXTCLOUD_USER, settings.NEXTCLOUD_PASSWORD))
        logger.debug(f"MKCOL Response: {mkcol_response.status_code} {mkcol_response.text}")
    except OSError as e:
        logger.error(f"Failed to create directory in Nextcloud: {e}")
        raise HTTPException(status_code=500, detail=[{"type": "nextcloud_connection_fail"}])

    file_unique_id = str(uuid.uuid4())
    new_temp_path = os.path.join(tempfile.gettempdir(), file_unique_id)
    audio_content = await audio_file.read()
    with open(new_temp_path, "wb+") as file_object:
        file_object.write(audio_content)

    try:
        logger.debug(f"Reading audio file info from: {new_temp_path}")
        audio_info = soundfile.info(new_temp_path)
    except RuntimeError as e:
        logger.error(f"Invalid audio file: {e}")
        raise HTTPException(status_code=400, detail=[{"type": "invalid_audio"}])

    os.remove(new_temp_path)

    extension = audio_info.format.lower()
    file_name = f"{file_unique_id}.{extension}"

    logger.debug(f"Uploading audio file to Nextcloud: {file_name}")
    put_url = f"{settings.NEXTCLOUD_HOST}/remote.php/dav/files/{settings.NEXTCLOUD_USER}/{file_directory}{file_name}"
    logger.debug(f"PUT URL: {put_url}")
    put_response = requests.put(put_url, data=audio_content, auth=(settings.NEXTCLOUD_USER, settings.NEXTCLOUD_PASSWORD))
    logger.debug(f"PUT Response: {put_response.status_code} {put_response.text}")

    if put_response.status_code != 201:
        logger.error(f"Failed to upload audio file to Nextcloud: {put_response.status_code}")
        raise HTTPException(status_code=500, detail=[{"type": "audio_upload_fail"}])

    file_url = f"{file_directory}{file_name}"

    meta = {
        "samplerate": audio_info.samplerate,
        "channels": audio_info.channels,
        "sections": audio_info.sections,
        "format": audio_info.format,
        "subtype": audio_info.subtype
    }

    seconds = floor(audio_info.duration)
    microseconds = int((audio_info.duration - seconds) * 100000)
    minutes, seconds = divmod(seconds, 60)
    hour, minutes = divmod(minutes, 60)
    duration = time(hour=hour, minute=minutes, second=seconds, microsecond=microseconds)

    return file_url, meta, duration

@router.get("/healthcheck-subservice")
def healthcheck():
    try:
        response = requests.get("http://api:8000/healthcheck")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

import requests

async def upload_to_inference_service(audio_file: UploadFile, current_user: models.User):
    files = {
        "file": (audio_file.filename, await audio_file.read(), audio_file.content_type)
    }
    data = {
        "email": current_user.email
    }
    
    # Add logging to debug the request data
    logger.info(f"Files: {files}")
    logger.info(f"Data: {data}")
    
    response = requests.post("http://api:8000/upload", files=files, data=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()






@router.post("/upload", response_model=schemas.MediaUploadResponse, status_code=200)
async def upload_audio(
    *,
    db: Session = Depends(deps.get_db),
    audio_file: UploadFile = File(None),
    audio_url: str = Form(None),
    audio_duration: str = Form(None),
    annotations: UploadFile = File(...),
    begin_date: str = Form(None),
    device_id: str = Form(None),
    site_id: str = Form(None),
    file_source: str = Form(...),
    current_user: models.User = Depends(deps.get_current_active_user),
    use_nextcloud: bool = False
):
    logger.debug("Starting upload_audio endpoint")
    file_url = audio_url
    duration = audio_duration
    meta = json.dumps({})

    if audio_file:
        if use_nextcloud:
            file_url, meta, duration = await upload_to_nextcloud(audio_file, current_user)
        else:
            inference_response = await upload_to_inference_service(audio_file, current_user)
            file_url = inference_response.get("file_url")
            meta = inference_response.get("meta")
            duration = inference_response.get("duration")

    logger.debug("Creating media entry in the database")
    media_in = schemas.MediaCreate(
        file_url=file_url,
        file_source=file_source,
        begin_date=begin_date,
        device_id=device_id,
        site_id=site_id,
        meta=json.dumps(meta),
        duration=duration
    )

    media = crud.media.create(db=db, obj_in=media_in, created_by=current_user.id)

    logger.debug("Reading annotations file")
    annotations_content = await annotations.read()
    existing_labels = crud.standardlabel.get_multi(db, limit=9999)
    (medialabel_schemas, invalid_lines) = get_medialabel_schemas_from_file_content(
        annotations_content, media.id, existing_labels)

    logger.debug("Creating medialabels in the database")
    medialabels = []
    for medialabel_schema in medialabel_schemas:
        medialabel = crud.medialabel.create(db=db, obj_in=medialabel_schema, created_by=current_user.id)
        medialabels.append(medialabel)

    response = schemas.MediaUploadResponse(
        medialabels=medialabels,
        media=media,
        invalid_lines=invalid_lines
    )
    logger.debug("Upload_audio endpoint completed successfully")
    return response
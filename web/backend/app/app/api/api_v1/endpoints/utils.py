import os
from typing import Any
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from pydantic.networks import EmailStr

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils.email import send_test_email
from app.utils.download import generate_mediae_zip

from app.core.config import settings

router = APIRouter()

@router.get("/count")
def count_entities(
    db: Session = Depends(deps.get_db),
) -> Any:
    return {
        "annotated_seconds": crud.media.get_duration_sum(db),
        "mediae": crud.media.count(db),
        "medialabels": crud.medialabel.count(db),
        "devices": crud.device.count(db),
        "sites": crud.site.count_public(db),
        "species": crud.species.get_count_by_annotations(db),
        "users": crud.user.count(db)
    }


@router.get("/personal-count")
def count_entities(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return {
        "annotated_seconds": crud.media.get_duration_sum(db, created_by=current_user.id),
        "mediae": crud.media.count(db, created_by=current_user.id),
        "medialabels": crud.medialabel.count(db, created_by=current_user.id),
        "species": crud.species.get_count_by_annotations(db, annotated_by=current_user.id),
        "sites": crud.site.count(db, created_by=current_user.id)
    }


@router.get("/download")
def download(
    db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    temp_folder = settings.TMP_PATH
    if not os.path.exists(temp_folder):
        Path(temp_folder).mkdir(parents=True, exist_ok=True)

    current_date = date.today().strftime("%Y_%m_%d")
    zip_name = f"mediae_{current_date}.zip"
    all_files_zip_path = f"{temp_folder}{zip_name}"
    if not os.path.exists(all_files_zip_path):
        mediae = crud.media.get_multi(db, skip=0, limit=9999)
        generate_mediae_zip(mediae, all_files_zip_path)

    return FileResponse(all_files_zip_path, filename=zip_name)


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}

from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils.email import send_test_email

router = APIRouter()

@router.get("/count")
def count_entities(
    db: Session = Depends(deps.get_db),
) -> Any:
    return { "mediae": crud.media.count(db),
            "medialabels": crud.medialabel.count(db),
            "devices": crud.device.count(db),
            "sites": crud.site.count(db),
            "users": crud.user.count(db) }

@router.get("/personal-count")
def count_entities(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return { "mediae": crud.media.count(db, created_by=current_user.id),
            "medialabels": crud.medialabel.count(db, created_by=current_user.id),
            "sites": crud.site.count(db, created_by=current_user.id) }

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

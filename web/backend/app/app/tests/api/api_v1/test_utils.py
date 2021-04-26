from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.utils.token import create_access_token
from app.tests.utils.faker import fake
from app.tests.utils.site import create_random_site
from app.tests.utils.medialabel import create_random_medialabel
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user

def test_get_count(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/utils/count", headers=normal_user_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert type(content["mediae"]) is int
    assert type(content["medialabels"]) is int
    assert type(content["devices"]) is int
    assert type(content["sites"]) is int
    assert type(content["users"]) is int


def test_get_personal_count(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:


    creator = create_random_user(db)
    creator_access_token = create_access_token(creator.id)

    create_random_media(db, created_by=creator.id)

    create_random_site(db, created_by=creator.id)

    create_random_medialabel(db, created_by=creator.id)
    create_random_medialabel(db, created_by=creator.id)

    response = client.get(
        f"{settings.API_V1_STR}/utils/personal-count", headers={ "Authorization":  "Bearer " + creator_access_token},
    )

    assert response.status_code == 200

    content = response.json()

    assert content["mediae"] == 1
    assert content["medialabels"] == 2
    assert content["sites"] == 1

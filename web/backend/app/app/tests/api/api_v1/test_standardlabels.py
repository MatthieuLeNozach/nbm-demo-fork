from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from datetime import datetime
from dateutil.parser import parse

from app.core.config import settings
from app.utils.token import create_access_token
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.standardlabel import create_random_standardlabel
from app.tests.utils.faker import fake
from math import ceil, floor

def test_create_standardlabel(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    name = fake.sentence()
    data = {"name": name}

    response = client.post(
        f"{settings.API_V1_STR}/standardlabels/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == data["name"]
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime

def test_read_standardlabel(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    standardlabel = create_random_standardlabel(db)
    response = client.get(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == standardlabel.name
    assert content["id"] == standardlabel.id
    assert content["created_by"] == standardlabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == standardlabel.created_at


def test_read_unexisting_standardlabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/standardlabels/9999999", headers=normal_user_token_headers,
    )

    assert response.status_code == 404


def test_read_standardlabels(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/standardlabels", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    standardlabels = response.json()

    assert type(standardlabels) is list

    content = standardlabels[0]

    assert type(content["name"]) is str
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime


def test_update_standardlabel_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    standardlabel = create_random_standardlabel(db)

    new_name = fake.sentence()
    data = { "name": new_name }
    response = client.put(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers=superuser_token_headers, json=data
    )

    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == data["name"]
    assert content["id"] == standardlabel.id
    assert content["created_by"] == standardlabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == standardlabel.created_at
    assert type(content["updated_by"]) is int
    assert type(datetime.strptime(content["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')) is datetime


def test_update_standardlabel_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = create_access_token(creator.id)
    standardlabel = create_random_standardlabel(db, created_by=creator.id)

    new_name = fake.sentence()
    data = { "name": new_name }
    response = client.put(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers={ "Authorization":  "Bearer " + creator_access_token}, json=data
    )

    assert response.status_code == 403


def test_update_standardlabel_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    standardlabel = create_random_standardlabel(db)

    data = { "name": "" }
    response = client.put(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 403


def test_update_unexisting_standardlabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = { "name": "" }
    response = client.put(
        f"{settings.API_V1_STR}/standardlabels/99999999", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 404


def test_delete_standardlabel_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    standardlabel = create_random_standardlabel(db)
    response = client.delete(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == standardlabel.id


def test_delete_standardlabel_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = create_access_token(creator.id)
    standardlabel = create_random_standardlabel(db, created_by=creator.id)
    response = client.delete(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers={ "Authorization":  "Bearer " + creator_access_token}
    )

    assert response.status_code == 403


def test_delete_standardlabel_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    standardlabel = create_random_standardlabel(db)
    response = client.delete(
        f"{settings.API_V1_STR}/standardlabels/{standardlabel.id}", headers=normal_user_token_headers
    )

    assert response.status_code == 403


def test_delete_unexisting_standardlabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/standardlabels/99999999", headers=normal_user_token_headers
    )

    assert response.status_code == 404


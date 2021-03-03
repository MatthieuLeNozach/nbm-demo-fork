from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from datetime import datetime
from dateutil.parser import parse

from app.core import security
from app.core.config import settings
from app.tests.utils.medialabel import create_random_medialabel
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.faker import fake

def test_create_medialabel(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    media = create_random_media(db)

    begin_time = fake.pyfloat()
    end_time = fake.pyfloat()
    low_freq = fake.pyfloat()
    high_freq = fake.pyfloat()
    label = fake.sentence()

    data = {"begin_time": begin_time,
            "end_time": end_time,
            "low_freq": low_freq,
            "high_freq": high_freq,
            "label": label,
            "media_id": media.id}

    response = client.post(
        f"{settings.API_V1_STR}/medialabels/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["begin_time"] == data["begin_time"]
    assert content["end_time"] == data["end_time"]
    assert content["low_freq"] == data["low_freq"]
    assert content["high_freq"] == data["high_freq"]
    assert content["label"] == data["label"]
    assert content["media_id"] == data["media_id"]
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime

def test_read_medialabel(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    response = client.get(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["begin_time"] == medialabel.begin_time
    assert content["end_time"] == medialabel.end_time
    assert content["low_freq"] == medialabel.low_freq
    assert content["high_freq"] == medialabel.high_freq
    assert content["label"] == medialabel.label
    assert content["media_id"] == medialabel.media_id
    assert content["id"] == medialabel.id
    assert content["created_by"] == medialabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == medialabel.created_at


def test_read_unexisting_medialabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/medialabels/9999999", headers=normal_user_token_headers,
    )

    assert response.status_code == 404


def test_read_medialabels(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/medialabels", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    medialabels = response.json()

    assert type(medialabels) is list

    content = medialabels[0]

    assert type(content["begin_time"]) is float
    assert type(content["end_time"]) is float
    assert type(content["low_freq"]) is float
    assert type(content["high_freq"]) is float
    assert type(content["label"]) is str
    assert type(content["media_id"]) is int
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime


def test_update_medialabel_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    data = { "begin_time": fake.pyfloat(), "label": fake.sentence() }
    response = client.put(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=superuser_token_headers, json=data
    )

    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    content = response.json()
    
    assert content["begin_time"] == data["begin_time"]
    assert content["label"] == data["label"]
    assert content["end_time"] == medialabel.end_time
    assert content["low_freq"] == medialabel.low_freq
    assert content["high_freq"] == medialabel.high_freq
    assert content["media_id"] == medialabel.media_id
    assert content["id"] == medialabel.id
    assert content["created_by"] == medialabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == medialabel.created_at
    assert type(content["updated_by"]) is int
    assert type(datetime.strptime(content["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')) is datetime




def test_update_medialabel_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = security.create_access_token(creator.id)
    medialabel = create_random_medialabel(db, created_by=creator.id)
    data = { "begin_time": fake.pyfloat(), "label": fake.sentence() }
    response = client.put(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers={ "Authorization":  "Bearer " + creator_access_token}, json=data
    )

    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers={ "Authorization":  "Bearer " + creator_access_token}
    )

    assert response.status_code == 200

    content = response.json()
    
    assert content["begin_time"] == data["begin_time"]
    assert content["label"] == data["label"]
    assert content["end_time"] == medialabel.end_time
    assert content["low_freq"] == medialabel.low_freq
    assert content["high_freq"] == medialabel.high_freq
    assert content["media_id"] == medialabel.media_id
    assert content["id"] == medialabel.id
    assert content["created_by"] == medialabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == medialabel.created_at
    assert type(content["updated_by"]) is int
    assert type(datetime.strptime(content["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')) is datetime


def test_update_medialabel_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    data = { "begin_time": fake.pyfloat() }
    response = client.put(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 403


def test_update_unexisting_medialabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    data = { "begin_time": fake.pyfloat() }
    response = client.put(
        f"{settings.API_V1_STR}/medialabels/99999999", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 404


def test_delete_medialabel_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    response = client.delete(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == medialabel.id


def test_delete_medialabel_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = security.create_access_token(creator.id)
    medialabel = create_random_medialabel(db, created_by=creator.id)
    response = client.delete(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers={ "Authorization":  "Bearer " + creator_access_token}
    )

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == medialabel.id


def test_delete_medialabel_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    response = client.delete(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=normal_user_token_headers
    )

    assert response.status_code == 403


def test_delete_unexisting_medialabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)
    response = client.delete(
        f"{settings.API_V1_STR}/medialabels/99999999", headers=normal_user_token_headers
    )

    assert response.status_code == 404


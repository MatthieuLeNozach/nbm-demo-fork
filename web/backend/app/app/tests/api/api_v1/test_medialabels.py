from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from datetime import datetime
from dateutil.parser import parse

from app.core.config import settings
from app.utils.token import create_access_token
from app.tests.utils.medialabel import create_random_medialabel
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.standardlabel import create_random_standardlabel
from app.tests.utils.faker import fake
from math import ceil, floor

def test_create_medialabel(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    media = create_random_media(db)
    label = create_random_standardlabel(db)

    begin_time = fake.pyfloat(positive=True)
    end_time = fake.pyfloat(positive=True, min_value=ceil(begin_time))
    low_freq = fake.pyfloat(positive=True)
    high_freq = fake.pyfloat(positive=True, min_value=ceil(low_freq))

    data = {"begin_time": begin_time,
            "end_time": end_time,
            "low_freq": low_freq,
            "high_freq": high_freq,
            "label_id": label.id,
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
    assert content["label_id"] == data["label_id"]
    assert content["media_id"] == data["media_id"]
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime


def test_create_medialabel_with_invalid_time(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    media = create_random_media(db)
    label = create_random_standardlabel(db)

    begin_time = fake.pyfloat(positive=True)
    end_time = fake.pyfloat(positive=True, max_value=ceil(begin_time))
    low_freq = fake.pyfloat(positive=True)
    high_freq = fake.pyfloat(positive=True, min_value=ceil(low_freq))

    data = {"begin_time": begin_time,
            "end_time": end_time,
            "low_freq": low_freq,
            "high_freq": high_freq,
            "label_id": label.id,
            "media_id": media.id}

    response = client.post(
        f"{settings.API_V1_STR}/medialabels/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 422
    content = response.json()

    assert type(content["detail"]) is list
    assert type(content["detail"][0]) is dict
    assert content["detail"][0]["msg"] == "Begin time must be lower than end time"


def test_create_medialabel_with_invalid_frequencies(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    media = create_random_media(db)
    label = create_random_standardlabel(db)

    begin_time = fake.pyfloat(positive=True)
    end_time = fake.pyfloat(positive=True, min_value=ceil(begin_time))
    low_freq = fake.pyfloat(positive=True)
    high_freq = fake.pyfloat(positive=True, max_value=ceil(low_freq))

    data = {"begin_time": begin_time,
            "end_time": end_time,
            "low_freq": low_freq,
            "high_freq": high_freq,
            "label_id": label.id,
            "media_id": media.id}

    response = client.post(
        f"{settings.API_V1_STR}/medialabels/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 422
    content = response.json()

    assert type(content["detail"]) is list
    assert type(content["detail"][0]) is dict
    assert content["detail"][0]["msg"] == "Low frequency must be lower than high frequency"


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
    assert content["label_id"] == medialabel.label_id
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
    if content["label_id"]:
        assert type(content["label_id"]) is int     
    assert type(content["media_id"]) is int
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime


def test_update_medialabel_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)

    begin_time = fake.pyfloat(positive=True, max_value=floor(medialabel.end_time))
    high_freq = fake.pyfloat(positive=True, min_value=ceil(medialabel.low_freq))
    data = { "begin_time": begin_time, "high_freq": high_freq }
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
    assert content["high_freq"] == data["high_freq"]
    assert content["end_time"] == medialabel.end_time
    assert content["low_freq"] == medialabel.low_freq
    assert content["media_id"] == medialabel.media_id
    assert content["label_id"] == medialabel.label_id
    assert content["id"] == medialabel.id
    assert content["created_by"] == medialabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == medialabel.created_at
    assert type(content["updated_by"]) is int
    assert type(datetime.strptime(content["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')) is datetime




def test_update_medialabel_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = create_access_token(creator.id)
    medialabel = create_random_medialabel(db, created_by=creator.id)

    begin_time = fake.pyfloat(positive=True, max_value=floor(medialabel.end_time))
    high_freq = fake.pyfloat(positive=True, min_value=ceil(medialabel.low_freq))
    data = { "begin_time": begin_time, "high_freq": high_freq }
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
    assert content["high_freq"] == data["high_freq"]
    assert content["end_time"] == medialabel.end_time
    assert content["low_freq"] == medialabel.low_freq
    assert content["media_id"] == medialabel.media_id
    assert content["label_id"] == medialabel.label_id
    assert content["id"] == medialabel.id
    assert content["created_by"] == medialabel.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == medialabel.created_at
    assert type(content["updated_by"]) is int
    assert type(datetime.strptime(content["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')) is datetime


def test_update_medialabel_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    medialabel = create_random_medialabel(db)

    data = { "begin_time": 0 }
    response = client.put(
        f"{settings.API_V1_STR}/medialabels/{medialabel.id}", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 403


def test_update_unexisting_medialabel(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = { "begin_time": 0 }
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
    creator_access_token = create_access_token(creator.id)
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
    response = client.delete(
        f"{settings.API_V1_STR}/medialabels/99999999", headers=normal_user_token_headers
    )

    assert response.status_code == 404


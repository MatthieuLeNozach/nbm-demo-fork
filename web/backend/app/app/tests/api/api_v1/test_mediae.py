from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.site import create_random_site
from app.tests.utils.device import create_random_device
from app.tests.utils.faker import fake

from datetime import datetime
from dateutil.parser import parse

def test_create_media(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    file_source = fake.uri()
    file_url = f"{file_source}{fake.file_name()}"
    file_type = "sound"

    creator = create_random_user(db)
    site = create_random_site(db)
    device = create_random_device(db)

    begin_date = fake.date_time_this_century()
    duration = fake.time_object()

    data = {"file_source": file_source,
            "file_url": file_url,
            "site_id": site.id,
            "device_id": device.id,
            "type": file_type,
            "begin_date": str(begin_date),
            "duration": str(duration)}

    response = client.post(
        f"{settings.API_V1_STR}/mediae/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["file_source"] == data["file_source"]
    assert content["file_url"] == data["file_url"]
    assert content["site_id"] == data["site_id"]
    assert content["device_id"] == data["device_id"]
    assert (datetime.strptime(content["begin_date"], '%Y-%m-%dT%H:%M:%S')
            == datetime.strptime(data["begin_date"], '%Y-%m-%d %H:%M:%S'))
    assert content["duration"] == str(data["duration"])
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime


def test_read_media(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    media = create_random_media(db)
    response = client.get(
        f"{settings.API_V1_STR}/mediae/{media.id}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["file_source"] == media.file_source
    assert content["file_url"] == media.file_url
    assert content["created_by"] == media.created_by
    assert content["site_id"] == media.site_id
    assert content["device_id"] == media.device_id
    assert datetime.strptime(content["begin_date"], '%Y-%m-%dT%H:%M:%S') == media.begin_date
    assert content["duration"] == str(media.duration)
    assert content["id"] == media.id
    assert content["created_by"] == media.created_by
    assert datetime.strptime(content["created_at"], '%Y-%m-%dT%H:%M:%S.%f') == media.created_at


def test_read_unexisting_media(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/mediae/9999999", headers=normal_user_token_headers,
    )

    assert response.status_code == 404


def test_read_mediae(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/mediae", headers=superuser_token_headers,
    )
    
    assert response.status_code == 200

    mediae = response.json()

    assert type(mediae) is list

    content = mediae[0]

    assert type(content["file_source"]) is str
    assert type(content["file_url"]) is str
    assert type(content["site_id"]) is int
    assert type(content["device_id"]) is int
    assert type(datetime.strptime(content["begin_date"], '%Y-%m-%dT%H:%M:%S')) is datetime
    assert type(content["duration"]) is str
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.device import create_random_device
from app.tests.utils.faker import fake

def test_create_device_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"model_name": fake.pystr()}
    response = client.post(
        f"{settings.API_V1_STR}/devices/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["model_name"] == data["model_name"]
    assert type(content["id"]) is int

def test_create_device_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {"model_name": fake.pystr()}
    response = client.post(
        f"{settings.API_V1_STR}/devices/", headers=normal_user_token_headers, json=data,
    )

    assert response.status_code == 403

def test_read_device(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    device = create_random_device(db)
    response = client.get(
        f"{settings.API_V1_STR}/devices/{device.id}", headers=normal_user_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["model_name"] == device.model_name
    assert content["id"] == device.id

def test_read_unexisting_device(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/devices/9999999", headers=normal_user_token_headers,
    )

    assert response.status_code == 404

def test_read_devices(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/devices", headers=normal_user_token_headers,
    )
    assert response.status_code == 200

    devices = response.json()
    assert type(devices) is list

    content = devices[0]
    assert type(content["model_name"]) is str
    assert type(content["id"]) is int

def test_impossible_device_duplication( 
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    model_name = "SuperMic2000"
    data = {"model_name": model_name}

    response = client.get(
        f"{settings.API_V1_STR}/devices?model_name={model_name}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    devices = response.json()

    assert type(devices) is list

    if (len(devices) == 0): # pragma: no cover. Not really a test, just if databse is not empty 
        response = client.post(
            f"{settings.API_V1_STR}/devices/", headers=superuser_token_headers, json=data,
        )
        assert response.status_code == 200

    response = client.post(
        f"{settings.API_V1_STR}/devices/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 409

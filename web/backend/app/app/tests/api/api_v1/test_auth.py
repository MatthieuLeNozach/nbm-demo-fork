from typing import Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.faker import fake


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_with_invalid_email(client: TestClient) -> None:
    login_data = {
        "username": "fake_email@fakedomain.com",
        "password": "fake_password",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)

    assert r.status_code == 400

    content = r.json()
    assert type(content["detail"]) is list
    assert type(content["detail"][0]) is dict
    assert content["detail"][0]["type"] == "invalid_credentials"


def test_get_access_token_for_inactive_user(client: TestClient, db: Session) -> None:
    email = fake.ascii_free_email()
    password = fake.sha256()
    user_in = UserCreate(email=email, password=password, is_active=False)
    crud.user.create(db, obj_in=user_in)

    login_data = {
        "username": email,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)

    assert r.status_code == 400

    content = r.json()
    assert type(content["detail"]) is list
    assert type(content["detail"][0]) is dict
    assert content["detail"][0]["type"] == "inactive_user"


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token", headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_register(client: TestClient) -> None:
    email = fake.ascii_free_email()
    password = fake.sha256()

    registration_data = {
        "email": email,
        "password": password,
        "password_confirmation": password,
    }

    r = client.post(f"{settings.API_V1_STR}/register", json=registration_data)

    assert r.status_code == 200

    content = r.json()
    assert type(content["access_token"]) is str


def test_register_with_existing_email(client: TestClient) -> None:
    email = fake.ascii_free_email()
    password = fake.sha256()

    registration_data = {
        "email": email,
        "password": password,
        "password_confirmation": password,
    }

    r = client.post(f"{settings.API_V1_STR}/register", json=registration_data)

    assert r.status_code == 200

    r = client.post(f"{settings.API_V1_STR}/register", json=registration_data)

    print(r.text)
    assert r.status_code == 400

    content = r.json()
    assert type(content["detail"]) is list
    assert type(content["detail"][0]) is dict
    assert content["detail"][0]["type"] == "existing_email"


def test_register_with_password_mismatch(client: TestClient) -> None:
    registration_data = {
        "email": fake.ascii_free_email(),
        "password": fake.sha256(),
        "password_confirmation": fake.sha256(),
    }

    r = client.post(f"{settings.API_V1_STR}/register", json=registration_data)

    assert r.status_code == 400

    content = r.json()
    assert type(content["detail"]) is list
    assert type(content["detail"][0]) is dict
    assert content["detail"][0]["type"] == "password_mismatch"


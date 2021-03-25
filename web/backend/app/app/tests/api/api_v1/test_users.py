from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.utils.token import create_access_token
from app.tests.utils.faker import fake

def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = fake.ascii_free_email()
    data = {"email": email, "password": fake.sha256()}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]


def test_update_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {"full_name": fake.name(), "password": "123456", "email": fake.ascii_free_email()}
    r = client.put(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers, json=data,
    )

    assert r.status_code == 200

    r = client.get(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers, json=data,
    )

    assert r.status_code == 200
    content = r.json()

    assert content["full_name"] == data["full_name"]


def test_update_non_existent_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"full_name": ""}
    r = client.put(
        f"{settings.API_V1_STR}/users/9999999", headers=superuser_token_headers, json=data,
    )

    assert r.status_code == 404


def test_update_user_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = fake.ascii_free_email()
    data = {"email": email, "password": fake.sha256()}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    print(r.text)
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]

    data = {"full_name": fake.name()}
    r = client.put(
        f"{settings.API_V1_STR}/users/{user.id}", headers=superuser_token_headers, json=data,
    )

    assert r.status_code == 200

    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=superuser_token_headers, json=data,
    )

    assert r.status_code == 200
    content = r.json()

    assert content["email"] == created_user["email"]
    assert content["full_name"] == data["full_name"]


def test_get_existing_user_by_normal_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = fake.ascii_free_email()
    user_in = UserCreate(email=email, password=fake.sha256())
    user = crud.user.create(db, obj_in=user_in)
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=normal_user_token_headers,
    )
    assert r.status_code == 403


def test_get_existing_user_by_self_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = fake.ascii_free_email()
    user_in = UserCreate(email=email, password=fake.sha256())
    user = crud.user.create(db, obj_in=user_in)

    creator_access_token = create_access_token(user.id)
    creator_headers = { "Authorization":  "Bearer " + creator_access_token}

    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=creator_headers,
    )

    assert r.status_code == 200

    api_user = r.json()
    assert user.email == api_user["email"]
    assert user.id == api_user["id"]
    assert user.full_name == api_user["full_name"]


def test_get_existing_user_by_super_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = fake.ascii_free_email()
    user_in = UserCreate(email=email, password=fake.sha256())
    user = crud.user.create(db, obj_in=user_in)
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=email)
    assert existing_user is not None
    assert existing_user.email == api_user["email"]


def test_create_user_existing_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = fake.ascii_free_email()
    password = fake.sha256()
    user_in = UserCreate(email=email, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    data = {"email": fake.ascii_free_email(), "password": fake.sha256()}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user_in = UserCreate(email=fake.ascii_free_email(), password=fake.sha256())
    crud.user.create(db, obj_in=user_in)

    user_in2 = UserCreate(email=fake.ascii_free_email(), password=fake.sha256())
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1

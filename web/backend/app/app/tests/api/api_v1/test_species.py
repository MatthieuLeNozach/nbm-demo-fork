from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from datetime import datetime
from dateutil.parser import parse

from app.core.config import settings
from app.utils.token import create_access_token
from app.tests.utils.media import create_random_media
from app.tests.utils.user import create_random_user
from app.tests.utils.species import create_random_species
from app.tests.utils.faker import fake
from math import ceil, floor

def test_create_species_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    name = fake.sentence()
    data = {"name": name}

    response = client.post(
        f"{settings.API_V1_STR}/species/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == data["name"]
    assert type(content["id"]) is int

def test_create_species_by_normal_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:

    name = fake.sentence()
    data = {"name": name}

    response = client.post(
        f"{settings.API_V1_STR}/species/", headers=normal_user_token_headers, json=data,
    )

    assert response.status_code == 403

def test_read_species(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    species = create_random_species(db)
    response = client.get(
        f"{settings.API_V1_STR}/species/{species.id}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == species.name
    assert content["id"] == species.id


def test_read_unexisting_species(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/species/9999999", headers=normal_user_token_headers,
    )

    assert response.status_code == 404


def test_read_multiple_species(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/species", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    species = response.json()

    assert type(species) is list

    content = species[0]

    assert type(content["name"]) is str
    assert type(content["id"]) is int


def test_update_species_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    species = create_random_species(db)

    new_name = fake.sentence()
    data = { "name": new_name }
    response = client.put(
        f"{settings.API_V1_STR}/species/{species.id}", headers=superuser_token_headers, json=data
    )

    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/species/{species.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == data["name"]
    assert content["id"] == species.id


def test_update_species_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = create_access_token(creator.id)
    species = create_random_species(db)

    new_name = fake.sentence()
    data = { "name": new_name }
    response = client.put(
        f"{settings.API_V1_STR}/species/{species.id}", headers={ "Authorization":  "Bearer " + creator_access_token}, json=data
    )

    assert response.status_code == 403


def test_update_species_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    species = create_random_species(db)

    data = { "name": "" }
    response = client.put(
        f"{settings.API_V1_STR}/species/{species.id}", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 403


def test_update_unexisting_species(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = { "name": "" }
    response = client.put(
        f"{settings.API_V1_STR}/species/99999999", headers=normal_user_token_headers, json=data
    )

    assert response.status_code == 404


def test_delete_species_by_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    species = create_random_species(db)
    response = client.delete(
        f"{settings.API_V1_STR}/species/{species.id}", headers=superuser_token_headers
    )

    assert response.status_code == 200

    content = response.json()

    assert content["id"] == species.id


def test_delete_species_by_creator(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = create_access_token(creator.id)
    species = create_random_species(db)
    response = client.delete(
        f"{settings.API_V1_STR}/species/{species.id}", headers={ "Authorization":  "Bearer " + creator_access_token}
    )

    assert response.status_code == 403


def test_delete_species_without_permission(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    species = create_random_species(db)
    response = client.delete(
        f"{settings.API_V1_STR}/species/{species.id}", headers=normal_user_token_headers
    )

    assert response.status_code == 403


def test_delete_unexisting_species(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/species/99999999", headers=normal_user_token_headers
    )

    assert response.status_code == 404


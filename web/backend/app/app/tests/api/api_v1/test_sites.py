from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.tests.utils.site import create_random_site
from app.tests.utils.user import create_random_user

from datetime import datetime
from dateutil.parser import parse
from app.tests.utils.faker import fake

def test_create_site(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:

    geo_info = fake.location_on_land()
    data = {"latitude": float(geo_info[0]), "longitude": float(geo_info[1]), "name": geo_info[2], "is_private": fake.boolean()}
    response = client.post(
        f"{settings.API_V1_STR}/sites/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["latitude"] == data["latitude"]
    assert content["longitude"] == data["longitude"]
    assert content["name"] == data["name"]
    assert content["is_private"] == data["is_private"]
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int
    assert type(parse(content["created_at"])) is datetime


def test_read_site(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    site = create_random_site(db)
    response = client.get(
        f"{settings.API_V1_STR}/sites/{site.id}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["latitude"] == site.latitude
    assert content["longitude"] == site.longitude
    assert content["name"] == site.name
    assert content["is_private"] == site.is_private
    assert content["id"] == site.id
    assert content["created_by"] == site.created_by

def test_read_sites(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/sites", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    sites = response.json()

    assert type(sites) is list

    content = sites[0]

    assert type(content["latitude"]) is float
    assert type(content["longitude"]) is float
    assert type(content["name"]) is str
    assert type(content["is_private"]) is bool
    assert type(content["id"]) is int
    assert type(content["created_by"]) is int

def test_read_sites_normal_user(
    client: TestClient, db: Session
) -> None:
    creator = create_random_user(db)
    creator_access_token = security.create_access_token(creator.id)
    site1 = create_random_site(db, created_by = creator.id, is_private = True)
    site2 = create_random_site(db, is_private = True)
    site3 = create_random_site(db, is_private = False)

    response = client.get(
        f"{settings.API_V1_STR}/sites", headers={ "Authorization":  "Bearer " + creator_access_token},
    )

    assert response.status_code == 200

    sites = response.json()

    
    assert type(sites) is list
    for site in sites:
        assert site["is_private"] == False or site["created_by"] == creator.id

def test_read_unexisting_site(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/sites/9999999", headers=normal_user_token_headers,
    )

    assert response.status_code == 404

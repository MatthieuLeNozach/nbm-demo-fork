from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.species import create_random_species
from app.tests.utils.medialabel import create_random_medialabel
from app.tests.utils.standardlabel import create_random_standardlabel


def test_get_annotations_species(client: TestClient, db: Session) -> None:
    species = create_random_species(db)
    standardlabel = create_random_standardlabel(db, species_id=species.id)
    create_random_medialabel(db, label_id=standardlabel.id)
    create_random_medialabel(db, label_id=standardlabel.id)

    response = client.get(f"{settings.API_V1_STR}/statistics/species_annotations")

    for item in response.json():
        if item['id'] == species.id:
            assert item['total'] == 2

    assert response.status_code == 200

from app.core import security
from app.tests.utils.user import create_random_user
from jose import jwt #jwt = java script web token which is a norm to store token in javascript see line 15 for example 
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from math import floor
from app.tests.utils.faker import fake


def test_create_access_token_with_delta(db: Session) -> None:
    user = create_random_user(db)
    expires_delta = timedelta(minutes=fake.pyint())
    expiration_date = datetime.utcnow() + expires_delta
    access_token = security.create_access_token(user.id, expires_delta)

    assert type(access_token) is str

    data = jwt.decode(access_token, settings.SECRET_KEY)

    assert type(data) is dict
    assert data["sub"] == str(user.id)
    assert data["exp"] == floor(expiration_date.timestamp()) #exp = expiration date in seconds 

def test_create_access_token_without_delta(db: Session) -> None:
    user = create_random_user(db)
    access_token = security.create_access_token(user.id)
    
    assert type(access_token) is str

    data = jwt.decode(access_token, settings.SECRET_KEY)
    
    assert type(data) is dict
    assert data["sub"] == str(user.id)

    expiration_date = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    assert data["exp"] == floor(expiration_date.timestamp())

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils.token import generate_password_reset_token, verify_password_reset_token, create_access_token
from app.utils.email import send_reset_password_email

from app.schemas import (
    UserRegister,
    UserWithToken,
)

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail=[{"type": "invalid_credentials"}])
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail=[{"type": "inactive_user"}])
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=[{"type": "nonexistent_email"}],
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail=[{"type": "invalid_token"}])
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=[{"type": "nonexistent_email"}],
        )

    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail=[{"type": "inactive_user"}])
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}

@router.post("/register", response_model=schemas.UserWithToken)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserRegister
) -> UserWithToken:

    user_in_db = crud.user.get_by_email(db, email=user_in.email)
    if user_in_db is not None:
        print(user_in_db.__dict__)
    """
    Register, get an access token and profile data
    """
    if user_in_db:
        raise HTTPException(
            status_code=400,
            detail=[{"type": "existing_email"}],
        )

    if user_in.password != user_in.password_confirmation:
        raise HTTPException(
            status_code=400,
            detail=[{"type": "password_mismatch"}],
        )

    user_out = crud.user.register(
        db, user_in=user_in
    )
    if not (user_out): # pragma: no cover
        raise HTTPException(
            status_code=500,
            detail=[{"type": "unknown_error"}],
        )
    print(user_out)
    print(user_out.__dict__)
    access_token = create_access_token(user_out.id)
    user_data = jsonable_encoder(user_out)
    return {
        **user_data,
        'access_token': access_token
    }

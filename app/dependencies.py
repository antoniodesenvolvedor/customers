from datetime import datetime, timedelta
from typing import Optional

from fastapi import Header, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import custom_exceptions, schemas, models, config
from app.database import SessionLocal
from app.security import verify_password
from app.services.user_service import UserService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_service = UserService(db)
    return user_service.get_user_by_token(token=token)


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise custom_exceptions.inactive_user_exception
    return current_user


async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise custom_exceptions.login_unauthorized_exception
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserService.create_access_token(
        data={"sub": user.token_uuid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def login_for_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise custom_exceptions.login_unauthorized_exception
    return user


def authenticate_user(db: Session, username: str, password: str):
    user_service = UserService(db)
    user = user_service.get_user_by_name(username=username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user






from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models, dependencies
from app.services.user_service import UserService


router = APIRouter(
    prefix="/user",
    # tags=["customers"],
    # dependencies=[Depends(dependencies.get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=schemas.User)
def read_user(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return current_user

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    user_service = UserService(db)
    return user_service.create_user(user=user)


@router.put("/")
def change_password(user: schemas.UserUpdate, current_user: schemas.User = Depends(dependencies.get_current_active_user),
                db: Session = Depends(dependencies.get_db)):
    user_service = UserService(db)
    return user_service.change_password(username=current_user.username, user=user)


@router.delete("/")
def delete_user(current_user: schemas.User = Depends(dependencies.get_current_active_user),
                db: Session = Depends(dependencies.get_db)):
    user_service = UserService(db)
    return user_service.delete_user_by_name(username=current_user.username)


@router.post("/token", response_model=schemas.Token)
def login(token: dict = Depends(dependencies.login_for_access_token)):
    return token


@router.put("/token", response_model=schemas.Token)
def change_token(db: Session = Depends(dependencies.get_db), user: schemas.User = Depends(dependencies.login_for_user)):

    user_service = UserService(db)
    return user_service.change_token(user_id=user.id)

    return token

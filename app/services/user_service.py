import uuid
from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func, update, delete
from jose import JWTError, jwt

from app import models, schemas, custom_exceptions, security, config


class UserService:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_name(self, username: str):
        return self.db.query(models.User).filter(func.lower(models.User.username) == func.lower(username)).first()

    def get_user_by_uuid(self, token_uuid: str):
        return self.db.query(models.User).filter(models.User.token_uuid == token_uuid).first()

    def create_user(self, user: schemas.UserCreate):

        user_exists = self.get_user_by_name(user.username)
        if user_exists is not None:
            raise custom_exceptions.user_already_exists_exception

        user_dict = user.dict()
        hashed_password = security.get_password_hash(user_dict.get("password"))
        user_dict.update({"password": hashed_password})

        user = models.User(**user_dict)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def change_password(self, username: str, user: schemas.UserUpdate):
        hashed_password = security.get_password_hash(user.password)

        statement = update(models.User).where(models.User.username == username).\
            values(password=hashed_password).execution_options(synchronize_session='fetch')

        num_rows_matched = self.db.execute(statement).rowcount
        self.db.commit()

        if not num_rows_matched:
            raise custom_exceptions.user_not_found_exception
        return {"message": "Senha atualizada com sucesso"}

    def change_token(self, user_id: int):
        new_uuid = str(uuid.uuid4())

        statement = update(models.User).where(models.User.id == user_id). \
            values(token_uuid=new_uuid).execution_options(synchronize_session='fetch')

        num_rows_matched = self.db.execute(statement).rowcount
        self.db.commit()

        if not num_rows_matched:
            raise custom_exceptions.user_not_found_exception

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = UserService.create_access_token(
            data={"sub": new_uuid}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


    def delete_user_by_name(self, username: str):
        statement = delete(models.User).where(models.User.username == username).\
            execution_options(synchronize_session='fetch')

        num_rows_matched = self.db.execute(statement).rowcount
        self.db.commit()

        if not num_rows_matched:
            raise custom_exceptions.user_not_found_exception
        return {"message": "Usuário apagado com sucesso"}

    def get_user_by_token(self, token: str):
        try:
            payload = jwt.decode(token, config.TOKEN_KEY, algorithms=[config.TOKEN_ALGORITHM])
            token_uuid: str = payload.get("sub")
            if token_uuid is None:
                raise custom_exceptions.credentials_not_valid_exception
            token_data = schemas.TokenData(token_uuid=token_uuid)
        except JWTError:
            raise custom_exceptions.credentials_not_valid_exception

        user = self.get_user_by_uuid(token_uuid=token_data.token_uuid)

        if user is None:
            raise custom_exceptions.credentials_not_valid_exception
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if not expires_delta:
            expires_delta = timedelta(minutes=15)

        expire = datetime.utcnow() + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.TOKEN_KEY, algorithm=config.TOKEN_ALGORITHM)
        return encoded_jwt









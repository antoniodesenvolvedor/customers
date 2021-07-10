from datetime import datetime

from typing import Optional, List
from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    email: str
    cpf: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CustomerList(BaseModel):
    total: int
    items: List[Customer]

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    number: str


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    token_uuid: Optional[str] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True






from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    email: str
    cpf: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

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




from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.types import DateTime

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(BYTEA, nullable=False)
    cpf = Column(BYTEA)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    number = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    owner = relationship("Customer", back_populates="contacts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    token_uuid = Column(String(255), unique=True, nullable=False, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    disabled = Column(Boolean(), default=False)


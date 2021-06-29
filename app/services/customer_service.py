from sqlalchemy.orm import Session

from src.models import models
from src.schemas import schemas


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_customer(self, customer_id: int):
        return self.db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    def get_customer_by_email(self, email: str):
        return self.db.query(models.Customer).filter(models.Customer.email == email).first()

    def get_customers(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Customer).offset(skip).limit(limit).all()

    def create_customer(self, customer: schemas.CustomerCreate):
        db_customer = models.Customer(**customer.dict())
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer





from typing import Dict

from sqlalchemy.orm import Session
from sqlalchemy import update, delete, func
from fastapi import HTTPException, status

from app import models
from app import schemas
from app import security


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_customer(self, customer_id: int):
        customer = self.db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        return self.decrypt_customer_data(customer)

    def get_customers(self, skip: int = 0, limit: int = 100):
        customers = self.db.query(models.Customer).offset(skip).limit(limit).all()
        customers = list(map(self.decrypt_customer_data, customers))

        total_customers = self.db.query(func.count(models.Customer.id)).scalar()

        return {
            "total": total_customers,
            "items": customers
        }

    def create_customer(self, customer: schemas.CustomerCreate):

        customer_dict = customer.dict()
        encrypted_customer_dict = self.encrypt_customer_data(customer_dict)

        db_customer = models.Customer(**encrypted_customer_dict)
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)

        return self.decrypt_customer_data(db_customer)

    def delete_customer(self, customer_id: int):
        statement = delete(models.Customer).where(models.Customer.id == customer_id).\
            execution_options(synchronize_session='fetch')

        num_rows_matched = self.db.execute(statement).rowcount
        self.db.commit()

        if not num_rows_matched:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer não encontrado")
        else:
            return {"message": f"Customer {customer_id} apagado com sucesso"}

    def update_customer(self, customer_id: int, customer: schemas.CustomerCreate):

        customer_update_values = {key: value for key, value in customer.dict().items() if value}
        if not customer_update_values:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Necessário informar pelo menos um valor a ser atualizado")

        customer_update_values = self.encrypt_customer_data(customer_update_values)

        statement = update(models.Customer).where(models.Customer.id == customer_id).values(**customer_update_values).\
            execution_options(synchronize_session='fetch')

        num_rows_matched = self.db.execute(statement).rowcount
        self.db.commit()

        if not num_rows_matched:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer não encontrado")
        else:
            return {"messange": f"Customer {customer_id} atualizado com sucesso"}


    @staticmethod
    def encrypt_customer_data(customer: Dict) -> Dict:
        cryptographer = security.Cryptographer()

        for key, value in customer.items():
            if key in ('email', 'cpf'):
                if value:
                    customer[key] = cryptographer.encrypt(value)

        return customer


    @staticmethod
    def decrypt_customer_data(customer: models.Customer) -> models.Customer:
        cryptographer = security.Cryptographer()

        if customer.email:
            customer.email = cryptographer.decrypt(customer.email)
        if customer.cpf:
            customer.cpf = cryptographer.decrypt(customer.cpf)

        return customer








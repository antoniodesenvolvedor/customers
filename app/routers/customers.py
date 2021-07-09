from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import schemas
from app.services.customer_service import CustomerService
from app import dependencies





router = APIRouter(
    prefix="/customers",
    # tags=["customers"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)





@router.get("/users/me", response_model=dependencies.User)
async def read_users_me(current_user: dependencies.User = Depends(dependencies.get_current_active_user)):
    return current_user

@router.get("/users/me/items/")
async def read_ows_items(current_user: dependencies.User = Depends(dependencies.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post('/', response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(dependencies.get_db)):
    customer_service = CustomerService(db)
    return customer_service.create_customer(customer=customer)
#
# @router.get('/{customer_id}', response_model=schemas.Customer)
# def read_customer(customer_id: int = 0, db: Session = Depends(get_db)):
#     customer_service = CustomerService(db)
#     customer = customer_service.get_customer(customer_id=customer_id)
#     if not customer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer não encontrado")
#     return customer
#
#
#
# @router.get('/', response_model=schemas.CustomerList)
# def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     customer_service = CustomerService(db)
#     return customer_service.get_customers(skip=skip, limit=limit)


@router.delete('/{customer_id}')
def delete_customer(customer_id: int, db: Session = Depends(dependencies.get_db)):
    customer_service = CustomerService(db)
    return customer_service.delete_customer(customer_id=customer_id)



@router.put('/{customer_id}')
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(dependencies.get_db)):
    customer_service = CustomerService(db)
    return customer_service.update_customer(customer_id=customer_id, customer=customer)



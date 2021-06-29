from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_token_header

router = APIRouter(
    prefix="/customers",
    # tags=["customers"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post('/', response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    customer_service = CustomerService(db)
    db_customer = customer_service.get_customer_by_email(email=customer.email)
    if db_customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    return customer_service.create_customer(customer=customer)

@router.get('/', response_model=List[schemas.Customer])
def read_customer(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customer_service = CustomerService(db)
    customers = customer_service.get_customers(skip=skip, limit=limit)
    return customers

@router.get('/{customer_id}', response_model=schemas.Customer)
def read_customer(customer_id: int = 0, db: Session = Depends(get_db)):
    customer_service = CustomerService(db)
    customer = customer_service.get_customer(customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return customer
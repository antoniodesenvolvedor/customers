# from app.dependencies import get_db
# from contextlib import contextmanager
# from app.database import SessionLocal
# from app import models


import os
import fastapi
import requests
import uvicorn
import cryptography
if True:
    print("Olha")




print(os.environ.get('POSTGRES_USER', 'defaultttt'))
print(os.getenv('POSTGRES_USER', 'defaultttt'))

# def testando():
#     connection = SessionLocal()
#     customers = connection.query(models.Customer).all()
#     for customer in customers:
#         print(customer.name)
#
#
#
# if __name__ == "__main__":
#     testando()

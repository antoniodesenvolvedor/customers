from fastapi import FastAPI

from app import models
from app.database import engine

# app.include_router(contacts.router)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()








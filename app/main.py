from fastapi import FastAPI, Depends
import uvicorn

from app import models
from app.database import engine
from app.routers import customers, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customers.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8001)








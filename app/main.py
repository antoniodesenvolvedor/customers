from fastapi import FastAPI, Depends
import uvicorn


from app import models
from app.database import engine
from app.routers import customers
from app import dependencies
from app import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customers.router)


@app.post("/token", response_model=schemas.Token)
def login(token: dict = Depends(dependencies.login_for_access_token)):
    return token


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8001)








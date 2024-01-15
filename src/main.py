from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from .routers import auth 
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(auth.router)

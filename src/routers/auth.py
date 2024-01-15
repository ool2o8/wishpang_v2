from fastapi import APIRouter

from ..db.database import SessionLocal

router = APIRouter(
    prefix="/api/auth",
)


@router.get("/login")
def login():
    return {"Hello": "login"}
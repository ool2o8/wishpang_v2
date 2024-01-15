from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ..db.database import SessionLocal
from ..core.config import KAKAO_REST_API_KEY
import status
router = APIRouter(
    prefix="/api/auth",
)



@router.get("/login/callback")
def login():
    return {"Hello": "callback"}

@router.get("/login")
def login():
    REDIRECT_URI = 'http://127.0.0.1/api/auth/login/callback'

    API_HOST = f'https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&prompt=login'

    return RedirectResponse(url=API_HOST, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

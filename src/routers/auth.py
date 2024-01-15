from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import insert, select

from ..db.database import SessionLocal, get_db
from ..core.config import KAKAO_REST_API_KEY
import status, requests
from sqlalchemy.orm import Session
from ..models.models import User

router = APIRouter(
    prefix="/api/auth",
)


kakao_token_api = 'https://kauth.kakao.com/oauth/token'
@router.get("/login/callback")
def login(code:str, db: Session = Depends(get_db)):
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_REST_API_KEY,
        'redirection_uri': 'http://127.0.0.1',
        'code': code
    }
    token_response = requests.post(kakao_token_api, data=data)
    access_token = token_response.json().get('access_token')

    response = requests.get(
        'https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    if response.status_code==200:
        user_info=response.json()
        stmt=select(User).where(User.kakao_id == user_info["id"])
        user=db.execute(stmt).scalar_one_or_none()
        if not user:
            stmt=insert(User).values(kakao_id=user_info["id"]).returning(User.id, User.kakao_id, User.created_at)
            user=db.execute(stmt).scalar()
            db.commit()
    return user

@router.get("/login")
def login():
    REDIRECT_URI = 'http://127.0.0.1/api/auth/login/callback'

    API_HOST = f'https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&prompt=select_account'

    return RedirectResponse(url=API_HOST, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

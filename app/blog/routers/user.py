from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from blog import schema
from  blog.db.database import SessionLocal, engine, get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from blog.auth_token import get_current_user

from blog.repository import user


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)

@router.post('/', response_model=schema.ShowUser, )
def create_user(req: schema.User, response: Response, db: Session = Depends(get_db)):
    return user.create_user(req, response, db)

@router.get('/{user_id}', response_model=schema.ShowUser, )
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return user.get_user_by_id(user_id, db)

@router.get('/', response_model=schema.ShowUser, )
def get_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return user.get_user(current_user, db)
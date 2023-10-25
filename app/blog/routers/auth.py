from fastapi import APIRouter, Depends, HTTPException, Response
from blog.hashing import Hash
from blog import schema, models
from blog.db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from blog.auth_token import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
tags=['Auth'],
prefix="/api/v1/auth"
) 

@router.post('/login')
def login(response: Response, req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == req.username).first()
  if not user:
      raise HTTPException(status_code=404, detail=f"User not registered")
  if not Hash.verify(req.password, user.password):
    raise HTTPException(status_code=401, detail="Password incorrect")
  
  # generate and return jwt
  access_token = create_access_token(data={"sub": user.username})
  return {"access_token": access_token, "token_type": "bearer"}
  # return user
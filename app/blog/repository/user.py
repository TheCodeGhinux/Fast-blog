from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from blog import models
from passlib.context import CryptContext
from blog.hashing import Hash

def get_all_users():
  pass

def get_user(user_id, db: Session):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
      raise HTTPException(status_code=404, detail=f"User does not exist")
  return user

def create_user(req, response, db: Session):
  hashedPassword = Hash.bcrypt(req.password)
  new_user = models.User(firstname=req.firstname, lastname=req.lastname, username=req.username, password=hashedPassword)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  response.status_code = status.HTTP_201_CREATED
  return new_user
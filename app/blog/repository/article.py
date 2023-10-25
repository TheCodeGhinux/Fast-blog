from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from blog import models
from blog import schema

def get_all(db: Session):
  articles = db.query(models.article).all()
  return articles

def get_article(db: Session, article_id):
  article = db.query(models.article).filter(models.article.id == article_id).first()
  if not article:
      raise HTTPException(status_code=404, detail=f"article with id {article_id} not found")
  return article

def create_article(req, response, db: Session, current_user_id: int):
    new_article = models.article(title=req.title, body=req.body, creator_id=current_user_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    response.status_code = status.HTTP_201_CREATED
    return new_article

def update_article(article_id, req, response, db: Session, current_user: schema.User):
    article = db.query(models.article).filter(models.article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail=f"Article with id {article_id} not found")

    if article.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    article.title = req.title
    article.body = req.body

    db.commit()
    db.refresh(article)
    response.status_code = status.HTTP_200_OK
    return article

def delete_article(article_id, response, db: Session, current_user: schema.User):
    article = db.query(models.article).filter(models.article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail=f"Article with id {article_id} not found")

    if article.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(article)
    db.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return {"detail": f"Article with id {article_id} deleted successfully"}
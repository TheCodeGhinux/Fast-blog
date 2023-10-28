from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from blog import models, schema

def get_all(db: Session):
  articles = db.query(models.Article).all()
  return articles

def get_article(db: Session, article_id):
  article = db.query(models.Article).filter(models.Article.id == article_id).first()
  if not article:
      raise HTTPException(status_code=404, detail=f"article with id {article_id} not found")
  return article

def create_article(req, response, db: Session, current_user_id: int):
    new_article = models.Article(title=req.title, content=req.content, blog_id=req.blog_id, creator_id = current_user_id )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    response.status_code = status.HTTP_201_CREATED
    return new_article

def update_article(article_id, req, response, db: Session, current_user: schema.User):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail=f"Article with id {article_id} not found")

    if article.creator_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    article.title = req.title
    article.content = req.content

    db.commit()
    db.refresh(article)
    response.status_code = status.HTTP_200_OK
    return article

def delete_article(article_id, response, db: Session, current_user: schema.User):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail=f"Article with id {article_id} not found")

    if article.creator_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(article)
    db.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return {"detail": f"Article with id {article_id} deleted successfully"}

async def like_article(article_id: int, db: Session, current_user):
    # Your logic to like an article here
    article = db.query(models.Article).filter(models.Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Create an instance of ArticleLike and link it to the current_user and the article
    article_like = models.ArticleLike(creator_id=current_user, article_id=article_id)
    db.add(article_like)
    db.commit()
    db.refresh(article_like)

    return article_like

async def unlike_article(article_id: int, db: Session, current_user: schema.User):
    # Your logic to unlike an article here
    article_like = db.query(models.ArticleLike).filter_by(creator_id=current_user, article_id=article_id).first()

    if not article_like:
        raise HTTPException(status_code=404, detail="Article like not found")

    db.delete(article_like)
    db.commit()

    return article_like

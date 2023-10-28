from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from blog.auth_token import get_current_user
from blog.repository import article as article_repo
from blog import schema
from blog.db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

# models.Base.metadata.create_all(engine)

router = APIRouter(
    prefix="/api/v1/article",
    tags=["article"]
)


@router.get("/", response_model=List[schema.Article], )
def get_all_article(db: Session = Depends(get_db)):
    return article_repo.get_all(db)


@router.get("/{article_id}", response_model=schema.Article, )
def get_article(article_id: int, response: Response, db: Session = Depends(get_db)):
    return article_repo.get_article(db, article_id)


@router.post("/", response_model=schema.Article, )
def create_article(req: schema.ArticleBase, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    return article_repo.create_article(req, response, db, current_user)


@router.put("/{article_id}", response_model=schema.Article, )
def update_article(article_id: int, req: schema.ArticleUpdateBase, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    return article_repo.update_article(article_id, req, response, db, current_user)


@router.delete("/{article_id}", )
def delete_article(article_id: int, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    return article_repo.delete_article(article_id, response, db, current_user)

@router.put("/{article_id}/like", response_model=schema.ArticleLike)
async def like_article(article_id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    return await article_repo.like_article(article_id, db, current_user)


@router.delete("/{article_id}/unlike", response_model=schema.ArticleLike)
async def unlike_article(article_id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    return await article_repo.unlike_article(article_id, db, current_user)
from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from blog.auth_token import get_current_user
from blog.repository import blog as blog_repo
from blog import schema
from  blog.db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)

from blog.repository import blog
# from .schemas import Blog, BlogCreate, BlogUpdate

router = APIRouter(
      prefix="/api/v1/blogs",
    tags=["blogs"]
)


@router.get("/", response_model=List[schema.Blog])
async def get_all_blogs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    print(current_user)
    logger.info(current_user)
    return await blog_repo.get_all_blogs(db)


@router.get("/{blog_id}", response_model=schema.Blog)
async def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = await blog_repo.get_blog(blog_id, db)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.post("/", response_model=schema.Blog)
async def create_blog(req: schema.BlogBase, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    return await blog_repo.create_blog(req, response, db, current_user)


@router.put("/{blog_id}", response_model=schema.Blog)
async def update_blog(blog_id: int, req: schema.BlogBase, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    updated_blog = await blog_repo.update_blog(blog_id, req, response, db, current_user)
    if updated_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog


@router.delete("/{blog_id}")
async def delete_blog(blog_id: int, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    deleted_blog = await blog_repo.delete_blog(db, blog_id, response, current_user)
    if deleted_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return deleted_blog

@router.post("/{blog_id}/like", response_model=schema.BlogLike)
async def like_blog(blog_id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    liked_blog = await blog_repo.like_blog(blog_id, db, current_user)
    if not liked_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return liked_blog


@router.post("/{blog_id}/unlike", response_model=schema.BlogLike)
async def unlike_blog(blog_id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    unliked_blog = await blog_repo.unlike_blog(blog_id, db, current_user)
    if not unliked_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return unliked_blog
from typing import List
from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from blog import models, schema


async def get_all_blogs(db: Session):
    return db.query(models.Blog).all()


async def get_blog(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"article with id {blog_id} not found")
    return blog
    # return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


async def create_blog(req, response, db: Session, current_user):
    db_blog = models.Blog(
        title=req.title, description=req.description, creator_id=current_user)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    response.status_code = status.HTTP_201_CREATED
    return db_blog


async def update_blog(blog_id, req, response, db: Session, current_user):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog.creator_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not db_blog:
        raise HTTPException(
            status_code=404, detail=f"Blog with id {blog_id} not found")
    else:
        for var, value in vars(req).items():
            setattr(db_blog, var, value) if value else None
        db.commit()
        db.refresh(db_blog)
        response.status_code = status.HTTP_200_OK
    return db_blog


async def delete_blog(db: Session, blog_id: int, response, current_user):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog.creator_id != current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if db_blog:
        db.delete(db_blog)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    return db_blog

async def like_blog(blog_id: int, db: Session, creator_id: int):
    db_blog_like = db.query(models.BlogLike).filter(
        models.BlogLike.blog_id == blog_id, models.BlogLike.creator_id == creator_id).first()
    if db_blog_like:
        raise HTTPException(
            status_code=400, detail="Blog already liked by this user")
    else:
        new_blog_like = models.BlogLike(blog_id=blog_id, creator_id=creator_id)
        db.add(new_blog_like)
        db.commit()
        db.refresh(new_blog_like)
        return new_blog_like


async def unlike_blog(blog_id: int, db: Session, creator_id: int):
    db_blog_like = db.query(models.BlogLike).filter(
        models.BlogLike.blog_id == blog_id, models.BlogLike.creator_id == creator_id).first()
    if not db_blog_like:
        raise HTTPException(
            status_code=400, detail="Blog not liked by this user")
    else:
        db.delete(db_blog_like)
        db.commit()
        return db_blog_like

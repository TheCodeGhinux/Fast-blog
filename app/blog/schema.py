from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    username: str
    password: str

class BlogBase(BaseModel):
    title: str
    description: str

class ArticleBase(BaseModel):
    blog_id: int
    title: str
    content: str

class ArticleUpdateBase(BaseModel):
    title: str
    content: str

class CommentBase(BaseModel):
    content: str

class BlogLike(BaseModel):
    id: int
    blog_id: int
    creator_id: int

class ArticleLike(BaseModel):
    id: int
    article_id: int
    creator_id: int

class CommentLike(BaseModel):
    id: int
    comment_id: int
    creator_id: int

class User(UserBase):
    class Config:
        orm_mode = True

class Blog(BlogBase):
    id: int
    creator_id: int
    articles: List[ArticleBase] = []
    blog_likes: List["BlogLike"] = []

    class Config:
        orm_mode = True

class Article(ArticleBase):
    id: int
    blog_id: int
    article_comments: List[CommentBase] = []
    article_likes: List["ArticleLike"] = []

    class Config:
        orm_mode = True

class Comment(CommentBase):
    id: int
    article_id: int
    creator_id: int
    comment_likes: List[CommentLike] = []

    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    blog: List[Blog] = []

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str

class ShowArticle(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

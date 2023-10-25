from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    username: str
    password: str
    
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class BlogBase(BaseModel):
    title: str
    description: str

class Blog(BlogBase):
    id: int
    user_id: int
    articles: List["Article"] = []
    blog_likes: List["BlogLike"] = []

    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    content: str

class Article(ArticleBase):
    id: int
    blog_id: int
    article_comments: List["Comment"] = []
    article_likes: List["ArticleLike"] = []

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class Comment(CommentBase):
    id: int
    article_id: int
    user_id: int
    comment_likes: List["CommentLike"] = []

    class Config:
        from_attributes = True

class BlogLike(BaseModel):
    id: int
    blog_id: int
    user_id: int

    class Config:
        from_attributes = True

class ArticleLike(BaseModel):
    id: int
    article_id: int
    user_id: int

    class Config:
        from_attributes = True

class CommentLike(BaseModel):
    id: int
    comment_id: int
    user_id: int

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    posts: List["Blog"] = []

    class Config:
        from_attributes = True

class Post(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    posts: List[Post]

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class ShowPost(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
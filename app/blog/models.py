from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from blog.db.database import Base


# class Post(Base):
#     __tablename__ = 'posts'

#     id = Column(Integer, primary_key= True, index=True)
#     title = Column(String)
#     body = Column(String)
#     creator_id = Column(Integer, ForeignKey("users.id"))
    
#     creator = relationship("User", back_populates="posts")

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     firstname = Column(String, index=True)
#     lastname = Column(String, index=True)
#     username = Column(String, unique=True, index=True)
#     password = Column(String)
#     # is_active = Column(Boolean, default=True)

#     posts = relationship("Post", back_populates="creator")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    blogs = relationship("Blog", back_populates="user")

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    articles = relationship("Article", back_populates="blog")
    blog_likes = relationship("BlogLike", back_populates="blog")

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    article_comments = relationship("Comment", back_populates="article")
    article_likes = relationship("ArticleLike", back_populates="article")

class BlogLike(Base):
    __tablename__ = 'blog_likes'
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    comment_likes = relationship("CommentLike", back_populates="comment")

class ArticleLike(Base):
    __tablename__ = 'article_likes'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

class CommentLike(Base):
    __tablename__ = 'comment_likes'
    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


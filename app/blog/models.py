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
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)

    blogs = relationship("Blog", back_populates="user")
    articles = relationship("Article", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    blog_likes = relationship("BlogLike", back_populates="user")
    article_likes = relationship("ArticleLike", back_populates="user")
    comment_likes = relationship("CommentLike", back_populates="user")


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="blogs")
    articles = relationship("Article", back_populates="blog", cascade="all, delete")
    blog_likes = relationship("BlogLike", back_populates="blog")


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    creator_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="articles")
    blog = relationship("Blog", back_populates="articles")
    article_comments = relationship("Comment", back_populates="article")
    article_likes = relationship("ArticleLike", back_populates="article")


class BlogLike(Base):
    __tablename__ = 'blog_likes'
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    creator_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="blog_likes")
    blog = relationship("Blog", back_populates="blog_likes")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    article_id = Column(Integer, ForeignKey('articles.id'))
    creator_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="comments")
    comment_likes = relationship("CommentLike", back_populates="comment")
    article = relationship("Article", back_populates="article_comments", cascade="all, delete") 


class ArticleLike(Base):
    __tablename__ = 'article_likes'
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    creator_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="article_likes")
    article = relationship("Article", back_populates="article_likes")


class CommentLike(Base):
    __tablename__ = 'comment_likes'
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    creator_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="comment_likes")
    comment = relationship("Comment", back_populates="comment_likes")

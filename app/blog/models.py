import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship("Image")

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
    image_id = Column(Integer, ForeignKey('images.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

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
    image_id = Column(Integer, ForeignKey('images.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

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


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

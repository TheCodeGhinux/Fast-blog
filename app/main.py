from typing import Union
from fastapi import FastAPI
from blog.routers import user, blog, article, auth
# from repository import user
from blog import models
from blog.db.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(article.router)
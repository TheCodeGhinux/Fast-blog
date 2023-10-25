import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://codeghinux:password@localhost:5432/fast-blog"

SQLALCHEMY_DATABASE_URL = "postgresql://codeghinux:0661TAWRXjxUdD234Mo7eXRACHDy2mWy@dpg-cksgk96nfb1c73epeakg-a.oregon-postgres.render.com:5432/tcgblog"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# if os.getenv('DATABASE_URL'):
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
# else:
#     SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

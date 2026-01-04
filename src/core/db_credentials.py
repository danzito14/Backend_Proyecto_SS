from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()  # ✅ BASE ORM REAL

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./mydb.sqlite3"  # или твоё значение

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
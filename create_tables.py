from pathlib import Path
from sqlalchemy import create_engine
from models import Base

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mydb.sqlite3"
engine = create_engine(f"sqlite:///{DB_PATH}")

if __name__ == "__main__":
    print("Создаём таблицы в", DB_PATH)
    Base.metadata.create_all(bind=engine)
    print("Готово")

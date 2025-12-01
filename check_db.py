# для проверки содержимого БД
from pathlib import Path
from sqlalchemy import create_engine, inspect
from models import Base

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mydb.sqlite3"
print("DB:", DB_PATH, "exists:", DB_PATH.exists())

engine = create_engine(f"sqlite:///{DB_PATH}")
insp = inspect(engine)
print("Tables:", insp.get_table_names())
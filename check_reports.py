# проверка корректности создания таблиц reports
import os
from sqlalchemy import create_engine, inspect, text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mydb.sqlite3")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

insp = inspect(engine)
print("Tables:", insp.get_table_names())

with engine.connect() as conn:
    rows = conn.execute(
        text("SELECT id, report_at, order_id, count_product FROM order_reports")
    ).fetchall()
    print("order_reports rows:", rows)

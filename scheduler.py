from datetime import date
from pathlib import Path

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from taskiq_aio_pika import AioPikaBroker
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from models import Order, Product
from models import OrderReport

# --- конфигурация БД (аналогично rabbitMQ.py) ---

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mydb.sqlite3"

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# --- брокер TaskIQ на RabbitMQ ---

broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/local",
    exchange_name="report",
    queue_name="cmd_order",
)

# --- планировщик ---

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

# --- задача по расписанию: сформировать отчёт по заказам ---

@broker.task(
    schedule=[
        {
            # пример: запуск каждый день в 00:00
            "cron": "0 0 * * *",
            "schedule_id": "orders_daily_report",
            # здесь можно передавать аргументы, если нужны
        }
    ]
)
async def my_scheduled_task() -> str:
    """
    Периодическая задача:
    - ищет заказы за текущий день,
    - считает количество товаров в каждом,
    - пишет строки в таблицу order_reports.
    """
    today = date.today()

    async with async_session() as session:
        # вариант Order и Product связаны через relationship Order.products
        result = await session.execute(
            select(
                Order.id.label("order_id"),
                func.count(Product.id).label("count_product"),
            )
            .join(Order.products)
            .where(func.date(Order.created_at) == today)
            .group_by(Order.id)
        )

        rows = result.all()

        for row in rows:
            report = OrderReport(
                report_at=today,
                order_id=row.order_id,
                count_product=row.count_product,
            )
            session.add(report)

        await session.commit()

    return f"Created {len(rows)} report rows for {today.isoformat()}"

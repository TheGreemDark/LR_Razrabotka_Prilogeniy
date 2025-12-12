import asyncio
import os
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User
from models import OrderReport
from models import Order

from datetime import date, datetime
from models import User, Address, Order, OrderReport 

# Формируем путь к БД в том же каталоге, где лежит init_db.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'mydb.sqlite3')}",
)


async def init_db() -> None:
    # Создаём async-engine
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Полностью пересоздаём схему для всех моделей, привязанных к Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Создаём сессию
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Добавляем тестовые данные
    async with async_session() as session:
        # 1. пользователь
        user = User(
            username="test_user",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        session.add(user)
        await session.flush()  # получим user.id

        # 2. адрес пользователя
        address = Address(
            user_id=user.id,
            city="Test City",
            street="Test Street, 1",
        )
        session.add(address)
        await session.flush()  # получим address.id

        # 3. заказ с валидным shipping_address_id
        order = Order(
            user_id=user.id,
            shipping_address_id=address.id,  # вот здесь раньше было None
            created_at=datetime(2025, 12, 10),
        )
        session.add(order)
        await session.flush()  # order.id

        # 4. (опционально) продукт и позиция отчёта
        report_row = OrderReport(
            report_at=date(2025, 12, 10),
            order_id=order.id,
            count_product=3,
        )
        session.add(report_row)

        await session.commit()


    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database initialized successfully!")

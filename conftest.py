import pytest
import pytest_asyncio
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from models import Base

# URL тестовой базы данных SQLite с асинхронным драйвером
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def engine():
    # Создаём асинхронный движок SQLAlchemy для подключения к тестовой базе данных
    return create_async_engine(TEST_DATABASE_URL, echo=True)


@pytest_asyncio.fixture(scope="session")
async def tables(engine):
    # Создаём и удаляем таблицы в БД на уровне всей сессии тестов
    async with engine.begin() as conn:
        # Удаляем все таблицы, если они есть (чистим БД)
        await conn.run_sync(Base.metadata.drop_all)
        # Создаём все таблицы по моделям из Base
        await conn.run_sync(Base.metadata.create_all)
    yield
    # После завершения тестов удаляем созданные таблицы для очистки
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(engine, tables):
    # Создаём асинхронную сессию для работы с БД с отключённым expire_on_commit
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    # Создаём контекст сессии, используемый в каждом тесте
    async with async_session() as session:
        yield session  # Передаём сессию тестам


@pytest.fixture
def user_repository(session):
    # Фикстура для создания репозитория пользователей с текущей сессией
    return UserRepository(session)


@pytest.fixture
def product_repository(session):
    # Фикстура для создания репозитория продуктов с текущей сессией
    return ProductRepository(session)


@pytest.fixture
def order_repository(session):
    # Фикстура для создания репозитория заказов с текущей сессией
    return OrderRepository(session)


@pytest.fixture
def client():
    return TestClient(app=app)

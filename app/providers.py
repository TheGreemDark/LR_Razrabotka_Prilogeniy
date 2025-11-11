from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    from app.main import async_session_factory
    async with async_session_factory() as session:
        yield session

async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Database session provider"""
    async for session in get_session():
        yield session

async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """User repository provider"""
    repo = UserRepository()
    repo.session = db_session
    return repo

async def provide_user_service(user_repository: UserRepository) -> UserService:
    """User service provider"""
    return UserService(user_repository)
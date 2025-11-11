import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import Base

# Database configuration
DATABASE_URL = "sqlite+aiosqlite:///mydb.sqlite3"

async def init_db():
    # Create engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Create a test user
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        from app.models.user import User
        test_user = User(
            username="test_user",
            email="test@example.com",
            full_name="Test User"
        )
        session.add(test_user)
        await session.commit()

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database initialized successfully!")
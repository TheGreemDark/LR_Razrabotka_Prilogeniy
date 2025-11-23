from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filter(
        self, count: int | None = None, page: int | None = None, **filters
    ) -> list[User]:
        stmt = select(User)
        if filters:
            for attr, val in filters.items():
                if val is not None and hasattr(User, attr):
                    stmt = stmt.where(getattr(User, attr) == val)

        if count is not None and page is not None:
            stmt = stmt.offset((page - 1) * count).limit(count)

        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as err:
            await self.session.rollback()
            raise err

    async def update(self, user_id: int, user_data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        update_fields = user_data.model_dump(exclude_unset=True)
        for key, value in update_fields.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

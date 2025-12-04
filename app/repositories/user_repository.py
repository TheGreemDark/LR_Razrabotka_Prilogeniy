from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.redis_cache import get_redis_cache
from app.schemas.user_schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self):
        self.session: AsyncSession | None = None
        self.cache = get_redis_cache()
        self.cache_ttl = 3600  # 1 час в секундах

    def _get_cache_key(self, user_id: int) -> str:
        """Получить ключ кэша для пользователя"""
        return f"user:{user_id}"

    def _user_to_dict(self, user: User) -> dict:
        """Конвертировать User в dict для кэша"""
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,  # Используем first_name
            "last_name": user.last_name,  # Используем last_name
        }

    async def get_by_id(self, user_id: int) -> User | None:
        cache_key = self._get_cache_key(user_id)
        cached_data = self.cache.get(cache_key)

        if cached_data:
            print(f"[CACHE HIT] User {user_id} from cache")
            user = User(**cached_data)
            return user

        print(f"[CACHE MISS] User {user_id} from database")
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            self.cache.set(cache_key, self._user_to_dict(user), self.cache_ttl)

        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filter(
        self, count: int | None = None, page: int | None = None, **kwargs
    ) -> list[User]:
        query = select(User)
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(User, key) and value is not None:
                    query = query.where(getattr(User, key) == value)

        if count is not None and page is not None:
            offset = (page - 1) * count
            query = query.offset(offset).limit(count)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, user_data: UserCreate) -> User:
        try:
            user = User(
                username=user_data.username,
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, user_id: int, user_data: UserUpdate) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return None

        update_dict = user_data.model_dump(exclude_unset=True)

        if user_data.first_name or user_data.last_name:
            user.first_name = user_data.first_name or user.first_name
            user.last_name = user_data.last_name or user.last_name

        for field, value in update_dict.items():
            if field not in ["first_name", "last_name"] and hasattr(user, field):
                setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)

        cache_key = self._get_cache_key(user_id)
        self.cache.delete(cache_key)
        print(f"[CACHE DELETE] User {user_id} removed from cache after update")

        return user

    async def delete(self, user_id: int) -> None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            await self.session.delete(user)
            await self.session.commit()

            cache_key = self._get_cache_key(user_id)
            self.cache.delete(cache_key)
            print(f"[CACHE DELETE] User {user_id} removed from cache after delete")

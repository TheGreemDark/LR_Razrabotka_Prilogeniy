from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(
        self, count: int = 10, page: int = 1, **filters
    ) -> list[User]:
        return await self.user_repository.get_by_filter(
            count=count, page=page, **filters
        )

    async def create(self, user_data: UserCreate) -> User:
        # Проверяем наличие пользователя с таким username или email
        existing_users = await self.user_repository.get_by_filter(
            username=user_data.username
        )
        if any(user.email == user_data.email for user in existing_users):
            raise ValueError("Пользователь с таким username или email уже существует")

        if existing_users:
            raise ValueError("Пользователь с таким username уже существует")

        return await self.user_repository.create(user_data)

    async def update(self, user_id: int, user_data: UserUpdate) -> User | None:
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)

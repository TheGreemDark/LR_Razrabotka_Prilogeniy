import pytest
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate

class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        """Тест создания пользователя в репозитории"""
        # Формируем данные для нового пользователя
        user_data = UserCreate(
            email="test@example.com",
            username="john_doe",
            first_name="John",
            last_name="Doe",
        )
        
        # Вызываем метод создания пользователя в репозитории
        user = await user_repository.create(user_data)
        
        # Проверяем, что у пользователя появился id (создан в БД)
        assert user.id is not None
        # Проверяем правильность сохранённых полей
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.username == "john_doe"

    @pytest.mark.asyncio
    async def test_get_by_email(self, user_repository: UserRepository):
        """Тест получения пользователя по email"""
        # Создаём нового пользователя для поиска
        user = await user_repository.create(
            UserCreate(
                email="unique@example.com",
                username="user_test",
                first_name="Test",
                last_name="User",
            )
        )
        
        # Пытаемся получить пользователя из репозитория по email
        found_user = await user_repository.get_by_email("unique@example.com")
        
        # Проверяем, что пользователь найден
        assert found_user is not None
        # Проверяем идентификацию по id
        assert found_user.id == user.id
        # Проверяем совпадение email
        assert found_user.email == "unique@example.com"

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        """Тест обновления пользователя"""
        # Создаём пользователя с исходными данными
        user = await user_repository.create(
            UserCreate(
                email="update@example.com",
                username="test",
                first_name="Original",
                last_name="Name",
            )
        )
        
        # Обновляем только поле first_name у пользователя
        updated_user = await user_repository.update(
            user.id,
            UserUpdate(first_name="Updated")
        )
        
        # Проверяем, что username остался без изменений
        assert updated_user.username == "test"
        # Проверяем, что first_name обновился на новое значение
        assert updated_user.first_name == "Updated"
        # Проверяем, что last_name остался прежним
        assert updated_user.last_name == "Name"
    @pytest.mark.asyncio
    async def test_get_by_filter(self, user_repository: UserRepository):
        """Тест получения списка всех пользователей"""
        # Создаём нескольких пользователей
        await user_repository.create(
            UserCreate(
                email="user1@example.com", username="user1", first_name="User1", last_name="One"
            )
        )
        await user_repository.create(
            UserCreate(
                email="user2@example.com", username="user2", first_name="User2", last_name="Two"
            )
        )
        # Получаем список всех пользователей
        user_list = await user_repository.get_by_filter()
        # Проверяем, что список содержит хотя бы двух пользователей
        emails = [u.email for u in user_list]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert len(user_list) >= 1

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        """Тест удаления пользователя"""
        # Создаём пользователя
        user = await user_repository.create(
            UserCreate(
                email="delete_me@example.com", username="delete_me", first_name="Delete", last_name="Me"
            )
        )
        # Удаляем пользователя
        await user_repository.delete(user.id)
        # Пытаемся получить пользователя по email после удаления
        deleted_user = await user_repository.get_by_email("delete_me@example.com")
        # Проверяем, что пользователь не найден
        assert deleted_user is None
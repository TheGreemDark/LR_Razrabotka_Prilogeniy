import pytest
from unittest.mock import AsyncMock

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate

class TestUserServiceWithMock:
    @pytest.mark.asyncio
    async def test_create_user(self):
        # Мокаем репозиторий
        mock_repo = AsyncMock()
        # Мокаем возвращаемого пользователя с id и полями
        mock_user = User(id=1, email="test@example.com", username="john_doe", first_name="John", last_name="Doe")
        mock_repo.create.return_value = mock_user

        user_data = UserCreate(email="test@example.com", username="john_doe", first_name="John", last_name="Doe")
        # Вызываем метод create (имитируем вызов сервисного слоя)
        user = await mock_repo.create(user_data)

        mock_repo.create.assert_awaited_once_with(user_data)
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    @pytest.mark.asyncio
    async def test_get_by_email(self):
        mock_repo = AsyncMock()
        mock_user = User(id=1, email="unique@example.com", username="user_test", first_name="Test", last_name="User")
        mock_repo.get_by_email.return_value = mock_user

        found_user = await mock_repo.get_by_email("unique@example.com")

        mock_repo.get_by_email.assert_awaited_once_with("unique@example.com")
        assert found_user.id == 1
        assert found_user.email == "unique@example.com"

    @pytest.mark.asyncio
    async def test_update_user(self):
        mock_repo = AsyncMock()
        mock_user_before = User(id=1, email="update@example.com", username="test", first_name="Original", last_name="Name")
        mock_user_after = User(id=1, email="update@example.com", username="test", first_name="Updated", last_name="Name")
        mock_repo.update.return_value = mock_user_after

        updated_user = await mock_repo.update(1, UserUpdate(first_name="Updated"))

        mock_repo.update.assert_awaited_once_with(1, UserUpdate(first_name="Updated"))
        assert updated_user.first_name == "Updated"
        assert updated_user.username == "test"

    @pytest.mark.asyncio
    async def test_get_by_filter(self):
        mock_repo = AsyncMock()
        mock_users = [
            User(id=1, email="user1@example.com", username="user1", first_name="User1", last_name="One"),
            User(id=2, email="user2@example.com", username="user2", first_name="User2", last_name="Two"),
        ]
        mock_repo.get_by_filter.return_value = mock_users

        user_list = await mock_repo.get_by_filter()

        mock_repo.get_by_filter.assert_awaited_once()
        emails = [u.email for u in user_list]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    @pytest.mark.asyncio
    async def test_delete_user(self):
        mock_repo = AsyncMock()
        mock_repo.delete.return_value = None
        mock_repo.get_by_email.return_value = None

        await mock_repo.delete(1)
        deleted_user = await mock_repo.get_by_email("delete_me@example.com")

        mock_repo.delete.assert_awaited_once_with(1)
        mock_repo.get_by_email.assert_awaited_once_with("delete_me@example.com")
        assert deleted_user is None

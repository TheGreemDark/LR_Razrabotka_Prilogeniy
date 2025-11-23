from typing import Any, List

import pytest
from litestar import Litestar
from litestar.di import Provide
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from litestar.testing import create_test_client

from app.controllers.user_controller import UserController
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.user_service import UserService


def _user_dict(
    *,
    id: int = 1,
    username: str = "john",
    email: str = "john@example.com",
    first_name: str = "John",
    last_name: str = "Doe",
) -> dict[str, Any]:
    return {
        "id": id,
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }


def _user_obj(**kwargs) -> User:
    return User(**kwargs)


@pytest.mark.asyncio
async def test_get_user_by_id_success():
    expected = _user_dict(id=1)
    user = _user_obj(**expected)

    class MyService(UserService):
        def __init__(self):
            pass

        async def get_by_id(self, user_id: int) -> User | None:
            return user

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.get("/users/1")
        assert response.status_code == HTTP_200_OK
        assert response.json() == expected


@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    class MyService(UserService):
        def __init__(self):
            pass

        async def get_by_id(self, user_id: int) -> User | None:
            return None

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.get("/users/999")
        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_all_users_success():
    users = [
        _user_obj(**_user_dict(id=1, username="john")),
        _user_obj(
            **_user_dict(
                id=2,
                username="jane",
                email="jane@example.com",
                first_name="Jane",
                last_name="Roe",
            )
        ),
    ]

    class MyService(UserService):
        def __init__(self):
            pass

        async def get_by_filter(
            self, count: int = 10, page: int = 1, **kwargs
        ) -> List[User]:
            return users

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.get("/users")
        assert response.status_code == HTTP_200_OK
        assert response.json() == [
            _user_dict(id=1, username="john"),
            _user_dict(
                id=2,
                username="jane",
                email="jane@example.com",
                first_name="Jane",
                last_name="Roe",
            ),
        ]


@pytest.mark.asyncio
async def test_create_user_success():
    payload = {
        "username": "new_user",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
    }
    created = _user_dict(id=10, **payload)

    class MyService(UserService):
        def __init__(self):
            pass

        async def create(self, data: UserCreate) -> User:
            return _user_obj(**created)

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.post("/users", json=payload)
        assert response.status_code in (HTTP_200_OK, HTTP_201_CREATED)
        assert response.json() == created


@pytest.mark.asyncio
async def test_create_user_conflict_returns_400():
    payload = {
        "username": "dup",
        "email": "dup@example.com",
        "first_name": "Dup",
        "last_name": "User",
    }

    class MyService(UserService):
        def __init__(self):
            pass

        async def create(self, data: UserCreate) -> User:
            raise ValueError("User with this username or email already exists")

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.post("/users", json=payload)
        assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update_user_success():
    updated = _user_dict(
        id=1,
        username="john",
        first_name="Updated",
        email="john@example.com",
        last_name="Doe",
    )

    class MyService(UserService):
        def __init__(self):
            pass

        async def update(self, user_id: int, data: UserUpdate) -> User | None:
            return _user_obj(**updated)

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.put("/users/1", json={"first_name": "Updated"})
        assert response.status_code == HTTP_200_OK
        assert response.json() == updated


@pytest.mark.asyncio
async def test_update_user_not_found():
    class MyService(UserService):
        def __init__(self):
            pass

        async def update(self, user_id: int, data: UserUpdate) -> User | None:
            return None

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.put("/users/999", json={"first_name": "Updated"})
        # Controller wraps not found into 400 Bad Request
        assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_delete_user_success():
    class MyService(UserService):
        def __init__(self):
            pass

        async def delete(
            self, user_id: int
        ) -> None:  # pragma: no cover - just ensure it is called without error
            return None

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: MyService())},
    ) as client:
        response = client.delete("/users/1")
        # Controller returns 204 No Content on successful delete
        assert response.status_code == 204

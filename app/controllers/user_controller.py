from typing import List
from litestar import Controller, get, post, put, delete
from litestar.params import Parameter
from litestar.exceptions import NotFoundException, HTTPException

from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse

class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def fetch_user(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        """Получение пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if user is None:
            raise NotFoundException(detail=f"Пользователь с ID {user_id} не найден")
        return UserResponse.model_validate(user)

    @get()
    async def list_users(
        self,
        user_service: UserService,
        count: int = Parameter(default=10, ge=1),
        page: int = Parameter(default=1, ge=1),
    ) -> List[UserResponse]:
        """Получение списка пользователей с пагинацией"""
        users = await user_service.get_by_filter(count=count, page=page)
        return [UserResponse.model_validate(u) for u in users]

    @post()
    async def add_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """Создание нового пользователя"""
        try:
            user = await user_service.create(data)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {err}")
        return UserResponse.model_validate(user)

    @put("/{user_id:int}")
    async def modify_user(
        self,
        user_service: UserService,
        user_id: int,
        data: UserUpdate,
    ) -> UserResponse:
        """Обновление пользователя"""
        try:
            user = await user_service.update(user_id, data)
            if user is None:
                raise NotFoundException(detail=f"Пользователь с ID {user_id} не найден")
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Ошибка при обновлении пользователя: {err}")
        return UserResponse.model_validate(user)

    @delete("/{user_id:int}")
    async def remove_user(
        self,
        user_service: UserService,
        user_id: int,
    ) -> None:
        """Удаление пользователя"""
        await user_service.delete(user_id)
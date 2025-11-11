from typing import List
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter
from litestar.exceptions import NotFoundException, HTTPException

from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.providers import provide_user_service

class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        """Get user by ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(default=10, ge=1),
        page: int = Parameter(default=1, ge=1),
    ) -> List[UserResponse]:
        """Get all users with pagination"""
        users = await user_service.get_by_filter(count=count, page=page)
        return [UserResponse.model_validate(user) for user in users]

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """Create a new user"""
        try:
            user = await user_service.create(data)
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        data: UserUpdate,
    ) -> UserResponse:
        """Update an existing user"""
        try:
            user = await user_service.update(user_id, data)
            if not user:
                raise NotFoundException(detail=f"User with ID {user_id} not found")
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int,
    ) -> None:
        """Delete a user"""
        await user_service.delete(user_id)
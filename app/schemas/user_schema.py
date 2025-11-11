from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
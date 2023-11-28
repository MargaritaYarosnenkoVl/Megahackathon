import uuid
from typing import Optional, Any
from datetime import datetime
from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Field
from enum import Enum


class RoleName(str, Enum):
    admin = "admin"
    user = "user"
    director = "director"
    editor = "editor"


class Role(BaseModel):
    id: int
    name: RoleName = Field(default="user")

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[int]):
    id: int
    full_name: str | None
    phone_number: str | None
    registred_at: datetime
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str = "user"
    email: EmailStr = "user@example.com"
    password: str = "123456"
    role_id: int = 1
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass

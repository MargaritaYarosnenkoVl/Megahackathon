import uuid
from typing import Optional, Any
from datetime import datetime
from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Field
from enum import Enum


class RoleName(str, Enum):
    user = "user"
    admin = "admin"
    director = "director"
    editor = "editor"


class UserRole(BaseModel):
    id: int
    name: RoleName = Field(default="user")

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[int]):
    id: int = Field(ge=1)
    full_name: str | None
    phone_number: str | None
    registred_at: datetime
    email: EmailStr
    username: str
    role_name: RoleName
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str = "user"
    full_name: str = "Иванов Иван Иванович"
    phone_number: str = "9871234567"
    email: EmailStr = "user@example.com"
    password: str = "123456"
    role_name: RoleName
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str = "user"
    full_name: str = "Иванов Иван Иванович"
    role_name: RoleName
    email: EmailStr = "user@example.com"
    phone_number: str = "9871234567"
    password: str = "123456"
    registred_at: datetime
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        orm_mode = True

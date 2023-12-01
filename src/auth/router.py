from fastapi import APIRouter, Depends
from auth.models import User, Role
from fastapi_users import FastAPIUsers
from typing import List
from auth.manager import get_user_manager
from auth.auth import auth_backend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .schemas import UserRead, UserCreate, UserRole

router = APIRouter(prefix="/auth",
                   tags=["auth"])
fastapi_users = FastAPIUsers[User, int](get_user_manager,
                                        [auth_backend]
                                        )
current_user = fastapi_users.current_user()

user = User.__table__
role = Role.__table__


@router.get("/get_all_roles", response_model=List[UserRole])
async def get_all_roles(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(role).order_by(role.c.id.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}



@router.get("/get_all_users", response_model=List[UserRead])
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).order_by(user.c.id.desc())
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {"status": "error",
                "data": e,
                "details": e}


@router.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@router.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"


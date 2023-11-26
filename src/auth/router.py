from fastapi import APIRouter, Depends
from auth.models import User
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.auth import auth_backend

router = APIRouter(prefix="/auth",
                   tags=["auth"])
fastapi_users = FastAPIUsers[User, int](get_user_manager,
                                        [auth_backend]
                                        )
current_user = fastapi_users.current_user()


@router.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@router.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"

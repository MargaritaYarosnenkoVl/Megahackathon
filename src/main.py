from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastadmin import fastapi_app as admin_app

from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.parse_news.router import router as router_parser


app = FastAPI(
    title="This is ХОРОШО!"
)

app.mount("/admin", admin_app)

fastapi_users = FastAPIUsers[User, int](get_user_manager,
                                        [auth_backend]
                                        )

app.include_router(fastapi_users.get_auth_router(auth_backend),
                   prefix="/auth/jwt",
                   tags=["auth"],
                   )

app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                   prefix="/auth",
                   tags=["auth"]
                   )

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym"


app.include_router(router_parser)
